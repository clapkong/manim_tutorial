"""9장. 고급 프로젝트 (공식 문서 Advanced Projects)

https://docs.manim.community/en/stable/examples.html#advanced-projects

실행:
    uv run manim -pql scenes/ch09_advanced.py OpeningManim
    uv run manim -pql scenes/ch09_advanced.py SineCurveUnitCircle
    uv run manim -pql scenes/ch09_advanced.py SineCurveTracker   # 리팩터링 버전
"""

from manim import *


class OpeningManim(Scene):
    """공식 예제 그대로: Tex/MathTex → Transform → NumberPlane → 비선형 변환."""

    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()

        grid = NumberPlane()
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
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
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


class SineCurveUnitCircle(Scene):
    """공식 예제 그대로: 단위원 위의 점이 사인 곡선을 그린다.

    contributed by heejin_park, https://infograph.tistory.com/230
    """

    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"),
            MathTex(r"2 \pi"),
            MathTex(r"3 \pi"),
            MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2 * i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += dt * rate
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)


class SineCurveTracker(Scene):
    """같은 장면을 ValueTracker + Axes + TracedPath 로 다시 짠 버전.

    원본과 비교 포인트:
      - self.t_offset 을 dt 로 직접 누적 → ValueTracker 하나(θ)가 모든 걸 구동
      - Line 을 수동으로 이어 붙임 → axes.plot 으로 '지금까지의 구간'을 다시 그림
      - 좌표 하드코딩 → axes.c2p 로 수학 좌표 사용
      - 코사인 곡선까지 쉽게 추가 가능
    """

    def construct(self):
        theta = ValueTracker(0)

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

        dot = always_redraw(lambda: Dot(on_circle(), color=YELLOW))
        radius = always_redraw(lambda: Line(center, on_circle(), color=BLUE))
        angle_arc = always_redraw(
            lambda: Arc(radius=0.3, start_angle=0, angle=theta.get_value() % TAU, arc_center=center, color=BLUE)
        )
        graph_point = lambda: axes.c2p(theta.get_value(), np.sin(theta.get_value()))  # noqa: E731
        link = always_redraw(lambda: DashedLine(on_circle(), graph_point(), color=YELLOW_A, stroke_width=2))
        sine = always_redraw(
            lambda: axes.plot(np.sin, x_range=[0, max(theta.get_value(), 1e-3)], color=YELLOW_D)
        )
        label = MathTex(r"y = \sin\theta", color=YELLOW_D).to_corner(UR)

        self.add(axes, x_labels, circle)
        self.play(Write(label), run_time=0.8)
        self.add(sine, radius, angle_arc, link, dot)
        self.play(theta.animate.set_value(4 * PI), run_time=8, rate_func=linear)
        self.wait()
