from manim import *

class FinalWithQMarker(Scene):
    def construct(self):
        OFFSET = DOWN * 1.5
        LEFT_BASE = LEFT * 3 + OFFSET

        # 创建坐标系（保持不变）
        horizontal = Line(LEFT_BASE, LEFT_BASE + RIGHT * 6, stroke_width=3)
        diagonal = Line(
            start=LEFT_BASE,
            end=LEFT_BASE + 6 * (np.cos(30 * DEGREES) * RIGHT + np.sin(30 * DEGREES) * UP),
            stroke_width=3
        )

        # 标题部分（保持不变）
        title = Text("一定两动",
                     font_size=36,
                     color=GOLD,
                     font="Source Han Sans CN"
                     ).to_edge(UP, buff=0.6)
        title.add_background_rectangle(
            color=BLACK,
            opacity=0.8,
            buff=0.3
        )

        # A点及其对称点A'系统
        A = Dot(
            diagonal.get_start() + UP * 2.5 + RIGHT * 2.0,
            color=GREEN,
            radius=0.1
        )
        # 计算A关于斜线的对称点A'
        diagonal_line = Line(diagonal.get_start(), diagonal.get_end())
        A_projection = diagonal_line.get_projection(A.get_center())
        A_prime = Dot(
            2*A_projection - A.get_center(),  # 镜像公式
            color=GREEN,
            radius=0.1
        )
        # 修改点A'标签样式（与A统一）
        A_label = Text("A", font_size=24, color=GREEN, font="Source Han Sans CN").next_to(A, UR * 0.3)
        A_prime_label = Text("A'", font_size=24, color=GREEN, font="Source Han Sans CN").next_to(A_prime,
                                                                                                 UL * 0.3)  # 修改字体设置

        # 新增A-A'虚线连接
        AA_prime_line = DashedLine(
            A.get_center(), A_prime.get_center(),
            color=GREEN,
            stroke_width=2.5,
            dash_length=0.1,
            dashed_ratio=0.5455  # 与AP线参数一致
        )
        # 垂线系统（保持不变）
        foot_point = np.array([A.get_center()[0], horizontal.get_start()[1], 0])
        vertical_line = DashedLine(
            A.get_center(), foot_point,
            color=GREEN,
            stroke_width=2.5,
            dash_length=0.1
        )
        right_angle = VGroup(
            Line(foot_point, foot_point + UR * 0.15, color=GREEN, stroke_width=3),
            Line(foot_point + RIGHT * 0.15, foot_point + UR * 0.15, color=GREEN, stroke_width=3),
            Line(foot_point + UP * 0.15, foot_point + UR * 0.15, color=GREEN, stroke_width=3)
        )
        Q_label = Text("Q", font_size=24, color=GREEN).next_to(foot_point, DOWN * 0.3)

        # 动态点系统（保持不变）
        P_tracker = ValueTracker(0.0)
        P = always_redraw(lambda: Dot(
            diagonal.point_from_proportion(P_tracker.get_value()),
            color=GREEN,
            radius=0.08
        ))
        P_label = always_redraw(lambda: Text("P", font_size=24, color=GREEN)
                                .next_to(P, UP * 0.3 + RIGHT * 0.3))
        Q_prime = always_redraw(lambda: Dot(
            horizontal.point_from_proportion(1 - P_tracker.get_value()),
            color=GREEN,
            radius=0.08
        ))
        Q_prime_label = always_redraw(lambda: Text("Q'", font_size=24, color=GREEN)
                                      .next_to(Q_prime, DOWN * 0.3))

        # 连接线系统（新增A'P连线）
        AP_line = always_redraw(lambda: DashedLine(
            A.get_center(), P.get_center(),
            color=GREEN,
            stroke_width=2.5,
            dash_length=0.1,
            dashed_ratio=0.5455
        ))
        A_prime_P_line = always_redraw(lambda: Line(  # 新增对称点连线
            A_prime.get_center(), P.get_center(),
            color=YELLOW,
            stroke_width=3
        ))
        PQ_line = always_redraw(lambda: Line(
            P.get_center(), Q_prime.get_center(),
            color=GREEN,
            stroke_width=3
        ))

        # 公式显示（保持不变）
        formula = MathTex(r"A'P + PQ' \geq AQ",  # 修改此处
                          font_size=36,
                          color=YELLOW_D).to_edge(DOWN, buff=0.8)

        # 添加所有元素（新增A'相关元素）
        self.add(title, horizontal, diagonal)
        self.add(A, A_prime, P, Q_prime,
                AP_line, A_prime_P_line, PQ_line,  # 新增A'P连线
                vertical_line, right_angle, Q_label,
                A_label, A_prime_label, P_label, Q_prime_label, formula)

        # 动画设置（保持不变）
        self.play(
            P_tracker.animate.set_value(1).set_rate_func(linear),
            run_time=3
        )
        self.play(
            P_tracker.animate.set_value(0).set_rate_func(linear),
            run_time=3
        )
