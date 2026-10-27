## 11. 보안 불변식

`../formal-specs/` 아래의 Quint/TLA+ 모델은 아래 불변식의 여러 버전을 기술한다.
불변식은 규범적이다. 모델 체킹 결과는 명시된 모델, 가정, 탐색 범위(bounds), 도구 실행에 대해서만
적용된다; 모델 파일 자체만으로는 모든 구현 실행에 대한 증명이 되지 않는다. 귀속(attribution) 색인과
부록 H는 이러한 산출물을 런타임 강제 및 미결 적합성 의무와 구분한다.

### 11.1 강제되는 불변식

| 불변식 | 규칙(규범적) | 강제 수단 |
|-----------|------------------|-------------|
| INV-02 / 세션 상한 | 세션 지출은 **MUST** 세션 상한 이하여야 한다 | `agent_transfer`가 `remaining_session_cap()`을 확인한다 (`SessionCapExceeded`) |
| `fail_task` 권한 | 권한을 부여받고 속도 제한이 적용되는 리포터만이 **MUST** 태스크를 실패 처리해야 한다 | 없음: 태스크별 경로와 그 `fail_task` 호출은 제거되었으므로(부록 H.5), 이 규칙이 구속하는 현행 호출은 없다 |
| INV-S01 / 세션 논스 | 세션 논스는 **MUST** 단조 증가해야 한다(재전송 방지) | `SessionInfo.nonce`를 사용마다 검증 후 증가시킨다 (`InvalidSessionNonce`) |
| INV-M06 / 지급 원자성 | 정산 지급은 **MUST** 전부 아니면 전무(all-or-nothing)여야 한다: 마이너 및 검증자 레그, 에이전트 환불, `FLOPFoundationAccount`로의 `φ·(E−P)` 이전(R12.1d)이 모두 반영되거나 하나도 반영되지 않아야 한다 | 컴퓨트 채널 `payout_settlement`: 마이너 이전, 에이전트 환불, 페널티 레그 중 하나라도 실패하면 정산 익스트린식이 되돌려지므로, 어느 레그도 다른 레그 없이 반영되지 않는다(페널티 레그 싱크: 부록 H.5) |
| 공급 | 발행 상한 + 반감기 단조성이 **MUST** 유지되어야 한다 | `tokenomics-supply.qnt` |
| HTLC | 로컬 보존 + 조건부 완료 + 타임락 대칭성(§10) | `htlc-atomic-swap.qnt` |
| 채널 | 보존 + 이중 정산 금지가 **MUST** 유지되어야 한다 | `channel/channel-settlement.qnt` |
| DA | 검색 가능성(retrievability) + 서빙 또는 슬래시(serve-or-slash)(§5.3) | `da/da-retrievability.qnt` |

### 11.2 세션 `G_n` 정산 게이트

- **R11.2.** 채널 `settle` / `force_settle`은 지급 또는 크레딧 이전에 **MUST** `GnSink::validate_session_gn`을
  호출해야 한다: 0이 아닌 집계 `G_n`은 **MUST** 크레딧 도메인, 마이너 효율 상한, 파이널라이즈된
  캘리브레이션 상한, §6.1 용량 본드, 거부 전용(reject-only) 처리량 트립와이어(§4.1)에 부합해야 한다.
- **R11.2a.** 이는 **타당성 한계(plausibility bound)이며 실행 검증이 아니다.** `settle`은 **MUST** 제출된
  각 `VerifiedTurn`의 서명과 머클 경로를 하나의 `final_root`에 대해 검증하고, 중복되거나 범위를 벗어난
  턴 인덱스를 거부하며, 제출된 `g_n` 값을 오버플로 검사 합산(checked-sum)하고, 그 합이 `aggregate_gn`과
  같도록 요구해야 한다(`verified_work_from_turns`; §12.1). 이는 제출된 리프 값과 그 산술을 인증한다.
  그러나 주장된 실행이 실제로 일어났음을, 또는 제출된 턴이 독립적으로 커밋된 트랜스크립트 전체를
  망라함을 증명하지는 않는다(E.43/E.44).
