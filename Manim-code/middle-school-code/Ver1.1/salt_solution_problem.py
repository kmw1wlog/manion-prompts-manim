from manim import *
import numpy as np

# Layout constants
MARGIN = 0.06
GAP = 0.04
LEFT_RATIO = 0.55
RIGHT_RATIO = 0.45
DEBUG = False

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, items, bounds_rect, min_scale=0.7, step_shift=0.15):
        # keep inside bounds
        for m in items:
            bbox = m.get_bounding_box()
            rbb = bounds_rect.get_bounding_box()
            dx, dy = 0, 0
            if bbox[0][0] < rbb[0][0]:
                dx = rbb[0][0] - bbox[0][0] + 0.02
            if bbox[2][0] > rbb[2][0]:
                dx = rbb[2][0] - bbox[2][0] - 0.02
            if bbox[0][1] < rbb[0][1]:
                dy = rbb[0][1] - bbox[0][1] + 0.02
            if bbox[2][1] > rbb[2][1]:
                dy = rbb[2][1] - bbox[2][1] - 0.02
            if dx or dy:
                m.shift(np.array([dx, dy, 0]))
        # pairwise overlap resolve
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
    left_box = Rectangle(width=left_w, height=H*(1-2*MARGIN)).move_to(
        LEFT*(GAP/2*W) + LEFT*(right_w/2)).shift(RIGHT*(W*MARGIN))
    right_box = Rectangle(width=right_w, height=H*(1-2*MARGIN)).to_edge(RIGHT, buff=W*MARGIN)
    if DEBUG:
        for r, color in [(left_box, YELLOW), (right_box, BLUE)]:
            r.set_stroke(color, 1).set_fill(opacity=0)
            scene.add(r.copy())
    return left_box, right_box

class SaltSolutionScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.95, max_lines=3)

        # SEC_PROBLEM
        beaker = Rectangle(width=left_box.width*0.4, height=left_box.height*0.6)
        beaker.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [beaker], left_box)
        self.play(Create(beaker))
        t_problem = Tex(r"200g, 10\% 소금물")
        t_problem.next_to(beaker, UP)
        LayoutGuard.ensure_no_overlap(self, [t_problem], left_box)
        self.play(Write(t_problem))

        p_text = Tex(r"먼저 x g을 빼내고 물을 채운다")
        p_text.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [p_text], right_box)
        self.play(Write(p_text))
        board.add_line(self, p_text)

        # SEC_GIVENS
        step1 = MathTex(r"\text{초기 소금} = 0.1\times200=20")
        step1.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [step1], right_box)
        self.play(Write(step1))
        board.add_line(self, step1)

        # SEC_WORK
        step2 = MathTex(r"\text{남은 소금} = 20-0.1x")
        step2.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [step2], right_box)
        self.play(Write(step2))
        board.add_line(self, step2)

        step3 = MathTex(r"(20-0.1x)+5 = 18")
        step3.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [step3], right_box)
        self.play(Write(step3))
        board.add_line(self, step3)

        step4 = MathTex(r"x = 70\,g")
        step4.move_to(right_box.get_left()+RIGHT*0.2)
        LayoutGuard.ensure_no_overlap(self, [step4], right_box)
        self.play(Write(step4))
        board.add_line(self, step4)

        # SEC_RESULT
        answer_box = SurroundingRectangle(step4, color=YELLOW)
        self.play(Create(answer_box))
        self.wait(1)
