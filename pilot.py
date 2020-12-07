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

        # dict of SAS modes and associated keys
        self.SAS_modes = {
            pygame.K_0: "OFF",
            pygame.K_1: "assist",
            pygame.K_2: "stabilize",
            pygame.K_3: "hover",
            pygame.K_4: "land"
        }

    def handle_controls(self, game):

        # apply the auto controls
        self.auto_constrols()

        # apply the user controls
        for event in game.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.rocket.engine.ignited = not self.rocket.engine.ignited
            # set SAS mode
            elif event.type == pygame.KEYDOWN and event.key in self.SAS_modes:
                self.sas_mode = self.SAS_modes[event.key]

        # handle pressed keys
        if game.pressed_keys[pygame.K_UP]:
            self.rocket.engine.increase_thrust(50)
        if game.pressed_keys[pygame.K_DOWN]:
            self.rocket.engine.increase_thrust(-50)
        if game.pressed_keys[pygame.K_LEFT]:
            self.rocket.body.angle += 0.002
            self.rocket.engine.angle += 0.003
        if game.pressed_keys[pygame.K_RIGHT]:
            self.rocket.body.angle -= 0.002
            self.rocket.engine.angle -= 0.003

    def auto_constrols(self):
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
            # slowly cancel angular angular velocity
            engine.increase_angle(-0.02*angular_velocity)

        if self.sas_mode in ["hover", "land", "stabilize"]:
            # control engine's thrust angle
            thrust_angle = 0
            # cancel rocket angle
            thrust_angle -= abs(velocity.x)*angle*0.2 * sas_aggr
            # cancel angular velocity
            thrust_angle -= angular_velocity*2
            # cancel lateral velocity
            thrust_angle += 0.02*velocity.x * sas_aggr
            # apply thrust_angle to engine
            engine.set_angle(thrust_angle)

            # control engine thrust
            if self.sas_mode in ["hover", "land"]:
                # set TWR = 1
                thrust = rocket.mass * abs(rocket.space.gravity[1])
                # cancel vertical velocity
                if self.sas_mode == "hover":
                    thrust -= rocket.mass * velocity.y * sas_aggr
                # scale thrust to vertical component
                thrust /= max(abs(math.cos(engine.angle - angle)), 0.7)
                # apply thrust to engine
                engine.set_thrust(thrust)

        if self.sas_mode == "land":
            critical_velocity = 10
            if velocity.y > critical_velocity:
                factor = 0
            elif velocity.y < -critical_velocity:
                factor = rocket.h / position.y * \
                    abs(velocity.y) / critical_velocity * 0.3
            else:
                factor = 0.5
            if position.y < rocket.h / 1.65:
                engine.ignited = False
                self.sas_mode = "stabilize"
            engine.set_thrust(factor * engine.thrust)

    def trajectory(self):
        # TODO: estimate the trajectory of the rocket
        pass
