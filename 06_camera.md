# 6. 카메라

> 예제: [`scenes/ch06_camera.py`](scenes/ch06_camera.py)

기본 `Scene`의 카메라는 고정되어 있습니다. 카메라를 움직이려면 **Scene 클래스를 바꿔야** 합니다.

| Scene | 카메라 | 조작 |
|---|---|---|
| `MovingCameraScene` | 2D 이동과 줌 | `self.camera.frame.animate.scale(0.5).move_to(...)` |
| `ZoomedScene` | 돋보기 창 추가 | `self.zoomed_camera.frame`, `self.activate_zooming()` |
| `ThreeDScene` | 3D 궤도 | `set_camera_orientation`, `move_camera` (7장) |

`self.camera.frame`은 "카메라가 보는 사각형"이라는 **Mobject**입니다. 그래서 `.animate`, `save_state()`, `Restore()`, updater를 모두 쓸 수 있습니다.

## FollowingGraphCamera (공식 예제)

![](gifs/FollowingGraphCamera.gif)

```python
self.camera.frame.save_state()
self.play(self.camera.frame.animate.scale(0.5).move_to(dot))   # 줌인
self.camera.frame.add_updater(lambda f: f.move_to(dot))        # 따라가기
self.play(MoveAlongPath(dot, graph))
self.play(Restore(self.camera.frame))                          # 원래대로
```

## ZoomIntoDetail: 깊이 줌인

![](gifs/ZoomIntoDetail.gif)

재귀 함수로 시에르핀스키 삼각형을 만들고, 모서리로 10배 줌인했다가 빠져나옵니다.

## MagnifyingGlass: 돋보기 창

![](gifs/MagnifyingGlass.gif)

```python
class MagnifyingGlass(ZoomedScene):
    def __init__(self, **kwargs):
        super().__init__(zoom_factor=0.25, zoomed_display_width=4, **kwargs)
    def construct(self):
        self.activate_zooming(animate=True)
        self.play(self.zoomed_camera.frame.animate.move_to(...))
```

## 🧩 빈칸 실습

위에서 본 예제 코드에 빈칸을 뚫었습니다. 실습 사이트(`index.html`)에서 열면 바로 채우고 채점할 수 있습니다.
GitHub에서 읽을 때는 `⟦정답⟧` 부분이 빈칸입니다.

```exercise
id: ch06-follow
title: 카메라로 점 따라가기
scene: ch06_camera.py FollowingGraphCamera
gif: FollowingGraphCamera
hint: 카메라를 움직이려면 MovingCameraScene. 카메라 사각형은 self.camera.frame.
---
from manim import *


class FollowingGraphCamera(⟦MovingCameraScene⟧):
    """카메라가 그래프 위를 달리는 점을 따라간다. (공식 예제)"""

    def construct(self):
        self.camera.⟦frame⟧.⟦save_state⟧()

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
        self.play(⟦MoveAlongPath⟧(moving_dot, graph, rate_func=linear), run_time=4)
        self.camera.frame.remove_updater(update_curve)

        self.play(⟦Restore⟧(self.camera.frame))
```

```exercise
id: ch06-zoom
title: 돋보기 창 띄우기
scene: ch06_camera.py MagnifyingGlass
gif: MagnifyingGlass
hint: 돋보기용 Scene은 ZoomedScene, 켜는 메서드는 activate_zooming.
---
from manim import *


class MagnifyingGlass(⟦ZoomedScene⟧):
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

        frame = self.⟦zoomed_camera⟧.frame
        frame.move_to(text.get_left() + RIGHT * 0.3).set_color(YELLOW)
        self.zoomed_display.display_frame.set_color(YELLOW)
        self.zoomed_display.to_corner(UR)

        self.⟦activate_zooming⟧(animate=True)
        self.play(frame.animate.move_to(text.get_right() + LEFT * 0.3), run_time=3)
        self.play(frame.animate.scale(0.5), run_time=1)
        self.wait(0.5)
```

## ✍️ 직접 해보기

1. `FollowingGraphCamera`에서 카메라가 점을 따라가는 동안 점점 더 줌인되도록 바꿔 보세요. (updater 안에서 `f.scale(...)`를 쓰면 매 프레임 누적되니 주의하세요. `set_width`로 절대 크기를 지정하는 게 안전합니다.)
2. 긴 수식을 화면에 띄워 두고, 카메라가 항 하나하나를 차례로 줌인하며 설명하는 장면을 만들어 보세요.
