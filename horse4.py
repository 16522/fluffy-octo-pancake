from manim import *

class GeometricRelationship(Scene):
    def construct(self):
        # 配置参数（关键修改点📍）
        CONFIG = {
            "line_length": 10.0,
            "vertical_offset": 1.2,
            "dot_radius": 0.08,
            "a_position": 0.25,
            "a_offset_scale": 1.8,
            "b_position": 0.55,
            "animation_duration": 6,  # 总时长设为6秒
            "base_line_y": 0.3
        }


        # 创建基准线（水平线）
        base_line = Line(
            LEFT * CONFIG["line_length"] / 2,
            RIGHT * CONFIG["line_length"] / 2,
            color=GREY_B
        ).shift(UP * CONFIG["base_line_y"])

        # 点生成函数（带偏移量）
        def create_anchored_point(proportion, color, label, offset_scale=1.0):
            base_point = base_line.point_from_proportion(proportion)
            dot_position = base_point + UP * CONFIG["vertical_offset"] * offset_scale
            dot = Dot(dot_position, color=color, radius=CONFIG["dot_radius"])
            label = Tex(label, font_size=28).next_to(dot, UP if offset_scale > 0 else DOWN, buff=0.12)
            return dot, label

        # 创建固定点
        dot_a, label_a = create_anchored_point(CONFIG["a_position"], GREEN_D, "A", CONFIG["a_offset_scale"])
        dot_b, label_b = create_anchored_point(CONFIG["b_position"], BLUE_D, "B'", 0.7)
        dot_b_prime, label_b_prime = create_anchored_point(CONFIG["b_position"], BLUE_C, "B", -0.7)

        # 计算Q点（AB延长线与基准线的交点）
        def calculate_intersection(a, b, base_y):
            """计算两点连线与水平线的交点"""
            if a[1] == b[1]:  # 处理水平线情况
                return b if abs(a[1] - base_y) < 1e-6 else np.array([np.inf, base_y, 0])

            t = (base_y - a[1]) / (b[1] - a[1])
            x = a[0] + t * (b[0] - a[0])
            return np.array([x, base_y, 0])

        q_point = calculate_intersection(
            dot_a.get_center(),
            dot_b.get_center(),
            CONFIG["base_line_y"]
        )
        q_dot = Dot(q_point, color=GREY_D, radius=CONFIG["dot_radius"])
        q_label = Tex("Q", font_size=24).next_to(q_dot, DOWN, buff=0.1)

        # BQ段虚线
        bq_dashed = DashedLine(
            dot_b.get_center(), q_point,
            color=GREY,
            dash_length=0.15,
            stroke_width=2.5
        )

        # 点P初始位置设为左侧端点
        moving_p = Dot(base_line.get_start(),  # 初始位置改为左侧
                      color=RED_D,
                      radius=CONFIG["dot_radius"])
        label_p = always_redraw(lambda: Tex("P", font_size=24).next_to(moving_p, DOWN, buff=0.1))

        # 动态连接线
        connections = VGroup(
            always_redraw(lambda: Line(
                dot_a.get_center(), moving_p.get_center(),
                color=GREEN_B,
                stroke_width=3.5
            )),
            always_redraw(lambda: DashedLine(
                dot_b.get_center(), moving_p.get_center(),
                color=BLUE_B,
                dash_length=0.2,
                stroke_width=3.5
            )),
            always_redraw(lambda: Line(
                moving_p.get_center(), dot_b_prime.get_center(),
                color=PURPLE_B,
                stroke_width=3.5
            ))
        )

        # 创建标题
        title = Text("两定一动（异侧）",
                   font_size=36,
                   color=GOLD_C,
                   font="Source Han Sans CN"
                   ).to_edge(UP, buff=0.6)
        title.add_background_rectangle(color=BLACK, opacity=0.8)

        # 添加所有元素
        self.add(
            base_line,
            dot_a, dot_b, dot_b_prime, q_dot,
            moving_p,
            label_a, label_b, label_b_prime, label_p, q_label,
            connections,
            bq_dashed,
            title
        )

        # 添加公式标注
        formula = MathTex(r"|PA - PB| \leq AB'",
                         font_size=36,
                         color=YELLOW_D).to_edge(DOWN, buff=0.8)
        self.add(formula)

        # 往返动画
        self.play(
            moving_p.animate(rate_func=linear).move_to(base_line.get_end()),
            run_time=CONFIG["animation_duration"] / 2  # 去程3秒
        )
        self.play(
            moving_p.animate(rate_func=linear).move_to(base_line.get_start()),
            run_time=CONFIG["animation_duration"] / 2  # 返程3秒
        )
