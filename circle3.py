from manim import *
import numpy as np


class HiddenCircleModel(Scene):
    def construct(self):
        # 标题配置
        title = Text("定弦定角", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 精确几何参数
        radius = 2.0
        target_ratio = 6 / 7
        L = 2 * radius * target_ratio

        h = np.sqrt(radius ** 2 - (L / 2) ** 2)
        x = L / 2

        # 创建几何元素
        O = Dot(ORIGIN, color=BLUE)
        A = Dot([-x, -h, 0], color=RED)
        B = Dot([x, -h, 0], color=RED)
        chord = Line(A, B, color=GREY, stroke_width=2)

        # 标签系统
        O_label = Tex("O", color=BLUE).next_to(O, UP, 0.2)
        A_label = Tex("A", color=RED).next_to(A, DOWN, 0.2)
        B_label = Tex("B", color=RED).next_to(B, DOWN, 0.2)

        # 动态点P配置
        P = Dot([radius, 0, 0], color=GREEN)
        P_label = Tex("P", color=GREEN).next_to(P, UR, 0.2)
        P_label.add_updater(lambda m: m.next_to(P, UR, 0.2))

        # 连接线
        PA = Line(P, A, color=YELLOW, stroke_width=3)
        PB = Line(P, B, color=YELLOW, stroke_width=3)

        self.add(O, A, B, chord, PA, PB, O_label, A_label, B_label, P, P_label)

        # 高精度虚线圆
        dashed_circle = DashedVMobject(
            Circle(radius=radius, color=WHITE),
            num_dashes=150,
            dashed_ratio=0.2,
            stroke_width=2.5
        )

        # 动态更新器
        PA.add_updater(lambda m: m.become(Line(P.get_center(), A.get_center(),
                                               color=YELLOW, stroke_width=3)))
        PB.add_updater(lambda m: m.become(Line(P.get_center(), B.get_center(),
                                               color=YELLOW, stroke_width=3)))

        # 正向动画（逆时针绘制）
        self.play(
            Rotate(P, 2 * PI, about_point=O.get_center(), rate_func=linear),
            Create(dashed_circle, rate_func=linear),
            run_time=3.5
        )

        # 逆向动画（顺时针擦除）最终修正版
        dash_offset_tracker = ValueTracker(-2 * PI * radius)  # 初始偏移-4π
        circumference = 2 * PI * radius

        def update_dash(mob):
            mob.set_dash_offset(dash_offset_tracker.get_value())

        dashed_circle.add_updater(update_dash)

        self.play(
            Rotate(P, -2 * PI, about_point=O.get_center(), rate_func=linear),
            dash_offset_tracker.animate.set_value(0),  # 从-4π到0线性变化
            run_time=3.5
        )

        dashed_circle.remove_updater(update_dash)
        self.remove(dashed_circle)
