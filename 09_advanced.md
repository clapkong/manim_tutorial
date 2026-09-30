# 9. 고급 프로젝트 (공식 예제)

> 예제: [`scenes/ch09_advanced.py`](scenes/ch09_advanced.py)
> 원본: https://docs.manim.community/en/stable/examples.html#advanced-projects

공식 갤러리의 Advanced Projects에 있는 두 예제입니다. 1~5장에서 배운 것이 모두 들어 있습니다.

## OpeningManim

![](gifs/OpeningManim.gif)

```bash
uv run manim -pql scenes/ch09_advanced.py OpeningManim
```

**여기서 볼 것**

| 코드 | 배운 곳 |
|---|---|
| `VGroup(title, basel).arrange(DOWN)` | 1장: 배치 |
| `Write`, `FadeIn(shift=DOWN)`을 한 `play`에 | 2장: 동시 재생 |
| `LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel])` | 2장: 수식 **조각별로** 차례로 퇴장 |
| `Create(grid, run_time=3, lag_ratio=0.1)` | 2장: `lag_ratio`로 격자선이 차례로 그려짐 |
| `self.add(grid, grid_title)` 순서 | **나중에 add한 것이 위에 그려짐** (z-order) |
| `grid.prepare_for_nonlinear_transform()` + `apply_function` | 5장: 비선형 변환 |

## SineCurveUnitCircle

![](gifs/SineCurveUnitCircle.gif)

```bash
uv run manim -pql scenes/ch09_advanced.py SineCurveUnitCircle
```

한국 개발자(heejin_park)가 기여한 예제입니다. 단위원 위의 점이 돌면서 사인 곡선을 그립니다.

**구조**
1. `dot.add_updater(go_around_circle)`: `dt` updater로 점이 원을 돕니다 (`self.t_offset`을 누적).
2. `always_redraw(get_line_to_circle)`: 중심에서 점까지 반지름 선
3. `always_redraw(get_line_to_curve)`: 점에서 곡선 끝까지 수평선
4. `always_redraw(get_curve)`: 매 프레임 짧은 `Line`을 하나씩 **이어 붙여** 곡선을 그립니다.

## 리팩터링: SineCurveTracker

![](gifs/SineCurveTracker.gif)

원본은 잘 동작하지만 4장과 5장의 도구를 쓰면 더 깔끔하게 만들 수 있습니다.

| | 원본 | 리팩터링 |
|---|---|---|
| 시간 | `self.t_offset += dt * rate` (Scene 속성을 직접 누적) | `theta = ValueTracker(0)` 하나 |
| 재생 | `self.wait(8.5)` 후 updater 제거 | `self.play(theta.animate.set_value(4*PI), rate_func=linear)` |
| 곡선 | `Line`을 매 프레임 **추가** (프레임 수만큼 객체가 쌓임) | `axes.plot(np.sin, x_range=[0, θ])`로 매 프레임 다시 그림 |
| 좌표 | `np.array([-4,0,0])` 하드코딩 | `axes.c2p(θ, sin θ)` |
| 확장 | 코사인 추가가 번거로움 | `axes.plot(np.cos, ...)` 한 줄 |

ValueTracker 방식의 장점은 **시간을 자유롭게 다룰 수 있다**는 것입니다. `theta.animate.set_value(PI)`로 멈추거나 되감을 수 있고, `rate_func`도 바꿀 수 있습니다. dt 방식에서는 이런 제어가 어렵습니다.

## 🧩 빈칸 실습

위에서 본 예제 코드에 빈칸을 뚫었습니다. 실습 사이트(`index.html`)에서 열면 바로 채우고 채점할 수 있습니다.
GitHub에서 읽을 때는 `⟦정답⟧` 부분이 빈칸입니다.

