## 9. 발행과 공급

| 파라미터 | 값 |
|-----------|-------|
| 총 제네시스 공급 | [`genesis_supply`](#param-genesis_supply) = 4,400,000,000 FLOP (VC 프리민트 없음, 경매 없음) — 세 건의 에어드롭: [`genesis_miner_airdrop`](#param-genesis_miner_airdrop) = 1,200,000,000 · [`genesis_validator_airdrop`](#param-genesis_validator_airdrop) = 1,200,000,000 · [`genesis_agent_airdrop`](#param-genesis_agent_airdrop) = 1,200,000,000; 여기에 [`genesis_reserve`](#param-genesis_reserve) = 800,000,000 잔여분(생태계/인센티브이며, 에어드롭이 아니다)이 더해진다 |
| 에라 0 블록 보상 | [`initial_block_reward`](#param-initial_block_reward) = 96 FLOP/블록 (블록당 고정 파라미터; 스케줄에 따라 반감; 상한 없음) |
| 분배 | [`miner_share_ppt`](#param-miner_share_ppt) = 75% 마이너 · [`validator_share_ppt`](#param-validator_share_ppt) = 10% 검증자 · [`agent_share_ppt`](#param-agent_share_ppt) = 10% 에이전트 · [`staker_share_ppt`](#param-staker_share_ppt) = 5% 스테이커 (에라 0: 72 · 9.6 · 9.6 · 4.8 FLOP/블록) |
| 검증자 몫 | 검증자 10% 풀, 스테이크에 비례하여 배분하되 현재 파이널리티 위원회 구성원에게는 [`finality_committee_premium_weight_ppm`](#param-finality_committee_premium_weight_ppm) = 1.1×를 적용한다; 잠금된 스테이크로 자동 복리 적립된다 (검증자 수익의 유동성은 미결 항목 [E.39](#appendix-e--open-specification-items)이다) |
| 에이전트 및 스테이커 레그(leg) | 각 블록 보상의 10% + 5%를 프로토콜 파생 소버린 풀 계정에 발행한다; 분배 정책은 미비준 상태다 ([E.40](#appendix-e--open-specification-items)) |
| Labs/재단 보조금(subsidy) | [`subsidy_per_block_per_recipient`](#param-subsidy_per_block_per_recipient) = 8 + 8 FLOP/블록의 별도 발행(`flop-subsidy`)이며, 5개 보조금 에라 전체에 걸쳐 보상과 함께 반감된다 ([`subsidy_duration_blocks`](#param-subsidy_duration_blocks) = 315,360,000, 약 10년); 총 1,955,232,000 FLOP |
| 첫 반감 | 블록 63,072,001 (730일차) → 48 FLOP/블록 |
| 영구 하한 | 에라 5(블록 315,360,001, 3650일차)부터 [`floor_reward`](#param-floor_reward) = 3 FLOP/블록이 영구히 적용된다 |

### 9.1 요구사항

- **R9.1 — 블록 보상 출처.** 블록당 보상은 `params/flop-protocol-params.yaml`
  ([`initial_block_reward`](#param-initial_block_reward), `RewardInitialPerBlock`으로 미러링)에서 **MUST**
  조달되어야 하며, 하드코딩되거나 초당으로 산정된 것이 **아니어야** 한다. 이 보상은 고정된 반감 스케줄을
  따르며, 그 위에 놓이는 거버넌스 발행 상한의 적용을 **받지 않는다** — 제네시스 보상 *자체가* 그 한계다
  (`emission ≤ 96`).
- **R9.2 — 반감.** 발행은 하한이 설정된 채로 기하급수적으로 **MUST** 반감되어야 한다:
  [`max_halvings`](#param-max_halvings) = 5회 이후 `96 → 48 → 24 → 12 → 6 → 3`이 되고, 그 다음에는
  [`floor_reward`](#param-floor_reward) = 3 FLOP/블록이 영구히 유지된다. 모든 해제는 블록 단위 선형이다
  (클리프 없음). 반감 국면 전체(에라 5 종료, 약 12년차)의 누적 발행량은
  11,920,608,000 FLOP이며, 에라 6 종료 시점(약 14년차)에 `2·R₀·H` = 12,109,824,000 FLOP에 도달한다
  — 이는 **하드 캡이 아니다**; 이후 영구 하한이
  [`floor_annual_emission`](#param-floor_annual_emission) = 94,608,000 FLOP/년을 영구히 추가한다.
- **R9.3 — 보조금(subsidy).** Labs/재단 보조금은 블록 보상 위에 더해지는 — 결코 그 일부가 아닌 — 별도
  발행(`flop-subsidy`)이어야 **MUST** 한다. FLOP Labs와 FLOP 재단 각각은 반감 에라 0에서
  [`subsidy_per_block_per_recipient`](#param-subsidy_per_block_per_recipient) = 8 FLOP/블록을 **MUST**
  수령해야 하며, 그 비율은 블록 보상과 동일한 63,072,000 블록 경계에서 **MUST** 반감되어야 하고
  (수령자당 8 → 4 → 2 → 1 → 0.5) **에라 5부터는 정확히 0**이어야 한다 — 보조금은 보상이 하한에 도달하는
  바로 그 경계에서 종료된다. 에라 4의 0.5 FLOP은 FLOP 단위로는 소수이지만 기본 단위로는 정확하며
  (5 × 10¹⁷), 구현은 이를 절사해서는 **MUST NOT** 안 된다. 지속 기간은
  [`subsidy_duration_blocks`](#param-subsidy_duration_blocks) = 315,360,000 블록(5개 에라, 약 10년)이다;
  총 발행량 = 63,072,000 × (16 + 8 + 4 + 2 + 1) = 1,955,232,000 FLOP.
- **R9.4 — 제네시스.** 제네시스는 워크 퍼스트(work-first)다(VC 프리민트 없음, 경매 없음, 팀 배분 없음).
  [`genesis_supply`](#param-genesis_supply) = 4,400,000,000 FLOP은 정확히 네 개의 제네시스 버킷에만
  **MUST** 배분되어야 하며 그 밖의 어디에도 배분되어서는 안 된다: 세 건의 에어드롭 —
  [`genesis_miner_airdrop`](#param-genesis_miner_airdrop),
  [`genesis_validator_airdrop`](#param-genesis_validator_airdrop),
  [`genesis_agent_airdrop`](#param-genesis_agent_airdrop) (합계 3,600,000,000 FLOP, 각 1,200,000,000) — 그리고 생태계
  리저브 [`genesis_reserve`](#param-genesis_reserve) = 800,000,000 FLOP이며, 이 리저브는 제네시스
  배분이지만 에어드롭은 **아니다**. 이 넷은 `genesis_supply`와 정확히 일치하도록 **MUST** 합산되어야 한다.
  검증자 코호트는 정의상 총 본드 —
  [`validator_min_stake`](#param-validator_min_stake) ×
  [`validator_active_set_cap`](#param-validator_active_set_cap) — 이므로, 제네시스 파라미터를 정할 때
  본드 하한을 바꾸면 이 코호트가, 따라서 `genesis_supply`가 함께 움직인다(D-0440).
- **R9.5 — 위원회 프리미엄.** 검증자 10% 풀은 추론(inference) 할증료나 두 번째 발행으로 증액되어서는
  **MUST NOT** 안 된다. 이 풀은 내부에서
  `stake_i × (1.1 if i ∈ current finality committee else 1.0)` 가중으로 분할되며, 정수 잔돈(dust)은
  결정론적으로 할당되어 지급액 합계가 풀과 정확히 일치한다. 이는 4분할 체계에서도 변하지 않는다: 에이전트
  레그와 스테이커 레그는 **마이너 잔여분에서 깎아낸 것**([`miner_share_ppt`](#param-miner_share_ppt)
  900 → 750 ppt)이지 결코 위에 더한 것이 아니므로,
  [`validator_share_ppt`](#param-validator_share_ppt)는 100 ppt로 유지된다.
- **R9.6 — 트랜잭션 수수료 분배.** 트랜잭션 수수료 수령자 분배는
  [`tx_fee_burn_percent_live`](#param-tx_fee_burn_percent_live) = 10% 소각(`BurnFees`)이어야 **MUST**
  하며, 블록 작성자는 소각되지 않은 잔액의
  [`tx_fee_author_share_percent_live`](#param-tx_fee_author_share_percent_live) = 100%를 수령한다
  (회계상으로는 마이너별 `G_n` 수수료 귀속이 마이너 몫을 분할하기 전까지 800 ppt 마이너 프록시 + 100 ppt
  검증자 몫이 블록 작성자에게 함께 배치된다). 팁은 100% 블록 작성자에게 귀속된다.
  **비준된 목표치**는 마이너 80% / 검증자 10% / 소각 10%이며, 작성자 프록시 회계는 그 잠정적 구현이다.
  전체 분류 체계: [부록 D](#appendix-d--fee--revenue-map).
- **R9.12 — 에이전트 및 스테이커 레그.** [`agent_share_ppt`](#param-agent_share_ppt) = 100 ppt 및
  [`staker_share_ppt`](#param-staker_share_ppt) = 50 ppt 레그는 매 분배 주기마다 두 개의 프로토콜 파생
  소버린 풀 계정(`PalletId`, §9.3 R9.10 형태)에 레그당 하나씩 **MUST** 발행되어야 한다. 어느 풀에서든
  후속 분배는 해당 풀의 분배 정책이 비준되기 전까지 이루어져서는 **MUST NOT** 안 된다
  ([E.40](#appendix-e--open-specification-items)); 풀은 적립되며 발행은 이벤트로 기록된다. 두 레그는
  마이너 몫에서 **MUST** 깎아내야 하며, 그 결과 네 레그의 합은 1000 ppt가 되고 검증자 풀은 변하지 않는다
  (§9.1 R9.5).

### 9.2 서바이벌 거버너 *(기본값 OFF, 거버넌스로 활성화)*

상태 의존적인 공급 측 거버너는 붕괴 임계값 부근에서만 엑소더스 나선을 감쇠시키기 위해 거버넌스에 의해
**MAY** 활성화될 수 있다([`governor_default_enabled`](#param-governor_default_enabled) = false):
**가동률(utilization) 연동 발행 감쇠**(가동률이 낮을 때 마이너 보상을 상향한다; 가동률에 연동하며
**결코 가격에 연동하지 않는다** — 안티 테라;
[`governor_emission_damping_util_floor`](#param-governor_emission_damping_util_floor) /
[`governor_emission_damping_max_boost`](#param-governor_emission_damping_max_boost))와 **동적 소각
스케줄**(에라별 10→15→25%: [`governor_dynamic_burn_tier1`](#param-governor_dynamic_burn_tier1) …
[`tier3`](#param-governor_dynamic_burn_tier3))이다. 730일차의 참여자 수익 절벽(마이너 72 → 36,
검증자 9.6 → 4.8 FLOP/블록)이 첫 번째 스트레스 사례이며, 보조금이 일몰되는 대신 보상과 함께 반감되기
때문에 그 지점에서 블록당 총 발행량은 정확히 절반으로 떨어진다(112 → 56). 이제 총 발행량의 가장 깊은
계단은 3650일차(에라 5)로, 여기서 보상은 영구 하한에 도달하고 보조금은 즉시 종료된다: 7 → 3 FLOP/블록,
4/7 ≈ 57.1% 하락.

**수요 연동 보상(불변식).** PoUI는 지불자 승인 수요 기록, 해당하는 검증 증거, 그리고 정산을 갖춘 작업에
대해서만, 또는 명시적으로 한정된 합성 태스크 부트스트랩 하한에 대해서만 **MUST** 지급해야 한다. 지불자
승인 기록은 프로토콜 수요를 증명하지만, 경제적으로 독립적인 고객의 존재를 증명하지는 않는다. 마이너가
통제하는 지불자는 진짜 추론(inference)을 구매하면서 작업 보상을 추구하는 동시에 그 지불금의 상당 부분을
회수할 수 있다. 이것이 수익성이 있는지는 회수 불가능한 연산, 수수료, 자본, 감사 비용, 보상 및 리베이트
스케줄, 그리고 연합 소유 구조에 달려 있다; 외부 수요 및 워시 수요 모델은
[E.49](#appendix-e--open-specification-items)이다.

### 9.3 제네시스 구성

합의에 결정적인 제네시스 필수 요소들이다(운영 배포 런북 — `GENESIS_AND_DESUDO_RUNBOOK` — 은 별도로
유지된다).

- **R9.7 — 제네시스 시점의 공급.** 총 제네시스 공급은
  [`genesis_supply`](#param-genesis_supply) = 4,400,000,000 FLOP(18 소수 자릿수)이어야 **MUST** 하며,
  제네시스 시점에는 **오직** 세 에어드롭 코호트와 §9.1 R9.4의 생태계 리저브만이 이를 보유한다 — VC
  프리민트 없음, 경매 없음, 팀 배분 없음. 제네시스에서는 어떠한 블록 보상도 발행되지 않았다; 에라 0
  발행은 블록 생산과 함께 시작된다.
- **R9.8 — 체인 스펙 상수.** 제네시스에 고정되며 합의에서 관측 가능한 값들이다: **18 소수 자릿수**(기본
  단위 10⁻¹⁸ FLOP); `TOKEN_SYMBOL`을 통한 사용자 대면 티커(메인넷 브랜딩 단계, §14.2);
  **SS58 프리픽스**(`SS58Prefix`; 메인넷은 `SS58_ZKV_PREFIX`, 데브넷은 별도의 프리픽스 — §6.5); 1초 블록
  타임; 최소 잔고(existential deposit) 0.01 FLOP.
- **R9.9 — 초기 권한자.** 제네시스 체인 스펙은 초기 검증자 집합과 그 세션 키(BABE + AlephBFT)를 **MUST**
  시드해야 하며, 이로써 §2 파이널리티 위원회를 부트스트랩한다. 제네시스 이후 이 집합은 **오직** §15
  로테이션을 통해서만 변화한다; `ActiveValidators`에 진입하는 다른 경로는 없다.
- **R9.10 — 프로토콜 소버린 계정.** **FLOP 재단**과 **FLOP Labs** 계정은 프로토콜 파생 계정이다
  (`PalletId` 소버린 계정; 메인넷에서는 각각을 멀티시그에 **SHOULD** 결속해야 한다). 이들은 Labs/재단
  보조금(§9.1 R9.3), 슬래싱 수익과 위임 손실 워터폴(§11.3), 그리고 실패한 세션 페널티 `φ`(§12.1d)에
  대해 제네시스에서 정의된 수령처/싱크이며 — 결코 마이너 수익이 아니다.
- **R9.11 — 부트스트랩 오리진(origin)과 de-sudo(단방향).** 제네시스에서 Root는 `pallet_sudo`(§14.1,
  인덱스 50)가 보유한다 — 데브넷에서는 공개 개발 키, 메인넷에서는 멀티시그다. **de-sudo 핸드오프**가
  `pallet_sudo`를 무력화하고 제거하며 `RawOrigin::Root`를 `protocol_upgrade` 트랙으로 라우팅하기
  전까지(§14.1) 거버넌스는 유일한 Root 권한이 **아니다**. 프로덕션 런타임은 핸드오프 이후 Sudo 키나
  비거버넌스 Root 경로를 노출해서는 **MUST NOT** 안 된다. 임의의 거버넌스 승인 `set_code`는 이러한
  가드를 대체할 수 있다; 따라서 이 주장은 승인된 런타임 코드에 한정된다(§14.1, E.50).

### 근거 및 출처 *(비규범적)*

출처: `D-0440`(검증자 본드 305,505 → 1,200,000, 이에 따라 검증자 코호트
305,505,000 → 1,200,000,000, 풀 3,500,000,000 → 4,400,000,000; D-0438의 풀과 D-0435의 본드를
대체하며, 발행은 그대로 둔다), `D-0438`(제네시스 풀 2,483,460,000 → 3,500,000,000, 네 코호트를 재분할한다;
D-0421/D-0435의 풀 규모를 대체하며, 발행은 그대로 둔다), `D-0436`(5회 반감, 3 FLOP
하한, 5개 에라 보조금 — D-0421의 6회차 반감
조항을 대체하고 D-0435의 보조금 스케줄을 수정한다), `D-0435`(4분할, 반감하는 보조금), `D-0421`
(워크 퍼스트 제네시스),
`D-0408`(검증자 분배), `D-0410`(서바이벌 거버너). 균형 상태의 부트스트랩(연산 비용 이하로 유용한 추론(inference)을 보조하는 토큰 시뇨리지 —
Duplexia 체제): Pass et al., *Economics of PoUW*, arXiv:2606.06700, FLOP의 듀플렉스 오버헤드
`δ ≈ low single-digit %`(Pearl의 cuPOW 약 10% 기준치 미만, arXiv:2606.04819)는
`Duplexia.subsidy_below_cost`로 기계 검증되었다. 근거 자료:
halving-exodus-boundary-conditions.md,
fee-design.md, miner-validator-economics.md,
agent-token-economics.md,
f2-exodus-threat-model.md,
pouw-landscape-2026.md,
gonka-cocoon-deep-dive.md,
demand-bound-useful-work-certificates.md. 수요/가치 리스크 증거 검토:
[prepublication-evidence.md](research/prepublication-evidence.md). 보조금 및 참여자 경제성에 관한
주장은 E.8, E.35, E.38–E.40, E.49의 외부 수요, 분배, 담보 가치, 동시 노출 입력값에 여전히 조건부다.
출처 명확화: `D-0501`. 전체 모델:
Tokenomics Specification. 형식 명세:
`tokenomics-supply.qnt`,
`FlopSpecs.lean`,
`FlopSpecs/HalvingBoundary.lean`. 상태:
[부록 H](#appendix-h--conformance--implementation-status-matrix).

---
