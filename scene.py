from manim import *

class GraphLinearFunction(Scene):
    def construct(self):
        # 设置坐标轴，确保 x 和 y 的单位长度相同
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            axis_config={"color": BLUE},
            x_length=6,  # 设置 x 轴的长度
            y_length=6   # 设置 y 轴的长度，确保单位长度一致
        )

        # 绘制 y = kx + b 的图像，假设 k = 1, b = 1
        k = 1
        b = 1
        graph = axes.plot(lambda x: k * x + b, color=WHITE)

        # 将图像向右下方移动
        graph.shift(RIGHT * 0.5 + DOWN * 1)  # 调整图像位置

        # 标注 y = kx + b
        graph_label = axes.get_graph_label(graph, label='y = kx + b')

        # 将标签向下移动
        graph_label.shift(DOWN * 0.75)  # 调整标签位置，确保标签可见

        # 创建坐标轴标签
        axes_labels = axes.get_axis_labels(x_label='x', y_label='y')

        # 添加说明文字
        description = Text("1.当k>0时，y随x的增大而增大", font_size=24)
        description.next_to(axes, LEFT, buff=1)  # 将文字放在坐标轴左侧
        description.shift(RIGHT * 1.4 + UP * 3)  # 向右移动并适当调整文字的位置

        # 绘制第一个图像和文字
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), Write(graph_label))
        self.play(Write(description))  # 显示说明文字

        # 等待2秒钟后清空当前内容
        self.wait(2)
        self.play(Uncreate(graph), Uncreate(graph_label), Uncreate(description))  # 清空图像和文字

        # 绘制第二个图像，假设 k = -1, b = 1
        k = -1
        graph = axes.plot(lambda x: k * x + b, color=WHITE)
        
        # 将图像向右下方移动
        graph.shift(RIGHT * 0.5 + DOWN * 1)  # 调整图像位置

        # 标注 y = kx
        graph_label = axes.get_graph_label(graph, label='y = kx + b')
        
        # 将标签向左移动
        graph_label.shift(LEFT * 0)  # 向左移动2单位

        # 更新说明文字
        description = Text("2.当k<0时，y随x的增大而减小", font_size=24)
        description.next_to(axes, LEFT, buff=1)  # 将文字放在坐标轴左侧
        description.shift(RIGHT * 1.4 + UP * 3)  # 向右移动并调整文字位置

        # 绘制第二个图像和文字
        self.play(Create(graph), Write(graph_label))
        self.play(Write(description))  # 显示新的说明文字

        # 等待2秒钟后清空当前内容
        self.wait(2)
        self.play(Uncreate(graph), Uncreate(graph_label), Uncreate(description))  # 清空图像和文字

        # 绘制第三个图像，假设 b = 0，k = 1
        k = 1
        b = 0
        graph = axes.plot(lambda x: k * x + b, color=WHITE)

        # 标注 y = kx
        graph_label = axes.get_graph_label(graph, label='y = kx')

        # 将标签向左移动
        graph_label.shift(LEFT * 2)  # 向左移动2单位

        # 更新说明文字
        description = Text("3当b=0时，y=kx (k≠0)", font_size=24)
        description.next_to(axes, LEFT, buff=1)  # 将文字放在坐标轴左侧
        description.shift(RIGHT * 0.3 + UP * 3)  # 向右移动并调整文字位置

        # 绘制第三个图像和文字
        self.play(Create(graph), Write(graph_label))
        self.play(Write(description))  # 显示新的说明文字
        self.wait(2)  # 等待2秒钟，让文字能显示出来
