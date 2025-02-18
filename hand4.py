from manim import *

class SquareRotationWithFill(Scene):
    def construct(self):
        # 场景配置
        B = ORIGIN
        square_size = 2.0
        sub_size = 1.2

        # 主正方形顶点
        A = B + LEFT * square_size
        C = B + UP * square_size
        F = A + UP * square_size

        # 子正方形顶点
        E = B + RIGHT * sub_size
        G = E + DOWN * sub_size
        D = B + DOWN * sub_size

        # 图形元素
        main_square = Polygon(A, B, C, F, color=BLUE, stroke_width=4)
        sub_square = Polygon(B, E, G, D, color=GREEN_B, stroke_width=4)

        # 填充区域
        fill_abe = Polygon(A, B, E, fill_opacity=0.4, fill_color=BLUE, stroke_width=0)
        fill_bdc = Polygon(B, D, C, fill_opacity=0.4, fill_color=YELLOW, stroke_width=0)

        # 顶点标签
        labels = VGroup(
            Tex("A").next_to(A, LEFT, 0.1),
            Tex("B").next_to(B, DOWN, 0.1),
            Tex("C").next_to(C, UP, 0.1),
            Tex("F").next_to(F, UL, 0.1),
            Tex("E").next_to(E, RIGHT, 0.1),
            Tex("G").next_to(G, DR, 0.1),
            Tex("D").next_to(D, DOWN, 0.1)
        )

        # 文字和公式元素
        title = Text("正方形", font_size=36).to_edge(UP)
        math_text1 = Tex(r"$\angle ABE = \angle CBD$", color=YELLOW).scale(0.9)
        math_text2 = Tex(r"$\triangle ABE \cong \triangle CBD$", color=YELLOW).scale(0.9)
        math_group = VGroup(math_text1, math_text2)\
            .arrange(DOWN, aligned_edge=LEFT, buff=0.6)\
            .to_edge(DL, buff=1.0)\
            .add_background_rectangle(opacity=0.8)

        # 动态元素
        moving_group = Group(sub_square, labels[4], labels[5], labels[6])
        moving_group.add_updater(lambda m: m.rotate(0.6 * DEGREES, about_point=B))  # 加速旋转

        # 动态更新填充区域
        fill_abe.add_updater(lambda m: m.set_points_as_corners([A, B, sub_square.get_vertices()[1]]))
        fill_bdc.add_updater(lambda m: m.set_points_as_corners([B, sub_square.get_vertices()[3], C]))

        # 添加所有元素到场景
        self.add(main_square, sub_square, labels, fill_abe, fill_bdc)

        # 动画序列（总时长6秒）
        self.play(
            Rotate(moving_group, angle=360*DEGREES, about_point=B, run_time=6, rate_func=linear),
            Succession(
                Write(title, run_time=1.5),
                AnimationGroup(
                    Write(math_text1, run_time=1.0),
                    Write(math_text2, run_time=1.0),
                    lag_ratio=0.4
                ),
                lag_ratio=0.6
            ),
        )
