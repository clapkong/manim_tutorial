# 8. 자료구조 시각화

예제 원본: [`scenes/ch08_structures.py`](scenes/ch08_structures.py)

## 핵심 개념

알고리즘, 자료구조, 데이터 설명 영상에 쓰는 도구들입니다. 그래프, 행렬, 표, 막대그래프 모두 안쪽 요소(정점, 원소, 셀, 막대)를 따로 꺼낼 수 있어서, 특정 부분만 색칠하거나 강조하며 설명할 수 있습니다.

## GraphBFS: 그래프 탐색

정점과 간선 목록으로 그래프를 그리고, BFS 방문 순서대로 정점과 간선을 색칠하는 예제입니다. 그래프 알고리즘은 파이썬으로 평소처럼 짜고, 방문할 때마다 해당 정점이나 간선 Mobject를 꺼내 애니메이션합니다.

- `Graph(정점목록, 간선목록, layout=, labels=True)`: 그래프 생성
  - 정점은 번호나 이름, 간선은 `(u, v)` 튜플
  - `layout`: `"spring"`, `"circular"`, `"kamada_kawai"`, `"planar"`, `"shell"`, `"partite"`, `"tree"`
  - `"tree"`는 `root_vertex=`로 뿌리를 정해야 함
- `g.vertices[v]`: 정점 Mobject
- `g.edges[(u, v)]`: 간선 Mobject
  - 정의한 방향 그대로 키가 됨
- `collections.deque`: BFS용 큐
  - `popleft()`: 앞에서 꺼냄

