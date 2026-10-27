## 부록 G — 익스트린식 색인

구현자가 대상으로 삼아 구축하는 합의 결정적 익스트린식들이다(규범적 시그니처이며, 오류/이벤트는
축약했다). 전체 온체인 연산 지도는 On-Chain Flows이다.

### G.1 컴퓨트 채널 — `pallet_compute_channel` (유일한 추론(inference) 디스패치 경로, §12.1)

| 익스트린식 | 오리진(origin) | 효과 | 주요 오류 |
|-----------|--------|--------|-----------|
| `open_channel(miner, model_hash, measured_root, decode_policy_hash, precision, enclave_key, agent_key, sla, escrow, nonce, settlement_class)` | 에이전트 (서명) | 에스크로를 예약한다; 부록 F.3의 `SettlementClass`를 고정한다; 마이너 캘리브레이션 보증 티어를 스냅숏한다; 레지스트리와 대조하여 측정된 루트를 검증한다; 상태 → `Open` | 루트 불일치; 예약 상한 초과; 만료된 리스 |
| `force_open(miner, model_hash, measured_root, decode_policy_hash, precision, agent_key, sla, escrow, nonce)` | 에이전트 (서명) | `SettlementClass::Standard`를 고정한다; 상태 → `PendingAck { ack_deadline }`; 세션 서명 키는 결속되지 않는다 | 예약 상한 초과 |
| `force_ack(channel_id, enclave_key)` | 지명된 마이너 (서명) | 출처 중립적인 세션 서명 키를 결속한다; 마이너 캘리브레이션 보증 티어를 스냅숏한다; 상태 → `Open` | 지명된 마이너가 아님; 윈도 경과 |
| `register_session_evidence(channel_id, slot, commitment, size_bytes:u32)` | 지명된 마이너 (서명) | 자금이 조달된 Open 채널에 한함; R5.3g를 통해 범위가 한정된 Ephemeral DA를 할당한다; 동일한 재시도는 만료를 보존한다; 새 슬롯에 대해서만 SessionEvidenceRegistered를 발생시킨다 | NotAParty; BadState; ZeroToplocCommitment; VerifiedTurnOutOfBounds; SessionEvidenceTooLarge; SessionEvidenceConflict; 레지스트리 오류 |
| `expire_force_open(channel_id)` | 누구나 (서명) | 에스크로를 전액 환불한다; 에스크로가 하한 이상이면 `FailedAcks += 1` | 아직 ack 윈도 이내 |
| `top_up_escrow(channel_id, amount)` | 에이전트 (서명) | 예약 용량 상한을 증액한다(스플라이스 인) | 채널이 `Open` 상태가 아님 |
| `settle(channel_id, final_root, aggregate_gn, claimed_measured_root, agent_receipt_sig, transcript_ref, verified_turns)` | 마이너 (서명); 에이전트가 영수증에 양자 서명한다 | 버전이 지정된 영수증, 명시적으로 버전이 지정된 모든 턴 서명/경로, 서로 구별되는 인덱스, 검사된 집계값, 캘리브레이션/`GnSink`, 측정된 루트, 필수 TOPLOC 기록, 그리고 열린 에스컬레이션이 없음을 검증한다; 예약된 에스크로의 즉시 비공개 지급; 공개 작업 적립 없음 (R11.2b/E.44) | `BadReceiptSignature`; `UnsupportedLeafVersion`; `AggregateGnMismatch`; `TooManySettlementTurns`; `MerklePathTooLong`; `GnTripwireRejected`; 루트/TOPLOC/에스컬레이션 오류 |
| `force_settle(channel_id, final_root, aggregate_gn, claimed_measured_root, agent_receipt_sig, transcript_ref, verified_turns)` | 마이너 또는 에이전트 (서명) | 동일한 영수증/턴/청구 게이트를 검증한다; 2부 요금제 `P`를 계산한다; 챌린지 윈도를 개시한다 | 영수증/턴/루트/청구 오류; `P > E`이면 `TariffExceedsEscrow`로 거부한다(R12.1d) |
| `finalize(channel_id)` | 누구나 (서명) | 챌린지 윈도 이후 `P` → 마이너, `(1−φ)(E−P)` → 에이전트, `φ(E−P)` → `FLOPFoundationAccount`(소각 0, R12.1d)로 지급한다; `P`는 에스크로의 기본 단위(10⁻¹⁸ FLOP)로 표시되며, `channel_base_per_turn = rate_G = 1` 기본 단위이다 | 윈도 미경과; 분쟁 진행 중 |
| `timeout(channel_id)` | 누구나 (서명) | 미이행 → 전액 환불 (`φ=0`) | `max_duration` 미경과 |
| `open_dispute(channel_id, contested_turn)` | 세션 에이전트 또는 활성 검증자 | [`channel_challenger_bond`](#param-channel_challenger_bond)를 잠근다; 정산된 턴 하나를 계쟁하며, 마이너는 `respond_dispute`로 응답한다 | `NoDisputeStanding`; `DisputeTurnNotSettled`; `DisputeExists`; 윈도 경과; 트랜스크립트 이용 불가 |
| `open_bisection_dispute(channel_id, n_turns)` | 세션 에이전트 또는 활성 검증자 | 챌린저 본드를 잠근다; `n_turns`는 정산된 2의 거듭제곱 리프 수(2에서 `MaxSettlementTurns`까지)와 같다; 번들 전체에 대해 중간점 라운드를 개시한다 | `BisectionBadTurnCount`; `DisputeTurnNotSettled`; 자격 및 윈도 오류는 `open_dispute`와 같다 |
| `respond_bisection(channel_id, left_root, right_root)` | 지명된 마이너 (서명) | 두 자식 루트를 공개하며, 그 해시는 해당 구간의 부모 루트와 같아야 한다; 응답 윈도를 리셋한다 | `NotAParty`; `BisectionNotAwaitingResponse`; `BisectionBadChildRoots`; 윈도 경과 |
| `challenge_bisection(channel_id, choose_left)` | 해당 분쟁의 챌린저 | 왼쪽 또는 오른쪽 절반을 고른다; 턴이 하나 남으면 마이너가 `respond_dispute`로 응답한다 | `NotAParty`; `BisectionNotAwaitingChallenge`; `BisectionRoundCap`; 윈도 경과 |
| `respond_dispute(channel_id, leaf_version, turn_index, h_in, h_out, g_n, decode_policy_hash, h_ids, toploc_commitment_hash, miner_recv_ms, miner_done_ms, latency_ms, enclave_sig, merkle_path)` | 마이너 (서명) | 부록 F의 리프 프리이미지를 정확히 하나 선택한다; 서명 + 머클 멤버십을 검증한다 | 지원되지 않는 버전; 잘못된 서명/경로; 윈도 경과 → 사기로 기본 판정 |
| `report_toploc_mismatch(channel_id, evidence)` | 활성 검증자 | 정족수로 판정된 활성화 불일치 → 위조 슬래싱 | 캘리브레이션되지 않은 셀 (페일 클로즈드로 무효) |

### G.2 PoUI 직접 레일 — `pallet_flop_poui` (합성/고스트/캘리브레이션/시뮬레이터, §3.6)

| 익스트린식 | 오리진(origin) | 효과 |
|-----------|--------|--------|
| `submit_stark_batch(proofs, gn_weight, task_hash, latency_ms, model_hash, output_hash)` | 마이너 (서명) | `PendingVerifications`에 기록한다; 재생 방지 `ProcessedTasks[task_hash]` |
| `submit_validator_attestations(bundle)` | 없음 (서명되지 않은 인히런트; `ensure_none`) — 검증자 신원은 익스트린식 오리진이 아니라 번들 내부의 서명으로 인증된다 | 서명 + 활성 검증자 확인 + 튜플 합치 + 정족수를 검증한다; 정족수 달성 시 `report_data`/`output_hash`를 검증하고, `gn_weight`를 적립하며, `OnProofVerified`를 발화한다 |
| `set_validator_attestation_threshold(perbill)` | 루트/거버넌스 | BFT 정족수 비율을 설정한다 |

### G.3 스테이킹, 캘리브레이션, 베스팅, DA, HTLC

| 익스트린식 | 팔레트 | 효과 |
|-----------|--------|--------|
| `register_miner(commission)` / unbond *(commission, `delegate`, `set_commission`은 폐기됨, D-0530)* | `miner_staking` | 용량 비례 요구치(§6.1) 이상의 셀프 스테이크를 본딩한다; 슬래싱 잠금 언본딩 |
| `register` / `rotate` / `un_jail` / `rejoin` / `do_slash` | `validators` | `register`는 `effective_minimum_stake()`를 고정하고 `ValidatorQueue`에 대기시킨다; `rotate`는 `ValidatorQueue`에서 `ActiveValidators`로 승격시키고 방출/해동한다; `un_jail`(활성 상태 감옥(liveness jail)의 경우 `MinJailBlocks` = 3,600 이후)과 `rejoin`(장기 다운타임으로 인한 퇴출의 경우, 셀프 스테이크를 `effective_minimum_stake()`까지 보충)은 `ActiveSetCap` = 1,000 미만인 동안 `ActiveValidators`로 직접 복귀시킨다; 단일 슬래싱 권한 |
| `sponsor_register_miner(miner, amount, commission, reward_policy)` / `sponsor_top_up(position_id, amount)` | `miner_staking`; 스폰서 (서명) | R6.1a; [`sponsored_self_stake_enabled`](#param-sponsored_self_stake_enabled)가 아니면 거부된다(`SponsoredSelfStakeDisabled`). 등록: `register_miner`의 승인 검사, `amount ≥ required_self_stake_for(miner)`, 스폰서의 기존 스테이킹 동결을 초과하는 스폰서 보증 및 인덱스 여유; 자기 스테이크 0과 스폰서에게 동결된 Active 스폰서 포지션을 기록한다; `MinerRegistered{self_stake: 0}` 다음에 `SponsorPositionCreated`를 발생시킨다. 보충은 호출자의 Active 포지션을 늘린다(`SponsorPositionToppedUp`). 해제: `sponsor_unbond` → `sponsor_withdraw`; `deregister_miner`는 마이너가 바쁘지 않은 한 모든 Active 포지션을 언본딩한다. 슬래시 수익 계정은 여기서, 그리고 활성화된 런타임에서는 `sponsor_miner`에서도 스폰서로 거부된다. 활성화된 런타임에서 스폰서는 여기서와 `sponsor_miner`에서 두 스테이킹 팰릿 어디에도 다른 스테이킹 동결을 보유할 수 없으며, 그 경우 스폰서 계정은 `register_miner`, `top_up_self_stake`, `delegate`를 할 수 없다(`SponsorStakeOverlap`). `register_miner`와 이 호출은 이전 등록의 계정 포지션이 인출될 때까지 대기한다(`StaleSponsorPositions`); 운영자는 파이널라이즈된 잠금 해제 이후 이를 인출하고 고아가 된 포지션을 완전히 언본딩할 수 있다. 활성화 스캔으로 인한 격리(`LegacyOverlapCount`)는 모든 후원 적립을 중단시킨다. 오류 `InsufficientSelfStake`, `InvalidSponsorAmount`, `TooManySponsorPositions`, `NotSponsor`, `InvalidSponsorPositionStatus`, `SponsorIsSlashProceedsAccount`, `SponsorStakeOverlap` |
| `sponsor_register_validator(validator, amount, reward_policy)` / `sponsor_top_up(position_id, amount)` | `validators`; 스폰서 (서명) | R6.1a; 동일한 게이트. 등록: `register`의 승인 검사, `amount ≥ effective_minimum_stake()`, 이전 등록에서 남은 활성 후원이 없음(`StaleSponsorPositions`); `register`처럼 대기열에 오른다; `ValidatorRegistered{self_stake: 0}` 다음에 `SponsorPositionCreated`를 발생시킨다. 보충은 마이너와 같다. `deregister`는 모든 Active 포지션을 언본딩한다. 슬래시 수익 계정은 여기서, 그리고 활성화된 런타임에서는 `sponsor_validator`에서도 스폰서로 거부된다. 동일한 단일 스테이킹 동결 규칙이 적용되며, `register`, `rejoin`, `delegate`가 자기 스테이크 경로이다(`SponsorStakeOverlap`). 활성화된 런타임에서 `sponsor_unbond`가 활성 검증자를 유효 최소치 미만으로 떨어뜨리면 그 검증자를 큐로 되돌린다(하한에서는 `MinimumActiveValidators`) |
| `accept_benchmark_burst(...)` / `renew_benchmark_cap(...)` | `hw_calibration` | 스테이크로 뒷받침되는 집계 상한 / 리스 갱신 |
| `claim_vested()` | `airdrop_vesting`; 수혜자 (서명) | 파이널라이즈된 헤드를 사용한다; 기존 그랜트와 `claimed`를 초과하는 양의 잠금 해제 금액을 요구한다; 그랜트 동결을 줄이고 `AirdropClaimed`를 발생시킨다; 오류 `NoGrant`, `NothingToClaim` |
| `record_attested_gpu_inventory(...)` / `record_hardware_fingerprint(...)` | `hw_calibration` | 신원 결속; 변경 시 무효화 |
| `batch_issue_calibration_jobs(...)` | `synthetic_tasks` | 발행자가 선정한 시간 제한 일회성 팩 |
| `create_grant(miner, amount)` | `work_vesting` | 루트 전용; 마이너의 0이 아닌 파이널라이즈된 §7 캘리브레이션 기준선을 요구하고 이를 `B_p`로 스냅숏한다(R8.1) |
| `force_create_grant(miner, amount, pledge_baseline)` | `work_vesting` | 루트 전용; 호출자가 제공한 0이 아닌 `B_p`로 파이널라이즈된 캘리브레이션 기준선 검사를 명시적으로 우회한다(R8.1) |
| `register_miner(model_hash, gpu_model, vram_gb, tee_type)` / `set_measured_root` | `model_registry` | 모델 가용성 + 측정된 dm-verity 루트 |
| DA 등록 / 감사 / `top_up_lease` / `withdraw_lease(commitment)` | `da_registry` | `DataRef` 커밋먼트; 서브 오어 슬래시 감사; 무료 리스 증액; `withdraw_lease`: 게시자 (서명); 기존 `Leased` 블롭, 일치하는 게시자, `pin_count == 0`을 요구하며 `lease_end` 조건은 없다; 블롭을 제거하고(이후 감사는 발행될 수 없다) 예치금 전액을 게시자에게 환불한다; 인출 전에 발행된 감사는 취소하지 않는다(E.47); 오류 `UnknownBlob`, `NotLeased`, `NotPublisher`, `BlobPinned`; `LeaseWithdrawn`, `LeaseDepositRefunded`를 발생시킨다 |
| `create/redeem/refund_htlc`, `create_cross_chain_htlc`, `relay_preimage`, `register_relayer` | `has-station` | HTLC 생명주기(§10); 퍼미션드 릴레이어 |
| 세션 키 / 에이전트 지갑 위임, 상한, 폐기 | `session_keys` / `agent_wallet` | §6.2 위임된 자율성 |

---

### G.4 유료 객체 스토리지(§5.4)

**R5.4p — 인터페이스 고정.** 이들은 논리적 인터페이스이다; E.54는 활성화 전에 범위가 한정된 와이어 타입과 디스패치 인덱스를 **MUST** 고정해야 한다. 모든 호출은
비활성/미지의 프로파일을 **MUST** 거부해야 한다. 이벤트는 비공개 내용이나 키 없이, 영향을 받는
예약/레인/객체 식별자와 회계 변동분을 **MUST** 포함해야 한다.

| 시그니처 | 오리진(origin) | 전제 조건 / 주요 오류 | 이벤트 |
|---|---|---|---|
| `vote_tariff(epoch, tariff)` | 자격 있는 검증자 | 다음 에포크가 아직 시작되지 않음; 용량 선언이 있을 때만 집계됨; 중복 / 자격 없음 | `TariffVoteRecorded` |
| `declare_capacity(epoch, encoded_bytes)` | 자격 있는 검증자 | E.54 본드 프로파일에 따라 사용 가능한 담보; 여러 의무에 걸쳐 재사용되지 않음; 자격 없음 / 담보 부족 | `CapacityDeclared` |
| `open_reservation(reserved_bytes, term, max_cost, nonce)` | 지급자 | 유효한 권한(capabilities), `max_cost` 이내에서 현재 요율 기준 `C_rent`를 충당할 자금, 비어 있는 선언 용량; 권한 없음 / 예산 또는 용량 부족 | `ReservationPending`; 다음 파이널라이즈된 난수에서 프로토콜 배정에 의해 `ReservationActivated`, 또는 에스크로 반환과 함께 `ReservationAborted` |
| `extend_reservation(reservation, additional_term, max_cost)` | 권한 있고 자금을 댄 갱신자 | 자금 조달 에포크의 요율에 대한 새로운 동의, 제공자들의 선언 용량; 종료됨 / 예산 부족 | `ReservationExtended` |
| `transfer_reservation(reservation, new_payer, consent)` | 새 지급자의 서명된 수락을 받은 소유자 | 활성 예약, 대기 중인 이전 없음; 권한 없음 / 청구 대기 중 | `ReservationTransferred`; 조건, 제공자, 책임은 변경되지 않음 |
| `set_memory_head(namespace, key, expected_version, new_object)` | 소유자 또는 범위가 지정된 작성자 | 선택적인 체인 고정 느린 경로; 정확한 이전 버전(체인 고정 또는 정족수 영수증 확보); 오래된 헤드 / 권한 없음 | `MemoryHeadPinned`; 해당 키에 대해 제공자 영수증보다 우선하는 권위를 가짐 |
| `post_checkpoint(epoch, root, counters_commitment)` | 배정된 검증자 | 유예 기간 내 에포크당 제공자별 1회; 중복 / 지연 / 충돌 | `CheckpointPosted`; 유예 기간 후의 지연 또는 누락은 결함 |
| *(프로토콜 동작, 익스트린식 없음)* 에포크별 임대료 지급 | 블록 실행 | 해당 구간에 대해 과거 슬롯 보유자의 감사 및 체크포인트 상태가 수락됨; 챌린지 윈도 경과; 적립되지 않은 기간 위치; 슬롯/트랜치별 `R_sk(b) − R_sk(a)`만; 검사된 산술 | 해당 구간의 보유자에게 `RentReleased`, 교체 이후 포함 |
| `challenge_storage(reservation, generation, evidence)` | 프로파일이 승인한 챌린저; 이중 서명(equivocation)은 누구나 | 객관적 증거: 감사 실패, 활성화 윈도 이후 보관 영수증 누락, 유예 기간 이후 체크포인트 누락, 또는 서로 충돌하는 영수증/체크포인트; 해당 본드/자격; 오래된 배정 / 무효한 증거 | `StorageChallenged`; 프로파일에 결속된 `RepairAssigned` / `StorageFault` / `EquivocationSlashed` |
| `finalize_reservation(reservation)` | 만료되었거나 실패한 예약에 대해 누구나 | 원인에 결속된 파이널라이즈된 종료; 범위가 한정된 청구와 책임이 종결된 후에만; 존속하는 과거 임대료 수급권 정산; 살아 있는 보류 없음; 검사된 슬롯별 환불 `Σ_k B_sk − paid − held`; 청구 대기 중 | `ReservationClosed`, 해당 시 결함 구제, 실패/미제공/몰수된 임대료와 잉여금의 지급자 반환, 프루닝 승인 |
| `set_object_policy(namespace, expected_epoch, policy_commitment)` | 소유자 | 단조 증가하는 파이널라이즈된 에포크와 범위가 한정된 정책; 오래된 에포크 / 권한 없음 | `ObjectPolicyUpdated` |
| `fund_service_lane(reservation, provider, budget, nonce)` | 지급자 | 배정된 제공자, 새 논스, 지갑 총량 상한과 보류된 자금; 권한 없음 / 예산 초과 | `ServiceLaneFunded` |
| `redeem_service(lane, voucher)` | 레인의 제공자, 직접 또는 제공자로서 디스패치하는 인가된 프록시를 통해; 수취인은 고정 | 서명/도메인/범위; 엄격히 증가하는 시퀀스와 감소하지 않는 카운터; 지급액을 초과하고 예산 이내인 고정 요율 기준의 정확한 금액; Closing 상태에서는 서명 시점과 무관하게 알려진 파이널라이즈 높이 ≤ 기한을 요구; 누적 변동분만; 재생 / 과다 청구 / 만료된 청구 / 알 수 없는 클록 | `ServicePaid` |
| `close_service_lane(lane)` / `finalize_service_lane(lane)` | 종료는 지급자; 파이널라이즈는 누구나 | 종료 포함 시점 또는 그보다 이른 예약 종료 시점에 경계 고정; 고정 기한 = 경계 + 청구 윈도; 슬롯과 에스크로 보존; 알려진 파이널라이즈 높이 > 기한인 경우에만 정확히 남은 에스크로를 환불; 권한 없음 / 청구 대기 중 / 알 수 없는 클록 | `ServiceLaneClosing` / `ServiceLaneClosed` |

---
