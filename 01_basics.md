# 1. Scene과 Mobject

예제 원본: [`scenes/ch01_basics.py`](scenes/ch01_basics.py)

## 핵심 개념

Manim 영상 한 편은 `Scene` 하나이고, 화면에 나오는 모든 것(도형, 글자, 그래프)은 `Mobject`입니다. `Scene`의 `construct()` 안에서 Mobject를 만들고, `self.play()`로 애니메이션을 재생하면 그 한 번의 재생이 영상 한 토막이 됩니다.

```
Scene(장면)  ─ construct() 안에 연출을 순서대로 쓴다
  └─ Mobject(화면 객체)  ─ Circle, Text, Axes ... 전부 Mobject
       └─ self.play(Animation)  ─ Mobject를 움직이고, 한 번의 play가 영상 한 토막이 된다
```

- `ORIGIN`: 화면 중앙 `(0, 0, 0)`
  - 기본 화면 크기는 가로 약 14.2, 세로 8
- `UP`, `DOWN`, `LEFT`, `RIGHT`, `UL`, `UR`, `DL`, `DR`: 방향 벡터
  - numpy 벡터라서 더하고 곱할 수 있음. 예: `LEFT * 3 + UP`
- `VGroup(a, b, ...)`: 여러 Mobject를 하나로 묶음
  - 묶음 단위로 이동, 정렬, 색칠, 애니메이션 가능

이 장부터는 예제마다 설명, 목표 GIF, 빈칸 코드 순서로 진행합니다. 설명에 나온 이름으로 빈칸을 채워 보세요.

## HelloManim: 가장 작은 Scene

Manim 영상 한 편은 `Scene`을 상속한 클래스 하나이고, `construct()` 안에 적은 순서대로 장면이 진행됩니다. 도형은 `Circle()`, `Square()`처럼 클래스 이름으로 만들고, 크기, 색, 채우기 같은 속성은 인자로 넘깁니다. 만든 도형은 `self.play()`에 애니메이션으로 넣어야 화면에 나타납니다.

- `Circle(radius=)` / `Square(side_length=)`: 원 / 정사각형 생성
  - `color`: 테두리 색
  - `fill_opacity`: 채우기 불투명도 (0~1)
- `self.play(애니메이션)`: 애니메이션 재생
- `Create(mob)`: 테두리를 따라 그리며 등장
- `Transform(a, b)`: a의 모양을 b의 모양으로 변경
- `self.wait(초)`: 멈춤
  - 인자를 비우면 1초

실행 명령은 아래와 같습니다. `-p`는 렌더가 끝나면 바로 재생, `-ql`은 저화질로 빠르게 렌더하는 옵션입니다.

```bash
manim -pql practice.py HelloManim
```

![](gifs/HelloManim.gif)

```exercise
id: ch01-hello
title: 원을 그리고 사각형으로 바꾸기
scene: ch01_basics.py HelloManim
gif: HelloManim
hint: 선을 그리며 등장하는 애니메이션은 Create, 모양을 바꾸는 애니메이션은 Transform입니다.
---
from manim import *


class HelloManim(Scene):
    """가장 작은 Scene: 원 하나를 그리고 사각형으로 바꾼다."""

    def construct(self):
        circle = ⟦Circle⟧(radius=1.5, color=BLUE, fill_opacity=0.5)  # 원 만들기
        square = Square(side_length=3, color=ORANGE, fill_opacity=0.5)

        self.play(⟦Create⟧(circle))  # 원을 그리며 등장
        self.play(⟦Transform⟧(circle, square))  # 원을 사각형 모양으로 변형
        self.⟦wait⟧()  # 1초 대기
```

## ShapesAndLayout: 도형과 배치

도형의 위치를 좌표로 일일이 계산하는 대신 배치 메서드를 씁니다. 배치 메서드는 대부분 자기 자신을 돌려주기 때문에 `Circle().shift(UP).set_color(RED)`처럼 이어서 쓸 수 있습니다. 여러 도형을 한꺼번에 배치할 때는 `VGroup`으로 묶은 뒤 묶음에 메서드를 호출합니다.

