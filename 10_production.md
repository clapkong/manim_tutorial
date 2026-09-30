# 10. 실제 영상 만들기

예제 원본: [`scenes/ch10_production.py`](scenes/ch10_production.py), [`scenes/ch10_shorts.py`](scenes/ch10_shorts.py)

## 핵심 개념

1~9장은 기능을 다뤘고, 이 장은 한 편의 영상을 만들고 관리하는 방법을 다룹니다. 채널 스타일을 한 곳에서 정하고, 반복되는 요소를 부품으로 만들고, 영상을 구간으로 나눠 편집 툴로 넘기는 흐름입니다.

## Episode: 한 편의 영상 구조

인트로, 본문, 아웃트로로 나뉜 짧은 영상 한 편입니다. 파일 맨 위에서 배경색과 글자 크기 기본값을 정하고, 설명 박스와 챕터 제목은 클래스로 만들어 재사용합니다. 구간마다 `next_section`으로 나눠 두면 구간별 영상 파일을 따로 뽑을 수 있고, 효과음과 자막도 코드에서 넣을 수 있습니다.

```bash
manim -pqh practice.py Episode --save_sections --disable_caching
```

- `config.background_color`: 배경색
- `Text.set_default(font_size=36)`: 클래스별 기본값
  - 팀 프로젝트라면 이 설정을 `style.py`로 빼서 모든 장면에서 사용
- `class Callout(VGroup)`: 반복되는 요소를 `VGroup` 상속 클래스로 제작
  - `__init__`에서 `super().__init__()` 호출 후, 부품을 만들어 `self.add(...)`로 담음
  - 만든 뒤에는 보통 Mobject처럼 배치하고 애니메이션 가능
- `pop_in(mob)`: 자주 쓰는 애니메이션 조합을 Animation을 돌려주는 함수로 제작
- `self.next_section("이름")`: 여기서부터 새 구간
  - `--save_sections`를 주면 구간별 mp4가 따로 나옴
- `self.add_sound("파일.wav")`: 지금 시점에 효과음
- `self.add_subcaption("문장", duration=초)`: 자막
  - 영상 옆에 `.srt` 파일이 생김
  - 소리와 자막은 mp4에만 들어감 (GIF에는 없음)
- `TransformMatchingShapes(a, b)`: 모양이 같은 글자끼리 짝지어 변형
  - 3장의 `TransformMatchingTex`와 달리 조각을 나눌 필요 없음
