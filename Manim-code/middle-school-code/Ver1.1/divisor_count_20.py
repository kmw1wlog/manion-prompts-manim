from manim import *
import numpy as np

# layout constants
LEFT_RATIO = 0.55
RIGHT_RATIO = 0.45
MARGIN = 0.06
GAP = 0.04
DEBUG = False

# forbidden tokens for middle-school scope
forbid_tokens = ["\\sin", "\\cos", "\\tan", "\\mathrm{i}", "i", "\\sqrt{-}", "복소수", "라디안", "행렬", "벡터", "미분", "적분"]

def safe_MathTex(tex: str) -> MathTex:
    for token in forbid_tokens:
        if token in tex:
            raise ValueError(f"Forbidden token {token} found in {tex}")
    return MathTex(tex)

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, items, bounds_rect, min_scale=0.7, step_shift=0.15):
        for m in items:
            bbox = m.get_bounding_box()
            rbb = bounds_rect.get_bounding_box()
            dx, dy = 0, 0
            if bbox[0][0] < rbb[0][0]: dx = rbb[0][0] - bbox[0][0] + 0.02
            if bbox[2][0] > rbb[2][0]: dx = rbb[2][0] - bbox[2][0] - 0.02
            if bbox[0][1] < rbb[0][1]: dy = rbb[0][1] - bbox[0][1] + 0.02
            if bbox[2][1] > rbb[2][1]: dy = rbb[2][1] - bbox[2][1] - 0.02
            if dx or dy:
                m.shift(np.array([dx, dy, 0]))
        def overlap(a, b):
            Ab, Bb = a.get_bounding_box(), b.get_bounding_box()
            return not (Ab[2][0] < Bb[0][0] or Bb[2][0] < Ab[0][0] or
                        Ab[2][1] < Bb[0][1] or Bb[2][1] < Ab[0][1])
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                a, b = items[i], items[j]
                tries = 0
                while overlap(a, b) and tries < 6:
                    for m in (a, b):
                        if m.width > bounds_rect.width * 0.9 and m.get_scale() > min_scale:
                            m.scale(0.9)
                    b.shift(RIGHT*step_shift + DOWN*step_shift)
                    tries += 1

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

class DivisorCountScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.95, max_lines=3)

        # SEC_PROBLEM
        problem = safe_MathTex(r"2\times5^n\text{ 의 약수의 개수가 }20\text{개일 때 }n\text{은?}")
        problem.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        self.play(Write(problem))
        board.add_line(self, problem)

        left_expr = safe_MathTex(r"2\times5^n")
        left_expr.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [left_expr], left_box)
        self.play(Write(left_expr))

        # SEC_GIVENS
        factor_right = safe_MathTex(r"2\times5^n = 2^1\times5^n")
        factor_right.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [factor_right], right_box)
        self.play(Write(factor_right))
        board.add_line(self, factor_right)

        factor_left = safe_MathTex(r"2^1\times5^n")
        factor_left.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [factor_left], left_box)
        self.play(TransformMatchingTex(left_expr, factor_left))

        # SEC_WORK
        formula = safe_MathTex(r"(1+1)(n+1)=20")
        formula.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [formula], right_box)
        self.play(Write(formula))
        board.add_line(self, formula)

        eq_n1 = safe_MathTex(r"n+1=10")
        eq_n1.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [eq_n1], right_box)
        self.play(Write(eq_n1))
        board.add_line(self, eq_n1)

        eq_n = safe_MathTex(r"n=9")
        eq_n.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [eq_n], right_box)
        self.play(Write(eq_n))
        board.add_line(self, eq_n)

        check = safe_MathTex(r"(1+1)(9+1)=20")
        check.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [check], right_box)
        self.play(Write(check))
        board.add_line(self, check)

        # SEC_RESULT
        self.play(*[FadeOut(m) for m in board.lines], FadeOut(factor_left))
        result = safe_MathTex(r"n=9").scale(1.5)
        box = SurroundingRectangle(result, color=YELLOW)
        LayoutGuard.ensure_no_overlap(self, [result], self.camera.frame)
        self.play(Write(result))
        self.play(Create(box))
        self.wait()
