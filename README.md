# 제미나이 4 아르곤 API 호출 예제 — 원자 모형 만들기

코난쌤 유튜브 영상 「제미나이 4 아르곤 직접 써봤습니다」의 직접 호출 구간(07:44~09:12)에서 쓴 코드와 결과물이에요.

- **결과 페이지 바로 보기:** https://conanssam.com/gemini4-argon-demo/
  (영상에 나온 실행에서 아르곤이 만든 HTML 그대로예요. API 키 없이 열려요.)

## 무엇을 했나요

Gemini API로 `gemini-4-argon` 모델에 한 문장 요청을 보냈어요.

> HTML 파일 하나로 '아르곤 원자' 인터랙티브 모형을 만들어 줘. 가운데 원자핵, 전자껍질 3개(전자 2·8·8개)가 궤도를 도는 애니메이션, 껍질을 클릭하면 오른쪽 카드에 그 껍질 설명이 나오게. 라벨은 한국어, 밝은 배경, 외부 라이브러리 없이. 코드만 출력해.

영상에 나온 실행 기록(`example/last_run.json`):

| 항목 | 값 |
|---|---|
| 첫 글자까지 | 3.8초 |
| 전체 생성 | 46.6초 (기록값 46.55초) |
| 입력 / 출력 토큰 | 113 / 4,939 |
| 저장한 HTML | 15,115자 |

같은 요청으로 먼저 시험했을 땐 전체 50.9초가 걸렸고 화면 구성도 달랐어요. **돌릴 때마다 결과가 달라요.**

## 파일

| 파일 | 설명 |
|---|---|
| `argon.py` | 모델 정보 조회(`--info`)와 스트리밍 호출. 파이썬 표준 라이브러리만 써요 |
| `prompt.txt` | 영상에서 쓴 요청문 |
| `example/argon-atom.html` | 영상에 나온 생성 결과(원본) |
| `example/last_run.json` | 그 실행의 시간·토큰 기록 |
| `index.html` | 위 결과와 같은 파일(GitHub Pages용) |

## 직접 돌려 보기

필요한 것: Python 3, 인터넷, `gemini-4-argon`을 쓸 수 있는 Gemini API 키(유료 플랜).

```sh
# 키는 코드나 저장소에 쓰지 말고 환경변수로만 넣어요 (zsh 예시, 화면에 안 보이게 입력)
read -s 'GEMINI_API_KEY?Gemini API key: '
export GEMINI_API_KEY

python3 argon.py --info                                        # 모델 정보: 입력·출력 한도, 생각 모드
python3 argon.py "$(cat prompt.txt)" --out argon-atom-new.html # 새로 생성 (API 비용이 들어요)
```

만든 `argon-atom-new.html`을 브라우저로 열고 원자핵과 K·L·M 껍질을 눌러 보세요. 실행할 때마다 `last_run.json`이 새 기록으로 바뀌고, 영상 기록은 `example/`에 그대로 남아요.

## 한계

- 모델 정보 조회와 텍스트 생성만 다뤄요. 이미지·영상 입력, 로봇 제어, 안티그래비티 연동은 없어요.
- 자동 재시도나 사용량 상한이 없어요. API 오류는 파이썬 예외로 보여요.
- 원자 모형은 전자 배치 2·8·8을 보여 주는 단순화한 그림이에요. 실제 전자 운동 시뮬레이션이 아니고, 수업에 쓰기 전에 설명 문구를 꼭 검토하세요.
- 영상의 약 0.05달러는 2026-10-13 발표 기준 출시 특가(100만 토큰당 입력 2달러·출력 10달러)로 계산한 값이에요. 실제 청구액이 아니고, 특가는 2026-11-30에 끝나요. 쓰기 전에 현재 요금과 제공 여부를 확인하세요.

## 출처

- 구글 발표(2026-10-13): https://blog.google/intl/ko-kr/products/introducing-gemini-4-argon-kr/
- 로보틱스 글(모델 ID `gemini-4-argon`): https://developers.googleblog.com/gemini-4-argon-for-robotics/

`argon.py`는 MIT 라이선스예요. `example/argon-atom.html`·`index.html`은 Gemini 4 Argon이 생성한 결과물을 그대로 둔 예시예요.
