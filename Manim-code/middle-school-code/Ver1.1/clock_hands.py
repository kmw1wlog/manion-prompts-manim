from manim import *

DEG = PI / 180

# --- layout helpers -------------------------------------------------
class RollingBoard(VGroup):
    def __init__(self, width, max_lines=3, line_gap=0.3, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.max_lines = max_lines
        self.line_gap = line_gap
        self.lines = VGroup()
        self.add(self.lines)

    def add_line(self, scene, tex):
        tex.scale_to_fit_width(self.width)
        self.lines.add(tex)
        self.lines.arrange(DOWN, aligned_edge=LEFT, buff=self.line_gap)
        scene.play(Write(tex))
        if len(self.lines) > self.max_lines:
            old = self.lines[0]
            self.lines.remove(old)
            scene.play(FadeOut(old))
            self.lines.arrange(DOWN, aligned_edge=LEFT, buff=self.line_gap)

class LayoutGuard:
    @staticmethod
    def ensure_no_overlap(scene, mobs, box):
        for m in mobs:
            m.move_to(box.get_center())

def reserve_panels(scene, margin=0.06, gap=0.04):
    W, H = config.frame_width, config.frame_height
    left_w = W * (0.55 - gap/2 - margin)
    right_w = W * (0.45 - gap/2 - margin)
    left_box  = Rectangle(width=left_w,  height=H*(1-2*margin)).to_edge(LEFT,  buff=W*margin)
    right_box = Rectangle(width=right_w, height=H*(1-2*margin)).to_edge(RIGHT, buff=W*margin)
    return left_box, right_box
# --------------------------------------------------------------------

class ClockHands(Scene):
    def construct(self):
        # 패널 배치 ----------------------------------------------------
        left_box, right_box = reserve_panels(self)
        board = RollingBoard(width=right_box.width*0.9)
        board.move_to(right_box.get_center())
        self.add(board)

        # 좌측 시계 준비 ----------------------------------------------
        hour_ang = ValueTracker(0)
        min_ang  = ValueTracker(0)
        clock = Circle(radius=2)
        h_hand = always_redraw(lambda:
            Line(ORIGIN, UP*1.2, color=BLUE, stroke_width=6).rotate(hour_ang.get_value())
        )
        m_hand = always_redraw(lambda:
            Line(ORIGIN, UP*1.8, color=GREEN, stroke_width=3).rotate(min_ang.get_value())
        )
        clock_group = VGroup(clock, h_hand, m_hand)
        clock_group.move_to(left_box.get_center())
        LayoutGuard.ensure_no_overlap(self, [clock_group], left_box)
        self.play(Create(clock), FadeIn(h_hand), FadeIn(m_hand))

        # 섹션1 --------------------------------------------------------
        board.add_line(self, MathTex(r"2\text{시와 }3\text{시 사이}"))
        board.add_line(self, MathTex(r"60+0.5x = 6x"))
        x = 120/11
        board.add_line(self, MathTex(r"x=\frac{120}{11}\text{분}"))
        self.play(
            hour_ang.animate.set_value((60+0.5*x)*DEG),
            min_ang.animate.set_value(6*x*DEG)
        )
        t1 = MathTex(r"2\text{시 }10\frac{10}{11}\text{분}").set_color(YELLOW)
        t1_box = SurroundingRectangle(t1, color=YELLOW)
        t1_group = VGroup(t1, t1_box).move_to(left_box.get_bottom()+UP)
        self.play(FadeIn(t1_group))

        # 섹션2 --------------------------------------------------------
        board.add_line(self, MathTex(r"4\text{시와 }5\text{시 사이}"))
        board.add_line(self, MathTex(r"6y-(120+0.5y)=180"))
        y = 600/11
        board.add_line(self, MathTex(r"y=\frac{600}{11}\text{분}"))
        self.play(
            hour_ang.animate.set_value((120+0.5*y)*DEG),
            min_ang.animate.set_value(6*y*DEG)
        )
        t2 = MathTex(r"4\text{시 }54\frac{6}{11}\text{분}").set_color(ORANGE)
        t2_box = SurroundingRectangle(t2, color=ORANGE)
        t2_group = VGroup(t2, t2_box).next_to(t1_group, DOWN)
        self.play(FadeIn(t2_group))

        self.wait(2)
