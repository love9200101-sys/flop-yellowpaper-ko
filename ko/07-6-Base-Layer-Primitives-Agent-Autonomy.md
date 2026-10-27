## 6. 기본 계층 프리미티브와 에이전트 자율성

### 6.1 프리미티브

FLOP의 경제 계층은 **계정/nonce 기반 Substrate**이다(UTXO 전무). 사용 가능한 프리미티브는 다음과 같다.

| 프리미티브 | 세부 내용 |
|-----------|-----------|
| 토큰 전송 | `pallet_balances`; 최소 잔고(existential deposit) 0.01 FLOP; 동적 수수료 |
| 멀티시그 | `pallet_multisig`; 서명자 ≤100명 |
| 프록시 / 권한 위임 | `pallet_proxy`; Any / NonTransfer / Governance / Staking 유형 |
| 검증자 스테이킹 및 권한 집합 | `pallet_validators` — **단일 진실 공급원**이자 `SessionManager`/권한 소스이다. 최소 스테이크는 [`validator_min_stake`](#param-validator_min_stake)이며([`validator_growth_numerator`](#param-validator_growth_numerator)/[`validator_growth_denominator`](#param-validator_growth_denominator) = 연 +9 %로 복리 증가), 가치 연동 하한 `max(baseline, k·V_booked)`를 가진다. 자기 스테이크만 허용하며(위임 스테이킹 없음), 최소 성능 게이트를 갖춘 스테이크 순 로테이션을 사용한다. `pallet_staking`은 존재하지 않는다. |
| 마이너 스테이킹 | `pallet_miner_staking`; [`miner_unbonding_blocks`](#param-miner_unbonding_blocks) 언본딩, [`min_miner_self_stake`](#param-min_miner_self_stake) 최소 자체 스테이크; 자체 스테이크만 허용(레거시 커미션 [`miner_commission_cap_percent`](#param-miner_commission_cap_percent)과 [`max_delegators_per_miner`](#param-max_delegators_per_miner)는 폐기됨) |
| 운영자 자체 스테이크와 커뮤니티 스테이킹 풀 | 운영자(검증자와 마이너): 자체 스테이크만 허용하며, 제3자 스테이크 위임이나 커미션 공제는 없다(`miner_staking::delegate`, `validators::delegate`, `delegation-cap`은 폐기됨); 운영하지 않는 보유자: 슬래싱 위험 없이 7개의 잠금 기간 티어에 걸쳐 [`staker_share_ppt`](#param-staker_share_ppt) = 5% 블록 보상 배분을 공유하는 **기간 잠금형 커뮤니티 스테이킹 풀**(§9.1 R9.12, [E.40](#appendix-e--open-specification-items)) |
| 타임락 / 베스팅 | `pallet_vesting`, `work-vesting`(`R_p²`), `airdrop-vesting`; HTLC 에스크로(§10) |
| 선언적 지출 조건 계층 | **계정** 모델 위에서 동작하는 Miniscript/Simplicity 스타일의 유계 술어(서명 · 해시 · 타임락 · 임계값) — 오피코드(opcode) 유사의 조합성을 제공하며, UTXO 스크립트 엔진은 없다(§6.4) |

**용량 비례 마이너 자체 스테이크(규범적).** 요구되는 마이너 자체 스테이크는 보정된 처리량에 대해 **MUST**
선형이어야 하며 **상한이 없어야(no cap)** 한다(상한을 두면 최대 규모 마이너의 인플레이션 사기가 +EV가 된다).

```
required_self_stake(B_p) = min_miner_self_stake + miner_capacity_stake_per_gflop · B_p
```

여기서 [`min_miner_self_stake`](#param-min_miner_self_stake) = 10,000 FLOP,
[`miner_capacity_stake_per_gflop`](#param-miner_capacity_stake_per_gflop) = 0.01 FLOP/(G_n/s)이다. 이
계수는 발행 인플레이션 사기를 방어한다. `X·B_p`를 주장하는 마이너가 분쟁 윈도우 `W` 동안 실현하는 추가
보상은 `r·(X−1)·B_p·W`이므로(`B_p`에 선형), 상수 `k`는 보안 하한
`k_min(EV) = ((1−p)/p)·(X−1)·P·W / B_total`를 추종한다. 이 한계의 온보딩 형태는 부록 C.1이다.

**R6.1a — 후원 등록 본드.** 스폰서는 마이너 또는 검증자의 등록 본드 전체를 게시하고 이후 이를 보충할
**MAY** 수 있다(부록 G.3). 후원된 원금은 스폰서 계정이 **MUST** 계속 소유하고 그 계정에 동결되어 있어야 한다:
운영자는 그것을 이전하거나, 그것으로 수수료를 내거나, 보류 또는 에스크로에 두거나, 그것으로 다른 스테이크를 보증할 수
**MUST NOT** 있어서는 안 된다. 그것은 활성 상태이거나 언본딩 중인 동안 슬래싱 가능 상태로 **MUST** 남아 있어야 하며,
해당 역할의 언본딩 윈도가 파이널라이즈된 프리픽스 상에서 경과한 후에 스폰서에게만 **MUST** 환불되어야 한다.
활성 후원 원금은 [`sponsored_self_stake_enabled`](#param-sponsored_self_stake_enabled)로 빌드된 런타임에서만
위의 마이너 자기 스테이크 요구치와 검증자 유효 최소치(§15.2)에 **MUST** 산입되어야 한다; 그 밖의 모든 런타임에서
그것은 보증일 뿐이며, 후원 등록과 보충은 **MUST** 거부되어야 한다. 슬래시 수익 계정은 자기 스테이크로 산입되는 원금을
게시해서는 **MUST NOT** 안 된다. 그 슬래시가 자신에게 되돌아 지급될 것이기 때문이다; 그 계정이 이 규칙 이전부터의
살아 있는 스폰서 포지션을 여전히 보유하는 동안 런타임은 어떤 후원 원금도 산입해서는 **MUST NOT** 안 된다. 동결은 합산되지
않고 중첩되므로, 활성화된 런타임에서 스폰서 원금은 스폰서 계정의 유일한 스테이킹 동결이어야 **MUST** 한다: 자기
스테이크, 위임, 또는 다른 스테이킹 팰릿의 어떤 스테이킹 동결이든 보유한 계정은 스폰서 포지션을 열거나 늘려서는
**MUST NOT** 안 되며, 스폰서 계정은 어느 스테이킹 팰릿에서도 자기 스테이크나 위임을 추가해서는 **MUST NOT** 안 된다.
가동 중인 체인이 이 규칙을 처음 활성화할 때, 스폰서가 이미 다른 스테이킹 동결을 보유한 모든 살아 있는 포지션은
**MUST** 격리되어야 하며, 블록당 한정된 배치로 실행되는 그 스캔이 완료될 때까지, 그리고 격리된 포지션이 하나라도
살아 있는 동안에는 어떤 후원 원금도 산입되지 않는다. 활성화된 런타임에서는 해당 계정의 이전 등록에서 비롯된
스폰서 포지션이 살아 있는 동안 자기 등록이든 후원 등록이든 **MUST** 거부되어야 하며, 따라서 새 등록에 대한 슬래시가
이전 등록의 스폰서에게 닿지 않는다; 운영자는 그러한 포지션을 파이널라이즈된 잠금 해제 이후 인출할 **MAY** 수 있고,
자신의 등록보다 오래 남은 포지션의 완전한 언본딩을 시작할 **MAY** 수 있다. 활성화된 런타임에서 감금된 검증자는
유효 최소치 미만으로 활성 집합에 복귀해서는 **MUST NOT** 안 된다: `un_jail`은 `rejoin`과 마찬가지로 먼저 자신의
여유 잔액으로부터 본딩된 자기 스테이크를 복원한다. 활성화된
런타임에서 활성 검증자를 유효 최소치 미만으로 떨어뜨리는 스폰서 언본딩은 그 검증자를 큐로 **MUST** 되돌려야 하며,
그것이 최소 활성 집합을 넘어서게 되는 경우에는 **MUST** 거부되어야 한다. 활성화된 런타임에서
운영자의 등록 해지는 그 활성 스폰서 포지션들의 언본딩을 **MUST** 시작해야 한다. 네이티브 위임에 대한 검증자
자기 스테이크 비율은 운영자 소유 스테이크만 **MUST** 산입해야 한다. 체인 상태와 이벤트는 자기 스테이크와 후원
스테이크를 **MUST** 분리하여 보고해야 한다; 후원 본드는 어떤 배분 권리도 만들지 않는다(R8.4).

### 6.2 에이전트 자율성 — 행위별 합의 없이 운영하기

`pallet_session_keys` + `pallet_agent_wallet`은 소유자가 위임 대리인(delegate) 에이전트에게 생애 한도,
트랜잭션당 한도와 일일 한도, 팔레트/목적지 허용 목록, 그리고 서킷 브레이커
([`circuit_breaker_window`](#param-circuit_breaker_window) / [`circuit_breaker_tx_count`](#param-circuit_breaker_tx_count) /
[`circuit_breaker_flop_cap`](#param-circuit_breaker_flop_cap))를 부여하여 사전 승인하도록 해 준다. 세션 키
생애는 **MUST** 864,000 블록(`SessionKeysMaxDuration`) 이하여야 한다. 이는 중단 없는 1초 목표 주기에서만
경과 시간 기준으로 약 10일에 해당하며, 누락되거나 지연된 블록은 경과 생애를 연장시킨다.
각 지갑의 일일 한도는 `create_wallet`에서 선택된다;
[`agent_daily_cap_autonomous`](#param-agent_daily_cap_autonomous)는 시뮬레이터 시나리오 값이며,
런타임 전체의 한도가 아니다.

- **R6.2a.** 위임 대리인은 자신의 한계 범위 안에서 행위별 합의 없이 — 오직 결정론적 온체인 검사만으로 —
  **MUST** 행위할 수 있어야 한다. 그래야 에이전트가 무인으로 실행되며 비동기적으로 제출하고, 검증자가
  순서를 정한다.
- **R6.2b.** 소유자는 언제든지 **MUST** 취소할 수 있어야 한다. 지출은 세션 상한(§11 INV-02), 일일 상한,
  서킷 브레이커에서 **MUST** 차단되어야 한다. 탈취된 세션 키는 이러한 상한들에 의해 **MUST**
  제한되어야 한다. 지갑 및 세션의 일일 예산은 지갑 또는 세션 생성 시점, 또는 직전 리셋 시점으로부터
  [`agent_cap_window_blocks`](#param-agent_cap_window_blocks)(86,400 블록) 이후 또는 그 시점의 첫 지출에서 **MUST**
  리셋되어야 한다. 그 지출이 다음 윈도를 시작한다; 이 리셋은 BABE 에포크 경계를 사용하지 않는다.
- **R6.2c — 서킷 브레이커.** 브레이커 윈도는 위임 대리인별이며 그 세션들 전체에 걸쳐 공유된다: 위임
  대리인의 첫 `create_session`에서 열리고, 경과한 뒤에는 위임 대리인의 다음 트랜잭션에서 다음 윈도가
  열린다. 트랜잭션 개수 한도와 지출 한도는 독립적으로 발동한다; 어느 쪽이든 발동하면 윈도가 끝나 자동
  리셋될 때까지 위임 대리인의 모든 트랜잭션 거부를 **MUST** 래치해야 하며, Root는
  `force_reset_circuit_breaker`로 이를 더 일찍 **MAY** 리셋할 수 있다
  (`pallets/pallets/session-keys/src/lib.rs::{check_and_update_circuit_breaker,is_circuit_breaker_tripped}`).

### 6.3 트랜잭션 / 상태 모델

FLOP는 **계정 모델**을 유지한다. 완전한 UTXO 네이티브로 가는 것은 **미채택으로 의결되었다**.

- **에이전트 간 병렬성은 비용 없이 확보된다** — 독립적인 에이전트들은 서로소인 계정을 다루며, BFT-DAG가
  이들의 동시 블록 순서를 정한다.
- **에이전트 내부** 트랜잭션은 하나의 단조 증가 `u32` 계정 nonce를 사용한다. 런타임은 한 블록 안에서 한
  계정의 연속된 nonce를 받아들인다(`pallets/runtime/zkverify/src/lib.rs::SignedExtra`는
  `frame_system::CheckNonce<Runtime>`를 사용한다); 단일 레인 동시 진행 한도는 클라이언트 정책이다.
  구현체는 nonce가 자기 스트림만 직렬화하도록 각 에이전트에 (`agent-wallet`을 통해) 자체 계정을
  **SHOULD** 부여해야 하며, head-of-line 블로킹을 제거하기 위해 2차원/병렬 nonce(계정당 복수 레인)를
  **MAY** 추가할 수 있다; 2차원 레인은 채택되지 않았다. 이는 세션(§12.1)에 의해 대체로 무의미해진다. 스트리밍 세션은 OPEN/SETTLE
  시점에만 체인에 접촉하기 때문이다.

순수한 고빈도 마이크로페이먼트 핫 경로를 위해 UTXO 결제 사이드 레일은 여전히 선택지로 남아 있으나, 이는
제2의 상태 모델이 아니다.

### 6.4 협업 풀과 조합

에스크로 프리미티브("자금을 모아 협업한다")는 `pallet_compute_channel`(§12.1)로 구현되었다. 이는
양자간(에이전트↔마이너) 에스크로로서, 지급이 정산/분쟁 판정에 조건부이며, 필수 타임아웃 환불을 갖추며, 각
에스크로 유입액이 마이너 순지급, 구매자 환불, 소각 또는 라우팅된 페널티, 누적 감사 적립분, 미정산 채널을 위해
아직 보유된 자금에 걸쳐 보존된다. 누적 감사 적립분은 지급된 감사 수수료와 미사용 감사 준비금을 모두 포함한다;
감사 수수료를 다시 더하면 그 배분을 이중으로 계산하게 된다. 선도 본드는 별도의 자금 원천이며 자체 보존 원장을
가진다. 이것이 일반화 가능한 에스크로 프리미티브이다.

- **R6.4a.** 에스크로는 자금을 **MUST** 보존해야 하고, 쿼럼/판정 또는 타임아웃 환불 시에만 지급해야 하며,
  참여자별로 회계 처리해야 하고, 단일 당사자가 풀을 인출하도록 결코 허용해서는 안 된다.

`N`자간 일반화(공유 자금, 프로그래머블 쿼럼 분배)와 하나의 세션을 여러 마이너에 걸쳐 분산하는 MPP
팬아웃은 향후 과제이다. 그때까지는 `multisig + treasury`를 조합하거나 1:1 HTLC를 사용한다. 더 넓은 조합
목표는 선언적이고 유계이며 보존 안전한 세 개의 계층이다. 즉 조합 가능한 지출 조건(Miniscript 스타일 —
구현 완료), 감쇠 가능한 권한(UCAN/macaroon 스타일, §6.2 세션 키의 일반화 — 향후), 그리고 종료하는
다자간 에스크로(Marlowe 스타일 — 위의 프리미티브)이다.

### 6.5 암호학적 프리미티브와 계정

다른 모든 절이 의존하는 프리미티브를 한곳에 고정한다. 합의에 치명적인 영역이며, 여기서의 변경은
인코딩/건전성 변경이다(§14.1).

**계정.**
- **R6.5a.** 계정은 32바이트 `AccountId`이며, 표시할 때는 체인의 `SS58Prefix`(모든 FLOP 네트워크에서 42, R9.8)
  아래에서 SS58로 인코딩된다. 익스트린식은 `MultiAddress<AccountId, ()>`를 통해 계정을 지정한다. 네트워크는
  주소 인코딩이 아니라 제네시스 해시로 구별되므로, 가치를 인가하는 오프체인 진술(예: 제네시스 청구 진술)은
  제네시스 해시 또는 체인 ID로 네트워크를 **MUST** 바인딩해야 한다.
- **R6.5b.** 계정은 최소 잔고(existential deposit, `EXISTENTIAL_DEPOSIT` = 0.01 FLOP) 이상을 **MUST**
  보유해야 하며, 그렇지 않으면 소멸(reap)된다. 잔액은 18 소수 자릿수를 가지며 10⁻¹⁸ FLOP
  기본 단위의 정수 개수이다.
- **R6.5c.** 계정 내부 트랜잭션은 단조 증가하는 `u32` nonce 위에서 직렬화된다(§6.3). 위임 대리인
  에이전트는 자신의 nonce 스트림이 독립적이 되도록 자체 계정을 **SHOULD** 보유해야 한다. 런타임은 한
  블록 안에서 한 계정의 연속된 nonce를 **MUST** 받아들여야 한다; 단일 레인 동시 진행 한도는 런타임
  제약이 아니라 클라이언트 정책이다(`frame_system::CheckNonce<Runtime>`).

**서명 방식.** 런타임 서명 타입은 `MultiSignature`(서명자 `MultiSigner`)이며, **sr25519**, **ed25519**,
**ecdsa/secp256k1**을 허용한다. 역할별 사용은 고정되어 있다.

| 사용처 | 방식 | 비고 |
|-------|------|------|
| 체인 트랜잭션 / 계정 | sr25519 (`MultiSignature` 경유) | 기본값이며, ed25519/ecdsa도 허용된다 |
| 검증자 어테스테이션 (`ValidatorAttestation`) | **sr25519** | 검증자당 서명 1개, SCALE 인코딩된 서명 대상 페이로드에 대해 서명(§3.6, 부록 F.2) |
| 세션 인클레이브 키 (턴별 트랜스크립트 리프) | **sr25519** | 32바이트 `enclave_key`, `open_channel`에서 RA-TLS로 한 번 어테스트된다. 에이전트가 영수증에 공동 서명한다(§12.1b) |
| HTLC — Bitcoin 레그 | secp256k1 | 네이티브 P2SH/Taproot(§10.2) |
| HTLC — NEAR 레그 | ed25519 | NEAR 계정은 일급 FLOP 계정이며, `flop_account = SS58(derived_pubkey)`이다. NEAR MPC는 NEAR가 제어하는 체인을 위해 secp256k1에도 서명한다(§10.2) |

- **R6.5d.** 포스트 양자 내성은 **범위 밖**이다(§12.4). 확장 가능한 양자 공격자는
  sr25519/ed25519/secp256k1을 깨뜨리고(Shor), SHA-256 프리이미지 보안을 절반으로 낮춘다(Grover). 이
  경계는 묵시적이 아니라 명시적이다.

**해시 함수.** 각각은 자신의 역할에 고정되어 있으니 대체하지 말 것.

| 해시 | 용도 |
|------|------|
| `BlakeTwo256` | 블록/상태/익스트린식 해싱(런타임 `Hashing`); `task_hash = blake2_256(…)`(부록 F.1) |
| `SHA256` | `report_data` 쿼트 바인딩 프리이미지(§3.3)와 HTLC 해시락 `H = SHA256(s)`(§10) |
| `keccak256` | 도메인별 머클 루트로 수집되는 집계 스테이트먼트 해시(§3.6) |
| 머클 (BlakeTwo256 리프) | 세션 트랜스크립트 누산기(§12.1b, 부록 F.3); dm-verity는 자체 4 KB 블록 머클 트리를 사용한다(§3.3) |

- **R6.5e — 도메인 분리.** 서명되거나 해시되는 페이로드는 한 맥락의 서명 또는 커밋먼트가 다른 맥락에서
  재생될 수 없도록 **MUST** 도메인 분리되어야 한다. 트랜스크립트 리프는 `channel_id ‖ turn_index`를
  바인딩하고(§12.1b), `task_hash` v1은 필드들 앞에 `"FLOP/POUI/TASK"` 태그, 버전 바이트,
  `genesis_hash`를 두고 시작하며(부록 F.1),
  `report_data`는 전체 `(task_hash, gn_weight, …, tee_type)` 튜플을 바인딩한다(§3.3).

### 근거 및 출처 *(비규범적)*

출처: `D-0513`(모든 네트워크에서 SS58 프리픽스 42; 네트워크는 제네시스 해시로 구별, R6.5a),
`D-0408`(단일 검증자 스테이킹 시스템), `D-0413`(가치 연동 스테이크 하한), `D-0416`
(스테이크 순 로테이션), `D-0417`(선언적 지출 조건 계층, UTXO 미채택), `D-0418`
(용량 비례 마이너 스테이크, 시뮬레이션 보정 대기 중인 잠정안), `D-0403`(에스크로 프리미티브의 첫 사례로서의
세션), `D-0530`(운영자 자기 스테이크 전용; 위임과 커미션 폐기; 5% 기간 잠금형 커뮤니티 스테이킹 풀). 근거 자료:
agent-composition-primitives.md,
agent-token-lifecycle.md,
model-selection-pricing-inference.md,
miner-capacity-stake-calibration.md. R6.2c 래치와
리셋 경로는
`session-circuit-breaker.qnt`에 한정된 모델이 있다. 차단을 일으킨 호출 이후에 실패하는, 이를 감싸는
원자적 배치는 래치를 함께 롤백한다; 이는 수용된다. 한도 초과 호출은 어느 경우든 실행되지 않으며, 위임 대리인은
한도 아래에 머무르는 것으로 얻을 수 없는 어떤 것도 얻지 못하기 때문이다. 선행 연구:
Miniscript, Simplicity, Clarity, Marlowe, Move resources, UCAN. 상태:
[부록 H](#appendix-h--conformance--implementation-status-matrix).

---
