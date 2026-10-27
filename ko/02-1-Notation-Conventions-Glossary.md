## 1. 표기법, 규약 및 용어집

별도 언급이 없으면 온체인 수량은 정확한 정수이다; 유리수는 고정소수점(백만분율
`ppm`, 또는 천분율 `ppt`)을 사용한다. FLOP 잔고는 18 소수 자릿수를 가지므로 **기본 단위**는
10⁻¹⁸ FLOP이고 모든 온체인 잔고는 그 정수 개수이다; 기본 단위에는 별도의 이름이 없으며
금액은 FLOP으로 쓰거나 기본 단위의 개수로 쓴다. `‖`는 연결(concatenation)을 나타낸다; `SHA256`과 `blake2_256`은 각각 해당
32바이트 해시를 나타낸다.

### 1.1 용어집 — 역할과 소프트웨어의 구분

**노드**는 소프트웨어이며, 아래의 다른 모든 용어는 *스테이킹되거나 위임된 역할*이다. 검증자와 마이너는
각각 노드와 역할별 서비스를 실행한다. 이 용어들은 문서 전체에서 정확히 이 의미로 사용된다.

| 용어 | 정의 |
|------|-----------|
| **노드** | 소프트웨어 프로세스(`relay-node` / `zkv-service` + 역할 서비스). 역할이 아니다: 검증자와 마이너 모두 노드를 실행한다. |
| **검증자** | 스테이킹된 합의 역할: 블록을 생성하고(BABE), 샘플링된 위원회에서 BFT 파이널리티를 실행하며(§2), 서브-오어-슬래시(serve-or-slash) 하에 DA 샤드를 저장·서빙하고(§5), 마이너의 증명(§3.6)과 체커 판정(§3.5)을 어테스테이션한다. GPU나 TEE를 필요로 하지 않으며 추론을 결코 실행하지 않는다(§15.1). 검증자 블록 보상 지분을 얻는다. 최소 자기 스테이크는 부록 A를 따른다([`validator_min_stake`](#param-validator_min_stake), 복리; 가치 결합 하한 `max(baseline, k·V_booked)`). |
| **마이너**(컴퓨트 제공자) | 스테이킹된 컴퓨트 역할: 추론을 실행하고 세션 정산 수익과 작업 게이트 보상을 얻는다(§4, §8). 최소 자기 스테이크 [`min_miner_self_stake`](#param-min_miner_self_stake)에 용량 비례 항을 더한다(§6.1). *아무것도 "채굴"되지 않는다; 이 명칭은 관용적 표현이다.* |
| **에이전트** | 컴퓨트 소비자: 세션을 열고, 수수료를 지불하고, FLOP을 보유하는 자율 계정(종종 세션 키를 통해 위임됨, §6.2). |
| **검증자 리더** | 검증자의 에포크별 순환 하위 역할: 암호화된 고스트 태스크를 발행한다(§8.1). 별개의 스테이크나 영구적 특권이 아니다. |
| **위임자** | 보상 지분을 대가로 검증자 또는 마이너의 스테이크를 뒷받침하는 FLOP 보유자(마이너: 자기 스테이크의 ≤10×). |
| **퍼블리셔** | 모델을 등록하는 계정: 가중치 스토리지 임대 보증금과 레지스트리 보증금을 지불한다; 모델의 저자일 필요는 없다. |

*어테스테이션 권한.* **별도의 오라클 역할은 없다.** 활성 검증자가 TEE 쿼트(quote)를
오프체인에서 검증하고 서명된 `ValidatorAttestation` 번들을 제출한다; 활성 검증자의 BFT 쿼럼
(§3.6, §13.3)이 온체인 어테스테이션 권한이다.

| 기호 | 정의 |
|--------|-----------|
| `F_eff` | **유효 FLOPs(Effective-FLOPs)** — 실행 입력으로부터 결정론적으로 산출되는 참조 작업량 회계(§4); 물리적 명령어 수와는 구별된다. |
| `G_n` | `F_eff / 10⁹`; 계량/과금 단위. |
| `P`, `P_active`, `N`, `n_ctx`, `d` | 파라미터 수; 활성 파라미터 수(MoE); 생성 토큰 수; 컨텍스트 길이; 은닉 차원. |
| `G_n_max`, `B_p`, `R_p`, `E_c` | 캘리브레이션 최대값; 플레지 베이스라인(Pledge Baseline); 상한이 적용된 워크 베스팅 플레지 비율(Pledge Ratio) `min(G_n_actual/B_p, 1)`; 효율 계수(Efficiency Coefficient). |
| `C_emp`, `C_effective`, `u_min` | 경험적 캘리브레이션 상한; 티어에 따라 활성화되는 상한; ppm 단위의 최소 캘리브레이션 활용률(§7). |
| `model_hash` | 로드된 가중치에 대한 **측정된** 커밋먼트(dm-verity 머클 루트). |
| `report_data` | 정확히 64 B인 TEE 쿼트 바인딩 값: 어테스트된 태스크 필드에 대한 `SHA256` 다이제스트를 0으로 패딩한 것; [부록 F.1](#f1-identity--binding-preimages)의 `report_data` v1에 따라 도출된다. |
| `output_hash` | 추론 출력에 대한 커밋먼트로, `report_data`와 서명된 `ValidatorAttestation`에 바인딩된다. |
| `task_hash` | 직접 레일 태스크 신원(H256)으로, 도메인 태그가 붙고 배포의 `genesis_hash`에 바인딩된다; [부록 F.1](#f1-identity--binding-preimages)의 `task_hash` v1에 따라 도출된다. |
| `p` | 챌린지 샘플링 확률(낙관적 검증). |
| `H`, `s`, `T_lock` | 해시락 `SHA256(s)`; 프리이미지; HTLC 타임락. |

### 1.2 프로토콜 클록 — 정식 표

보안 논증이 의존하는 모든 시간 상수를 한 곳에 모았다. **결합 불변식**은
클록들을 일관되게 유지하는 규칙이다; 강제되는 결합은 코드에서 검사되고, 원칙적 결합은
리뷰 규칙이다. 모든 지속 시간은 1초 블록을 가정한다. 기준 값은 부록 A에 있다.

| 클록 | 값 | 클록 대상 | 결합 / 불변식 |
|---|---|---|---|
| 블록 시간 | **1 s**(BABE 블록 생성) | 포함, 웨이트 예산 | — |
| 파이널리티 | AlephBFT, 헤드보다 수 초 뒤 | 모든 비가역적 행위(지급, 만료, 슬래시, 프루닝)는 팁이 아니라 `FinalizedPrefix`를 읽는다 | **파이널리티 정지는 구조적으로 경제적 기한을 MUST 동결해야 한다**(§13 F1); 운영 클록은 자금을 해제하지 않는 경우에만 계속 진행할 수 있다 |
| BABE 에포크 / 위원회 세션 | 에포크 **1 h** 프로덕션(`EpochDurationInBlocks`; fast-dev에서는 1 min); 위원회 세션은 모든 빌드에서 **900 blocks**(`AlephEpochBlocks`, ~15 min; 프로덕션에서는 에포크당 4개, fast-dev에서는 15 에포크당 1개) | BABE 랜덤성 에포크; `pallet_aleph`가 매 세션 PoUI 게이트 파이널리티 위원회를 다시 스냅숏한다 | 900블록 세션은 연 35,040회 추첨을 제공한다; 프로덕션에서 한 에포크의 네 세션은 모두 그 에포크의 랜덤성으로부터 추첨된다(R15.4b); 위원회 장악 경계를 적격 집합 집중도와 결합한다(§15) |
| 에이전트 일일 상한 윈도 | **86,400 blocks**([`agent_cap_window_blocks`](#param-agent_cap_window_blocks); 중단 없는 1 s 목표 주기에서 24 h) | 지갑별·세션별 지출 예산 | 지갑 또는 세션 생성 시점에 시작한다; 경계 시점 또는 그 이후의 첫 지출이 해당 예산을 리셋하고 다음 윈도를 시작한다(§6.2). BABE 에포크와 무관하다 |
| PoUI 속도 제한 윈도 | **1 day**([`poui_submission_window_blocks`](#param-poui_submission_window_blocks) = 86,400; [`poui_max_submissions_epoch`](#param-poui_max_submissions_epoch) = 윈도당 10회 제출) | 마이너별 제출 속도 리셋 | 블록 정렬됨; BABE 에포크와 무관하다 |
| `force_open` 확인(ack) 윈도 | **~10 min**([`channel_ack_window_blocks`](#param-channel_ack_window_blocks) = 600) | 무허가 개설에 대한 마이너의 비준 | 확인 누락 ⇒ 슬래시가 아니라 평판 반영; 더스트 하한이 카운터를 게이트한다 |
| 분쟁 응답 윈도 | **~2 h**([`channel_dispute_response_window_blocks`](#param-channel_dispute_response_window_blocks) = 7,200) | 지명된 계쟁 턴에 마이너가 응답할 윈도 | 누락 ⇒ 사기 디폴트 |
| 어테스테이션 중단 일시정지 상한 | **4 h**([`attestation_outage_pause_cap_blocks`](#param-attestation_outage_pause_cap_blocks) = 14,400) | 어테스테이션 의존 클록의 채널별 최대 일시정지(§13 O1) | 범위가 한정된 일시정지이며, 결코 전역 정지가 아니다 |
| 캘리브레이션 버스트 | **10 min**([`calibration_min_burst_blocks`](#param-calibration_min_burst_blocks) = 600) | 마이너 집계 호스트 진입 측정 | 활성 갱신형 상한이 서빙을 게이트한다(§7) |
| 챌린지 / 분쟁 윈도 | **7 days**([`channel_dispute_window_blocks`](#param-channel_dispute_window_blocks) = 604,800) | 강제 정산 계쟁 | 개시까지의 시간 `D`; 분쟁 전체 수명의 한계는 DA 보존 행의 R1.2a이다. ~1 d로의 조정은 분석되었으나 보류되었다 |
| 마이너 언본딩 | **7 days**([`miner_unbonding_blocks`](#param-miner_unbonding_blocks)) | 마이너 스테이크 퇴출 | 세션/분쟁이 활성인 동안 차단된다; 스테이크가 계쟁 기간보다 오래 존속하도록 분쟁 윈도 이상으로 MUST 유지되어야 한다 |
| DA 보존(Ephemeral) | **14 days**([`da_ephemeral_retention_blocks`](#param-da_ephemeral_retention_blocks)) | 트랜스크립트/쿼트 검색 가능성 | R1.2a 전체 생명주기 한계: `W > D + (2·⌈log₂ n_max⌉ + 2)·R`; 현재 `604,800 + 22·7,200 = 763,200 < 1,209,600`. 보장된 수명 이후의 손실 ⇒ 저하 모드의 페일 클로즈드(fail-closed) 환불, 디폴트 판정 없음(§13.0) |
| 체크포인트 | **매일**; 라이트 클라이언트 신선도 **21 days** | 약한 주관성(weak-subjectivity) 앵커 | 고가치 퇴출은 다음 체크포인트까지 SHOULD 냉각되어야 한다(§15) |
| 검증자 언본딩 | **21 days**([`validator_unbonding_blocks`](#param-validator_unbonding_blocks)) | 검증자/위임자 스테이크 퇴출 | 의무를 높이는 모든 거버넌스 변경은 이 값 이상의 시행 지연을 SHOULD 가져야 한다(E.9) |
| 세션 키 수명 | **≤ 864,000 blocks**(`SessionKeysMaxDuration`; 중단 없는 1 s 목표 주기에서 ~10일) | 위임된 에이전트 권한 | 예산 + 팔레트 범위가 피해 범위를 한정한다. *(일부 코드 주석의 "60일" 수치는 6 s 블록 기준의 오래된 해석이다; [`session_key_expiry_days`](#param-session_key_expiry_days) 참조.)* |
| 반감 에라 | **~730 days**([`halving_interval_blocks`](#param-halving_interval_blocks); 5회 반감 + 하한) | 발행 단계; Labs/재단 보조금은 보상과 함께 반감되며 에라 5 하한에서 종료된다 | 반감마다의 이탈 방지 경계 조건이 96→48 참여자 단계를 헤지한다 |

- **R1.2a — 분쟁 전체에 대한 트랜스크립트 보존.** Ephemeral DA 보존 기간 `W`는
  `D + (2·⌈log₂ n_max⌉ + 2)·R`를 **MUST** 초과해야 하며, 이는 최대 깊이 이분 탐색, 말단 리프 응답,
  1회의 R13.0b 저하 모드 연장을 포괄한다. `force_settle`은 참조된 블롭을 고정(pin)하기 전에 그 미래
  블록 시점에서 해당 블롭을 **MUST** 확인해야 한다; 사용 고정은 프루닝을 막지만 블롭의 만료를 **MUST NOT** 연장해서는 안 된다.
  `integrity_test`는 구성된 상수 한계를 **MUST** 강제해야 한다.

**읽기 규칙(규범적 리뷰 게이트).** 더 짧은 클록은 자신이 보호하는 더 긴 클록을 **MUST NOT** 고립시킬 수
있어서는 안 된다: 분쟁은 보존 기간 안에 들어가고, 스테이크는 분쟁보다 오래 존속하며, 체크포인트는 퇴출보다 오래 존속하고, 시행은
언본딩보다 오래 존속한다. 이 값들 중 하나라도 변경하면 결합 열을 MUST 재검토해야 한다.

### 1.3 약어 및 기술 용어

이 스펙에서 사용되는 모든 약어와 자명하지 않은 기술 용어를 한 번씩 풀어 쓴다. 프로토콜 내부
식별자(`open_channel`, `report_data`, …)는 사용 지점과 부록 F–G에서 정의된다;
역할/기호는 §1.1에 있다.

**합의 및 런타임**

| 용어 | 전개 / 의미 |
|------|--------------------|
| **BABE** | *Blind Assignment for Blockchain Extension* — Substrate의 슬롯 기반 블록 생성 엔진 |
| **AlephBFT** | FLOP이 채택한 비동기 BFT 아토믹 브로드캐스트 파이널리티 프로토콜(Aleph, AFT 2019) |
| **BFT** | *Byzantine Fault Tolerant/Tolerance*(비잔틴 장애 허용) — AlephBFT 안전성은 엄격히 `< ⅓`의 비잔틴 위원회 시트를 가정한다 |
| **DAG** | *Directed Acyclic Graph*(유향 비순환 그래프) — 위원회가 순서를 정하는 유닛 그래프 |
| **BFT-DAG** | 비잔틴 합의 프로토콜로 순서가 정해지는 DAG(결정론적 파이널리티) |
| **VRF** | *Verifiable Random Function*(검증 가능 무작위 함수) — 위원회 샘플링의 시드가 되는 BABE 에포크 랜덤성 |
| **FRAME** | Substrate의 런타임 프레임워크(팔레트/런타임 프로그래밍 모델); 실행/상태 계층 |
| **WASM** | *WebAssembly* — `set_code`로 교체되는 온체인 런타임 바이트코드 |
| **SCALE** | 스토리지/익스트린식 페이로드를 위한 Substrate의 정식 바이너리 코덱 |
| **Perbill** | Substrate의 십억분율 고정소수점 타입(예: 어테스테이션 임계값) |
| **RPC / P2P** | 원격 프로시저 호출 인터페이스 / 피어 투 피어 네트워킹 |
| **FinalizedPrefix** | AlephBFT가 파이널라이즈한 블록 프리픽스를 노출하는 엔진 독립적 인터페이스 |

**PoUI 및 검증**

| 용어 | 전개 / 의미 |
|------|--------------------|
| **PoUI** | *Proof of Useful Inference*(유용한 추론 증명) — FLOP의 작업 검증/보상 메커니즘 |
| **TEE** | *Trusted Execution Environment*(신뢰 실행 환경) — 하드웨어 격리 기밀 실행(선택적 HARD 티어, §3.3) |
| **CC** | *Confidential Computing*(기밀 컴퓨팅) — NVIDIA GPU CC 모드(VRAM 암호화 + 어테스테이션) |
| **CVM** | *Confidential Virtual Machine*(기밀 가상 머신) — 어테스테이션된 호스트 VM |
| **TDX** | *Intel Trust Domain Extensions* — 호스트 CPU TEE |
| **DCAP** | *Data Center Attestation Primitives* — Intel의 쿼트 검증 스택(`dcap-qvl` = 그 검증 라이브러리) |
| **dstack** | 런타임이 온체인에서 사용하는 기밀 컴퓨팅 어테스테이션/검증기 스택 |
| **MRTD / RTMR** | TDX 쿼트 내의 *Measurement of Root of Trust for Domain* / *Runtime Measurement Registers*(RTMR0–3) |
| **dm-verity** | Linux 디바이스 매퍼 블록 무결성 타깃; 그 머클 루트가 측정된 `model_hash`이다 |
| **EROFS** | *Enhanced Read-Only File System* — dm-verity가 보호하는 패킹된 읽기 전용 가중치 이미지 |
| **VRAM** | GPU 비디오 메모리(CC 하에서 암호화됨) |
| **TOPLOC** | 활성값 커밋먼트 검증 방식(arXiv:2501.16007); 필수 Tier-2 하한 |
| **RA-TLS** | *Remote-Attestation TLS* — 세션을 인클레이브 키에 바인딩하는 어테스테이션된 전송 계층 |
| **ZK / zkVerify** | *Zero-Knowledge*(영지식) 증명 / 정산 증명 집계 계층(Groth16/PLONK/STARK/RISC0/EZKL 검증기) |
| **GEMM** | *General Matrix Multiply*(일반 행렬 곱) — Freivalds 스폿 체크 분쟁에서 재실행되는 리프 |
| **Freivalds** | Freivalds의 `O(n²)` 확률적 행렬 곱 검증 |
| **KAT** | *Known-Answer Test*(정답 기지 테스트) — 연산 수 엔진을 해석적 연산 수에 고정하는 테스트 |
| **SDC** | *Silent Data Corruption*(무증상 데이터 손상) — 검출되지 않은 하드웨어 연산 오류(드리프트 시그니처) |
| **MLPerf** | 업계 ML 벤치마크 스위트(타당성 상한 참조) |
| **CUPTI / DCGM / nvml** | 인클레이브 내에서 읽는 NVIDIA CUDA 프로파일링 / 데이터센터 GPU 매니저 / 관리 라이브러리 카운터 |
| **MoE** | *Mixture of Experts*(전문가 혼합) — *활성* 파라미터 기준으로 과금되는 모델 |
| **LLM** | *Large Language Model*(대규모 언어 모델) |
| **QKV / FFN** | 어텐션 Query/Key/Value 프로젝션 / 트랜스포머 Feed-Forward Network(연산 수 항) |
| **FP16 / INT8 / INT4** | 16비트 부동소수점 / 8비트 / 4비트 정수 수치 정밀도 |
| **SKU** | *Stock-Keeping Unit* — 여기서는 특정 어테스테이션된 GPU 모델(HARD 티어 상한) |
| **EWMA** | *Exponentially-Weighted Moving Average*(지수 가중 이동 평균) — 드리프트/지연 베이스라인 |
| **SLA** | *Service-Level Agreement*(서비스 수준 협약) — 세션 지연 정책 |

**데이터 가용성 및 스토리지**

| 용어 | 전개 / 의미 |
|------|--------------------|
| **DA** | *Data Availability*(데이터 가용성) — 소버린 검증자 호스팅 스토리지 계층(§5.3) |
| **RS / Reed–Solomon** | 레이트 ½ 소거 부호(`R`=6 샤드, 임의의 `k`=3으로 복원) |
| **Merkle** | 머클 해시 트리/루트(트랜스크립트 누산기, dm-verity, 집계) |
| **SHA256 / blake2_256 / keccak256** | 바인딩 / 신원 / 집계에 사용되는 32바이트 해시 함수 |
| **고스트 태스크(Ghost Task)** | 암호화된 고정 시드 정답 기지 카나리 태스크(라이브니스 + 정확성 + 수요 하한, §8.1) |

**경제, 거버넌스 및 암호**

| 용어 | 전개 / 의미 |
|------|--------------------|
| **Era T** | 거버넌스가 비준한 전환 스냅숏까지 운영되는 공개 인센티브 테스트넷; 그 FLOP은 메인넷 가치가 없다. |
| **Era 0** | 메인넷 제네시스 발행 에라로, Era-T 전환 스냅숏 이후에 시작된다. |
| **VFY** | **FLOP 단위가 아니다** — 토큰 1개 전체와 같은 런타임 *상수*(`VFY = 10¹⁸` 기본 단위)의 이름으로, FLOP이 기반으로 하는 zkVerify 런타임에서 물려받았다. 부록 A가 코드 리터럴을 그대로 옮기는 곳에서만 등장한다; 프로토콜 금액은 FLOP 또는 기본 단위로 표시하며, 결코 VFY로 표시하지 않는다 |
| **HTLC** | *Hashed Timelock Contract*(해시 타임락 계약) — 아토믹 스왑 프리미티브(§10); **MAD-HTLC**는 수수료 매수 공격 모델이다 |
| **MEV** | *Maximal Extractable Value*(최대 추출 가능 가치) — 순서/타이밍 가치 추출(여기서는 컴퓨트 상의 MEV) |
| **FIP** | *FLOP Improvement Proposal* — 레퍼렌덤에 결부된 번호 부여 오프체인 설계 문서 |
| **OpenGov** | FLOP이 채택한 Substrate/Polkadot 온체인 거버넌스 프레임워크 |
| **MADR** | *Markdown Architectural Decision Record* — `D-04xx` 결정 로그의 형식 |
| **FOCIL** | *Fork-Choice-enforced Inclusion Lists*(EIP-7805) — V6를 위한 검열 방지 접근법 |
| **TUF** | *The Update Framework* — 모델 퍼블리싱을 위한 공급망 출처 모델(P3) |
| **TWAP / BOM / EV** | *Time-Weighted Average Price*(시간 가중 평균 가격) / *Bill of Materials*(자재 명세서) / *Expected Value*(기대값) |
| **AEAD** | *Authenticated Encryption with Associated Data*(연관 데이터 인증 암호화) — 내용을 암호화하고 바인딩된 컨텍스트를 인증한다 |
| **PaidObject** | 클라이언트 측에서 암호화된 콘텐츠를 위한 불변의 불투명 애플리케이션 객체로, 자금이 예치된 용량 예약에 기록되며 온체인이 아니라 제공자 그룹의 네임스페이스 매니페스트에 기록된다(§5.4) |
| **용량 예약(Capacity reservation)** | 프로토콜이 배정한 제공자 집합 위에서, 에포크 요율로 예약된 인코딩 바이트에 대해 자금이 예치된 고정 기간 약정; 지불자당 하나이며 여러 네임스페이스를 담는다; 유료 객체는 여기에 기록되고 삭제된 객체는 그 안의 공간을 비운다(§5.4); §12.2의 신원별 컴퓨트 용량 예약과는 별개이다 |
| **에포크 요율(Epoch tariff)** | 에포크마다 하나인 가격 벡터(인코딩 바이트-블록당 임대료, 쓰기당 설정비, 바이트당 회수비, 요청 수수료)로, 용량을 신고한 검증자들의 투표에 대한 스테이크 가중 중앙값에 의해 제한된 스텝 안에서 정해진다(§5.4) |
| **메모리 헤드(Memory head)** | 불변인 유료 객체 버전을 가리키는 파이널라이즈된 가변 포인터로, compare-and-swap으로 갱신된다 |
| **서비스 레인(Service lane)** | `ServiceLane`: 지불자가 용량 예약 아래에서 자금을 예치하는 제공자별 에스크로; 설정비와 회수비를 지불하며, 지불자 또는 위임 대리인이 서명한 누적 바우처로 상환된다(§5.4) |
| **UCAN** | *User-Controlled Authorization Networks* — 감쇠 가능한 권한(capability) 모델(향후 §6.4 계층) |
| **PQ** | *Post-Quantum*(양자 내성) — PQ 프리미티브가 로드맵에 오르기 전까지 범위 외인 암호(§12.4) |
| **sr25519 / ed25519 / secp256k1** | 서명 방식(각각 체인 / NEAR / Bitcoin-NEAR-MPC) |
| **SS58** | Substrate 계정 주소 형식(`flop_account = SS58(derived_pubkey)`) |
| **NEP-141** | NEAR 대체 가능 토큰 표준(브리지된 자산은 동일한 HTLC를 통해 정산된다) |
| **MPC / MITM / P2SH** | *Multi-Party Computation*(다자간 계산) / *Man-in-the-Middle*(중간자) / Bitcoin *Pay-to-Script-Hash* |

**위협 모델 프레임워크(참조만 하며 여기서 정의하지 않음):** OWASP Agentic Top-10, ATFAA, STRIDE,
MITRE ATLAS는 §12.3에서 인용되는 외부 카탈로그이다.

---
