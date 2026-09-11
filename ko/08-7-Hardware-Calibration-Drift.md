## 7. 하드웨어 캘리브레이션과 드리프트

```
C_emp = floor(Σ G_job · 10⁶ / (Δblocks · u_min))
C_hard = min(C_emp, d_hard · Σ_s n_s C_sku(s))
```

### 7.1 진입 — 벤치마크 버스트

**R7.1.** 마이너는 독립적으로 발행되고 정확성이 검증된 캘리브레이션 작업의 체인 시간 기준 버스트를 거친
후 **MAY** 진입할 수 있다. 각 크리덴셜은 마이너, 태스크 해시, 예상 작업량, 발행/해결 블록, 팩 ID, 출력
커밋먼트를 **MUST** 바인딩해야 하며; **MUST** 주장된 버스트 시작 시점보다 이르지 않게 발행된 것이어야
하고 **MUST** 한 번만 소비되어야 한다.

**R7.1a.** `accept_benchmark_burst`는 다음 경우에 **MUST** 닫힘 실패(fail closed)해야 한다: 상한이 0인 경우;
[`calibration_min_verified_jobs`](#param-calibration_min_verified_jobs) 미만인 경우;
[`calibration_min_burst_blocks`](#param-calibration_min_burst_blocks)보다 짧은 윈도우; 만료되었거나
미검증된 크리덴셜; `C_emp · Δblocks · u_min` 미만의 검증된 작업량; 용량 비례 자기 스테이크 부족; 또는
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
`C_effective × max(1, current_block − renewal_trigger) × calibration_min_utilization_ppm / 10^6`을 **MUST** 충당해야 한다.
작업 수만으로는 상한을 **MUST NOT** 갱신해서는 안 된다. 갱신은 실측 용량이나 유효 용량 어느 쪽도
**MUST NOT** 증가시켜서는 안 된다.

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
갱신형 상한, 생애주기 재검증). 가격 산정된 마이너 BOM:
validator-miner-hardware-costs.md. SDC/드리프트 탐지기
문헌: arXiv:2502.12340, arXiv:2605.04213, arXiv:2604.10390. 형식 검증:
`FlopSpecs/CalibrationFastPath.lean`,
`FlopSpecs/CalibrationDrift.lean`,
`FlopSpecs/Calibration.lean`. 미결: E.22
(통계적 성능 저하, 캐시 인지 계량, 집계 다중 채널 예약, MLPerf 데이터).
상태: [부록 H](#appendix-h--conformance--implementation-status-matrix).

---
