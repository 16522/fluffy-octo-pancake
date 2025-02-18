from manim import *


class ColoredGeometricRotation(Scene):
    def construct(self):
        # 位移配置
        shift_vector = LEFT * 1 + DOWN * 1

        # 主三角形配置
        main_length = 3.5
        A = LEFT * (main_length / 2) + shift_vector
        B = RIGHT * (main_length / 2) + shift_vector
        C = UP * (np.sqrt(3) / 2 * main_length) + shift_vector

        # 子三角形配置
        sub_length = 2.2
        D = B + RIGHT * sub_length
        E = B + RIGHT * (sub_length / 2) + UP * (np.sqrt(3) / 2 * sub_length)

        # 图形元素
        main_tri = Polygon(A, B, C, color=BLUE, stroke_width=4)
        sub_tri = Polygon(B, D, E, color=GREEN_B, stroke_width=4)

        # 填充区域
        fill_ABE = Polygon(A, B, E,
                           fill_color=BLUE,
                           fill_opacity=0.45,
                           stroke_width=0)
        fill_CBD = Polygon(C, B, D,
                           fill_color=YELLOW,
                           fill_opacity=0.4,
                           stroke_width=0)

        # 顶点标签
        labels = VGroup(
            Tex("A").scale(0.8).next_to(A, DL, buff=0.1),
            Tex("B").scale(0.8).next_to(B, DR, buff=0.1),
            Tex("C").scale(0.8).next_to(C, UP, buff=0.15),
            Tex("D").scale(0.7).next_to(D, RIGHT, buff=0.1),
            Tex("E").scale(0.7).next_to(E, UR, buff=0.1)
        )

        # 文字元素
        center_text = Text("正三角形", font_size=48, color=WHITE).move_to(ORIGIN + UP * 3)

        # 数学公式
        math_text1 = Tex(r"$\angle ABE = \angle CBD$",
                         color=YELLOW).scale(0.9)
        math_text2 = Tex(r"$\triangle ABE \cong \triangle CBD$",
                         color=YELLOW).scale(0.9)
        math_group = VGroup(math_text1, math_text2) \
            .arrange(DOWN, buff=0.6) \
            .to_edge(DOWN, buff=0.8) \
            .shift(LEFT * 3)  # 新增左移1.2单位

        # 添加基本元素
        self.add(main_tri, sub_tri, fill_ABE, fill_CBD, labels)

        # 动画配置
        moving_group = Group(sub_tri, labels[3:5])
        fill_ABE.add_updater(lambda m: m.set_points_as_corners([A, B, sub_tri.get_vertices()[2]]))
        fill_CBD.add_updater(lambda m: m.set_points_as_corners([C, B, sub_tri.get_vertices()[1]]))

        # 执行复合动画
        self.play(
            Rotate(
                moving_group,
                angle=2 * PI,
                about_point=B,
                rate_func=linear,
                run_time=6
            ),
            Succession(
                # 第一阶段：3秒完成正三角形文字
                Write(center_text, run_time=3),
                # 第二阶段：显示数学公式
                AnimationGroup(
                    Write(math_text1),
                    Write(math_text2),
                    lag_ratio=0.3
                )
            )
        )

        # 确保所有元素保持显示
        self.add(center_text, math_group
