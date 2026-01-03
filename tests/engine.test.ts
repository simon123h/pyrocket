import { describe, it, expect, beforeEach } from "vitest";
import { Engine } from "../src/engine";

describe("Engine", () => {
  let engine: Engine;

  beforeEach(() => {
    engine = new Engine();
  });

  it("should initialize with default values", () => {
    expect(engine.ignited).toBe(false);
    expect(engine.thrust).toBe(engine.MAX_THRUST);
    expect(engine.angle).toBe(0);
  });

  it("should ignite and cut off", () => {
    engine.ignite();
    expect(engine.ignited).toBe(true);
    engine.cut_off();
    expect(engine.ignited).toBe(false);
  });

  it("should set thrust within bounds", () => {
    engine.set_thrust(engine.MAX_THRUST + 1000);
    expect(engine.thrust).toBeLessThanOrEqual(engine.MAX_THRUST);

    engine.set_thrust(engine.MIN_THRUST - 1000);
    expect(engine.thrust).toBeGreaterThanOrEqual(engine.MIN_THRUST);
  });

  it("should increase and decrease thrust within limits", () => {
    const initialThrust = engine.thrust;
    engine.increase_thrust(5000);
    // It's already at MAX_THRUST in constructor, so it shouldn't increase
    expect(engine.thrust).toBe(engine.MAX_THRUST);

    engine.set_thrust(engine.MIN_THRUST + 10000);
    const currentThrust = engine.thrust;
    engine.increase_thrust(5000);
    expect(engine.thrust).toBe(currentThrust + 5000);
  });

  it("should set angle within bounds", () => {
    engine.set_angle(engine.MAX_ANGLE + 1);
    expect(engine.angle).toBe(engine.MAX_ANGLE);

    engine.set_angle(-engine.MAX_ANGLE - 1);
    expect(engine.angle).toBe(-engine.MAX_ANGLE);
  });
});