```exercise
id: ch09-opening
title: OpeningManim 완성하기
scene: ch09_advanced.py OpeningManim
gif: OpeningManim
hint: 수식을 조각별로 차례로 내보낼 땐 LaggedStart, 격자는 NumberPlane, 비선형 변환 전엔 prepare_for_nonlinear_transform.
---
from manim import *


class OpeningManim(Scene):
    """공식 예제 그대로: Tex/MathTex → Transform → NumberPlane → 비선형 변환."""

    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).⟦arrange⟧(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            ⟦LaggedStart⟧(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()

        grid = ⟦NumberPlane⟧()
        grid_title = Tex("This is a grid", font_size=72)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(r"That was a non-linear function \\ applied to the grid")
        grid_transform_title.move_to(grid_title, UL)
        grid.⟦prepare_for_nonlinear_transform⟧()
        self.play(
            grid.animate.⟦apply_function⟧(
                lambda p: p
                + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()
```

```exercise
id: ch09-sine
title: SineCurveTracker 완성하기
scene: ch09_advanced.py SineCurveTracker
gif: SineCurveTracker
hint: 모든 움직임은 theta 하나가 구동합니다. 그래프 좌표는 axes.c2p, 일정한 속도는 rate_func=linear.
---
from manim import *


class SineCurveTracker(Scene):
    """같은 장면을 ValueTracker + Axes + TracedPath 로 다시 짠 버전.

    원본과 비교 포인트:
      - self.t_offset 을 dt 로 직접 누적 → ValueTracker 하나(θ)가 모든 걸 구동
      - Line 을 수동으로 이어 붙임 → axes.plot 으로 '지금까지의 구간'을 다시 그림
      - 좌표 하드코딩 → axes.c2p 로 수학 좌표 사용
      - 코사인 곡선까지 쉽게 추가 가능
    """

    def construct(self):
        theta = ⟦ValueTracker⟧(0)

        axes = Axes(
            x_range=[0, 4 * PI, PI], y_range=[-1.5, 1.5, 1],
            x_length=8, y_length=3, tips=False,
        ).shift(RIGHT * 1.8)
        x_labels = VGroup(
            *[MathTex(tex).scale(0.8).next_to(axes.c2p(k * PI, 0), DOWN) for k, tex in
              [(1, r"\pi"), (2, r"2\pi"), (3, r"3\pi"), (4, r"4\pi")]]
        )
        unit = axes.get_y_unit_size()  # 원의 반지름을 그래프 y축 1 과 맞춘다
        circle = Circle(radius=unit, color=WHITE).move_to(axes.get_origin() + LEFT * (unit + 1.2))
        center = circle.get_center()

        def on_circle():
            a = theta.get_value()
            return center + unit * np.array([np.cos(a), np.sin(a), 0])

        dot = ⟦always_redraw⟧(lambda: Dot(on_circle(), color=YELLOW))
        radius = always_redraw(lambda: Line(center, on_circle(), color=BLUE))
        angle_arc = always_redraw(
            lambda: Arc(radius=0.3, start_angle=0, angle=theta.get_value() % TAU, arc_center=center, color=BLUE)
        )
        graph_point = lambda: axes.⟦c2p⟧(theta.get_value(), np.sin(theta.get_value()))  # noqa: E731
        link = always_redraw(lambda: DashedLine(on_circle(), graph_point(), color=YELLOW_A, stroke_width=2))
        sine = always_redraw(
            lambda: axes.plot(np.sin, x_range=[0, max(theta.get_value(), 1e-3)], color=YELLOW_D)
        )
        label = MathTex(r"y = \sin\theta", color=YELLOW_D).to_corner(UR)

        self.add(axes, x_labels, circle)
        self.play(Write(label), run_time=0.8)
        self.add(sine, radius, angle_arc, link, dot)
        self.play(theta.animate.set_value(⟦4 * PI|4*PI⟧), run_time=8, rate_func=⟦linear⟧)
        self.wait()
```

## ✍️ 직접 해보기

1. `SineCurveTracker`에 코사인 곡선(파란색)을 추가하고, 원 위의 점에서 수직선도 그려 보세요.
2. `OpeningManim`의 비선형 함수를 `p + [sin(p[1]), 0, 0]`(한 방향만)으로 바꾸면 어떻게 되는지 보세요.
3. **종합 과제**: 원 대신 정사각형 둘레를 도는 점으로 바꿔서 "정사각형 사인파"를 그려 보세요. (힌트: `square.point_from_proportion(t)`)
