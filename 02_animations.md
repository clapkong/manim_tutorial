# 2. 애니메이션

> 예제: [`scenes/ch02_animations.py`](scenes/ch02_animations.py)

## 핵심 개념

- `self.play(anim1, anim2, ...)`: 인자로 준 애니메이션이 **동시에** 재생됩니다.
- 공통 인자: `run_time=초`, `rate_func=함수`, `lag_ratio=`(하위 객체들 사이의 시간차)
- `self.add(mob)`: 애니메이션 없이 바로 화면에 올립니다. `self.remove(mob)`: 바로 지웁니다.
- `self.wait(초)`: 멈춰 있기. updater(4장)는 이 동안에도 계속 돌아갑니다.

## BasicAnimations: 등장 → 변형 → 퇴장

![](gifs/BasicAnimations.gif)

| 분류 | 애니메이션 (`animation/`) |
|---|---|
| 등장 | `Create`, `Write`, `DrawBorderThenFill`, `FadeIn(shift=, scale=)`, `GrowFromCenter`, `GrowArrow`, `SpinInFromNothing` |
| 퇴장 | `Uncreate`, `Unwrite`, `FadeOut`, `ShrinkToCenter` |
| 변형 | `Transform`, `ReplacementTransform`, `TransformFromCopy`, `FadeTransform`, `Swap`, `CyclicReplace` |
| 이동 | `MoveAlongPath`, `Rotate`, `Rotating` |

> **`Transform` vs `ReplacementTransform`**
> `Transform(a, b)` 뒤에는 화면에 있는 객체가 여전히 **`a`**입니다 (모양만 b가 됨). 이후 코드에서 `a`로 다뤄야 합니다.
> `ReplacementTransform(a, b)` 뒤에는 `a`가 빠지고 **`b`**가 화면에 남습니다. 헷갈리면 `ReplacementTransform`을 쓰세요.

## AnimateSyntax: `.animate`

![](gifs/AnimateSyntax.gif)

```python
self.play(sq.animate.shift(LEFT * 3))
self.play(sq.animate.rotate(PI / 4).set_color(YELLOW))       # 체이닝
self.play(sq.animate(run_time=2, rate_func=there_and_back).move_to(ORIGIN))

sq.save_state()                     # 현재 상태 저장
self.play(sq.animate.scale(3))
self.play(Restore(sq))              # 저장한 상태로 복귀
```

`.animate`는 **시작 상태와 끝 상태를 보간**합니다. 그래서 `rotate(PI)`처럼 시작과 끝 모양이 같으면 돌아가는 모습이 보이지 않습니다. 회전 과정을 보여 주려면 `Rotate(mob, PI)`를 쓰세요.

## RateFunctions: 움직임의 "느낌"

![](gifs/RateFunctions.gif)

`utils/rate_functions.py`에 49개가 있습니다. 자주 쓰는 것:
`smooth`(기본값), `linear`(일정한 속도, 회전이나 흐름에 적합), `there_and_back`(갔다 돌아옴), `rush_into`, `rush_from`, `rate_functions.ease_out_bounce`, `rate_functions.ease_in_out_back`.

> `ease_*` 계열은 `from manim import *`로 바로 불러와지지 않습니다. `rate_functions.ease_out_bounce`처럼 모듈 이름을 붙여서 쓰세요.

## Composition: 애니메이션 조합

![](gifs/Composition.gif)

| | 동작 |
|---|---|
| `AnimationGroup(*anims)` | 동시에 |
| `LaggedStart(*anims, lag_ratio=0.3)` | 조금씩 겹치며 차례로 (가장 많이 씀) |
| `Succession(*anims)` | 하나 끝나면 다음 |
| `LaggedStartMap(FadeIn, group)` | 그룹의 각 원소에 같은 애니메이션을 적용 |

## Emphasis: 강조

![](gifs/Emphasis.gif)

