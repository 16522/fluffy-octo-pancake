from manim import *


class MovingPointWithTitle(Scene):
    def construct(self):
        # 坐标系配置
        coord = Axes(x_range=[-4, 4], y_range=[-3, 3], tips=False)
        horizontal_line = Line(LEFT * 4, RIGHT * 4).set_opacity(0.7)
        A = Dot(point=[-3, -2, 0], color=BLUE)
        B = Dot(point=[3, 2, 0], color=BLUE)
        AB_line = DashedLine(A, B, color=GRAY, dash_length=0.1)

        # 新增：计算Q点（AB与水平线交点）
        def get_intersection():
            a = A.get_center()
            b = B.get_center()
            denominator = b[1] - a[1]
            if abs(denominator) < 1e-6:  # 处理水平情况
                return None
            t = -a[1] / denominator
            qx = a[0] + t * (b[0] - a[0])
            return np.array([qx, 0, 0])

        q_point = get_intersection()
        Q = Dot(q_point, color=BLUE) if q_point is not None else VMobject()
        BQ_line = DashedLine(B, Q, color=GRAY, dash_length=0.1) if q_point is not None else VMobject()
        Q_label = Tex("Q").next_to(Q, UP, buff=0.15).add_background_rectangle(
            opacity=0.7) if q_point is not None else VMobject()

        # 动态元素配置
        P = Dot(color=RED).move_to(horizontal_line.get_start())
        PA_line = always_redraw(lambda: Line(A, P, color=GREEN))
        PB_line = always_redraw(lambda: Line(B, P, color=GREEN))

        # 修正后的中文标题
        title = Text("两定一动（同侧）",
                     font_size=36,
                     color=GOLD_C,
                     font="Source Han Sans CN") \
            .to_edge(UP, buff=0.6) \
            .add_background_rectangle(color=BLACK, opacity=0.8)

        # 标签系统
        label_group = VGroup(
            Tex("A").next_to(A, DOWN),
            Tex("B").next_to(B, UP),
            Tex("P").add_updater(lambda m: m.next_to(P, DOWN, 0.2))
        )

        # 不等式标注
        inequality = MathTex(r"PA + PB \geq AB", color=YELLOW).to_edge(DOWN, buff=0.6)

        # 场景元素添加（新增Q相关元素）
        self.add(horizontal_line, AB_line, P, PA_line, PB_line,
                 label_group, inequality, title)
        if q_point is not None:  # 仅在存在交点时添加
            self.add(Q, BQ_line, Q_label)

        # 保持原有动画序列
        self.play(
            P.animate.move_to(horizontal_line.get_end()),
            run_time=2.5,
            rate_func=linear
        )
        self.play(
            P.animate.move_to(horizontal_line.get_start()),
            run_time=2.5,
            rate_func=linear
        )
        self.wait(0.5)
