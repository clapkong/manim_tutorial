"""2장. 애니메이션

실행:
    uv run manim -pql scenes/ch02_animations.py BasicAnimations
"""

from manim import *


class BasicAnimations(Scene):
    """등장 / 변형 / 퇴장 애니메이션 한 바퀴."""

    def construct(self):
        sq = Square(color=BLUE, fill_opacity=0.5)
        circ = Circle(color=RED, fill_opacity=0.5)
        tri = Triangle(color=GREEN, fill_opacity=0.5).scale(1.3)
        caption = Text("", font_size=28).to_edge(DOWN)

        def say(msg):
            return Transform(caption, Text(msg, font_size=28).to_edge(DOWN))

        self.add(caption)
        self.play(Create(sq), say("Create"))
        self.play(Transform(sq, circ), say("Transform(sq, circ)"))
        # ReplacementTransform: 이후로는 tri 변수로 다룬다
        self.play(ReplacementTransform(sq, tri), say("ReplacementTransform"))
        self.play(Indicate(tri), say("Indicate"))
        self.play(FadeOut(tri, shift=DOWN), say("FadeOut(shift=DOWN)"))
        self.wait(0.5)


class AnimateSyntax(Scene):
    """`.animate` : 메서드 호출을 그대로 애니메이션으로."""

    def construct(self):
        sq = Square(color=BLUE, fill_opacity=0.7)
        self.add(sq)

        self.play(sq.animate.shift(LEFT * 3))
        self.play(sq.animate.rotate(PI / 4).set_color(YELLOW))  # 체이닝 가능
        self.play(sq.animate.scale(0.5).to_corner(UR))
        self.play(sq.animate(run_time=2, rate_func=there_and_back).move_to(ORIGIN))

        # 상태 저장 / 복원
        sq.save_state()
        self.play(sq.animate.scale(3).set_opacity(0.2))
        self.play(Restore(sq))
        self.wait(0.5)


class RateFunctions(Scene):
    """rate_func: 같은 이동이라도 '느낌'을 바꾸는 이징 함수."""

    def construct(self):
        rf = rate_functions
        funcs = [linear, smooth, rush_into, rush_from, there_and_back, rf.ease_out_bounce, rf.ease_in_out_back]
        rows = VGroup()
        for f in funcs:
            label = Text(f.__name__, font_size=22).set_width(2.4)
            dot = Dot(color=YELLOW)
            track = Line(LEFT * 3, RIGHT * 3, stroke_opacity=0.3)
            dot.move_to(track.get_start())
            rows.add(VGroup(label, track, dot))
        for r in rows:
            r[0].next_to(r[1], LEFT, buff=0.4)
        rows.arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.add(rows)

        self.play(
            *[r[2].animate(rate_func=f).move_to(r[1].get_end()) for r, f in zip(rows, funcs)],
            run_time=3,
        )
        self.wait(0.5)


class Composition(Scene):
    """AnimationGroup / LaggedStart / Succession 비교."""

    def construct(self):
        def make_row(y):
            return VGroup(*[Square(0.6, fill_opacity=0.8) for _ in range(6)]).arrange(RIGHT).shift(y * UP)

        rows = [make_row(2), make_row(0), make_row(-2)]
        rows[0].set_color(BLUE)
        rows[1].set_color(GREEN)
        rows[2].set_color(RED)
        labels = VGroup(
            Text("AnimationGroup", font_size=22),
            Text("LaggedStart", font_size=22),
            Text("Succession", font_size=22),
        )
        for lab, row in zip(labels, rows):
            lab.next_to(row, UP, buff=0.15)
        self.add(labels)

        self.play(AnimationGroup(*[GrowFromCenter(s) for s in rows[0]]))  # 동시에
        self.play(LaggedStart(*[GrowFromCenter(s) for s in rows[1]], lag_ratio=0.3))  # 겹치며 순차
        self.play(Succession(*[GrowFromCenter(s) for s in rows[2]]), run_time=2)  # 완전 순차
        self.wait(0.5)


class Emphasis(Scene):
    """강조 애니메이션 모음."""

    def construct(self):
        items = VGroup(*[Text(t, font_size=36) for t in ["Indicate", "Circumscribe", "Flash", "Wiggle", "ApplyWave"]])
        items.arrange(DOWN, buff=0.5)
        self.add(items)

        self.play(Indicate(items[0]))
        self.play(Circumscribe(items[1]))
        self.play(Flash(items[2].get_right() + RIGHT * 0.3, color=YELLOW))
        self.play(Wiggle(items[3]))
        self.play(ApplyWave(items[4]))
        self.wait(0.5)
