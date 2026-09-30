"""3장. 텍스트, 수식, 코드

실행:
    uv run manim -pql scenes/ch03_text_math.py EquationSteps
주의: MathTex / Tex 는 LaTeX 설치가 필요하다. (Text 는 필요 없음)
"""

from manim import *


class TextStyles(Scene):
    """Text / MarkupText 스타일링."""

    def construct(self):
        t1 = Text("Hello, Manim!", font_size=60, gradient=(BLUE, GREEN))
        t2 = Text("단어별 색칠하기: red and blue", font_size=36, t2c={"red": RED, "blue": BLUE})
        t3 = MarkupText('<b>굵게</b>, <i>기울임</i>, <span fgcolor="yellow">노랑</span>', font_size=36)
        t4 = Text("slant & weight", font_size=36, slant=ITALIC, weight=BOLD)
        group = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.5)

        for t in group:
            self.play(Write(t), run_time=1)
        self.wait()

        # 글자 하나하나도 submobject 다
        self.play(LaggedStart(*[c.animate.shift(UP * 0.3).set_color(YELLOW) for c in t1], lag_ratio=0.1))
        self.play(LaggedStart(*[c.animate.shift(DOWN * 0.3) for c in t1], lag_ratio=0.1))
        self.wait(0.5)


class EquationSteps(Scene):
    """TransformMatchingTex: 같은 기호끼리 짝지어 식을 전개한다."""

    def construct(self):
        # {{ }} 로 감싼 부분이 별도 조각이 되어 서로 매칭된다
        eqs = [
            MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2"),
            MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2"),
            MathTex("{{a}}", "=", r"\sqrt{", "{{c}}^2", "-", "{{b}}^2", "}"),
        ]
        for e in eqs:
            e.scale(1.6)

        self.play(Write(eqs[0]))
        self.wait(0.5)
        for prev, nxt in zip(eqs, eqs[1:]):
            self.play(TransformMatchingTex(prev, nxt, path_arc=PI / 2))
            self.wait(0.5)

        box = SurroundingRectangle(eqs[-1], color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait()


class ColoredFormula(Scene):
    """수식 일부만 골라서 색칠하고 설명 달기."""

    def construct(self):
        formula = MathTex(r"e^{i\pi}", "+", "1", "=", "0").scale(2)
        self.play(Write(formula))

        formula.set_color_by_tex(r"e^{i\pi}", BLUE)
        note = Text("오일러 항등식", font_size=32).next_to(formula, DOWN, buff=0.6)
        brace = Brace(formula[0], UP)
        brace_label = brace.get_tex(r"\cos\pi + i\sin\pi")
        self.play(FadeIn(note, shift=UP))
        self.play(GrowFromCenter(brace), Write(brace_label))
        self.wait()


class CodeTyping(Scene):
    """Code: 구문 강조된 코드 블록 + 한 줄씩 강조."""

    def construct(self):
        src = '''def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a'''
        code = Code(code_string=src, language="python", background="window", formatter_style="monokai")
        code.scale(1.1)
        self.play(FadeIn(code, shift=UP))

        # code.code_lines[i] 가 i번째 줄
        lines = code.code_lines
        highlight = SurroundingRectangle(lines[0], color=YELLOW, buff=0.05)
        self.play(Create(highlight))
        for line in lines[1:]:
            self.play(highlight.animate.become(SurroundingRectangle(line, color=YELLOW, buff=0.05)), run_time=0.5)
        self.wait(0.5)

        # 타자 치듯 출력하기
        out = Text(">>> fib(10)  # 55", font="Menlo", font_size=28).next_to(code, DOWN, buff=0.5)
        cursor = Rectangle(height=0.35, width=0.15, fill_opacity=1, stroke_width=0, color=WHITE)
        self.play(TypeWithCursor(out, cursor))
        self.play(Blink(cursor, blinks=2))
        self.wait(0.5)