`Indicate`, `Circumscribe`, `Flash`, `Wiggle`, `ApplyWave`, `FocusOn`, `ShowPassingFlash`, `Blink`

## 🧩 빈칸 실습

위에서 본 예제 코드에 빈칸을 뚫었습니다. 실습 사이트(`index.html`)에서 열면 바로 채우고 채점할 수 있습니다.
GitHub에서 읽을 때는 `⟦정답⟧` 부분이 빈칸입니다.

```exercise
id: ch02-basic
title: 등장 → 변형 → 강조 → 퇴장
scene: ch02_animations.py BasicAnimations
gif: BasicAnimations
hint: ReplacementTransform 뒤에는 tri를 다룹니다. 퇴장 방향은 shift= 인자로 줍니다.
---
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
        self.play(⟦Create⟧(sq), say("Create"))
        self.play(⟦Transform⟧(sq, circ), say("Transform(sq, circ)"))
        # ReplacementTransform: 이후로는 tri 변수로 다룬다
        self.play(⟦ReplacementTransform⟧(sq, tri), say("ReplacementTransform"))
        self.play(⟦Indicate⟧(tri), say("Indicate"))
        self.play(FadeOut(tri, ⟦shift⟧=DOWN), say("FadeOut(shift=DOWN)"))
        self.wait(0.5)
```

```exercise
id: ch02-animate
title: `.animate`로 이동·회전·복원하기
scene: ch02_animations.py AnimateSyntax
gif: AnimateSyntax
hint: .animate 뒤에 메서드를 이어 붙입니다. 상태 저장은 save_state, 복원 애니메이션은 Restore 입니다.
---
from manim import *


class AnimateSyntax(Scene):
    """`.animate` : 메서드 호출을 그대로 애니메이션으로."""

    def construct(self):
        sq = Square(color=BLUE, fill_opacity=0.7)
        self.add(sq)

        self.play(sq.⟦animate⟧.shift(LEFT * 3))
        self.play(sq.animate.⟦rotate⟧(PI / 4).⟦set_color⟧(YELLOW))  # 체이닝 가능
        self.play(sq.animate.scale(0.5).to_corner(UR))
        self.play(sq.animate(run_time=2, rate_func=⟦there_and_back⟧).move_to(ORIGIN))

        # 상태 저장 / 복원
        sq.⟦save_state⟧()
        self.play(sq.animate.scale(3).set_opacity(0.2))
        self.play(⟦Restore⟧(sq))
        self.wait(0.5)
```

```exercise
id: ch02-compose
title: 동시에 / 겹치며 / 차례로
scene: ch02_animations.py Composition
gif: Composition
hint: 동시에 = AnimationGroup, 겹치며 차례로 = LaggedStart, 완전히 하나씩 = Succession
---
from manim import *


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

        self.play(⟦AnimationGroup⟧(*[GrowFromCenter(s) for s in rows[0]]))  # 동시에
        self.play(⟦LaggedStart⟧(*[GrowFromCenter(s) for s in rows[1]], ⟦lag_ratio⟧=0.3))  # 겹치며 순차
        self.play(⟦Succession⟧(*[GrowFromCenter(s) for s in rows[2]]), run_time=2)  # 완전 순차
        self.wait(0.5)
```

## ✍️ 직접 해보기

1. `BasicAnimations`의 `Transform`을 `FadeTransform`으로 바꿔서 차이를 보세요.
2. `RateFunctions`에 `rate_functions.ease_in_out_elastic`과 `wiggle`을 추가해 보세요.
3. 정사각형 9개를 3×3 격자로 만들고, 가운데에서 바깥으로 퍼지듯 `LaggedStart`로 등장시켜 보세요. (힌트: 중심과의 거리로 정렬한 뒤 넣으면 됩니다)
4. `sq.animate.rotate(PI)`와 `Rotate(sq, PI)`를 나란히 재생해서 차이를 직접 확인해 보세요.
