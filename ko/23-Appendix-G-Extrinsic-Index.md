## 부록 G — 익스트린식 색인

구현자가 대상으로 삼아 구축하는 합의 결정적 익스트린식들이다(규범적 시그니처이며, 오류/이벤트는
축약했다). 전체 온체인 연산 지도는 On-Chain Flows이다.

### G.1 컴퓨트 채널 — `pallet_compute_channel` (유일한 추론(inference) 디스패치 경로, §12.1)

| 익스트린식 | 오리진(origin) | 효과 | 주요 오류 |
|-----------|--------|--------|-----------|
| `open_channel(miner, model_hash, measured_root, decode_policy_hash, precision, enclave_key, agent_key, sla, escrow, nonce, settlement_class)` | 에이전트 (서명) | 에스크로를 예약한다; 레지스트리와 대조하여 측정된 루트를 검증한다; 상태 → `Open` | 루트 불일치; 예약 상한 초과; 만료된 리스 |
| `force_open(miner, model_hash, measured_root, decode_policy_hash, precision, agent_key, sla, escrow, nonce)` | 에이전트 (서명) | 상태 → `PendingAck { ack_deadline }`; 인클레이브 키는 결속되지 않는다 | 예약 상한 초과 |
| `force_ack(channel_id, enclave_key)` | 지명된 마이너 (서명) | 인클레이브 키를 결속한다; 상태 → `Open` | 지명된 마이너가 아님; 윈도 경과 |
| `expire_force_open(channel_id)` | 누구나 (서명) | 에스크로를 전액 환불한다; 에스크로가 하한 이상이면 `FailedAcks += 1` | 아직 ack 윈도 이내 |
| `top_up_escrow(channel_id, amount)` | 에이전트 (서명) | 예약 용량 상한을 증액한다(스플라이스 인) | 채널이 `Open` 상태가 아님 |
| `settle(channel_id, final_root, aggregate_gn, claimed_measured_root, agent_receipt_sig, transcript_ref, verified_turns)` | 마이너 (서명); 에이전트가 영수증에 양자 서명한다 | 버전이 지정된 영수증, 명시적으로 버전이 지정된 모든 턴 서명/경로, 서로 구별되는 인덱스, 검사된 집계값, 캘리브레이션/`GnSink`, 측정된 루트, 필수 TOPLOC 기록, 그리고 열린 에스컬레이션이 없음을 검증한다; 예약된 에스크로의 즉시 지급 + 청구된 `G_n` 적립 (E.44) | `BadReceiptSignature`; `UnsupportedLeafVersion`; `AggregateGnMismatch`; `TooManySettlementTurns`; `MerklePathTooLong`; `GnTripwireRejected`; 루트/TOPLOC/에스컬레이션 오류 |
| `force_settle(channel_id, final_root, aggregate_gn, claimed_measured_root, agent_receipt_sig, transcript_ref, verified_turns)` | 마이너 또는 에이전트 (서명) | 동일한 영수증/턴/청구 게이트를 검증한다; 2부 요금제 `P`를 계산한다; 챌린지 윈도를 개시한다 | 영수증/턴/루트/청구 오류; `P > E`이면 `TariffExceedsEscrow`로 거부한다(R12.1d) |
| `finalize(channel_id)` | 누구나 (서명) | 챌린지 윈도 이후 `P` → 마이너, `(1−φ)(E−P)` → 에이전트, `φ(E−P)` → 소각/재단으로 지급한다; `P`는 에스크로의 기본 단위(10⁻¹⁸ FLOP)로 표시되며, `channel_base_per_turn = rate_G = 1` 기본 단위이다 | 윈도 미경과; 분쟁 진행 중 |
| `timeout(channel_id)` | 누구나 (서명) | 미이행 → 전액 환불 (`φ=0`) | `max_duration` 미경과 |
| `open_dispute(channel_id, turn_index, bond)` | 세션 에이전트 또는 활성 검증자 | [`channel_challenger_bond`](#param-channel_challenger_bond)를 잠근다; 이분 탐색을 개시한다 | 자격 없음; 채널이 분쟁 대상이 아님 |
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
| `register_miner(commission)` / unbond | `miner_staking` | 용량 비례 요구치(§6.1) 이상을 본딩한다; 슬래싱 잠금 언본딩 |
| `register` / `rotate` / `do_slash` | `validators` | 셀프 스테이크 등록 → 큐; 스테이크 순서에 따른 로테이션; 단일 슬래싱 권한 |
| `accept_benchmark_burst(...)` / `renew_benchmark_cap(...)` | `hw_calibration` | 스테이크로 뒷받침되는 집계 상한 / 리스 갱신 |
| `record_attested_gpu_inventory(...)` / `record_hardware_fingerprint(...)` | `hw_calibration` | 신원 결속; 변경 시 무효화 |
| `batch_issue_calibration_jobs(...)` | `synthetic_tasks` | 발행자가 선정한 시간 제한 일회성 팩 |
| `register_miner(model_hash, gpu_model, vram_gb, tee_type)` / `set_measured_root` | `model_registry` | 모델 가용성 + 측정된 dm-verity 루트 |
| DA 등록 / 감사 / `top_up_lease` | `da_registry` | `DataRef` 커밋먼트; 서브 오어 슬래시 감사; 무료 리스 증액 |
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
| *(프로토콜 동작, 익스트린식 없음)* 에포크별 임대료 지급 | 블록 실행 | 해당 에포크에 대해 제공자의 감사 및 체크포인트 상태가 수락됨; 챌린지 윈도 경과; 누적 변동분만 | `RentReleased` |
| `challenge_storage(reservation, generation, evidence)` | 프로파일이 승인한 챌린저; 이중 서명(equivocation)은 누구나 | 객관적 증거: 감사 실패, 활성화 윈도 이후 보관 영수증 누락, 유예 기간 이후 체크포인트 누락, 또는 서로 충돌하는 영수증/체크포인트; 해당 본드/자격; 오래된 배정 / 무효한 증거 | `StorageChallenged`; 프로파일에 결속된 `RepairAssigned` / `StorageFault` / `EquivocationSlashed` |
| `finalize_reservation(reservation)` | 만료되었거나 실패한 예약에 대해 누구나 | 원인에 결속된 파이널라이즈된 종료; 범위가 한정된 청구와 책임이 종결된 후에만; 청구 대기 중 | `ReservationClosed`, 해당 시 결함 구제, 잉여금 반환 및 프루닝 승인 |
| `set_object_policy(namespace, expected_epoch, policy_commitment)` | 소유자 | 단조 증가하는 파이널라이즈된 에포크와 범위가 한정된 정책; 오래된 에포크 / 권한 없음 | `ObjectPolicyUpdated` |
| `fund_service_lane(reservation, provider, budget, nonce)` | 지급자 | 배정된 제공자, 새 논스, 지갑 총량 상한과 보류된 자금; 권한 없음 / 예산 초과 | `ServiceLaneFunded` |
| `redeem_service(lane, voucher)` | 유효한 서명 바우처를 가진 누구나; 수취인은 고정 | 서명/도메인/범위/카운터/예산 및 종료 윈도 유효성; 최대 누적 변동분까지; 재생 / 과다 청구 / 만료된 청구 | `ServicePaid` |
| `close_service_lane(lane)` / `finalize_service_lane(lane)` | 종료는 지급자; 파이널라이즈는 누구나 | 새 승인 중단; 바우처 청구 기한 이후에만 환불; 권한 없음 / 청구 대기 중 | `ServiceLaneClosing` / `ServiceLaneClosed` |

---
