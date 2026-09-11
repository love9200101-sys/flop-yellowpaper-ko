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
| `force_settle(channel_id, final_root, aggregate_gn, claimed_measured_root, agent_receipt_sig, transcript_ref, verified_turns)` | 마이너 또는 에이전트 (서명) | 동일한 영수증/턴/청구 게이트를 검증한다; 챌린지 윈도를 개시한다; 2부 요금제 `P` | 영수증/턴/루트/청구 오류 |
| `finalize(channel_id)` | 누구나 (서명) | 챌린지 윈도 이후 `P` → 마이너, `(1−φ)(E−P)` → 에이전트, `φ(E−P)` → 소각/재단으로 지급한다 | 윈도 미경과; 분쟁 진행 중 |
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
