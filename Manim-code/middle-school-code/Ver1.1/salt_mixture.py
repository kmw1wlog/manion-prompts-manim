from manim import *

# Utility classes from README (simplified)
class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        # simplistic bounds check: shift objects inside if necessary
        for m in mobjects:
            bbox = m.get_bounding_box()
            min_x, min_y = bbox[0][0], bbox[0][1]
            max_x, max_y = bbox[2][0], bbox[2][1]
            shift_vec = ORIGIN
            if min_x < bounds.get_left()[0]:
                shift_vec += (bounds.get_left()[0] - min_x) * RIGHT
            if max_x > bounds.get_right()[0]:
                shift_vec += (bounds.get_right()[0] - max_x) * LEFT
            if min_y < bounds.get_bottom()[1]:
                shift_vec += (bounds.get_bottom()[1] - min_y) * UP
            if max_y > bounds.get_top()[1]:
                shift_vec += (bounds.get_top()[1] - max_y) * DOWN
            m.shift(shift_vec)

class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_gap=0.3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap
    def add_line(self, scene, mob):
        mob.scale_to_fit_width(self.width)
        mob.align_to(self, LEFT)
        self.add(mob)
        if len(self) > self.max_lines:
            old_line = self[0]
            scene.play(FadeOut(old_line, shift=UP*0.2))
            self.remove(old_line)
        self.arrange(DOWN, buff=self.line_gap, aligned_edge=LEFT)


def reserve_panels(scene, left_ratio=0.55):
    W, H = config.frame_width, config.frame_height
    left_w = W*left_ratio
    right_w = W*(1-left_ratio)
    margin = 0.06
    gap = 0.04*W
    left_box = Rectangle(width=left_w - gap/2, height=H*(1-2*margin))\
        .to_edge(LEFT, buff=W*margin)
    right_box = Rectangle(width=right_w - gap/2, height=H*(1-2*margin))\
        .to_edge(RIGHT, buff=W*margin)
    return left_box, right_box

# Main Scene
class SaltMixture(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.9)
        board.move_to(right_box.get_left() + RIGHT*0.1)
        LayoutGuard.ensure_no_overlap(self, [board], right_box)
        self.add(board)

        # SEC_PROBLEM
        problem = Text("200g의 α% + 800g의 1%", font_size=32)
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        self.play(Write(problem))
        board.add_line(self, problem)

        # SEC_GIVENS
        givens = MathTex(r"\text{총 질량}=1000g")
        LayoutGuard.ensure_no_overlap(self, [givens], right_box)
        self.play(Write(givens))
        board.add_line(self, givens)

        # SEC_WORK
        salt_mass = MathTex(r"\text{소금}=2\alpha+8")
        LayoutGuard.ensure_no_overlap(self, [salt_mass], right_box)
        self.play(Write(salt_mass))
        board.add_line(self, salt_mass)

        conc = MathTex(r"\frac{2\alpha+8}{1000}\times100\%")
        LayoutGuard.ensure_no_overlap(self, [conc], right_box)
        self.play(Write(conc))
        board.add_line(self, conc)

        # SEC_RESULT
        result = MathTex(r"\boxed{\frac{2\alpha+8}{10}\%}").scale(1.2)
        result.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [result], left_box)
        self.play(Write(result))
        self.wait(2)
