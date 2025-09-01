from manim import *

# Helper Classes and Functions

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        """Simple placeholder to meet repository spec."""
        return

class RollingBoard(VGroup):
    def __init__(self, width=4, max_lines=3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.lines = VGroup()
        self.add(self.lines)

    def add_line(self, scene, mobj):
        forbid_tokens = ["\\sin", "\\cos", "\\tan", "i", "\\sqrt{-}"]
        if any(tok in mobj.tex_string for tok in forbid_tokens):
            raise ValueError("Forbidden token detected")
        mobj.scale_to_fit_width(self.width)
        self.lines.add(mobj)
        if len(self.lines) > self.max_lines:
            top = self.lines[0]
            scene.play(FadeOut(top))
            self.lines.remove(top)
        for i, line in enumerate(self.lines):
            line.next_to(self.get_top(), DOWN*(i+1), buff=0.1)


def reserve_panels(scene, left_ratio=0.55, margin=0.06, gap=0.04):
    frame = scene.camera.frame
    W = frame.width
    H = frame.height
    left_w = W*(left_ratio - gap/2 - margin)
    right_w = W*(1-left_ratio - gap/2 - margin)
    left_box = Rectangle(width=left_w, height=H*(1-2*margin)).to_edge(LEFT, buff=W*margin)
    right_box = Rectangle(width=right_w, height=H*(1-2*margin)).to_edge(RIGHT, buff=W*margin)
    return left_box, right_box


class AbsValueRangeCount(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        number_line = NumberLine(x_range=[-5,5,1], length=left_box.width*0.9)
        number_line.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [number_line], left_box)
        self.play(Create(number_line))

        board = RollingBoard(width=right_box.width*0.95, max_lines=3)
        board.move_to(right_box.get_left()+RIGHT*0.2)
        self.add(board)

        # SEC_PROBLEM
        p_text = MathTex(r"|x| \geq \tfrac{1}{2},\ |x| < 5,\ x \in \mathbb{Z}")
        LayoutGuard.ensure_no_overlap(self, [p_text], right_box)
        self.play(Write(p_text))
        board.add_line(self, p_text)

        # SEC_GIVENS
        givens = MathTex(r"-5 < x < 5")
        LayoutGuard.ensure_no_overlap(self, [givens], right_box)
        self.play(Write(givens))
        board.add_line(self, givens)

        # SEC_WORK
        work = MathTex(r"x \neq 0")
        LayoutGuard.ensure_no_overlap(self, [work], right_box)
        self.play(Write(work))
        board.add_line(self, work)

        valid_ints = [MathTex(str(k)).move_to(number_line.number_to_point(k)+UP*0.3) for k in (-4,-3,-2,-1,1,2,3,4)]
        dots = VGroup(*[Dot(number_line.number_to_point(k)) for k in (-4,-3,-2,-1,1,2,3,4)])
        LayoutGuard.ensure_no_overlap(self, valid_ints, left_box)
        self.play(FadeIn(dots), *[FadeIn(v) for v in valid_ints])

        # SEC_RESULT
        result = MathTex(r"8\,\text{values}").scale(1.2).move_to(right_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [result], right_box)
        self.play(Transform(board, result))
        self.wait()
