## 5. 온체인 / 오프체인 아키텍처 및 사이징

### 5.1 분할

| 온체인 (최소, 합의 핵심) | 오프체인 (무거움, 신뢰되지 않으나 검증됨) |
|----------------------------------------|-------------------------------------------|
| 검증자 어테스테이션 검증(sr25519 서명 + BFT 쿼럼 + `report_data`); 재전송 방지; `G_n` 크레딧 부여 | 추론 실행; 쿼트 생성(TEE 기반인 경우) |
| 증명 집계 머클 루트; 분쟁 판정 + 슬래싱 | DCAP 검증(tee-bridge, `dstack-verifier`) — 검증자, 오프체인 |
| 스테이킹, 베스팅, 레지스트리, 캘리브레이션 기준선, HTLC 정산; **DA 커밋먼트(`DataRef`) + 서브 오어 슬래시(serve-or-slash) 감사**(`pallet_da_registry`) | TOPLOC 커밋 + 재실행; 증명/쿼트/I-O를 위한 **소버린 검증자 DA**(§5.3); 크로스체인 릴레이 |

**검증 비대칭(규범적).** 체인은 모델을 재실행해서는 **MUST NOT** 안 된다; 체인은 어테스테이션과 분쟁만을 판정한다. 신뢰는 (a) *주장된 경우의* 하드웨어 RoT, (b) 경제적 슬래싱, (c) 독립 재실행으로 이동한다 — 결코 실행자에게로는 아니다.

### 5.2 블록 및 트랜잭션 사이징

런타임은 5 MiB 최대 블록 길이를 설정한다: Normal 디스패치는 최대 3,932,160 B(75%)를 소비할 수 있고, Operational 디스패치는 전체 5,242,880 B를 사용할 수 있다. 독립적인 ref-time 상한은 블록당 750,000,000,000이며, 그중 562,500,000,000이 Normal 디스패치에 가용하다; 증명 크기(proof size) 또한 가중치 차원이다. 기본 블록/익스트린식 작업과 경쟁 트래픽이 이 엔벨로프를 소비한다.

이는 어드미션 최대치이며, 전파, 실행, 처리량, 서빙, 파이널리티 프로파일이 아니다. 이전의 125,000 B 시나리오는 D-0502에 의해 철회되었다. 바이트, ref-time, 증명 크기, 상태 접근, 서빙 용량, 파이널리티 통신 중 어느 것이 먼저 병목이 되는지는 E.46의 런타임 및 네트워크 측정을 요구한다.

### 5.3 검증된 태스크 풋프린트 및 소버린 DA

검증된 태스크는 바이트 자체가 아니라 블롭당 약 32 B만을 온체인에 **MUST** 커밋해야 한다. 약 2 MB `StarkProof` 상한은 **제출 호출 데이터(call-data) 경로**이며(익스트린식에 일시적으로 실려 블록과 함께 프루닝된다), 영구 저장소가 아니다 — 증명/쿼트/I-O는 DA에 존재하고 해시로 참조된다:

```
direct-rail attestation Vec bytes/claim = compact_len(quorum_size) + 275 B × quorum_size
off-chain (DA, by DataRef)              = proof_data, TEE quote (5–10 KB), event log (≤256 KB)
```

현재 고정 필드 SCALE 크기는 `ValidatorAttestation`당 275 B이다; 서명되는 부분집합은 179 B이다. 서명 번들은 쿼럼 크기에 선형이다. 소스에서 확인된 SCALE 픽스처는 런타임 팔레트/호출 인덱스, v5 bare 프리앰블, 외부 compact 길이, 그리고 내장된 검증자 서명을 포함한다. 기본 3분의 2 규칙 하에서 100명의 활성 검증자는 67개의 서명을 요구한다: 인수 벡터는 18,427 B이고 완전한 익스트린식은 18,434 B이다. 지원되는 활성 집합 최대치 200에서는 134개의 서명이 각각 36,852 B와 36,859 B를 생성한다. 7바이트 차이는 호출 인덱스 2바이트, bare 프리앰블 1바이트, 4바이트 길이 접두사이다. 파이널리티 위원회는 100으로 상한이 정해진 별도의 집합이다; 1,000명의 활성 검증자는 지원되는 런타임 상태가 아니다. 상수 크기 서명 집계는 명시되어 있지 않다. 이 바이트 측정값은 처리량 주장으로 나누어 계산되지 않는다; 청구되는 가중치, 경쟁 트래픽, 파이널리티는 별도의 제약으로 남는다. 전체 픽스처 및 한계: [prepublication evidence](research/prepublication-evidence.md).

**DA 요구사항(소버린, 검증자 호스팅, FLOP 표시).**

