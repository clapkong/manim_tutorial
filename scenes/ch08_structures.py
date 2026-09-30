"""8장. 자료구조 시각화: Graph / Matrix / Table / BarChart

실행:
    uv run manim -pql scenes/ch08_structures.py GraphBFS
"""

from collections import deque

from manim import *


class GraphBFS(Scene):
    """Graph 로 BFS 탐색 순서를 색칠한다."""

    def construct(self):
        vertices = list(range(1, 10))
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (5, 8), (6, 9)]
        g = Graph(
            vertices,
            edges,
            layout="tree",
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
            u = queue.popleft()
            self.play(Indicate(g.vertices[u], color=YELLOW), run_time=0.4)
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


class MatrixMultiply(Scene):
    """Matrix 의 행과 열을 강조하며 곱셈 결과를 채운다."""

    def construct(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = Matrix([["?", "?"], ["?", "?"]])
        eq = VGroup(A, MathTex(r"\times"), B, MathTex("="), C).arrange(RIGHT)
        self.play(Write(eq))

        a, b = np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])
        result = a @ b
        rows, cols = A.get_rows(), B.get_columns()
        for i in range(2):
            for j in range(2):
                r_box = SurroundingRectangle(rows[i], color=BLUE)
                c_box = SurroundingRectangle(cols[j], color=GREEN)
                entry = C.get_entries()[i * 2 + j]
                value = Integer(result[i, j]).move_to(entry)
                self.play(Create(r_box), Create(c_box), run_time=0.4)
                self.play(Transform(entry, value), run_time=0.5)
                self.play(FadeOut(r_box, c_box), run_time=0.3)
        self.wait()


class TableDemo(Scene):
    """Table: 행/열 라벨, 셀 강조."""

    def construct(self):
        table = Table(
            [["98", "85", "77"], ["72", "91", "88"], ["65", "70", "95"]],
            row_labels=[Text("세진"), Text("준희"), Text("수빈")],
            col_labels=[Text("수학"), Text("영어"), Text("과학")],
            include_outer_lines=True,
        ).scale(0.6)
        self.play(table.create())
        # 최고 점수 셀 강조 (좌표는 라벨 포함, 1부터 시작)
        for pos in [(2, 2), (3, 3), (4, 4)]:
            cell = table.get_highlighted_cell(pos, color=GREEN_E)
            table.add_to_back(cell)  # 글자 뒤에 깔리도록
            self.play(FadeIn(cell), run_time=0.5)
        self.play(Circumscribe(table.get_rows()[1]))
        self.wait()


class AnimatedBarChart(Scene):
    """BarChart 값 변화 애니메이션."""

    def construct(self):
        chart = BarChart(
            values=[3, 5, 2, 7, 4],
            bar_names=["A", "B", "C", "D", "E"],
            y_range=[0, 10, 2],
            y_length=5,
            x_length=8,
        )
        labels = chart.get_bar_labels(font_size=28)
        self.play(Create(chart), FadeIn(labels))
        self.wait(0.5)

        for values in [[6, 2, 8, 3, 5], [9, 7, 1, 4, 6]]:
            self.play(FadeOut(labels), run_time=0.2)
            self.play(chart.animate.change_bar_values(values), run_time=1.2)
            labels = chart.get_bar_labels(font_size=28)
            self.play(FadeIn(labels), run_time=0.3)
        self.wait()
