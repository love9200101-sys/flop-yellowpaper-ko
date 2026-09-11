## 4. 유효 FLOP 미터링

### 4.1 요구사항

- **R4.1 — 단위.** 작업은 버전이 부여된 참조 작업 단위(reference-work unit) `F_eff`로 **MUST** 회계 처리되어야 하며, `G_n = floor(F_eff / 10⁹)`이다. 이는 결정론적 프로토콜 회계 규약이다; 물리적 FP16/INT8/INT4 명령어 수, 에너지, 지연, 인증서 가중치와는 구별된다.
- **R4.2 — 참조 작업 회계.** `G_n`은 공유 결정론적 `no_std` 프리미티브(`hp_poui::flop_meter`, `tee-bridge/inference/attestor/flop_meter.py`에 미러링됨)에 의해 실행 입력으로부터 **MUST** 계산되어야 하며, 단순한 `2·P·N`으로부터 도출되어서는 안 된다. 입력에는 프롬프트/컨텍스트 길이, 생성 토큰 수, 활성 파라미터/MoE 항, 그리고 참조 공식이 정의하는 어텐션 항이 포함된다. 미터를 TEE 내부에서 실행하는 것이 미터를 물리적 명령어 카운터로 만들거나, 모델링되지 않은 라우팅, 캐시, 배칭, 추측 디코딩(speculative decoding) 작업을 확립하는 것은 아니다.
- **R4.3 — 트립와이어는 거부 전용이다.** 건전성(sanity) 트립와이어는 암시된 처리량 `gn·1000/latency_ms`가 [`throughput_tripwire_gflops_per_sec`](#param-throughput_tripwire_gflops_per_sec)를 초과하는 클레임을 **MUST** 거부해야 한다(절대 클램프하거나 재작성하지 않음)(fail-closed, 거버넌스 토글, 기본 활성). GPU별 MLPerf 상한과 과소 보고 하한은 어테스테이션된 GPU id / 어테스테이션된 토큰 수가 바인딩되는 곳(트랜스크립트 리프 `g_n`)에서 활성화된다.
- **R4.4 — 표현.** 정산된 `G_n`은 10억 참조 FLOP 단위의 정수 개수를 나타내는 부호 없는 카운트이다. 직접 레일 클레임은 `u64`를 사용한다; 세션 리프, 영수증, 집계, 잔고는 `u128`을 사용한다. 둘 모두 서명/해시되는 프리이미지에서는 고정 폭 리틀 엔디언 정수를, 호출과 저장소에서는 SCALE의 고정 폭 인코딩을 사용한다. 구현은 `F_eff / 10⁹`에서 한 번만 floor 연산을 수행하고, 대상 폭을 벗어나는 값을 거부하며, 검사된(checked) 집계를 **MUST** 사용해야 한다; 구현은 반올림, 클램프, 과거 값의 재해석, 또는 이 필드에 물리적 FP16/INT8/INT4 연산, 줄(joule), 지연, 인증서 가중치 의미를 부여하는 것을 **MUST NOT** 해서는 안 된다. 그러한 측정값은 별도로 타입이 지정된 텔레메트리이다.
- **R4.5 — 캐시 회계.** 와이어 프로파일 v1은 재사용된 KV 캐시 접두사(prefix)를 포함하여 참조 공식의 전체 프롬프트/컨텍스트 항을 청구한다. 캐시 재사용은 지연이나 물리적 작업을 줄일 수 있지만 정산된 `G_n`을 할인하지 않는다. 증명에 바인딩된 캐시 할인은 새 미터/프로파일 버전을 요구한다; 이는 기존 리프 또는 영수증 금액을 묵시적으로 변경해서는 **MUST NOT** 안 된다(E.22; #1153).

### 4.2 연산 수 모델

참조 작업 카운트는 활성 파라미터(MoE 인식), 2차 어텐션 항, 임베딩을 회계 처리한다; 이는 참조 모델에 대한 해석적 카운트에 대해 KAT로 고정되어 있다(Llama-3-8B → 16, Llama-3-70B → 140 `G_n`/토큰; Rust ⇄ Python 패리티). 교차 검사(CUPTI/DCGM을 통한 GPU 성능 카운터; `nvml`을 통한 에너지)는 인클레이브 내부에서 물리적 한계로 읽힌다.

단순 휴리스틱은 **건전성 검사 전용**이며(R4.3), 절대 청구 금액이 아니다:

```
F_eff ≈ 2 · P_active · N  +  2 · n_layer · n_ctx · d_attn   (attention term)
```

토큰당, 레이어당: QKV `6d²`, 어텐션 출력 `2d²`, FFN `16d²`. 단순 `2·P·N`은 약 2–3× 정확도이다(2차 어텐션 항, 임베딩/언임베딩, LayerNorm/softmax를 생략한다; MoE는 *활성* 파라미터를 사용한다; KV 캐시는 FLOP 효과가 아니라 대역폭 효과이다). 참조 예시(≈, 명시된 아키텍처 가정 하에서): Llama-3-8B 16, DeepSeek-V3 74, Llama-3-70B 140 `G_n`/토큰. 독점(proprietary) 모델 수치는 프로토콜 측정값이 아니다.

**가격 대 작업.** 가격은 컨텍스트/모델 승수를 포함하여 토큰 단위로 제시되는 반면, 작업은 `F_eff`로 미터링된다(`flop-poui` 수수료 `(base+priority)·gflops/1000·precision_mult`). 트랜잭션 수수료의 수령자 분배는 §9 / Appendix D에 명시되어 있다.

### 근거 및 출처 *(비규범적)*

거부 전용 트립와이어(청구 금액을 절대 재작성하지 않음)를 가진 참조 작업 `G_n`은 `D-0405`이다; `D-0501`은 미터가 정확한 물리적 측정이 아니라 회계 규칙임을 명확히 한다. 근거:
latency-gflop-calibration.md,
workload-class-metering.md,
gpu-precision-tripwire-note.md. 형식 검증:
`FlopSpecs/Calibration.lean`,
`FlopSpecs/Computable.lean`. 리뷰 증거:
[prepublication-evidence.md](research/prepublication-evidence.md). 미결: E.34(비LLM 워크로드
클래스) 및 E.22(증명에 바인딩된 캐시 할인). 상태:
[Appendix H](#appendix-h--conformance--implementation-status-matrix).

---
