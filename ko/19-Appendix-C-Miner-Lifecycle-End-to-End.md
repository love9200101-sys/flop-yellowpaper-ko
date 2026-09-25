## 부록 C — 마이너 생명주기(엔드 투 엔드)

정직한 경로를 따라간 실무 예시다(정보 제공용이며, 규범적 규칙은 §4–§8, §12이다). 운영자
단계: `docs/onboarding/miner.md`.

| 단계 | 마이너가 하는 일 | 관장 § |
|-------|---------------------|-------------|
| C.1 온보딩 | 스테이크 본딩, 하드웨어 캘리브레이션, 모델 가용성 등록 | §6.1, §7 |
| C.2 서비스 개시 | 모델을 광고한다; 에이전트가 오프체인에서 마이너를 선택한다 | §12 |
| C.3 수립 | 세션 개설 (`open_channel` / `force_open` → `force_ack`) | §12.1 |
| C.4 서빙 | 턴 스트리밍; 턴별 서명 + 에이전트 공동 서명 | §12.1 |
| C.5 청구 | 최종 루트 + 집계 `G_n` + 마지막 상호 영수증 게시 | §12.1 |
| C.6 종료 | `settle` / `force_settle` → `finalize` / `timeout` / 분쟁 | §12.1 |
| C.7 연장 | `top_up_escrow`; 지속 기간 한정; 마이너 간 체이닝 | §12.1 |

**C.1 온보딩.** `miner_staking::register_miner(commission)`을 통해 용량 비례 요구치(§6.1) 이상을
본딩한다; 언본딩은 세션/분쟁/감사 중 하나라도 열려 있는 동안 슬래싱 잠금 상태가 된다. §7의 시간 제한
벤치마크를 완료한다(SOFT: 인벤토리 상한 없음; HARD: 어테스테이션된 `(SKU,count)`의 합계 상한으로 한정).
활성화 전에 용량 스테이크를 예치한다; 워커는 새로운 카나리로부터 7일 상한을 갱신한다. 제공하는 각 모델을
`model_registry::register_miner(...)`로 등록하고, 측정된 dm-verity 루트를 결속한다
(`set_measured_root`; §3.3).

**C.2 서비스 개시.** 세션은 에이전트가 개시하며 1:1이다; 에이전트는 오프체인에서 마이너를 선택하고
(`model_registry::find_best_miners`) 채널을 개설한다. 온체인 탐색/평판은 향후 과제이며, 체인은 오프체인
라우터를 위한 평판 신호(`FailedAcks`)를 발행한다.

**C.3 수립.** 협조적 경로: RA-TLS 핸드셰이크가 인클레이브를 어테스테이션한 뒤, 에이전트가
`open_channel(miner, model_hash, measured_root, decode_policy_hash, precision, enclave_key, agent_key, sla, escrow, nonce, settlement_class)`를
호출한다; 에스크로가 예약되며 이것이 **곧** 가격이다. 퍼미션리스 경로: `force_open(...)`은 채널을
`PendingAck { ack_deadline = now + AckWindow }` 상태로 둔다; 지명된 마이너는 `force_ack(channel_id,
enclave_key)`로 수락한다; 그렇지 않으면 `expire_force_open`이 전액을 환불하며, 에스크로가
[`min_force_open_escrow_for_failed_ack`](#param-min_force_open_escrow_for_failed_ack) 이상인 경우에만
`FailedAcks`를 기록한다.

**C.4 서빙.** 매 턴은 오직 부록 F.3에서만 정의되는 서명된 트랜스크립트 리프 해시와 진행 중인 머클 누산기를
사용한다; V3는 `ChannelDecodePolicies` 마커를 지닌 채널을 위한 현행 TOPLOC 결속 형식이다. 에이전트는
출력을 수락하기 전에 리프와 누적 루트를 검증하고 부록 F.3의 턴별 에이전트 확인(ack)으로 해당 턴에
맞서명한다. 에이전트가 공동 서명을 거부하면 마이너는 마지막 상호 영수증을 기준으로
일방적으로 정산한다. 재어테스테이션은 `k` 턴마다 반복된다(§12.1h).

**C.5 청구.** 종료 시 마이너는 최종 루트, 집계 `G_n`, 마지막 상호 영수증을
`settle`/`force_settle`에 게시한다; 적립은 `GnSink::validate_session_gn`(타당성 한계
— §11.2) 직후 즉시 이루어지며, 이어서 `payout_settlement`이 집계 `G_n`을 `WorkVesting`/`BlockRewards`
누산기에 투입한다. settle 경로는 측정된 루트를 레지스트리와 대조하여 재확인한다.

**C.6 종료.** `settle`(양측 서명 → 즉시 지급, 미사용분 환불 없음); `force_settle` →
`finalize`(챌린지 윈도 7일 ≤ `W`); `timeout`(미이행 → 전액 환불, `φ=0`); 실패/조기
종료(3자 분할, §12.1d); 분쟁(사기에 한함 — 이분 탐색; 무응답 → 사기 판정).

**C.7 연장/체이닝.** `top_up_escrow`는 예약 용량 상한을 증액한다. `D_max`/`n_max`를 넘어서면 새로운
핸드셰이크로 재개설한다. 세션 중 크래시 복구는 영수증으로 방어된다(공동 서명된 최고 누적 영수증까지만
지급하며, 미확인 테일은 `MaxUnackedGn`으로 한정된다); 복구는 클라이언트가 보유한 컨텍스트 재생과 함께
다른 마이너에서 새로 재개설하는 방식이다.

**근거 자료:** miner-capacity-stake-calibration.md,
r2-payment-channel-sessions.md.

---
