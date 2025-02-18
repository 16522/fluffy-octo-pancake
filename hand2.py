from manim import *


class CorrectTriangleRotation(Scene):
    def construct(self):
        # 场景配置
        B = np.array([0, -1, 0])  # 共同顶点B的位置
        main_arm_length = 2.5  # 主三角形腰长
        sub_arm_length = 1.2  # 子三角形腰长
        main_angle = 30  # 顶角角度

        # ===== 顶角角度计算 =====
        theta = np.radians(main_angle / 2)  # 顶角的一半（15度）
        base_angle = np.radians((180 - main_angle) / 2)  # 底角75度

        # ===== 主三角形ABC顶点计算 =====
        A = B + main_arm_length * np.array([-np.sin(theta), np.cos(theta), 0])
        C = B + main_arm_length * np.array([np.sin(theta), np.cos(theta), 0])

        # ===== 子三角形BDE顶点计算 =====
        D = B + sub_arm_length * np.array([-np.sin(theta), -np.cos(theta), 0])
        E = B + sub_arm_length * np.array([np.sin(theta), -np.cos(theta), 0])

        # 图形元素
        main_tri = Polygon(A, B, C, color=BLUE, stroke_width=4)
        sub_tri = Polygon(B, D, E, color=GREEN_B, stroke_width=4)

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
        center_text = Text("相似等腰三角形", font_size=36).to_edge(UP)
        math_text1 = Tex(r"$\angle ABE = \angle CBD$", color=YELLOW).scale(0.9)
        math_text2 = Tex(r"$\triangle ABE \cong \triangle CBD$", color=YELLOW).scale(0.9)
        math_group = VGroup(math_text1, math_text2) \
            .arrange(DOWN, buff=0.6) \
            .to_edge(DOWN, buff=0.8) \
            .shift(LEFT * 3)

        # 动画执行
        self.add(main_tri, sub_tri, fill_ABE, fill_CBD, labels)

        moving_group = Group(sub_tri, labels[3:5])
        fill_ABE.add_updater(lambda m: m.set_points_as_corners([A, B, sub_tri.get_vertices()[2]]))
        fill_CBD.add_updater(lambda m: m.set_points_as_corners([C, B, sub_tri.get_vertices()[1]]))

        self.play(
            Rotate(moving_group, 2 * PI, about_point=B, rate_func=linear, run_time=6),
            Succession(
                Write(center_text, run_time=2),
                AnimationGroup(
                    Write(math_text1),
                    Write(math_text2),
                    lag_ratio=0.33
                )
            ),
            run_time=6
        )

        # 保持最终画面
        self.add(center_text, math_group)
