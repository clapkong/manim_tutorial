"""6장. 카메라 다루기

실행:
    uv run manim -pql scenes/ch06_camera.py FollowingGraphCamera
"""

from manim import *


class FollowingGraphCamera(MovingCameraScene):
    """카메라가 그래프 위를 달리는 점을 따라간다. (공식 예제)"""

    def construct(self):
        self.camera.frame.save_state()

        ax = Axes(x_range=[-1, 10], y_range=[-1, 10])
        graph = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[0, 3 * PI])

        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE)
        dot_1 = Dot(ax.i2gp(graph.t_min, graph))
        dot_2 = Dot(ax.i2gp(graph.t_max, graph))

        self.add(ax, graph, dot_1, dot_2, moving_dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear), run_time=4)
        self.camera.frame.remove_updater(update_curve)

        self.play(Restore(self.camera.frame))


class ZoomIntoDetail(MovingCameraScene):
    """프랙탈처럼 작은 디테일로 줌인했다가 빠져나오기."""

    def construct(self):
        tri = Triangle().scale(3.2)

        def sierpinski(t, depth):
            if depth == 0:
                return VGroup(t)
            v = t.get_vertices()
            subs = [Polygon(v[i], (v[i] + v[(i + 1) % 3]) / 2, (v[i] + v[(i + 2) % 3]) / 2) for i in range(3)]
            return VGroup(*[sierpinski(s, depth - 1) for s in subs])

        fractal = sierpinski(tri, 5).set_stroke(width=1).set_fill(opacity=0.8)
        fractal.set_color_by_gradient(BLUE, PURPLE, PINK)
        self.play(Create(fractal, lag_ratio=0.01), run_time=2)

        frame = self.camera.frame
        frame.save_state()
        target = tri.get_vertices()[1]
        self.play(frame.animate.scale(0.1).move_to(target + UR * 0.08), run_time=3)
        self.wait(0.5)
        self.play(Restore(frame), run_time=2)
        self.wait(0.5)


class MagnifyingGlass(ZoomedScene):
    """ZoomedScene: 화면 일부를 돋보기 창으로 보여준다."""

    def __init__(self, **kwargs):
        super().__init__(
            zoom_factor=0.25,
            zoomed_display_height=3,
            zoomed_display_width=4,
            image_frame_stroke_width=3,
            zoomed_camera_config={"default_frame_stroke_width": 3},
            **kwargs,
        )

    def construct(self):
        text = Text("tiny details are hidden here", font_size=14).move_to(LEFT * 3 + DOWN)
        dots = VGroup(*[Dot(radius=0.02, color=random_bright_color()) for _ in range(40)])
        for d in dots:
            d.move_to(LEFT * 3 + DOWN + np.random.uniform(-1, 1, 3) * [1.3, 0.6, 0])
        self.add(text, dots)

        frame = self.zoomed_camera.frame
        frame.move_to(text.get_left() + RIGHT * 0.3).set_color(YELLOW)
        self.zoomed_display.display_frame.set_color(YELLOW)
        self.zoomed_display.to_corner(UR)

        self.activate_zooming(animate=True)
        self.play(frame.animate.move_to(text.get_right() + LEFT * 0.3), run_time=3)
        self.play(frame.animate.scale(0.5), run_time=1)
        self.wait(0.5)
