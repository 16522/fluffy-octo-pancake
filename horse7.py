from manim import *

class FinalWithQMarker(Scene):
    def construct(self):
        # 基础坐标系设置
        OFFSET = DOWN * 1.5
        LEFT_BASE = LEFT * 3 + OFFSET
        
        # 创建坐标轴
        horizontal = Line(LEFT_BASE, LEFT_BASE + RIGHT * 6, stroke_width=3)
        diagonal = Line(
            start=LEFT_BASE,
            end=LEFT_BASE + 6 * (np.cos(30 * DEGREES) * RIGHT + np.sin(30 * DEGREES) * UP),
            stroke_width=3
        )

        # 标题系统
        title = Text("一定两动",
                    font_size=36,
                    color=GOLD,
                    font="Source Han Sans CN"
                    ).to_edge(UP, buff=0.6)
        title.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.3)

        # 核心点系统
        A = Dot(
            diagonal.get_start() + UP * 2.5 + RIGHT * 2.0,  # 保持原始坐标
            color=GREEN,
            radius=0.1
        )

        # 对称点计算函数
        def get_reflection(point, line):
            proj = line.get_projection(point)
            return 2 * proj - point

        # 对称点系统
        A1 = Dot(get_reflection(A.get_center(), diagonal), color=GREEN, radius=0.1)  # 斜线对称
        A2 = Dot(get_reflection(A1.get_center(), horizontal), color=GREEN, radius=0.1)  # A1关于水平线的对称点

        # 标签系统
        A_label = Text("A", font_size=24, color=GREEN).next_to(A, UR * 0.3)
        A1_label = Text("A1", font_size=24, color=GREEN).next_to(A1, UL * 0.3)
        A2_label = Text("A2", font_size=24, color=GREEN).next_to(A2, DOWN * 0.3)

        # 连接线系统
        AA1_line = DashedLine(A, A1, color=GREEN, stroke_width=2.5, dash_length=0.1)  # A和A1的虚线
        A1A2_line = DashedLine(A1, A2, color=GREEN, stroke_width=2.5, dash_length=0.1)  # A1和A2的虚线
        AA2_line = DashedLine(A, A2, color=GREEN, stroke_width=2.5, dash_length=0.1)  # A和A2的虚线

        # 动态点系统
        P_tracker = ValueTracker(0.0)
        P = always_redraw(lambda: Dot(
            diagonal.point_from_proportion(P_tracker.get_value()),
            color=GREEN,
            radius=0.08
        ))
        Q_prime = always_redraw(lambda: Dot(
            horizontal.point_from_proportion(1 - P_tracker.get_value()),
            color=GREEN,
            radius=0.08
        ))

        # 动态连接线
        AP_line = always_redraw(lambda: DashedLine(A, P, color=GREEN, stroke_width=2.5))
        A1P_line = always_redraw(lambda: Line(A1, P, color=YELLOW, stroke_width=3))
        PQ_line = always_redraw(lambda: Line(P, Q_prime, color=GREEN, stroke_width=3))

        # 公式显示
        formula = MathTex(r"A1P + PQ' \geq AQ", font_size=36, color=YELLOW_D).to_edge(DOWN, buff=0.8)

        # 坐标验证（调试用）
        print(f"A点坐标: {np.round(A.get_center(), 2)}")
        print(f"A2理论y值: {2*horizontal.get_start()[1] - A.get_center()[1]:.2f}")
        print(f"A2实际坐标: {np.round(A2.get_center(), 2)}")

        # 场景组装
        self.add(title, horizontal, diagonal)
        self.add(A, A1, A2)
        self.add(P, Q_prime, AP_line, A1P_line, PQ_line)
        self.add(A_label, A1_label, A2_label, formula)

        # 添加连接线
        self.add(AA1_line, A1A2_line, AA2_line)  # 添加A和A2的虚线

        # 动画演示
        self.play(P_tracker.animate.set_value(1).set_rate_func(linear), run_time=3)
        self.play(P_tracker.animate.set_value(0).set_rate_func(linear), run_time=3)
