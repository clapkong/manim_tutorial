# 4. Updater와 ValueTracker

예제 원본: [`scenes/ch04_updaters.py`](scenes/ch04_updaters.py)

## 핵심 개념

이 장이 Manim에서 가장 중요합니다. "A가 움직이면 B가 따라간다"는 관계를 한 번 선언해 두면, 애니메이션 하나만 재생해도 연결된 모든 객체가 같이 움직입니다. 관계는 updater로 선언하고, 여러 객체를 한꺼번에 움직일 기준 값은 `ValueTracker`로 만듭니다.

- `mob.add_updater(lambda m: ...)`: 매 프레임 기존 객체를 수정
  - 위치나 값만 바뀔 때 사용 (가벼움)
- `always_redraw(lambda: 새객체(...))`: 매 프레임 객체를 새로 생성
  - 모양 자체가 바뀔 때 사용 (편하지만 무거움)
- `mob.add_updater(lambda m, dt: ...)`: 프레임 사이 시간 `dt`를 받는 updater
  - 애니메이션 없이 계속 움직일 때 사용 (회전, 흐름)
- `ValueTracker(시작값)`: 화면에 안 보이는 숫자 변수
  - `t.get_value()`: 현재 값 읽기
  - `t.animate.set_value(x)`: x까지 부드럽게 변경
  - `t.animate.increment_value(dx)`: 현재 값에 dx를 더함

## ValueTrackerBasics: 값 하나로 여러 객체 움직이기

`ValueTracker` 값 하나를 포인터, 숫자, 원이 함께 읽는 예제입니다. 트래커만 움직이면 세 객체가 모두 따라 움직입니다. 위치만 바뀌는 객체는 updater로, 모양이 바뀌는 객체는 `always_redraw`로 만듭니다.

- `line.n2p(값)`: 수직선 위 값을 화면 좌표로 변환 (number to point)
- `pointer.add_updater(...)`: 포인터가 트래커 값을 따라 이동
- `always_redraw(lambda: Circle(radius=t.get_value()))`: 반지름이 바뀌는 원을 매번 새로 생성
- `self.add(...)`: updater를 붙인 객체는 반드시 화면에 추가해야 동작

![](gifs/ValueTrackerBasics.gif)

```exercise
id: ch04-tracker
title: ValueTracker 하나로 여러 객체 움직이기
scene: ch04_updaters.py ValueTrackerBasics
gif: ValueTrackerBasics
hint: 값을 읽을 땐 get_value(), 애니메이션으로 바꿀 땐 t.animate.set_value(x). 모양이 바뀌면 always_redraw.
---
from manim import *


class ValueTrackerBasics(Scene):
    """ValueTracker 하나로 여러 객체를 동시에 구동한다."""

    def construct(self):
        t = ⟦ValueTracker⟧(1)  # 화면에 안 보이는 숫자 변수 (시작값 1)

        line = NumberLine(x_range=[0, 3, 0.5], length=8, include_numbers=True).to_edge(DOWN, buff=1)
        pointer = Triangle(color=YELLOW, fill_opacity=1).scale(0.15).rotate(PI)
        label = DecimalNumber(num_decimal_places=2, font_size=36)

        # add_updater: 매 프레임마다 tracker 값을 읽어 자기 자신을 갱신
        pointer.⟦add_updater⟧(lambda m: m.next_to(line.n2p(t.⟦get_value⟧()), UP, buff=0.1))  # 매 프레임 포인터를 트래커 값 위치로 이동
        label.add_updater(lambda m: m.set_value(t.get_value()).next_to(pointer, UP))

        # always_redraw: 매 프레임 객체를 '새로 만든다' (모양 자체가 바뀔 때 편함)
        circle = ⟦always_redraw⟧(  # 반지름이 바뀌는 원을 매 프레임 새로 생성
            lambda: Circle(radius=t.get_value(), color=BLUE, fill_opacity=0.3).shift(UP)
        )
        r_text = always_redraw(
            lambda: MathTex(f"r = {t.get_value():.2f}").next_to(circle, RIGHT)
        )

        self.add(line, pointer, label, circle, r_text)
        self.play(t.animate.⟦set_value⟧(2.5), run_time=2)  # 트래커 값을 2.5까지 부드럽게 변경
        self.play(t.animate.set_value(0.5), run_time=2)
        self.play(t.animate.set_value(1.5), run_time=1, rate_func=there_and_back)
        self.wait(0.5)
```