- **R5.3a.** DA 저장소는 외부 통화/토큰/네트워크 의존성을 **MUST** 사용하지 않아야 한다; **검증자가 스테이크 하의 저장 노드이다**. `pallet_da_registry`는 `DataRef = (commitment, provider_id, retention_class)`와 배정된 검증자 부분집합 및 감사 장부만을 보관한다; 이레이저 코딩된 바이트(Reed–Solomon 레이트 ½, [`da_shard_count`](#param-da_shard_count) R=6, 임의의 [`da_min_replication_factor`](#param-da_min_replication_factor) k=3개로 복원)는 결정론적 스테이크 가중 부분집합(`hash(commitment) → subset`)에 오프체인으로 존재한다. 게시자가 커밋먼트에 영향을 줄 수 있으므로, 배정의 그라인딩 방지 규칙, 운영자/장애 도메인 다양성, 복구 프로세스, 누적 보존 예산은 [E.47](#appendix-e--open-specification-items)에서 미결로 남아 있다.
- **R5.3b — 서브 오어 슬래시.** 회수 가능성(retrievability) 감사(고스트 태스크 알려진 답(known-answer) 패턴)는 서빙하지 않는 검증자의 본드에서 한계가 정해진 금액([`da_serve_or_slash_percent`](#param-da_serve_or_slash_percent), 라이브니스(Liveness) 클래스, 사기가 아님)을 **MUST** 슬래시해야 한다. 페널티는 *현행(live)* 검증자 집합으로부터 **MUST** 재도출되어야 한다(로테이션으로 빠진 제공자를 오래된 정보로 슬래시하지 않음).
- **R5.3c — 바이트당 DA 수수료 없음.** DA는 검증자의 **의무**이며, 블록 보상 + 수수료의 검증자 지분으로 재원이 조달된다; 바이트당 DA 수수료나 DA 수수료 수입 흐름이 **MUST NOT** 존재해서는 안 된다. 서브 오어 슬래시는 이미 대가가 지급된 의무가 수행되도록 하는 강제 수단이다.
- **R5.3d — 보존 클래스.** `Ephemeral`(≥ 챌린지 윈도우, 이후 프루닝 가능)은 쿼트/증명/트랜스크립트/I-O를 커버한다 — **무료**이며, 그러한 블롭은 수수료가 부과되는 흐름을 통해서만 생성 가능하므로 스팸이 한계 지어진다. `Leased`는 모델 가중치 + dm-verity 이미지를 커버한다 — 고정 기간이며 **저장 수수료 없음**이지만 **환불 가능한 스팸 방지 예치금**(`bytes × `[`da_lease_deposit_per_byte`](#param-da_lease_deposit_per_byte), 전용 홀드 사유 하에 보유되며, 프루닝 또는 인출 시 **전액 반환** — 결코 수익이 아님)이 있고, 누구나 무료로 연장할 수 있으며(`top_up_lease`, tx 수수료만), `lease_end + grace`(14 d) 이후에만 **그리고** 어떤 소비자도 사용 **핀(pin)**을 보유하지 않는 동안에만 프루닝된다. 프루닝은 **MUST** 복구 가능해야 한다: dm-verity 루트는 결정론적이므로 재업로드는 동일한 커밋먼트를 재현하고 신원(`MeasuredRoots`)은 유지된다.
- **R5.3e — 리오그 안전 서빙.** 오프체인 인덱서는 AlephBFT 파이널라이즈된 접두사 내부의 높이만을 **MUST** 서빙해야 하며(파이널라이즈된 블록은 절대 고아가 될 수 없다), 절대 최선 팁(best tip)을 서빙해서는 안 된다.

리싱(leasing)은 무제한 "영구(persistent)" 티어를 대체한다 — 모델의 유효 기간은 6–12개월이다. TEE 쿼트를 마이너의 HTTP 서버에서 옮기는 것은 마이너 단독 보관을 제거한다. 그것이 가용성을 검증자 집합으로부터 독립시키는 것은 아니다: 등록, 만료되지 않은 레코드, 성공적인 스팟 감사, 그리고 전체 분쟁 생애주기에 걸친 복원 가능성은 별개의 술어(predicate)이다. 서브 오어 슬래시는 감사와 복구를 조건으로 하는 인센티브이며, 무조건적인 가용성 보증이 아니다(E.47).

### 근거 및 출처 *(비규범적)*

사이징 목표 및 소버린 DA 결정: `D-0402`(소버린 검증자 DA), `D-0412`(DA는 검증자 의무, 바이트당 수수료 없음; D-0402/D-0407의 수수료 조항을 대체), `D-0407`(리스형 모델 저장소). 전체 설계 da-sovereign-validator-design.md; 사이징
indexer-scaling.md, scaling-500k-agents.md,
scaling-500m-1b-agents.md,
r3-throughput-ceiling.md. 형식 검증:
`FlopSpecs/DataAvailability.lean`,
`FlopSpecs/DaProviderRotation.lean`,
`FlopSpecs/IndexerReorgSafety.lean`,
`da/da-retrievability.qnt`. 리뷰 산술 및 가용성
가정: [prepublication-evidence.md](research/prepublication-evidence.md). 출처 명확화:
`D-0501`. 상태:
[Appendix H](#appendix-h--conformance--implementation-status-matrix).

---
