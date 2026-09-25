## 부록 F — 메시지와 저장 포맷

정규(canonical) 와이어 상·온체인 필드 레이아웃(규범적). 모든 해시는 32바이트이며, 다중 필드
프리이미지는 나열된 순서대로 필드를 연결(`‖`)한다. 별도 언급이 없는 한 온체인 저장/익스트린식
페이로드의 코덱은 SCALE이다. 정규(canonical) 양성/음성 코퍼스는
[`evidence/wire-format-v1.json`](evidence/wire-format-v1.json)이며,
[`evidence/wire-format-v1.schema.json`](evidence/wire-format-v1.schema.json)으로 검증한다. 생성 또는 확인은
`uv run --script evidence/generate-wire-format-vectors.py [--check]`로 하며, Rust, TypeScript, Python 테스트가
모두 동일한 파일을 사용한다.

### F.0 코덱과 거부 프로파일

- 고정 부호 없는 정수는 정확히 `u8`/`u16`/`u32`/`u64`/`u128`이며 리틀 엔디언이다. 인코더는 음수 또는
  오버플로 입력을 **MUST** 거부해야 하며, 포화, 잘림, 부동소수점 변환, 반올림은 허용되지 않는다.
  `H256`, AccountId32, 공개 키, 서명은 각각 32/32/32/64바이트 원시 문자열이다.
- SCALE 구조체 필드는 선언 순서대로 연결된다. 열거형(enum) 판별자는 1바이트이며 아래에 나열한다.
  `bool`은 `00`/`01`, `Option<T>`는 `00` 또는 `01 ‖ T`, `Vec<T>`는 정규(canonical) SCALE `Compact<u32>(count) ‖
  items`이다. 알 수 없는 태그, 유효하지 않은 불리언/옵션, 비최소 컴팩트 정수, 잘린 필드, 한계
  위반, 또는 길이 구분 객체 내부의 후행 바이트는 **MUST** 거부해야 한다.
- `Compact<u32>`는 `2⁶` 미만에서 1바이트, `2¹⁴` 미만에서 2바이트, `2³⁰` 미만에서 4바이트를 사용하고, 그 외에는 `03 ‖ u32LE`이다.
  길이는 요소 개수이며 결코 바이트 수가 아니다. 공개 코퍼스에는 `0`, 모든 모드 경계,
  `u32::MAX`, 잘린 인코딩, 과장 인코딩, 그리고 `u32`보다 넓은 값이 포함된다.
- 해시는 표시된 정확한 바이트에 대해 계산하며, 명시적 도메인을 넘어서는 암묵적 SCALE, UTF-8 종결자, 길이,
  개인화(personalization)는 없다. sr25519는 Substrate `b"substrate"` 서명 컨텍스트를 사용하며 명시된
  메시지 바이트 또는 32바이트 리프 해시에 서명한다. F.7의 스토리지 메시지를 제외하면, 서명되는 메시지는
  검증자 어테스테이션, 트랜스크립트 리프, 에이전트 영수증 v1, 턴별 에이전트 확인(ack)이며, 확인 메시지는
  `channel_id ‖ turn_index:u32LE ‖ leaf_hash ‖ agent_send_ms:u64LE ‖ agent_recv_ms:u64LE`이다.

### F.1 신원과 바인딩 프리이미지

