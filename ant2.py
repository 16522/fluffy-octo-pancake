from manim import *

class EllipticalCylinderUnfold(Scene):
    def construct(self):
        # Step 1: Add title with a yellow rounded rectangle as background
        title = Text("最短路径问题", font_size=36, color=WHITE).to_edge(UP)
        title_box = RoundedRectangle(
            width=title.width + 0.5,  # Add padding to the box
            height=title.height + 0.3,
            corner_radius=0.2,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.5
        ).move_to(title.get_center())  # Align the box to the title
        subtitle = Text(
            "在底面半径为 r, 高为 h 的圆柱中，求蚂蚁沿点 P 沿圆柱表面螺旋爬行到点 Q 的最短路径",
            font_size=24,
            color=WHITE
        ).next_to(title_box, DOWN)

        self.play(FadeIn(title_box), Write(title))
        self.play(Write(subtitle))
        self.wait(1)

        # Step 2: Draw the bottom ellipse (base of the cylinder)
        bottom_ellipse = Ellipse(width=2, height=1.5, color=WHITE)
        bottom_ellipse.shift(DOWN + LEFT * 4)  # Move ellipse further to the left

        # Step 3: Draw the top ellipse (top of the cylinder)
        top_ellipse = Ellipse(width=2, height=1.5, color=WHITE)
        top_ellipse.shift(UP + LEFT * 4)  # Move ellipse further to the left

        # Step 4: Draw two parallel lines connecting the ellipses
        left_line = Line(start=bottom_ellipse.get_left(), end=top_ellipse.get_left(), color=WHITE)
        right_line = Line(start=bottom_ellipse.get_right(), end=top_ellipse.get_right(), color=WHITE)

        # Add labels for points P and Q, radius r, and height h
        point_p = Dot(point=bottom_ellipse.get_left(), color=YELLOW)  # Point P at the bottom-left corner
        label_p = MathTex("P", font_size=30).next_to(point_p, LEFT)

        point_q = Dot(point=top_ellipse.get_right(), color=YELLOW)  # Point Q at the top-right corner
        label_q = MathTex("Q", font_size=30).next_to(point_q, RIGHT)

        radius_label = MathTex("r", font_size=30).next_to(bottom_ellipse.get_right(), DOWN).shift(
            LEFT * 0.3)  # Move left
        radius_line = DashedLine(start=bottom_ellipse.get_center(), end=bottom_ellipse.get_right(), color=WHITE)

        height_label = MathTex("h", font_size=30).next_to(left_line, LEFT)

        # Group the cylinder parts
        cylinder = VGroup(bottom_ellipse, top_ellipse, left_line, right_line, point_p, label_p, point_q, label_q, radius_label, radius_line, height_label)

        # Step 5: Draw the unfolded rectangle
        unfolded_rectangle = Rectangle(width=PI, height=2, color=WHITE)
        unfolded_rectangle.move_to(RIGHT * 3)  # Move rectangle to the right

        # Add points P and Q
        rectangle_p = Dot(point=unfolded_rectangle.get_corner(LEFT + DOWN), color=YELLOW)  # Point P at the bottom-left corner
        rectangle_label_p = MathTex("P", font_size=30).next_to(rectangle_p, LEFT)

        # Point Q is at the rightmost point of the top edge
        rectangle_q = Dot(point=unfolded_rectangle.get_edge_center(UP),
                          color=YELLOW)  # Point Q at the midpoint of the top edge
        rectangle_label_q = MathTex("Q", font_size=30).next_to(rectangle_q, UP)

        # Draw the line connecting P and Q (diagonal line)
        shortest_path = Line(start=rectangle_p.get_center(), end=rectangle_q.get_center(), color=YELLOW, stroke_width=4)

        # Draw the vertical line through Q to the bottom edge
        vertical_line = Line(start=rectangle_q.get_center(), end=unfolded_rectangle.get_bottom(), color=WHITE)

        # Label πr at the midpoint of the bottom edge, center it below the long edge
        rectangle_radius = MathTex(r"\pi r", font_size=30).next_to(unfolded_rectangle.get_bottom(), DOWN, aligned_edge=RIGHT)

        # Move h label downward slightly
        height_label = MathTex("h", font_size=30).next_to(rectangle_q, RIGHT).shift(DOWN * 0.5)  # Shift it downward

        # Create arc for the path from P to Q along the surface of the cylinder
        arc_path = ArcBetweenPoints(start=point_p.get_center(), end=point_q.get_center(), radius=2, color=YELLOW)

        # Group all the elements
        unfolded_group = VGroup(
            unfolded_rectangle,
            rectangle_p, rectangle_label_p,
            rectangle_q, rectangle_label_q,
            shortest_path, vertical_line,
            rectangle_radius, height_label, arc_path
        )

        # Add arrow and label for "展开后"
        arrow = Arrow(LEFT, RIGHT, buff=0.1, color=WHITE).move_to(ORIGIN + LEFT * 1)  # Move arrow further left
        arrow_label = Text("展开后", font_size=24, color=WHITE).next_to(arrow, UP).shift(LEFT * 0)  # Move left


        # Step 6: Create animations
        self.play(Create(bottom_ellipse, run_time=1))  # Faster bottom ellipse drawing
        self.play(Create(top_ellipse, run_time=1))  # Faster top ellipse drawing
        self.play(Create(left_line), Create(right_line))
        self.play(Create(point_p), Write(label_p))
        self.play(Create(point_q), Write(label_q))
        self.play(Write(radius_label), Create(radius_line), Write(height_label))

        # Add arrow animation
        self.play(FadeIn(arrow), Write(arrow_label))

        # **Step before showing unfolded rectangle, add arc animation**
        self.play(Create(arc_path))  # Arc animation comes **before** unfolded rectangle

        # Show unfolded rectangle
        self.play(Create(unfolded_rectangle))
        self.wait(1)
        self.play(Create(shortest_path))
        self.play(Create(rectangle_p), Write(rectangle_label_p))
        self.play(Create(rectangle_q), Write(rectangle_label_q))
        self.play(Write(rectangle_radius), Write(height_label))

        # Add vertical line animation
        self.play(Create(vertical_line))

        # Step 7: Add explanatory text for shortest path
        explanation_text = Text(
            "最短路径: ",
            font_size=36,
            color=WHITE
        ).next_to(unfolded_rectangle, DOWN, aligned_edge=LEFT).shift(DOWN * 0.5)  # Move downward slightly

        formula = MathTex(
            r"\sqrt{(\pi r)^2 + h^2}",
            font_size=36,
            color=WHITE
        ).next_to(explanation_text, RIGHT)

        self.play(Write(explanation_text), Write(formula))
        self.wait(2)