![](gifs/GraphBFS.gif)

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
        g = ⟦Graph⟧(  # 그래프 생성
            vertices,
            edges,
            layout="⟦tree⟧",  # 트리 모양 배치
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
            u = queue.⟦popleft⟧()  # 큐 앞에서 꺼내기
            self.play(Indicate(g.⟦vertices⟧[u], color=YELLOW), run_time=0.4)  # 방문 중인 정점 강조
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

## MatrixMultiply: 행렬 곱

행렬 곱셈 결과를 한 칸씩 채우는 예제입니다. 계산할 칸마다 사용하는 행과 열에 테두리를 두르고, 결과 칸의 `?`를 숫자로 바꿉니다.

- `Matrix([[1, 2], [3, 4]])`: 행렬 생성
  - `IntegerMatrix`: 정수 전용
  - `MobjectMatrix`: 아무 Mobject나 원소로
- `get_rows()` / `get_columns()`: 행 묶음 / 열 묶음
- `get_entries()`: 모든 원소 (왼쪽 위부터 한 줄씩)
- `get_brackets()`: 괄호
- `SurroundingRectangle(행 또는 열)`: 행이나 열에 테두리
- `Transform(entry, 숫자)`: `?`를 숫자로 교체

![](gifs/MatrixMultiply.gif)

```exercise
id: ch08-matrix
title: 행렬 곱을 한 칸씩 채우기
scene: ch08_structures.py MatrixMultiply
gif: MatrixMultiply
hint: 행렬은 Matrix. 행은 get_rows(), 열은 get_columns(), 원소는 get_entries().
---
from manim import *


class MatrixMultiply(Scene):
    """Matrix 의 행과 열을 강조하며 곱셈 결과를 채운다."""

    def construct(self):
        A = ⟦Matrix⟧([[1, 2], [3, 4]])  # 행렬 A
        B = Matrix([[5, 6], [7, 8]])
        C = Matrix([["?", "?"], ["?", "?"]])
        eq = VGroup(A, MathTex(r"\times"), B, MathTex("="), C).arrange(RIGHT)
        self.play(Write(eq))

        a, b = np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])
        result = a @ b
        rows, cols = A.⟦get_rows⟧(), B.⟦get_columns⟧()  # A의 행 묶음, B의 열 묶음
        for i in range(2):
            for j in range(2):
                r_box = SurroundingRectangle(rows[i], color=BLUE)
                c_box = SurroundingRectangle(cols[j], color=GREEN)
                entry = C.⟦get_entries⟧()[i * 2 + j]  # 결과 행렬의 (i, j) 원소
                value = Integer(result[i, j]).move_to(entry)
                self.play(Create(r_box), Create(c_box), run_time=0.4)
                self.play(Transform(entry, value), run_time=0.5)
                self.play(FadeOut(r_box, c_box), run_time=0.3)
        self.wait()
```

## TableDemo: 표

성적표를 만들고 과목별 최고 점수 칸에 배경색을 까는 예제입니다. 표는 데이터와 행, 열 라벨을 받아 만들고, 셀 좌표로 원하는 칸을 꺼냅니다.

- `Table(데이터, row_labels=, col_labels=, include_outer_lines=True)`: 표 생성
  - 데이터는 문자열의 2차원 리스트
  - 라벨은 `Text` 목록
- `table.create()`: 선을 그리고 글자를 쓰는 표 전용 등장 애니메이션
- `table.get_highlighted_cell((행, 열), color=)`: 셀 배경 생성
  - 좌표는 라벨을 포함해 1부터 셈. 예: 첫 데이터 칸은 `(2, 2)`
- `table.add_to_back(mob)`: 객체를 맨 뒤로 보냄
  - 배경이 글자를 가리지 않게 할 때 사용

![](gifs/TableDemo.gif)

```exercise
id: ch08-table
title: 성적표 만들고 최고점 강조하기
scene: ch08_structures.py TableDemo
gif: TableDemo
hint: 표는 Table(데이터, row_labels=, col_labels=). 표 전용 등장은 table.create(). 셀 배경은 get_highlighted_cell, 글자 뒤로 보내기는 add_to_back.
---
from manim import *


class TableDemo(Scene):
    """Table: 행/열 라벨, 셀 강조."""

    def construct(self):
        table = ⟦Table⟧(  # 표 생성
            [["98", "85", "77"], ["72", "91", "88"], ["65", "70", "95"]],
            ⟦row_labels⟧=[Text("세진"), Text("준희"), Text("수빈")],  # 행 라벨 (이름)
            col_labels=[Text("수학"), Text("영어"), Text("과학")],
            include_outer_lines=True,
        ).scale(0.6)
        self.play(table.⟦create⟧())  # 표 전용 등장 애니메이션
        # 최고 점수 셀 강조 (좌표는 라벨 포함, 1부터 시작)
        for pos in [(2, 2), (3, 3), (4, 4)]:
            cell = table.⟦get_highlighted_cell⟧(pos, color=GREEN_E)  # 셀 배경 만들기
            table.⟦add_to_back⟧(cell)  # 배경을 글자 뒤로 보내기
            self.play(FadeIn(cell), run_time=0.5)
        self.play(Circumscribe(table.get_rows()[1]))
        self.wait()
```

## AnimatedBarChart: 막대그래프

막대그래프를 그리고 값을 두 번 바꾸는 예제입니다. 막대 높이는 애니메이션으로 바뀌지만 막대 위 숫자 라벨은 자동으로 바뀌지 않아서, 값을 바꿀 때마다 라벨을 새로 만듭니다.

- `BarChart(values=, bar_names=, y_range=[최소, 최대, 간격])`: 막대그래프 생성
- `chart.get_bar_labels(font_size=)`: 막대 위 숫자 라벨
- `chart.animate.change_bar_values(새값들)`: 값 변경 애니메이션

![](gifs/AnimatedBarChart.gif)

```exercise
id: ch08-bar
title: 막대그래프 값 바꾸기
scene: ch08_structures.py AnimatedBarChart
gif: AnimatedBarChart
hint: BarChart의 값을 바꾸는 메서드는 change_bar_values, 막대 위 숫자는 get_bar_labels.
---
from manim import *


class AnimatedBarChart(Scene):
    """BarChart 값 변화 애니메이션."""

    def construct(self):
        chart = ⟦BarChart⟧(  # 막대그래프 생성
            values=[3, 5, 2, 7, 4],
            bar_names=["A", "B", "C", "D", "E"],
            y_range=[0, 10, 2],
            y_length=5,
            x_length=8,
        )
        labels = chart.⟦get_bar_labels⟧(font_size=28)  # 막대 위 숫자 라벨
        self.play(Create(chart), FadeIn(labels))
        self.wait(0.5)

        for values in [[6, 2, 8, 3, 5], [9, 7, 1, 4, 6]]:
            self.play(FadeOut(labels), run_time=0.2)
            self.play(chart.animate.⟦change_bar_values⟧(values), run_time=1.2)  # 막대 높이를 새 값으로 변경
            labels = chart.get_bar_labels(font_size=28)
            self.play(FadeIn(labels), run_time=0.3)
        self.wait()
```

## ✍️ 직접 해보기

1. `GraphBFS`를 DFS로 바꿔 보세요 (queue 대신 stack). 방문 순서가 어떻게 달라지는지 확인해 보세요.
2. 배열 `[5, 2, 8, 1, 9]`를 `Square`와 `Integer`로 그리고, 버블 정렬을 `Swap` 애니메이션으로 보여 주세요.
3. 피보나치 DP 표를 `Table`로 만들고, 칸을 채울 때마다 참조하는 두 칸을 하이라이트해 보세요.
