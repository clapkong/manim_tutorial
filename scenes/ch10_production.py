"""10장. 실제 영상 만들기: 구성 / 재사용 / 외부 소스 / 소리·자막

실행:
    uv run manim -pqh scenes/ch10_production.py Episode --save_sections
    (소리와 자막은 mp4 로 렌더할 때만 들어간다. gif 에는 없음)
"""

from pathlib import Path

from manim import *

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ── 1. 채널 스타일을 한 곳에서 정한다 ─────────────────────────────
config.background_color = "#1e1e2e"
Text.set_default(font_size=36)
MathTex.set_default(font_size=48)

ACCENT = "#f5c2e7"
SUB = "#89b4fa"


# ── 2. 반복해서 쓰는 요소는 VGroup 을 상속한 '컴포넌트'로 ──────────────
class Callout(VGroup):
    """둥근 박스 안의 설명 문구. 영상 전체에서 같은 모양을 쓰고 싶을 때."""

    def __init__(self, text: str, color=ACCENT, **kwargs):
        super().__init__(**kwargs)
        label = Text(text, font_size=28)
        box = RoundedRectangle(
            corner_radius=0.2, width=label.width + 0.6, height=label.height + 0.4,
            stroke_color=color, fill_color=color, fill_opacity=0.15,
        )
        self.add(box, label)


class ChapterTitle(VGroup):
    def __init__(self, number: int, title: str, **kwargs):
        super().__init__(**kwargs)
        num = Text(f"Part {number}", font_size=28, color=SUB)
        name = Text(title, font_size=56, weight=BOLD)
        line = Line(LEFT * 3, RIGHT * 3, color=ACCENT)
        self.add(VGroup(num, name, line).arrange(DOWN, buff=0.25))


# ── 3. 재사용 가능한 애니메이션 = Animation 을 돌려주는 함수 ───────────
def pop_in(mob, **kwargs):
    return FadeIn(mob, scale=0.6, rate_func=rate_functions.ease_out_back, **kwargs)


class Episode(Scene):
    """next_section 으로 구간을 나눈 '한 편의 영상'."""

    def construct(self):
        # ── 인트로
        self.next_section("intro")
        title = ChapterTitle(1, "피타고라스 정리")
        self.play(pop_in(title))
        self.add_subcaption("오늘은 피타고라스 정리를 봅니다.", duration=2)
        sound = ASSETS / "ding.wav"
        if sound.exists():
            self.add_sound(str(sound))
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP))

        # ── 본문: 도형
        self.next_section("figure")
        tri = Polygon(ORIGIN, RIGHT * 3, UP * 2, color=WHITE).move_to(LEFT * 2)
        a_lab = MathTex("a").next_to(tri, LEFT)
        b_lab = MathTex("b").next_to(tri, DOWN)
        c_lab = MathTex("c").move_to(tri.get_center() + UR * 0.5)
        self.play(Create(tri), Write(VGroup(a_lab, b_lab, c_lab)))
        note = Callout("직각삼각형의 세 변").next_to(tri, RIGHT, buff=1)
        self.play(pop_in(note))
        self.add_subcaption("직각삼각형의 세 변을 a, b, c 라고 합시다.", duration=2)
        self.wait(1.5)

        # ── 본문: 식
        self.next_section("formula")
        eq = MathTex("a^2", "+", "b^2", "=", "c^2").next_to(tri, RIGHT, buff=1)
        self.play(FadeOut(note, shift=UP), Write(eq))
        self.play(Circumscribe(eq, color=ACCENT))

        # TransformMatchingShapes: TeX 조각 지정 없이 '모양'이 같은 글자끼리 매칭
        swapped = MathTex("c^2 = b^2 + a^2").move_to(eq)
        self.play(TransformMatchingShapes(eq, swapped, path_arc=PI / 2))
        self.wait()

        # ── 아웃트로
        self.next_section("outro")
        self.play(*[FadeOut(m) for m in self.mobjects])
        end = Callout("구독과 좋아요", color=SUB).scale(1.5)
        self.play(pop_in(end))
        self.wait()


class ExternalAssets(Scene):
    """SVG, 비트맵 이미지, numpy 배열을 화면에 가져오기."""

    def construct(self):
        # SVG: path 하나하나가 VMobject 로 들어와서 Create/색칠이 다 된다
        svg = SVGMobject(str(ASSETS / "rocket.svg")).set_height(2.5)
        svg_label = Text("SVGMobject", font_size=24)

        # numpy 배열 → 이미지 (픽셀 단위로 직접 만든 그라데이션)
        n = 256
        arr = np.zeros((n, n, 3), dtype=np.uint8)
        arr[..., 0] = np.linspace(0, 255, n)[None, :]
        arr[..., 2] = np.linspace(255, 0, n)[:, None]
        img = ImageMobject(arr).set_height(2.5)
        img_label = Text("ImageMobject(np.array)", font_size=24)

        col1 = Group(svg, svg_label).arrange(DOWN)
        col2 = Group(img, img_label).arrange(DOWN)
        Group(col1, col2).arrange(RIGHT, buff=2)

        self.play(DrawBorderThenFill(svg), FadeIn(svg_label))
        self.play(FadeIn(img), FadeIn(img_label))
        self.play(svg.animate.set_color_by_gradient(ACCENT, SUB), img.animate.rotate(PI / 12))
        # ImageMobject("path/to/photo.png") 처럼 파일 경로도 된다
        self.wait()


class FlowField(Scene):
    """ArrowVectorField + StreamLines: 물리/미분방정식 시각화."""

    def construct(self):
        def func(p):
            x, y = p[0], p[1]
            return np.array([np.sin(y), np.sin(x), 0]) * 0.8

        field = ArrowVectorField(func, x_range=[-7, 7, 1], y_range=[-4, 4, 1])
        self.play(Create(field), run_time=1.5)
        self.wait(0.5)

        stream = StreamLines(func, stroke_width=3, max_anchors_per_line=30, padding=1, colors=[BLUE, TEAL, YELLOW])
        self.play(FadeOut(field))
        self.add(stream)
        stream.start_animation(warm_up=True, flow_speed=1.5)
        self.wait(3)
        self.play(stream.end_animation())


class LinearMap(LinearTransformationScene):
    """LinearTransformationScene: 3b1b 스타일 행렬 변환."""

    def __init__(self, **kwargs):
        super().__init__(leave_ghost_vectors=True, **kwargs)

    def construct(self):
        matrix = [[1, 1], [0, 1]]  # shear
        label = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}").to_corner(UL).add_background_rectangle()
        self.add_foreground_mobject(label)
        self.add_vector([1, 2], color=YELLOW)
        # 주의: 여기서 self.wait() 를 넣으면 라벨/ghost 가 한 번 더 변환되는 버그가 있다 (v0.21)
        self.apply_matrix(matrix)
        self.wait()