| 이름 | 프리이미지 / 정의 | 비고 |
|------|----------------------|-------|
| 다이렉트 레일 `task_hash` v1 | `blake2_256("FLOP/POUI/TASK" ‖ 01 ‖ genesis_hash:H256 ‖ agent:AccountId32 ‖ nonce:u64LE ‖ model_hash ‖ payload_hash ‖ commit_hash)` | 생산자가 파생한 태스크 신원. 런타임은 불투명한 H256을 수신하고 배포 로컬 `ProcessedTasks` 맵에서 재사용을 거부한다. 검증자는 서명 전에 이 v1 파생을 **MUST** 요구해야 한다 |
| 컴퓨트 `channel_id` v1 | `blake2_256("FLOP/COMPUTE_CHANNEL/ID" ‖ 01 ‖ genesis_hash:H256 ‖ agent:AccountId32 ‖ miner:AccountId32 ‖ nonce:u64LE)` | 런타임이 파생한다. 프로토콜, 배포/네트워크, 당사자, 세션 논스를 바인딩한다 |
| `model_hash` | 패킹된 가중치 이미지의 dm-verity 머클 루트(4 KB 블록) | 측정된 커밋먼트(§3.3). `(model, precision)`별로 레지스트리에 핀 고정된다 |
| `output_hash` | 추론 출력에 대한 커밋먼트 | `report_data` + `ValidatorAttestation`에 바인딩된다 |
| `decode_policy_hash` v1 | `SHA256("FLOP_DECODE_POLICY_HASH_V1" ‖ SCALE(DecodePolicy))` | `DecodePolicy = version:u16(1), class, tokenizer_hash, SamplingParams, stop_conditions_hash, output_transform, class_policy_hash`. 클래스 태그는 `TextGeneration=0`, `ImageDenoise=1`, `Rollout=2`, `ControlLoop=3`, `Other(u16)=4`. 출력 변환 태그는 `Identity=0`, `TransformId(H256)=1` |
| `SamplingParams` | `temperature_milli:u32, top_p_ppm:u32, top_k:u32, repetition_penalty_ppm:u32, beam_width:u16, seed:u64` | 이 순서의 고정 폭 SCALE. 정수 정책으로 부동소수점 인코딩을 피한다 |
| `report_data` v1 | `SHA256(task_hash ‖ gn_weight:u64LE ‖ latency_ms:u64LE ‖ model_hash ‖ output_hash ‖ decode_policy_hash ‖ SCALE(tee_type)) ‖ 00×32` | 정확히 64 B. TEE 태그는 `IntelTdx=0`, `NvidiaHopperCc=1`, `NvidiaRubinCc=2`, `Simulator=3` |

다이렉트 레일의 런타임은 페이로드, 커밋, 에이전트, 논스가 모두 호출 인자는 아니기 때문에 `task_hash`를
재구성할 수 없다. 배포된 시행은 대기 중인 H256과의 정확한 일치 및 로컬 리플레이 거부에서 시작한다. 이는
암묵적 폴백이 아니라 명시적 신뢰 경계다. 배포 간 보호는 어테스테이션 이전에 생산자 측 v1 파생을 시행하는
활성 검증자에게 달려 있다.

### F.2 어테스테이션과 증명(다이렉트 레일, §3.6)

