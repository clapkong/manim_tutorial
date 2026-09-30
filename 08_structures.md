# 8. 자료구조 시각화

> 예제: [`scenes/ch08_structures.py`](scenes/ch08_structures.py)

알고리즘, 자료구조, 데이터 설명 영상에 쓰는 도구들입니다.

## GraphBFS: 그래프 탐색

![](gifs/GraphBFS.gif)

```python
g = Graph(vertices, edges, layout="tree", root_vertex=1, labels=True)
g.vertices[3]              # 정점 Mobject
g.edges[(1, 3)]            # 간선 Mobject (방향 주의: 정의한 순서대로)
```

- `layout` 옵션: `"spring"`, `"circular"`, `"kamada_kawai"`, `"planar"`, `"random"`, `"shell"`, `"spectral"`, `"tree"`, `"partite"`. 좌표 dict를 직접 넘길 수도 있습니다.
- `g.add_vertices(...)`, `g.remove_edges(...)`를 `self.play()` 안에서 쓰면 그래프 변화도 애니메이션이 됩니다.
- 방향 그래프는 `DiGraph`를 쓰세요.

## MatrixMultiply

![](gifs/MatrixMultiply.gif)

```python
A = Matrix([[1, 2], [3, 4]])
A.get_rows(), A.get_columns(), A.get_entries(), A.get_brackets()
```

`IntegerMatrix`, `DecimalMatrix`, `MobjectMatrix`(아무 Mobject나 원소로)도 있습니다.

## TableDemo

![](gifs/TableDemo.gif)

```python
table = Table(data, row_labels=[...], col_labels=[...])
table.create()                                   # 표 전용 등장 애니메이션
table.get_highlighted_cell((row, col), color=)   # 셀 배경 (좌표는 라벨 포함, 1부터 시작)
table.get_cell((r, c)), table.get_rows(), table.get_columns()
```

## AnimatedBarChart

![](gifs/AnimatedBarChart.gif)

```python
chart = BarChart(values=[...], bar_names=[...], y_range=[0, 10, 2])
self.play(chart.animate.change_bar_values(new_values))
```

## 🧩 빈칸 실습

위에서 본 예제 코드에 빈칸을 뚫었습니다. 실습 사이트(`index.html`)에서 열면 바로 채우고 채점할 수 있습니다.
GitHub에서 읽을 때는 `⟦정답⟧` 부분이 빈칸입니다.

```exercise
id: ch08-bfs
title: 그래프에서 BFS 색칠하기
scene: ch08_structures.py GraphBFS
gif: GraphBFS
hint: BFS는 큐(deque)에서 왼쪽을 꺼냅니다(popleft). 정점은 g.vertices[v], 간선은 g.edges[(u, v)].
---
from collections import deque

from manim import *


class GraphBFS(Scene):
    """Graph 로 BFS 탐색 순서를 색칠한다."""

    def construct(self):
        vertices = list(range(1, 10))
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (5, 8), (6, 9)]
        g = ⟦Graph⟧(
            vertices,
            edges,
            layout="⟦tree⟧",
            root_vertex=1,
            labels=True,
            layout_scale=2.5,
            vertex_config={"radius": 0.3, "fill_color": GREY_D},
        )
        g.shift(UP * 0.5)
        title = Text("BFS", font_size=40).to_corner(UL)
        self.play(Create(g), Write(title))

        adj = {v: [] for v in vertices}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        seen, queue = {1}, deque([1])
        order = VGroup()  # 방문 순서를 화면 아래에 쌓는다
        self.play(g.vertices[1].animate.set_fill(YELLOW))
        while queue:
            u = queue.⟦popleft⟧()
            self.play(Indicate(g.⟦vertices⟧[u], color=YELLOW), run_time=0.4)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
                    edge = g.edges[(u, v)] if (u, v) in g.edges else g.edges[(v, u)]
                    self.play(edge.animate.set_color(YELLOW), g.vertices[v].animate.set_fill(ORANGE), run_time=0.4)
            self.play(g.vertices[u].animate.set_fill(GREEN), run_time=0.3)
            item = Integer(u, font_size=32)
            order.add(item)
            order.arrange(RIGHT, buff=0.4).to_edge(DOWN)
            self.play(FadeIn(item, shift=UP * 0.2), run_time=0.2)
        self.wait()
```

```exercise
id: ch08-matrix
title: 행렬 곱을 한 칸씩 채우기
scene: ch08_structures.py MatrixMultiply
gif: MatrixMultiply
hint: 행렬은 Matrix. 행은 get_rows(), 열은 get_columns(), 원소는 get_entries().
---
from collections import deque

from manim import *


class MatrixMultiply(Scene):
    """Matrix 의 행과 열을 강조하며 곱셈 결과를 채운다."""

    def construct(self):
        A = ⟦Matrix⟧([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = Matrix([["?", "?"], ["?", "?"]])
        eq = VGroup(A, MathTex(r"\times"), B, MathTex("="), C).arrange(RIGHT)
        self.play(Write(eq))

        a, b = np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])
        result = a @ b
        rows, cols = A.⟦get_rows⟧(), B.⟦get_columns⟧()
        for i in range(2):
            for j in range(2):
                r_box = SurroundingRectangle(rows[i], color=BLUE)
                c_box = SurroundingRectangle(cols[j], color=GREEN)
                entry = C.⟦get_entries⟧()[i * 2 + j]
                value = Integer(result[i, j]).move_to(entry)
                self.play(Create(r_box), Create(c_box), run_time=0.4)
                self.play(Transform(entry, value), run_time=0.5)
                self.play(FadeOut(r_box, c_box), run_time=0.3)
        self.wait()
```

```exercise
id: ch08-bar
title: 막대그래프 값 바꾸기
scene: ch08_structures.py AnimatedBarChart
gif: AnimatedBarChart
hint: BarChart의 값을 바꾸는 메서드는 change_bar_values, 막대 위 숫자는 get_bar_labels.
---
from collections import deque

from manim import *


class AnimatedBarChart(Scene):
    """BarChart 값 변화 애니메이션."""

    def construct(self):
        chart = ⟦BarChart⟧(
            values=[3, 5, 2, 7, 4],
            bar_names=["A", "B", "C", "D", "E"],
            y_range=[0, 10, 2],
            y_length=5,
            x_length=8,
        )
        labels = chart.⟦get_bar_labels⟧(font_size=28)
        self.play(Create(chart), FadeIn(labels))
        self.wait(0.5)

        for values in [[6, 2, 8, 3, 5], [9, 7, 1, 4, 6]]:
            self.play(FadeOut(labels), run_time=0.2)
            self.play(chart.animate.⟦change_bar_values⟧(values), run_time=1.2)
            labels = chart.get_bar_labels(font_size=28)
            self.play(FadeIn(labels), run_time=0.3)
        self.wait()
```

## ✍️ 직접 해보기

1. `GraphBFS`를 DFS로 바꿔 보세요 (queue 대신 stack). 방문 순서가 어떻게 달라지는지 확인해 보세요.
2. 배열 `[5, 2, 8, 1, 9]`를 `Square`와 `Integer`로 그리고, 버블 정렬을 `Swap` 애니메이션으로 보여 주세요.
3. 피보나치 DP 표를 `Table`로 만들고, 칸을 채울 때마다 참조하는 두 칸을 하이라이트해 보세요.
