from manim import *

class Projectile(VMobject):
    def __init__(self,
                 scene : Scene | ThreeDScene,  # Scene where you use Projectile
                 x0    : int | float = 0,         # Initial x Position
                 y0    : int | float = 0,         # Initial y Position
                 v0    : int | float = 1,         # Initial Velocity the velocity vector
                 theta : int | float = PI/4,         # Angle of launch
                 includeXTracker : bool = True
                 ):
        super().__init__()
        self.theta = theta
        self.x0    = x0
        self.y0    = y0
        self.vx0   = v0 * np.cos(theta)         # Horizontal Component of Velocity
        self.vy0   = v0 * np.sin(theta)         # Vertical Component of Velocity
        self.scene = scene
        self.time  = ValueTracker(0)

        # Projectile
        self.projectile = Dot()
        # Updaters
        # Moves Projectile with changing value of time
        self.projectile.add_updater(lambda mobj : mobj.move_to(self.position(self.time.get_value())))
        # This Function makes sure the projectile never goes below zero (or below ground)
        self.projectile.add_updater(lambda mobj : self.stop() if mobj.get_center()[1] < self.y0 and len(self.scene.updaters) >= 1 else ... )
        path = TracedPath(self.projectile.get_center)

        self.add(self.projectile, path)
    
    # Position and Velocity
    def position(self, t):
        """Returns the Position at a given instance of time."""
        return np.array([self.x0 + self.vx0 * t * np.cos(self.theta),
                         self.y0 + self.vy0 * t * np.sin(self.theta) - 0.5 * 9.8 * t**2,
                         0
                        ])

    def velocity(self, t):
        """Returns the Velocity at a given instance of time."""
        return np.array([self.v0 * np.cos(self.theta),
                         self.v0 * np.sin(self.theta) - 9.8 * t,
                         0
                        ])

    # X and Y Lines View
    def x_tracker(self):
        dash = always_redraw(lambda : Line().rotate(PI/2).scale(0.1).set_color(BLUE).move_to([self.position(self.time.get_value())[0], self.y0, 0]))
        line = always_redraw(lambda : Line([self.x0, self.y0, 0], dash.get_center()).set_color(BLUE))
        xValue = always_redraw(lambda : MathTex(f"{round(self.position(self.time.get_value())[0] - self.x0, 2)}").set_color(BLUE).next_to(dash, DOWN))

        self.add(dash, line, xValue)

    def y_tracker(self):
        dash = always_redraw(lambda : Line().scale(0.1).set_color(YELLOW).move_to([self.x0, self.position(self.time.get_value())[1], 0]))
        line = always_redraw(lambda : Line([self.x0, self.y0, 0], dash.get_center()).set_color(YELLOW))
        yValue = always_redraw(lambda : MathTex(f"{round(self.position(self.time.get_value())[1] - self.y0, 2)}").set_color(YELLOW).next_to(dash, LEFT))

        self.add(dash, line, yValue)

    def launch(self):
        self.scene.add_updater(lambda dt : self.time.increment_value(dt))

    def stop(self):
        self.scene.remove_updater(self.scene.updaters[-1])

class Test(Scene):
    def construct(self):
        p = Projectile(self, -4, -3, 15, PI/3)
        self.add(NumberPlane())
        p.x_tracker()
        p.y_tracker()
        self.add(p)
        self.wait(2)
        p.launch()
        self.add(p)
        self.wait(5)
