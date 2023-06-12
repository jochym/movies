from manim import *

def s(t, v, ta):
    a = v/ta
    return (a*t*sqrt(1- a**2 * t**2) + arcsin(a*t))/(2*a)

def sdot(t, v, ta):
    return sqrt(1-(v*t/ta)**2)

def sim(t, v, tm, ta):
    t1 = ta
    t2 = tm/2 - ta
    t3 = tm/2 + ta
    t4 = tm - ta
    t5 = tm
    if t < t1:
        return v * t / ta
    elif t < t2 :
        return v
    elif t < t3 :
        return v * (tm/2 - t)/ta
    elif t < t4 :
        return -v
    else :
        return -v * (tm - t)/ta

class XTDiagram(Scene):
    def construct(self):
        c = 1                   # Skala prędkości
        v = 0.6                 # Max velocity (c=1)
        tm = 7                  # max time of worldline
        ta = 0.75                  # acceleration time
        t0 = 0
        t1 = ta
        t2 = tm/2 - ta
        t3 = tm/2 + ta
        t4 = tm - ta
        eps=1e-3
        play_kw = {"run_time": 15}

        t = ValueTracker(0)

        def wlfun(t, v, tm, ta):
            t1 = ta
            t2 = tm/2 - ta
            t3 = tm/2 + ta
            t4 = tm - ta

            if t < t1 :
                r = ta * v * (t/ta)**2 / 2
            elif t < t2 :
                r = v*(t - t1 + ta/2)
            elif t < t3 :
                r = ta * v * ((t-t2)*(t3-t) / ta**2 / 2 + (t2 - t1)/ta + 1/2)
            elif t < t4 :
                r = - v * (t - tm + ta/2)
            else :
                r = ta * v * ((t - tm)/ta)**2 /2
            return r

        ax = NumberPlane(
            y_range=(-0.5,7.5),
            background_line_style={"stroke_opacity": 0.4}
        )

        self.add(ax)
        self.wait(2)

        O = Dot(ax.c2p(0, t0), color=RED)
        E = Dot(ax.c2p(0, tm), color=RED)

        # self.add(O, E)
        # self.wait(2)
        
        light = ax.plot(lambda x: x, color=YELLOW)

        self.add(ax, light) 
        self.wait(2)

        worldline = ax.plot_parametric_curve(
            lambda t: np.array(
                [
                    wlfun(t,v,tm,ta),
                    t,
                    0
                ]
            ),
            t_range=[t0, tm],
            color=GREEN
        )


        self.add(worldline) 
        self.wait(2)

        b1 = Dot(point=ax.c2p(0, t0))
        b2 = Dot(point=ax.c2p(0, t0))
        simline = Line(ax.c2p(0,t0), ax.c2p(0,t0))

        b1.add_updater(lambda o: o.move_to(
            ax.c2p(
                0, 
                t.get_value()-sim(t.get_value(), v, tm, ta)*wlfun(t.get_value(), v, tm, ta)
            )))

        b2.add_updater(lambda o: o.move_to(ax.c2p(
                                            wlfun(t.get_value(), v, tm, ta),
                                            t.get_value()
                                            )
                                        ))
        simline.add_updater(lambda z: z.become(Line(b1.get_center(), b2.get_center())))
        self.add(b1, b2, simline)
        self.play(t.animate.set_value(tm), rate_func=linear, run_time=20)

        self.wait(5)