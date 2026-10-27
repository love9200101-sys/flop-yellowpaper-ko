## 15. 검증자 — 온보딩, 의무, 선출, 로테이션

검증자는 스테이크된 보안 기반이다: 각 검증자는 블록을 작성(BABE)하고, 파이널라이즈(AlephBFT)하며, 마이너의
증명을 어테스테이션(§3.6)하고, 체커 판정을 판결(§3.5)하며, 소버린 DA 계층을 호스팅한다(§5.3).
팔레트 `pallet_validators`; 위원회 게이트 `hp_consensus::select_committee`.

### 15.1 역할

검증자는 합의를 보호하고, 그 역할의 일부로서 BFT 쿼럼을 통해 마이너의 어테스테이션과 체커 판정을 검증하고
공동 서명한다. 검증자 기능은 **MUST NOT** 추론(inference) 실행, PoUI 증명 생산, 또는 GPU나 TEE 소유를
요구해서는 안 된다: 위원회 적격성은 검증 라이브니스(§15.4)이며, 재실행은 체커 의무(§3.5)이다. 검증자는
마이너가 아니다 — 검증자 계정은 **MAY** 마이너로도 등록할 수 있으나, 마이너 활동은 검증자 적격성을
부여하지 않는다.

### 15.2 온보딩 *(규범적)*

등록은 자체 서명되며 스테이크 하한 이상에서는 무허가(permissionless)이다. `register`는 정확히
`effective_minimum_stake()`만큼을 자기 스테이크로 동결하고 검증자를 `ValidatorQueue`에 배치하며, `ActiveValidators`에
직접 배치하지 **않는다** — 승격은 로테이션(§15.5)을 통해서만 이루어진다.

