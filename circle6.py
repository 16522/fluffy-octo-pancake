from manim import *
import numpy as np


class FourPointCircle(Scene):
    def construct(self):
        # 1. 标题动画
        title = Text("对角互补", font="SimHei", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. 创建基本元素
        circle = Circle(radius=2, color=WHITE).shift(UP * 0.5)
        O = Dot(ORIGIN + UP * 0.5, color=YELLOW)
        label_O = Tex("O", color=YELLOW).next_to(O, DOWN, buff=0.2)

        # 点位置参数
        angles = {
            "A": 130 * DEGREES,
            "B": 210 * DEGREES,
            "C": 20 * DEGREES,
            "D": 330 * DEGREES
        }

        points = {
            "A": Dot(color=BLUE).move_to(circle.point_at_angle(angles["A"])),
            "B": Dot(color=BLUE).move_to(circle.point_at_angle(angles["B"])),
            "C": Dot(color=RED).move_to(circle.point_at_angle(angles["C"])),
            "D": Dot(color=RED).move_to(circle.point_at_angle(angles["D"]))
        }

        # 3. 动态移动控制
        phase_tracker = ValueTracker(0)

        def update_point_positions(mob, point_name):
            base_angle = angles[point_name]
            if point_name in ["A", "B"]:
                delta = 8 * np.sin(1 * phase_tracker.get_value()) * DEGREES
            else:
                delta = 6 * np.sin(1 * phase_tracker.get_value() + PI / 2) * DEGREES
            new_angle = base_angle + delta
            mob.move_to(circle.point_at_angle(new_angle))

        for name in points:
            points[name].add_updater(lambda m, n=name: update_point_positions(m, n))

        # 4. 标签配置
        labels = VGroup(
            Tex("A", color=BLUE).add_updater(
                lambda m: m.move_to(
                    points["A"].get_center() + normalize(points["A"].get_center() - O.get_center()) * 0.7)),
            Tex("B", color=BLUE).add_updater(
                lambda m: m.move_to(
                    points["B"].get_center() + normalize(points["B"].get_center() - O.get_center()) * 0.7)),
            Tex("C", color=RED).add_updater(lambda m: m.next_to(points["C"], UR, buff=0.2)),
            Tex("D", color=RED).add_updater(lambda m: m.next_to(points["D"], DR, buff=0.2))
        )

        # 5. 连接线
        lines = VGroup(
            always_redraw(lambda: Line(points["A"], points["B"], color=GREEN_B)),
            always_redraw(lambda: Line(points["B"], points["D"], color=BLUE_B)),
            always_redraw(lambda: Line(points["C"], points["D"], color=RED_B)),
            always_redraw(lambda: Line(points["A"], points["C"], color=YELLOW_B))
        )

        # 6. 添加说明文字
        equation = Text(
            "∠A + ∠D = ∠B + ∠C",
            font="SimHei",
            font_size=32,
            color=YELLOW
        )
        conclusion = Text(
            "四点共圆",
            font="SimHei",
            font_size=32,
            color=YELLOW
        )

        # 调整文字布局
        text_group = VGroup(equation, conclusion).arrange(DOWN, buff=0.5)
        text_group.next_to(circle, DOWN, buff=1)

        # 添加所有元素
        self.add(circle, O, label_O, *points.values(), labels, lines)

        # 7. 同步动画（关键修改部分）
        self.play(
            phase_tracker.animate.set_value(2 * PI),
            Write(text_group),
            run_time=5,
            rate_func=linear
        )
