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

등록은 자체 서명되며 스테이크 하한 이상에서는 무허가(permissionless)이다. `register`는 계정의 감소 가능한
(reducible) 전체 잔액을 자기 스테이크로 동결하고 검증자를 `ValidatorQueue`에 배치하며, `ActiveValidators`에
직접 배치하지 **않는다** — 승격은 로테이션(§15.5)을 통해서만 이루어진다.

| 요구사항 | 규칙 |
|-------------|------|
| 자기 스테이크 | `≥ effective_minimum_stake() = max(`[`validator_min_stake`](#param-validator_min_stake)`, ValueCoupledStakeFloor)`; 기준선 305,505 FLOP, 연 +9% 복리 |
| 자기 스테이크 비율 | 자기 스테이크는 **MUST** (자기 + 위임된) 스테이크의 ≥ 20%여야 한다(`MinSelfStakeRatio`) |
| 엔티티별 슬롯 | ≤ 5(`MaxSlotsPerEntity`) |
| 블랙리스트 미등재 | 사기로 블랙리스트된 계정은 **MUST NOT** 재등록해서는 안 된다 |
| 검증 라이브니스(위원회) | 마지막으로 수락된 검증 의무(R15.4c; `LastVerifiedWork`)가 `WorkRecencyWindow` = 86,400 blk(24 h) 이내; 그렇지 않으면 활성 상태이지만 PoUI 위원회에서는 제외 |

위임(최소 100 FLOP, ≤ [`max_delegators_per_miner`](#param-max_delegators_per_miner)급 한계)과
수수료(commission)는 §6.1을 따른다.

### 15.3 의무와 자원 집약도

| 의무 | 비용 | 강제 수단 |
|------|------|-------------|
| BABE 블록 작성 | 경량 CPU; 지연 민감 가십 | 보상 + Liveness 슬래시(V1) |
| AlephBFT 파이널리티 투표 | 경량 CPU; BFT 투표 가십 O(committee) | 보상 지분 + Equivocation 슬래시(V2) |
| 검증자 어테스테이션(TEE 인용 검증 → 공동 서명) | DCAP/dstack 검증(경량 CPU + 어테스테이션 컬래터럴(collateral) 페치) | 쿼럼 2/3(§3.6); 선택적 어테스테이션 **[GAP]** O3 |
| DA 저장 및 서빙 | Reed–Solomon 레이트 ½(`R=6`, k=3+3); GB 규모 대역폭 | 서빙 아니면 슬래시(serve-or-slash) 감사; 보상 지분으로 재원 조달, **바이트당 수수료 없음** |
| 회수 가능성 / 고스트 태스크 감사 | 경량(정답이 알려진 방식) | 보유 결합(V3/V10) |
| 검증 의무 — 어테스테이션, 쿼럼 공동 서명, 감사 응답(위원회 라이브니스, R15.4c) | 경량 CPU | `WorkRecencyWindow` 내에 수락된 의무가 없으면 위원회에서 탈락 |
| 샘플링 재실행(TOPLOC 프리필 재생) | **검증자 의무 아님** — 체커 레인(R3.5d) | 검증자는 판정을 검증하고 공동 서명 |
| 분쟁 판결 / 포함 | 경량 | 검열 **[GAP]** V6 |

유일하게 무거운 부분은 DA 저장/서빙이다; 어떤 검증자 의무도 GPU나 TEE를 요구하지 않는다. 프로덕션 검증자는
**SHOULD** validator-miner-hardware-costs.md §2.1의 참조 프로파일을
프로비저닝해야 한다: SMT를 끈 ≥3.4 GHz 물리 코어 8개, 32 GB ECC RAM, 4 TB 엔터프라이즈 NVMe(체인 상태 및 §5.3
보존 기간 하의 DA 보관(custody)), 1 Gbps 대칭 무제한(unmetered) 링크 — AlephBFT급 노드 참조 사양에 스토리지를
더한 것이다.

### 15.4 선출 — PoUI로 게이팅된 위원회

- **R15.4a.** 파이널리티 위원회는 **MUST** `ActiveValidators`를 `effective_minimum_stake()` **그리고** 최근
  수락된 검증 의무(R15.4c; 스테이크 **그리고** 검증 라이브니스 — §2.3 하위 증명 1 및 3)를 충족하는
  검증자로 필터링한 뒤, **BABE-VRF** 시드로부터 [`finality_committee_size`](#param-finality_committee_size) =
  100명의 서로 다른 구성원을 **스테이크 가중 비복원 추출**로 무작위 샘플링하여 구성되어야 한다
  (`hp_consensus::sample_committee_weighted`). `pallet_aleph`는 매 에포크 이 위원회를 스냅숏하고
  `authorities()`를 `finality-aleph`에 노출한다.
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

### 15.5 로테이션과 집합 크기

로테이션은 `on_initialize`에서 매
[`validator_rotation_interval_blocks`](#param-validator_rotation_interval_blocks)(~30 d)마다 실행되며, 수동
`rotate`도 있다.

- **R15.5.** 로테이션은 **MUST** 하위 [`validators_to_eject`](#param-validators_to_eject) = 50명을 방출하고,
  `ValidatorQueue`에서 스테이크 ≥ 현재 최소치인 상위 [`validators_to_promote`](#param-validators_to_promote) = 50명을
  승격해야 한다; 방출된 검증자는
  [`ejection_cooldown_blocks`](#param-ejection_cooldown_blocks)(~7 d)을 거친 후 스테이크를 현재 최소치까지
  보충하여 `rejoin`한다. 순위는 **MUST** 최소 성능 하한(R15.4c의 검증 라이브니스 + 업타임)을 조건으로
  **스테이크** 순이어야 하며, 따라서 라이브니스 신호를 부풀려도 순위가 개선되지 않는다(하한 통과만이
  게임 가능한 부분으로 남는다).

- **R15.5b.** 활성 집합은 **MUST NOT**
  [`validator_active_set_cap`](#param-validator_active_set_cap) = **1,000**을 초과해서는 안 된다. `register`는
  `ValidatorQueue`에 진입시키며 활성 집합에 직접 진입시키지 않는다; 로테이션은 **MUST** 슬롯이 비어 있는
  동안에만 큐에서 승격해야 하므로, 상한은 `ActiveValidators`를 한정하며 등록은 결코 한정하지 않는다. 큐에
  있는 검증자는 스테이크를 보유하고 유용한 작업을 수행할 수 있으나, 승격되기 전까지는 파이널리티 적격이 아니다.

**집합 크기.** 활성 집합은 **1,000**으로 상한이 설정된다; **파이널라이즈 위원회는 100**(§15.4)이며 활성
집합에서 샘플링되므로, 둘은 별개의 한계이다. 상한 미만의 실효 집합 크기는 로테이션 처리량과 스테이크
게이트에 의해 결정된다.

### 15.6 세션 생명주기 전반에서의 검증자

추론(inference)은 오프체인으로 스트리밍되므로, 통상적인 검증은 모든 추론 턴을 재실행하지 않는다. 정산은
여전히 제출된 턴, 서명, Merkle 경로에 비례하는 작업을 수행하며, 샘플링 감사는 체커 레인(R3.5d)에 의한
오프체인 재실행을 추가하되 검증자 자체가 수행하는 것은 아니다. 검증자 접점:

| 세션 단계 | 검증자 행동 |
|---------------|------------------|
| `open_channel` / `force_open` | 블록 작성자가 tx를 포함; DA가 임시 트랜스크립트 `DataRef`를 등록 |
| `force_ack` 대기 | `AckWindow`; 마이너가 자신의 인클레이브 키를 비준하거나 에이전트가 에스크로를 회수(`expire_force_open`) |
| 스트리밍 턴(오프체인) | **없음** — 인클레이브가 리프에 서명; *에이전트*가 영수증을 공동 서명 |
| `settle` / `force_settle` | **어떤 쿼럼도 협력적 크레딧을 게이팅하지 않음** — 에이전트의 공동 서명된 영수증이 지급 + 즉시 청구된 `G_n` 크레딧을 승인하지만, 실행 정확성을 증명하지는 않음(E.44); `force_settle`은 챌린지 윈도우를 열며, 그 안에서 검증자가 체커 레인(R3.5d)의 TOPLOC/측정 루트 불일치 판정을 검증하고 공동 서명(2/3) → 사기 슬래시 |
| 분쟁(사기만) | 자격 = 세션 에이전트(자기 채널) + 활성 검증자(모든 채널); 이분 탐색(bisection) 판결; DA 서빙 아니면 슬래시가 쟁점 리프를 제공; 무응답 → 사기 판정 + 슬래시 |

**두 가지 별개의 공동 서명:** (a) **검증자 BFT 어테스테이션 쿼럼**은 직접 레일(direct rail)에서의 `G_n`
크레딧을 위해 증명을 공동 서명한다; (b) **에이전트**는 각 턴의 영수증과 정산 영수증을 공동 서명한다.
(a)만이 검증자 의무이며, 둘 중 어느 것의 배후에 있는 재실행이든 체커 레인(R3.5d)의 것이다. 마이너 및
모델 선택은 **에이전트 주도**이다(`open_channel`이 마이너를 지명하고 `model_hash`를 고정한다); 온체인
스케줄러는 없다.

### 15.7 슬래싱과 복구

`pallet_validators`는 단일 처벌 권한이다(§11.3 표). 사기(Collusion / Equivocation /
EvidenceForgery / TeeAttestationFailure) = 100% 소각 + 방출 + 블랙리스트; Liveness = 1% + 제일(jail); 장기
다운타임 = 5% + 퇴출. 상관 이중 서명(equivocation)은 복구 가능 곡선을 따른다.
[`validator_unbonding_blocks`](#param-validator_unbonding_blocks) = 21 d이며 세션/분쟁/감사가 열려 있는 동안
슬래시 락이 적용되고, 이는 14 d DA 보존 기간 `W`보다 안전한 여유를 두고 크다.

### 근거 및 출처 *(비규범적)*

출처: `D-0408`(단일 검증자 스테이킹 시스템), `D-0413`(가치 연동 하한), `D-0416`
(스테이크 순 로테이션), `D-0437`(활성 집합 상한), `D-0409`/`D-0419`/`D-0420`
(슬래싱/언본딩), `D-0501`(의석 전제 및 협력적 크레딧 범위), `D-0439`(검증
라이브니스; CPU급 검증자). 근거 자료:
validator-miner-hardware-costs.md(§2.1 참조 프로파일
및 비교 대상), miner-validator-economics.md,
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
