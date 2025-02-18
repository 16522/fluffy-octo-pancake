from manim import *


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
        label_P = Tex("P").next_to(P, RIGHT)

        # 3. 实时更新的半径
        radius = always_redraw(lambda: Line(O, P, color=YELLOW))

        # 4. 动态虚线圆周
        def update_arc(arc):
            angle = angle_of_vector(P.get_center() - O.get_center())
            adjusted_angle = angle if angle >= 0 else TAU + angle
            new_arc = Arc(
                radius=2,
                start_angle=0,
                angle=adjusted_angle,
                color=GREEN
            )
            arc.become(DashedVMobject(new_arc, num_dashes=20))

        dynamic_arc = Arc(radius=2, start_angle=0, angle=0, color=GREEN)
        dashed_arc = DashedVMobject(dynamic_arc, num_dashes=20)
        dashed_arc.add_updater(update_arc)

        # 动画序列
        self.play(Create(O), Write(label_O))
        self.play(
            Create(radius),
            Create(P),
            Write(label_P),
            run_time=1.5
        )
        self.add(dashed_arc)

        # 5. 组合动画（正放+倒放）
        label_P.add_updater(lambda m: m.next_to(P, RIGHT))

        # 正向旋转
        self.play(
            Rotate(P,
                   angle=TAU,
                   about_point=O.get_center(),
                   rate_func=smooth
                   ),
            run_time=4
        )
        # 倒放旋转
        self.play(
            Rotate(P,
                   angle=TAU,
                   about_point=O.get_center(),
                   rate_func=lambda t: smooth(1 - t)  # 反转速率函数
                   ),
            run_time=4
        )
