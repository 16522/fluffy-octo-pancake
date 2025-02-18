from manim import *
import numpy as np


class HiddenCircleModel(Scene):
    def construct(self):
        # 1. 标题动画
        title = Text("定点定长", font="SimHei", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. 创建基本元素
        O = Dot(ORIGIN, color=BLUE)
        label_O = Tex("O").next_to(O, DOWN)
        P = Dot(RIGHT * 2, color=RED)

        # P点标签配置
        label_P = Tex("P").add_updater(
            lambda m: m.next_to(
                P,
                direction=normalize(P.get_center() - O.get_center()) if np.linalg.norm(
                    P.get_center() - O.get_center()) > 0 else RIGHT,
                buff=0.3
            )
        )

        # 3. 动态元素配置
        radius = always_redraw(lambda: Line(O, P, color=YELLOW))

        # 4. 动态虚线圆弧
        dynamic_arc = Arc(radius=2, start_angle=0, angle=0, color=GREEN)
        dashed_arc = DashedVMobject(dynamic_arc, num_dashes=40)

        # 5. Q点配置
        def get_q_position():
            op_vector = P.get_center() - O.get_center()
            midpoint = O.get_center() + op_vector * 0.5
            if np.linalg.norm(op_vector) > 0:
                perp_vector = np.array([-op_vector[1], op_vector[0], 0])
                perp_unit = perp_vector / np.linalg.norm(perp_vector)
            else:
                perp_unit = np.zeros(3)
            return midpoint + perp_unit * 0.6

        Q = Dot(color=PURPLE).add_updater(lambda m: m.move_to(get_q_position()))
        label_Q = Tex("Q").add_updater(lambda m: m.next_to(Q, LEFT, buff=0.15))

        # 6. 连接线配置
        connections = VGroup(
            always_redraw(lambda: DashedLine(O, Q, color=BLUE, dash_length=0.1)),
            always_redraw(lambda: DashedLine(P, Q, color=RED, dash_length=0.1))
        )

        # 7. 动画序列
        self.play(
            Create(O),
            Write(label_O),
            Create(P),
            Write(label_P),
            run_time=1.5
        )

        self.add(radius, connections, Q, label_Q)

        # 动态圆弧更新器
        dashed_arc.add_updater(
            lambda m: m.become(DashedVMobject(
                Arc(
                    radius=2,
                    start_angle=0,
                    angle=(np.arctan2(P.get_center()[1], P.get_center()[0]) + 2 * PI) % (2 * PI),
                    color=GREEN
                ),
                num_dashes=40
            ))
        )
        self.add(dashed_arc)

        # 8. 组合动画（正放+倒放）
        # 创建正放动画
        forward_anim = Rotate(
            P,
            angle=2 * PI,
            about_point=O.get_center(),
            rate_func=linear,
            run_time=3
        )

        # 创建倒放动画
        reverse_anim = Rotate(
            P,
            angle=-2 * PI,
            about_point=O.get_center(),
            rate_func=linear,
            run_time=3
        )

        # 执行组合动画
        self.play(forward_anim, UpdateFromFunc(dashed_arc, lambda m: m))
        self.play(reverse_anim, UpdateFromFunc(dashed_arc, lambda m: m))
