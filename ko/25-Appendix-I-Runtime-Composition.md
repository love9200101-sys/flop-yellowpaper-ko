## 부록 I — 런타임 구성

`construct_runtime!` 인벤토리이다(출처: `pallets/runtime/zkverify/src/lib.rs`). **팔레트 인덱스는 합의와
인코딩에 결정적이다.** 인덱스는 모든 디스패치와 저장 키의 접두사가 되므로, 인덱스 변경은 마이그레이션이
필요한 호환성 파괴 런타임 업그레이드다(§14.1). 인덱스는 순번이 아닌 안정적인 식별자이며, 빈 구간은
의도적이다(제거된 팔레트의 인덱스는 재사용하지 않는다). 이 부록은 인덱스 값에 대해 규범적이다.

**핵심 / 시스템**

| Idx | 팔레트 | 역할 |
|----:|--------|------|
| 0 | `frame_system` | 기본 런타임 |
| 1 · 2 | `scheduler` · `preimage` | 거버넌스 시행 / 타임락 / 대형 호출 저장(§14) |
| 3 | `timestamp` | 블록 시각 |
| 4 | `balances` | 토큰 계정; 최소 존재 보증금(existential deposit)(§6.5) |
| 5 | `transaction_payment` | 수수료 모델(§4.2, §9) |

**합의**

| Idx | 팔레트 | 역할 |
|----:|--------|------|
| 6 | `authorship` | 블록 생성자 기록 |
| 8 · 9 | `offences` · `session_historical` | 위법 행위 보고 / 과거 세션 증명(슬래싱, §11) |
| 10 · 11 · 13 | `babe` · `session` · `authority_discovery` | BABE 블록 생성; 세션 키; 피어 탐색(§2) |
| 104 | `aleph` | AlephBFT 위원회 스냅샷 + `LastFinalized` → `FinalizedPrefix`(§2, §15.4) |

*제거됨(D-0408): `pallet_staking`(이전 7) 및 `bags_list`(이전 19) — `validators`(96)가 유일한 권한
출처다(§6.1).*

**거버넌스 및 유틸리티**

| Idx | 팔레트 | 역할 |
|----:|--------|------|
| 14 | `treasury` | 온체인 재무부(§14) |
| 15 · 16 · 17 | `conviction_voting` · `referenda` · `custom_origins` | OpenGov(§14.1–§14.2) |
| 25 · 26 | `bounties` · `child_bounties` | 재무부 바운티 |
| 30–33 | `utility` · `multisig` · `proxy` · `identity` | 배칭; 멀티시그(§6.1); 프록시 위임(§6.1); 신원 |
| 99 · 105 | `emergency_override` · `emergency_pause` | 비상 개입(break-glass) + 회로 차단기(§14.1 R14.6) |

**부트스트랩(메인넷 제네시스 이관 시 제거)**

| Idx | 팔레트 | 역할 |
|----:|--------|------|
| 50 | `sudo` | 부트스트랩 Root; 디수도(de-sudo) 시 **무력화 + 제거**(§14.1 R14.3/R14.5) |
| 51 | `vesting` | 범용 베스팅; 베스팅 완료 후 제거 가능 |

**FLOP 프로토콜**

| Idx | 팔레트 | 역할 · 명세 § |
|----:|--------|---------------|
| 81 | `aggregate` | 크로스체인 디스패치를 위한 검증된 명제 머클 루트(§3.6) |
| 83 · 84 | `token_claim` · `crl` | 에어드롭 청구 · 인증서 폐기 |
| 85 | `has_station` | HTLC + 조건부(predicate) 에스크로(§10) |
| 86 | `flop_poui` | PoUI 증명 검증, 검증자 어테스테이션, `flop_meter`(§3.6, §4) |
| 87 | `hw_calibration` | 집계 호스트 캘리브레이션 상한 + 갱신 가능한 리스(§7) |
| 88 · 91 | `work_vesting` · `airdrop_vesting` | `R_p²` 성능 베스팅(§8) · 에어드롭 베스팅(§9) |
| 89 | `synthetic_tasks` | 고스트 태스크 — 라이브니스 + 정확성 카나리(§8.1) |
| 90 | `attest` | 공유 어테스테이션 프로파일 레지스트리(§3.6) |
| 92 · 93 | `block_rewards` · `flop_subsidy` | 발행 분배(§9) · 0기(era-0) Labs/재단 보조금(§9) |
| 94 · 95 · 106 | `session_keys` · `agent_wallet` · `agent_identity` | 에이전트 위임 + 상한 + 회로 차단기(§6.2) |
| 96 · 97 · 98 · 100 | `validators` · `miner_staking` · `delegation_cap` · `miner_slashing` | 검증자 권한 + 로테이션 + 슬래싱(§15); 마이너 스테이크 + 위임 상한 + 슬래싱(§6.1, §11) |
| 101 · 102 · 103 | `model_registry` · `da_registry` · `compute_channel` | 측정 루트 + 디코드 정책 핀 고정(§3.3); 소버린 DA(§5.3); 세션(§12) |
| 107 | `metering_verifier` | 미터링 인증서 검증(§4, E.34) |

**정산 검증기**(`160–170`) — **추론 증명이 아닌 zkVerify 집계**(§3.6):
`common`(160), `groth16`(161), `risc0`(162), `ultraplonk`(163), `plonky2`(165), `fflonk`(166),
`sp1`(167), `ultrahonk`(168), `ezkl`(169), `tee`(170).
