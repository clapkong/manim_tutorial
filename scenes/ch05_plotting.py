"""5장. 좌표계와 그래프

실행:
    uv run manim -pql scenes/ch05_plotting.py SinAndCos
"""

from manim import *


class SinAndCos(Scene):
    """Axes + plot + 라벨 + 특정 점 표시. (공식 예제 SinAndCosFunctionPlot 변형)"""

    def construct(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={"numbers_to_include": np.arange(-10, 10.01, 2)},
            tips=False,
        )
        axes_labels = axes.get_axis_labels()

        sin_graph = axes.plot(np.sin, color=BLUE)
        cos_graph = axes.plot(np.cos, color=RED)
        sin_label = axes.get_graph_label(sin_graph, r"\sin(x)", x_val=-10, direction=UP / 2)
        cos_label = axes.get_graph_label(cos_graph, label=r"\cos(x)")

        vert_line = axes.get_vertical_line(axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line)
        line_label = axes.get_graph_label(cos_graph, r"x=2\pi", x_val=TAU, direction=UR, color=WHITE)

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(sin_graph), FadeIn(sin_label))
        self.play(Create(cos_graph), FadeIn(cos_label))
        self.play(Create(vert_line), Write(line_label))
        self.wait()


class RiemannToArea(Scene):
    """리만 합의 직사각형이 점점 가늘어져 넓이가 된다."""

    def construct(self):
        ax = Axes(x_range=[0, 5], y_range=[0, 6], x_length=7, y_length=5, tips=False).add_coordinates()
        curve = ax.plot(lambda x: 0.25 * (x - 1) ** 3 - 0.8 * (x - 1) + 2.5, x_range=[0, 4.5], color=YELLOW)
        self.play(Create(ax), Create(curve))

        rects = ax.get_riemann_rectangles(curve, x_range=[0.5, 4], dx=0.5, fill_opacity=0.6)
        self.play(Create(rects))
        for dx in [0.25, 0.1, 0.05]:
            new = ax.get_riemann_rectangles(curve, x_range=[0.5, 4], dx=dx, fill_opacity=0.6)
            self.play(Transform(rects, new), run_time=0.8)

        area = ax.get_area(curve, x_range=[0.5, 4], color=(BLUE, GREEN), opacity=0.6)
        integral = MathTex(r"\int_{0.5}^{4} f(x)\,dx").to_corner(UR)
        self.play(FadeTransform(rects, area), Write(integral))
        self.wait()


class ArgMin(Scene):
    """ValueTracker 로 점을 곡선 위 최솟값까지 굴린다. (공식 예제 ArgMinExample)"""

    def construct(self):
        ax = Axes(x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False})
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        t = ValueTracker(0)

        def func(x):
            return 2 * (x - 5) ** 2

        graph = ax.plot(func, color=MAROON)

        dot = Dot(point=ax.c2p(t.get_value(), func(t.get_value())))
        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))

        x_space = np.linspace(*ax.x_range[:2], 200)
        minimum_index = func(x_space).argmin()

        self.add(ax, labels, graph, dot)
        self.play(t.animate.set_value(x_space[minimum_index]), run_time=2)
        self.wait()


class DerivativeSecant(Scene):
    """할선이 접선으로: dx → 0 을 ValueTracker 로 표현."""

    def construct(self):
        ax = Axes(x_range=[0, 6], y_range=[0, 10], x_length=8, y_length=5.5, tips=False)
        graph = ax.plot(lambda x: 0.3 * x**2 + 1, color=BLUE)
        dx = ValueTracker(2.5)

        secant = always_redraw(
            lambda: ax.get_secant_slope_group(
                x=1.5, graph=graph, dx=dx.get_value(),
                dx_label="dx", dy_label="dy", secant_line_length=6, secant_line_color=RED,
            )
        )
        dx_value = always_redraw(
            lambda: MathTex(f"dx = {dx.get_value():.2f}").to_corner(UL)
        )
        self.add(ax, graph)
        self.play(Create(secant), Write(dx_value))
        self.play(dx.animate.set_value(0.01), run_time=4)
        self.wait()


class ComplexMap(Scene):
    """ComplexPlane 에 f(z) = z² 적용."""

    def construct(self):
        plane = ComplexPlane(x_range=[-3, 3], y_range=[-3, 3]).add_coordinates()
        title = MathTex("f(z) = z^2").to_corner(UL).add_background_rectangle()
        self.add(plane, title)
        self.wait(0.5)

        plane.prepare_for_nonlinear_transform()  # 곡선이 매끄럽게 휘도록 점을 늘린다
        self.play(plane.animate.apply_complex_function(lambda z: z**2 / 3), run_time=3)
        self.wait()
