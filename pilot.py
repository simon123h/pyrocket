import math
import pygame
from settings import PHYSICS_DT


class Pilot():

    def __init__(self, rocket):
        self.rocket = rocket

    def handle_constrols(self, game):
        pass


class Autopilot(Pilot):

    def __init__(self, rocket):
        super().__init__(rocket)
        self.sas_mode = "OFF"

    def handle_controls(self, game):

        self.steer()

        for event in game.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.rocket.engine.ignited = not self.rocket.engine.ignited
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                self.rocket.pilot.sas_mode = "OFF"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.rocket.pilot.sas_mode = "assist"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.rocket.pilot.sas_mode = "stabilize"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.rocket.pilot.sas_mode = "hover"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                self.rocket.pilot.sas_mode = "land"

        # handle pressed keys
        if game.pressed_keys[pygame.K_UP]:
            self.rocket.engine.thrust += 50
        if game.pressed_keys[pygame.K_DOWN]:
            self.rocket.engine.thrust -= 50
            self.rocket.engine.thrust = max(self.rocket.engine.thrust, 0)
        if game.pressed_keys[pygame.K_LEFT]:
            self.rocket.body.angle += 0.002
            self.rocket.engine.angle += 0.2 / 180. * math.pi
        if game.pressed_keys[pygame.K_RIGHT]:
            self.rocket.body.angle -= 0.002
            self.rocket.engine.angle -= 0.2 / 180. * math.pi

    def steer(self):
        dt = PHYSICS_DT
        rocket = self.rocket
        telemetry = rocket.get_telemetry()
        engine = rocket.engine

        # get telemetry data
        position = telemetry["position"]
        angle = telemetry["angle"]
        velocity = telemetry["velocity"]
        angular_velocity = telemetry["angular_velocity"]
        # how aggressive is SAS?
        sas_aggr = dt * 120.
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
