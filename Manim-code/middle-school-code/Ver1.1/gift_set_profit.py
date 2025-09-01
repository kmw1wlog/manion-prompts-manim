from manim import *

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        for mob in mobjects:
            # simple guard: keep inside bounds
            center = mob.get_center()
            x_min, x_max = bounds.get_left()[0], bounds.get_right()[0]
            y_min, y_max = bounds.get_bottom()[1], bounds.get_top()[1]
            new_x = min(max(center[0], x_min), x_max)
            new_y = min(max(center[1], y_min), y_max)
            mob.move_to([new_x, new_y, 0])

class RollingBoard(VGroup):
    def __init__(self, width=4, line_height=0.6, max_lines=3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.line_height = line_height
        self.max_lines = max_lines
        self.lines = VGroup()

    def add_line(self, scene, tex):
        tex.scale_to_fit_width(self.width)
        self.lines.add(tex)
        scene.play(Write(tex), run_time=0.6)
        if len(self.lines) > self.max_lines:
            top_line = self.lines[0]
            scene.play(FadeOut(top_line), run_time=0.3)
            self.lines.remove(top_line)
        scene.play(self.lines.animate.arrange(DOWN, aligned_edge=LEFT, buff=0.2), run_time=0.2)


def reserve_panels(scene):
    W, H = config.frame_width, config.frame_height
    MARGIN = 0.06
    GAP = 0.04
    left_w = W * 0.55
    right_w = W * 0.45
    left_box = Rectangle(width=left_w, height=H*(1-2*MARGIN)).to_edge(LEFT, buff=W*MARGIN)
    right_box = Rectangle(width=right_w, height=H*(1-2*MARGIN)).to_edge(RIGHT, buff=W*MARGIN)
    return left_box, right_box


class GiftSetProfit(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        left_box.set_stroke(width=0)
        right_box.set_stroke(width=0)

        # left panel: simple number line showing cost and selling price
        number_line = NumberLine(x_range=[0, 8000, 1000], length=left_box.width*0.8)
        number_line.move_to(left_box.get_center())
        cost_dot = Dot(number_line.n2p(6000), color=BLUE)
        sell_dot = Dot(number_line.n2p(6600), color=GREEN)
        cost_label = MathTex("6000\\,원").scale(0.7).next_to(cost_dot, DOWN)
        sell_label = MathTex("6600\\,원").scale(0.7).next_to(sell_dot, DOWN)
        LayoutGuard.ensure_no_overlap(self, [number_line, cost_label, sell_label], left_box)
        self.play(Create(number_line))
        self.play(FadeIn(cost_dot), FadeIn(cost_label))
        self.play(FadeIn(sell_dot), FadeIn(sell_label))

        board = RollingBoard(width=right_box.width*0.9)

        # SEC_PROBLEM
        problem = MathTex(r"x\times1.2-600=x\times1.1")
        problem.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        board.add_line(self, problem)

        # SEC_GIVENS
        eq1 = MathTex(r"1.2x-600=1.1x")
        eq1.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [eq1], right_box)
        board.add_line(self, eq1)

        # SEC_WORK
        work1 = MathTex(r"0.1x=600")
        work1.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [work1], right_box)
        board.add_line(self, work1)
        work2 = MathTex(r"x=6000")
        work2.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [work2], right_box)
        board.add_line(self, work2)

        # SEC_RESULT
        result_box = SurroundingRectangle(work2, color=YELLOW)
        self.play(Create(result_box))
        self.wait(2)
