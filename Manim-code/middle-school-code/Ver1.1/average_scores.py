from manim import *

# Forbidden tokens to ensure middle-school math scope
forbid_tokens = [
    "\\mathrm{i}", "\\sqrt{-", "sin", "cos", "tan", "미분", "적분", "행렬", "벡터", "복소수", "라디안"
]

def check_tokens(tex_string: str):
    for token in forbid_tokens:
        if token in tex_string:
            raise ValueError(f"Forbidden token detected: {token}")

class RollingBoard(VGroup):
    def __init__(self, width=4, max_lines=3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.lines = VGroup()

    def add_line(self, scene: Scene, mobj: Mobject, line_gap=0.2):
        check_tokens(mobj.tex_string if hasattr(mobj, "tex_string") else "")
        mobj.scale_to_fit_width(self.width)
        mobj.next_to(self.lines, DOWN, buff=line_gap) if len(self.lines) > 0 else mobj.move_to(ORIGIN)
        scene.add(mobj)
        self.lines.add(mobj)
        if len(self.lines) > self.max_lines:
            first = self.lines[0]
            scene.play(FadeOut(first, shift=UP))
            self.lines.remove(first)
            for line in self.lines:
                scene.play(line.animate.shift(UP))

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene: Scene, mobjects, bounds):
        for mobj in mobjects:
            if not bounds.get_bounding_box().contains(mobj.get_bounding_box()):
                mobj.shift(bounds.get_center() - mobj.get_center())

H, W = config.frame_height, config.frame_width
MARGIN = 0.06
PANEL_GAP = 0.04

def reserve_panels(scene: Scene):
    left_w = W * (0.55 - PANEL_GAP / 2)
    right_w = W * (0.45 - PANEL_GAP / 2)
    left_box = Rectangle(width=left_w, height=H * (1 - 2 * MARGIN)).to_edge(LEFT, buff=W * MARGIN)
    right_box = Rectangle(width=right_w, height=H * (1 - 2 * MARGIN)).to_edge(RIGHT, buff=W * MARGIN)
    return left_box, right_box

class AverageScoreScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)

        # SEC_PROBLEM
        problem = Text("40명 중 n명은 81점, 나머지는 70점", font_size=28)
        problem.move_to(right_box.get_top() + DOWN * 0.5)
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        self.play(Write(problem))

        # SEC_GIVENS
        board = RollingBoard(width=right_box.width * 0.95)
        eq1 = MathTex(r"\text{81점인 학생} = n")
        eq2 = MathTex(r"\text{70점인 학생} = 40 - n")
        for eq in [eq1, eq2]:
            eq.next_to(board.lines, DOWN) if len(board.lines) > 0 else eq.move_to(right_box.get_left() + RIGHT * 0.3 + DOWN * 1)
            LayoutGuard.ensure_no_overlap(self, [eq], right_box)
            self.play(Write(eq))
            board.add_line(self, eq)

        # Visual on left panel
        group81 = Rectangle(width=1.5, height=1, color=BLUE).move_to(left_box.get_center() + LEFT * 1)
        label81 = MathTex("n", color=BLUE).next_to(group81, UP, buff=0.1)
        group70 = Rectangle(width=1.5, height=1, color=RED).next_to(group81, RIGHT, buff=0.5)
        label70 = MathTex("40-n", color=RED).next_to(group70, UP, buff=0.1)
        LayoutGuard.ensure_no_overlap(self, [group81, label81, group70, label70], left_box)
        self.play(Create(group81), FadeIn(label81), Create(group70), FadeIn(label70))

        # SEC_WORK
        eq3 = MathTex(r"\text{평균} = \frac{81n + 70(40-n)}{40}")
        eq3.next_to(board.lines, DOWN)
        LayoutGuard.ensure_no_overlap(self, [eq3], right_box)
        self.play(Write(eq3))
        board.add_line(self, eq3)

        # SEC_RESULT
        result = MathTex(r"70 + \frac{11n}{40}")
        result.next_to(board.lines, DOWN)
        LayoutGuard.ensure_no_overlap(self, [result], right_box)
        box = SurroundingRectangle(result, color=YELLOW)
        self.play(Write(result))
        board.add_line(self, result)
        self.play(Create(box))
        self.wait()
