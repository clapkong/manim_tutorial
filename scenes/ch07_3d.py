"""7장. 3D

실행:
    uv run manim -pql scenes/ch07_3d.py GaussianSurface
"""

from manim import *


class GaussianSurface(ThreeDScene):
    """ThreeDAxes + Surface + 카메라 회전."""

    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[0, 2], x_length=6, y_length=6, z_length=3)

        def gauss(u, v):
            return axes.c2p(u, v, 1.6 * np.exp(-(u**2 + v**2) / 1.5))

        surface = Surface(gauss, u_range=[-3, 3], v_range=[-3, 3], resolution=(24, 24))
        surface.set_style(fill_opacity=0.8)
        surface.set_fill_by_value(axes=axes, colorscale=[(BLUE, 0), (GREEN, 0.8), (YELLOW, 1.6)], axis=2)

        # phi: 위에서 내려다보는 각, theta: 수평 회전각
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        title = Text("z = e^-(x²+y²)", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)  # 카메라가 돌아도 화면에 고정

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=20 * DEGREES, run_time=1.5)  # 위에서 보기
        self.wait(0.5)


class Solids(ThreeDScene):
    """기본 입체 도형들."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        solids = [
            Sphere(radius=0.8, resolution=(16, 16)).set_color(BLUE),
            Cube(side_length=1.3, fill_color=RED, fill_opacity=0.8),
            Cone(base_radius=0.7, height=1.5).set_color(GREEN),
            Torus(major_radius=0.7, minor_radius=0.25, resolution=(16, 16)).set_color(ORANGE),
            Dodecahedron().scale(0.6).set_color(PURPLE),
        ]
        positions = [LEFT * 4, LEFT * 2, ORIGIN, RIGHT * 2, RIGHT * 4]
        for s, p in zip(solids, positions):
            s.move_to(p)

        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in solids], lag_ratio=0.2))
        self.play(*[Rotate(s, angle=PI, axis=UP) for s in solids], run_time=2)
        self.move_camera(theta=120 * DEGREES, run_time=2)
        self.wait(0.5)
