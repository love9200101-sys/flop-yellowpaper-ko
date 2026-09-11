# FLOP Network Yellow Paper — 비공식 한국어 번역

FLOP Labs가 공개한 **FLOP Network Yellow Paper 0.5.0 (draft)** 의 한국어 번역이다.

> **이 번역은 비공식이며 비규범적이다.**
> FLOP Labs가 만들거나 검토하거나 승인한 문서가 아니다. 규범적 효력을 갖는 것은 영문 원문뿐이다.
> 번역과 원문이 어긋나면 **언제나 원문이 옳다.** 구현, 감사, 계약, 투자 판단은 원문을 근거로 해야 한다.

| | |
|---|---|
| 원문 | [flop-labs/yellowpaper](https://github.com/flop-labs/yellowpaper) · `yellowpaper.md` |
| 고정 커밋 | [`3eaf2f2`](https://github.com/flop-labs/yellowpaper/blob/3eaf2f25bc46a501df225cae4e4e991975f6b2a9/yellowpaper.md) |
| 원문 SHA-256 | `cb414e5cdfe72eec048102720c0ebff5e25b00d8910ae2affe137746b59c8ea9` (248,811 바이트) |
| 원문 버전 | 0.5.0 (draft) |
| 번역 기준일 | 2026-09-11 |
| 라이선스 | 원문·번역 모두 [CC BY 4.0](LICENSE) · 저작자 표시와 변경 내역은 [NOTICE.md](NOTICE.md) |

전체를 한 파일로 읽으려면 [`yellowpaper.ko.md`](yellowpaper.ko.md), 절별로 읽으려면 [`ko/`](ko/) 를 보면 된다.
기계 판독용 출처 정보는 [`SOURCE.json`](SOURCE.json)에 있다.

## 무엇을 번역했고 무엇을 그대로 두었나

번역한 것은 **사람이 읽는 문장뿐**이다. 본문, 제목, 표의 서술 칸, 목록, 인용이 이에 해당한다.

다음은 **원문 그대로 유지**했다. 옮기면 의미가 깨지거나 대조가 불가능해지는 것들이다.

- 코드 스팬과 코드 블록, 파라미터 이름 (`genesis_supply`), 팔레트·익스트린식·오류 식별자 (`open_channel`, `BadReceiptSignature`)
- 요구사항·결정·미결 항목 식별자 (`R12.1a`, `D-0438`, `E.38`, `INV-02`, `SPEC-022`)
- 모든 수치와 단위, 수식, 바이트 레이아웃과 타입 (`g_n:u128LE`), 해시·서명 스킴 이름, 16진 문자열
- 절 번호, 링크 대상, HTML 앵커 (`<a id="param-…">`)
- RFC 2119 키워드는 원문의 굵은 영문 그대로 두고 뒤에 한국어 서술을 붙였다. 예: "네 개의 코호트 파라미터는 **MUST** 정확히 합산되어야 한다"

## 어떻게 검증했나

`tools/` 의 스크립트로 누구나 재현할 수 있다.

```sh
python3 tools/verify_source.py     # 원문을 다시 받아 고정 해시와 대조
python3 tools/check_fidelity.py    # 식별자·수치·앵커가 번역에 살아남았는지 대조
```

현재 상태다.

- **구조 일치**: 26개 파일 전부에서 표의 행 수, 제목 개수와 단계, `param-` 앵커의 개수와 순서가 원문과 같다.
- **축자 요소 보존**: 요구사항 ID 109개, 결정 ID 185개, 미결 항목 104개, 파라미터명 653개, 큰 수 124개, RFC 2119 키워드 201개, HTML 앵커 145개를 대조해 단 한 건의 의도된 예외를 빼고 모두 보존됐다.
- 그 예외는 부록 A의 `parts-per-10,000`을 `1만분율`로 옮긴 것이다. 숫자가 아니라 단위 표현이라 한국어로 번역하는 편이 옳다고 판단했다.

**검증하지 않은 것도 분명히 밝힌다.** 위 검사는 기계적 대조일 뿐 의미 검토가 아니다. 원어민 전문가의 문장 단위 감수는 거치지 않았다. 번역 과정에서 옮기기 애매하다고 표시된 대목이 스무 곳가량 있으며, 대부분 원문이 새로 만든 용어이거나 원문 자체가 문장 중간에서 잘린 곳이다.

## 알려진 한계

1. **원문이 초안이다.** 0.5.0은 draft이고 부록 E에는 미결 항목이 29건 남아 있다. 원문이 갱신되면 이 번역은 그만큼 낡는다. 그래서 커밋과 해시를 고정해 두었다. 항상 위 표의 커밋과 비교해서 읽어야 한다.
2. **의미 감수가 남아 있다.** 위 참조.
3. **표준 역어가 없는 용어가 있다.** `serve-or-slash`, `adjudication-inert`, `length-disjoint` 처럼 원문이 새로 만든 표현은 음차하거나 풀어 쓰고 첫 등장 시 영문을 괄호로 병기했다.

오역을 발견하면 이 저장소에 이슈로 알려주기 바란다. **원문 자체의 오류라고 판단되면 이곳이 아니라 [원문 저장소의 이슈](https://github.com/flop-labs/yellowpaper/issues)로 보내야 한다.** 그쪽이 정오표·모호성·이의제기 양식을 갖추고 있다.

## 라이선스와 저작자 표시

원문 저작권자는 FLOP Labs다.

> FLOP Labs, "FLOP Network Yellow Paper", 0.5.0 (draft), 2026.
> https://github.com/flop-labs/yellowpaper

원문은 [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) 으로 배포되며([전문](LICENSE), [저작자 표시와 변경 내역](NOTICE.md)), 이 번역본도 같은 조건으로 배포한다. CC BY 4.0에 따라 **변경 사항을 밝힌다. 이 저작물은 영문 원문을 한국어로 번역한 2차적 저작물이다.**

FLOP Labs는 이 번역을 보증하지 않으며 이 번역과 아무런 관련이 없다. 원문 라이선스는 FLOP Labs의 상표·로고·브랜드 자산에 대한 권리를 부여하지 않으며, 이 저장소도 그것들을 사용하지 않는다.

---

# FLOP Network Yellow Paper — Unofficial Korean Translation

An unofficial Korean translation of the **FLOP Network Yellow Paper 0.5.0 (draft)**.

> **Unofficial and non-normative.** Not produced, reviewed, or endorsed by FLOP Labs.
> Only the English original is normative. **Where this translation and the original
> disagree, the original governs.** Implement, audit, and decide from the English text.

Source: [flop-labs/yellowpaper](https://github.com/flop-labs/yellowpaper) `yellowpaper.md`
at commit `3eaf2f25bc46a501df225cae4e4e991975f6b2a9`,
SHA-256 `cb414e5cdfe72eec048102720c0ebff5e25b00d8910ae2affe137746b59c8ea9` (248,811 bytes),
retrieved 2026-09-11. Pin details in [`SOURCE.json`](SOURCE.json).

Only human-language prose is translated. Code spans, parameter names, requirement and
decision identifiers, numbers, formulas, byte layouts, link targets, HTML anchors and
RFC 2119 keywords are reproduced verbatim. `tools/verify_source.py` re-checks the pinned
source hash and `tools/check_fidelity.py` re-checks that those verbatim classes survived.
Structural parity (table rows, headings, `param-` anchors) holds across all 26 files.
No expert semantic review has been performed; see 알려진 한계 above.

Attribution, per CC BY 4.0:

> FLOP Labs, "FLOP Network Yellow Paper", 0.5.0 (draft), 2026.
> https://github.com/flop-labs/yellowpaper — licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
> **Changes were made: the text was translated from English into Korean.**

FLOP Labs does not endorse this translation. The licence covers the specification text
only and grants no rights in FLOP Labs trademarks, logos, or brand assets; none are used here.