- **R11.2b.** 현행 프로파일의 채널 지급은 공개 작업 적립을 발행하거나, 보상 누산기 또는 성능 베스팅 작업량을
  증가시키거나, 위원회 최신성(recency)을 갱신하거나, 영수증으로부터 캘리브레이션을 업데이트해서는 **MUST NOT** 안 된다.
  이는 협력적, 인증서, 일방적, 선도(forward), 복구 불가 DA 지급 모두에 적용된다.
  챌린지 만료만으로 영수증이 공개 작업 적립 대상이 되어서는 **MUST NOT** 안 된다. (§8.2 R8.7에 따른 Era-0 에어드롭
  그랜트의 비공개·지급액 기준 Miner 언락 적립과 Agent 지출 적립은 공개 작업 적립, 블록 보상 누적, `work-vesting`(`R_p²`)이
  아니며, R8.7이 규율하는 대로 파이널리티에 [`channel_dispute_window_blocks`](#param-channel_dispute_window_blocks)를
  더한 시점 이후에 적립된다.) 향후 독립적으로 감사되는 공개 작업 적립과
  과거 적립의 복구에는 E.44의 별도 증거와 프로토콜 처분이 필요하다.

### 11.3 검증자 슬래싱 표

`pallet_validators`는 검증자 페널티에 대한 단일 권한 주체다.

| 위반 | 페널티 | 효과 | 재진입 |
|---------|---------|--------|----------|
| 결탁(가짜 `G_n` 증명에 서명) | [`slash_fraud_percent`](#param-slash_fraud_percent) = 100% 슬래시(재단으로) | 퇴출 + 블랙리스트 | 없음 |
| 이중 서명(equivocation, 상충하는 블록) | 상관형(Eth2 방식): 단독 [`slash_equivocation_lone_percent`](#param-slash_equivocation_lone_percent) = 50% 슬래시(나머지 50%는 180 d 후 반환), ≥⅓ 상관 → 100% 슬래시(재단으로) | 단독: 퇴출(재스테이크 가능); 카르텔: 퇴출 + 블랙리스트 | 단독: 180 d 반환 + 언락 쿨다운 후 재스테이크; 카르텔: 없음 |
| 증거 위조 | 100% 슬래시(재단으로) | 퇴출 + 블랙리스트 | 없음 |
| TEE 어테스테이션 실패 *(HARD 티어 어테스테이션에 한함)* | 100% 슬래시(재단으로) | 퇴출 + 블랙리스트 | 없음 |
| 라이브니스 — 다운타임 > 300 블록 | [`slash_liveness_percent`](#param-slash_liveness_percent) = 1% | 감금(jailed) | ≥ 1 h 경과 후 `un_jail` |
| 장기 다운타임 > 24 h | [`validator_extended_downtime_slash_percent`](#param-validator_extended_downtime_slash_percent) = 5% | 강제 퇴출(kicked) | 전체 스테이크 증액과 함께 `rejoin` |

결탁/위조/TEE는 100% 고정으로 유지된다(증거에 기반한 사기). 이중 서명은 유일한 상관형·회복 가능
등급이다(단독 이중 서명은 대개 정직한 페일오버 버그다). 슬래싱된 모든 담보는 소각 없이 100%
`FLOPFoundationAccount`로 라우팅된다(§9.3 R9.10). 운영자 스테이크는 자기 스테이크만 가능하다(제3자 위임 스테이킹은
금지된다); 레거시 또는 테스트넷의 후원 보증(E.32)이 있는 경우, 손실 순서는 운영자 자기 스테이크를 먼저 부과하고
그다음 결함률(fault rate)로 스폰서에게 부과한다(레거시 위임자 워터폴 항목은 폐기되었다).

### 근거 및 출처 *(비규범적)*

출처: R11.2b 지급 전용 범위,
`D-0409`(슬래싱 표 정합), `D-0420`(상관형 이중 서명), `D-0419`(언본딩 슬래시 락),
`D-0529`(소각 0; 슬래시의 100%를 `FLOPFoundationAccount`로), `D-0530`(운영자 자기 스테이크 전용; 위임 워터폴 폐기). P0 에이전트
경제 점검(INV-02, `fail_task`, 세션 논스, 지급 원자성)은 플래그되었으나 미강제였던 네 개의 불변식을
종결했다. 근거:
`formal-specs-agent-economics.md`,
session-work-verification-gap.md,
fee-design.md,
economic-security-proofs.md,
network-valuation.md(가치 결합 하한 `V_booked = a·n_eff + b·n_eff² + c·v̄·D₂`, C5/D-0413). 형식 명세: `FlopSpecs/Security.lean`
(`StakingSlashing`, `CoCVoC`), `FlopSpecs/Sessions.lean`,
`channel/session-gn-integrity.qnt`. 상태:
[부록 H](#appendix-h--conformance--implementation-status-matrix).

---