## MovingAngle: 움직이는 각도 (공식 예제)

두 선 사이의 각도가 바뀔 때 각도 호와 θ 라벨이 따라오는 예제입니다. 각도 값은 `ValueTracker`로 두고, 움직이는 선, 호, 라벨이 모두 updater로 그 값을 따라갑니다.

- `Angle(선1, 선2, radius=)`: 두 선 사이의 각도 호
- `x.become(새객체)`: 객체를 새 객체의 모양으로 통째로 변경
  - updater 안에서 자주 사용
- `DEGREES`: 도를 라디안으로 바꾸는 상수
  - 예: `110 * DEGREES`
- `t.animate.set_value(x)`: 절대값으로 이동
- `t.animate.increment_value(dx)`: 현재 값에 더함

![](gifs/MovingAngle.gif)

```exercise
id: ch04-angle
title: 움직이는 각도 표시하기
scene: ch04_updaters.py MovingAngle
gif: MovingAngle
hint: 각도 호는 Angle(선1, 선2). updater 안에서 통째로 바꿀 땐 become. 현재 값에 더하는 건 increment_value.
---
from manim import *


class MovingAngle(Scene):
    """각도가 변하면 Angle 호와 θ 라벨이 따라온다. (공식 예제 MovingAngle)"""

    def construct(self):
        rotation_center = LEFT
        theta_tracker = ⟦ValueTracker⟧(110)  # 각도 값 (시작 110도)

        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(theta_tracker.get_value() * DEGREES, about_point=rotation_center)

        a = ⟦Angle⟧(line1, line_moving, radius=0.5, other_angle=False)  # 두 선 사이의 각도 호
        tex = MathTex(r"\theta").move_to(
            Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        self.add(line1, line_moving, a, tex)

        line_moving.add_updater(
            lambda x: x.⟦become⟧(line_ref.copy()).rotate(  # 기준선 복사본으로 통째로 바꾼 뒤 회전
                theta_tracker.get_value() * ⟦DEGREES⟧, about_point=rotation_center  # 도 단위를 라디안으로
            )
        )
        a.add_updater(lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False)))
        tex.add_updater(
            lambda x: x.move_to(
                Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.⟦increment_value⟧(140))  # 현재 각도에 140도 더하기
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))
        self.wait(0.5)
```

## DtUpdater: 시간 기반 updater

updater 함수가 인자를 두 개 받으면 Manim이 두 번째 인자로 직전 프레임과의 시간 차이(초)를 넣어 줍니다. 이 시간에 비례해서 움직이면 프레임 수와 상관없이 일정한 속도가 됩니다.

- `add_updater(lambda m, dt: m.rotate(dt * 속도))`: 초당 일정한 속도로 회전
  - `self.play` 없이 `self.wait()` 동안에도 계속 움직임
- `mob.clear_updaters()`: 붙은 updater를 모두 뗌
- `mob.remove_updater(함수)`: updater 하나만 뗌

![](gifs/DtUpdater.gif)

```exercise
id: ch04-dt
title: 시간으로 계속 도는 updater
scene: ch04_updaters.py DtUpdater
gif: DtUpdater
hint: 두 번째 인자로 프레임 간 시간을 받습니다. updater를 모두 떼는 메서드는 clear_updaters.
---
from manim import *


class DtUpdater(Scene):
    """dt 를 받는 updater: 애니메이션 없이 wait() 동안에도 계속 움직인다."""

    def construct(self):
        square = Square(color=TEAL, fill_opacity=0.5)
        # (mobject, dt) 시그니처면 시간 기반 updater 가 된다 (dt = 프레임 간 시간)
        square.add_updater(lambda m, ⟦dt⟧: m.rotate(dt * PI / 2))  # 두 번째 인자로 프레임 간 시간을 받음
        self.add(square)
        self.⟦wait⟧(2)  # 2초 대기 (그동안에도 계속 회전)

        # 도중에 updater 를 떼면 멈춘다
        square.⟦clear_updaters⟧()  # 붙은 updater 모두 떼기
        self.play(square.animate.set_color(RED))
        self.wait(0.5)
```

