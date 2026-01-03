import { describe, it, expect, beforeEach } from "vitest";
import Matter from "matter-js";
import { Rocket } from "../src/rocket";

describe("Rocket", () => {
  let engine: Matter.Engine;
  let world: Matter.World;
  let rocket: Rocket;

  beforeEach(() => {
    engine = Matter.Engine.create();
    world = engine.world;
    rocket = new Rocket(world, 0, 0);
  });

  it("should initialize correctly", () => {
    expect(rocket.body).toBeDefined();
    expect(rocket.engine).toBeDefined();
    expect(rocket.pilot).toBeDefined();
    expect(rocket.mass).toBe(300);
  });

  it("should calculate TWR correctly", () => {
    rocket.space = { gravity: { x: 0, y: -600 } };
    // TWR = thrust / mass / g
    // Default thrust = 1e5, mass = 300, g = 600
    const expectedTWR = 1e5 / 300 / 600;
    expect(rocket.twr()).toBeCloseTo(expectedTWR);
  });

  it("should update fuel usage when ignited", () => {
    rocket.engine.ignite();
    const initialFuel = rocket.stats.fuel_used;
    rocket.update_forces();
    expect(rocket.stats.fuel_used).toBeGreaterThan(initialFuel);
  });

  it("should not update fuel usage when not ignited", () => {
    rocket.engine.cut_off();
    const initialFuel = rocket.stats.fuel_used;
    rocket.update_forces();
    expect(rocket.stats.fuel_used).toBe(initialFuel);
  });

  it("should provide telemetry data", () => {
    const telemetry = rocket.get_telemetry();
    expect(telemetry.position).toBeDefined();
    expect(telemetry.velocity).toBeDefined();
    expect(telemetry.angle).toBeDefined();
    expect(telemetry.angular_velocity).toBeDefined();
  });
});
