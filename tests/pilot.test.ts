import { describe, it, expect, beforeEach, vi } from "vitest";
import Matter from "matter-js";
import { Rocket } from "../src/rocket";
import { Autopilot } from "../src/pilot";
import { RocketGame } from "../src/game";

describe("Autopilot", () => {
  let rocket: Rocket;
  let autopilot: Autopilot;
  let mockGame: any;

  beforeEach(() => {
    const engine = Matter.Engine.create();
    rocket = new Rocket(engine.world, 0, 0);
    autopilot = new Autopilot(rocket);
    mockGame = {
      engine: { gravity: { x: 0, y: -600 } },
      events: [],
      pressed_keys: {},
      DT: 1 / 50,
    };
  });

  it("should switch SAS modes via handle_controls", () => {
    mockGame.events = [{ type: "keydown", code: "Digit1" }];
    autopilot.handle_controls(mockGame);
    expect(autopilot.sas_mode).toBe("assist");
    expect(rocket.engine.ignited).toBe(true);

    mockGame.events = [{ type: "keydown", code: "Digit0" }];
    autopilot.handle_controls(mockGame);
    expect(autopilot.sas_mode).toBe("OFF");
  });

  it("should adjust engine angle in assist mode", () => {
    autopilot.sas_mode = "assist";
    if (rocket.body) {
      Matter.Body.setAngularVelocity(rocket.body, 1.0);
    }
    const initialAngle = rocket.engine.angle;
    autopilot.auto_controls(mockGame);
    // assist mode: engine.increase_angle(-0.001 * angular_velocity)
    expect(rocket.engine.angle).toBeLessThan(initialAngle);
  });

  it("should ignite engine for landing mode if vertical velocity is high", () => {
    autopilot.sas_mode = "land";
    if (rocket.body) {
      Matter.Body.setPosition(rocket.body, { x: 0, y: 300 }); // Lower height
      Matter.Body.setVelocity(rocket.body, { x: 0, y: -2000 }); // Faster
    }
    autopilot.auto_controls(mockGame);
    expect(rocket.engine.ignited).toBe(true);
  });
});
