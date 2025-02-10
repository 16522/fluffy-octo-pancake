from manim import *

class SymmetricPendulumWithPBPrime(Scene):
    def construct(self):
        # 基准线配置
        base_line = Line(LEFT * 5, RIGHT * 5, color=GRAY)

        # 悬挂点参数
        POS_OFFSET = 1.5
        A_vert = 2.0  # A点垂直偏移
        B_vert = 1.5  # B点垂直偏移

        # 创建标题系统
        title = Text("两定一动（异侧）",
                     font_size=36,
                     color=GOLD_C,
                     font="Source Han Sans CN") \
            .to_edge(UP, buff=0.6) \
            .add_background_rectangle(color=BLACK, opacity=0.8)

        # 悬挂点坐标计算
        A_pos = base_line.get_start() + RIGHT * POS_OFFSET + UP * A_vert
        B_pos = base_line.get_end() + LEFT * POS_OFFSET + UP * B_vert

        # 悬挂点系统
        A = Dot(A_pos, color=GREEN_E, radius=0.08)
        B = Dot(B_pos, color=GREEN_E, radius=0.08)
        A_label = Text("A", font_size=24).next_to(A, UP, buff=0.15)
        B_label = Text("B", font_size=24).next_to(B, UP, buff=0.15)

        # 创建B'点系统
        B_prime = Dot(B.get_center() - 2 * B.get_y() * UP,
                      color=BLUE_E,
                      radius=0.08)
        B_prime_label = Text("B'", font_size=24).next_to(B_prime, DOWN, buff=0.15)
        symmetry_line = DashedLine(B, B_prime,
                                   color=GRAY,
                                   dash_length=0.2,
                                   stroke_width=2)

        # 新增：计算AB'与基准线的交点Q
        def calculate_q():
            a = A.get_center()
            b_prime = B_prime.get_center()
            denominator = b_prime[1] - a[1]
            if abs(denominator) < 1e-6:  # 处理平行情况
                return None
            t = (base_line.get_y() - a[1]) / denominator
            qx = a[0] + t * (b_prime[0] - a[0])
            return np.array([qx, base_line.get_y(), 0])

        q_point = calculate_q()
        Q = Dot(q_point, color=MAROON_E, radius=0.08) if q_point is not None else VMobject()
        BprimeQ_line = DashedLine(B_prime, Q,
                                 color=GRAY,
                                 dash_length=0.2,
                                 stroke_width=2) if q_point is not None else VMobject()
        Q_label = Text("Q", font_size=24).next_to(Q, UP, buff=0.15) if q_point is not None else VMobject()

        # 动点P系统
        P = Dot(base_line.get_start(), color=RED)
        P_label = always_redraw(lambda: Text("P").scale(0.8).next_to(P, DOWN, buff=0.1))

        # 动态连接线
        line_config = {
            "color": GREEN_E,
            "stroke_width": 4,
            "stroke_opacity": 0.8
        }
        connections = VGroup(
            always_redraw(lambda: Line(A.get_center(), P.get_center(), **line_config)),
            always_redraw(lambda: Line(B.get_center(), P.get_center(), **line_config))
        )

        # PB'动态虚线
        pb_prime_line = always_redraw(lambda: DashedLine(
            P.get_center(),
            B_prime.get_center(),
            color=PURPLE_C,
            dash_length=0.18,
            stroke_width=2.5,
            stroke_opacity=0.9
        ))

        # 其他静态元素
        a_b_prime_line = DashedLine(
            A.get_center(), B_prime.get_center(),
            color=GOLD,
            dash_length=0.25,
            stroke_width=2.5
        )

        # 直角符号系统
        foot_point = np.array([B.get_x(), base_line.get_y(), 0])
        symbol_size = 0.18
        perpendicular_symbol = VGroup(
            Line(foot_point + UP * symbol_size,
                 foot_point + UP * symbol_size + RIGHT * symbol_size,
                 color=RED_C, stroke_width=3),
            Line(foot_point + RIGHT * symbol_size + UP * symbol_size,
                 foot_point + RIGHT * symbol_size,
                 color=RED_C, stroke_width=3)
        )

        # 不等式标注
        inequality = MathTex(r"PA + PB \geq AB'",
                             color=YELLOW,
                             font_size=38
                             ).to_edge(DOWN, buff=0.6)

        # 组装场景元素（添加Q点相关元素）
        self.add(
            title, base_line, A, B, B_prime,
            connections, P, P_label, A_label, B_label,
            B_prime_label, symmetry_line, a_b_prime_line,
            perpendicular_symbol, pb_prime_line, inequality
        )
        if q_point is not None:  # 条件化添加Q点元素
            self.add(Q, BprimeQ_line, Q_label)

        # 运行动画（保持原有动画参数）
        self.play(P.animate(rate_func=linear).move_to(base_line.get_end()), run_time=3)
        self.play(P.animate(rate_func=linear).move_to(base_line.get_start()), run_time=3)
