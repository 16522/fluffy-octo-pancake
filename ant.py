from manim import *

class EllipticalCylinderUnfold(Scene):
    def construct(self):
        # Step 1: 添加标题和副标题
        title = Text("最短路径问题", font_size=36, color=WHITE).to_edge(UP)
        title_box = RoundedRectangle(
            width=title.width + 0.5,
            height=title.height + 0.3,
            corner_radius=0.2,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.5
        ).move_to(title.get_center())
        subtitle = Text(
            "在底面半径为 r, 高为 h 的圆柱中，求蚂蚁沿点 P 沿圆柱表面爬行到点 Q 的最短路径",
            font_size=24,
            color=WHITE
        ).next_to(title_box, DOWN)

        self.play(FadeIn(title_box), Write(title))
        self.play(Write(subtitle))
        self.wait(1)

        # Step 2: 绘制圆柱底部椭圆
        bottom_ellipse = Ellipse(width=2, height=1.5, color=WHITE)
        bottom_ellipse.shift(DOWN + LEFT * 4)

        # Step 3: 绘制圆柱顶部椭圆
        top_ellipse = Ellipse(width=2, height=1.5, color=WHITE)
        top_ellipse.shift(UP + LEFT * 4)

        # Step 4: 绘制连接椭圆的母线
        left_line = Line(start=bottom_ellipse.get_left(), end=top_ellipse.get_left(), color=WHITE)
        right_line = Line(start=bottom_ellipse.get_right(), end=top_ellipse.get_right(), color=WHITE)

        # 添加标签和标注
        point_p = Dot(point=bottom_ellipse.get_right(), color=YELLOW)
        label_p = MathTex("P", font_size=30).next_to(point_p, RIGHT)

        point_q = Dot(point=top_ellipse.get_right(), color=YELLOW)
        label_q = MathTex("Q", font_size=30).next_to(point_q, RIGHT)

        radius_label = MathTex("r", font_size=30).next_to(bottom_ellipse.get_right(), DOWN)
        radius_line = DashedLine(start=bottom_ellipse.get_center(), end=bottom_ellipse.get_right(), color=WHITE)

        height_label = MathTex("h", font_size=30).next_to(left_line, LEFT)

        # 组合圆柱相关元素
        cylinder = VGroup(bottom_ellipse, top_ellipse, left_line, right_line,
                          point_p, label_p, point_q, label_q,
                          radius_label, radius_line, height_label)

        # Step 5: 绘制展开后的矩形
        unfolded_rectangle = Rectangle(width=2 * PI, height=2, color=WHITE)
        unfolded_rectangle.move_to(RIGHT * 3)

        # 绘制对角线（最短路径）
        shortest_path = Line(
            start=unfolded_rectangle.get_corner(UL),
            end=unfolded_rectangle.get_corner(DR),
            color=YELLOW,
            stroke_width=4
        )

        # 添加展开后的标签
        rectangle_p = Dot(point=unfolded_rectangle.get_corner(UL), color=YELLOW)
        rectangle_label_p = MathTex("P", font_size=30).next_to(rectangle_p, LEFT)

        rectangle_q = Dot(point=unfolded_rectangle.get_corner(DR), color=YELLOW)
        rectangle_label_q = MathTex("Q", font_size=30).next_to(rectangle_q, RIGHT)

        rectangle_radius = MathTex(r"2\pi r", font_size=30).next_to(unfolded_rectangle.get_top(), UP)
        rectangle_height = MathTex(r"h", font_size=30).next_to(unfolded_rectangle.get_left(), LEFT)

        unfolded_group = VGroup(unfolded_rectangle, shortest_path,
                                rectangle_p, rectangle_label_p,
                                rectangle_q, rectangle_label_q,
                                rectangle_radius, rectangle_height)

        # 添加箭头标注
        arrow = Arrow(LEFT, RIGHT, buff=0.1, color=WHITE).move_to(ORIGIN + LEFT * 1.5)
        arrow_label = Text("展开后", font_size=24, color=WHITE).next_to(arrow, UP)

        # Step 6: 创建动画序列
        self.play(Create(bottom_ellipse, run_time=1))
        self.play(Create(top_ellipse, run_time=1))
        self.play(Create(left_line), Create(right_line))
        self.play(Create(point_p), Write(label_p))
        self.play(Create(point_q), Write(label_q))
        self.play(Write(radius_label), Create(radius_line), Write(height_label))

        # 显示展开箭头
        self.play(FadeIn(arrow), Write(arrow_label))

        #Step 7: Create arc for P to midpoint of left line (arc downwards)
        left_line_midpoint = left_line.get_center()  # Get midpoint of left line
        arc_1 = ArcBetweenPoints(start=point_p.get_center(), end=left_line_midpoint, radius=-2, color=YELLOW)
        self.play(Create(arc_1))  # Arc for P to midpoint, downward curve

        # Step 8: Create arc for midpoint to Q (arc upwards)
        # 使用负半径确保弧线向上弯曲
        arc_2 = ArcBetweenPoints(start=left_line_midpoint, end=point_q.get_center(), radius=-2, color=YELLOW)
        self.play(Create(arc_2))  # 弧线向上弯曲




        # Step 9: 显示展开后的矩形
        self.play(Create(unfolded_rectangle))
        self.wait(1)
        self.play(Create(shortest_path))
        self.play(Create(rectangle_p), Write(rectangle_label_p))
        self.play(Create(rectangle_q), Write(rectangle_label_q))
        self.play(Write(rectangle_radius), Write(rectangle_height))

        # Step 10: 添加公式说明
        explanation_text = Text(
            "最短路径: ",
            font_size=36,
            color=WHITE
        ).next_to(unfolded_rectangle, DOWN, aligned_edge=LEFT)

        formula = MathTex(
            r"\sqrt{(2\pi r)^2 + h^2}",
            font_size=36,
            color=WHITE
        ).next_to(explanation_text, RIGHT)

        self.play(Write(explanation_text), Write(formula))
        self.wait(2)