| 요구사항 | 규칙 |
|-------------|------|
| 자기 스테이크 | `≥ effective_minimum_stake() = max(MinimumValidatorStake, ValueCoupledStakeFloor)`; 기준선 `MinimumValidatorStake`는 [`validator_min_stake`](#param-validator_min_stake) = 1,200,000 FLOP에서 시작하여, `n mod 31,536,000 = 0`(`365 × 86,400` 블록)인 모든 `n > 0`에서 `on_initialize(n)`을 통해 정수 내림 나눗셈 `⌊old × 109 / 100⌋`([`validator_growth_numerator`](#param-validator_growth_numerator) / [`validator_growth_denominator`](#param-validator_growth_denominator) = 연 +9%)으로 매년 복리 증가하되, 현재 `total_issuance`의 1%로 상한이 정해진다(`min(⌊old × 109 / 100⌋, ⌊0.01 × total_issuance⌋)`); `force_set_minimum_stake`와 `set_value_coupled_floor`도 동일한 `total_issuance`의 1% 상한을 강제한다 |
| 자기 스테이크 비율 | 운영자 스테이크는 **자기 스테이크 전용**이다(제3자 위임 금지; 레거시 [`MinSelfStakeRatio`](#param-validator_min_self_stake_ratio_percent) ≥ 20%는 E.32 후원 보증이 활성화된 경우에만 적용) |
| 엔티티별 슬롯 | ≤ 5(`MaxSlotsPerEntity`) |
| 블랙리스트 미등재 | 사기로 블랙리스트된 계정은 **MUST NOT** 재등록해서는 안 된다 |
| 검증 라이브니스(위원회) | 마지막으로 수락된 검증 의무(R15.4c; `LastVerifiedWork`)가 [`WorkRecencyWindow`](#param-validator_work_recency_window_blocks) = 86,400 blk(24 h) 이내; 그렇지 않으면 활성 상태이지만 PoUI 위원회에서는 제외 |

검증자와 마이너 스테이크는 자기 스테이크 전용이다(§6.1); 제3자 위임(레거시
[`max_delegators_per_miner`](#param-max_delegators_per_miner)급 한계와 운영자 수수료(commission))은
폐기되었다.

레거시 또는 테스트넷 후원 보증(E.32)이 런타임에서 활성화된 경우, `MinSelfStakeRatio`(20%)는 승인되는 보증을
기록된 자기 스테이크의 4배로 한정한다. 등록은 정확히 유효 최소치만 본딩하므로 잉여 가용 잔액은 이 한도를 늘리지
않으며, 승인 검사는 슬래시가 자기 스테이크를 줄인 이후에는 그 비율을 유지하지 않는다(부록 H).

[`sponsored_self_stake_enabled`](#param-sponsored_self_stake_enabled)가 성립하는 경우, 활성 후원 원금도
큐 승격과 `rejoin` 시점의 자기 스테이크 하한에 산입되며(R6.1a), 스폰서는 잔액이 전혀 없는 검증자를 등록할 수
있다. 네이티브 위임은 여전히 운영자 소유 스테이크만 산입하므로, 전액 후원된 검증자는 위임을 전혀 받지 않는다.

### 15.3 의무와 자원 집약도

| 의무 | 비용 | 강제 수단 |
|------|------|-------------|
| BABE 블록 작성 | 경량 CPU; 지연 민감 가십 | 보상 + Liveness 슬래시(V1) |
| AlephBFT 파이널리티 투표 | 경량 CPU; BFT 투표 가십 O(committee) | 보상 지분 + Equivocation 슬래시(V2) |
| 검증자 어테스테이션(TEE 인용 검증 → 공동 서명) | DCAP/dstack 검증(경량 CPU + 어테스테이션 컬래터럴(collateral) 페치) | 쿼럼 2/3(§3.6); 선택적 어테스테이션 **[GAP]** O3 |
| 프로토콜 DA 저장 및 서빙(§5.3) | Reed–Solomon 레이트 ½(`R=6`, k=3+3); GB 규모 대역폭 | 서빙 아니면 슬래시(serve-or-slash) 감사; 보상 지분으로 재원 조달, **바이트당 수수료 없음** |
| 회수 가능성 / 고스트 태스크 감사 | 경량(정답이 알려진 방식) | 보유 결합(V3/V10) |
| 검증 의무 — 어테스테이션, 쿼럼 공동 서명, 감사 응답(위원회 라이브니스, R15.4c) | 경량 CPU | `WorkRecencyWindow` 내에 수락된 의무가 없으면 위원회에서 탈락 |
| 샘플링 재실행(TOPLOC 프리필 재생) | **검증자 의무 아님** — 체커 레인(R3.5d) | 검증자는 판정을 검증하고 공동 서명 |
| 분쟁 판결 / 포함 | 경량 | 검열 **[GAP]** V6 |

유일하게 무거운 부분은 DA 저장/서빙이다; 어떤 검증자 의무도 GPU나 TEE를 요구하지 않는다. 프로덕션 검증자는
**SHOULD** 다음 참조 프로파일을 프로비저닝해야 한다: SMT를 끈 ≥3.4 GHz 물리 코어 8개, 32 GB ECC RAM, 4 TB 엔터프라이즈 NVMe(체인 상태 및 §5.3
보존 기간 하의 DA 보관(custody)), 1 Gbps 대칭 무제한(unmetered) 링크 — AlephBFT급 노드 참조 사양에 스토리지를
더한 것이다.

배치는 개별 장비가 아니라 집합 수준의 문제이다. R2.3은 비잔틴 **의석**을 세므로,
다음 장애 도메인 규칙이 프로덕션 검증자에게 적용된다 — 기계당 세션 키 하나, 공유 키 페일오버 금지, 그리고 어떤 호스팅 ASN, 대도시권,
운영 그룹도 실현된 위원회 크기에서 `3f < n`(R2.3)을 깨뜨리는 비잔틴 의석 수 — 100석 위원회에 대해서는 34 —
만큼의 적격 검증자를 보유하지 않을 것. 의석은 결코 신원 수를 넘지 않기 때문이다. 신원 수와 스테이크에 대한
더 엄격한 도메인당 10 % 상한이 D-0507에서 제안되어 있다(보류 중).

### 15.4 선출 — PoUI로 게이팅된 위원회

- **R15.4a.** 파이널리티 위원회는 **MUST** `ActiveValidators`를 `effective_minimum_stake()` **그리고** 최근
  수락된 검증 의무(R15.4c; 스테이크 **그리고** 검증 라이브니스 — §2.3 하위 증명 1 및 3)를 충족하는
  검증자로 필터링한 뒤, **BABE-VRF** 시드로부터 [`finality_committee_size`](#param-finality_committee_size) =
  100명의 서로 다른 구성원을 **스테이크 가중 비복원 추출**로 무작위 샘플링하여 구성되어야 한다
  (`hp_consensus::sample_committee_weighted`). `pallet_aleph`는 매 세션 이 위원회를 스냅숏하고
  (`AlephEpochBlocks` = 900 블록; 프로덕션 BABE 에포크당 세션 4개) `authorities()`를 `finality-aleph`에
  노출한다. 선출 술어는 샘플링 시점의 활성 집합, 스테이크, 최근성을 사용한다; 저장된 위원회의 수명 동안
  그 입력들이 변하지 않고 유지된다고 주장하지는 않는다.
- **R15.4b.** 샘플링 시드는 **MUST** BABE-VRF 에포크 무작위성(에포크 동안 고정, 한 에포크 이전 값)이어야
  하며, 로테이션별로 도메인 분리되어야 한다. 이는 현재 블록 작성자의 영향을 지연시키고 제한하지만, 그
  자체로 비편향성을 증명하지는 않는다. 시드 영향 및 반복 추출 분석은 E.42이다.
- **R15.4c — 검증 라이브니스.** 검증자의 최근성 신호(`LastVerifiedWork`)는 **MUST** 온체인에서 **수락된**
  검증 의무에 의해서만 갱신되어야 한다: (a) 수락된 검증자 어테스테이션 번들의 서명자가 되는 것(R3.6b);
  (b) 수락된 TOPLOC 불일치 또는 에스컬레이션 해제 쿼럼의 서명자가 되는 것(R3.5d, §12.1); (c) 수락된 DA
  회수 가능성 감사 응답(R5.3b); (d) 검증자에 의한 수락된 분쟁 개시(R12.1f); (e) 프로토콜이 발행한
  **정답이 알려진 검증 챌린지**에 대한 정답 — §8.1 고스트 태스크 패턴을 검증에 적용한 것으로, 체인이
  이미 기대 판정을 보유한 VRF 선택 픽스처(어테스테이션 번들 또는 프로토콜이 시드한 라이브니스 블롭의 DA
  개방)이다. 수락된 번들 또는 쿼럼의 모든 서명자는 **MUST** 크레딧되어야 한다. 증명자 크레딧(`OnProofVerified`)은
  **MUST NOT** 이를 갱신해서는 안 된다. 이 신호는 `WorkRecencyWindow` = 86,400 블록 이내이면 최근으로
  간주된다. (a)–(d)는 트래픽이 있을 때만 존재하므로, 프로토콜은 **MUST** 특권 오리진이 아닌 블록
  초기화에서 모든 활성 검증자에게 윈도우당 최소 한 번의 챌린지 (e)를 발행해야 하며, 그 응답 기한은 해당
  검증자의 현재 최근성이 만료되기 전에 도래해야 한다. 이로써 조용한 체인이나 새 체인에서 정직한 검증자가
  시효 만료로 탈락하는 일이 없다. 게이트 배선은 E.52이다.

적격 풀의 신원이 100개 미만이면, 선출은 **MUST** 적합성을 주장하기 전에 E.42에서 비준된 최소 안전 크기
및 부트스트랩 프로파일을 따라야 한다. `N=100` 포획 한계는 더 작은 실현 위원회에는 적용되지 않으며, 유급
작업만으로는 정직한 합의 행동이 입증되지 않는다.

복합 성능 점수 = 40% uptime + 30% block_rate + 20% accuracy + 10% latency
([`performance_score_weights`](#param-performance_score_weights)); 이는 로테이션 하한의 입력이다.

비준 대기 중(v0.5 결정 기록): [D-0508](decisions/v0.5.md#d-0508--rotation-on-underperformance-floor-based-ejection-and-on-chain-performance-signal)은
네 구성요소를 온체인에서 관측 가능한 신호로 재정의하고 root 오리진 점수 오라클을 폐지한다.
[D-0509](decisions/v0.5.md#d-0509--committee-session-cadence-aligned-to-the-babe-epoch)는
900블록 위원회 세션을 BABE 에포크에 맞추게 된다.

### 15.5 로테이션과 집합 크기

로테이션은 `on_initialize`에서 매
[`validator_rotation_interval_blocks`](#param-validator_rotation_interval_blocks)(~30 d)마다 실행되며, 수동
`rotate`도 있다.

- **R15.5.** 로테이션은 활성 집합의 하위에서 최대 [`validators_to_eject`](#param-validators_to_eject) = 50명을
  **MUST** 방출해야 하며 — 이는
  [`validator_rotation_churn_percent`](#param-validator_rotation_churn_percent) = 10%(올림)로 한정되고,
  최소 [`validator_min_active_validators`](#param-validator_min_active_validators) = 4개의 활성 의석을 보존하도록
  절단된다(`deregister`, `jail`, 퇴출도 마찬가지로 하한 이하로의 제거를 **MUST** 거부해야 하며, 하한에서의 입증된
  결함 슬래시는 스테이크를 **MUST** 몰수하고(R9.10에 따라 재단으로 이전) 즉시 블랙리스트에 올리되, 로테이션이 집합을
  대체하거나 축소할 수 있을 때까지 의석 제거는 유예해야 한다; E.56 참조) — `ValidatorQueue`에서 기록된 자기
  스테이크 ≥ `effective_minimum_stake()`인 검증자를 최대 [`validators_to_promote`](#param-validators_to_promote) = 50명
  승격해야 한다. 로테이션 방출은 검증자를 `ActiveValidators`에서 제거하고 그 자기 스테이크 동결을 해동한다(원금은
  운영자 계정에 남는다); 재진입은 [`ejection_cooldown_blocks`](#param-ejection_cooldown_blocks)
  (~7 d; `Config`에 구성되며 `register`에서의 강제는 대기 중) 이후 `register`를 통해 `ValidatorQueue`로 이루어지는
  반면, `un_jail`(라이브니스 제일의 경우 `MinJailBlocks` = 3,600 이후)과 `rejoin`(장기 다운타임 퇴출의 경우, 가용
  잔액에서 자기 스테이크를 `effective_minimum_stake()`까지 보충)은
  [`validator_active_set_cap`](#param-validator_active_set_cap) 미만의 슬롯이 비어 있는 동안 제일 또는 퇴출된
  검증자를 `ActiveValidators`로 직접 복귀시킨다. 순위는 **MUST** 최소 성능 하한(R15.4c의 검증 라이브니스 + 업타임)을 조건으로
  **스테이크** 순이어야 하며, 따라서 라이브니스 신호를 부풀려도 순위가 개선되지 않는다(하한 통과만이
  게임 가능한 부분으로 남는다).

- **R15.5b.** 활성 집합은 **MUST NOT**
  [`validator_active_set_cap`](#param-validator_active_set_cap) = **1,000**을 초과해서는 안 된다. `register`는
  `ValidatorQueue`에 진입시키며 활성 집합에 직접 진입시키지 않는다; `ValidatorQueue`로부터의 로테이션 승격과
  `un_jail` 또는 `rejoin`을 통한 직접 복귀는 슬롯이 비어 있는 동안에만 `ActiveValidators`에 **MUST** 받아들여야
  하므로, 상한은 `ActiveValidators`를 한정하며 등록은 결코 한정하지 않는다. 큐에
  있는 검증자는 스테이크를 보유하고 유용한 작업을 수행할 수 있으나, 승격되기 전까지는 파이널리티 적격이 아니다.

현재 구현은 요청된 예산과 빈 슬롯 이내에서 LIFO 순서로 승격을 시도한다; 스테이크 순 선택은 #1713으로
남아 있다. 자금이 부족한 후보는 본드와 보증이 온전한 채로 큐에 남는다. 승격은 스테이크와 커미션 필드를
보존하고 성능과 합류 에포크를 리셋한다.

큐에 있는 후보에게는 제자리 자기 스테이크 보충 수단이 없다: 자금을 더 이전해도 기록된 본드는 갱신되지 않으며,
`rejoin`은 장기 다운타임 퇴출에만 적용된다. 따라서 연간 기준선 인상을 포함한 유효 하한의 상승은 하한이 다시
내려가거나 운영자가 등록을 교체할 때까지 승격을 유예시킬 수 있다. 교체를 조율하는 운영자는 먼저 스폰서
언본딩을 마련하고(네이티브 위임은 폐기됨), 이어 등록을 해지하고 새 최소치로 등록한다; 등록 해지는 이 보증 제거
절차를 강제하지 않는다. 누락된 보충 경로는 부록 H가 기록한다.

**집합 크기.** 활성 집합은 **1,000**으로 상한이 설정된다; **파이널라이즈 위원회는 100**(§15.4)이며 활성
집합에서 샘플링되므로, 둘은 별개의 한계이다. D-0526(E.41을 옵션 (a)로 해소) 하에서 모든 활성 검증자(최대 1,000)는
BABE 블록 작성 권한자이며(`MAX_ACTIVE_VALIDATORS` = `MaxAuthorities` = 1,000), AlephBFT 파이널리티는 엄격히
100명 PoUI 위원회 내에서 평가된다. 상한 미만의 실효 집합 크기는 로테이션 처리량, 스테이크 게이트, 런타임
최소 집합 및 이탈(churn) 가드([`validator_min_active_validators`](#param-validator_min_active_validators) =
4, [`validator_rotation_churn_percent`](#param-validator_rotation_churn_percent) = 10%,
[`validator_min_scored_samples`](#param-validator_min_scored_samples) = 3)에 의해 결정된다. 그 런타임 하한이
출시 코호트, 위원회 안전성 전제, 건너뛰기 대 절단 정책과 어떻게 관련되는지는 E.56이다.

메인넷 제네시스 시점의 첫 활성 집합 구성(테스트넷 이후 검증 라이브니스 기준 순위, 배치 신고, 도메인당 10 %
상한)과, 고정 하위 50 방출에서 성능 하한으로의 전환은 비준 대기 중인 제안이다:
[D-0507](decisions/v0.5.md#d-0507--post-testnet-genesis-validator-selection-and-placement-admission),
[D-0508](decisions/v0.5.md#d-0508--rotation-on-underperformance-floor-based-ejection-and-on-chain-performance-signal).

### 15.6 세션 생명주기 전반에서의 검증자

추론(inference)은 오프체인으로 스트리밍되므로, 통상적인 검증은 모든 추론 턴을 재실행하지 않는다. 정산은
여전히 제출된 턴, 서명, Merkle 경로에 비례하는 작업을 수행하며, 샘플링 감사는 체커 레인(R3.5d)에 의한
오프체인 재실행을 추가하되 검증자 자체가 수행하는 것은 아니다. 검증자 접점:

| 세션 단계 | 검증자 행동 |
|---------------|------------------|
| `open_channel` / `force_open` | 블록 작성자가 tx를 포함; 임시 트랜스크립트 `DataRef`는 `force_settle`에서 바인딩됨(R1.2a, R12.1f, G.1) |
| `force_ack` 대기 | `AckWindow`; 마이너가 자신의 인클레이브 키를 비준하거나 에이전트가 에스크로를 회수(`expire_force_open`) |
| 스트리밍 턴(오프체인) | **없음** — 인클레이브가 리프에 서명; *에이전트*가 영수증을 공동 서명 |
| `settle` / `force_settle` | 에이전트의 공동 서명된 영수증이 공개 작업 크레딧 없이 비공개 지급을 승인(R11.2b); `force_settle`은 챌린지 윈도우를 열며, 그 안에서 검증자가 체커 레인(R3.5d)의 TOPLOC/측정 루트 불일치 판정을 검증하고 공동 서명(2/3) → 사기 슬래시; 종료된 채널의 회수는 미결(E.44) |
| 분쟁(사기만) | 자격 = 세션 에이전트(자기 채널) + 활성 검증자(모든 채널); 이분 탐색(bisection) 판결; DA 서빙 아니면 슬래시가 쟁점 리프를 제공; 무응답 → 사기 판정 + 슬래시 |

**두 가지 별개의 공동 서명:** (a) **검증자 BFT 어테스테이션 쿼럼**은 직접 레일(direct rail)에서의 `G_n`
크레딧을 위해 증명을 공동 서명한다; (b) **에이전트**는 각 턴의 영수증과 정산 영수증을 공동 서명한다.
(a)만이 검증자 의무이며, 둘 중 어느 것의 배후에 있는 재실행이든 체커 레인(R3.5d)의 것이다. 마이너 및
모델 선택은 **에이전트 주도**이다(`open_channel`이 마이너를 지명하고 `model_hash`를 고정한다); 온체인
스케줄러는 없다.

### 15.7 슬래싱과 복구

`pallet_validators`는 단일 처벌 권한이다(§11.3 표); 슬래싱된 모든 담보는 소각 없이 100%
`FLOPFoundationAccount`로 이전된다(§9.3 R9.10). 사기(Collusion / EvidenceForgery /
TeeAttestationFailure) = 100% 슬래시 + 방출 + 블랙리스트. 이중 서명(Equivocation)은 상관 곡선을 따른다. 단독
위반은 50%를 슬래시하고 나머지 50%를 180 d 후 반환하며, 검증자를 방출하되 재스테이크는 가능하다. ≥⅓ 상관
이중 서명은 100%를 슬래시하고 방출하며 블랙리스트에 올린다. Liveness = 1% + 제일(jail); 장기
다운타임 = 5% + 퇴출.
[`validator_unbonding_blocks`](#param-validator_unbonding_blocks) = 21 d이며 세션/분쟁/감사가 열려 있는 동안
슬래시 락이 적용된다(D-0419). 쿨다운은 14 d DA 보존 기간 `W`보다 길며, 전체 분쟁 생명주기에 대한 그 구성은
E.57이다.

### 근거 및 출처 *(비규범적)*

출처: `D-0408`(단일 검증자 스테이킹 시스템), `D-0413`(가치 연동 하한), `D-0416`
(스테이크 순 로테이션), `D-0437`(활성 집합 상한), `D-0409`(일률적 사기 등급), `D-0419`
(언본딩 슬래시 락), `D-0420`(상관 이중 서명), `D-0501`(의석 전제 및 협력적 크레딧 범위), `D-0439`(검증
라이브니스; CPU급 검증자), `D-0529`(`FLOPFoundationAccount`로의 소각 없는 슬래시 라우팅), `D-0530`(운영자 자기
스테이크 전용). 근거 자료:
validator-miner-hardware-costs.md(§2.1 참조 프로파일
및 비교 대상), validator-set-diversity.md(의석 기준
배치 한계), miner-validator-economics.md,
da-sovereign-validator-design.md,
miner-capacity-stake-calibration.md,
r2-payment-channel-sessions.md,
session-work-verification-gap.md,
[prepublication-evidence.md](research/prepublication-evidence.md),
session-matching-orderbook-vs-agent-select.md.
운영 가이드: `docs/onboarding/validator.md`. 형식 명세:
`FlopSpecs/Sessions.lean`,
`formal-specs/channel/channel-settlement.qnt`. 상태:
[부록 H](#appendix-h--conformance--implementation-status-matrix).

---
