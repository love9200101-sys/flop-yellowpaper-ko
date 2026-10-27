## 7. 하드웨어 캘리브레이션과 드리프트

```
C_ceiling = Σ_s n_s C_sku(s)
C_emp   (miner-proposed; accepted iff floor(C_emp · Δblocks · u_min / 10⁶) ≤ Σ G_job)
C_hard = min(C_emp, floor(C_ceiling · d_hard / 10⁶))
C_effective ≔ C_emp                                                (SOFT)
              min(C_hard, floor(C_ceiling_current · d_hard / 10⁶)) (HARD)
```

`Σ G_job`은 정수 `G_n` 단위로 검증된 참조 작업량이다; `Δblocks`는 1s 블록 시간축에서 초를 측정하므로, `C_emp`, `C_ceiling`, `C_effective`는 `G_n/s` 단위의 속도이다. 수락된 상한은 작업 베스팅을 위해 `G_n/day` 단위의 `B_p = C_effective · 86,400`도 산출한다. 마이너 스테이킹 어댑터는 용량 스테이크 계수를 적용하기 전에 `B_p`를 86,400 s/day로 나눈다; PoUI 및 세션 적립 게이트는 순간 속도 `C_effective`를 읽는다. 기존의 직접 PoUI 게이트는 증명당 작업 수를 지속 시간 계수 없이 이 속도와 비교한다; 그 차원 불일치는 #1597의 단위 감사에 기록되어 있다. 여기서 `u_min ≔` [`calibration_min_utilization_ppm`](#param-calibration_min_utilization_ppm)이고
`d_hard ≔` [`calibration_provisional_discount_ppm`](#param-calibration_provisional_discount_ppm)이다.
`C_effective`는 활성화된 상한이다. `C_hard`는 저장된 HARD 티어 상한이다; 갱신 시 현재의 거버넌스
인벤토리 상한은 이를 조일 수는 있으나 올릴 수는 없다. 마이너가 `C_emp`를 제안한다; 작업 게이트는 비교 전에
요구량을 내림(floor)하고, 버스트가 충당하는 어떤 상한이든 수락한다. 그러한 상한 중 가장 큰 것을 요구하지는
않으므로 더 낮은 주장도 수락된다(M13 캘리브레이션 샌드배깅 공백).

### 7.1 진입 — 벤치마크 버스트

**R7.1.** 마이너는 독립적으로 발행되고 정확성이 검증된 캘리브레이션 작업의 체인 시간 기준 버스트를 거친
후 **MAY** 진입할 수 있다. 각 크리덴셜은 마이너, 태스크 해시, 예상 작업량, 발행/해결 블록, 팩 ID, 출력
커밋먼트를 **MUST** 바인딩해야 하며; **MUST** 주장된 버스트 시작 시점보다 이르지 않게 발행된 것이어야
하고 **MUST** 한 번만 소비되어야 한다.

**R7.1a.** `accept_benchmark_burst`는 다음 경우에 **MUST** 닫힘 실패(fail closed)해야 한다: 상한이 0인 경우;
[`calibration_min_verified_jobs`](#param-calibration_min_verified_jobs) 미만인 경우;
[`calibration_min_burst_blocks`](#param-calibration_min_burst_blocks)보다 짧은 윈도우; 만료되었거나
미검증된 크리덴셜; `floor(C_emp · Δblocks · u_min / 10⁶)` 미만의 검증된 작업량(`C_effective`가 아니라 실측 상한 기준);
`C_effective`에 대한 용량 비례 자기 스테이크 부족; 또는
[`calibration_min_recalibration_interval_blocks`](#param-calibration_min_recalibration_interval_blocks)
이내에 수락된 초기 상한. 용량 예치금은 상한 활성화 전에 **MUST** 존재해야 한다.

- **SOFT 티어** — 어테스테이션된 GPU 인벤토리 없음; 상한은 실측 작업량과
  용량 스테이크에 의해 제한되고,
  서지 승수 + 스팟 체크 노출([`soft_tier_spot_check_rate_ppm`](#param-soft_tier_spot_check_rate_ppm))을 수반한다.
- **HARD 티어** — 어테스테이션이 최대
  [`calibration_max_gpu_inventory_entries`](#param-calibration_max_gpu_inventory_entries)개의 서로 다른
  `(SKU,count)` 항목을 바인딩한다. 호스트 상한은 장치별 거버넌스 상한의 합에
  [`calibration_provisional_discount_ppm`](#param-calibration_provisional_discount_ppm)로 할인을 적용한 뒤
  실측 처리량으로 제한한 값이다.
  **R7.1b.** 거버넌스 SKU 상한이 하나라도 누락된 어테스테이션된 인벤토리는 **MUST** 닫힘 실패해야 하며 **MUST NOT**
  SOFT로 하향 전환되어서는 안 된다. 인벤토리 항목은 SKU 기준으로 **MUST** 정규화(canonicalize)되어야 한다.

**R7.1c.** 캘리브레이션은 마이너 호스트 단위이다. `C_emp`는 연결된 모든 GPU와 프로덕션 배칭/동시성을 한 번
포함하며; GPU 수, 채널 수, 세션 수, 배치 크기로 **MUST NOT** 곱해져서는 안 된다.

*SOFT 티어는 비-TEE 경로(§3.2, R3.2)이며, 그 종단 간 정산/분쟁 정책은 E.33이다.*

### 7.2 갱신형 상한

**R7.2.** 수락된 상한은
[`calibration_lease_blocks`](#param-calibration_lease_blocks)의 리스(lease)이다. 정확한 만료 경계에서 모든
등록, PoUI, 스테이크/베스팅, 컴퓨트 채널 소비자는 **MUST** 닫힘 실패해야 한다.
`renew_benchmark_cap`은 마이너가 선언한 갱신 트리거 시점 이후에 발행된 최소
[`calibration_renewal_min_verified_jobs`](#param-calibration_renewal_min_verified_jobs)개의 신규 원샷
작업을 요구한다. 그 트리거는 **MUST NOT** 미래이거나
[`calibration_renewal_max_age_blocks`](#param-calibration_renewal_max_age_blocks)보다 오래된 것이어서는
안 된다. 이들의 집계 검증 작업량은
`floor(C_effective × max(1, current_block − renewal_trigger) × u_min / 10⁶)`을 **MUST** 충당해야 한다.
작업 수만으로는 상한을 **MUST NOT** 갱신해서는 안 된다. 각 성공적인 갱신은 해당 갱신 직전에 저장된 값에 비해 실측 용량이나 유효 용량 어느 쪽도
**MUST NOT** 증가시켜서는 안 된다. 이후 거버넌스 SKU 상한이 올라가더라도 이전 갱신에서 잃은 용량은 복원되지 않는다;
용량 증가에는 §7.1에 따른 새로운 최초 수락이 필요하다.

수락된 유효 상한은 리스 기간 동안 **MUST** 동결 상태로 유지되어야 한다. 거버넌스에 의한 SKU 상한 변경은
이미 수락된 상한을 **MUST NOT** 조용히 변경하거나 비활성화해서는 안 된다. 변경된 상한은 다음 버전
갱신 또는 초기 수락 시점에 적용되며, 그 시점에 갱신 용량을 축소하는 방향으로만 작용할 수 있다.

고정 3단계 Dyno는 제거되었다. 대체 레거시 상한이나 거버넌스 강제 파이널라이즈 경로는 존재하지 않는다.
장기 윈도우 통계적 성능 저하/하향 조정은 E.22로 남아 있으며; 그때까지 갱신은 지속적인 정확한 실행,
라이브니스, 최소 단기 윈도우 처리량을 증명하지만 상한을 올리거나 통계적으로 재추정하지는 않는다.

### 7.3 드리프트와 재캘리브레이션

드리프트 탐지는 Synthetic Task Engine을 통한 카나리 태스크(고정 시드, 정답 기지)를 기반으로 하며,
*정확성*(SDC와 정밀도 속임을 잡아낸다 — INT4는 동일 연산 수에서 출력을 바꾼다)과 *타이밍*
(스로틀링)을 검사한다. 정확성 카나리 자체는 가동 중이며(§8.1); 통계 계층 — EWMA 기준선 +
관리도(control chart) → 위반 시 재캘리브레이션, 그리고 MLPerf 타당성 상한 — 은 설계 단계이다(E.22).

**R7.3.** 마이너 슈퍼바이저는 모든 프로세스/호스트 재시작과 체인 재연결 후, 그리고 리스 잔여 기간이 하루가
되었을 때 **MUST** 갱신을 요청해야 한다. 만료되었으나 변경되지 않은 호스트는 갱신 팩으로 **MAY** 복구할 수 있다.
`(SKU,count)` 인벤토리 또는 장치/드라이버/펌웨어 지문이 변경되면 이전 상한은 **MUST**
무효화되어야 하며 새로운 §7.1 버스트가 **MUST** 완료되어야 한다. 갱신 카나리를 놓치면 상한이 만료된다.
열려 있는 세션은
스냅샷된 상한/버전을 상한선으로 유지하며; 이후의 버전 갱신은 정산을 축소할 수 있고, 새
세션은 최신 `calibration_version`을 사용한다.

독립적인 Ghost 발행자는 유기적 수요와 무관하게 캘리브레이션 리저브를 **MUST** 유지해야 한다:
저장된 상한이 없는 호스트에 64개 작업, 있는 호스트에 8개. 마이너가 트리거한 수락은 마이너가 선택한
작업을 승인하는 것이 아니다. 초기 교체는 스로틀링되며; 갱신은 신규 크리덴셜을 소비하고 용량을
증가시킬 수 없기 때문에 스로틀링되지 않는다.

드리프트와 속임은 시그니처로 **MUST** 구별되어야 한다: 드리프트는 느리고 단조적이며
온도와 상관되고 *출력은 정확*하다; 속임은 계단식 변화, 잘못된 출력, 또는 어테스테이션된 상한을
초과하는 처리량이다. **지연 조정:** `Adjusted_G_n = G_n · clamp(target/actual, 0.5, 1.5)`
(추적 중; 보상 가중은 E.22).

### 근거 및 출처 *(비규범적)*

출처(provenance): `D-0405`(측정된 `G_n`), `D-0418`(용량 스테이크), `D-0433`(신속 진입,
갱신형 상한, 생애주기 재검증). 런타임 정합:
`hw-calibration::{accept_benchmark_burst,effective_cap,discounted_cap,renew_benchmark_cap}`
은 초기 작업 게이트에는 실측 상한을, 본딩과 갱신에는 티어에 따라 달라지는 유효 상한을 사용한다. 거버넌스
하한값에서 600 블록 동안 64 jobs × 1,000 G는 최대 `C_emp = 213`까지 허용한다; 요구 작업량은 63,900 G이므로
64,000 G는 통과한다. 가격 산정된 마이너 BOM:
validator-miner-hardware-costs.md,
gn-unit-audit.md. SDC/드리프트 탐지기
문헌: arXiv:2502.12340, arXiv:2605.04213, arXiv:2604.10390. 형식 검증:
`FlopSpecs/CalibrationFastPath.lean`,
`FlopSpecs/CalibrationDrift.lean`,
`FlopSpecs/Calibration.lean`. 미결: E.22
(통계적 성능 저하, 캐시 인지 계량, 집계 다중 채널 예약, MLPerf 데이터).
상태: [부록 H](#appendix-h--conformance--implementation-status-matrix).

---
