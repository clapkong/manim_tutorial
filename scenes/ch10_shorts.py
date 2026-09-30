"""10장 보너스. 세로 영상(쇼츠 / 릴스, 9:16)

실행:
    uv run manim -pqh scenes/ch10_shorts.py VerticalShort

config 는 파일 맨 위에서 바꾸면 이 파일의 모든 Scene 에 적용된다.
CLI 로만 바꾸고 싶으면: manim -r 1080,1920 ...  (단, 이 경우 frame_width 는 따로 안 바뀐다)
"""

from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9  # 화면 좌표계 폭. 높이는 비율에 맞게 16 이 된다
config.frame_height = 16
config.background_color = "#101014"


class VerticalShort(Scene):
    def construct(self):
        hook = Text("1 + 2 + 3 + ... = ?", font_size=64).to_edge(UP, buff=1.5)
        self.play(Write(hook))

        dots = VGroup()
        for row in range(1, 7):
            dots.add(VGroup(*[Dot(radius=0.18, color=BLUE) for _ in range(row)]).arrange(RIGHT, buff=0.15))
        dots.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT) for r in dots], lag_ratio=0.2))

        # 180° 돌린 복사본을 맞물리면 n × (n+1) 직사각형이 된다
        step = dots[0][0].width + 0.15  # 점 하나 + 간격
        copy = dots.copy().set_color(ORANGE).rotate(PI)
        copy.align_to(dots, UP).align_to(dots, RIGHT).shift(RIGHT * step)
        self.play(TransformFromCopy(dots, copy, path_arc=PI / 2), run_time=1.5)
        self.play(VGroup(dots, copy).animate.move_to(ORIGIN))

        answer = MathTex(r"\frac{n(n+1)}{2}", font_size=96).to_edge(DOWN, buff=2)
        self.play(Write(answer))
        self.play(Circumscribe(answer, color=YELLOW))
        self.wait()
