from manim import *
import numpy as np

# Layout utilities
class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobjects, bounds):
        for m in mobjects:
            if m.width > bounds.width:
                m.scale_to_fit_width(bounds.width*0.9)
            if m.height > bounds.height:
                m.scale_to_fit_height(bounds.height*0.9)
            min_x, max_x = bounds.get_left()[0], bounds.get_right()[0]
            min_y, max_y = bounds.get_bottom()[1], bounds.get_top()[1]
            m_min_x, m_max_x = m.get_left()[0], m.get_right()[0]
            m_min_y, m_max_y = m.get_bottom()[1], m.get_top()[1]
            shift = np.array([
                0 if min_x <= m_min_x and m_max_x <= max_x else (min_x - m_min_x + 0.1 if m_min_x < min_x else max_x - m_max_x - 0.1),
                0 if min_y <= m_min_y and m_max_y <= max_y else (min_y - m_min_y + 0.1 if m_min_y < min_y else max_y - m_max_y - 0.1),
                0])
            m.shift(shift)

class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_gap=0.3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap
        self.lines = []

    def add_line(self, scene, mob):
        mob.scale_to_fit_width(self.width)
        if len(self.lines) == self.max_lines:
            top = self.lines.pop(0)
            scene.play(FadeOut(top), run_time=0.2)
            for line in self.lines:
                scene.play(line.animate.shift(UP*(mob.height+self.line_gap)), run_time=0.2)
        else:
            for line in self.lines:
                scene.play(line.animate.shift(UP*(mob.height+self.line_gap)), run_time=0.2)
        mob.next_to(self, DOWN)
        scene.play(Write(mob))
        self.add(mob)
        self.lines.append(mob)

# panel reservation
W, H = config.frame_width, config.frame_height
MARGIN = 0.06
GAP = 0.04

def reserve_panels(scene):
    left_w = W*0.55 - W*(MARGIN+GAP/2)
    right_w = W*0.45 - W*(MARGIN+GAP/2)
    left_box = Rectangle(width=left_w, height=H*(1-2*MARGIN)).to_edge(LEFT, buff=W*MARGIN)
    right_box = Rectangle(width=right_w, height=H*(1-2*MARGIN)).to_edge(RIGHT, buff=W*MARGIN)
    return left_box, right_box

# Scenes
class TrapezoidAreaScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.9)
        board.move_to(right_box.get_top() + DOWN*0.5)
        # SEC_PROBLEM
        prob = Tex(r"윗변 a, 아랫변 b, 높이 h인 사다리꼴 넓이")
        prob.move_to(right_box.get_top() + DOWN*0.5)
        LayoutGuard.ensure_no_overlap(self, [prob], right_box)
        self.add(board)
        self.play(Write(prob))
        board.add_line(self, MathTex(r"A = ?"))
        # Left trapezoid
        top = 2
        bottom = 4
        height = 2.5
        trapezoid = Polygon(
            [-top/2, height/2, 0],
            [top/2, height/2, 0],
            [bottom/2, -height/2, 0],
            [-bottom/2, -height/2, 0],
        ).set_stroke(BLUE)
        trapezoid.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [trapezoid], left_box)
        self.play(Create(trapezoid))
        # SEC_GIVENS
        top_lbl = MathTex("a").next_to(trapezoid.get_top(), UP)
        bottom_lbl = MathTex("b").next_to(trapezoid.get_bottom(), DOWN)
        height_lbl = MathTex("h").next_to(trapezoid, RIGHT)
        LayoutGuard.ensure_no_overlap(self, [top_lbl, bottom_lbl, height_lbl], left_box)
        self.play(FadeIn(top_lbl), FadeIn(bottom_lbl), FadeIn(height_lbl))
        board.add_line(self, MathTex(r"A=\frac{(a+b)h}{2}"))
        # SEC_RESULT
        result = MathTex(r"A=\frac{(a+b)h}{2}")
        result.move_to(right_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [result], right_box)
        self.play(Transform(board.lines[-1], result.copy().scale(1.2)))
        self.play(Circumscribe(result))
        self.wait()

class TravelTimeScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.9)
        board.move_to(right_box.get_top() + DOWN*0.5)
        # SEC_PROBLEM
        prob = Tex(r"20km를 시속 xkm로 달린 시간")
        prob.move_to(right_box.get_top() + DOWN*0.5)
        LayoutGuard.ensure_no_overlap(self, [prob], right_box)
        self.add(board)
        self.play(Write(prob))
        board.add_line(self, MathTex(r"t=?"))
        # Left: simple path
        line = Line(left_box.get_left()+RIGHT*0.5, left_box.get_right()+LEFT*0.5)
        LayoutGuard.ensure_no_overlap(self, [line], left_box)
        self.play(Create(line))
        car = Dot(line.get_start())
        self.play(FadeIn(car))
        self.play(MoveAlongPath(car, line), run_time=2)
        # SEC_WORK
        board.add_line(self, MathTex(r"t=\frac{\text{distance}}{\text{speed}}"))
        board.add_line(self, MathTex(r"t=\frac{20}{x}"))
        # SEC_RESULT
        result = MathTex(r"t=\frac{20}{x}\,\text{시간}")
        result.move_to(right_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [result], right_box)
        self.play(Write(result))
        self.play(Circumscribe(result))
        self.wait()

class SaltMixtureScene(Scene):
    def construct(self):
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.9)
        board.move_to(right_box.get_top() + DOWN*0.5)
        self.add(board)
        # SEC_PROBLEM
        prob = Tex(r"a\% b g + c\% d g 소금물의 소금양")
        prob.move_to(right_box.get_top() + DOWN*0.5)
        LayoutGuard.ensure_no_overlap(self, [prob], right_box)
        self.play(Write(prob))
        board.add_line(self, MathTex(r"\text{Salt}= ?"))
        # Left: beakers
        beaker1 = Rectangle(width=1, height=2).set_stroke(BLUE)
        beaker2 = Rectangle(width=1, height=2).set_stroke(GREEN)
        mix = Rectangle(width=1, height=2).set_stroke(YELLOW)
        group = VGroup(beaker1, beaker2, mix).arrange(RIGHT, buff=0.5)
        group.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [group], left_box)
        self.play(Create(group))
        # SEC_WORK
        board.add_line(self, MathTex(r"\text{Salt}=\frac{a}{100}b+\frac{c}{100}d"))
        # SEC_RESULT
        result = MathTex(r"\frac{ab}{100}+\frac{cd}{100}\,\text{g}")
        result.move_to(right_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [result], right_box)
        self.play(Write(result))
        self.play(Circumscribe(result))
        self.wait()

