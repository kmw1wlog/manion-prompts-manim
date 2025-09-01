from manim import *

# Constants for layout
MARGIN = 0.06
GAP = 0.04
LEFT_RATIO = 0.55
RIGHT_RATIO = 0.45
DEBUG = False

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        for m in mobjects:
            # scale to fit width if needed
            if m.width > bounds.width:
                m.scale_to_fit_width(bounds.width * 0.9)
            # keep inside bounds
            if m.get_left()[0] < bounds.get_left()[0]:
                m.shift(RIGHT * (bounds.get_left()[0] - m.get_left()[0]))
            if m.get_right()[0] > bounds.get_right()[0]:
                m.shift(LEFT * (m.get_right()[0] - bounds.get_right()[0]))
            if m.get_top()[1] > bounds.get_top()[1]:
                m.shift(DOWN * (m.get_top()[1] - bounds.get_top()[1]))
            if m.get_bottom()[1] < bounds.get_bottom()[1]:
                m.shift(UP * (bounds.get_bottom()[1] - m.get_bottom()[1]))

class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_gap=0.15, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap
        self.lines = []

    def add_line(self, scene, mobj):
        mobj.scale_to_fit_width(self.width)
        if self.lines:
            lowest = self.lines[-1]
            mobj.next_to(lowest, DOWN, buff=self.line_gap).align_to(lowest, LEFT)
        else:
            mobj.to_edge(DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)
        self.lines.append(mobj)
        scene.add(mobj)
        if len(self.lines) > self.max_lines:
            top = self.lines.pop(0)
            scene.play(FadeOut(top, shift=UP*0.2), run_time=0.3)
            for k, line in enumerate(self.lines):
                if k == 0:
                    continue
                line.next_to(self.lines[k-1], UP, buff=self.line_gap).align_to(self.lines[k-1], LEFT)

def reserve_panels(scene):
    frame = scene.camera.frame
    W, H = frame.get_width(), frame.get_height()
    left_x = -W/2 + W*MARGIN
    right_x = W/2 - W*MARGIN
    inner_w = W*(1 - 2*MARGIN - GAP)
    left_w = inner_w * LEFT_RATIO
    right_w = inner_w * RIGHT_RATIO
    left_box = Rectangle(width=left_w, height=H*(1-2*MARGIN)).move_to(LEFT*(GAP/2*W) + LEFT*(right_w/2)).shift(RIGHT*(W*MARGIN))
    right_box = Rectangle(width=right_w, height=H*(1-2*MARGIN)).to_edge(RIGHT, buff=W*MARGIN)
    if DEBUG:
        for r, color in [(left_box, YELLOW), (right_box, BLUE)]:
            r.set_stroke(color, 1).set_fill(opacity=0)
            scene.add(r.copy())
    return left_box, right_box

# Problem specific values
A_VAL = 7.5
B_VAL = -2.5

class SolveOppositeSigns(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.95, max_lines=3)

        # SEC_PROBLEM
        prob = MathTex(r"|a|+|b|=10,\; |a|=3|b|", substrings_to_isolate=["a", "b"])
        prob.move_to(right_box.get_left() + RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [prob], right_box)
        self.play(Write(prob))
        board.add_line(self, prob)

        # SEC_GIVENS
        eq1 = MathTex(r"|a| = 3|b|")
        eq2 = MathTex(r"|a| + |b| = 10")
        for eq in [eq1, eq2]:
            eq.move_to(right_box.get_left() + RIGHT*0.2)
            LayoutGuard.ensure_no_overlap(self, [eq], right_box)
            self.play(Write(eq), run_time=0.6)
            board.add_line(self, eq)

        # SEC_WORK
        work1 = MathTex(r"3|b| + |b| = 10")
        work2 = MathTex(r"4|b| = 10")
        work3 = MathTex(r"|b| = 2.5,\; |a| = 7.5")
        for w in [work1, work2, work3]:
            w.move_to(right_box.get_left() + RIGHT*0.2)
            LayoutGuard.ensure_no_overlap(self, [w], right_box)
            self.play(Write(w), run_time=0.6)
            board.add_line(self, w)

        # Number line for visual on left
        axes = NumberLine(x_range=[-5,10,1], length=left_box.width*0.9)
        axes.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [axes], left_box)
        self.play(Create(axes))
        a_dot = Dot(color=YELLOW).move_to(axes.number_to_point(A_VAL))
        b_dot = Dot(color=BLUE).move_to(axes.number_to_point(B_VAL))
        a_label = MathTex('a').next_to(a_dot, UP)
        b_label = MathTex('b').next_to(b_dot, UP)
        for m in [a_label, b_label]:
            LayoutGuard.ensure_no_overlap(self, [m], left_box)
        self.play(FadeIn(a_dot), FadeIn(b_dot), FadeIn(a_label), FadeIn(b_label))

        # SEC_RESULT
        result = MathTex(r"a=7.5,\; b=-2.5")
        result_box = SurroundingRectangle(result, color=GREEN)
        group = VGroup(result, result_box)
        group.move_to(right_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [group], right_box)
        self.play(FadeIn(group))
        self.wait(2)
