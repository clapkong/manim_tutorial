# Manim Tutorial

직접 코드를 돌려 보면서 Manim Community Edition(v0.21.0)을 익히는 튜토리얼입니다. 설치된 라이브러리 소스와 [공식 예제 갤러리](https://docs.manim.community/en/stable/examples.html)를 바탕으로 만들었습니다.

## 시작하기

Manim이 이미 설치되어 동작한다고 가정합니다. 실습 사이트는 저장소 폴더를 로컬 서버로 띄워서 열고, 빈칸을 다 채운 코드는 저장소 최상위의 `practice.py`에 붙여 넣어 렌더합니다.

- Manim 외에 추가로 설치할 파이썬 라이브러리는 없음
- LaTeX: 수식과 숫자 라벨(`MathTex`, 좌표축 눈금, `Matrix` 등)을 쓰는 문제에 필요
  - `manim checkhealth`에서 latex 항목이 PASSED면 준비 완료
- 인터넷 연결: 사이트가 md 렌더러, 코드 하이라이터, 글꼴을 CDN에서 불러옴

1. 실습 사이트 열기

   ```bash
   cd manim_tutorial
   python3 -m http.server
   ```

   브라우저에서 http://localhost:8000 에 접속합니다. 서버를 끄려면 터미널에서 `Ctrl + C`.

2. 빈칸 채우기

   사이트에서 챕터를 골라 설명을 읽고 빈칸을 채운 뒤 `채점`을 누릅니다. 다 맞히면 `완성 코드 복사` 버튼이 나옵니다.

3. `practice.py`에 붙여 넣고 렌더하기

   복사한 코드를 저장소 최상위의 빈 파일 `practice.py`에 통째로 붙여 넣고, 서버와는 다른 터미널에서 저장소 폴더 기준으로 실행합니다.

   ```bash
   cd manim_tutorial
   manim -pql practice.py HelloManim     # 마지막 인자는 Scene 클래스 이름
   ```

- `-p`: 렌더가 끝나면 바로 재생, `-ql`: 저화질로 빠르게
- Scene 이름은 사이트의 실행 명령 칸이나 코드의 `class 이름(Scene)`에서 확인
- uv 환경에서 Manim을 쓴다면 명령 앞에 `uv run`을 붙임
- 결과 영상은 `media/videos/practice/480p15/`에 저장 (git에는 올라가지 않음)
- 다음 문제를 풀 때는 `practice.py` 내용을 지우고 새 코드를 붙여 넣으면 됨
- `index.html`을 더블클릭해서 `file://`로 열면 문서를 불러오지 못하므로 꼭 서버로 열기

![](gifs/Epicycles.gif)

## 실습 사이트 구성

각 챕터는 예제마다 제목, 설명, 목표 GIF, 빈칸 코드 순서로 되어 있습니다. 설명에 나온 이름으로 빈칸을 채우면 되고, 예제는 모두 39개입니다. 사이트에서는 바로 채우고 채점할 수 있고, 다 맞히면 완성 코드를 복사해서 직접 렌더할 수 있습니다.

- GitHub에서 md로 읽을 때는 `⟦정답⟧` 부분이 빈칸

문제를 추가하려면 md 파일에 아래 형식의 코드 블록을 넣습니다.

- `⟦정답⟧`: 빈칸
- `⟦정답|다른정답⟧`: 여러 답 허용
- `id`: 사이트 전체에서 겹치지 않게
- `gif`: `gifs/` 폴더의 파일 이름 (확장자 제외)

````
```exercise
id: ch01-example
title: 원을 그리고 사각형으로 바꾸기
scene: ch01_basics.py HelloManim
gif: HelloManim
hint: 선을 그리는 애니메이션은 Create
---
from manim import *

class HelloManim(Scene):
    def construct(self):
        self.play(⟦Create⟧(Circle()))
```
````

## Manim 명령 모음

원본 예제는 `scenes/` 폴더에 챕터별로 있고, `manim` 명령에 파일과 Scene 이름을 넘겨 렌더합니다. 결과물은 `media/videos/<파일명>/<화질>/` 아래에 저장됩니다.

```bash
# 한 장면 렌더 + 미리보기
uv run manim -pql scenes/ch01_basics.py HelloManim

# 파일 안의 모든 Scene 렌더
uv run manim -ql -a scenes/ch01_basics.py

# GIF로 저장 / 마지막 프레임만 PNG로 저장
uv run manim -ql --format gif scenes/ch01_basics.py HelloManim
uv run manim -ql -s scenes/ch01_basics.py HelloManim
```

| 플래그 | 의미 |
|---|---|
| `-ql` / `-qm` / `-qh` / `-qk` | 480p15 / 720p30 / 1080p60 / 4K60. 작업 중엔 `-ql`, 최종본은 `-qh` |
| `-p` | 렌더 후 바로 재생 |
| `-s` | 마지막 프레임만 이미지로 (레이아웃 확인할 때 제일 빠름) |
| `-a` | 파일 안의 모든 Scene |
| `-n 3,5` | 3~5번째 애니메이션만 렌더 (긴 장면 디버깅) |
| `--format gif/webm/mov` | 출력 형식 |
| `-t` / `--transparent` | 투명 배경 (영상 편집 툴에 얹을 때) |
| `-r 1080,1920` | 해상도 직접 지정 |
| `--save_sections` | `next_section()` 단위로 파일 분리 |
| `--disable_caching` | 캐시 끄기 (소리가 빠지는 등 이상할 때) |

- `MathTex`, `Tex`: LaTeX 설치 필요
  - macOS는 MacTeX
- `Text`: LaTeX 없이 동작

## 목차

| 장 | 내용 | 예제 파일 |
|---|---|---|
| [1. Scene과 Mobject](01_basics.md) | 도형, 배치, 색, 중괄호, 불리언 연산 | `ch01_basics.py` |
| [2. 애니메이션](02_animations.md) | Create/Transform, `.animate`, rate function, 조합, 강조 | `ch02_animations.py` |
| [3. 텍스트, 수식, 코드](03_text_math.md) | Text, MathTex, TransformMatchingTex, Code | `ch03_text_math.py` |
| [4. Updater와 ValueTracker](04_updaters.md) | 살아 움직이는 객체, 에피사이클 | `ch04_updaters.py` |
| [5. 좌표계와 그래프](05_plotting.md) | Axes, 넓이, 미분, 복소함수 | `ch05_plotting.py` |
| [6. 카메라](06_camera.md) | 따라가기, 줌, 돋보기 | `ch06_camera.py` |
| [7. 3D](07_3d.md) | 곡면, 입체, 카메라 회전 | `ch07_3d.py` |
| [8. 자료구조 시각화](08_structures.md) | Graph(BFS), Matrix, Table, BarChart | `ch08_structures.py` |
| [9. 고급 프로젝트 (공식)](09_advanced.md) | OpeningManim, SineCurveUnitCircle, 다시 짠 버전 | `ch09_advanced.py` |
| [10. 실제 영상 만들기](10_production.md) | 스타일, 컴포넌트, 섹션, 소리, 자막, SVG/이미지, 쇼츠 | `ch10_production.py`, `ch10_shorts.py` |

1~4장을 먼저 보는 것을 추천합니다. 4장(updater)까지 익히면 대부분의 장면을 만들 수 있고, 그다음 만들고 싶은 영상에 맞춰 5~8장을 골라 본 뒤 9장과 10장으로 마무리합니다.

## 이 튜토리얼이 다루는 범위

라이브러리의 `animation/`, `mobject/`, `scene/`, `camera/` 모듈 기준입니다. 다루지 않는 기능은 필요할 때 공식 문서에서 찾아보면 됩니다.

| 분야 | 다룸 | 다루지 않음 |
|---|---|---|
| 도형 | Circle, Polygon, Star, Line, Arrow, Brace, 불리언 연산 | `ArcPolygon`, `Cutout`, `LabeledArrow`, 화살촉 종류(`StealthTip` 등) |
| 애니메이션 | 등장, 변형, 강조, 이동, 조합, rate func | `Homotopy`, `PhaseFlow`, `ChangeSpeed`, `Broadcast`, `SpiralIn` |
| 텍스트 | Text, MarkupText, MathTex, Tex, Code, TypeWithCursor | `Paragraph`, `BulletedList`, `Typst`/`MathTypst`(0.21 신기능, typst 설치 필요) |
| 그래프 | Axes, 넓이, 리만 합, 할선, ComplexPlane, NumberLine | `PolarPlane`, `ImplicitFunction`, 로그 축, `plot_line_graph` |
| 카메라 | MovingCamera, ZoomedScene, ThreeDCamera | `MultiCamera`, `MappingCamera` |
| 3D | Surface, 기본 입체, 카메라 이동 | `ThreeDAxes.plot_parametric_curve`, 조명과 셰이딩 세부 |
| 구조 | Graph, Matrix, Table, BarChart | `DiGraph`, `MobjectTable`, `SampleSpace` |
| 제작 | config, 섹션, 소리, 자막, SVG, 이미지, 벡터장, 세로 영상 | OpenGL 렌더러와 `interactive_embed()`, 플러그인(manim-slides, manim-voiceover) |

## 참고 링크

- 공식 문서: https://docs.manim.community/
- API 레퍼런스: https://docs.manim.community/en/stable/reference.html
- 라이브러리 소스: `.venv/lib/python3.13/site-packages/manim/`
  - 예: `animation/indication.py`에 강조 애니메이션이 모두 있음
