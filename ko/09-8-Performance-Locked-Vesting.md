## 8. 성과 잠금 베스팅

```
R_p ≔ min(G_n_actual / B_p, 1) ∈ [0, 1]
UnlockRate = R_p²                                  (R_p = 0.5 → unlock 0.25)
Blackout:  capacity < 10% for blackout_revoke_blocks continuous blocks  →  grant revoked (1.0× slash)
```

- **R8.1.** `create_grant`로 생성된 워크 베스팅 그랜트는 그랜트 생성 시점에 스냅숏된, 0이 아닌
  파이널라이즈된 §7 캘리브레이션 베이스라인을 `B_p`로 **MUST** 취해야 한다; Root 전용 `force_create_grant`는
  그 검사를 우회하고 호출자가 제공한 0이 아닌 임의의 베이스라인을 취한다(부록 H). 그 플레지 비율은 제곱하기
  전에 1로 **MUST** 클램프되어야 하므로 `R_p ≔ min(G_n_actual / B_p, 1) ∈ [0, 1]`이다; 해제 비율은 **MUST**
  볼록 함수 `R_p²`이어야 한다(성과 미달은 초선형적으로 벌점이 부과된다; `R_p² ≤ R_p`).
- **R8.2.** [`blackout_revoke_blocks`](#param-blackout_revoke_blocks) 동안 10% 미만의 연속적인 용량
  블랙아웃은 **MUST** 그랜트를 취소해야 한다(1.0× 슬래시).

### 8.1 Synthetic Task Engine(고스트 태스크)

HARD 티어 마이너에 대해 Validator Leader는 마이너의 TEE 키에 봉인(seal)된 암호화 "고스트 태스크"를
주입한다. 이들은 실행 전에는 실제 태스크와 구별할 수 없도록 의도되어 있어, 어테스테이션된 하드웨어가
계속 가동 상태를 유지해야 한다(HARD 티어의 타임 슬라이싱 방지 메커니즘(§2.4)이자 정확성 카나리(§7)이기도 하다).
SOFT 마이너는 TEE 키가 없으며; 그 챌린지 전달, 신원 바인딩, 수요 하한 자격은
미해결 SOFT 프로파일(E.33)의 일부이므로, 봉인 태스크 보장은 해당 티어에 적용되지 않는다.

- **R8.1a.** 고스트 태스크는 고정 시드 / 정답 기지이다. *부정확한* 결과는 **MUST** 아무것도 완료하지
  않고 **유계 에스크로 슬래시**(`OnGhostTaskFailed`)를 적용해야 한다 — 일시적 드리프트가 사기로
  취급되지 않도록 의도적으로 PoUI의 100% 슬래시 + 블랙리스트 사기 경로가 *아니다*. *정확한* 결과는
  태스크를 완료하고; 기한을 놓치면 만료된다.
- **R8.1b.** 실패한 고스트 태스크는 자신이 게이트하는 베스팅 토큰을 **MUST** 소각하거나 재경로화해야 한다.

암호화 발행, 수요 하한 자동 주입, 정답 기지 정확성 카나리가 엔진의 핵심이며; 통계적 드리프트-속임
판별과 카나리 트리거 재캘리브레이션은 §7 / E.22이다.

### 근거 및 출처 *(비규범적)*

근거 자료: ghost-task-sampling-design.md(샘플링,
`GhostTaskCommitment`/`MinerExecutionEvidence`/`CheckerVerdict`, 발행자/검사자 분리 + 이의 제기),
miner-capacity-stake-calibration.md. 형식 검증:
`FlopSpecs/Vesting.lean`(`unlock_le_ratio`; 그
`h1 : R_p ≤ 1` 가정은 R8.1의 클램프로 강제된다). 낮은 `B_p`를 노리는 캘리브레이션 샌드배깅은 여전히
M13의 **[GAP]**으로 남아 있다. 상태:
[부록 H](#appendix-h--conformance--implementation-status-matrix).

---
