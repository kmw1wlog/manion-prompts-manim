from manim import *

# Helper classes from README guidelines
class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        # basic check to keep mobjects within bounds
        for m in mobjects:
            bbox = m.get_bounding_box()
            box = bounds.get_bounding_box()
            shift_vec = [0,0,0]
            if bbox[0][0] < box[0][0]:
                shift_vec[0] = box[0][0] - bbox[0][0]
            if bbox[2][0] > box[2][0]:
                shift_vec[0] = box[2][0] - bbox[2][0]
            if bbox[0][1] < box[0][1]:
                shift_vec[1] = box[0][1] - bbox[0][1]
            if bbox[2][1] > box[2][1]:
                shift_vec[1] = box[2][1] - bbox[2][1]
            if shift_vec != [0,0,0]:
                m.shift(shift_vec)

class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_gap=0.4, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap

    def add_line(self, scene, mobj):
        mobj.scale_to_fit_width(self.width)
        if len(self.submobjects) == 0:
            mobj.to_edge(UP)
        else:
            last = self.submobjects[-1]
            mobj.next_to(last, DOWN, buff=self.line_gap)
        self.add(mobj)
        if len(self.submobjects) > self.max_lines:
            first = self.submobjects.pop(0)
            scene.play(FadeOut(first, shift=UP))
            for line in self.submobjects:
                scene.play(line.animate.shift(UP*(mobj.height + self.line_gap)), run_time=0.2)


def reserve_panels(scene, left_ratio=0.55):
    W,H = config.frame_width, config.frame_height
    MARGIN = 0.06
    GAP = 0.04
    left_w = W*left_ratio - GAP/2
    right_w = W*(1-left_ratio) - GAP/2
    left_box = Rectangle(width=left_w, height=H*(1-2*MARGIN)).to_edge(LEFT, buff=W*MARGIN)
    right_box = Rectangle(width=right_w, height=H*(1-2*MARGIN)).to_edge(RIGHT, buff=W*MARGIN)
    return left_box, right_box


class DistanceSpeedTimeScene(Scene):
    def construct(self):
        # Reserve panels
        left_box, right_box = reserve_panels(self)

        # Left panel graphic: line from A to B labeled with distance d
        line = Line(left_box.get_left() + RIGHT*0.5, left_box.get_right() - RIGHT*0.5)
        A = Dot(line.get_start())
        B = Dot(line.get_end())
        label_A = MathTex('A').next_to(A, DOWN)
        label_B = MathTex('B').next_to(B, DOWN)
        d_label = MathTex('d\\,\\text{km}').next_to(line, UP)
        left_group = VGroup(line, A, B, label_A, label_B, d_label)
        LayoutGuard.ensure_no_overlap(self, left_group, left_box)
        self.play(Create(line), FadeIn(A), FadeIn(B), Write(label_A), Write(label_B), Write(d_label))

        # Right panel rolling board
        board = RollingBoard(width=right_box.width*0.95, max_lines=3)
        board.move_to(right_box.get_center())
        self.add(board)

        # SEC_PROBLEM
        problem = MathTex(r"\text{성호 }12\text{km/h, 지호 }4\text{km/h}")
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        self.play(Write(problem))
        board.add_line(self, problem)

        # SEC_GIVENS
        given1 = MathTex(r"t_S = \frac{d}{12}")
        given2 = MathTex(r"t_J = \frac{d}{4}")
        given3 = MathTex(r"t_J - t_S = \frac{20}{60}")
        for g in [given1, given2, given3]:
            LayoutGuard.ensure_no_overlap(self, [g], right_box)
            self.play(Write(g))
            board.add_line(self, g)

        # SEC_WORK
        eq1 = MathTex(r"\frac{d}{4} - \frac{d}{12} = \frac{1}{3}")
        eq2 = MathTex(r"\frac{d}{6} = \frac{1}{3}")
        eq3 = MathTex(r"d = 2")
        for e in [eq1, eq2, eq3]:
            LayoutGuard.ensure_no_overlap(self, [e], right_box)
            self.play(Write(e))
            board.add_line(self, e)

        # update left panel label
        final_label = MathTex('2\\,\\text{km}').next_to(line, UP)
        LayoutGuard.ensure_no_overlap(self, [final_label], left_box)
        self.play(TransformMatchingTex(d_label, final_label))

        # SEC_RESULT
        result = MathTex(r"AB = 2\,\text{km}")
        LayoutGuard.ensure_no_overlap(self, [result], right_box)
        self.play(Write(result), Indicate(final_label))
        board.add_line(self, result)
        self.wait()
