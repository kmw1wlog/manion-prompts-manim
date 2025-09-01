from manim import *

# Helper classes from README (simplified)
class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        pass

class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_spacing=0.3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_spacing = line_spacing

    def add_line(self, scene, mobj):
        mobj.scale_to_fit_width(self.width)
        mobj.next_to(self, DOWN, buff=self.line_spacing) if len(self) else mobj.move_to(ORIGIN)
        if len(self) == self.max_lines:
            top = self[0]
            scene.play(FadeOut(top, shift=UP))
            self.remove(top)
            for line in self:
                scene.play(line.animate.shift(UP*(mobj.height + self.line_spacing)))
        self.add(mobj)
        scene.play(Write(mobj))

# Reserve panels
LEFT_RATIO = 0.55
RIGHT_RATIO = 0.45
MARGIN = 0.06
GAP = 0.04


def reserve_panels(scene):
    W, H = config.frame_width, config.frame_height
    left_w = W * LEFT_RATIO
    right_w = W * RIGHT_RATIO
    left_box = Rectangle(width=left_w, height=H*(1-2*MARGIN)).to_edge(LEFT, buff=W*MARGIN)
    right_box = Rectangle(width=right_w, height=H*(1-2*MARGIN)).to_edge(RIGHT, buff=W*MARGIN)
    return left_box, right_box


class MatchstickSquares(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.9)
        board.move_to(right_box.get_center())
        self.add(board)

        # SEC_PROBLEM
        title = Text("문제")
        title.to_edge(UP)
        self.play(FadeIn(title))
        prob = MathTex(r"n\text{개의 정사각형을 나란히 만들 때}", r"\text{필요한 성냥개의 수}")
        prob.scale(0.8)
        prob.next_to(title, DOWN)
        self.play(Write(prob))

        # Draw squares for n=1..3
        start = left_box.get_left() + RIGHT*0.5*1 + DOWN*0.5
        squares = VGroup()
        size = 1
        for i in range(3):
            sq = Square(side_length=size)
            sq.shift(start + RIGHT*i*size)
            squares.add(sq)
        LayoutGuard.ensure_no_overlap(self, [squares], left_box)
        self.play(Create(squares[0]))
        self.play(TransformFromCopy(squares[0], squares[1]))
        self.play(TransformFromCopy(squares[1], squares[2]))

        # SEC_GIVENS
        self.wait(0.5)
        line1 = MathTex(r"1\text{개}:4,\;2\text{개}:7,\;3\text{개}:10")
        board.add_line(self, line1)

        # SEC_WORK
        self.wait(0.5)
        formula = MathTex(r"\text{성냥개비 수} = 3n + 1")
        board.add_line(self, formula)
        self.play(Circumscribe(formula))

        # SEC_RESULT
        result_box = SurroundingRectangle(formula, color=YELLOW)
        self.play(Create(result_box))
        self.wait(2)