- `VGroup.arrange(방향, buff=)`: 묶음 안의 객체를 한 줄로 정렬
  - `RIGHT`면 가로, `DOWN`이면 세로
  - `buff`: 객체 사이 간격
- `VGroup.arrange_in_grid(rows=, cols=, buff=)`: 격자로 정렬
- `mob.next_to(기준, 방향, buff=)`: 기준 객체의 해당 방향 옆에 붙임
- `mob.to_edge(UP)` / `mob.to_corner(UR)`: 화면 가장자리 / 모서리로 이동
- `mob.move_to(점 또는 객체)` / `mob.shift(벡터)`: 절대 이동 / 상대 이동
- `mob.align_to(기준, LEFT)`: 기준 객체와 한쪽 끝을 맞춤
- `set_color`, `set_fill`, `set_stroke`: 색, 채우기, 테두리 변경
- `set_color_by_gradient(색1, 색2)`: 묶음 전체에 그라데이션 색
- `LaggedStart(*애니메이션들, lag_ratio=)`: 여러 애니메이션을 조금씩 시간차를 두고 재생
  - 2장에서 자세히 다룸

![](gifs/ShapesAndLayout.gif)

```exercise
id: ch01-layout
title: 도형을 한 줄로 늘어놓고 라벨 붙이기
scene: ch01_basics.py ShapesAndLayout
gif: ShapesAndLayout
hint: VGroup.arrange(방향)으로 정렬하고, next_to(기준, 방향)로 옆에 붙이고, to_edge(UP)로 화면 위쪽에 붙입니다.
---
from manim import *


class ShapesAndLayout(Scene):
    """도형 만들기 + 배치(arrange / next_to / to_edge) + 색."""

    def construct(self):
        shapes = VGroup(
            Circle(radius=0.8, color=BLUE, fill_opacity=0.6),
            Square(side_length=1.6, color=GREEN, fill_opacity=0.6),
            Triangle(color=RED, fill_opacity=0.6).scale(1.1),
            RegularPolygon(n=6, color=YELLOW, fill_opacity=0.6),
            Star(n=5, outer_radius=0.9, color=PURPLE, fill_opacity=0.6),
        ).⟦arrange⟧(RIGHT, buff=0.5)  # 가로로 0.5 간격 정렬

        names = ["Circle", "Square", "Triangle", "RegularPolygon", "Star"]
        labels = VGroup(*[Text(n, font_size=20).⟦next_to⟧(s, ⟦DOWN⟧) for n, s in zip(names, shapes)])  # 도형마다 아래쪽에 이름 붙이기

        title = Text("Mobject = 화면에 나오는 모든 것", font_size=36).⟦to_edge⟧(UP)  # 제목을 화면 위쪽 끝으로

        self.play(Write(title))
        self.play(⟦LaggedStart⟧(*[GrowFromCenter(s) for s in shapes], lag_ratio=0.2))  # 도형을 시간차를 두고 하나씩 등장
        self.play(FadeIn(labels, shift=UP * 0.3))
        self.wait()

        # 그리드 배치와 그라데이션 색
        self.play(FadeOut(labels))
        self.play(shapes.animate.⟦arrange_in_grid⟧(rows=2, buff=0.6).set_color_by_gradient(BLUE, PINK))  # 2줄 격자로 재배치하며 그라데이션 색칠
        self.wait()
```

## BraceAnnotation: 중괄호로 주석 달기 (공식 예제)

도형이나 선분 옆에 중괄호를 붙이고 그 위에 설명을 다는 예제입니다. 중괄호는 대상 객체의 크기에 맞춰 자동으로 늘어나고, 라벨도 중괄호 옆 알맞은 자리에 붙습니다.

- `Brace(mob)`: 객체 아래쪽에 중괄호 생성
  - `direction=벡터`로 방향 변경
- `brace.get_text("...")`: 중괄호에 일반 글자 라벨
- `brace.get_tex("...")`: 중괄호에 수식 라벨
- `GrowFromCenter(mob)`: 가운데에서부터 커지며 등장
  - 중괄호에 잘 어울림
- 같은 `play()`에 여러 애니메이션을 넣으면 동시에 재생

![](gifs/BraceAnnotation.gif)

