## 14. 거버넌스와 프로토콜 업그레이드

거버넌스는 OpenGov이다: `pallet_referenda`, `pallet_conviction_voting`, 커스텀 `Origins`,
`pallet_scheduler` + `pallet_preimage`(발효/타임락/대형 호출 저장), `pallet_treasury`,
`pallet_multisig`, `pallet_proxy`(`Governance` 필터 포함). 브레이크글라스(break-glass): `pallet_emergency_override`
(Root 전용, [`emergency_override_timelock`](#param-emergency_override_timelock) = 72 h,
[`emergency_override_cooldown`](#param-emergency_override_cooldown) = 7 d) 및 `pallet_emergency_pause`
(자동 만료를 갖는 팔레트별/전역 세분화 서킷 브레이커).

### 14.1 요구사항

- **R14.1 — 프로토콜 업그레이드 트랙.** 프로덕션 `protocol_upgrade`(Root) 트랙은 레퍼렌덤이 `set_code` /
  모든 `EnsureRoot` 호출을 디스패치할 수 있도록 `RawOrigin::Root`를 **MUST** 라우팅해야 한다. 찬성은
  **MUST** 고정 [`protocol_upgrade_approval`](#param-protocol_upgrade_approval) = 67%(BFT 2/3)이어야 한다; 지지(support)는
  **MUST** 참여율(turnout) 하한 [`protocol_upgrade_support_floor`](#param-protocol_upgrade_support_floor)
  (`ActiveIssuance`의 50% → 15% 선형)을 충족해야 한다; 발효는 **MUST** Scheduler를 통해
  [`protocol_upgrade_enactment_timelock`](#param-protocol_upgrade_enactment_timelock) = 14 d로
  타임락되어야 한다. 결정 기간, 준비/확인, 결정 보증금은 [E.9](#appendix-e--open-specification-items)에 있다.
- **R14.2 — 부트스트랩 제출 게이트.** 첫 반감기(블록 63,072,000)까지 프로토콜 FIP 제출은 **MUST** FLOP
  Foundation(`EnsureFoundationProtocolSubmit`)에만 귀속되어야 한다 — **투표 통제가 아닌 제출 통제**이며,
  찬성/지지/타임락은 여전히 적용된다. 이 게이트는 해당 경계에서 일몰된다.
- **R14.3 — De-sudo.** 모든 `EnsureRoot` 사이트가 거버넌스 오리진을 통해 도달 가능하고 **그리고**
  `pallet_sudo`가 무력화되어(`remove_key`) 프로덕션 런타임에서 제거되기 전까지 거버넌스는 "가동(live)"
  상태가 아니다. 이는 승인된 런타임 코드의 속성이며, 향후 Root `set_code` 교체에 대한 불변식이
  아니다.
- **R14.4 — 발효 경계.** 포크 없는 변경(온체인 WASM `set_code`)은 **MUST** 스토리지 호환성 규율
  (`spec_version` 증가 + `try-runtime`)을 따라야 한다. 조정된 변경(합의 엔진, 호스트 함수, P2P,
  파이널리티 가젯)은 런타임 호출로 발효될 수 없다: 거버넌스가 *승인(authorize)*하고, 노드 바이너리
  릴리스가 업그레이드 기한 블록 높이에서 활성화한다.
- **R14.5 — 현행 런타임 안전 범위(safety envelope).** 승인된 런타임이 노출하는 파라미터 업데이트 호출은
  **MUST NOT** 안전 범위(≥67% 찬성, ≥15% 쿼럼, ≥14 d 타임락,
  ≥ [`validator_min_stake`](#param-validator_min_stake)(1,200,000 FLOP) 스테이크 하한, 자기 비활성화 금지.
  `governance.qnt`와 `Governance.lean`의 형식 모델은 이를 1,000 FLOP 단위의 1200으로 표현한다)를
  벗어나서는 안 된다; 이러한 각 발효는 **MUST** 속도 제한되어야 한다(`governance_param_max_step_pct`). 이
  가드와 그 형식 모델은 Root `set_code`를 통해 디스패치되는 임의의 교체 코드를 제약하지 않는다. 런타임
  교체 전반의 안전성은 리뷰, 투표자 찬성, 사회적 거버넌스에 의존한다; 승인된 코드 가정은
  [E.50](#appendix-e--open-specification-items)이다.
- **R14.6 — 서킷 브레이커.** 하드코딩된 보호 집합(합의/인히어런트, Scheduler/Preimage, 거버넌스 투표,
  브레이커 자체, Sudo)은 **MUST NOT** 일시 중지 가능해서는 안 된다; 일시 중지는 **MUST** 자동 만료되어야 한다.
  de-sudo 이후 일시 중지 오리진은 **MUST** 신속하게 유지되어야 하며(타임락된 트랙이 아닌 운영 멀티시그),
  별개의 재개 오리진을 가져야 한다.

### 14.2 FIP 결합

FIP는 번호가 부여된 오프체인 설계 문서이다. 온체인에서 `protocol_upgrade` 레퍼렌덤은
`referenda.set_metadata`(FIP 텍스트의 `Preimage` 해시)를 통해 이에 결합된다; 구조화된 온체인 FIP 메타데이터는
필요하지 않다.

### 근거 및 출처 *(비규범적)*

출처: `D-015`(67% + 브레이크글라스), `D-0415`(OpenGov 채택, 커스텀 FIP 팔레트
SPEC-024 대체), `D-0425`(첫 반감기까지 Foundation 제출 게이트), `D-0501`(현행 런타임 범위 및
승인된 코드 가정). 작업 분해:
`docs/plans/GOVERNANCE_ACTIVATION_PLAN.md`. 형식 명세:
`FlopSpecs/Governance.lean`(`GovernanceTransition`),
`governance/governance.qnt`. 이 증인(witness)들은
모델링된 허용 업데이트에 대해 한정하며, 임의의 교체 바이트코드에 대해서는 그렇지 않다. 리뷰 증거:
[prepublication-evidence.md](research/prepublication-evidence.md). 미결: E.9(트랙 크기), E.50
(임의 업그레이드 범위).
상태: [부록 H](#appendix-h--conformance--implementation-status-matrix).

---
