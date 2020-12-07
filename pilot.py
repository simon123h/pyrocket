import math


class Pilot():

    def __init__(self, rocket):
        self.rocket = rocket
        self.dt = 1. / 100.

    def control(self):
        pass


class Autopilot(Pilot):

    def __init__(self, rocket):
        super().__init__(rocket)
        self.sas_mode = "OFF"

    def control(self):
        rocket = self.rocket
        telemetry = rocket.get_telemetry()
        engine = rocket.engine

        # get telemetry data
        position = telemetry["position"]
        angle = telemetry["angle"]
        velocity = telemetry["velocity"]
        angular_velocity = telemetry["angular_velocity"]
        # how aggressive is SAS?
        sas_aggr = self.dt * 120.
        if self.sas_mode == "OFF":
            pass
        if self.sas_mode == "assist":
            # control thrust angle
            engine.angle -= angular_velocity*0.02
            engine.angle = min(engine.angle, math.pi/4)
            engine.angle = max(engine.angle, -math.pi/4)
        if self.sas_mode in ["hover", "land", "stabilize"]:
            # control thrust angle
            engine.angle = 0
            engine.angle -= abs(velocity.x)*angle*0.2 * sas_aggr
            engine.angle -= angular_velocity*2
            engine.angle += 0.02*velocity.x * sas_aggr
            engine.angle = min(engine.angle, math.pi/4)
            engine.angle = max(engine.angle, -math.pi/4)
            # control absolute thrust
            if self.sas_mode in ["hover", "land"]:
                engine.thrust = rocket.mass * abs(rocket.space.gravity[1])
                if self.sas_mode == "hover":
                    engine.thrust -= rocket.mass * velocity.y * sas_aggr
                engine.thrust = max(engine.thrust, 0)
                engine.thrust /= max(abs(math.cos(engine.angle -
                                                  angle)), 0.7)
        if self.sas_mode == "land":
            critical_velocity = 10
            if velocity.y > critical_velocity:
                factor = 0
            elif velocity.y < -critical_velocity:
                factor = rocket.h / position.y * \
                    abs(velocity.y) / critical_velocity * 0.3
            else:
                factor = 0.5
            if position.y < rocket.h / 1.6:
                engine.ignited = False
                self.sas_mode = "stabilize"
            engine.thrust *= factor
            engine.thrust = max(engine.thrust, 0)

    def trajectory(self):
        # TODO: estimate the trajectory of the rocket
        pass
