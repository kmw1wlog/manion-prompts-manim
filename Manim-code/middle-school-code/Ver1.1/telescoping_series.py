from manim import *

# Layout constants
LEFT_RATIO = 0.55
RIGHT_RATIO = 0.45
MARGIN = 0.06
GAP = 0.04
DEBUG = False


class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, items, bounds_rect, min_scale=0.7, step_shift=0.15):
        """Basic overlap and bounds checking."""
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
        # Greedy pairwise overlap resolution
        def overlap(a, b):
            Ab, Bb = a.get_bounding_box(), b.get_bounding_box()
            return not (Ab[2][0] < Bb[0][0] or Bb[2][0] < Ab[0][0] or
                        Ab[2][1] < Bb[0][1] or Bb[2][1] < Ab[0][1])
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                tries = 0
                while overlap(a, b) and tries < 6:
                    for m in (a, b):
                        if m.width > bounds_rect.width * 0.9 and m.get_scale() > min_scale:
                            m.scale(0.9)
                    b.shift(RIGHT * step_shift + DOWN * step_shift)
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
            scene.play(FadeOut(top, shift=UP * 0.2), run_time=0.3)
            for k, line in enumerate(self.lines):
                if k == 0:
                    continue
                line.next_to(self.lines[k - 1], UP, buff=self.line_gap).align_to(self.lines[k - 1], LEFT)


def reserve_panels(scene):
    frame = scene.camera.frame
    W, H = frame.get_width(), frame.get_height()
    left_x = -W / 2 + W * MARGIN
    right_x = W / 2 - W * MARGIN
    inner_w = W * (1 - 2 * MARGIN - GAP)
    left_w = inner_w * LEFT_RATIO
    right_w = inner_w * RIGHT_RATIO
    left_box = Rectangle(width=left_w, height=H * (1 - 2 * MARGIN)).move_to(
        LEFT * (GAP / 2 * W) + LEFT * (right_w / 2)
    ).shift(RIGHT * (W * MARGIN))
    right_box = Rectangle(width=right_w, height=H * (1 - 2 * MARGIN)).to_edge(RIGHT, buff=W * MARGIN)
    if DEBUG:
        for r, color in [(left_box, YELLOW), (right_box, BLUE)]:
            r.set_stroke(color, 1).set_fill(opacity=0)
            scene.add(r.copy())
    return left_box, right_box


class TelescopingSeriesScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width * 0.95, max_lines=3)

        # SEC_PROBLEM
        problem = MathTex(
            r"\frac1{1\cdot2} + \frac1{2\cdot3} + \cdots + \frac1{9\cdot10}",
            font_size=32,
        )
        problem.move_to(right_box.get_top() + DOWN * 0.5)
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        self.play(Write(problem))
        board.add_line(self, problem)

        # SEC_GIVENS
        prop = MathTex(r"\frac1{n(n+1)} = \frac1n - \frac1{n+1}")
        prop.next_to(problem, DOWN, aligned_edge=LEFT, buff=0.3)
        LayoutGuard.ensure_no_overlap(self, [prop], right_box)
        self.play(Write(prop))
        board.add_line(self, prop)

        # SEC_WORK
        telescoped = MathTex(r"1 - \frac1{10}")
        telescoped.next_to(prop, DOWN, aligned_edge=LEFT, buff=0.3)
        LayoutGuard.ensure_no_overlap(self, [telescoped], right_box)
        self.play(TransformMatchingTex(prop.copy(), telescoped))
        board.add_line(self, telescoped)

        series = MathTex(
            r"\left(1-\frac12\right)+\left(\frac12-\frac13\right)+\cdots+\left(\frac19-\frac1{10}\right)",
            font_size=32,
        )
        series.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [series], left_box)
        self.play(Write(series))

        # SEC_RESULT
        result = MathTex(r"\frac9{10}")
        result_box = SurroundingRectangle(result, color=YELLOW)
        group = VGroup(result, result_box)
        group.move_to(right_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [group], right_box)
        self.play(Write(result), Create(result_box))
        self.wait()
