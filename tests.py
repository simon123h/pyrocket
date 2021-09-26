import pymunk
import math


class Test():
    """
    A test can be performed on a game, runs some specific setup
    and measures some statistics and results.
    """

    def __init__(self):
        self.rocket_position = pymunk.Vec2d(0, 1000)
        self.rocket_velocity = pymunk.Vec2d(0, 0)
        self.rocket_angle = 0
        self.rocket_angular_velocity = 0
        self.sas_mode = "land"
        self.game = None
        self.stats_before = None
        self.t_before = 0
        self.t_after = 0
        self.stats_after = None
        self.next_test = None
        self.ignore_height = False

    def start(self, game):
        print("Running test...")
        # apply setup
        self.game = game
        game.test = self
        rocket = game.rocket
        rocket.body.position = self.rocket_position
        rocket.body.velocity = self.rocket_velocity
        rocket.body.angle = self.rocket_angle
        rocket.engine.ignited = True
        rocket.body.angular_velocity = self.rocket_angular_velocity
        rocket.pilot.sas_mode = self.sas_mode
        # measure stats before
        self.stats_before = rocket.stats.copy()
        self.t_before = self.game.time

    def is_finished(self):
        # check if the rocket landed
        rocket = self.game.rocket
        h = rocket.body.position.y
        v = rocket.body.velocity
        if (h > 200 and not self.ignore_height) or abs(v.x) > .1 or abs(v.y) > .1:
            return False
        # measure stats after
        self.stats_after = rocket.stats.copy()
        self.t_after = self.game.time
        # display test results
        self.display_results()
        print("Test finished.\n")
        return True

    # display test results
    def display_results(self):
        fuel_used = self.stats_after["fuel_used"] - \
            self.stats_before["fuel_used"]
        time_taken = self.t_after - self.t_before
        print(f"Fuel used: {fuel_used:f}")
        print(f"Time taken: {time_taken:f}")


# List of all tests
ALL_TESTS = []

test = Test()
test.rocket_position = pymunk.Vec2d(0, 1000)
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 6000)
test.rocket_velocity = pymunk.Vec2d(1000, 0)
test.rocket_angle = math.pi / 2
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 8000)
test.rocket_velocity = pymunk.Vec2d(1000, 0)
test.rocket_angle = -math.pi / 2
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 5000)
test.rocket_velocity = pymunk.Vec2d(1000, 0)
test.rocket_angle = math.pi / 2
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 10000)
test.rocket_velocity = pymunk.Vec2d(5000, 0)
test.rocket_angle = math.pi / 2
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 10000)
test.rocket_velocity = pymunk.Vec2d(500, 0)
test.rocket_angular_velocity = 100
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 6000)
test.rocket_velocity = pymunk.Vec2d(0, -500)
test.rocket_angular_velocity = 10
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 200000)
test.rocket_velocity = pymunk.Vec2d(0, -500)
test.rocket_angle = -math.pi+1e-3
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 120)
test.rocket_velocity = pymunk.Vec2d(10, 10)
test.rocket_angular_velocity = 4
test.sas_mode = "hover"
ALL_TESTS.append(test)

test = Test()
test.rocket_position = pymunk.Vec2d(0, 3000)
test.rocket_velocity = pymunk.Vec2d(20, -1000)
test.rocket_angular_velocity = 4
test.sas_mode = "hover"
test.ignore_height = True
ALL_TESTS.append(test)
