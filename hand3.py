from manim import *


class RightAngleTriangleRotation(Scene):
    def construct(self):
        B = np.array([0, 0, 0])  # 修改位置到画面中心 ★ 将Y坐标从-1改为0
        main_arm_length = 2.5
        sub_arm_length = 1.5
        main_angle = 90

        # ===== 顶角角度计算 =====
        theta = np.radians(main_angle / 2)
        base_angle = np.radians((180 - main_angle) / 2)

        # ===== 顶点计算（保持相对位置不变）=====
        A = B + main_arm_length * np.array([-np.sin(theta), np.cos(theta), 0])
        C = B + main_arm_length * np.array([np.sin(theta), np.cos(theta), 0])
        D = B + sub_arm_length * np.array([-np.sin(theta), -np.cos(theta), 0])
        E = B + sub_arm_length * np.array([np.sin(theta), -np.cos(theta), 0])

        # 图形元素
        main_tri = Polygon(A, B, C, color=BLUE, stroke_width=4)
        sub_tri = Polygon(B, D, E, color=GREEN_B, stroke_width=4)

        # 添加直角标记
        right_angle_main = RightAngle(Line(B, A), Line(B, C), length=0.3, color=RED)
        right_angle_sub = RightAngle(Line(B, D), Line(B, E), length=0.2, color=RED)

        # 填充区域
        fill_ABE = Polygon(A, B, E, fill_opacity=0.4, fill_color=BLUE, stroke_width=0)
        fill_CBD = Polygon(C, B, D, fill_opacity=0.4, fill_color=YELLOW, stroke_width=0)

        # 顶点标签
        labels = VGroup(
            Tex("A").next_to(A, UP + LEFT, 0.1),
            Tex("B").next_to(B, DOWN, 0.1),
            Tex("C").next_to(C, UP + RIGHT, 0.1),
            Tex("D").next_to(D, DOWN + LEFT, 0.1),
            Tex("E").next_to(E, DOWN + RIGHT, 0.1)
        )

        # 文字和公式元素
        center_text = Text("等腰直角三角形旋转", font_size=36).to_edge(UP)
        math_text1 = Tex(r"$\angle ABE = \angle CBD$", color=YELLOW).scale(0.9)
        math_text2 = Tex(r"$\triangle ABE \cong \triangle CBD$", color=YELLOW).scale(0.9)
        math_group = VGroup(math_text1, math_text2) \
            .arrange(DOWN, buff=0.6) \
            .to_edge(DOWN, buff=0.8) \
            .shift(LEFT * 3)

        # 动画执行
        self.add(main_tri, sub_tri, fill_ABE, fill_CBD, labels, right_angle_main, right_angle_sub)

        moving_group = Group(sub_tri, labels[3:5], right_angle_sub)
        fill_ABE.add_updater(lambda m: m.set_points_as_corners([A, B, sub_tri.get_vertices()[2]]))
        fill_CBD.add_updater(lambda m: m.set_points_as_corners([C, B, sub_tri.get_vertices()[1]]))

        self.play(
            Rotate(moving_group, 2 * PI, about_point=B, rate_func=linear, run_time=6),
            Succession(
                Write(center_text, run_time=2),
                AnimationGroup(
                    Write(math_text1),
                    Write(math_text2),
                    lag_ratio=0.3
                )
            ),
            run_time=6
        )

        # 保持最终画面
        self.add(center_text, math_group)