- ⚠️ 캐시된 애니메이션 재사용 시 소리가 누락될 수 있으니 최종 렌더는 `--disable_caching` 권장
- 내레이션을 코드와 맞추려면 [manim-voiceover](https://voiceover.manim.community/) 플러그인 참고

![](gifs/Episode.gif)

```exercise
id: ch10-episode
title: 섹션, 자막, 컴포넌트로 한 편 만들기
scene: ch10_production.py Episode
gif: Episode
hint: 구간 나누기는 next_section, 자막은 add_subcaption, 효과음은 add_sound, 모양 기준 매칭은 TransformMatchingShapes.
---
from pathlib import Path

from manim import *

ASSETS = Path("assets")  # 저장소 폴더에서 실행한다고 가정

config.background_color = "#1e1e2e"
Text.set_default(font_size=36)
MathTex.set_default(font_size=48)

ACCENT = "#f5c2e7"
SUB = "#89b4fa"


class Callout(⟦VGroup⟧):  # 여러 부품을 담는 묶음 클래스를 상속
    """둥근 박스 안의 설명 문구. 영상 전체에서 같은 모양을 쓰고 싶을 때."""

    def __init__(self, text: str, color=ACCENT, **kwargs):
        super().__init__(**kwargs)
        label = Text(text, font_size=28)
        box = RoundedRectangle(
            corner_radius=0.2, width=label.width + 0.6, height=label.height + 0.4,
            stroke_color=color, fill_color=color, fill_opacity=0.15,
        )
        self.add(box, label)


class ChapterTitle(VGroup):
    def __init__(self, number: int, title: str, **kwargs):
        super().__init__(**kwargs)
        num = Text(f"Part {number}", font_size=28, color=SUB)
        name = Text(title, font_size=56, weight=BOLD)
        line = Line(LEFT * 3, RIGHT * 3, color=ACCENT)
        self.add(VGroup(num, name, line).arrange(DOWN, buff=0.25))


# ── 3. 재사용 가능한 애니메이션 = Animation 을 돌려주는 함수 ───────────
def pop_in(mob, **kwargs):
    return FadeIn(mob, scale=0.6, rate_func=rate_functions.ease_out_back, **kwargs)


def pop_in(mob, **kwargs):
    return FadeIn(mob, scale=0.6, rate_func=rate_functions.ease_out_back, **kwargs)


class Episode(Scene):
    """next_section 으로 구간을 나눈 '한 편의 영상'."""

    def construct(self):
        # ── 인트로
        self.⟦next_section⟧("intro")  # 여기서부터 인트로 구간
        title = ChapterTitle(1, "피타고라스 정리")
        self.play(pop_in(title))
        self.⟦add_subcaption⟧("오늘은 피타고라스 정리를 봅니다.", duration=2)  # 자막 넣기
        sound = ASSETS / "ding.wav"
        if sound.exists():
            self.⟦add_sound⟧(str(sound))  # 효과음 넣기
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP))

        # ── 본문: 도형
        self.next_section("figure")
        tri = Polygon(ORIGIN, RIGHT * 3, UP * 2, color=WHITE).move_to(LEFT * 2)
        a_lab = MathTex("a").next_to(tri, LEFT)
        b_lab = MathTex("b").next_to(tri, DOWN)
        c_lab = MathTex("c").move_to(tri.get_center() + UR * 0.5)
        self.play(Create(tri), Write(VGroup(a_lab, b_lab, c_lab)))
        note = Callout("직각삼각형의 세 변").next_to(tri, RIGHT, buff=1)
        self.play(pop_in(note))
        self.add_subcaption("직각삼각형의 세 변을 a, b, c 라고 합시다.", duration=2)
        self.wait(1.5)

        # ── 본문: 식
        self.next_section("formula")
        eq = MathTex("a^2", "+", "b^2", "=", "c^2").next_to(tri, RIGHT, buff=1)
        self.play(FadeOut(note, shift=UP), Write(eq))
        self.play(Circumscribe(eq, color=ACCENT))

        # TransformMatchingShapes: TeX 조각 지정 없이 '모양'이 같은 글자끼리 매칭
        swapped = MathTex("c^2 = b^2 + a^2").move_to(eq)
        self.play(⟦TransformMatchingShapes⟧(eq, swapped, path_arc=PI / 2))  # 모양이 같은 글자끼리 짝지어 변형
        self.wait()

        # ── 아웃트로
        self.next_section("outro")
        self.play(*[FadeOut(m) for m in self.mobjects])
        end = Callout("구독과 좋아요", color=SUB).scale(1.5)
        self.play(pop_in(end))
        self.wait()
```

## ExternalAssets: SVG와 이미지 가져오기

외부에서 만든 그림을 화면으로 가져오는 예제입니다. SVG는 path마다 도형으로 들어와서 그리기, 색칠, 변형이 모두 되고, 비트맵 이미지는 이동, 회전, 크기 조절만 됩니다. Figma나 Illustrator에서 만든 로고와 아이콘을 SVG로 내보내면 그대로 애니메이션할 수 있습니다.

- `SVGMobject("파일.svg")`: 벡터 그림
- `ImageMobject("사진.png")`: 비트맵 이미지
- `ImageMobject(numpy배열)`: 배열을 바로 이미지로
  - `(높이, 폭, 3)` 모양의 `uint8` 배열
- `Group(...)`: 이미지와 도형을 섞어서 묶을 때 사용
  - `ImageMobject`는 벡터 도형이 아니라서 `VGroup`에 넣을 수 없음
- `DrawBorderThenFill(mob)`: 테두리를 그린 뒤 속을 채우며 등장
  - SVG 로고에 잘 어울림

![](gifs/ExternalAssets.gif)

```exercise
id: ch10-assets
title: SVG와 이미지 가져오기
scene: ch10_production.py ExternalAssets
gif: ExternalAssets
hint: SVG는 SVGMobject, 비트맵과 numpy 배열은 ImageMobject. ImageMobject는 VMobject가 아니라서 VGroup 대신 Group으로 묶습니다.
---
from pathlib import Path

from manim import *

ASSETS = Path("assets")  # 저장소 폴더에서 실행한다고 가정

config.background_color = "#1e1e2e"

ACCENT = "#f5c2e7"
SUB = "#89b4fa"


class ExternalAssets(Scene):
    """SVG, 비트맵 이미지, numpy 배열을 화면에 가져오기."""

    def construct(self):
        # SVG: path 하나하나가 VMobject 로 들어와서 Create/색칠이 다 된다
        svg = ⟦SVGMobject⟧(str(ASSETS / "rocket.svg")).set_height(2.5)  # SVG 파일 불러오기
        svg_label = Text("SVGMobject", font_size=24)

        # numpy 배열 → 이미지 (픽셀 단위로 직접 만든 그라데이션)
        n = 256
        arr = np.zeros((n, n, 3), dtype=np.uint8)
        arr[..., 0] = np.linspace(0, 255, n)[None, :]
        arr[..., 2] = np.linspace(255, 0, n)[:, None]
        img = ⟦ImageMobject⟧(arr).set_height(2.5)  # numpy 배열을 이미지로
        img_label = Text("ImageMobject(np.array)", font_size=24)

        col1 = ⟦Group⟧(svg, svg_label).arrange(DOWN)  # 이미지와 도형을 섞어 묶기
        col2 = Group(img, img_label).arrange(DOWN)
        Group(col1, col2).arrange(RIGHT, buff=2)

        self.play(⟦DrawBorderThenFill⟧(svg), FadeIn(svg_label))  # 테두리를 그린 뒤 속을 채우며 등장
        self.play(FadeIn(img), FadeIn(img_label))
        self.play(svg.animate.set_color_by_gradient(ACCENT, SUB), img.animate.rotate(PI / 12))
        # ImageMobject("path/to/photo.png") 처럼 파일 경로도 된다
        self.wait()
```

## FlowField: 벡터장과 유선

벡터장을 화살표로 보여 준 뒤, 같은 벡터장을 따라 흐르는 선으로 바꾸는 예제입니다. 물리나 미분방정식을 설명할 때 씁니다. 두 가지 모두 점을 받아 벡터를 돌려주는 함수 하나로 만듭니다.

- `ArrowVectorField(함수)`: 화살표 벡터장
- `StreamLines(함수)`: 흐르는 선
- `stream.start_animation(warm_up=True, flow_speed=)`: 흐르기 시작
- `stream.end_animation()`: 흐름 멈춤
  - `self.play()`에 넣어서 사용

![](gifs/FlowField.gif)

```exercise
id: ch10-flow
title: 흐르는 벡터장
scene: ch10_production.py FlowField
gif: FlowField
hint: 화살표 벡터장은 ArrowVectorField, 흐르는 선은 StreamLines와 start_animation.
---
from manim import *

config.background_color = "#1e1e2e"


class FlowField(Scene):
    """ArrowVectorField + StreamLines: 물리/미분방정식 시각화."""

    def construct(self):
        def func(p):
            x, y = p[0], p[1]
            return np.array([np.sin(y), np.sin(x), 0]) * 0.8

        field = ⟦ArrowVectorField⟧(func, x_range=[-7, 7, 1], y_range=[-4, 4, 1])  # 화살표 벡터장
        self.play(Create(field), run_time=1.5)
        self.wait(0.5)

        stream = ⟦StreamLines⟧(func, stroke_width=3, max_anchors_per_line=30, padding=1, colors=[BLUE, TEAL, YELLOW])  # 벡터장을 따라 흐르는 선
        self.play(FadeOut(field))
        self.add(stream)
        stream.⟦start_animation⟧(warm_up=True, flow_speed=1.5)  # 흐름 시작
        self.wait(3)
        self.play(stream.⟦end_animation⟧())  # 흐름 멈추기
```

## LinearMap: 선형대수 전용 Scene

행렬 하나로 평면 전체를 변환하는 3b1b 스타일 예제입니다. `LinearTransformationScene`은 격자와 기저 벡터(i-hat, j-hat)를 미리 준비해 두기 때문에, 벡터를 추가하고 행렬을 적용하기만 하면 됩니다.

- `LinearTransformationScene`: 선형대수 전용 Scene
  - 옵션은 `__init__`에서 넘김
- `leave_ghost_vectors=True`: 변환 전 벡터의 흐린 자국을 남김
- `self.add_vector([x, y])`: 벡터 추가
- `self.apply_matrix([[a, b], [c, d]])`: 행렬 변환
- `self.add_foreground_mobject(mob)`: 변환되지 않는 객체 추가
  - 행렬 라벨 등에 사용
- ⚠️ v0.21에서는 `apply_matrix` 바로 앞에 `self.wait()`를 넣으면 라벨과 흐린 자국이 한 번 더 변환되는 문제가 있음

![](gifs/LinearMap.gif)

```exercise
id: ch10-linear
title: 행렬로 평면 밀기(shear)
scene: ch10_production.py LinearMap
gif: LinearMap
hint: 선형대수 전용 Scene은 LinearTransformationScene. 벡터 추가는 add_vector, 변환은 apply_matrix, 변환되지 않을 라벨은 add_foreground_mobject.
---
from manim import *

config.background_color = "#1e1e2e"


class LinearMap(⟦LinearTransformationScene⟧):  # 선형대수 전용 Scene
    """LinearTransformationScene: 3b1b 스타일 행렬 변환."""

    def __init__(self, **kwargs):
        super().__init__(⟦leave_ghost_vectors⟧=True, **kwargs)  # 변환 전 벡터의 흐린 자국 남기기

    def construct(self):
        matrix = [[1, 1], [0, 1]]  # shear
        label = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}").to_corner(UL).add_background_rectangle()
        self.⟦add_foreground_mobject⟧(label)  # 변환되지 않는 라벨
        self.⟦add_vector⟧([1, 2], color=YELLOW)  # 벡터 (1, 2) 추가
        # 주의: 여기서 self.wait() 를 넣으면 라벨/ghost 가 한 번 더 변환되는 버그가 있다 (v0.21)
        self.⟦apply_matrix⟧(matrix)  # 행렬로 평면 변환
        self.wait()
```

## VerticalShort: 세로 영상 (쇼츠 / 릴스)

파일 맨 위에서 `config`를 바꾸면 그 파일의 모든 Scene에 적용됩니다. 세로 영상은 픽셀 해상도뿐 아니라 화면 좌표계 크기까지 9:16으로 바꿔야 좌표계도 세로가 됩니다. 화면 폭이 9밖에 안 되니 글자와 도형 크기를 다시 잡아야 합니다. 예제는 점 삼각형을 복사해 뒤집어 맞물리는 "1부터 n까지의 합" 증명입니다.

- `config.pixel_width`, `config.pixel_height`: 픽셀 해상도
  - 쇼츠는 1080 × 1920
- `config.frame_width`, `config.frame_height`: 화면 좌표계 크기
  - 9 × 16으로 설정
- `dots.copy().rotate(PI)`: 복사해서 180도 회전
- `TransformFromCopy(a, b)`: 원본은 두고 복사본이 b로 이동

![](gifs/VerticalShort.gif)

```exercise
id: ch10-shorts
title: 세로 영상(9:16) 만들기
scene: ch10_shorts.py VerticalShort
gif: VerticalShort
hint: 쇼츠 해상도는 1080×1920. 화면 좌표도 폭 9 : 높이 16으로 맞춥니다.
---
from manim import *

config.pixel_width = ⟦1080⟧  # 가로 픽셀
config.pixel_height = ⟦1920⟧  # 세로 픽셀
config.frame_width = 9
config.frame_height = ⟦16⟧  # 화면 좌표계 높이 (폭 9 : 높이 16)
config.background_color = "#101014"


class VerticalShort(Scene):
    def construct(self):
        hook = Text("1 + 2 + 3 + ... = ?", font_size=64).to_edge(UP, buff=1.5)
        self.play(Write(hook))

        dots = VGroup()
        for row in range(1, 7):
            dots.add(VGroup(*[Dot(radius=0.18, color=BLUE) for _ in range(row)]).arrange(RIGHT, buff=0.15))
        dots.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT) for r in dots], lag_ratio=0.2))

        # 180° 돌린 복사본을 맞물리면 n × (n+1) 직사각형이 된다
        step = dots[0][0].width + 0.15  # 점 하나 + 간격
        copy = dots.⟦copy⟧().set_color(ORANGE).rotate(⟦PI⟧)  # 복사해서 180도 회전
        copy.align_to(dots, UP).align_to(dots, RIGHT).shift(RIGHT * step)
        self.play(⟦TransformFromCopy⟧(dots, copy, path_arc=PI / 2), run_time=1.5)  # 원본은 두고 복사본이 날아가 맞물림
        self.play(VGroup(dots, copy).animate.move_to(ORIGIN))

        answer = MathTex(r"\frac{n(n+1)}{2}", font_size=96).to_edge(DOWN, buff=2)
        self.play(Write(answer))
        self.play(Circumscribe(answer, color=YELLOW))
        self.wait()
```

## 권장 작업 흐름

```
1. 스토리보드: 장면별로 "무엇을 보여줄지"를 한 줄씩 적는다
2. 장면 = Scene 클래스 하나 (30초~1분 단위로 짧게)
3. 작업 중엔 -ql, 레이아웃 확인은 -s, 긴 장면은 -n 으로 일부만
4. 공통 스타일과 컴포넌트는 style.py / components.py 로 분리
5. 최종: -qh --disable_caching, 필요하면 --save_sections
6. 편집 툴(Premiere, DaVinci, CapCut)에서 장면을 이어 붙이고 내레이션과 BGM 추가
   (배경 없이 합성하려면 -t 로 투명 mov)
```

## ✍️ 최종 과제

여러분 영상의 첫 30초를 만들어 보세요.

1. `style.py`에 색상과 폰트 기본값을 정해 보세요.
2. `ChapterTitle`과 `Callout` 같은 컴포넌트를 2개 이상 만들어 보세요.
3. 인트로, 본문, 아웃트로를 `next_section`으로 나눠 보세요.
4. 지금까지 배운 것 중 최소 하나(수식 전개, updater, 그래프, 카메라 중 하나)를 본문에 넣어 보세요.
5. `-qh --save_sections --disable_caching`으로 렌더해 보세요.
