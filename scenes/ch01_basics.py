"""1장. Scene과 Mobject 기본

실행:
    uv run manim -pql scenes/ch01_basics.py HelloManim
"""

from manim import *


class HelloManim(Scene):
    """가장 작은 Scene: 원 하나를 그리고 사각형으로 바꾼다."""

    def construct(self):
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=3, color=ORANGE, fill_opacity=0.5)

        self.play(Create(circle))
        self.play(Transform(circle, square))
        self.wait()


class ShapesAndLayout(Scene):
    """도형 만들기 + 배치(arrange / next_to / to_edge) + 색."""

    def construct(self):
        shapes = VGroup(
            Circle(radius=0.8, color=BLUE, fill_opacity=0.6),
            Square(side_length=1.6, color=GREEN, fill_opacity=0.6),
            Triangle(color=RED, fill_opacity=0.6).scale(1.1),
            RegularPolygon(n=6, color=YELLOW, fill_opacity=0.6),
            Star(n=5, outer_radius=0.9, color=PURPLE, fill_opacity=0.6),
        ).arrange(RIGHT, buff=0.5)  # 가로로 0.5 간격 정렬

        names = ["Circle", "Square", "Triangle", "RegularPolygon", "Star"]
        labels = VGroup(*[Text(n, font_size=20).next_to(s, DOWN) for n, s in zip(names, shapes)])

        title = Text("Mobject = 화면에 나오는 모든 것", font_size=36).to_edge(UP)

        self.play(Write(title))
        self.play(LaggedStart(*[GrowFromCenter(s) for s in shapes], lag_ratio=0.2))
        self.play(FadeIn(labels, shift=UP * 0.3))
        self.wait()

        # 그리드 배치와 그라데이션 색
        self.play(FadeOut(labels))
        self.play(shapes.animate.arrange_in_grid(rows=2, buff=0.6).set_color_by_gradient(BLUE, PINK))
        self.wait()


class BraceAnnotation(Scene):
    """점, 선, 중괄호(Brace)로 주석 달기. (공식 예제 BraceAnnotation)"""

    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)

        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")

        self.play(Create(line), FadeIn(dot, dot2))
        self.play(GrowFromCenter(b1), Write(b1text))
        self.play(GrowFromCenter(b2), Write(b2text))
        self.wait()


class BooleanShapes(Scene):
    """도형 불리언 연산: Union / Intersection / Difference / Exclusion."""

    def construct(self):
        a = Ellipse(width=4, height=5, fill_opacity=0.5, color=BLUE, stroke_width=8).move_to(LEFT)
        b = a.copy().set_color(RED).move_to(RIGHT)
        ab = VGroup(a, b).move_to(LEFT * 3)
        self.play(FadeIn(ab))

        ops = [
            (Intersection, GREEN, "Intersection"),
            (Union, ORANGE, "Union"),
            (Exclusion, YELLOW, "Exclusion"),
            (Difference, PINK, "Difference"),
        ]
        results = VGroup()
        for op, color, name in ops:
            shape = op(a, b, color=color, fill_opacity=0.6).scale(0.3)
            label = Text(name, font_size=18).next_to(shape, DOWN, buff=0.15)
            results.add(VGroup(shape, label))
        results.arrange_in_grid(rows=2, buff=0.6).move_to(RIGHT * 3)

        for r in results:
            self.play(TransformFromCopy(ab, r[0]), FadeIn(r[1]), run_time=0.8)
        self.wait()
