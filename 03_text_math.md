# 3. 텍스트, 수식, 코드

예제 원본: [`scenes/ch03_text_math.py`](scenes/ch03_text_math.py)

## 세 가지 텍스트 엔진

Manim에서 글자를 만드는 방법은 세 가지이고, 엔진이 달라서 할 수 있는 일도 다릅니다. 한글은 `Text` 계열로만 바로 쓸 수 있습니다.

| 클래스 | 엔진 | 한글 | 용도 |
|---|---|---|---|
| `Text`, `MarkupText`, `Paragraph` | Pango (시스템 폰트) | ✅ | 제목, 설명, 자막 |
| `MathTex`, `Tex` | LaTeX | ❌ (추가 설정 필요) | 수식 |
| `Code` | Pygments 구문 강조 | ✅ | 코드 블록 |

- 수식과 한글을 섞을 때: 수식은 `MathTex`, 한글은 `Text`로 따로 만든 뒤 `VGroup(...).arrange(RIGHT)`로 나란히 붙임

## TextStyles: 텍스트 꾸미기

`Text`는 시스템 폰트로 글자를 그리고, 크기, 색, 굵기 같은 스타일을 인자로 받습니다. `Text`의 글자 하나하나가 하위 객체라서 `for c in text:`로 돌면서 글자마다 따로 애니메이션을 줄 수도 있습니다.

- `Text("...", font_size=, gradient=(색1, 색2))`: 크기와 그라데이션
- `t2c={"단어": 색}`: 특정 단어만 색칠
  - t2c는 "text to color"의 줄임말
- `MarkupText('<b>굵게</b> <i>기울임</i> <span fgcolor="yellow">노랑</span>')`: 태그로 꾸미기
- `slant=ITALIC`, `weight=BOLD`: 기울임, 굵기
- `Write(mob)`: 글자를 쓰듯 등장
- `c.animate.shift(UP * 0.3)`: 글자 하나를 위로 이동
  - 위로 올렸다가 `DOWN`으로 다시 내리면 파도처럼 보임

![](gifs/TextStyles.gif)

```exercise
id: ch03-text
title: 텍스트 꾸미기
scene: ch03_text_math.py TextStyles
gif: TextStyles
hint: 단어별 색은 t2c(text to color) 딕셔너리, 태그로 꾸미는 텍스트는 MarkupText 입니다.
---
from manim import *


class TextStyles(Scene):
    """Text / MarkupText 스타일링."""

    def construct(self):
        t1 = Text("Hello, Manim!", font_size=60, gradient=(BLUE, GREEN))
        t2 = Text("단어별 색칠하기: red and blue", font_size=36, ⟦t2c⟧={"red": RED, "blue": BLUE})  # 단어별로 색칠
        t3 = ⟦MarkupText⟧('<b>굵게</b>, <i>기울임</i>, <span fgcolor="yellow">노랑</span>', font_size=36)  # 태그로 굵게, 기울임, 색 지정
        t4 = Text("slant & weight", font_size=36, slant=ITALIC, weight=BOLD)
        group = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.5)

        for t in group:
            self.play(⟦Write⟧(t), run_time=1)  # 글자를 쓰듯 등장
        self.wait()

        # 글자 하나하나도 submobject 다
        self.play(LaggedStart(*[c.animate.shift(UP * 0.3).set_color(YELLOW) for c in t1], lag_ratio=0.1))
        self.play(LaggedStart(*[c.animate.shift(⟦DOWN⟧ * 0.3) for c in t1], lag_ratio=0.1))  # 올렸던 글자를 다시 내리기
        self.wait(0.5)
```

## EquationSteps: 식 전개 애니메이션 ⭐

수식은 LaTeX 문법 그대로 `MathTex`에 씁니다. 식을 한 단계씩 전개하려면 식을 조각으로 나눠 두고, 다음 식에서 같은 조각끼리 짝을 지어 이동시킵니다. 짝이 없는 조각은 사라지거나 새로 나타납니다.

- `MathTex(r"...")`: 수식 생성
  - `^2`는 제곱, `\sqrt{}`는 루트
- `MathTex("a^2", "+", "b^2")`: 인자를 나누면 각각 조각이 됨
- `{{a}}`: 문자열 안에서 두 겹 중괄호로 감싼 부분도 따로 조각이 됨
- `TransformMatchingTex(이전식, 다음식)`: TeX 문자열이 같은 조각끼리 짝지어 변형
  - `path_arc=PI / 2`를 주면 조각들이 곡선을 그리며 이동
- `SurroundingRectangle(mob, color=, buff=)`: 객체에 네모 테두리

![](gifs/EquationSteps.gif)

```exercise
id: ch03-eq
title: 피타고라스 식 전개하기
scene: ch03_text_math.py EquationSteps
gif: EquationSteps
hint: 같은 TeX 조각끼리 짝지어 변형하는 애니메이션은 TransformMatchingTex 입니다. 조각은 {{ }}로 감쌉니다.
---
from manim import *


class EquationSteps(Scene):
    """TransformMatchingTex: 같은 기호끼리 짝지어 식을 전개한다."""

    def construct(self):
        # {{ }} 로 감싼 부분이 별도 조각이 되어 서로 매칭된다
        eqs = [
            ⟦MathTex⟧("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2"),  # 수식을 조각으로 나눠 생성
            MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2"),
            MathTex("{{a}}", "=", r"\sqrt{", "{{c}}^2", "-", "{{b}}^2", "}"),
        ]
        for e in eqs:
            e.scale(1.6)

        self.play(Write(eqs[0]))
        self.wait(0.5)
        for prev, nxt in zip(eqs, eqs[1:]):
            self.play(⟦TransformMatchingTex⟧(prev, nxt, path_arc=PI / 2))  # 같은 조각끼리 짝지어 다음 식으로 변형
            self.wait(0.5)

        box = ⟦SurroundingRectangle⟧(eqs[-1], color=YELLOW, buff=0.2)  # 마지막 식에 네모 테두리
        self.play(Create(box))
        self.wait()
```

