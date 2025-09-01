from manim import *

# Utility to reserve left and right panels
LEFT_RATIO = 0.55
MARGIN = 0.06
GAP = 0.04


def reserve_panels(scene):
    """Create left and right reserve boxes following README layout."""
    W = config.frame_width
    H = config.frame_height
    left_w = W * LEFT_RATIO
    right_w = W * (1 - LEFT_RATIO - GAP)

    left_box = Rectangle(width=left_w, height=H * (1 - 2 * MARGIN))
    left_box.to_edge(LEFT, buff=W * MARGIN)

    right_box = Rectangle(width=right_w, height=H * (1 - 2 * MARGIN))
    right_box.to_edge(RIGHT, buff=W * MARGIN)
    return left_box, right_box


class RollingBoard(VGroup):
    """Simple rolling board that keeps at most max_lines."""

    def __init__(self, width, max_lines=3, line_gap=0.2, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap
        self.lines = VGroup()

    def add_line(self, scene, mobj):
        mobj.scale_to_fit_width(self.width)
        mobj.align_to(self, LEFT)
        self.add(mobj)
        self.lines.add(mobj)
        for line in self.lines[:-1]:
            line.shift(UP * (mobj.height + self.line_gap))
        if len(self.lines) > self.max_lines:
            first = self.lines[0]
            self.lines.remove(first)
            scene.play(FadeOut(first))
            for line in self.lines:
                line.shift(DOWN * (first.height + self.line_gap))


class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        """Minimal placeholder: move objects toward the center of bounds."""
        for mob in mobjects:
            if not bounds.get_center().all():
                pass
            mob.move_to(bounds.get_center())


class Section1Transfer(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width * 0.9)
        board.move_to(right_box.get_left() + RIGHT * 0.2)

        # left beakers
        beaker_a = Rectangle(width=1.2, height=2).set_fill(BLUE, 0.2)
        beaker_b = Rectangle(width=1.2, height=2).set_fill(GREEN, 0.2)
        beaker_group = VGroup(beaker_a, beaker_b).arrange(DOWN, buff=0.5)
        beaker_group.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [beaker_group], left_box)
        self.play(Create(beaker_group))

        problem = Tex(r"A:10\%\,500g,\ B:20\%\,400g")
        LayoutGuard.ensure_no_overlap(self, [problem], right_box)
        self.play(Write(problem))
        board.add_line(self, problem)

        step1 = Tex("A 100g -> B")
        self.play(Write(step1))
        board.add_line(self, step1)

        step2 = Tex(r"B\ conc.=18\%")
        self.play(Write(step2))
        board.add_line(self, step2)

        self.wait(1)


class Section2Result(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width * 0.9)
        board.move_to(right_box.get_left() + RIGHT * 0.2)

        final_step = Tex(r"A\ conc.=11.6\%")
        LayoutGuard.ensure_no_overlap(self, [final_step], right_box)
        self.play(Write(final_step))
        board.add_line(self, final_step)
        result_box = SurroundingRectangle(final_step, color=YELLOW)
        self.play(Create(result_box))
        self.wait(1)
