# 3. 텍스트, 수식, 코드

> 예제: [`scenes/ch03_text_math.py`](scenes/ch03_text_math.py)

## 세 가지 텍스트 엔진

| 클래스 | 엔진 | 한글 | 용도 |
|---|---|---|---|
| `Text`, `MarkupText`, `Paragraph` | Pango (시스템 폰트) | ✅ | 제목, 설명, 자막 |
| `MathTex`, `Tex` | LaTeX | ❌ (추가 설정 필요) | 수식 |
| `Code` | Pygments 구문 강조 | ✅ | 코드 블록 |

> 수식 안에 한글을 넣고 싶으면 수식은 `MathTex`로, 한글은 `Text`로 따로 만든 뒤 `VGroup(...).arrange(RIGHT)`로 나란히 붙이는 방법이 가장 간단합니다.

## TextStyles

![](gifs/TextStyles.gif)

```python
Text("Hello", font_size=60, gradient=(BLUE, GREEN))
Text("red and blue", t2c={"red": RED, "blue": BLUE})    # 특정 단어만 색칠
MarkupText('<b>굵게</b> <span fgcolor="yellow">노랑</span>')
Text("...", font="Apple SD Gothic Neo", weight=BOLD, slant=ITALIC)
```

`Text`의 글자 하나하나가 하위 객체라서 `text[0]`, `text[3:7]`처럼 인덱싱할 수 있습니다.

## EquationSteps: 식 전개 애니메이션 ⭐

![](gifs/EquationSteps.gif)

```python
MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2")
# 인자를 나누거나 {{ }}로 감싼 부분이 각각 '조각'이 된다
self.play(TransformMatchingTex(eq1, eq2))   # 같은 TeX 문자열끼리 짝지어 날아감
```

- `TransformMatchingTex`: TeX 문자열이 같은 조각끼리 매칭합니다. 조각을 잘 나누는 게 핵심입니다.
- `TransformMatchingShapes`: 조각을 나누지 않아도 **모양이 같은 글자**끼리 매칭합니다 (10장 참고).

## ColoredFormula: 수식 일부 색칠하고 설명 달기

![](gifs/ColoredFormula.gif)

`formula.set_color_by_tex(r"e^{i\pi}", BLUE)`로 해당 조각만 색칠하고, `Brace(formula[0], UP).get_tex(...)`로 설명을 붙입니다.

## CodeTyping: 코드 블록

![](gifs/CodeTyping.gif)

```python
code = Code(code_string=src, language="python", background="window", formatter_style="monokai")
code.code_lines[i]          # i번째 줄 (하이라이트할 때)
TypeWithCursor(text, cursor)  # 타자 치는 효과
```

## 🧩 빈칸 실습

위에서 본 예제 코드에 빈칸을 뚫었습니다. 실습 사이트(`index.html`)에서 열면 바로 채우고 채점할 수 있습니다.
GitHub에서 읽을 때는 `⟦정답⟧` 부분이 빈칸입니다.

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
        t2 = Text("단어별 색칠하기: red and blue", font_size=36, ⟦t2c⟧={"red": RED, "blue": BLUE})
        t3 = ⟦MarkupText⟧('<b>굵게</b>, <i>기울임</i>, <span fgcolor="yellow">노랑</span>', font_size=36)
        t4 = Text("slant & weight", font_size=36, slant=ITALIC, weight=BOLD)
        group = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.5)

        for t in group:
            self.play(⟦Write⟧(t), run_time=1)
        self.wait()

        # 글자 하나하나도 submobject 다
        self.play(LaggedStart(*[c.animate.shift(UP * 0.3).set_color(YELLOW) for c in t1], lag_ratio=0.1))
        self.play(LaggedStart(*[c.animate.shift(⟦DOWN⟧ * 0.3) for c in t1], lag_ratio=0.1))
        self.wait(0.5)
```

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
            ⟦MathTex⟧("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2"),
            MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2"),
            MathTex("{{a}}", "=", r"\sqrt{", "{{c}}^2", "-", "{{b}}^2", "}"),
        ]
        for e in eqs:
            e.scale(1.6)

        self.play(Write(eqs[0]))
        self.wait(0.5)
        for prev, nxt in zip(eqs, eqs[1:]):
            self.play(⟦TransformMatchingTex⟧(prev, nxt, path_arc=PI / 2))
            self.wait(0.5)

        box = ⟦SurroundingRectangle⟧(eqs[-1], color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait()
```

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

        formula.⟦set_color_by_tex⟧(r"e^{i\pi}", BLUE)
        note = Text("오일러 항등식", font_size=32).next_to(formula, DOWN, buff=0.6)
        brace = Brace(formula[0], ⟦UP⟧)
        brace_label = brace.get_tex(r"\cos\pi + i\sin\pi")
        self.play(FadeIn(note, shift=UP))
        self.play(⟦GrowFromCenter⟧(brace), Write(brace_label))
        self.wait()
```

## ✍️ 직접 해보기

1. `(a+b)^2 = a^2 + 2ab + b^2` 전개 과정을 `TransformMatchingTex`로 3단계에 걸쳐 보여 주세요.
2. 같은 전개를 `TransformMatchingShapes`로 바꿔 보고, 두 방식의 차이를 비교해 보세요.
3. 여러분 프로젝트의 파이썬 파일 하나를 `Code(code_file="...")`로 불러와서 한 줄씩 하이라이트해 보세요.
4. `Text`와 `MathTex`를 섞어서 "넓이 = πr²" 같은 한글과 수식이 섞인 문장을 만들어 보세요.
