## 12. 시장 행위자로서의 에이전트 — 세션과 정산

FLOP의 컴퓨트 소비자는 **자율적이고 전략적인 AI 에이전트**이다. 본 절은 이들이 사용하는 정산
경로(어테스트된 스트리밍 세션), 이들을 제한하는 신원별 상한, 그리고 이들이 만들어 내는 시장 행위자 위협
등급을 규정한다.

### 12.1 세션 — 어테스트된 스트리밍과 집계 정산

추론(inference)은 **`pallet_compute_channel`**을 통해 정산되며, 이것이 유일한 추론 디스패치 경로이다(이전의
태스크별 4개 익스트린식 RPC 레일은 제거되었다). 협력적 해피 패스에는 `open_channel`과 `settle`이라는 두
개의 주요 생애주기 포함(inclusion)이 있다. 일방적 종료, 증거 공표, 에스컬레이션, 분쟁은 호출을 추가한다.
정산 바이트 수와 검증 비용은 일정하지 않다. `settle`은 제출된 턴, 서명, 머클 경로를 실어 나르고 검증하며,
쌍별 중복 스캔은 제출된 턴 수에 대해 2차(quadratic)이다. 추론 스트림은 오프체인에 남지만, 처리량은
인코딩된 바이트 수, 런타임 웨이트, 증거 호출, 위원회 부하, GPU 용량에 의존한다
([E.46](#appendix-e--open-specification-items)).

- **R12.1a — 계량 환불이 아닌 예약 용량.** `open_channel` 시점의 에스크로가 **곧** 예약 용량에 대한
  지불이다. `settle`은 예약된 금액 전액을 지급한다(**정산 수수료 없음**). 미사용분은 **MUST NOT**
  환불되어서는 안 된다. 유일한 환불 경로는 미이행 타임아웃, 인용된 사기 분쟁, 또는 실패하거나 조기
  종료된 세션이다(R12.1d).
- **R12.1b — 트랜스크립트.** 인클레이브는(또는 SOFT 경로에서는 마이너 세션 키가) 각 턴의 32 B
  트랜스크립트 리프 해시를 진행 중인 머클 누산기에 **MUST** 서명해 넣어야 한다.
  [부록 F.3](#f3-session-transcript-compute-channel-121)이 유일한 리프 정의이자 허용 버전 규칙이다.
  V3는 `ChannelDecodePolicies` 마커를 가진 채널을 위한 현행 TOPLOC 바인딩 형식이다. 고유성은
  `channel_id ‖ turn_index`이며, 재생 방지는 단조 증가 카운터이다. 에이전트는 출력을 수락하기 전에 서명된
  리프와 누적 루트를 **MUST** 검증하고, 리프 해시와 타이밍 입력에 대한 부록 F.3의 턴별 에이전트 확인
  응답(ack)으로 해당 턴에 역서명해야 한다. 정산에는 별도의 에이전트 영수증 v1이 실리며, 이는
  `channel_id`, `final_root`, `aggregate_gn`, `payable`을 부록 F.3의 정의 그대로 바인딩한다. `settle`은
  최종 루트와 집계 `G_n`을 게시한다. 이 서명들은 영수증과 합계에 대한 합의를 증명할 뿐, 출력이 주장된 실행으로부터
  도출되었음을 증명하지는 않는다. 현행 협력적 경로는 공동 서명된 클레임을 즉시 지급하고 적립한다. 따라서
  공개 보상 자격과 사후 사기 회수는 [E.44](#appendix-e--open-specification-items)에서 미결로 남는다.
- **R12.1c — 티어별 모델 바인딩.** HARD 티어의 `open_channel`과 `settle`은 증명의 측정된 dm-verity 루트를
  레지스트리와 대조하여 **MUST** 검증해야 한다(`ModelRegistryQuery::verify_measured_root`). 정산 시점의
  잘못된 루트는 **MUST** 거부되어야 한다. SOFT 프로파일에는 TEE가 측정한 루트가 없으며, 그 모델/디코드
  바인딩, 증거 술어, 가치 상한, 분쟁 경로는 [E.33](#appendix-e--open-specification-items)이다.
- **R12.1d — 실패/조기 종료 분배.** 일방적 `force_settle → finalize` 경로에서 마이너는 2부 요율
  `P = BasePerTurn·n + rate_G·G_claimed`를 가져간다(`n`개 턴에 걸친 정액 턴당 지불에, 주장된 기준
  작업량을 지불 단위로 환산한 값을 더한 것). `P`는 에스크로의 기본 단위(10⁻¹⁸ FLOP)로 표시되며,
  [`channel_base_per_turn`](#param-channel_base_per_turn)과 `rate_G`는 각각 기본 단위 1이다. `G_n`은
  R4.4의 정수 단위 전체 기준 GFLOP 값이며, 이 요율은 요금 가격일 뿐 하나의 `G_n`이 1 FLOP 기본 단위와
  같다는 주장이 아니다. `force_settle`은 `P > E`이면 `TariffExceedsEscrow`로 **MUST** 거부해야 하며,
  `P`를 **MUST NOT** 잘라 내거나(clamp) 음수 지급 레그를 만들어서는 안 된다
  (`pallets/pallets/compute-channel/src/lib.rs::{turn_tariff_pay,verified_work_from_turns}`). 그 밖의 경우
  에이전트는 `(1−φ)·(E−P)`를 환불받으며, 페널티 `φ·(E−P)`
  ([`refund_penalty_phi_percent`](#param-refund_penalty_phi_percent) = 20%)는 **MUST** 소각되거나
  재단으로 라우팅되어야 한다 — 결코 마이너에게 가서는 안 된다. 마이너 과실에 의한 미이행은 `φ = 0`을
  사용한다(전액 환불). 보존: `P + (1−φ)(E−P) + φ(E−P) = E`. 이 경로의 호출자 제한과 요율 크기는
  E.24이다.
- **R12.1e — 초과 사용.** 중단(abort) 또는 제자리 `top_up_escrow`(Lightning의 splice-in)로 처리한다. 집계
  `G_n` 누산기는 이미 상한 없이 증가하며, 올라가는 것은 에스크로 상한뿐이다.
- **R12.1f — 분쟁(사기에 한함).** 낙관적 정산에 트랜스크립트 루트에 대한 이분 탐색을 결합한다. 챌린지는
  단일 쟁점 턴에서 해결된다(서명 + 머클 멤버십 검사).
  [`channel_dispute_response_window_blocks`](#param-channel_dispute_response_window_blocks) 이내에
  응답이 없으면 **MUST** 사기 판정으로 기본 처리되어야 하며 → `miner-slashing`의 위조 경로를 통한 슬래싱과
  에이전트 환불로 이어진다. 분쟁은 **프로토콜 사기만**(잘못된 측정 루트, 트랜스크립트 대비 부풀려진
  `G_n`, 위조된 서명, 미이행) 다루며, **출력 품질은 결코 다루지 않는다.** 챌린지 윈도우
  ([`channel_dispute_window_blocks`](#param-channel_dispute_window_blocks) = 7 d)는 DA 보존 기간
  `W`(14 d) 이하로 **MUST** 유지되어야 한다. **제기 자격**은 세션 에이전트(자신의 채널에 한함)와 임의의
  활성 검증자(모든 채널)에게 있다. 임의의 공개 챌린저는 본드 잠금 이전에 **MUST** 거부되어야 한다.
- **R12.1g — 파이널리티 정지 복구.** 기한은 `hp_consensus::FinalizedPrefix`를 **MUST** 읽어야 하며,
  경제적 기한은 파이널리티가 정지한 동안 **MUST** 동결되어야 한다. 자금은 파이널라이즈되지 않은 최선
  헤드로부터 **MUST NOT** 방출되어서는 안 된다. 복구는 AlephBFT 파이널리티의 회복 또는 §13.0a에 따라
  명시적으로 의결된 체크포인트 절차이다. 미해결 채널은 그러한 복구가 파이널라이즈된 프리픽스를 확립할
  때까지 동결 상태로 남는다.
- **R12.1h — 세션 길이와 재어테스테이션.** 신뢰는 `open_channel`에서 한 번 어테스트된 세션 인클레이브
  키로 이전된다. 채널은 최대 지속 시간 `D_max` / 최대 턴 수 `n_max`로 피해 범위를 **MUST** 제한해야 하며
  (`channel_max_settlement_turns`는 번들을 1,024로 제한한다), `k ≤ min(Bond / v_turn, T_tcb / t_turn)`을
  만족하는 `k`턴마다 **SHOULD** 재어테스트해야 한다.

**용량 처분.** 세션 제어의 블록당 트랜잭션 수, 초당 파이널라이즈된 생애주기 수, 포함/파이널리티 지연
목표는 규정하지 않는다. D-0502는 이전의 96/128 어드미션 수치와 48/64 생애주기 수치의 철회를 제안하는데, 이 수치가
직렬화 크기, 부과 웨이트, 상태 실행, 경합 트래픽, 서빙 부하, 네트워크 파이널리티가 아니라 호출 수로부터
도출되었기 때문이다. 어드미션은 여전히 런타임의 바이트, 2차원 웨이트, 상태, 유효성 게이트의 적용을 받는다.
향후 프로파일은 용량을 주장하기 전에 혼잡 상황에서 측정된 정산/분쟁 여유를 **MUST** 확보하고 E.46을
충족해야 한다.

### 12.2 신원별 용량 예약

- **R12.2.** 세션의 신원별 동시 진행 예약 상한은 open/force_open에서 **MUST** 강제되어야 한다. 기본값
  [`max_active_reservations_base`](#param-max_active_reservations_base)에 에스크로된
  [`escrow_per_reservation_slot`](#param-escrow_per_reservation_slot)당 슬롯 1개를 더한 값이며,
  settle/expire/timeout/fraud 시 해제된다. 블록당 작업량은 합의의 `max_gn_weight`(페이로드당
  ≤ 1 PFLOP)로 제한된다. 고가치/피해 범위 기준의 감사 강제는
  [`high_value_gn_threshold`](#param-high_value_gn_threshold)와
  [`audit_quantum_gn`](#param-audit_quantum_gn)을 사용한다.

### 12.3 시장 행위자 위협 등급

자율성은 대상/벡터 모델(§3.1, §2.4, §6.2) 중 어느 것도 포괄하지 못하는 위협 표면을 만든다. 즉 **암묵적
알고리즘 담합**(RL 입찰 에이전트가 의사소통 없이 초경쟁적 가격을 학습한다), 컴퓨트 사재기/매점, 워시/시빌
입찰, 어테스테이션을 악용한 가격 책정, 컴퓨트에 대한 MEV, 예약 그리핑이다. FLOP의 비대칭성은 이렇다.
TEE로 본드된 마이너는 시빌에 강한 *공급*인 반면 경량 에이전트는 시빌에 약한 *수요*이므로, §2.4의 시빌
비용은 수요 측으로 **MUST** 확장되어야 한다(등록된
[`agent_identity_min_stake`](#param-agent_identity_min_stake) + 예약 = 신원 수에 선형인 자본 하한). 현행
레지스트리는 그 최소액을 예치/잠금할 뿐 소각하거나 슬래싱하지 않으므로, 이 하한은 회수 불가능한 신원 비용이
아니라 자본 노출이다.

- **R12.3.** 담합 대응은 개인을 처벌하기보다(증명 가능한 고의가 없다) 메커니즘을 **MUST** 교란해야
  한다(경매 재무작위화, 그리드 조대화, 합성 수요 주입). 모니터링 게이지(입찰 분산 붕괴, 보유/유통 비율,
  이용률→희소성)가 탐지기와 §9.2의 거버너를 모두 구동한다.

### 12.4 암호학적 공격자 모델

본 명세의 모든 증명은 **고전적 PPT 공격자**를 가정한다(`Crypto.lean`은 기호적 Dolev–Yao 모델이다). 이는
양자 내성이 **없다**. 확장 가능한 양자 공격자는 sr25519/ed25519/secp256k1을 깨뜨리고(Shor) SHA-256 프리이미지
보안을 절반으로 낮춘다(Grover). 포스트 양자 마이그레이션은 PQ 프리미티브가 로드맵에 오를 때까지 **범위
밖**이다. 그 경계는 명시적이다(`crypto.quantum_adversary`, trusted/todo).

### 근거 및 출처 *(비규범적)*

출처: `D-0403`(용량 예약 세션), `D-0422`(환불 가능한 실패 세션), `D-0424`
(분쟁 제기 자격), `D-0427`(철회된 처리량 목표), `D-0430`(성능 저하 상태 행렬), `D-0501`
(검증·파이널리티·단위·클레임 범위 명확화), `D-0502`(용량 처분), `D-0511`
(정본 세션 트랜스크립트 및 영수증 정의). 위협은
OWASP Agentic Top-10 (2026) + ATFAA/STRIDE + MITRE ATLAS를 기준으로 프레이밍한다. 통제된 반복 경매 증거에
따르면 LLM 입찰자는 소규모 시장에서 초경쟁적 결과를 산출하며 입찰자 수가 늘어남에 따라 경쟁 쪽으로
회귀한다([Tolety 2025](https://arxiv.org/abs/2511.21802)). 이는 R12.3을 경험적으로 뒷받침하지만
형식적 억지 정리의 가정은 아니다. 근거 자료:
agent-market-threat-and-compute-economics.md,
agent-swarm-collusion-design.md (입찰 분산 + 가격 수준 탐지기, 메커니즘 교란, 재현 가능한 ABM),
r2-payment-channel-sessions.md,
session-matching-orderbook-vs-agent-select.md,
session-migration-semantics.md,
f1-f2-store-of-compute-and-network-survival.md,
compute-spot-market-formation.md,
frcr-methodology-v0.md,
triz-ifr-agent-market-ideas.md (C-TRIZ 패스: 시스템 IFR,
미해결 모순 원장, 검증/발견/공정성 클러스터),
proposal-capacity-reservation-units.md (CRU —
본드된 선도 컴퓨트, D-0434로 의결됨. 구현은 선도 일자 채널로 한다),
term-curve-methodology-v0.md (관측 기반 CRU 선도
커브: 종료 시점의 본드된 정산만, 1d/7d/30d 버킷, 공표 하한 아래에서의 수량 가중 중앙값 — 현물 FRCR와는
결코 혼합하지 않는다),
dispute-window-rightsizing.md (7 d → 약 1 d 적정화
분석, 보류됨),
agent-demand-discovery-mechanisms.md (에이전트 수요
루프: 유형화된 수요, 유계 현물 증명, 영수증 전파, 단계적 CRU 약정). 에이전트 보안 클러스터:
security-across-domains.md,
agent-security.md,
agent-specific-security.md. 형식 명세:
`DemandSideSybil.lean`,
`ChannelPayoutLiveness.lean`,
`FlopSpecs/Sessions.lean`,
`formal-specs/channel/channel-settlement.qnt`. `ChannelPayoutLiveness::escape_safe`는 이전의
최선 헤드 탈출을 모델링하며 D-0501 이후 R12.1g의 증거(witness)가 아니다. 파이널리티 안전한 대체물에는
새로운 증거가 필요하다. `DemandSideSybil.lean`은 자본과 인센티브를 분리한다. `postedCapital`은 노출이고,
`postedCapital_ge_card_mul_floor`는 신원 수에 선형인 자본 한계만을 증명하며, `individual_deterred_iff`는
억지를 위해 명시적인 회수 불가능 비용과 상실되는 계속 가치를 요구한다. yellowpaper#58은 이 구분을 현행
하한에 적용한다. yellowpaper#30과 yellowpaper#34에 보고된 거래소별 관찰은 규칙이 아니라 검증되지 않은 설계
입력이다. 도착 분산(도착 간격의 변동계수)과, 워시 쌍 계수(pair-counting)가 놓치는 타이밍/구조 신호가 후보
게이지이다. 출시된 `turn_ack_message`(`sdk/typescript/src/compute-channel/transcript.ts`와
`sdk/rust-compute-channel/src/transcript.rs`)에는 도메인 태그나 버전 바이트가 없다. 트랜스크립트 리프와
마찬가지로 이는 `channel_id ‖ turn_index` 바인딩에 의존하며, 어느 쪽 프리이미지를 바꾸는 것도 여기서는 범위
밖이다. 검토 증거:
[prepublication-evidence.md](research/prepublication-evidence.md). 상태:
[부록 H](#appendix-h--conformance--implementation-status-matrix).

---
