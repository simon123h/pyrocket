import Matter from "matter-js";
import { RocketGame } from "./game";

/**
 * Represents a landing test.
 */
export class Test {
  rocket_position: Matter.Vector = { x: 0, y: 1000 };
  rocket_velocity: Matter.Vector = { x: 0, y: 0 };
  rocket_angle = 0;
  rocket_angular_velocity = 0;
  sas_mode = "land";
  game: RocketGame | null = null;
  stats_before: { fuel_used: number } | null = null;
  t_before = 0;
  t_after = 0;
  stats_after: { fuel_used: number } | null = null;
  next_test: Test | null = null;
  ignore_height = false;

  start(game: RocketGame): void {
    console.log("Running test...");
    this.game = game;
    // game.test = this; // Need to add this to RocketGame if we want to follow exactly

    const rocket = game.rocket;
    if (!rocket || !rocket.body) {
      return;
    }

    Matter.Body.setPosition(rocket.body, this.rocket_position);
    Matter.Body.setVelocity(rocket.body, this.rocket_velocity);
    Matter.Body.setAngle(rocket.body, this.rocket_angle);
    Matter.Body.setAngularVelocity(rocket.body, this.rocket_angular_velocity);

    rocket.engine.ignited = true;
    rocket.pilot.sas_mode = this.sas_mode;

    this.stats_before = { ...rocket.stats };
    this.t_before = game.time;
  }

  is_finished(): boolean {
    if (!this.game || !this.game.rocket || !this.game.rocket.body) {
      return false;
    }

    const rocket = this.game.rocket;
    const body = rocket.body;
    if (!body) {
      return false;
    }
    const h = body.position.y;
    const v = body.velocity;

    if (h > 200 && !this.ignore_height) {
      return false;
    }
    if (Math.abs(v.x) > 0.4 || Math.abs(v.y) > 0.4) {
      return false;
    }

    this.stats_after = { ...rocket.stats };
    this.t_after = this.game.time;
    this.display_results();
    console.log("Test finished.\n");
    return true;
  }

  display_results(): void {
    if (!this.stats_after || !this.stats_before) {
      return;
    }
    const fuel_used = this.stats_after.fuel_used - this.stats_before.fuel_used;
    const time_taken = this.t_after - this.t_before;
    console.log(`Fuel used: ${fuel_used}`);
    console.log(`Time taken: ${time_taken}`);
  }
}

export const ALL_TESTS: Test[] = [];

{
  const t = new Test();
  t.rocket_position = { x: 0, y: 1000 };
  ALL_TESTS.push(t);
}

{
  const t = new Test();
  t.rocket_position = { x: 0, y: 6000 };
  t.rocket_velocity = { x: 1000, y: 0 };
  t.rocket_angle = Math.PI / 2;
  ALL_TESTS.push(t);
}

// Add more as needed...