```exercise
id: ch01-brace
title: 선분에 중괄호로 주석 달기
scene: ch01_basics.py BraceAnnotation
gif: BraceAnnotation
hint: 중괄호 클래스는 Brace이고, 중괄호에 글을 붙이는 메서드는 get_text / get_tex 입니다.
---
from manim import *


class BraceAnnotation(Scene):
    """점, 선, 중괄호(Brace)로 주석 달기. (공식 예제 BraceAnnotation)"""

    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)

        b1 = ⟦Brace⟧(line)  # 선분 아래에 중괄호
        b1text = b1.⟦get_text⟧("Horizontal distance")  # 중괄호에 글자 라벨
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.⟦get_tex⟧("x-x_1")  # 중괄호에 수식 라벨

        self.play(Create(line), FadeIn(dot, dot2))
        self.play(⟦GrowFromCenter⟧(b1), Write(b1text))  # 중괄호를 가운데서부터 키우며 등장
        self.play(GrowFromCenter(b2), Write(b2text))
        self.wait()
```

## BooleanShapes: 도형 불리언 연산

두 도형을 합치거나 빼서 새 도형을 만듭니다. 결과도 보통 도형이라 색칠하고 애니메이션할 수 있습니다.

- `Intersection(a, b)`: 겹치는 부분 (교집합)
- `Union(a, b)`: 합친 모양 (합집합)
- `Difference(a, b)`: a에서 b를 뺀 부분 (차집합)
- `Exclusion(a, b)`: 겹치는 부분만 뺀 나머지 (대칭차)
- `TransformFromCopy(a, b)`: a는 그대로 두고, a의 복사본이 b로 변하며 이동
- `arrange_in_grid(rows=2)`: 결과 네 개를 2줄 격자에 배치

![](gifs/BooleanShapes.gif)

```exercise
id: ch01-boolean
title: 두 타원으로 불리언 연산하기
scene: ch01_basics.py BooleanShapes
gif: BooleanShapes
hint: 교집합 Intersection, 합집합 Union, 대칭차 Exclusion, 차집합 Difference. 원본을 남긴 채 복사본을 변형하는 건 TransformFromCopy.
---
from manim import *


class BooleanShapes(Scene):
    """도형 불리언 연산: Union / Intersection / Difference / Exclusion."""

    def construct(self):
        a = Ellipse(width=4, height=5, fill_opacity=0.5, color=BLUE, stroke_width=8).move_to(LEFT)
        b = a.copy().set_color(RED).move_to(RIGHT)
        ab = VGroup(a, b).move_to(LEFT * 3)
        self.play(FadeIn(ab))

        ops = [
            (⟦Intersection⟧, GREEN, "Intersection"),  # 겹치는 부분
            (⟦Union⟧, ORANGE, "Union"),  # 합친 모양
            (Exclusion, YELLOW, "Exclusion"),
            (⟦Difference⟧, PINK, "Difference"),  # a에서 b를 뺀 부분
        ]
        results = VGroup()
        for op, color, name in ops:
            shape = op(a, b, color=color, fill_opacity=0.6).scale(0.3)
            label = Text(name, font_size=18).next_to(shape, DOWN, buff=0.15)
            results.add(VGroup(shape, label))
        results.⟦arrange_in_grid⟧(rows=⟦2⟧, buff=0.6).move_to(RIGHT * 3)  # 결과 네 개를 2줄 격자로 배치

        for r in results:
            self.play(⟦TransformFromCopy⟧(ab, r[0]), FadeIn(r[1]), run_time=0.8)  # 원본은 두고 복사본이 결과 도형으로 변하며 이동
        self.wait()
```

## ✍️ 직접 해보기

1. `HelloManim`에서 사각형 대신 `Star(n=7)`로 변하게 바꿔 보세요.
2. `ShapesAndLayout`에서 `arrange(RIGHT)`를 `arrange(DOWN)`으로 바꾸면 라벨이 어떻게 될까요? 라벨이 도형 오른쪽에 붙게 고쳐 보세요.
3. 원 두 개의 `Intersection`으로 렌즈 모양을 만들고, 그 위에 `Brace`로 폭을 표시해 보세요.
4. `-s` 옵션으로 마지막 프레임만 뽑아서 레이아웃을 빠르게 확인하는 습관을 들이세요.
