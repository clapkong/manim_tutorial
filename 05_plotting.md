# 5. 좌표계와 그래프

> 예제: [`scenes/ch05_plotting.py`](scenes/ch05_plotting.py)

## 핵심: "수학 좌표"와 "화면 좌표"를 구분하기

`Axes`는 자기만의 좌표계를 가집니다. 화면에 뭔가를 그릴 때는 반드시 변환을 거치세요.

```python
ax = Axes(x_range=[0, 10, 1], y_range=[0, 100, 10], x_length=10, y_length=6)
ax.c2p(x, y)          # coords → point (수학 좌표 → 화면 좌표)  ★ 제일 많이 씀
ax.p2c(point)         # 반대 방향
ax.i2gp(x, graph)     # x에서의 그래프 위 점
```

| 메서드 (`mobject/graphing/coordinate_systems.py`) | 하는 일 |
|---|---|
| `ax.plot(func, x_range=)` | 함수 그래프 |
| `ax.plot_parametric_curve(func, t_range=)` | 매개변수 곡선 |
| `ax.get_graph_label(graph, "tex")` | 그래프 라벨 |
| `ax.get_area(graph, x_range=)` | 곡선 아래 넓이 |
| `ax.get_riemann_rectangles(graph, dx=)` | 리만 합 |
| `ax.get_secant_slope_group(x, graph, dx=)` | 할선과 dx, dy |
| `ax.get_vertical_line(point)` | 수직 점선 |
| `ax.plot_line_graph(x_values, y_values)` | 데이터 꺾은선 |

좌표계 종류: `Axes`, `NumberPlane`(격자), `PolarPlane`, `ComplexPlane`, `ThreeDAxes`, `NumberLine`

## SinAndCos (공식 예제 변형)

![](gifs/SinAndCos.gif)

## RiemannToArea: 리만 합에서 적분으로

![](gifs/RiemannToArea.gif)

`dx`를 줄인 직사각형을 새로 만들고 `Transform`으로 바꿔 끼우는 방식입니다.

## ArgMin (공식 예제)

![](gifs/ArgMin.gif)

## DerivativeSecant: 할선이 접선이 되기까지

![](gifs/DerivativeSecant.gif)

```python
dx = ValueTracker(2.5)
secant = always_redraw(lambda: ax.get_secant_slope_group(x=1.5, graph=graph, dx=dx.get_value(), ...))
self.play(dx.animate.set_value(0.01))
```

4장의 ValueTracker와 `always_redraw`를 그래프에 적용한 예입니다.

## ComplexMap: 평면 전체를 함수로 변형

![](gifs/ComplexMap.gif)

```python
plane.prepare_for_nonlinear_transform()     # 직선을 잘게 쪼개서 휘어질 수 있게
self.play(plane.animate.apply_complex_function(lambda z: z**2))
```

`apply_function(lambda p: ...)`을 쓰면 복소수가 아닌 일반 2D 변환도 됩니다 (9장 OpeningManim 참고).

## 🧩 빈칸 실습

위에서 본 예제 코드에 빈칸을 뚫었습니다. 실습 사이트(`index.html`)에서 열면 바로 채우고 채점할 수 있습니다.
GitHub에서 읽을 때는 `⟦정답⟧` 부분이 빈칸입니다.

```exercise
id: ch05-sincos
title: sin과 cos 그래프
scene: ch05_plotting.py SinAndCos
gif: SinAndCos
hint: 좌표계는 Axes, 함수 그래프는 axes.plot(함수), 라벨은 get_graph_label.
---
from manim import *


class SinAndCos(Scene):
    """Axes + plot + 라벨 + 특정 점 표시. (공식 예제 SinAndCosFunctionPlot 변형)"""

    def construct(self):
        axes = ⟦Axes⟧(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={"numbers_to_include": np.arange(-10, 10.01, 2)},
            tips=False,
        )
        axes_labels = axes.get_axis_labels()

        sin_graph = axes.⟦plot⟧(np.⟦sin⟧, color=BLUE)
        cos_graph = axes.plot(np.cos, color=RED)
        sin_label = axes.get_graph_label(sin_graph, r"\sin(x)", x_val=-10, direction=UP / 2)
        cos_label = axes.⟦get_graph_label⟧(cos_graph, label=r"\cos(x)")

        vert_line = axes.⟦get_vertical_line⟧(axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line)
        line_label = axes.get_graph_label(cos_graph, r"x=2\pi", x_val=TAU, direction=UR, color=WHITE)

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(sin_graph), FadeIn(sin_label))
        self.play(Create(cos_graph), FadeIn(cos_label))
        self.play(Create(vert_line), Write(line_label))
        self.wait()
```

