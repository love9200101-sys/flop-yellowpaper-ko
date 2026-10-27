## 9. 발행과 공급

| 파라미터 | 값 |
|-----------|-------|
| 총 제네시스 공급 | [`genesis_supply`](#param-genesis_supply) = 4,400,000,000 FLOP (VC 프리민트 없음, 경매 없음) — 세 건의 에어드롭: [`genesis_miner_airdrop`](#param-genesis_miner_airdrop) = 1,200,000,000 · [`genesis_validator_airdrop`](#param-genesis_validator_airdrop) = 1,200,000,000 · [`genesis_agent_airdrop`](#param-genesis_agent_airdrop) = 1,200,000,000; 여기에 [`genesis_reserve`](#param-genesis_reserve) = 800,000,000 잔여분(생태계/인센티브 — 오프체인 익스플로러 추천 리더보드, 정기 추천 추첨, 빌더 프로그램, 보안 취약점 공개 보상의 재원이며, 에어드롭이 아니다)이 더해진다 |
| 에라 0 블록 보상 | [`initial_block_reward`](#param-initial_block_reward) = 96 FLOP/블록 (블록당 고정 파라미터; 스케줄에 따라 반감; 상한 없음) |
| 분배 | [`miner_share_ppt`](#param-miner_share_ppt) = 75% 마이너 · [`validator_share_ppt`](#param-validator_share_ppt) = 10% 검증자 · [`agent_share_ppt`](#param-agent_share_ppt) = 10% 에이전트 · [`staker_share_ppt`](#param-staker_share_ppt) = 5% 스테이커 (에라 0: 72 · 9.6 · 9.6 · 4.8 FLOP/블록) |
| 검증자 몫 | 검증자 10% 풀, 스테이크에 비례하여 배분하되 현재 파이널리티 위원회 구성원에게는 [`finality_committee_premium_weight_ppm`](#param-finality_committee_premium_weight_ppm) = 1.1×를 적용한다; 발행 즉시 유동이다 (§9.1 R9.13) |
| 에이전트 및 스테이커 레그(leg) | 10% 에이전트 레그 + 5% 기간 잠금형 커뮤니티 스테이킹 풀(7개 잠금 기간 티어, 슬래싱 위험 없음; 운영자 위임 없음)을 프로토콜 파생 소버린 풀 계정에 발행한다; 이후 지급 메커니즘은 [E.40](#appendix-e--open-specification-items)에 있다 |
| Labs/재단 보조금(subsidy) | [`subsidy_per_block_per_recipient`](#param-subsidy_per_block_per_recipient) = 8 + 8 FLOP/블록의 별도 발행(`flop-subsidy`)이며, 5개 보조금 에라 전체에 걸쳐 보상과 함께 반감된다 ([`subsidy_duration_blocks`](#param-subsidy_duration_blocks) = 315,360,000, 약 10년); 총 1,955,231,984 FLOP (블록 `1..=315,359,999`, 블록 0은 R9.7에 따라 보상 없음) |
| 첫 반감 | 블록 63,072,000 (730일차) → 48 FLOP/블록 |
| 영구 하한 | 에라 5(블록 315,360,000, 3650일차)부터 [`floor_reward`](#param-floor_reward) = 3 FLOP/블록이 영구히 적용된다 |

### 9.1 요구사항

- **R9.1 — 블록 보상 출처.** 블록당 보상은 `params/flop-protocol-params.yaml`
  ([`initial_block_reward`](#param-initial_block_reward), `RewardInitialPerBlock`으로 미러링)에서 **MUST**
  조달되어야 하며, 하드코딩되거나 초당으로 산정된 것이 **아니어야** 한다. 이 보상은 고정된 반감 스케줄을
  따르며, 그 위에 놓이는 거버넌스 발행 상한의 적용을 **받지 않는다** — 제네시스 보상 *자체가* 그 한계다
  (`emission ≤ 96`).
- **R9.2 — 반감.** 발행은 블록 인덱스 기반 에라 경계 `era(b) = ⌊b / H⌋`
  (`H` = [`halving_interval_blocks`](#param-halving_interval_blocks) = 63,072,000)에서 하한이 설정된 채로
  기하급수적으로 **MUST** 반감되어야 한다: [`max_halvings`](#param-max_halvings) = 5회 이후
  `96 → 48 → 24 → 12 → 6 → 3`이 되고, 그 다음에는 [`floor_reward`](#param-floor_reward) = 3 FLOP/블록이
  영구히 유지된다. 에라 경계에 걸친 분배 기간 `(last, now]`은 생산된 각 블록 `b ∈ (last, now]`을 `era(b)`의
  비율로 **MUST** 산정해야 한다. 제네시스 블록 `0`은 보상이 없으므로(R9.7), 에라 `0`은 보상받는 블록
  `H − 1` = 63,071,999개(`1..=63,071,999`)로 이루어지고, 각 에라 `e ≥ 1`은 보상받는 블록 `H` = 63,072,000개
  (`e·H..=(e+1)·H − 1`)로 이루어진다. 블록 보상은 발행 즉시 유동이다
  (R9.13); 에어드롭 그랜트는 §8.2 R8.7에 따라 언락된다. 반감 국면 전체(에라 5 종료, 블록 `378,431,999`,
  약 12년차)의 누적 발행량은 `R₀·H·63/32 − R₀` = 11,920,607,904 FLOP이며(보상 없는 블록 0을 빼기 전의
  에라당 `H` 블록 폐쇄형으로는 `2·R₀·H·63/64 =
  11,920,608,000`), 에라 6 종료 시점(블록 `441,503,999`, 약 14년차)에 `2·R₀·H − R₀` = 12,109,823,904 FLOP
  (블록 0을 빼기 전에는 `2·R₀·H = 12,109,824,000`)에 도달한다 — 이는 **하드 캡이 아니다**; 이후 영구 하한이
  [`floor_annual_emission`](#param-floor_annual_emission) = 94,608,000 FLOP/년을 영구히 추가한다.
- **R9.3 — 보조금(subsidy).** Labs/재단 보조금은 블록 보상 위에 더해지는 — 결코 그 일부가 아닌 — 별도
  발행(`flop-subsidy`)이어야 **MUST** 한다. FLOP Labs와 FLOP 재단 각각은 반감 에라 0에서
  [`subsidy_per_block_per_recipient`](#param-subsidy_per_block_per_recipient) = 8 FLOP/블록을 **MUST**
  수령해야 하며, 그 비율은 블록 보상과 동일한 63,072,000 블록 경계에서 **MUST** 반감되어야 하고
  (`era(b) = ⌊b / H⌋`: 수령자당 8 → 4 → 2 → 1 → 0.5) **에라 5부터는 정확히 0**이어야 한다 — 보조금은 보상이
  하한에 도달하는 바로 그 경계(`b = 315,360,000`)에서 종료된다. 에라 4의 0.5 FLOP은 FLOP 단위로는 소수이지만
  기본 단위로는 정확하며 (5 × 10¹⁷), 구현은 이를 절사해서는 **MUST NOT** 안 된다. 배타적 일몰 블록은
  [`subsidy_duration_blocks`](#param-subsidy_duration_blocks) = 315,360,000(`5·H`, 약 10년)이다; 제네시스
  블록 `0`은 보상이 없으므로(R9.7) 보조금은 생산 블록 `315,359,999`개(에라 0에서 `63,071,999`개, 에라 1–4
  각각에서 `63,072,000`개)에 발행되며, 따라서 총 발행량 =
  `63,072,000 × (16 + 8 + 4 + 2 + 1) − 16` = 1,955,231,984 FLOP이다(보상 없는 블록 0을 빼기 전의 에라당 `H`
  블록 폐쇄형으로는 `1,955,232,000`).
- **R9.4 — 제네시스.** 제네시스는 워크 퍼스트(work-first)다(VC 프리민트 없음, 경매 없음, 팀 배분 없음).
  [`genesis_supply`](#param-genesis_supply) = 4,400,000,000 FLOP은 정확히 네 개의 제네시스 버킷에만
  **MUST** 배분되어야 하며 그 밖의 어디에도 배분되어서는 안 된다: 세 건의 에어드롭 —
  [`genesis_miner_airdrop`](#param-genesis_miner_airdrop),
  [`genesis_validator_airdrop`](#param-genesis_validator_airdrop),
  [`genesis_agent_airdrop`](#param-genesis_agent_airdrop) (합계 3,600,000,000 FLOP, 각 1,200,000,000) — 그리고 생태계
  리저브 [`genesis_reserve`](#param-genesis_reserve) = 800,000,000 FLOP이며, 이 리저브는 제네시스
  배분이지만 에어드롭은 **아니다**(오프체인 익스플로러 추천 리더보드 지급, 정기 추천 추첨, 빌더 프로그램, 보안 취약점
  공개 보상에 충당되며, 온체인 추천 커미션을 대체한다). 이 넷은 `genesis_supply`와 정확히 일치하도록 **MUST** 합산되어야 한다.
  검증자 코호트는 정의상 총 본드 —
  [`validator_min_stake`](#param-validator_min_stake) ×
  [`validator_active_set_cap`](#param-validator_active_set_cap) — 이므로, 제네시스 파라미터를 정할 때
  본드 하한을 바꾸면 이 코호트가, 따라서 `genesis_supply`가 함께 움직인다(D-0440).
- **R9.5 — 위원회 프리미엄.** 블록 보상 검증자 10% 풀
  ([`validator_share_ppt`](#param-validator_share_ppt) = 100 ppt)은 발행 할증료나 두 번째 발행으로
  증액되어서는 **MUST NOT** 안 된다. (별도의 15% 추론(inference) 수수료 검증자 몫은 익스트린식 정산 수수료
  레그이며, 블록 보상의 발행이나 희석이 아니다; [부록 D](#appendix-d--fee--revenue-map) 참조.)
  이 풀은 내부에서 `stake_i × (1.1 if i ∈ current finality committee else 1.0)` 가중으로 분할되며, 정수
  잔돈(dust)은 결정론적으로 할당되어 지급액 합계가 풀과 정확히 일치한다. 이는 4분할 체계에서도 변하지
  않는다: 에이전트 레그와 스테이커 레그는 **마이너 잔여분에서 깎아낸 것**
  ([`miner_share_ppt`](#param-miner_share_ppt) 900 → 750 ppt)이지 결코 위에 더한 것이 아니므로,
  `validator_share_ppt`는 100 ppt로 유지된다.
- **R9.6 — 트랜잭션 수수료 분배.** 프로토콜 전반의 수수료 라우팅은 소각 없이 **MUST** 운영되어야 한다:
  [`tx_fee_burn_percent_live`](#param-tx_fee_burn_percent_live) = 0% 소각(`BurnFees`)이며, 블록 작성자는
  트랜잭션 포함 수수료(기본 + 인코딩 길이 + 조정 웨이트 수수료)의
  [`tx_fee_author_share_percent_live`](#param-tx_fee_author_share_percent_live) = 100%와 팁의 100%를 수령한다.
  추론 정산 수수료도 마찬가지로 소각이 0%이다(§12.1 R12.1a에 따라 마이너 85% / 검증자 15%로 분할).
  전체 분류 체계: [부록 D](#appendix-d--fee--revenue-map).
- **R9.12 — 에이전트 및 스테이커 레그.** [`agent_share_ppt`](#param-agent_share_ppt) = 100 ppt 및
  [`staker_share_ppt`](#param-staker_share_ppt) = 50 ppt 레그는 매 분배 주기마다 두 개의 프로토콜 파생
  소버린 풀 계정(`PalletId`, §9.3 R9.10 형태)에 레그당 하나씩 **MUST** 발행되어야 한다.
  [`staker_share_ppt`](#param-staker_share_ppt) = 50 ppt(5%) 레그는 슬래싱 위험 없이, 검증자나 마이너 중개자
  없이, 7개의 잠금 기간 티어에 걸친 기간 잠금형 커뮤니티 스테이킹 풀의 재원이 된다. 어느 풀에서든
  후속 분배는 해당 풀의 분배 정책이 비준되기 전까지 이루어져서는 **MUST NOT** 안 된다
  ([E.40](#appendix-e--open-specification-items)); 풀은 적립되며 발행은 이벤트로 기록된다. 두 레그는
  마이너 몫에서 **MUST** 깎아내야 하며, 그 결과 네 레그의 합은 1000 ppt가 되고 검증자 풀은 변하지 않는다
  (§9.1 R9.5).
- **R9.13 — 보상 유동성.** 모든 블록 보상의 마이너 및 검증자 레그와 Labs/재단 보조금은 발행 즉시 **MUST**
  유동이어야 한다: 프로토콜은 이를 스테이크로 자동 복리화하거나, 강제 스테이킹하거나, 베스팅하거나, 그 밖의 방식으로
  잠가서는 **MUST NOT** 안 된다. 에이전트 레그는 R9.12에 따라 소버린 풀에 적립되며, 그 적립은 잠금이 아니다;
  분배 정책이 비준되면([E.40](#appendix-e--open-specification-items)) 모든 에이전트 레그 지급은 지급 즉시
  **MUST** 유동이어야 한다. 유동 잔액을 스테이크로 본딩하는 것은 여전히 보유자의 선택이다. 스테이커 레그의
  유동성은 E.40에 남아 있다.

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
  **SS58 프리픽스** `SS58Prefix` = 42, 범용 Substrate 프리픽스로 모든 FLOP 네트워크에서 동일하다(§6.5);
  1초 블록 타임; 최소 잔고(existential deposit) 0.01 FLOP.
- **R9.9 — 초기 권한자.** 제네시스 체인 스펙은 초기 검증자 집합과 그 세션 키(BABE + AlephBFT)를 **MUST**
  시드해야 하며, 이로써 §2 파이널리티 위원회를 부트스트랩한다. 제네시스 이후 `ActiveValidators`는 **오직**
  `ValidatorQueue`로부터의 §15 로테이션 승격과, 감금되었거나 장기 다운타임으로 퇴출된 검증자의 `un_jail` /
  `rejoin` 복귀를 통해서만 [`validator_active_set_cap`](#param-validator_active_set_cap) 이내에서 검증자를
  받아들인다(§15.5, §15.7).
- **R9.10 — 프로토콜 소버린 계정.** **FLOP 재단**과 **FLOP Labs** 계정은 프로토콜 파생 계정이다
  (`PalletId` 소버린 계정; 메인넷에서는 각각을 멀티시그에 **SHOULD** 결속해야 한다). 이들은 Labs/재단
  보조금(§9.1 R9.3), 모든 결함 경로에 걸친 슬래싱 수익의 100%(§11.3, 소각 0), 그리고 실패한 세션 페널티
  `φ`(§12.1d)에 대해 제네시스에서 정의된 수령처/싱크이며 — 결코 마이너 수익이 아니다.
- **R9.11 — 부트스트랩 오리진(origin)과 de-sudo(단방향).** 제네시스에서 Root는 `pallet_sudo`(§14.1,
  인덱스 50)가 보유한다 — 데브넷에서는 공개 개발 키, 메인넷에서는 멀티시그다. **de-sudo 핸드오프**가
  `pallet_sudo`를 무력화하고 제거하며 `RawOrigin::Root`를 `protocol_upgrade` 트랙으로 라우팅하기
  전까지(§14.1) 거버넌스는 유일한 Root 권한이 **아니다**. 프로덕션 런타임은 핸드오프 이후 Sudo 키나
  비거버넌스 Root 경로를 노출해서는 **MUST NOT** 안 된다. 임의의 거버넌스 승인 `set_code`는 이러한
  가드를 대체할 수 있다; 따라서 이 주장은 승인된 런타임 코드에 한정된다(§14.1, E.50).

### 근거 및 출처 *(비규범적)*

출처: `D-0513`(모든 네트워크에서 SS58 프리픽스 42, R9.8), `D-0440`(검증자 본드 305,505 → 1,200,000, 이에 따라 검증자 코호트
305,505,000 → 1,200,000,000, 풀 3,500,000,000 → 4,400,000,000; D-0438의 풀과 D-0435의 본드를
대체하며, 발행은 그대로 둔다), `D-0438`(제네시스 풀 2,483,460,000 → 3,500,000,000, 네 코호트를 재분할한다;
D-0421/D-0435의 풀 규모를 대체하며, 발행은 그대로 둔다), `D-0436`(5회 반감, 3 FLOP
하한, 5개 에라 보조금 — D-0421의 6회차 반감
조항을 대체하고 D-0435의 보조금 스케줄을 수정한다), `D-0435`(4분할, 반감하는 보조금), `D-0421`
(워크 퍼스트 제네시스),
`D-0408`(검증자 분배), `D-0410`(서바이벌 거버너), `D-0529`(프로토콜 전반 소각 0: 트랜잭션 수수료 소각 0%,
추론 수수료 소각 0%, 슬래시의 100%를 `FLOPFoundationAccount`로; 잠정적 10% 소각과 80/10/10 목표를 대체),
`D-0530`(운영자 자기 스테이크 전용; 7개 티어에 걸친 5% 기간 잠금형 커뮤니티 스테이킹 풀), `D-0531`(`genesis_reserve`를
재원으로 하는 오프체인 익스플로러 추천 리더보드와 정기 추천 추첨; 워크북의 6–10% 온체인 추천 커미션을 대체). 균형 상태의 부트스트랩(연산 비용 이하로 유용한 추론(inference)을 보조하는 토큰 시뇨리지 —
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