| 구조 | 필드 | 제약 |
|-----------|--------|-----------|
| `ValidatorAttestation` v1 | 순서대로 `task_hash:H256`, `gn_weight:u64`, `latency_ms:u64`, `model_hash:H256`, `output_hash:H256`, `decode_policy_hash:H256`, `tee_type`, `quote_verified:bool`, `event_log_verified:bool`, `hardware_id_hash:H256`, `validator_id:[u8;32]`, `signature:[u8;64]` | 고정 필드 SCALE 크기 275 B. 서명은 `validator_id`와 `signature`를 제외한 처음 열 개 필드(179 B)를 포함한다. 서명자는 MUST 활성이어야 하고, 서명 대상 튜플은 MUST 바이트 단위로 일치해야 하며, 서명자 ID는 MUST 서로 달라야 하고, 번들은 MUST 정족수를 충족해야 한다 |
| 어테스테이션 정족수 | `ceil(active_count × `[`validator_attestation_threshold`](#param-validator_attestation_threshold)`).max(1)` 명의 서로 다른 서명자 | 기본값 2/3, 루트가 거버넌스 가능 |
| `PendingVerifications` / `PendingProof` | `task_hash`를 키로 하는 증명 레코드 | `ProcessedTasks[task_hash]`로 리플레이 방지 |
| `StarkProof`(제출) | ≤ 약 2 MB 호출 데이터 | 일시적. 블록과 함께 정리되며 온체인 저장이 **아니다** |
| 집계 루트 | 검증된 `keccak256` 명제 해시에 대한 도메인별 머클 루트 | 크로스체인 디스패치 |

### F.3 세션 트랜스크립트(컴퓨트 채널, §12.1)

| 구조 | 필드 | 제약 |
|-----------|--------|-----------|
| `TranscriptLeafVersion` | `V0=0`, `V1=1`, `V2=2`, `V3=3` | 현재의 모든 정산/분쟁 턴 컨테이너 시작부의 필수 SCALE 열거형(enum). 알 수 없는 태그는 거부한다. 검증기는 정확히 하나의 프리이미지를 선택하며 결코 재시도하지 않는다 |
| `VerifiedTurn` | 순서대로: `leaf_version`, `turn_index:u32`, `h_in:H256`, `h_out:H256`, `g_n:u128`, `decode_policy_hash:H256`, `h_ids:H256`, `toploc_commitment_hash:H256`, `miner_recv_ms:u64`, `miner_done_ms:u64`, `latency_ms:u64`, `enclave_sig:[u8;64]`, `merkle_path:Vec<(H256,bool)>` | 경로 길이 `L`에 대해 SCALE 크기 `269 + compact_len(L) + 33L` B |
| V3 리프 | `blake2_256(channel_id ‖ turn_index:u32LE ‖ h_in ‖ h_out ‖ g_n:u128LE ‖ decode_policy_hash ‖ h_ids ‖ toploc_commitment_hash ‖ miner_recv_ms:u64LE ‖ miner_done_ms:u64LE ‖ latency_ms:u64LE)` | 236 B 프리이미지. 서명은 32 B 리프 해시에 대한 것이다. FCC4에서 `h_ids`는 MUST 0이 아니어야 한다 |
| V2 리프 | `h_ids`와 `toploc_commitment_hash`가 없는 V3 | 172 B 프리이미지. 디코드 정책을 바인딩하지만 V3의 토큰 ID/TOPLOC 바인딩은 주장하지 않는다(#1404) |
| V1 리프 | `decode_policy_hash`가 없는 V2 | 140 B 프리이미지. 채널에 `ChannelDecodePolicies` 마커가 없는 경우에만 레거시로 허용된다(#686) |
| V0 리프 | 세 개의 타이밍 필드가 없는 V1 | 116 B 프리이미지. 채널에 `ChannelDecodePolicies` 마커가 없는 경우에만 레거시로 허용된다 |
| 머클 경로 | 각 항목은 `(sibling_hash:H256, sibling_is_left:bool)`. 노드 = `blake2_256(left ‖ right)` | 리프 순서는 턴 순서다. 왼쪽이 먼저다. 홀수인 마지막 노드는 복제된다. 빈 루트는 `00×32`다. 단일 리프 루트는 그 리프다. 노드의 64 B 프리이미지는 모든 리프 프리이미지와 길이가 서로 겹치지 않으므로 노드에는 접두사가 없다 |
| 턴별 에이전트 확인(ack) | 채널의 에이전트 키로 `channel_id ‖ turn_index:u32LE ‖ leaf_hash ‖ agent_send_ms:u64LE ‖ agent_recv_ms:u64LE`에 대해 서명한 sr25519 | 리프 해시와 두 타이밍 입력에 대해 역서명(counter-sign)한다. 에이전트 영수증 v1과는 별개다. `sdk/typescript/src/compute-channel/transcript.ts`와 `sdk/rust-compute-channel/src/transcript.rs`의 `turn_ack_message`로 구현된다 |
| 에이전트 영수증 v1 | `"FLOP/COMPUTE_CHANNEL/RECEIPT" ‖ 01 ‖ channel_id ‖ final_root ‖ aggregate_gn:u128LE ‖ payable:u128LE`에 대한 sr25519 | 정확한 채널, 루트, 집계, 정산 금액을 인가한다. `payable`은 10⁻¹⁸ FLOP 기본 단위 개수를 나타내는 `u128LE`이며, 감사 및 선도(forward) 조정 이전의 영수증 바인딩 총 정산 금액이다. 협력적 `settle`에서는 예약된 에스크로 전액, `force_settle`에서는 R12.1d 요율 `P`, 선도 채널에서는 저장된 `contract_payment` 재정의 값으로 파생된다(R12.1i). 마이너에게 가는 순이전액은 `payable`에서 감사 적립분(earmark)을 뺀 값이며, 선도 채널은 추가로 미획득 가용성 대금을 구매자에게 환불한다. 현재 채널에만 해당 |
| `aggregate_gn` 검사 | 서명/경로 검증 이후 제출된 서로 다른 `VerifiedTurn.g_n`의 검사된 합(`verified_work_from_turns`) | `aggregate_gn`과 MUST 같아야 한다. 산술/인증만 해당(§11.2 R11.2a) |
| 번들 한계 | ≤ [`channel_max_settlement_turns`](#param-channel_max_settlement_turns) 턴. 경로 ≤ [`channel_max_merkle_path_len`](#param-channel_max_merkle_path_len) | — |
| `ChallengeWindowExtensions` | `channel_id:H256 → extensions:u8` | 채널별 DA 저하 시 기한 연장 횟수로, 최대 1이다(R13.0b). 단 한 번의 연장은 현재 진행 중인 챌린지 또는 응답 기한에 [`channel_dispute_response_window_blocks`](#param-channel_dispute_response_window_blocks)를 더하며, 채널이 닫힐 때 초기화된다 |

**R12.1i — 영수증 `payable`.** 검증은 에이전트 영수증 v1의 `payable`을 위 행이 정의하는 대로
채널 상태와 정산 경로로부터 **MUST** 파생해야 한다.

**수락 버전 컷오프.** `ChannelDecodePolicies[channel_id]`가 존재하면 명시적으로 태그된
V2/V3 리프만 수락하고 동일한 정책 해시를 요구한다. 마커가 없으면(정책 바인딩 이전에 열린 채널) 명시적
V0–V3을 수락한다. `ChannelWireProfiles[channel_id]=1`은 영수증 v1을 요구한다. 마커가 없으면 과거의
태그 없는 96 B 영수증 프리이미지만 수락하며, 알 수 없는 값은 실패 폐쇄(fail closed)한다. 신규 개설은
디코드 정책 마커와 와이어 프로파일 마커를 기록한다. 기존 채널
레코드와 금액은 재작성되지 않는다. V2는 명시적으로 더 낮은 증거 포맷으로 남으며 V3/TOPLOC 바인딩
보증으로 보고되어서는 **MUST NOT** 안 된다. 남아 있는 그 수락을 제거하거나 바인딩을 추가하는 일은 #1404이 담당한다.

**R12.1j — 채널별 디코드 정책.** 개설 시 `ChannelDecodePolicies[channel_id]`는 하나의
`decode_policy_hash`를 핀 고정한다. 그 해시는 파이프라인에 참여하는 에이전트 수와 관계없이 해당 `channel_id` 아래의
모든 V2/V3 턴에서 **MUST** 동일해야 하며, 턴마다 **MUST NOT** 달라져서는 안 된다.

**DA 트랜스크립트 컨테이너.** 현재 SDK는 `FCC4 ‖ channel_id:H256 ‖ turn_count:u32LE`를 내보내고, 이어서 각
턴을 `leaf_version:u8 ‖ turn_index:u32LE ‖ h_in ‖ h_out ‖ g_n:u128LE ‖ has_policy:u8 [‖ policy_hash] ‖
h_ids:H256 ‖ toploc_hash:H256 ‖ recv:u64LE ‖ done:u64LE ‖ latency:u64LE ‖ enclave_sig:[u8;64] ‖ has_ack:u8
[‖ send:u64LE ‖ receive:u64LE ‖ agent_sig:[u8;64]]`로 내보내며, 여기서 `agent_sig`는 채널의 에이전트 키로 `channel_id ‖
turn_index:u32LE ‖ leaf_hash ‖ send:u64LE ‖ receive:u64LE`에 서명한 것이다. `has_*`는
정확히 0/1이다. FCC4 버전/필드 일관성은
실패 폐쇄다. V0/V1은 정책이 없고 V3 필드가 0이다. V2는 정책이 있고 V3 필드가 0이다. V3은 정책이 있고
`h_ids`가 0이 아니다. 디코더는 선언된 턴을 정확히 소비하고 후행/잘린 바이트를 거부한다. Rust/TS는
과거의 접두사 없는/FCC2/FCC3 블롭을 명시적 인메모리 리프 버전으로 마이그레이션하기 위해서만 읽을 수 있다.
이들은 결코 서명 성공으로부터 온체인 버전 선택을 하지 않는다.

### F.4 데이터 가용성(§5.3)

| 구조 | 필드 | 제약 |
|-----------|--------|-----------|
| `DataRef` v1 | 순서대로 SCALE `commitment:H256, provider_id:u8, retention_class` | 고정 34 B. 보존 기간 태그는 `Ephemeral=0`, `Leased=1`. 알 수 없는 제공자는 레지스트리 조회에 실패하고 알 수 없는 보존 기간은 SCALE 디코드에 실패한다 |
| 제공자 부분집합 | 검증자의 `hash(commitment) → subset` | 스테이크 가중, 결정적 |
| 소거 부호화 | Reed–Solomon 비율 ½: [`da_shard_count`](#param-da_shard_count) R=6, [`da_min_replication_factor`](#param-da_min_replication_factor) k=3 | R 중 임의의 k로 복원 |
| 보존 기간 클래스 | `Ephemeral`(≥ 챌린지 윈도) · `Leased`(고정 기간 + 환급 가능 보증금) | §5.3 R5.3d |
| 감사 챌린지 | 정답이 알려진 `blake2(audit_id ‖ shard)` | 보유 바인딩(제공 또는 슬래시) |

### F.5 TOPLOC 밴드 상수(§3.4)

`band_verdict` / `report_toploc_mismatch`가 사용하는 `(model, precision)`별 거버넌스 설정 상수:
`kappa_profile_hash`, `band_tau_accept`, `band_tau_slash`(
[`toploc_band_tau_accept_bf16_milli`](#param-toploc_band_tau_accept_bf16_milli),
[`toploc_band_tau_slash_bf16_milli`](#param-toploc_band_tau_slash_bf16_milli) 참조). 두 임계값 정책:
수락 / 에스컬레이션 / 슬래시. 셀은 이종 하드웨어
게이트를 통과하기 전까지 판정 비활성(커밋먼트 필요) 상태다.

### F.6 수락/정산 트레이스

| 벡터 계열 | 수락 소비자 경로 | 부정/거부 경로 |
|---------------|------------------------|-------------------------|
| `direct_rail_v1` | `submit_validator_attestations → check_one → check_threshold → process_verified_poui_result` | 알 수 없는 열거형(enum)/불리언, 잘못된 서명, 비활성/중복 서명자, 튜플 불일치, 대기 태스크 없음, 리플레이, 또는 정족수 부족 |
| `compute_channel_v1.channel_id/receipt` | `open_channel/force_open → channel_id`; `settle/force_settle → verify_receipt` | 잘못된 제네시스/네트워크, 당사자, 논스, 세션, 영수증 버전, 루트, 집계, 지급, 또는 서명 |
| `compute_channel_v1.leaf_versions/merkle` | `settle/force_settle → verified_work_from_turns → verify_turn_proof`; `respond_dispute` | 지원되지 않는 레거시 버전, 정책 불일치, 중복/범위 초과 턴, 잘못된 서명, 잘못된 경로/방향/루트, 과도한 경로, 또는 검사된 합 오버플로 |
| `compute_channel_v1.fcc4_transcript_blob` | Rust/TS/Python SDK DA 페치/감사/증거 빌더; 마이너 `record_ack` | 알 수 없는 컨테이너/리프 버전, 일관되지 않은 선택 필드, 유효하지 않은 옵션, 잘림, 후행 바이트, 또는 `verify_turn_ack`에 실패하는 에이전트 확인(ack) |
| `data_ref_v1` | `da_registry::register_blob/pin/is_live` 및 컴퓨트 채널 정산 | 알 수 없는 열거형(enum)/제공자, 누락/만료된 블롭, 잘못된 커밋먼트/보존 기간, 또는 핀 고정 실패 |
| V3 TOPLOC 필드 | `submit_toploc_evidence/report_toploc_mismatch` 및 정산 존재/에스컬레이션 게이트 | 0/누락 커밋먼트, 잘못된 채널/모델/정책/세션 바인딩, 미보정 셀, 미해결 에스컬레이션, 또는 불일치 판정 |

---

### F.7 유료 객체 스토리지(§5.4)

**R5.4o — 레코드 인코딩.** 각 레코드는 명시적 프로파일 버전을 **MUST** 담아야 하며 알 수 없는 변형은 거부한다. 서명은 체인
제네시스 해시와 서로 구별되는 메시지 유형 도메인을 **MUST** 바인딩해야 한다. 모든 리스트/문자열은 **MUST** 한계가 있어야 한다.
아래의 논리 필드는 **MUST** 존재해야 하며, 정규(canonical) 폭, 필드 순서, 코덱/암호 스위트,
도메인 바이트, 언어 간 벡터는 활성화 이전에 E.54가 **MUST** 확정해야 한다.

| 레코드 | 필수 논리 필드 | 수락 제약 |
|---|---|---|
| `EpochTariff`(온체인) | 에포크, 인코딩된 바이트 블록당 임대료 분자/분모, 제공자별 쓰기당 설정 수수료, 바이트당 회수 분자/분모, 요청 수수료, 이전 요율, 적용된 스텝 한계, 거버넌스 하한/상한 버전, 선언자 수 및 선언/여유 용량, 트립와이어 카운터 | 선언자 투표의 스테이크 가중 중앙값. 스텝 한계 이내. 에포크이 시작되면 불변 |
| `CapacityDeclaration`(온체인) | 제공자, 에포크, 제공 인코딩 바이트, 배정 인코딩 바이트, 예약된 담보, 투표 | 배정에 대한 동의. 용량과 담보는 동시 의무 간에 재사용되지 않음. 투표는 선언이 있을 때만 집계됨 |
| `CapacityReservation`(온체인) | 예약 ID, 지불자, 요율 버전, 제공자별 예약 인코딩 바이트, 배정 이력/세대, 활성화/종료, 에스크로, 제공자별 누적 임대료 카운터와 구간 예산, 네임스페이스 수, 이전 이력, 종료 사유, 담보 예약과 유보된 임대료, 상태, 청구 기한 | 보존성. 테이크 오어 페이(take-or-pay). 기간당 지불자별 하나. 장애 청구 우선. 과금 대상 배정의 중첩 없음 |
| `ServiceLane`(온체인) | 지불자, 제공자, 예약, 레인 논스, 요율 버전, 고정 예산, 상환된 쓰기/바이트/요청/금액, 정책 에포크, 종료 경계, 청구 기한, 상태 | 레인 예산은 보유 자금을 분할한다. 누적 카운터 집합당 하나의 요율. 모든 네임스페이스와 위임 대리인이 공유. 유효한 청구가 만료되기 전에는 환불 없음 |
| `ProviderCheckpoint`(온체인) | 제공자, 에포크, (네임스페이스 → 매니페스트 루트, 헤드 루트, 시퀀스)에 대한 루트, 누적 카운터 커밋먼트, 서명 | 에포크당 제공자별 하나. 유예 기간 이후 누락되거나 영수증과 충돌하면 장애다. 포함 증명은 클라이언트가 검증 가능 |
| `NamespaceManifest`(오프체인, 제공자 그룹) | 예약 ID, 네임스페이스, 시퀀스, 객체, 헤드, 툼스톤, 라이브 인코딩 바이트, 시퀀서 세대, 쿼럼 영수증 | 세대 순서 시퀀서가 순서를 매김. 모든 항목에 쿼럼 영수증. 루트는 각 제공자의 체크포인트에 커밋됨 |
| `PaidObject`(매니페스트 항목) | 네임스페이스, 불투명 객체 ID, 버전, 소유자, 페이로드 커밋먼트/길이, 선언된 암호/청크 엔벨로프 프로파일, 코덱 프로파일, 샤드 커밋먼트 루트, 비공개 매니페스트 커밋먼트, 보관(custody) 영수증, 설정 수수료 지급 플래그, 상태 | 불변의 불투명 페이로드. 한계가 있는 엔벨로프. 예약의 여유 바이트에 맞아야 함. 클라이언트는 평문 이름, 내용, 키를 오프체인에 둔다. 어드미션은 암호화나 비밀성을 증명하지 않음 |
| `MemoryHead`(매니페스트 항목, 핀 고정 시에만 온체인) | 네임스페이스, 불투명 키, 객체 ID/버전, 이전 버전, 시퀀스, 정책 에포크, 툼스톤 | 인가된 비교 후 교환(compare-and-swap). 체인에 핀 고정된 헤드는 해당 키에 대해 권위를 가짐. 한계가 있는 메타데이터 |
| `HeadReceipt`(오프체인) | 네임스페이스, 키, 이전 버전, 새 버전, 객체, 시퀀스, 시퀀서, 제공자 서명 | E.54 헤드 쿼럼. 한 제공자의 상충하는 영수증은 이중 서명(equivocation) 장애다 |
| `ObjectCapability` | 발행자, 주체, 네임스페이스/객체 범위, 연산, 바이트/요청/지출 한도, 만료, 정책 에포크, 위임 부모, 서명 | 요청 키 소유. 권한 축소(attenuation). 최종 확정된 취소와 지갑 한도 |
| `ServiceVoucher`(오프체인) | 레인, 시퀀스, 객체/버전, 요청 논스/범위 커밋먼트, 누적 활성화 쓰기, 요청별 중복 제거된 바이트, 요청 수와 금액, 인가된 지불자/위임 대리인 서명 | 누적 증분만. 요청 수와 수수료는 첫 청크 이전에 증가한다. 레인, 제공자, 객체, 체인 간 재사용 없음 |
| 서비스 어드미션 레코드(오프체인) | 제공자/지불자/상위 허용량, 연산/작업/요청 ID, 예약/소비된 바이트와 작업량, 미지급 익스포저, 재시도 카운터, 재충전 시계, 기한 | 원자적 총량 한도. 영속적이거나 실패 폐쇄. 차감 바우처가 아님 |
| 보관(custody) / 서비스 증거 | 예약, 객체, 배정 세대, 제공자, 샤드 위치/커밋먼트, 챌린지 ID, 구간, 오프닝/증명, 체크포인트 포함 증명, 서명자 | E.54 객관적 증명. 해시 에코나 제공자 로그로는 불충분 |

---
