from manim import *


class GeometryScene(Scene):
    def construct(self):
        # 1. 标题文字（28号字保持居中）
        title = Text("如图：若有PM⊥AB于M，则作PN⊥BC于N，可得到△BMP≌△BNP",
                     font="SimHei", font_size=28)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)

        # 2. 定义隐形区域
        area_a = Polygon([-6, 2.5, 0], [0, 2.5, 0], [0, -3.5, 0], [-6, -3.5, 0],
                         stroke_opacity=0, fill_opacity=0)
        area_b = Polygon([1, 2.5, 0], [6, 2.5, 0], [6, -3.5, 0], [1, -3.5, 0],
                         stroke_opacity=0, fill_opacity=0)
        self.add(area_a, area_b)

        # 3-4. 精确几何构造
        vertical_line = Line([-3, 1, 0], [-3, -3, 0],
                             color=WHITE, stroke_width=4)  # 4单位竖线
        B_point = vertical_line.get_end() + [0, 4, 0]  # 精确顶点定位

        # 构造40度斜边（长度=4/√2）
        angle = 40 * DEGREES
        ab_vec = 4 / np.sqrt(2) * np.array([-np.cos(angle), -np.sin(angle), 0])
        bc_vec = 4 / np.sqrt(2) * np.array([np.cos(angle), -np.sin(angle), 0])
        AB = Line(B_point, B_point + ab_vec, color=WHITE)
        BC = Line(B_point, B_point + bc_vec, color=WHITE)

        # 5-6. 虚线垂线构造
        def safe_ortho_project(point, line):
            start, end = line.get_start_and_end()
            vec = end - start
            t = np.dot(point - start, vec) / np.dot(vec, vec)
            return start + np.clip(t, 0.15, 0.85) * vec  # 15%安全边界

        P_point = vertical_line.point_from_proportion(0.666)  # 精确2/3处
        M_point = safe_ortho_project(P_point, AB)
        N_point = safe_ortho_project(P_point, BC)

        # 构造虚线元素
        PM = DashedLine(P_point, M_point, color=WHITE, dash_length=0.15)
        PN = DashedLine(P_point, N_point, color=GREEN, dash_length=0.15)
        PM_perp = RightAngle(PM, AB, length=0.2, color=WHITE, quadrant=(-1, 1))
        PN_perp = RightAngle(PN, BC, length=0.2, color=GREEN, quadrant=(-1, -1))

        # 标签组（优化布局）
        labels = VGroup(
            Tex("B").scale(0.8).next_to(B_point, UP, buff=0.15),
            Tex("A").scale(0.8).next_to(AB.get_end(), LEFT, buff=0.15),
            Tex("C").scale(0.8).next_to(BC.get_end(), RIGHT, buff=0.15),
            Tex("P").scale(0.8).next_to(P_point, RIGHT, buff=0.15),
            Tex("M").scale(0.8).next_to(M_point, LEFT, buff=0.15),
            Tex("N").scale(0.8).next_to(N_point, RIGHT, buff=0.15)
        )

        # 9. 区域B口诀（24号字）
        slogan_text = ["口诀：", "角平分线垂两边", "全等△必出现"]
        slogan = VGroup(*[
            Text(t, font="SimHei", color=ORANGE, font_size=28)
                        .set_max_width(area_b.width - 1.2)
            for t in slogan_text
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        slogan.move_to(area_b.get_center() + [0.4, 0, 0])  # 精确居中

        # 动画流程优化
        self.play(
            Create(vertical_line),
            Create(AB),
            Create(BC),
            run_time=2
        )
        self.play(LaggedStart(
            FadeIn(labels[0], shift=DOWN * 0.2),
            FadeIn(labels[1], shift=RIGHT * 0.2),
            FadeIn(labels[2], shift=LEFT * 0.2),
            lag_ratio=0.3
        ))
        self.play(
            GrowFromCenter(Dot(P_point)),
            Write(labels[3]),
            run_time=1.5
        )
        self.play(
            Create(PM),
            GrowFromCenter(Dot(M_point)),
            Write(labels[4]),
            Create(PM_perp),
            run_time=2
        )
        self.play(
            Create(PN),
            GrowFromCenter(Dot(N_point)),
            Write(labels[5]),
            Create(PN_perp),
            run_time=2
        )
        self.play(
            slogan.animate.shift(LEFT * 0.15),
            run_time=1.5
        )
        self.wait(2)
