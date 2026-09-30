# Manim Tutorial

직접 코드를 돌려 보면서 Manim Community Edition(v0.21.0)을 익히는 튜토리얼입니다.
설치된 라이브러리 소스(`.venv/lib/python3.13/site-packages/manim`)와
[공식 예제 갤러리](https://docs.manim.community/en/stable/examples.html)를 바탕으로 만들었습니다.

![](gifs/Epicycles.gif)

## 실습 사이트로 보기

이 문서들은 빈칸 채우기 실습 사이트(`index.html`)로도 볼 수 있습니다. 설명을 읽고, 목표 GIF를 보고, 코드의 빈칸을 채워 채점합니다.

```bash
uv run python -m http.server     # 저장소 폴더에서 실행
# 브라우저에서 http://localhost:8000 접속
```

GitHub Pages(Settings → Pages → `main` 브랜치 루트)를 켜면 설치 없이 바로 열 수 있습니다.
`file://`로 직접 열면 문서를 불러오지 못하니 꼭 서버로 여세요.

문제를 추가하려면 md 파일에 아래 형식의 코드 블록을 넣으면 됩니다. `⟦정답⟧`이 빈칸이 되고, `⟦정답|다른정답⟧`처럼 여러 답을 허용할 수 있습니다.

````
```exercise
id: ch01-hello          # 사이트 전체에서 겹치지 않게
title: 원을 그리고 사각형으로 바꾸기
scene: ch01_basics.py HelloManim
gif: HelloManim         # gifs/HelloManim.gif
hint: 선을 그리는 애니메이션은 Create
---
from manim import *

class HelloManim(Scene):
    def construct(self):
        self.play(⟦Create⟧(Circle()))
```
````

## 0. 시작하기

```bash
# 한 장면 렌더 + 미리보기 (-p: 끝나면 재생, -ql: 480p15 저화질 = 빠름)
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

결과물은 `media/videos/<파일명>/<화질>/` 아래에 저장됩니다.

> **LaTeX**: `MathTex`, `Tex`는 LaTeX 설치가 필요합니다 (이 맥에는 MacTeX가 있습니다). `Text`는 LaTeX 없이 됩니다.

## 목차

| 장 | 내용 | 예제 파일 |
|---|---|---|
| [1. Scene과 Mobject](01_basics.md) | 도형, 배치, 색, 중괄호, 불리언 연산 | `ch01_basics.py` |
| [2. 애니메이션](02_animations.md) | Create/Transform, `.animate`, rate function, 조합, 강조 | `ch02_animations.py` |
| [3. 텍스트·수식·코드](03_text_math.md) | Text, MathTex, TransformMatchingTex, Code | `ch03_text_math.py` |
| [4. Updater와 ValueTracker](04_updaters.md) | 살아 움직이는 객체, 에피사이클 | `ch04_updaters.py` |
| [5. 좌표계와 그래프](05_plotting.md) | Axes, 넓이, 미분, 복소함수 | `ch05_plotting.py` |
| [6. 카메라](06_camera.md) | 따라가기, 줌, 돋보기 | `ch06_camera.py` |
| [7. 3D](07_3d.md) | 곡면, 입체, 카메라 회전 | `ch07_3d.py` |
| [8. 자료구조 시각화](08_structures.md) | Graph(BFS), Matrix, Table, BarChart | `ch08_structures.py` |
| [9. 고급 프로젝트 (공식)](09_advanced.md) | OpeningManim, SineCurveUnitCircle + 리팩터링 | `ch09_advanced.py` |
| [10. 실제 영상 만들기](10_production.md) | 스타일, 컴포넌트, 섹션, 소리·자막, SVG/이미지, 쇼츠 | `ch10_production.py`, `ch10_shorts.py` |

**추천 순서**: 1 → 2 → 3 → 4를 먼저 보세요. 4장(updater)까지 익히면 대부분의 장면을 만들 수 있습니다.
그다음 만들고 싶은 영상에 맞춰 5~8장을 골라 보고, 9장과 10장으로 마무리합니다.

## 이 튜토리얼이 다루는 범위

라이브러리의 `animation/`, `mobject/`, `scene/`, `camera/` 모듈 기준입니다.

| 분야 | 다룸 | 다루지 않음 (필요할 때 찾아보기) |
|---|---|---|
| 도형 | Circle, Polygon, Star, Line, Arrow, Brace, 불리언 연산 | `ArcPolygon`, `Cutout`, `LabeledArrow`, 화살촉 종류(`StealthTip` 등) |
| 애니메이션 | 등장/변형/강조/이동/조합/rate func | `Homotopy`, `PhaseFlow`, `ChangeSpeed`, `Broadcast`, `SpiralIn` |
| 텍스트 | Text, MarkupText, MathTex, Tex, Code, TypeWithCursor | `Paragraph`, `BulletedList`, `Typst`/`MathTypst`(0.21 신기능, typst 설치 필요) |
| 그래프 | Axes, 넓이, 리만 합, 할선, ComplexPlane, NumberLine | `PolarPlane`, `ImplicitFunction`, 로그 축, `plot_line_graph` |
| 카메라 | MovingCamera, ZoomedScene, ThreeDCamera | `MultiCamera`, `MappingCamera` |
| 3D | Surface, 기본 입체, 카메라 이동 | `ThreeDAxes.plot_parametric_curve`, 조명·셰이딩 세부 |
| 구조 | Graph, Matrix, Table, BarChart | `DiGraph`, `MobjectTable`, `SampleSpace` |
| 제작 | config, 섹션, 소리, 자막, SVG, 이미지, 벡터장, 세로 영상 | OpenGL 렌더러와 `interactive_embed()`, 플러그인(manim-slides, manim-voiceover) |

## 참고 링크
- 공식 문서: https://docs.manim.community/
- API 레퍼런스: https://docs.manim.community/en/stable/reference.html
- 막히면 소스를 직접 보세요: `.venv/lib/python3.13/site-packages/manim/` (예: `animation/indication.py`에 강조 애니메이션이 전부 있습니다)
