## 부록 A — 파라미터 레퍼런스

아래 표는 `params/flop-protocol-params.yaml`(정식 기계 검증 계약; 모든 값이 런타임 / SDK / 시뮬레이션 코드에
미러링되며 `scripts/check_params.py`로 게이트됨)에서 **생성**된다.
`uv run --script scripts/gen_param_table.py`로 재생성하며, 드리프트가 있으면 `just verify-whitepaper`가 실패한다. 각
행은 `#param-<name>`으로 앵커되어 있으며, 본문은 해당 생성 앵커로 링크한다. 이 표는
값 자체에 대한 단일 권위 목록이다.

<!-- BEGIN GENERATED: param-table (source: params/flop-protocol-params.yaml via scripts/gen_param_table.py) -->

강제(enforced) 파라미터(`params/flop-protocol-params.yaml`); 아래의 모든 값은 코드에 미러링되며 `scripts/check_params.py`로 게이트된다. 스펙 어디에서든 생성된 `#param-<name>` 앵커로 파라미터를 링크할 수 있다.

**제네시스**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-genesis_supply"></a>`genesis_supply` | 4_400_000_000 FLOP | [§9.3](#93-genesis-configuration) | D-0440 | 제네시스(발행 전) 총 공급량. R9.7(§9.3)에 의해 규범적으로 고정된다. |
| <a id="param-genesis_miner_airdrop"></a>`genesis_miner_airdrop` | 1_200_000_000 FLOP | [§9.3](#93-genesis-configuration) | D-0438 | 제네시스 공급량 중 마이너 에어드롭 구성분(27.27%). |
| <a id="param-genesis_validator_airdrop"></a>`genesis_validator_airdrop` | 1_200_000_000 FLOP | [§9.3](#93-genesis-configuration) | D-0440 | 제네시스 공급량 중 검증자 에어드롭 구성분(27.27%). |
| <a id="param-genesis_agent_airdrop"></a>`genesis_agent_airdrop` | 1_200_000_000 FLOP | [§9.3](#93-genesis-configuration) | D-0438 | 제네시스 공급량 중 에이전트 에어드롭 구성분(27.27%). |
| <a id="param-genesis_reserve"></a>`genesis_reserve` | 800_000_000 FLOP | [§9.3](#93-genesis-configuration) | D-0440 | 제네시스 공급량 중 생태계/인센티브 리저브 구성분(18.18%) — KOL, 추천(referral) 및 성장 인센티브. |
| <a id="param-validator_min_stake"></a>`validator_min_stake` | 1_200_000 FLOP | [§9](#9-emission--supply) | D-0440 | 기준 하한; 연 9%로 복리 증가한다(MinimumValidatorStake). |
| <a id="param-airdrop_vesting_duration_blocks"></a>`airdrop_vesting_duration_blocks` | 7_776_000 blocks | [§8.2](#82-era-t-conversion-and-airdrop-vesting) | SPEC-022 | 잠정적 팰릿 일정: 1초 블록 시간 기준 90일 선형 에어드롭 베스팅이며, 비준된 어떤 그랜트 티어도 규율하지 않는다(§8.2). |

**발행과 보상**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-initial_block_reward"></a>`initial_block_reward` | 96 FLOP | [§9](#9-emission--supply) | D-008 | 제네시스 시점(에라 0)의 블록 보상. |
| <a id="param-halving_interval_blocks"></a>`halving_interval_blocks` | 63_072_000 blocks | [§9](#9-emission--supply) |  | 반감 사이의 블록 수(1s/block 기준 약 730일). |
| <a id="param-max_halvings"></a>`max_halvings` | 5 count | [§9](#9-emission--supply) | D-0436 | 보상이 영구적으로 하한에 도달하기 전까지의 반감 횟수. |
| <a id="param-floor_reward"></a>`floor_reward` | 3 FLOP | [§9](#9-emission--supply) | D-0436 | max_halvings 이후의 영구 블록당 보상(96 >> 5 = 3). |
| <a id="param-miner_share_ppt"></a>`miner_share_ppt` | 750 parts-per-thousand | [§9](#9-emission--supply) | D-0435 | 각 블록 보상 중 마이너 몫(75%; 옐로페이퍼 §9). |
| <a id="param-validator_share_ppt"></a>`validator_share_ppt` | 100 parts-per-thousand | [§9](#9-emission--supply) |  | 각 블록 보상 중 검증자 몫(10%). |
| <a id="param-agent_share_ppt"></a>`agent_share_ppt` | 100 parts-per-thousand | [§9](#9-emission--supply) | D-0435 | 각 블록 보상 중 에이전트/브로커 리베이트 몫(10%; 옐로페이퍼 §9). |
| <a id="param-staker_share_ppt"></a>`staker_share_ppt` | 50 parts-per-thousand | [§9](#9-emission--supply) | D-0435 | 각 블록 보상 중 커뮤니티 스테이커 몫(5%; 옐로페이퍼 §9) — 슬래싱 위험 없이, 운영자 위임 없이(D-0530) 7개의 잠금 기간 티어에 걸친 기간 잠금형 커뮤니티 스테이킹 풀로, 마이너와 검증자를 제외한 모든 FLOP 스테이커를 위한 것이다. |
| <a id="param-reward_distribution_period_blocks"></a>`reward_distribution_period_blocks` | 86_400 blocks | [§9](#9-emission--supply) |  | 블록 보상 분배 사이의 블록 수(1 s 블록 기준 하루). |
| <a id="param-gn_decay_factor_ppb"></a>`gn_decay_factor_ppb` | 1_000_000_000 ppb | [§9](#9-emission--supply) |  | 키가 없을 때 읽히는 GnDecayFactor: 1.0, 즉 감쇠 없음이므로 한 기간의 마이너 레그는 순전히 검증된 G_n에 따라 분할된다(소유자 결정 2026-10-01, #2144). |
| <a id="param-finality_committee_premium_weight_ppm"></a>`finality_committee_premium_weight_ppm` | 1_100_000 ppm | [§9](#9-emission--supply) |  | 검증자 10% 풀 내부에서의 파이널리티 위원회 검증자 보상 가중치. |

**개발자 보조금(블록 보상과 별개)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-subsidy_per_block_per_recipient"></a>`subsidy_per_block_per_recipient` | 8 FLOP | [§9](#9-emission--supply) | D-0436 | 96 FLOP 블록 보상에 더해, FLOP Labs와 FLOP 재단 각각에 지급되는 ERA-0 블록당 보조금(합산 16 FLOP/block; 옐로페이퍼 §9). |
| <a id="param-subsidy_duration_blocks"></a>`subsidy_duration_blocks` | 315_360_000 blocks | [§9](#9-emission--supply) | D-0436 | 배타적 보조금 일몰 블록(~3650일 = 10년 = 5 × halving_interval_blocks)으로, 그 시점 및 이후(`now >= SubsidyEndBlock`)에는 `on_initialize`가 0을 민팅한다. |

**스테이킹과 위임**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-min_miner_self_stake"></a>`min_miner_self_stake` | 10_000 FLOP | [§6.1](#61-primitives) |  | 마이너로 등록하기 위한 최소 자기 스테이크(anti-Sybil). |
| <a id="param-miner_commission_cap_percent"></a>`miner_commission_cap_percent` | 20 percent | [§6.1](#61-primitives) | D-0530 | [DEPRECATED — D-0530] 마이너가 위임자에게 부과할 수 있었던 레거시 최대 커미션(20%; 옐로페이퍼 §6.1). |
| <a id="param-miner_unbonding_blocks"></a>`miner_unbonding_blocks` | 604_800 blocks | [§6.1](#61-primitives) |  | 마이너 언본딩 기간(1s/block 기준 약 7일). |
| <a id="param-miner_capacity_stake_per_gflop"></a>`miner_capacity_stake_per_gflop` | VFY / 100 (= 0.01 FLOP per GFLOP/s) | [§6.1](#61-primitives) | D-0418 | 용량 비례 마이너 자기 스테이크 = min_miner_self_stake + B_p * 이 값(선형, 상한 없음 — 상한을 두면 최대 규모 마이너의 사기가 +EV가 됨; D-0418, ENG-8). 캘리브레이션된 B_p의 GFLOP/s당 0.01 FLOP(VFY/100, 여기서 VFY = 1 FLOP). |
| <a id="param-miner_stake_revocation_latency_blocks"></a>`miner_stake_revocation_latency_blocks` | 604_800 blocks | [§6.1](#61-primitives) |  | 마이너 스테이크 노출 계산에 사용되는 철회/분쟁 지연 윈도우: 필요 자기 스테이크는 cap × 이 윈도우 × stake_rate를 커버해야 한다. |
| <a id="param-miner_stake_surge_multiplier_ppm"></a>`miner_stake_surge_multiplier_ppm` | 1_250_000 ppm | [§6.1](#61-primitives) |  | 잠정 버스트 상한 스테이크 승수. 1_250_000 ppm = 상한이 아직 버스트/감사 래칫 상태인 동안 노출 스테이크 1.25배. |
| <a id="param-calibration_min_verified_jobs"></a>`calibration_min_verified_jobs` | 64 jobs | [§7.1](#71-entry--benchmark-burst) | D-0433 | D-0433 빠른 서빙 진입 버스트에서의 최소 독립 검증 작업 수. |
| <a id="param-calibration_min_burst_blocks"></a>`calibration_min_burst_blocks` | 600 blocks | [§7.1](#71-entry--benchmark-burst) | D-0433 | D-0433 체인 시간 기준 최소 서빙 진입 버스트(1s 블록 기준 10분). 옐로페이퍼 §7.1. |
| <a id="param-calibration_min_utilization_ppm"></a>`calibration_min_utilization_ppm` | 500_000 ppm | [§7.1](#71-entry--benchmark-burst) |  | 버스트 수락을 위한 지속 가동률 임계값. |
| <a id="param-calibration_provisional_discount_ppm"></a>`calibration_provisional_discount_ppm` | 900_000 ppm | [§7.1](#71-entry--benchmark-burst) |  | min(empirical_burst_cap, discounted_sku_ceiling) 이전에 어테스테이션된 SKU 상한에 적용되는 HARD 티어 잠정 할인. 옐로페이퍼 §7.1. |
| <a id="param-calibration_lease_blocks"></a>`calibration_lease_blocks` | 604_800 blocks | [§7.2](#72-renewable-cap) | D-0433 | D-0433 갱신 가능한 캘리브레이션 상한 리스(1s 블록 기준 7일). |
| <a id="param-calibration_renewal_min_verified_jobs"></a>`calibration_renewal_min_verified_jobs` | 8 jobs | [§7.2](#72-renewable-cap) | D-0433 | D-0433 빠른 재시작/오프라인/주기적 상한 갱신을 위한 최소 신규 원샷 고스트 카나리 수. |
| <a id="param-calibration_renewal_max_age_blocks"></a>`calibration_renewal_max_age_blocks` | 600 blocks | [§7.2](#72-renewable-cap) |  | 마이너가 트리거하는 갱신의 최대 윈도우(1s 블록 기준 10분). |
| <a id="param-calibration_min_recalibration_interval_blocks"></a>`calibration_min_recalibration_interval_blocks` | 600 blocks | [§7.1](#71-entry--benchmark-burst) |  | 수락된 초기 캘리브레이션 사이의 최소 간격(1s 블록 기준 10분). 급속한 상한 교체와 전략적 재시도 루프를 방지한다. |
| <a id="param-calibration_max_gpu_inventory_entries"></a>`calibration_max_gpu_inventory_entries` | 16 distinct SKUs | [§7.1](#71-entry--benchmark-burst) |  | 한 마이너 호스트에서 어테스테이션되는 서로 다른 GPU SKU의 최대 개수. |
| <a id="param-miner_capacity_stake_sim_per_10_gflop"></a>`miner_capacity_stake_sim_per_10_gflop` | 0.1 FLOP per 10 GFLOP/s | [§6.1](#61-primitives) | D-0418 | miner_capacity_stake_per_gflop의 시뮬레이터 미러(D-0418). |

**컴퓨트 채널 타이밍 경계**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-timing_max_clock_skew_ms"></a>`timing_max_clock_skew_ms` | 250 ms | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | 타이밍을 Eligible과 Ambiguous로 분류할 때 마이너와 에이전트의 벽시계 사이에 허용되는 최대 클록 스큐(ms). |
| <a id="param-timing_network_pad_ms"></a>`timing_network_pad_ms` | 100 ms | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | 영수증 타이밍을 평가할 때 클록 스큐 허용치에 더해지는 네트워크 왕복 패딩(ms). |

**세션 / 용량 예약(A1 안티스팸)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-max_active_reservations_base"></a>`max_active_reservations_base` | 4 count | [§12.2](#122-per-identity-capacity-reservation) |  | 에이전트 아이덴티티당 동시 활성 용량 예약의 기본 개수. |
| <a id="param-escrow_per_reservation_slot"></a>`escrow_per_reservation_slot` | 50 FLOP | [§12.2](#122-per-identity-capacity-reservation) |  | 기본치를 넘어 활성 예약 슬롯 +1개를 부여하는 에스크로(FLOP). |
| <a id="param-min_certificate_premium_ppm"></a>`min_certificate_premium_ppm` | 1_500_000 ppm | [§12.2](#122-per-identity-capacity-reservation) |  | 인증서 기반 프리미엄 정산에서 모델의 GFLOP당 요율에 대한 최소 가격 배수(1_500_000 = 1.5x)(#535). certificate_settle은 에스크로 >= price_per_gflop * aggregate_gn * multiple을 요구하므로, 프리미엄 등급의 증명된 작업이 표준 요율 에스크로로 지급될 수 없다. |
| <a id="param-sampled_audit_alpha_ppm"></a>`sampled_audit_alpha_ppm` | 50_000 ppm | [§3.5](#35-tier-3--independent-optimistic-re-execution--slashing) |  | 샘플링 감사 인증서 모드의 기본 α(#628 / 인증서 포맷 섹션 9.5; 옐로페이퍼 §3.5). 50_000 = 에포크 종료 후 VRF 비컨을 통해 선택되는 턴의 5%; 1_000_000 = 전수 감사. |
| <a id="param-sampled_audit_checkpoint_turns"></a>`sampled_audit_checkpoint_turns` | 16 turns | [§3.5](#35-tier-3--independent-optimistic-re-execution--slashing) |  | 샘플링 감사 재실행을 위한 KV 체크포인트 간격 C(#628). |
| <a id="param-audit_quantum_gn"></a>`audit_quantum_gn` | 100_000_000 G_n | [§12.2](#122-per-identity-capacity-reservation) |  | #764 폭발 반경 제어: 세션 호스트 / 체커는 서빙된 작업 G_n이 이 값만큼 누적될 때마다 최소 한 개의 감사 티켓을 강제한다(가치 퀀텀 Q). |
| <a id="param-high_value_gn_threshold"></a>`high_value_gn_threshold` | 10_000_000 G_n | [§12.2](#122-per-identity-capacity-reservation) |  | #764 비대칭성: G_n ≥ 이 값인 단일 턴은 강제 감사된다(해당 리프에 대해 실효 α=1). 따라서 드문 고-G_n 턴이 Bernoulli-α에 무임승차할 수 없다. 반드시 ≤ audit_quantum_gn으로 유지되어야 하며, 그래야 감사되지 않은 턴 하나만으로 퀀텀을 채울 수 없다(TRIZ P4 비대칭). |

**파이널리티 정지 안전 모드(컴퓨트 채널)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-finality_lag_warn"></a>`finality_lag_warn` | 30 blocks | [§13.0](#130-degraded-state-settlement-policy-normative) |  | 이 값을 넘는 파이널리티 지연에서 검출기가 Lagging을 보고한다(경보만; 파이널리티 기준 기한은 자연히 일시 정지). |
| <a id="param-finality_freeze_threshold"></a>`finality_freeze_threshold` | 120 blocks | [§13.0](#130-degraded-state-settlement-policy-normative) |  | 이 값 이상의 파이널리티 지연에서 채널이 Stalled에 진입한다: 파이널리티 의존 신규 open은 fail-closed로 거부된다(ensure_finality_open_allowed); 추가형 top-up/cancel 경로는 열린 상태로 유지된다. |
| <a id="param-max_finality_stall"></a>`max_finality_stall` | 3_600 blocks | [§13.0](#130-degraded-state-settlement-policy-normative) |  | 이 값 이상의 파이널리티 지연에서 체인은 EscapeEligible(안전 모드)이 된다: AlephBFT 파이널리티를 복구하거나 하드포크 런북을 통해 체크포인트 복구를 비준한다. 1초 블록에서 ~1h. |
| <a id="param-htlc_timelock_symmetry_safety_margin_percent"></a>`htlc_timelock_symmetry_safety_margin_percent` | 20 percent | [§10.1](#101-requirements) |  | 외부 체인 기간을 1초 FLOP 블록으로 변환한 뒤, 그 기간에 대한 백분율로 표현한 외부 체인 HTLC 최소 안전 마진. |
| <a id="param-htlc_burn_share_ppt"></a>`htlc_burn_share_ppt` | 0 ppt | [§13.0](#130-degraded-state-settlement-policy-normative) |  | 타임아웃 이후 파이널라이즈된 HTLC 해소에서 지급 전에 소각되는 몫. |
| <a id="param-btc_block_time_flop_blocks"></a>`btc_block_time_flop_blocks` | 600 blocks | [§10.1](#101-requirements) |  | 1초 FLOP 블록 단위로 표현한 Bitcoin 평균 블록 간격. |

**PoUI 시뮬레이터 모드 안전 플래그(#297 CRIT-02 / RT-C02)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-poui_allow_simulator_mode"></a>`poui_allow_simulator_mode` | cfg!(feature = "volta") flag |  |  | #297: AllowSimulatorMode는 TEE 없는 시뮬레이터 크레딧 경로를 게이트한다; `volta` devnet 피처에서 파생되므로 프로덕션 런타임은 fail-closed된다. |
| <a id="param-paid_storage_enabled"></a>`paid_storage_enabled` | cfg!(feature = "paid-storage-unratified") flag | [§5.4](#54-agent-memory-and-paid-data-storage) |  | 미비준 유료 에이전트 스토리지 팰릿을 위한 빌드 타임 게이트(옐로페이퍼 §5.4, R5.4k). |

**D-0528 스폰서 소유 등록 본드(devnet/testnet 전용)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-sponsored_self_stake_enabled"></a>`sponsored_self_stake_enabled` | cfg!(feature = "sponsored-self-stake") flag |  | D-0528 | D-0528: 활성 후원 원금이 마이너 용량 본드와 검증자 유효 최소치에 산입되며, 스폰서가 운영자의 등록 본드 전체를 게시할 수 있다(sponsor_register_miner / sponsor_register_validator). |

**PoUI 제출 속도 제한**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-poui_submission_window_blocks"></a>`poui_submission_window_blocks` | 86_400 blocks | [§1.2](#12-protocol-clocks--canonical-table) |  | 블록 정렬된 PoUI 제출 속도 제한 윈도우(1초 블록에서 1일). |
| <a id="param-poui_max_submissions_epoch"></a>`poui_max_submissions_epoch` | 10 count | [§1.2](#12-protocol-clocks--canonical-table) |  | 블록 정렬된 각 poui_submission_window_blocks 윈도우 동안 마이너당 최대 제출 수. |

**F2 공급 측 거버너(기본 OFF; 거버넌스 설정 가능)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-governor_default_enabled"></a>`governor_default_enabled` | false bool | [§9](#9-emission--supply) |  | 두 거버너 댐퍼의 마스터 기본값 — 제네시스에서 OFF(보험 목적, 거버넌스가 활성화). |
| <a id="param-governor_emission_damping_util_floor"></a>`governor_emission_damping_util_floor` | 0.3 fraction | [§9](#9-emission--supply) |  | 이 값 미만의 가동률에서 보존 보상 부스트가 작동한다(가동률 연동, 절대 가격 연동 아님 — anti-Terra). |
| <a id="param-governor_emission_damping_max_boost"></a>`governor_emission_damping_max_boost` | 1.5 multiplier | [§9](#9-emission--supply) |  | 거버너가 활성화된 경우 마이너 보상 승수의 하드 상한(최대 +50%). |
| <a id="param-governor_dynamic_burn_tier1"></a>`governor_dynamic_burn_tier1` | 0.1 fraction | [§9](#9-emission--supply) |  | 동적 소각이 활성화된 경우 에라 0–1(era_max 1)의 수수료 소각 비율. |
| <a id="param-governor_dynamic_burn_tier2"></a>`governor_dynamic_burn_tier2` | 0.15 fraction | [§9](#9-emission--supply) |  | 동적 소각이 활성화된 경우 에라 2–3(era_max 3)의 수수료 소각 비율. |
| <a id="param-governor_dynamic_burn_tier3"></a>`governor_dynamic_burn_tier3` | 0.25 fraction | [§9](#9-emission--supply) |  | 동적 소각이 활성화된 경우 에라 4 이상(era_max 99 센티널)의 수수료 소각 비율. |

**거버넌스**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-governance_root_track_approval"></a>`governance_root_track_approval` | 67 percent | [§14.2](#142-fip-binding) | D-015 | 루트 / 프로토콜 업그레이드 거버넌스 커브의 고정 승인 임계값(비잔틴 2/3). APP_ROOT로 인코딩되며 프로덕션 protocol_upgrade 트랙에서 사용된다(GOV-A, 옐로페이퍼 §14.2). |
| <a id="param-protocol_upgrade_support_floor"></a>`protocol_upgrade_support_floor` | 15 percent | [§14.2](#142-fip-binding) | D-0415 | 프로덕션 protocol_upgrade(Root) 트랙의 투표율 하한(min_support) — 50% 상한에서 15% 하한으로 감쇠(SPEC-024에 없던 쿼럼). |

**합의 / 파이널리티 위원회**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-babe_primary_probability_denominator"></a>`babe_primary_probability_denominator` | 50 ratio-denominator | [§15.4](#154-selection--the-poui-gated-committee) |  | BABE 프라이머리 슬롯 확률 c = 1/N. 검증자의 슬롯당 당선 확률은 p = 1 - (1 - c)^theta(theta = 스테이크 비율). |
| <a id="param-aleph_max_data_branch_len"></a>`aleph_max_data_branch_len` | 30 blocks | [§15.4](#154-selection--the-poui-gated-committee) |  | AlephBFT가 순서를 정하는 체인 제안 하나에 담기는 최대 블록 수 — 파이널리티 처리량 상한(파이널리티 속도 ~= 이 값 / 순서화 지연; 이전 값 7에서 1.66 blocks/s가 측정되었으며, 이는 제안 하나를 순서화하는 데 ~4.2 s가 걸림을 뜻한다). |
| <a id="param-aleph_max_round"></a>`aleph_max_round` | 65_535 round | [§15.4](#154-selection--the-poui-gated-committee) |  | 한 세션에서 수락되는 최대 AlephBFT 라운드. |
| <a id="param-aleph_gossip_protocol_version"></a>`aleph_gossip_protocol_version` | 5 version | [§15.4](#154-selection--the-poui-gated-committee) |  | AlephBFT 유닛 가십을 위한 알림 프로토콜 버전(/flop/aleph/N). |
| <a id="param-finality_committee_size"></a>`finality_committee_size` | 100 count | [§15.4](#154-selection--the-poui-gated-committee) | D-0437 | AlephBFT 파이널라이징 위원회 크기: PoUI 게이트 활성 집합에서 BABE-VRF 시드로 스테이크 가중 비복원 무작위 샘플링(#448/#848). |
| <a id="param-validator_attestation_threshold"></a>`validator_attestation_threshold` | 666_666_666 perbill-parts | [§3.6](#36-tier-4--on-chain-settlement-zk-aggregation--validator-bft-quorum) | D-0414 | BFT 어테스테이션 쿼럼(Perbill parts 666_666_666 = 2/3), 루트 거버넌스 가능; 직접 PoUI 증명 경로 + 고스트 태스크를 게이트한다. 옐로페이퍼 §3.6/§13.3. |
| <a id="param-attest_max_verifier_set_members"></a>`attest_max_verifier_set_members` | 100 count | [§15.4](#154-selection--the-poui-gated-committee) |  | 하나의 어테스테이션 프로파일에 저장되는 거버넌스 관리 검증기(verifier) 키의 최대 개수. |
| <a id="param-attest_max_claim_signatures"></a>`attest_max_claim_signatures` | 100 count | [§15.4](#154-selection--the-poui-gated-committee) |  | `pallet_attest` 공유 클레임 레일이 수락하는 최대 서명 수; 그 레일의 100명 거버넌스 검증자 집합 한계와 일치하며, 디스패치 웨이트와 블록 길이로 한정되는 `pallet_flop_poui` `submit_validator_attestations` 번들에는 상한을 두지 않는다. |
| <a id="param-poui_tee_v1_profile_id"></a>`poui_tee_v1_profile_id` | H256([4u8; 32]) profile-id | [§15.4](#154-selection--the-poui-gated-committee) |  | PoUI TEE v1 클레임을 위한 거버넌스 관리 공유 어테스테이션 프로파일 id. |
| <a id="param-poui_tee_v1_profile_version"></a>`poui_tee_v1_profile_version` | 1 profile-version | [§15.4](#154-selection--the-poui-gated-committee) |  | PoUI TEE v1 클레임의 초기 프로파일 버전. |

**검증자 보안 정책**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-validator_rotation_interval_blocks"></a>`validator_rotation_interval_blocks` | 2_592_000 blocks | [§15.5](#155-rotation--set-size) | D-0416 | 검증자 집합 로테이션 주기(1s 기준 약 30일); 자동 on_initialize + 수동 rotate. 옐로페이퍼 §15.5. |
| <a id="param-validators_to_eject"></a>`validators_to_eject` | 50 count | [§15.5](#155-rotation--set-size) |  | 로테이션당 요청 최대치; 실제 방출은 점수화된 증거도 요구하며(블랙리스트된 의석은 증거가 필요 없고 가장 먼저 방출된다), 이탈 비율과 최소 활성 집합을 준수한다. |
| <a id="param-validators_to_promote"></a>`validators_to_promote` | 50 count | [§15.5](#155-rotation--set-size) |  | 로테이션당 대기열에서의 승격 수(스테이크 >= 현재 최소치). 옐로페이퍼 §15.5. |
| <a id="param-validator_active_set_cap"></a>`validator_active_set_cap` | 1_000 count | [§9.3](#93-genesis-configuration) | D-0437 | ActiveValidators의 최대 활성 검증자 수(ValidatorQueue로부터의 로테이션 승격 또는 직접적인 un_jail/rejoin 복귀로 받아들여짐). 옐로페이퍼 §9.3 R9.9, §15.5. |
| <a id="param-validator_min_active_validators"></a>`validator_min_active_validators` | 4 count | [§15.5](#155-rotation--set-size) |  | 로테이션과 모든 제거 경로가 보존하는 최소 활성 집합. |
| <a id="param-validator_rotation_churn_percent"></a>`validator_rotation_churn_percent` | 10 percent | [§15.5](#155-rotation--set-size) |  | 한 번의 로테이션에서 방출되는 현재 활성 집합의 최대 비율로, 검증자 1명 단위로 올림한다. |
| <a id="param-validator_min_scored_samples"></a>`validator_min_scored_samples` | 3 count | [§15.5](#155-rotation--set-size) |  | 검증자가 방출될 수 있기 전에 한 로테이션 간격 내에 필요한 성능 점수 갱신 횟수. |
| <a id="param-ejection_cooldown_blocks"></a>`ejection_cooldown_blocks` | 604_800 blocks | [§15.5](#155-rotation--set-size) |  | 로테이션으로 방출된 검증자(방출 시 자기 스테이크 동결이 해동됨)가 effective_minimum_stake로 ValidatorQueue에 재등록할 수 있기까지의 쿨다운(~7 d); Config에 구성되며, register에서의 강제는 대기 중. |
| <a id="param-validator_unbonding_blocks"></a>`validator_unbonding_blocks` | 1_814_400 blocks | [§13](#13-failure-semantics--actor--failure-matrix) | D-0419 | 검증자 스테이크 언본딩 락업(약 21일); 위법 행위 후 인출을 제한한다. 옐로페이퍼 §13. |
| <a id="param-validator_extended_downtime_slash_percent"></a>`validator_extended_downtime_slash_percent` | 5 percent | [§13.2](#132-validator-consensus--da--leader-duties) | D-0409 | 장기 검증자 다운타임에 대한 슬래시 비율(이후 제거). 옐로페이퍼 §13.2. |
| <a id="param-validator_growth_numerator"></a>`validator_growth_numerator` | 109 ratio | [§15.2](#152-onboarding-normative) | D-0413 | 검증자 최소 스테이크 하한에 대한 연간 복리 계수의 분자(109/100 = +9%/yr). 옐로페이퍼 §15.2. |
| <a id="param-validator_growth_denominator"></a>`validator_growth_denominator` | 100 ratio | [§15.2](#152-onboarding-normative) | D-0413 | validator_growth_numerator와 짝을 이루는 분모(109/100 = +9%/yr). 옐로페이퍼 §15.2. |

**미터링 트립와이어**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-throughput_tripwire_gflops_per_sec"></a>`throughput_tripwire_gflops_per_sec` | 2_000_000 G_n/s | [§4.2](#42-the-op-count-model) | D-0405 | 암시된 gn*1000/latency_ms가 이 값을 초과하는 모든 클레임을 거부한다(절대 클램프하지 않음); 거부 전용, 거버넌스 가능, 기본 켜짐. 옐로페이퍼 §4.2. |
| <a id="param-soft_tier_spot_check_rate_ppm"></a>`soft_tier_spot_check_rate_ppm` | 25_000 ppm | [§7.1](#71-entry--benchmark-burst) |  | 품질 감사 가격 책정을 위해 캘리브레이션 스냅숏 이벤트와 함께 노출되는 SOFT 티어 채널 스팟체크 노출도. 옐로페이퍼 §7.1. |

**컴퓨트 채널 정산**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-refund_penalty_phi_percent"></a>`refund_penalty_phi_percent` | 20 percent | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0422 | 모호한 조기 종료 시 미사용 에스크로에 부과되는 정적 D-0422 페널티 비율 phi; 페널티는 소각 없이 100% FLOPFoundationAccount로 라우팅되며(R9.10), 결코 마이너에게 가지 않는다. |
| <a id="param-channel_max_settlement_turns"></a>`channel_max_settlement_turns` | 1_024 count | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | settle/force_settle 번들당 VerifiedTurns의 하드 상한이자, 개설 시점 SLA의 max_turns 상한. |
| <a id="param-channel_max_session_activation_bytes"></a>`channel_max_session_activation_bytes` | 65_536 bytes | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | 자금이 조달된 Open 세션의 활성화당 DA 할당 상한. |
| <a id="param-channel_max_merkle_path_len"></a>`channel_max_merkle_path_len` | 64 count | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | VerifiedTurn당 최대 머클 인증 경로 길이(최대 2^64개 리프를 가진 트리에서의 멤버십을 증명한다). |
| <a id="param-channel_base_per_turn"></a>`channel_base_per_turn` | 1 base unit (10^-18 FLOP) | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | 2부 요금제(#719 옵션 A)의 턴당 정액 요금: turn_pay = BasePerTurn + G_n(채널 지급 단위에서 rate=1). |
| <a id="param-channel_c_turn_fixed"></a>`channel_c_turn_fixed` | 1 base unit (10^-18 FLOP) | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | BasePerTurn이 반드시 충당해야 하는 턴당 고정 비용 하한(#719). integrity_test는 BasePerTurn ≥ CTurnFixed를 단언하여 더스트 턴이 마이너/네트워크에 순손실이 되지 않게 한다. |
| <a id="param-channel_dispute_window_blocks"></a>`channel_dispute_window_blocks` | 604_800 blocks | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0403 | 세션 분쟁/챌린지 윈도우(7일); integrity_test가 <= DaEphemeralRetention(14일)을 강제한다. 옐로페이퍼 §12.1. |
| <a id="param-channel_dispute_response_window_blocks"></a>`channel_dispute_response_window_blocks` | 7_200 blocks | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0403 | 개시된 분쟁에 응답할 시간(2시간); 무응답은 기본적으로 사기 판정으로 처리된다. 옐로페이퍼 §12.1. |
| <a id="param-channel_toploc_escalation_window_blocks"></a>`channel_toploc_escalation_window_blocks` | 7_200 blocks | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0431 | #754: 중간 대역 TOPLOC 에스컬레이션을 검증자들이 해소할 윈도우(2시간) — 더 강한 신고 → 슬래시, 또는 쿼럼 무혐의 — 결론 없이 타임아웃되기 전까지(에이전트 전액 환불, 마이너 지급 없음, 슬래시 없음). |
| <a id="param-channel_challenger_bond"></a>`channel_challenger_bond` | 100 FLOP | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | 챌린저가 세션 분쟁을 개시하기 위해 예치하는 본드(그리핑 방지). 옐로페이퍼 §12.1. |
| <a id="param-slash_fraud_percent"></a>`slash_fraud_percent` | 100 percent | [§13.2](#132-validator-consensus--da--leader-duties) | D-0529 | 전액 슬래시 결함 등급(D-0529에 따라 소각 없이 100% FLOPFoundationAccount로 라우팅): Collusion / EvidenceForgery / TEE 어테스테이션 실패 / 상관 이중 서명 / 이중 지불 → 100% 슬래시 + 방출 + 블랙리스트. 옐로페이퍼 §13.2. |
| <a id="param-channel_audit_forfeit_slash_ppm"></a>`channel_audit_forfeit_slash_ppm` | 1_000_000 ppm | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0403 | #844 공개-또는-몰수(publish-or-forfeit): 감사 데이터 라이브니스 몰수 슬래시 하한으로, 보류된 정산 윈도우 가치의 ppm 단위. |
| <a id="param-inference_fee_miner_share_ppt"></a>`inference_fee_miner_share_ppt` | 850 parts-per-thousand | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0525 | #2702(D-0525): 경영진 결정(Shu, 2026-10-14). |
| <a id="param-inference_fee_validator_share_ppt"></a>`inference_fee_validator_share_ppt` | 150 parts-per-thousand | [§9](#9-emission--supply) | D-0525 | #2702(D-0525): 경영진 결정(Shu, 2026-10-14). |
| <a id="param-audit_fee_split_ppm"></a>`audit_fee_split_ppm` | 10_000 ppm | [§9](#9-emission--supply) | D-0403 | #846, #2702(D-0525): 정산 지급액의 비준된 1%(10_000 ppm)를 15% 검증자 수수료 레그에서 충당하여, 감사 작업에 대해 검증자에게 지급하는 감사 풀에 넣는다. |
| <a id="param-audit_fee_per_turn"></a>`audit_fee_per_turn` | 1 FLOP | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0403 | #846: VRF로 배정된 검증자가 감사 판정 건당 감사 풀에서 청구하는 정액 수수료(claim_audit_fee). 제출된 증거와 풀의 지급 능력에 따라 게이트된다(미지급 의무 경로 없음). 1 FLOP은 자리표시값이며, 거버넌스가 측정된 감사 비용에 맞춰 재보정할 수 있다. |
| <a id="param-channel_ack_window_blocks"></a>`channel_ack_window_blocks` | 600 blocks | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) |  | 만료로 에스크로가 환불되기 전에, 지정된 마이너가 퍼미션리스 force_open을 force_ack할 수 있는 윈도우. 옐로페이퍼 §12.1, 부록 C.3. |
| <a id="param-min_force_open_escrow_for_failed_ack"></a>`min_force_open_escrow_for_failed_ack` | 0.05 FLOP | [§12.1](#121-sessions--attested-streaming--aggregate-settlement) | D-0423 | 만료되고 ack되지 않은 요청이 지정 마이너의 FailedAcks 카운터를 증가시키게 하는 최소 force_open 에스크로. |

**파생 TOPLOC 밴드(모델/정밀도별 거버넌스 설정; #685, #705)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-toploc_band_constants_fields"></a>`toploc_band_constants_fields` | kappa_profile_hash structural |  |  | band_verdict / report_toploc_mismatch가 소비하는, (모델, 정밀도)별 파생 TOPLOC 밴드 커밋 상수: kappa_profile_hash, band_tau_accept, band_tau_slash, challenge_k, challenge_window_w. |
| <a id="param-toploc_band_tau_accept_bf16_milli"></a>`toploc_band_tau_accept_bf16_milli` | 2_900 milli_exponent_error |  |  | 파생된 bf16 수락 임계값 τ_accept≈2.9 지수 오차, 밀리 단위(×1000). |
| <a id="param-toploc_band_tau_slash_bf16_milli"></a>`toploc_band_tau_slash_bf16_milli` | 185_600 milli_exponent_error |  |  | 파생된 bf16 슬래시 임계값 τ_slash≈185.6 지수 오차, 밀리 단위(×1000). |
| <a id="param-toploc_band_eng29_threshold_milli"></a>`toploc_band_eng29_threshold_milli` | 38_000 milli_exponent_error |  |  | ENG-29에서 경험적으로 배포된 지수 오차 임계값(38), 밀리 단위. |
| <a id="param-toploc_band_kappa_within_llama31_8b_bf16"></a>`toploc_band_kappa_within_llama31_8b_bf16` | 4.5 dimensionless |  |  | Llama-3.1-8B bf16에 대해 피팅/선정된 레이어 내 κ(ENG-29). |

**모델 레지스트리(디코드 정책 집합)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-max_decode_policies_per_model"></a>`max_decode_policies_per_model` | 32 count |  |  | 모델의 선택적 허용 집합에 고정할 수 있는 디코드 정책 해시의 최대 개수(BoundedDecodePolicySet = BoundedVec<H256, ConstU32<MAX_DECODE_POLICIES_PER_MODEL>>). |

**미터링 인증서 바이트당 토큰 밴드(#871)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-tokens_per_byte_band_ppm_llama3"></a>`tokens_per_byte_band_ppm_llama3` | 500_000 ppm | [§4](#4-effective-flop-metering) |  | Llama-3 토크나이저의 정직한 바이트당 토큰 수에 대한 인증된 상한(ppm; 500000 = 0.5 토큰/바이트) — 미터링 인증서 패딩 제약 (e)를 제한하는 (모델, 토크나이저)별 모델 레지스트리 필드: prompt_tokens ≤ ⌈len(input_bytes) · band/1e6⌉ 및 generated_tokens ≤ ⌈(len(output_bytes) + 1) · band/1e6⌉(#871, 명세 whitepaper/research/metering-cert-spec.md §4). |

**미터링 인증서 회로 버전 + 게스트 image-id 레지스트리(#929)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-metering_cert_circuit_version"></a>`metering_cert_circuit_version` | 3 version |  |  | 미터링 인증서가 증명 대상으로 삼는, 거버넌스가 고정한 회로 레이아웃(V3 트랜스크립트 리프, #929). |
| <a id="param-metering_cert_guest_image_id"></a>`metering_cert_guest_image_id` | OptionQuery storage-default |  |  | 미터링 인증서를 위해 거버넌스가 고정한 RISC0 게스트 image id(안전 구역, #945). |

**트랜잭션 수수료(라이브 값)**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-tx_fee_burn_percent_live"></a>`tx_fee_burn_percent_live` | 0 percent | [§9.1](#91-requirements) | D-0529 | base+length+weight 트랜잭션 수수료의 LIVE 소각 비율(0%; D-0529). |
| <a id="param-tx_fee_author_share_percent_live"></a>`tx_fee_author_share_percent_live` | 100 percent | [§9](#9-emission--supply) | D-0529 | 블록 작성자에게 지급되는 트랜잭션 수수료의 LIVE 몫(0% 소각 하에서 전체 수수료의 100%, D-0529). |
| <a id="param-tx_weight_to_fee"></a>`tx_weight_to_fee` | 5_000_000 base units/weight (1 base unit = 10^-18 FLOP) | [§9.1](#91-requirements) |  | WeightToFee ConstantMultiplier; 기본 수수료의 weight당 구성분(실효 하한: MinimumMultiplier = 1.0). 옐로페이퍼 §9.1. |
| <a id="param-tx_length_to_fee"></a>`tx_length_to_fee` | 5_000_000 base units/byte (1 base unit = 10^-18 FLOP) | [§9.1](#91-requirements) |  | LengthToFee ConstantMultiplier; 기본 수수료의 바이트당 구성분. 옐로페이퍼 §9.1. |
| <a id="param-tx_target_block_fullness_percent"></a>`tx_target_block_fullness_percent` | 75 percent | [§9.1](#91-requirements) |  | TargetedFeeAdjustment 승수의 혼잡 목표치(블록이 찰수록 수수료를 기본 하한 위로 올린다). 옐로페이퍼 §9.1. |
| <a id="param-tx_operational_fee_multiplier"></a>`tx_operational_fee_multiplier` | 5 ratio | [§9.1](#91-requirements) |  | operational 클래스 디스패치에 적용되는 할증 배수. pallet_transaction_payment 설정. |

**데이터 가용성**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-da_ephemeral_retention_blocks"></a>`da_ephemeral_retention_blocks` | 1_209_600 blocks | [§5.3](#53-the-verified-task-footprint--sovereign-da) | D-0412 | Ephemeral DA 블롭(견적/증명/트랜스크립트/I-O)의 보존 기간 W(14일); 세션 챌린지 윈도우를 제한한다. 옐로페이퍼 §5.3. |
| <a id="param-da_shard_count"></a>`da_shard_count` | 6 count | [§5.3](#53-the-verified-task-footprint--sovereign-da) | D-0402 | DA 소거 코딩 샤드 수 R = 6, Reed-Solomon 레이트 1/2(k = 3+3, 임의의 3개로 복원). 옐로페이퍼 §5.3. |
| <a id="param-da_min_replication_factor"></a>`da_min_replication_factor` | 3 count | [§5.3](#53-the-verified-task-footprint--sovereign-da) | D-0402 | DA Reed-Solomon 복원 임계값 k = 3(R개 샤드 중 임의의 k개로 복원); 거버넌스 가능한 da_shard_count의 하드 하한이므로 R < k(복원 불가)에는 도달할 수 없다. 옐로페이퍼 §5.3. |
| <a id="param-da_lease_deposit_per_byte"></a>`da_lease_deposit_per_byte` | 200 FLOP per 10^9 bytes (= 2e-7 FLOP/byte) | [§5.3](#53-the-verified-task-footprint--sovereign-da) | D-0412 | D-0412 리스 DA(모델 가중치)에 대한 환불 가능한 스팸 방지 예치금: deposit = bytes × DepositPerByte, 게시자에게 보유되며(검증자 수익이 아님), 프루닝/인출 시 전액 반환된다. |

**에이전트 지갑 / 세션 키**

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-agent_cap_window_blocks"></a>`agent_cap_window_blocks` | 86_400 blocks | [§6.2](#62-agent-autonomy--operating-without-per-action-consensus) |  | 지갑 및 세션 일일 지출 상한 윈도: 지갑 또는 세션 생성 시점, 또는 직전 리셋 시점으로부터 86,400 블록 이후 또는 그 시점의 첫 지출에서 리셋된다. |
| <a id="param-agent_identity_min_stake"></a>`agent_identity_min_stake` | 10 FLOP | [§12.3](#123-market-actor-threat-class) |  | 에이전트 아이덴티티를 등록하기 위해 잠기는 환불 가능한 최소 스테이크: 회수 불가능한 아이덴티티 비용이 아니라 자본 노출이다. 옐로페이퍼 §12.3. |
| <a id="param-circuit_breaker_window"></a>`circuit_breaker_window` | 60 blocks | [§6.2](#62-agent-autonomy--operating-without-per-action-consensus) |  | 고정된 에이전트 세션 키 서킷 브레이커 윈도우(60 blocks): 트랜잭션 수 또는 지출 중 어느 한 갈래(limb)라도 독립적으로 트립되며, 윈도우 종료까지 래치된 뒤 자동으로 리셋된다. 옐로페이퍼 §6.2. |
| <a id="param-circuit_breaker_tx_count"></a>`circuit_breaker_tx_count` | 100 count | [§6.2](#62-agent-autonomy--operating-without-per-action-consensus) |  | 에이전트 세션 키 서킷 브레이커의 트랜잭션 수 갈래(limb): circuit_breaker_flop_cap과 독립적으로 윈도우 내 100건의 tx에서 트립된다. 옐로페이퍼 §6.2. |
| <a id="param-circuit_breaker_flop_cap"></a>`circuit_breaker_flop_cap` | 250 FLOP | [§6.2](#62-agent-autonomy--operating-without-per-action-consensus) |  | 윈도우당 에이전트 세션 키 서킷 브레이커 최대 지출(60 blk / 100 tx / 250 FLOP 3종 조합). 옐로페이퍼 §6.2. |

**참조 전용** — 정식으로 문서화된 값이지만 단일 지점에만 존재하거나 아직 교차 언어 강제에 연결되지 않은 값이다(`enforce: false`).

| 파라미터 | 값 | § | 결정 | 설명 |
|-----------|-------|---|----------|-------------|
| <a id="param-validator_min_self_stake_ratio_percent"></a>`validator_min_self_stake_ratio_percent` | 20 percent | [§15.2](#152-onboarding-normative) |  | 후원 보증이 활성화된 경우의 레거시 최소 검증자 자기 스테이크 비율(§15.2). |
| <a id="param-validator_work_recency_window_blocks"></a>`validator_work_recency_window_blocks` | 86_400 blocks | [§15.2](#152-onboarding-normative) |  | PoUI 위원회 적격성을 위한, 수락된 검증 의무의 최근성 윈도(§15.2, R15.4c). |
| <a id="param-protocol_upgrade_approval"></a>`protocol_upgrade_approval` | 67 percent | [§14.2](#142-fip-binding) | GOV-A | 프로덕션 protocol_upgrade(Root) 트랙 승인(고정 BFT 2/3); APP_ROOT로 라이브(위에서 governance_root_track_approval + protocol_upgrade_support_floor로 강제됨). |
| <a id="param-protocol_upgrade_decision_period"></a>`protocol_upgrade_decision_period` | 28 days | [§14.2](#142-fip-binding) |  | [RATIFY] protocol_upgrade 트랙의 심의 윈도우. 옐로페이퍼 §14.2. |
| <a id="param-protocol_upgrade_enactment_timelock"></a>`protocol_upgrade_enactment_timelock` | 1_209_600 blocks | [§14.1](#141-requirements) |  | 1s 기준 14일 — Scheduler min_enactment_period(업그레이드 타임락). 옐로페이퍼 §14.1. |
| <a id="param-fip_decision_deposit"></a>`fip_decision_deposit` | RATIFY FLOP | [§14.2](#142-fip-binding) |  | [RATIFY] protocol_upgrade 레퍼렌덤에 대한 결정 예치금 스팸 장벽(FLOP 단위; 규모 TBD). 옐로페이퍼 §14.2. |
| <a id="param-emergency_override_timelock"></a>`emergency_override_timelock` | 259_200 blocks |  | SPEC-015 | 1s 기준 72시간 — pallet_emergency_override 비상 개입(break-glass) 타임락(root 전용). |
| <a id="param-emergency_override_cooldown"></a>`emergency_override_cooldown` | 604_800 blocks |  | SPEC-015 | 1s 기준 7일 — 비상 오버라이드 사이의 최소 간격. |
| <a id="param-governance_vote_locking_period"></a>`governance_vote_locking_period` | 604_800 blocks |  |  | 7일 컨빅션 VoteLockingPeriod(pallet_conviction_voting, 라이브).. |
| <a id="param-sudo_pallet_index"></a>`sudo_pallet_index` | 50 index | [§14.1](#141-requirements) | GOV-B | pallet_sudo — devnet/testnet 구간에서 Root를 부트스트랩한다; 메인넷 제네시스 인계 시점에 제거/무력화된다(GOV-B). 옐로페이퍼 §14.1. |
| <a id="param-subsidy_total_per_block"></a>`subsidy_total_per_block` | 16 FLOP | [§9](#9-emission--supply) | D-0436 | 반감 에라 0(1~2년차)에 Labs 8 + Foundation 8로, 96 FLOP 보상에 더해진다(옐로페이퍼 §9); 보상과 함께 반감하며(`era(b) = ⌊b / H⌋`: 합산 16 -> 8 -> 4 -> 2 -> 1), 보상이 하한에 도달하는 era 5(`b = 315,360,000`)부터 정확히 0이 된다. |
| <a id="param-emission_at_end_of_era6"></a>`emission_at_end_of_era6` | 12_109_823_904 FLOP |  | D-0436 | 2·R₀·H − R₀ = 12,109,823,904(보상 없는 제네시스 블록 0을 빼기 전에는 2·R₀·H = 12,109,824,000, R9.7)로, max_halvings=5 하에서 에라 6 종료 시점(블록 441,503,999, 약 14년차)에 도달한다 — 대체된 maxHalvings=6이 두었던 시점보다 한 에라 이르다(따라서 emission_at_end_of_era7에서 이름이 바뀌었다). |
| <a id="param-emission_through_halving_eras"></a>`emission_through_halving_eras` | 11_920_607_904 FLOP |  | D-0436 | R₀·H·63/32 − R₀ = 63,072,000 × (96+48+24+12+6+3) − 96 = 11,920,607,904(보상 없는 제네시스 블록 0을 빼기 전에는 11,920,608,000, R9.7) = max_halvings=5 하에서 반감 국면 전체(에라 5 종료, 블록 378,431,999, 약 12년차)의 누적 발행량. |
| <a id="param-floor_annual_emission"></a>`floor_annual_emission` | 94_608_000 FLOP |  | D-0436 | 영구 하한 테일: 3 FLOP/block × 31,536,000 blocks/yr(= 189,216,000 FLOP/era). |
| <a id="param-max_delegators_per_miner"></a>`max_delegators_per_miner` | 10_000 count | [§6.1](#61-primitives) | D-0530 | [DEPRECATED — D-0530] 운영자 자기 스테이크 전용 결정(§6.1, §15.2)으로 대체됨; 레거시 MinerStaking.MaxDelegatorsPerMiner 상수는 팰릿 정리 전까지 유지된다. |
| <a id="param-agent_daily_cap_autonomous"></a>`agent_daily_cap_autonomous` | 500 FLOP | [§6.2](#62-agent-autonomy--operating-without-per-action-consensus) |  | 시뮬레이터의 자율 에이전트 시나리오 일일 상한; 런타임은 전역 500 FLOP 상수를 강제하지 않고 create_wallet 시점에 각 지갑이 선택한 daily_cap을 저장한다; 옐로페이퍼 §6.2. |
| <a id="param-agent_per_tx_limit"></a>`agent_per_tx_limit` | 100 FLOP |  |  |  |
| <a id="param-attestation_outage_pause_cap_blocks"></a>`attestation_outage_pause_cap_blocks` | 14_400 blocks | [§13.0](#130-degraded-state-settlement-policy-normative) |  | R13.0e / O1에 따른 어테스테이션 의존 클록의 채널별 일시정지에 대한 4 h 상한으로, 설계되었으나 구현되지 않았다; 런타임이나 팔레트 구현 위치가 없다. 옐로페이퍼 §13.0. |
| <a id="param-da_endpoint_deposit"></a>`da_endpoint_deposit` | VFY (= 1 FLOP) |  |  | 검증자의 DA 서빙 엔드포인트 공지가 DaRegistry에 존재하는 동안 보유되는 환불 가능한 스팸 방지 예치금. 1 VFY = 1 FLOP. HoldReason 하에 보유되며, clear_endpoint 시 전액 해제된다. |
| <a id="param-da_max_endpoint_bytes"></a>`da_max_endpoint_bytes` | 256 bytes |  |  | DaRegistry에 저장되는 검증자 DA 서빙 엔드포인트 URL의 최대 UTF-8 바이트 길이(예: 'http://host:7000'). |
| <a id="param-validator_stake_value_coupled_floor"></a>`validator_stake_value_coupled_floor` | dynamic FLOP |  | D-0413 | D-0413 (C5): 거버넌스가 재설정하는 가치 연동 스테이크 하한 k·V_booked(스토리지 ValueCoupledStakeFloor, 기본값 0 = 기준선과 동일). |
| <a id="param-security_kappa_extractable"></a>`security_kappa_extractable` | 0.2 dimensionless |  | DEC-5 | 가정(ASSUMPTION) — 정리가 아니다; 거버넌스/DEC-5 리스크 입력값이다. κ = AlephBFT 안전성 침해에 성공했을 때 추출되는 실현 가치 V_booked의 비율; 이는 가치 연동 스테이크 하한이 기대는 레버다(k ≥ m·κ/(θ·N·σ·δ), κ에 선형 — k_threshold_scales_with_kappa). |
| <a id="param-da_deposit_max_step_factor"></a>`da_deposit_max_step_factor` | 100 ratio |  |  | pallet_da_registry MAX_DEPOSIT_STEP_FACTOR: 한 번의 set_deposit_per_byte 호출은 예치금을 어느 방향으로든 ≤100배까지만 이동시킬 수 있다(쇼크 방지; 하드 하한은 >0). |
| <a id="param-governance_param_max_step_pct"></a>`governance_param_max_step_pct` | 50 percent |  |  | MAX_STEP_PCT: Model 측 레일에서 불변식으로 증명된, 형식 모델(FORMAL-MODEL)의 인액트먼트당 비례 경계(100·\|Δ\| ≤ pct·\|old\|); 런타임은 동일한 비례 형식(FORM)을 파라미터별로(예: da_deposit_max_step_factor) 각자의 크기로 인스턴스화한다. |
| <a id="param-da_serve_or_slash_percent"></a>`da_serve_or_slash_percent` | 1 percent | [§5.3](#53-the-verified-task-footprint--sovereign-da) | D-0402 | 서브-오어-슬래시 라이브니스 경계: DA 감사에 실패한 검증자는 ≤1% 슬래시된다(사기가 아니라 제한된 슬래시). 옐로페이퍼 §5.3. |
| <a id="param-slash_liveness_percent"></a>`slash_liveness_percent` | 1 percent | [§13.2](#132-validator-consensus--da--leader-duties) | D-0409 | 라이브니스 결함 슬래시(300 blk 초과 수감). 옐로페이퍼 §13.2. |
| <a id="param-slash_equivocation_lone_percent"></a>`slash_equivocation_lone_percent` | 50 percent | [§13.2](#132-validator-consensus--da--leader-duties) | D-0420 | 단독 이중 서명 슬래시(상관 Eth2 스타일 커브; 180일 후 +50% 반환, ≥1/3 상관 시 → 100%). 옐로페이퍼 §13.2. |
| <a id="param-session_key_expiry_days"></a>`session_key_expiry_days` | 10 days | [§6.2](#62-agent-autonomy--operating-without-per-action-consensus) |  | 864,000 블록 세션 키 한도(옐로페이퍼 §6.2)를 목표 주기로 환산한 값: 중단 없는 1초 블록에서 약 10일이며, 벽시계 기준 상한은 아니다; 런타임 및 blocks_per_day와 대조 검사된다. |
| <a id="param-blackout_revoke_blocks"></a>`blackout_revoke_blocks` | 86_400 blocks | [§8](#8-performance-locked-vesting) |  | 성능 베스팅 블랙아웃: 용량이 86,400 연속 블록(약 1일) 동안 10% 미만이면 그랜트를 취소한다(1.0× 슬래시). 옐로페이퍼 §8. |
| <a id="param-performance_score_weights"></a>`performance_score_weights` | 40/30/20/10 percent | [§15.4](#154-selection--the-poui-gated-committee) |  | 복합 검증자 성능 점수: 40% 업타임 + 30% block_rate + 20% 정확도 + 10% 지연(1만분율); 로테이션 하한의 입력값. 옐로페이퍼 §15.4/§15.5. |

**교차 언어 이름(정식 ⇄ Rust ⇄ Lean ⇄ Quint).** 동일한 프로토콜 값이 관례상 언어마다 다른 식별자를 갖는다; 어떤 언어가 실제(데모가 아닌) 수치를 고정한 경우 값은 일치한다. 강제 행은 `check_params.py`에 의해 Rust 지점을 기준으로 값이 게이트된다.

| 파라미터 | Rust (runtime) | Lean (lean-proofs) | Quint (formal-specs) |
|-----------|----------------|--------------------------|----------------------|
| [`genesis_supply`](#param-genesis_supply) | `FLOP_TOTAL_SUPPLY` | `HalvingBoundary.genesisSupply` | `GENESIS_MICRO` |
| [`validator_min_stake`](#param-validator_min_stake) | `ValidatorInitialMinimumStake` | — | — |
| [`initial_block_reward`](#param-initial_block_reward) | `RewardInitialPerBlock` | `Emission.initialReward` | `P_EMISSION_CAP` |
| [`max_halvings`](#param-max_halvings) | `RewardMaxHalvings` | `Emission.maxHalvings` | `MAX_HALVINGS` |
| [`floor_reward`](#param-floor_reward) | — | `Emission.floorReward` | `FLOOR_MICRO` |
| [`miner_share_ppt`](#param-miner_share_ppt) | `MINER_SHARE_PPT` | `SettlementInt.BlockRewards.minerPpt` | — |
| [`validator_share_ppt`](#param-validator_share_ppt) | `VALIDATOR_SHARE_PPT` | `SettlementInt.BlockRewards.validatorPpt` | — |
| [`agent_share_ppt`](#param-agent_share_ppt) | `AGENT_SHARE_PPT` | `SettlementInt.BlockRewards.agentPpt` | — |
| [`staker_share_ppt`](#param-staker_share_ppt) | `STAKER_SHARE_PPT` | `SettlementInt.BlockRewards.stakerPpt` | — |
| [`reward_distribution_period_blocks`](#param-reward_distribution_period_blocks) | `RewardDistributionPeriodBlocks` | — | `PERIOD_BLOCKS` |
| [`gn_decay_factor_ppb`](#param-gn_decay_factor_ppb) | `DEFAULT_GN_DECAY_FACTOR_PPB` | — | `DEFAULT_DECAY_PPB` |
| [`finality_committee_premium_weight_ppm`](#param-finality_committee_premium_weight_ppm) | `FINALITY_COMMITTEE_PREMIUM_WEIGHT_PPM` | — | — |
| [`poui_submission_window_blocks`](#param-poui_submission_window_blocks) | `PouiEpochDurationBlocks` | — | — |
| [`poui_max_submissions_epoch`](#param-poui_max_submissions_epoch) | `PouiMaxSubmissionsPerEpoch` | — | — |
| [`governance_root_track_approval`](#param-governance_root_track_approval) | `APP_ROOT` | — | `P_APPROVAL_FLOOR` |
| [`babe_primary_probability_denominator`](#param-babe_primary_probability_denominator) | `PRIMARY_PROBABILITY` | — | — |
| [`aleph_max_data_branch_len`](#param-aleph_max_data_branch_len) | `MAX_DATA_BRANCH_LEN` | — | — |
| [`aleph_max_round`](#param-aleph_max_round) | `MAX_ROUND` | — | — |
| [`finality_committee_size`](#param-finality_committee_size) | `AlephMaxCommittee` | — | — |
| [`validator_attestation_threshold`](#param-validator_attestation_threshold) | `PouiDefaultValidatorAttestationThreshold` | — | — |
| [`attest_max_verifier_set_members`](#param-attest_max_verifier_set_members) | `AttestMaxVerifierSetMembers` | — | — |
| [`attest_max_claim_signatures`](#param-attest_max_claim_signatures) | `AttestMaxClaimSignatures` | — | — |
| [`poui_tee_v1_profile_id`](#param-poui_tee_v1_profile_id) | `POUI_TEE_V1_PROFILE_ID` | — | — |
| [`poui_tee_v1_profile_version`](#param-poui_tee_v1_profile_version) | `PouiTeeV1Profile` | — | — |
| [`validator_rotation_interval_blocks`](#param-validator_rotation_interval_blocks) | `RotationIntervalBlocks` | — | — |
| [`validators_to_eject`](#param-validators_to_eject) | `ValidatorsToEject` | — | — |
| [`validators_to_promote`](#param-validators_to_promote) | `ValidatorsToPromote` | — | — |
| [`validator_active_set_cap`](#param-validator_active_set_cap) | `ValidatorActiveSetCap` | — | — |
| [`validator_min_active_validators`](#param-validator_min_active_validators) | `ValidatorMinActiveValidators` | — | — |
| [`validator_rotation_churn_percent`](#param-validator_rotation_churn_percent) | `ValidatorRotationChurnPercent` | — | — |
| [`validator_min_scored_samples`](#param-validator_min_scored_samples) | `ValidatorMinScoredSamples` | — | — |
| [`ejection_cooldown_blocks`](#param-ejection_cooldown_blocks) | `EjectionCooldownBlocks` | — | — |
| [`validator_unbonding_blocks`](#param-validator_unbonding_blocks) | `ValidatorUnbondingPeriodBlocks` | — | — |
| [`validator_extended_downtime_slash_percent`](#param-validator_extended_downtime_slash_percent) | `ValidatorExtendedDowntimeSlash` | — | — |
| [`validator_growth_numerator`](#param-validator_growth_numerator) | `ValidatorGrowthNumerator` | — | — |
| [`validator_growth_denominator`](#param-validator_growth_denominator) | `ValidatorGrowthDenominator` | — | — |
| [`throughput_tripwire_gflops_per_sec`](#param-throughput_tripwire_gflops_per_sec) | `PouiGnThroughputCeilingGflopsPerSec` | — | — |
| [`refund_penalty_phi_percent`](#param-refund_penalty_phi_percent) | `ChannelRefundPenalty` | — | — |
| [`channel_max_settlement_turns`](#param-channel_max_settlement_turns) | `ChannelMaxSettlementTurns` | — | — |
| [`channel_max_session_activation_bytes`](#param-channel_max_session_activation_bytes) | `ChannelMaxSessionActivationBytes` | — | — |
| [`channel_max_merkle_path_len`](#param-channel_max_merkle_path_len) | `ChannelMaxMerklePathLen` | — | — |
| [`channel_base_per_turn`](#param-channel_base_per_turn) | `ChannelBasePerTurn` | — | — |
| [`channel_c_turn_fixed`](#param-channel_c_turn_fixed) | `ChannelCTurnFixed` | — | — |
| [`channel_dispute_window_blocks`](#param-channel_dispute_window_blocks) | `ChannelDisputeWindow` | — | — |
| [`channel_dispute_response_window_blocks`](#param-channel_dispute_response_window_blocks) | `ChannelDisputeResponseWindow` | — | — |
| [`channel_toploc_escalation_window_blocks`](#param-channel_toploc_escalation_window_blocks) | `ChannelToplocEscalationWindow` | — | — |
| [`channel_challenger_bond`](#param-channel_challenger_bond) | `ChannelChallengerBond` | — | — |
| [`channel_audit_forfeit_slash_ppm`](#param-channel_audit_forfeit_slash_ppm) | `ChannelAuditForfeitSlashPpm` | — | — |
| [`inference_fee_miner_share_ppt`](#param-inference_fee_miner_share_ppt) | `INFERENCE_FEE_MINER_SHARE_PPT` | — | — |
| [`inference_fee_validator_share_ppt`](#param-inference_fee_validator_share_ppt) | `INFERENCE_FEE_VALIDATOR_SHARE_PPT` | — | — |
| [`audit_fee_split_ppm`](#param-audit_fee_split_ppm) | `ChannelAuditFeeSplitPpm` | — | — |
| [`audit_fee_per_turn`](#param-audit_fee_per_turn) | `ChannelAuditFeePerTurn` | — | — |
| [`channel_ack_window_blocks`](#param-channel_ack_window_blocks) | `ChannelAckWindow` | — | — |
| [`min_force_open_escrow_for_failed_ack`](#param-min_force_open_escrow_for_failed_ack) | `MinForceOpenEscrowForFailedAck` | — | — |
| [`toploc_band_tau_accept_bf16_milli`](#param-toploc_band_tau_accept_bf16_milli) | — | `ToplocBandInt.tauAcceptBf16` | — |
| [`toploc_band_tau_slash_bf16_milli`](#param-toploc_band_tau_slash_bf16_milli) | — | `ToplocBandInt.tauSlashBf16` | — |
| [`toploc_band_eng29_threshold_milli`](#param-toploc_band_eng29_threshold_milli) | — | `ToplocBandInt.eng29Threshold` | — |
| [`max_decode_policies_per_model`](#param-max_decode_policies_per_model) | `MAX_DECODE_POLICIES_PER_MODEL` | — | — |
| [`tokens_per_byte_band_ppm_llama3`](#param-tokens_per_byte_band_ppm_llama3) | — | `MeteringCertInt.tokensPerByteBandPpmLlama3` | — |
| [`tx_fee_burn_percent_live`](#param-tx_fee_burn_percent_live) | `BurnFees` | — | — |
| [`tx_fee_author_share_percent_live`](#param-tx_fee_author_share_percent_live) | `AllFeesToAuthor` | — | — |
| [`tx_weight_to_fee`](#param-tx_weight_to_fee) | `TransactionPicosecondFee` | — | — |
| [`tx_length_to_fee`](#param-tx_length_to_fee) | `TransactionByteFee` | — | — |
| [`tx_target_block_fullness_percent`](#param-tx_target_block_fullness_percent) | `TargetBlockFullness` | — | — |
| [`tx_operational_fee_multiplier`](#param-tx_operational_fee_multiplier) | `OperationalFeeMultiplier` | — | — |
| [`da_ephemeral_retention_blocks`](#param-da_ephemeral_retention_blocks) | `DaEphemeralRetention` | — | — |
| [`da_shard_count`](#param-da_shard_count) | `DaReplicationFactor` | — | — |
| [`da_min_replication_factor`](#param-da_min_replication_factor) | `MIN_REPLICATION_FACTOR` | `k` | — |
| [`da_lease_deposit_per_byte`](#param-da_lease_deposit_per_byte) | `DaDepositPerByte` | — | — |
| [`agent_cap_window_blocks`](#param-agent_cap_window_blocks) | `AgentEpochLength` | — | — |
| [`agent_identity_min_stake`](#param-agent_identity_min_stake) | `AgentIdentityMinStake` | — | — |
| [`circuit_breaker_window`](#param-circuit_breaker_window) | `SessionKeysCircuitBreakerPeriod` | — | — |
| [`circuit_breaker_tx_count`](#param-circuit_breaker_tx_count) | `SessionKeysCircuitBreakerMaxTxs` | — | — |
| [`circuit_breaker_flop_cap`](#param-circuit_breaker_flop_cap) | `SessionKeysCircuitBreakerMaxSpend` | — | — |
| [`validator_min_self_stake_ratio_percent`](#param-validator_min_self_stake_ratio_percent) | `ValidatorMinSelfStakeRatio` | — | — |
| [`validator_work_recency_window_blocks`](#param-validator_work_recency_window_blocks) | `ValidatorWorkRecencyWindow` | — | — |

<!-- END GENERATED: param-table -->

**파생 수량 및 서술적 상수** — 구조적 값, 공식, 메커니즘 상수로서 위의 기계 검증 수치 계약에는
포함되지 *않는다*(그래서 params 파일이 아니라 여기에 위치한다):

| 파라미터 | 값 | § | D-id |
|-----------|-------|---|------|
| 블록 간격 / 런타임 길이 엔벨로프 | 1 s / 최대 5 MiB, 75% Normal; 측정된 용량 프로파일 없음 | [2.1](#21-requirements) / [5.2](#52-block--transaction-sizing) | D-0401, D-0502 |
| 파이널리티 / BFT 내성 | 순서가 정해지면 결정적; 지연 목표 없음 / 비잔틴 위원회 좌석 엄격히 < ⅓ | [2.1](#21-requirements) | D-0401, D-0501, D-0502 |
| 위원회 선정 | PoUI 게이트: 스테이크 + 최근 수락된 검증 임무(`hp-consensus::select_committee`; R15.4c) | [2.1](#21-requirements) / [2.3](#23-safety--the-three-sub-proofs) / [15.4](#154-selection--the-poui-gated-committee) | D-0401, D-0439 |
| 합의 엔진 | BABE 블록 작성 + 스테이크 BFT-DAG **AlephBFT 파이널리티**; `pallet_aleph` 런타임 **인덱스 104**가 `LastFinalized`를 `AlephFinalizedPrefix`에 보고한다 | [2](#2-consensus) | D-0401 |
| 마이너/검사자 시빌 비용 / 아이덴티티 | ≥10k FLOP 기본 + 용량 예치금 + 어테스트된 인벤토리 + 활성 갱신형 상한 | [2.4](#24-sybil-model--miner-and-checker-identities) | D-0418, D-0433 |
| 검증자 슬래싱 | 라이브니스 1 %(300 blk 초과 수감) / 장기 다운타임 5 %(24시간 초과 축출); **이중 서명은 상관 기반** — 단독 50 %(180일 후 +50 % 반환) → ≥⅓ 상관 시 100 %; 담합 / 증거 위조 / TEE / 이중 지불 100 % + 퇴출 + 블랙리스트 | [11](#11-security-invariants) / [13.2](#132-validator-consensus--da--leader-duties) | D-0409, D-0420 |
| 언본딩 슬래시 락 | 세션/분쟁/감사가 열려 있는 동안에는 언본드를 완료할 수 없다; 언락 쿨다운 ≥ 분쟁 윈도우 + 해소 기간(마이너 `[LIVE]`; 검증자 동결 및 마진 구성은 E.57) | [6.1](#61-primitives) / [13](#13-failure-semantics--actor--failure-matrix) | D-0419 |
| 검증자 로테이션 | [`RotationIntervalBlocks`](#param-validator_rotation_interval_blocks); **스테이크 순**으로, 검증된 작업 + 라이브니스 **최소 성능 하한**에 의해 게이트된다; [퇴출](#param-validators_to_eject)/[승격](#param-validators_to_promote) = 50, [쿨다운](#param-ejection_cooldown_blocks) 약 7일 | [6.1](#61-primitives) / [13.2](#132-validator-consensus--da--leader-duties) | D-0416, D-0409 |
| `G_n` / `F_eff` | `F_eff/10⁹`; 결정적 레퍼런스 작업량 회계(`hp_poui::flop_meter`)이며, 물리적 명령어 측정과는 구별된다 | [4.1](#41-requirements) / [4.2](#42-the-op-count-model) | D-0405, D-0501 |
| 처리량 트립와이어 상한 | `gn·1000/latency_ms` > [**2,000,000 GFLOPS/s**](#param-throughput_tripwire_gflops_per_sec)이면 거부한다(거부 전용이며 `gn`을 절대 클램프하지 않는다; 거버넌스 가능, 기본 켜짐) | [4.2](#42-the-op-count-model) | D-0405 |
| 휴리스틱(정합성 확인 전용) | `2·P_active·N + 2·n_layer·n_ctx·d_attn`, 약 2–3× | [4.2](#42-the-op-count-model) | D-0405 |
| `model_hash` | 측정된 dm-verity 머클 루트(재현 가능한 패커 `[tools/modelpack]`), RTMR3로 확장되고, `(model, precision)`별로 레지스트리에 고정되며, fail-closed `Vk::V3` | [3.3](#33-tier-1--tee-attestation--measuring-model_hash-optional--hard-tier) | D-0404 |
| 검증자 어테스테이션 쿼럼 | [**BFT 비율, 기본 2/3**](#param-validator_attestation_threshold)(`ValidatorAttestationThreshold: Perbill`, 루트 거버넌스 가능); 서로 다른 활성 검증자 서명이 `ceil(active_count × threshold).max(1)`개 필요하다 | [3.6](#36-tier-4--on-chain-settlement-zk-aggregation--validator-bft-quorum), [13.3](#133-validator-attestation-quorum-bft-fraction) | D-0414 (D-0406 대체) |
| 다이렉트 레일 어테스테이션 익스트린식 | active=100/q=67에서 18,434 B; 지원되는 최대치인 active=200/q=134에서 36,859 B; 처리량 추론 불가 | [5.3](#53-the-verified-task-footprint--sovereign-da) | D-0502 |
| 프로토콜 DA(주권 검증자, §5.3) | [`R = 6` 샤드](#param-da_shard_count), Reed–Solomon **레이트 ½**(k=3+3, 임의의 3개로 복원); `Ephemeral` [보존 기간 `W` = **14 d**](#param-da_ephemeral_retention_blocks); 감사 기한 약 5분; 서브-오어-슬래시 1%로 제한(`Liveness`); **바이트당 DA 수수료 없음** — DA는 검증자 보상 몫으로 재원이 조달되는 검증자 의무다(D-0412) | [5.3](#53-the-verified-task-footprint--sovereign-da) | D-0402, D-0412 |
| DA 리스 모델 스토리지(D-0407) | 기본 리스 기간 **180 d**; 기간 단위 / 톱업 단위 **30 d**; `lease_end` **30 d** 전 만료 경고(1회성, 지연 실행); 유예 **14 d**(= `W`); **스토리지 수수료 없음** — `top_up_lease`는 무료다(tx 비용만); **환불 가능한** 스팸 방지 예치금 = `bytes × DepositPerByte`가 **보유**되며(전용 hold reason), 프루닝 / 자발적 인출 시 **전액 반환**된다(D-0412); 사용 **핀**은 프루닝을 막는다; 프루닝은 복구 가능하며(결정적 루트), 재활성화하면 예치금이 다시 잠긴다 | [5.3](#53-the-verified-task-footprint--sovereign-da) | D-0407, D-0412 |
| 세션 키 만료 / 상한 | **≤10 d**(1 s 기준 `SessionKeysMaxDuration = 864,000` 블록); tx당 + 일일 상한; 서킷 브레이커 60 blk / [100 tx](#param-circuit_breaker_tx_count) / [250 FLOP](#param-circuit_breaker_flop_cap) | [6.2](#62-agent-autonomy--operating-without-per-action-consensus) | — |
| 컴퓨트 채널(세션 정산) | 협조적 라이프사이클의 주요 포함 2건과 증거/분쟁 호출; 바이트 수와 검증량은 턴 수에 따라 증가한다; 에스크로 = 마이너에게 지급되는 예약 용량(미사용 환불 없음, 정산 수수료 없음); [**분쟁 윈도우 7 d**](#param-channel_dispute_window_blocks) ≤ DA `W` = 14 d; [**분쟁 응답 윈도우 2 h**](#param-channel_dispute_response_window_blocks); `top_up_escrow` | [12.1](#121-sessions--attested-streaming--aggregate-settlement) / [12.2](#122-per-identity-capacity-reservation) | D-0403 |
| Tx 모델 / 조합성 | 계정 + 단조 증가 `u32` nonce(2차원 레인은 선택 사항이며 채택하지 않음); UTXO 네이티브는 **채택하지 않는다**; 옵코드 유사 조합성은 **선언적 지출 조건 레이어**(Miniscript 스타일) + 멀티시그/프록시/타임락/HTLC로 제공한다; UTXO 사이드 레일 = 향후 마이크로페이먼트 옵션 | [6.3](#63-transaction--state-model) / [6.4](#64-collaborative-pool--composition) | D-0401, D-0417 |
| 캘리브레이션된 호스트 용량 | 경험적으로 시간 측정된 작업; HARD는 합산된 `(SKU,count)` 상한의 90% 이하; 7일 리스 | [7](#7-hardware-calibration--drift) | D-0433 |
| UnlockRate / 블랙아웃 | `R_p²` / 86,400 블록 동안 10% 미만 → 취소 | [8](#8-performance-locked-vesting) | — |
| `T_lock` | 쌍별로 고유하다; 기본 7,200 FLOP 블록 대 3,600 s 카운터 기간은 미할당 포함 예산이 0이다 | [10](#10-htlc-atomic-swap) | — |

위에서 참조된 미정/미설정 값들은
[부록 E — 미해결 명세 항목](#appendix-e--open-specification-items)에 번호가 매겨진 채움 스텁으로 명시되어 있다.

---
