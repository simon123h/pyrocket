import math
import pygame


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
        self.auto_constrols(game)

        # apply the user controls
        for event in game.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.rocket.engine.ignited = not self.rocket.engine.ignited
            # set SAS mode
            elif event.type == pygame.KEYDOWN and event.key in self.SAS_modes:
                self.sas_mode = self.SAS_modes[event.key]
                self.rocket.engine.ignited = True

        # for some SAS modes, we give user controls a higher weight
        servo = 1
        if self.sas_mode in ["hover", "land", "stabilize"]:
            servo = 8

        # handle pressed keys
        if game.pressed_keys[pygame.K_UP]:
            self.rocket.engine.increase_thrust(100*servo)
        if game.pressed_keys[pygame.K_DOWN]:
            self.rocket.engine.increase_thrust(-100*servo)
        if game.pressed_keys[pygame.K_LEFT]:
            self.rocket.body.angle += 0.002 * servo
            self.rocket.engine.angle += 0.003 * servo
        if game.pressed_keys[pygame.K_RIGHT]:
            self.rocket.body.angle -= 0.002 * servo
            self.rocket.engine.angle -= 0.003 * servo

    def auto_constrols(self, game):
        dt = game.DT
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
            engine.increase_angle(-0.2*angular_velocity)

        if self.sas_mode in ["hover", "land", "stabilize"]:
            # cancel rocket angle and lateral velocity
            target_angle = max(min(0.001*velocity.x, 0.2), -0.2)
            weight = min(abs(velocity.x), 300)
            thrust_angle = -0.1*(angle-target_angle) * sas_aggr * weight
            # cancel angular velocity
            thrust_angle -= 0.2*angular_velocity
            # apply thrust_angle to engine
            engine.set_angle(thrust_angle)

            # control engine thrust
            if self.sas_mode in ["hover", "land"]:
                # set TWR = 1
                thrust = rocket.mass * abs(rocket.space.gravity[1])
                # cancel vertical velocity
                if self.sas_mode == "hover":
                    thrust -= 10 * rocket.mass * velocity.y * sas_aggr
                # scale thrust to vertical component
                thrust /= max(abs(math.cos(engine.angle - angle)), 0.5)
                # apply thrust to engine
                engine.set_thrust(thrust)

        if self.sas_mode == "land":
            # thrust control

            h = position.y - rocket.h / 1.9  # target height
            v = velocity.y
            m = rocket.mass
            g = abs(rocket.space.gravity[1])

            # calculate the necessary thrust for landing
            thrust = 2 * v**2 * m / h + g
            # angle correction for tilted thrust vector
            thrust *= min(1. / math.cos(engine.angle + angle), 3)
            # safety factor: costs fuel, but makes the landing more gentle
            thrust *= 2

            # no thrust if going upwards of if thrust would be too low
            if v > 0 or (thrust < engine.MIN_THRUST and not engine.ignited):
                thrust = 0
                engine.ignited = False
            else:
                engine.ignited = True

            # set the thrust
            engine.set_thrust(thrust)

            # kill thrust when too low
            if position.y < rocket.h / 1.8:
                engine.ignited = False
                self.sas_mode = "stabilize"
            # enable airbrakes
            rocket.airbrakes_enabled = True
        else:
            rocket.airbrakes_enabled = False

    def trajectory(self):
        # TODO: estimate the trajectory of the rocket
        pass