## Epicycles: 미니 푸리에 에피사이클

회전하는 화살표 두 개를 이어 붙이고, 끝점이 지나간 자리를 선으로 남기면 복잡한 곡선이 그려집니다. 화살표 위치는 `ValueTracker` 하나로 계산하고, 트래커가 움직일 때마다 화살표와 자취가 함께 갱신됩니다. 이 원리를 확장한 것이 `manimations` 프로젝트의 푸리에 그리기(`src/manimations/fourier_*.py`)입니다.

- `always_redraw(lambda: ...)`: 매 프레임 객체를 새로 생성
  - 화살표처럼 모양이 계속 바뀌는 객체에 사용
- `TracedPath(함수)`: 함수가 돌려주는 점의 자취를 그림
  - 예: `TracedPath(dot.get_center)`
  - 메서드를 괄호 없이 넘김
- `TAU`: 한 바퀴 (2π)
- `rate_func=linear`: 처음부터 끝까지 같은 속도
  - 속도가 일정해야 자취가 고르게 그려짐

![](gifs/Epicycles.gif)

```exercise
id: ch04-epi
title: 회전하는 벡터 두 개로 그림 그리기
scene: ch04_updaters.py Epicycles
gif: Epicycles
hint: 자취를 그리는 클래스는 TracedPath. 일정한 속도로 돌리려면 rate_func=linear.
---
from manim import *


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
        vec1 = ⟦always_redraw⟧(lambda: Arrow(center, tip1(), buff=0, color=BLUE))  # 첫 번째 화살표를 매 프레임 새로 생성
        vec2 = always_redraw(lambda: Arrow(tip1(), tip2(), buff=0, color=GREEN))
        pen = always_redraw(lambda: Dot(tip2(), color=YELLOW, radius=0.05))
        trace = ⟦TracedPath⟧(pen.⟦get_center⟧, stroke_color=YELLOW, stroke_width=3)  # 펜 위치가 지나간 자취 그리기

        self.add(circle1, circle2, vec1, vec2, trace, pen)
        self.play(t.animate.set_value(⟦TAU⟧), run_time=6, rate_func=⟦linear⟧)  # 한 바퀴를 일정한 속도로
        self.wait(0.5)
```

## 자주 하는 실수

- updater를 붙인 객체를 `self.add()` 하지 않음
  - 화면에 없는 객체는 업데이트되지 않음
- `always_redraw` 객체에 `.animate` 사용
  - 매 프레임 새로 만들어지므로 효과가 사라짐. 대신 트래커를 움직임
- lambda가 반복문 변수를 캡처
  - `for i in ...: lambda m: ... i ...`는 모두 마지막 `i`를 봄
  - `lambda m, i=i: ...`로 고정
- updater 해제를 잊음
  - 이후 애니메이션과 충돌하면 `mob.clear_updaters()` 또는 `mob.suspend_updating()`

## ✍️ 직접 해보기

1. `ValueTrackerBasics`에 넓이 `πr²`를 보여 주는 `DecimalNumber`를 추가해 보세요.
2. `Epicycles`에 세 번째 벡터를 추가하고, 각속도를 바꿔 가며 어떤 모양이 나오는지 보세요.
3. 진자를 만들어 보세요. `theta = ValueTracker(...)`, 추(`Dot`)와 줄(`Line`)은 `always_redraw`로, 흔들림은 `rate_func=there_and_back`으로 표현합니다.
4. 시계를 만들어 보세요. 시침과 분침에 `dt` updater를 붙이고, 분침은 시침보다 12배 빠르게 돌립니다.
