from manim import *


class FinalWithQMarker(Scene):
    def construct(self):
        OFFSET = DOWN * 1.5
        LEFT_BASE = LEFT * 3 + OFFSET

        # 创建坐标系
        horizontal = Line(LEFT_BASE, LEFT_BASE + RIGHT * 6, stroke_width=3)
        diagonal = Line(
            start=LEFT_BASE,
            end=LEFT_BASE + 6 * (np.cos(30 * DEGREES) * RIGHT + np.sin(30 * DEGREES) * UP),
            stroke_width=3
        )

        # 标题部分
        title = Text("一定两动",
                     font_size=36,
                     color=GOLD,
                     font="Source Han Sans CN"
                     ).to_edge(UP, buff=0.6)
        title.add_background_rectangle(
            color=BLACK,
            opacity=0.8,
            buff=0.3
        )

        # A点位置
        A = Dot(
            diagonal.get_start() + UP * 2.5 + RIGHT * 2.0,
            color=GREEN,
            radius=0.1
        )
        A_label = Text("A", font_size=24, color=GREEN).next_to(A, UR * 0.3)

        # 计算垂足点
        foot_point = np.array([A.get_center()[0], horizontal.get_start()[1], 0])

        # 虚线垂线
        vertical_line = DashedLine(
            A.get_center(), foot_point,
            color=GREEN,
            stroke_width=2.5,
            dash_length=0.1
        )

        # 直角标记
        right_angle = VGroup(
            Line(foot_point, foot_point + UR * 0.15, color=GREEN, stroke_width=3),
            Line(foot_point + RIGHT * 0.15, foot_point + UR * 0.15, color=GREEN, stroke_width=3),
            Line(foot_point + UP * 0.15, foot_point + UR * 0.15, color=GREEN, stroke_width=3)
        )

        # Q点标签
        Q_label = Text("Q", font_size=24, color=GREEN).next_to(foot_point, DOWN * 0.3)

        # 点P系统
        P_tracker = ValueTracker(0.0)
        P = always_redraw(lambda: Dot(
            diagonal.point_from_proportion(P_tracker.get_value()),
            color=GREEN,
            radius=0.08
        ))
        P_label = always_redraw(lambda: Text("P", font_size=24, color=GREEN)
                                .next_to(P, UP * 0.3 + RIGHT * 0.3))

        # 点Q'系统
        Q_prime = always_redraw(lambda: Dot(
            horizontal.point_from_proportion(1 - P_tracker.get_value()),
            color=GREEN,
            radius=0.08
        ))
        Q_prime_label = always_redraw(lambda: Text("Q'", font_size=24, color=GREEN)
                                      .next_to(Q_prime, DOWN * 0.3))

        # 连线系统
        AP_line = always_redraw(lambda: Line(
            A.get_center(), P.get_center(),
            color=GREEN,
            stroke_width=4
        ))
        PQ_line = always_redraw(lambda: Line(
            P.get_center(), Q_prime.get_center(),
            color=GREEN,
            stroke_width=3
        ))

        # 添加不等式公式（关键修改点）
        formula = MathTex(r"AP + PQ' \geq AQ",
                          font_size=36,
                          color=YELLOW_D).to_edge(DOWN, buff=0.8)

        # 添加所有元素
        self.add(title, horizontal, diagonal)
        self.add(A, P, Q_prime, AP_line, PQ_line,
                 vertical_line, right_angle, Q_label,
                 A_label, P_label, Q_prime_label, formula)

        # 修改后的动画设置（总时长6秒）
        self.play(
            P_tracker.animate.set_value(1).set_rate_func(linear),
            run_time=3  # 从3秒缩短到2.5秒
        )
        self.play(
            P_tracker.animate.set_value(0).set_rate_func(linear),
            run_time=3  # 从3秒缩短到2.5秒
        )

