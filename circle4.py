from manim import *
import numpy as np


class HiddenCircleModel(Scene):
    def construct(self):
        # 标题配置（总1秒）
        title = Text("直径对直角", font_size=36).to_edge(UP)
        self.play(Write(title, run_time=0.8))
        self.wait(0.2)

        # 几何参数
        radius = 2.0
        target_ratio = 1
        L = 2 * radius * target_ratio

        # 创建几何元素
        O = Dot(ORIGIN, color=BLUE)
        A = Dot([-radius, 0, 0], color=RED)
        B = Dot([radius, 0, 0], color=RED)
        chord = Line(A, B, color=GREY, stroke_width=2)

        # 标签系统
        O_label = Tex("O", color=BLUE).next_to(O, UP, 0.2)
        A_label = Tex("A", color=RED).next_to(A, LEFT, 0.2)
        B_label = Tex("B", color=RED).next_to(B, RIGHT, 0.2)

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
            num_dashes=100,  # 减少虚线数量提升性能
            dashed_ratio=0.3,
            stroke_width=2.5
        )

        # 动态更新器
        PA.add_updater(lambda m: m.become(Line(P.get_center(), A.get_center(),
                                               color=YELLOW, stroke_width=3)))
        PB.add_updater(lambda m: m.become(Line(P.get_center(), B.get_center(),
                                               color=YELLOW, stroke_width=3)))

        # 正向动画：2秒完成圆周运动
        self.play(
            Rotate(P, 2 * PI, about_point=O.get_center(), rate_func=linear),
            Create(dashed_circle, rate_func=linear),
            run_time=2
        )

        # 逆向动画配置
        dash_offset_tracker = ValueTracker(-2 * PI * radius)
        circumference = 2 * PI * radius

        def update_dash(mob):
            mob.set_dash_offset(dash_offset_tracker.get_value())

        dashed_circle.add_updater(update_dash)

        # 文字提示
        theorem_text = Text(
            "根据圆周角定理，∠APB=90°",
            font_size=36,
            color=YELLOW
        ).to_edge(DOWN).shift(UP * 0.3)

        # 同步动画：3秒完成逆向运动+文字显示
        self.play(
            Rotate(P, -2 * PI, about_point=O.get_center(), rate_func=linear),
            dash_offset_tracker.animate.set_value(0),
            Write(theorem_text),
            run_time=3,
            rate_func=linear
        )


        # 清理阶段
        dashed_circle.remove_updater(update_dash)
        self.remove(dashed_circle)
