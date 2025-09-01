from manim import *

# Helper classes from README
class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        for m in mobjects:
            # Ensure object fits within bounds
            if m.width > bounds.width * 0.95:
                m.scale_to_fit_width(bounds.width * 0.95)
            if m.height > bounds.height * 0.95:
                m.scale_to_fit_height(bounds.height * 0.95)
            # Keep inside bounds
            m.move_to(bounds.get_center())

class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_gap=0.2, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap
        self.lines = VGroup()
        self.add(self.lines)

    def add_line(self, scene, line_mob):
        line_mob.scale_to_fit_width(self.width)
        if len(self.lines) >= self.max_lines:
            top = self.lines[0]
            scene.play(FadeOut(top))
            self.lines.remove(top)
            for l in self.lines:
                scene.play(l.animate.shift(UP*(top.height + self.line_gap)), run_time=0.3)
        if self.lines:
            line_mob.next_to(self.lines[-1], DOWN, aligned_edge=LEFT, buff=self.line_gap)
        else:
            line_mob.to_edge(UP, buff=0)
        scene.play(Write(line_mob), run_time=0.7)
        self.lines.add(line_mob)


def reserve_panels(scene, margin=0.06, gap=0.04, left_ratio=0.55):
    W, H = config.frame_width, config.frame_height
    left_w = (W - 2*W*margin - W*gap)*left_ratio
    right_w = (W - 2*W*margin - W*gap)*(1-left_ratio)
    left_box = Rectangle(width=left_w, height=H*(1-2*margin)).to_edge(LEFT, buff=W*margin)
    right_box = Rectangle(width=right_w, height=H*(1-2*margin)).to_edge(RIGHT, buff=W*margin)
    return left_box, right_box


class PencilDistributionScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)

        board = RollingBoard(width=right_box.width*0.95, max_lines=3)
        board.move_to(right_box.get_top() + DOWN*0.5)

        LayoutGuard.ensure_no_overlap(self, [board], right_box)
        self.add(board)

        # SEC_PROBLEM
        problem_text = Tex(
            "한 학생에게 5자루씩 주면 10자루가 남고, 6자루씩 주면 5자루가 부족합니다.",
            tex_environment="flushleft"
        ).scale(0.6)
        problem_text.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [problem_text], left_box)
        self.play(Write(problem_text))

        # SEC_GIVENS
        e1 = MathTex(r"y = 5x + 10")
        e2 = MathTex(r"y = 6x - 5")
        for e in [e1, e2]:
            LayoutGuard.ensure_no_overlap(self, [e], right_box)
            board.add_line(self, e)

        # SEC_WORK
        eq = MathTex(r"5x + 10 = 6x - 5")
        LayoutGuard.ensure_no_overlap(self, [eq], right_box)
        board.add_line(self, eq)

        solve_x = MathTex(r"x = 15")
        LayoutGuard.ensure_no_overlap(self, [solve_x], right_box)
        board.add_line(self, solve_x)

        compute_y = MathTex(r"y = 5x + 10 = 85")
        LayoutGuard.ensure_no_overlap(self, [compute_y], right_box)
        board.add_line(self, compute_y)

        # SEC_RESULT
        result = Tex("학생 수 15명, 연필 85자루", tex_environment="flushleft").scale(0.8)
        result.move_to(left_box.get_center())
        self.play(Transform(problem_text, result))
        self.wait(2)