```exercise
id: ch05-area
title: 리만 합에서 넓이로
scene: ch05_plotting.py RiemannToArea
gif: RiemannToArea
hint: 직사각형은 get_riemann_rectangles(graph, dx=...), 넓이는 get_area(graph, x_range=...).
---
from manim import *


class RiemannToArea(Scene):
    """리만 합의 직사각형이 점점 가늘어져 넓이가 된다."""

    def construct(self):
        ax = Axes(x_range=[0, 5], y_range=[0, 6], x_length=7, y_length=5, tips=False).add_coordinates()
        curve = ax.plot(lambda x: 0.25 * (x - 1) ** 3 - 0.8 * (x - 1) + 2.5, x_range=[0, 4.5], color=YELLOW)
        self.play(Create(ax), Create(curve))

        rects = ax.⟦get_riemann_rectangles⟧(curve, x_range=[0.5, 4], dx=0.5, fill_opacity=0.6)
        self.play(Create(rects))
        for dx in [0.25, 0.1, 0.05]:
            new = ax.get_riemann_rectangles(curve, x_range=[0.5, 4], dx=dx, fill_opacity=0.6)
            self.play(⟦Transform⟧(rects, new), run_time=0.8)

        area = ax.⟦get_area⟧(curve, x_range=[0.5, 4], color=(BLUE, GREEN), opacity=0.6)
        integral = MathTex(r"\int_{0.5}^{4} f(x)\,dx").to_corner(UR)
        self.play(⟦FadeTransform⟧(rects, area), Write(integral))
        self.wait()
```

```exercise
id: ch05-argmin
title: 최솟값까지 점 굴리기
scene: ch05_plotting.py ArgMin
gif: ArgMin
hint: 수학 좌표 → 화면 좌표 변환은 c2p(x, y). 가장 작은 값의 위치는 numpy의 argmin.
---
from manim import *


class ArgMin(Scene):
    """ValueTracker 로 점을 곡선 위 최솟값까지 굴린다. (공식 예제 ArgMinExample)"""

    def construct(self):
        ax = Axes(x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False})
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        t = ValueTracker(0)

        def func(x):
            return 2 * (x - 5) ** 2

        graph = ax.plot(func, color=MAROON)

        dot = Dot(point=ax.⟦c2p⟧(t.get_value(), func(t.get_value())))
        dot.⟦add_updater⟧(lambda x: x.⟦move_to⟧(ax.c2p(t.get_value(), func(t.get_value()))))

        x_space = np.linspace(*ax.x_range[:2], 200)
        minimum_index = func(x_space).⟦argmin⟧()

        self.add(ax, labels, graph, dot)
        self.play(t.animate.set_value(x_space[minimum_index]), run_time=2)
        self.wait()
```

```exercise
id: ch05-complex
title: 평면에 z² 적용하기
scene: ch05_plotting.py ComplexMap
gif: ComplexMap
hint: 휘어지기 전에 prepare_for_nonlinear_transform()을 호출하고, 복소함수는 apply_complex_function.
---
from manim import *


class ComplexMap(Scene):
    """ComplexPlane 에 f(z) = z² 적용."""

    def construct(self):
        plane = ⟦ComplexPlane⟧(x_range=[-3, 3], y_range=[-3, 3]).add_coordinates()
        title = MathTex("f(z) = z^2").to_corner(UL).add_background_rectangle()
        self.add(plane, title)
        self.wait(0.5)

        plane.⟦prepare_for_nonlinear_transform⟧()  # 곡선이 매끄럽게 휘도록 점을 늘린다
        self.play(plane.animate.⟦apply_complex_function⟧(lambda z: z**⟦2⟧ / 3), run_time=3)
        self.wait()
```

## ✍️ 직접 해보기

1. `SinAndCos`에 `tan(x)`를 추가해 보세요. 불연속점은 `discontinuities=[...]`와 `use_smoothing=False` 옵션으로 처리합니다.
2. `RiemannToArea`에서 `input_sample_type="right"`와 `"center"`를 비교해 보세요.
3. `ArgMin`을 경사하강법으로 바꿔 보세요. 점이 한 번에 가지 말고 `x -= lr * f'(x)` 단계마다 이동하게 만듭니다.
4. `ComplexMap`에서 `z**2` 대신 `np.exp(z)`나 `1/z`를 적용해 보세요.