## ColoredFormula: 수식 일부만 색칠하고 설명 달기

수식을 조각으로 나눠 두면 조각 단위로 색칠하거나 설명을 붙일 수 있습니다. 조각은 TeX 문자열로 찾을 수도 있고, 번호로 꺼낼 수도 있습니다.

- `formula.set_color_by_tex(조각문자열, 색)`: 해당 조각을 찾아 색칠
- `formula[i]`: i번째 조각
  - 예: `MathTex(r"e^{i\pi}", "+", "1")`이면 `formula[0]`이 `e^{i\pi}`
- `Brace(대상, 방향)`: 조각에 중괄호
  - 위쪽은 `UP`
- `brace.get_tex(...)`: 중괄호에 설명 수식
- `GrowFromCenter(brace)`: 중괄호 등장

![](gifs/ColoredFormula.gif)

```exercise
id: ch03-color
title: 수식 일부 색칠하고 설명 붙이기
scene: ch03_text_math.py ColoredFormula
gif: ColoredFormula
hint: set_color_by_tex(조각, 색). 중괄호는 Brace(대상, 방향).
---
from manim import *


class ColoredFormula(Scene):
    """수식 일부만 골라서 색칠하고 설명 달기."""

    def construct(self):
        formula = MathTex(r"e^{i\pi}", "+", "1", "=", "0").scale(2)
        self.play(Write(formula))

        formula.⟦set_color_by_tex⟧(r"e^{i\pi}", BLUE)  # e^{iπ} 조각만 파랗게
        note = Text("오일러 항등식", font_size=32).next_to(formula, DOWN, buff=0.6)
        brace = Brace(formula[0], ⟦UP⟧)  # 첫 조각 위쪽에 중괄호
        brace_label = brace.get_tex(r"\cos\pi + i\sin\pi")
        self.play(FadeIn(note, shift=UP))
        self.play(⟦GrowFromCenter⟧(brace), Write(brace_label))  # 중괄호를 가운데서부터 키우며 등장
        self.wait()
```

## CodeTyping: 코드 블록

코드 설명 영상을 위한 예제입니다. `Code`는 문법 강조가 된 코드 블록을 만들고, 줄 단위로 꺼낼 수 있어서 한 줄씩 짚으며 설명할 수 있습니다. 마지막에는 실행 결과를 타자 치듯 출력합니다.

- `Code(code_string=, language="python", background="window", formatter_style="monokai")`: 코드 블록 생성
  - 파일은 `code_file="경로"`로 불러옴
- `code.code_lines`: 줄 목록
  - `code.code_lines[0]`이 첫 줄
- `box.animate.become(새박스)`: 박스를 새 박스 모양으로 통째로 바꿈
  - 하이라이트를 다음 줄로 옮길 때 사용
- `TypeWithCursor(텍스트, 커서)`: 커서와 함께 타자 치듯 출력
  - 커서는 작은 `Rectangle`
- `Blink(mob, blinks=횟수)`: 깜빡임

![](gifs/CodeTyping.gif)

```exercise
id: ch03-code
title: 코드 블록을 한 줄씩 짚기
scene: ch03_text_math.py CodeTyping
gif: CodeTyping
hint: Code(code_string=..., language=...). 줄 목록은 code.code_lines. 박스를 새 위치로 바꿀 땐 become. 타자 효과는 TypeWithCursor.
---
from manim import *


class CodeTyping(Scene):
    """Code: 구문 강조된 코드 블록 + 한 줄씩 강조."""

    def construct(self):
        src = '''def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a'''
        code = ⟦Code⟧(code_string=src, language="⟦python⟧", background="window", formatter_style="monokai")  # 문법 강조된 코드 블록 (파이썬)
        code.scale(1.1)
        self.play(FadeIn(code, shift=UP))

        # code.code_lines[i] 가 i번째 줄
        lines = code.⟦code_lines⟧  # 코드의 줄 목록
        highlight = SurroundingRectangle(lines[0], color=YELLOW, buff=0.05)
        self.play(Create(highlight))
        for line in lines[1:]:
            self.play(highlight.animate.⟦become⟧(SurroundingRectangle(line, color=YELLOW, buff=0.05)), run_time=0.5)  # 하이라이트 박스를 다음 줄 박스 모양으로 바꾸기
        self.wait(0.5)

        # 타자 치듯 출력하기
        out = Text(">>> fib(10)  # 55", font="Menlo", font_size=28).next_to(code, DOWN, buff=0.5)
        cursor = Rectangle(height=0.35, width=0.15, fill_opacity=1, stroke_width=0, color=WHITE)
        self.play(⟦TypeWithCursor⟧(out, cursor))  # 커서와 함께 타자 치듯 출력
        self.play(⟦Blink⟧(cursor, blinks=2))  # 커서 두 번 깜빡이기
        self.wait(0.5)
```

## ✍️ 직접 해보기

1. `(a+b)^2 = a^2 + 2ab + b^2` 전개 과정을 `TransformMatchingTex`로 3단계에 걸쳐 보여 주세요.
2. 같은 전개를 `TransformMatchingShapes`로 바꿔 보고, 두 방식의 차이를 비교해 보세요.
3. 여러분 프로젝트의 파이썬 파일 하나를 `Code(code_file="...")`로 불러와서 한 줄씩 하이라이트해 보세요.
4. `Text`와 `MathTex`를 섞어서 "넓이 = πr²" 같은 한글과 수식이 섞인 문장을 만들어 보세요.
