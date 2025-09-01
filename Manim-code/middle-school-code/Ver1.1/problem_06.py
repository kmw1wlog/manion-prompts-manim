from manim import *

# Utility functions from README
MARGIN = 0.06
GAP = 0.04
LEFT_RATIO = 0.55
RIGHT_RATIO = 0.45


def reserve_panels(scene: Scene, debug: bool = False):
    """Reserve left and right panels with fixed margins."""
    W, H = config.frame_width, config.frame_height
    left_w = (W - GAP) * LEFT_RATIO
    right_w = (W - GAP) * RIGHT_RATIO
    left_box = Rectangle(width=left_w, height=H * (1 - 2 * MARGIN)).to_edge(LEFT, buff=W * MARGIN)
    right_box = Rectangle(width=right_w, height=H * (1 - 2 * MARGIN)).to_edge(RIGHT, buff=W * MARGIN)
    if debug:
        for box, color in [(left_box, YELLOW), (right_box, BLUE)]:
            scene.add(box.set_stroke(color, 1).set_fill(opacity=0))
    return left_box, right_box


class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene: Scene, mobjects, bounds):
        for m in mobjects:
            m.scale_to_fit_width(bounds.width * 0.95)
            if m.get_left()[0] < bounds.get_left()[0]:
                m.shift(RIGHT * (bounds.get_left()[0] - m.get_left()[0]))
            if m.get_right()[0] > bounds.get_right()[0]:
                m.shift(LEFT * (m.get_right()[0] - bounds.get_right()[0]))


class RollingBoard(VGroup):
    def __init__(self, width: float, max_lines: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.lines = []

    def add_line(self, scene: Scene, mobj: Mobject):
        mobj.scale_to_fit_width(self.width * 0.9)
        if not self.lines:
            mobj.to_edge(UP, buff=0.1).align_to(self, LEFT)
        else:
            mobj.next_to(self.lines[-1], DOWN, aligned_edge=LEFT)
        self.add(mobj)
        self.lines.append(mobj)
        scene.play(Write(mobj), run_time=0.6)
        if len(self.lines) > self.max_lines:
            old = self.lines.pop(0)
            shift = old.height + 0.1
            scene.play(FadeOut(old), *[line.animate.shift(UP * shift) for line in self.lines])


class Problem06(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)

        # Left panel: number line with a dot for the number x
        number_line = NumberLine(x_range=[0, 10, 1], length=left_box.width * 0.9)
        number_line.move_to(left_box.get_center())
        x_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(number_line.n2p(x_tracker.get_value()), color=YELLOW))
        LayoutGuard.ensure_no_overlap(self, [number_line], left_box)
        self.play(Create(number_line))
        self.play(FadeIn(dot))

        # Right panel: rolling board for steps
        board = RollingBoard(width=right_box.width * 0.95, max_lines=3)

        # SEC_PROBLEM: display problem statement
        # (Problem text)
        prob_text = MathTex(r"x \times \frac{2}{5} = \frac{4}{3}")
        prob_text.move_to(right_box.get_left() + RIGHT * 0.2)
        LayoutGuard.ensure_no_overlap(self, [prob_text], right_box)
        board.add_line(self, prob_text)

        # SEC_GIVENS: solve for x from wrong operation
        x_equation = MathTex(r"x = \frac{\frac{4}{3}}{\frac{2}{5}} = \frac{10}{3}")
        x_equation.move_to(right_box.get_left() + RIGHT * 0.2)
        LayoutGuard.ensure_no_overlap(self, [x_equation], right_box)
        board.add_line(self, x_equation)
        self.play(x_tracker.animate.set_value(10/3))

        # SEC_WORK: compute correct result
        correct = MathTex(r"x \div \frac{2}{5} = \frac{25}{3}")
        correct.move_to(right_box.get_left() + RIGHT * 0.2)
        LayoutGuard.ensure_no_overlap(self, [correct], right_box)
        board.add_line(self, correct)

        # SEC_RESULT: final boxed answer in center
        answer = MathTex(r"\boxed{\frac{25}{3}}", color=GREEN)
        LayoutGuard.ensure_no_overlap(self, [answer], right_box)
        self.play(answer.animate.move_to(self.camera.frame_center))
        self.wait(1)


if __name__ == "__main__":
    scene = Problem06()
    scene.render()
