from manim import *
import numpy as np

class HiddenCircleModel(Scene):
    def construct(self):
        # 标题配置
        title = Text("同弦等角", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 几何参数
        radius = 2.0
        target_ratio = 6 / 7
        L = 2 * radius * target_ratio
        h = np.sqrt(radius ** 2 - (L / 2) ** 2)
        theta = 2 * np.arcsin(L / (2 * radius))  # 计算圆心角

        # 创建几何元素
        O = Dot(ORIGIN, color=BLUE)
        A = Dot([-L / 2, -h, 0], color=RED)  # 下方弦端点
        B = Dot([L / 2, -h, 0], color=RED)
        chord = Line(A, B, color=GREY, stroke_width=2)

        # 动态点初始化（上方对称点）
        P = Dot([-L / 2, h, 0], color=GREEN)
        Q = Dot([L / 2, h, 0], color=YELLOW)
        labels = VGroup(
            Tex("O", color=BLUE).next_to(O, UP, 0.1),
            Tex("A", color=RED).next_to(A, DOWN, 0.1),
            Tex("B", color=RED).next_to(B, DOWN, 0.1),
            Tex("P", color=GREEN).add_updater(lambda m: m.next_to(P, UP, 0.1)),
            Tex("Q", color=YELLOW).add_updater(lambda m: m.next_to(Q, UP, 0.1))
        )

        # 连接线配置
        lines = VGroup(
            Line(P, A, color=YELLOW, stroke_width=3),
            Line(P, B, color=YELLOW, stroke_width=3),
            Line(Q, A, color=PURPLE, stroke_width=3),
            Line(Q, B, color=PURPLE, stroke_width=3)
        )

        # 虚线圆
        dashed_circle = DashedVMobject(
            Circle(radius=radius, color=WHITE),
            num_dashes=100,
            dashed_ratio=0.3
        )

        # 添加所有元素
        self.add(O, A, B, chord, dashed_circle, P, Q, labels, lines)

        # 更新器函数
        def update_lines():
            for i, (start, end) in enumerate([(P, A), (P, B), (Q, A), (Q, B)]):
                lines[i].become(Line(start.get_center(), end.get_center(),
                                     color=lines[i].get_color(),
                                     stroke_width=3))

        # 添加持续更新
        lines.add_updater(lambda _: update_lines())

        # 文字提示配置
        theorem_text = Text(
            "∠AQB=∠APB，四点共圆",
            font_size=36,
            color=YELLOW,
            font="SimHei"
        ).to_edge(DOWN).shift(UP * 0.3)

        # 合并动画序列
        self.play(
            Rotate(P, -theta, about_point=O.get_center(), rate_func=linear),
            Rotate(Q, theta, about_point=O.get_center(), rate_func=linear),
            run_time=3
        )
        self.play(
            Rotate(P, theta, about_point=O.get_center(), rate_func=linear),
            Rotate(Q, -theta, about_point=O.get_center(), rate_func=linear),
            Write(theorem_text, rate_func=linear),  # 同步写入文字
            run_time=3
        )

        # 在动画结束时统一清理更新器
        lines.remove_updater(update_lines)
