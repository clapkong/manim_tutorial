"""4장. Updater와 ValueTracker: '살아 움직이는' 객체

실행:
    uv run manim -pql scenes/ch04_updaters.py ValueTrackerBasics
"""

from manim import *


class ValueTrackerBasics(Scene):
    """ValueTracker 하나로 여러 객체를 동시에 구동한다."""

    def construct(self):
        t = ValueTracker(1)  # 화면에 안 보이는 '숫자 변수'

        line = NumberLine(x_range=[0, 3, 0.5], length=8, include_numbers=True).to_edge(DOWN, buff=1)
        pointer = Triangle(color=YELLOW, fill_opacity=1).scale(0.15).rotate(PI)
        label = DecimalNumber(num_decimal_places=2, font_size=36)

        # add_updater: 매 프레임마다 tracker 값을 읽어 자기 자신을 갱신
        pointer.add_updater(lambda m: m.next_to(line.n2p(t.get_value()), UP, buff=0.1))
        label.add_updater(lambda m: m.set_value(t.get_value()).next_to(pointer, UP))

        # always_redraw: 매 프레임 객체를 '새로 만든다' (모양 자체가 바뀔 때 편함)
        circle = always_redraw(
            lambda: Circle(radius=t.get_value(), color=BLUE, fill_opacity=0.3).shift(UP)
        )
        r_text = always_redraw(
            lambda: MathTex(f"r = {t.get_value():.2f}").next_to(circle, RIGHT)
        )

        self.add(line, pointer, label, circle, r_text)
        self.play(t.animate.set_value(2.5), run_time=2)
        self.play(t.animate.set_value(0.5), run_time=2)
        self.play(t.animate.set_value(1.5), run_time=1, rate_func=there_and_back)
        self.wait(0.5)


class MovingAngle(Scene):
    """각도가 변하면 Angle 호와 θ 라벨이 따라온다. (공식 예제 MovingAngle)"""

    def construct(self):
        rotation_center = LEFT
        theta_tracker = ValueTracker(110)

        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(theta_tracker.get_value() * DEGREES, about_point=rotation_center)

        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        self.add(line1, line_moving, a, tex)

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )
        a.add_updater(lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False)))
        tex.add_updater(
            lambda x: x.move_to(
                Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))
        self.wait(0.5)


class DtUpdater(Scene):
    """dt 를 받는 updater: 애니메이션 없이 wait() 동안에도 계속 움직인다."""

    def construct(self):
        square = Square(color=TEAL, fill_opacity=0.5)
        # (mobject, dt) 시그니처면 시간 기반 updater 가 된다 (dt = 프레임 간 시간)
        square.add_updater(lambda m, dt: m.rotate(dt * PI / 2))
        self.add(square)
        self.wait(2)

        # 도중에 updater 를 떼면 멈춘다
        square.clear_updaters()
        self.play(square.animate.set_color(RED))
        self.wait(0.5)


class Epicycles(Scene):
    """회전하는 벡터 두 개 + TracedPath = 미니 푸리에 에피사이클."""

    def construct(self):
        t = ValueTracker(0)
        center = LEFT * 1.5
        r1, w1 = 1.6, 1  # 반지름, 각속도
        r2, w2 = 0.6, -3

        def tip1():
            return center + r1 * np.array([np.cos(w1 * t.get_value()), np.sin(w1 * t.get_value()), 0])

        def tip2():
            return tip1() + r2 * np.array([np.cos(w2 * t.get_value()), np.sin(w2 * t.get_value()), 0])

        circle1 = Circle(radius=r1, stroke_opacity=0.3).move_to(center)
        circle2 = always_redraw(lambda: Circle(radius=r2, stroke_opacity=0.3).move_to(tip1()))
        vec1 = always_redraw(lambda: Arrow(center, tip1(), buff=0, color=BLUE))
        vec2 = always_redraw(lambda: Arrow(tip1(), tip2(), buff=0, color=GREEN))
        pen = always_redraw(lambda: Dot(tip2(), color=YELLOW, radius=0.05))
        trace = TracedPath(pen.get_center, stroke_color=YELLOW, stroke_width=3)

        self.add(circle1, circle2, vec1, vec2, trace, pen)
        self.play(t.animate.set_value(TAU), run_time=6, rate_func=linear)
        self.wait(0.5)
