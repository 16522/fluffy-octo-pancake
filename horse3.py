from manim import *

class AdjustedPointsWithQ(Scene):
    def construct(self):
        # 创建基准线（长度10单位，灰色）
        base_line = Line(LEFT * 5, RIGHT * 5, color=GRAY)

        # 调整后的坐标
        A_pos = [-3.5, 2.5, 0]  # 基准线左侧上方
        B_pos = [-1.5, 1.5, 0]  # 基准线左侧中部

        # 创建点对象
        A = Dot(A_pos, color=GREEN_E, radius=0.1)
        B = Dot(B_pos, color=GREEN_C, radius=0.1)

        # 计算Q点坐标（AB延长线与基准线的交点）
        def find_intersection():
            ax, ay = A.get_center()[:2]
            bx, by = B.get_center()[:2]
            denominator = by - ay
            if abs(denominator) < 1e-6:
                return None
            t = -ay / denominator
            qx = ax + t * (bx - ax)
            return [qx, 0, 0]

        q_point = find_intersection()

        # 创建BQ段虚线
        BQ_dashed = DashedLine(
            B.get_center(), q_point,
            color=GRAY,
            dash_length=0.2,
            stroke_width=2
        ) if q_point is not None else VMobject()

        # 标签系统
        A_label = Text("A", font_size=28, color=WHITE).next_to(A, UP, buff=0.2)
        B_label = Text("B", font_size=28, color=WHITE).next_to(B, UP, buff=0.2)
        Q_label = Text("Q", font_size=24, color=WHITE).next_to(q_point, DOWN, buff=0.15)

        # 数学公式标注
        inequality = MathTex(r"|PA - PB| \leq AB",
                             color=YELLOW,
                             font_size=38
                             ).add_background_rectangle(
            color=BLACK,
            opacity=0.7,
            buff=0.18
        ).to_edge(DOWN, buff=1.8)

        # 动点系统
        P = Dot(base_line.get_start(), color=RED)
        PA = always_redraw(lambda: Line(A.get_center(), P.get_center(), color=GREEN_E))
        PB = always_redraw(
            lambda: Line(B.get_center(), P.get_center())
            .set_stroke(width=3)
            .set_color_by_gradient(GREEN_B, GREEN_E)
        )

        # 动态标签
        P_label = always_redraw(lambda: Text("P", font_size=24)
                                .add_background_rectangle(opacity=0.7)
                                .next_to(P, DOWN, buff=0.15))

        # 创建标题（新增部分）
        title = Text("两定一动（同侧）",
                     font_size=36,
                     color=GOLD_C,
                     font="Source Han Sans CN"
                     ).to_edge(UP, buff=0.6)
        title.add_background_rectangle(color=BLACK, opacity=0.8)

        # 组装场景元素（添加标题到元素列表）
        elements = [
            base_line, A, B,
            A_label, B_label,
            P, P_label,
            PA, PB,
            BQ_dashed,
            inequality,
            title
        ]
        if q_point is not None:
            elements.append(Q_label.add_background_rectangle(opacity=0.7))
        self.add(*elements)

        # 修改后的动画部分（总时长6秒）
        self.play(
            P.animate(rate_func=linear).move_to(base_line.get_end()),
            run_time=3,  # 去程时间缩短到3秒
        )
        self.play(
            P.animate(rate_func=linear).move_to(base_line.get_start()),
            run_time=3,  # 返程时间缩短到3秒
        )
