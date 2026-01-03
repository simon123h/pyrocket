import Matter from "matter-js";
import { Rocket } from "./rocket";

export interface GameState {
  events: { type: string; code: string }[]; // We'll use a simplified event system
  pressed_keys: { [key: string]: boolean };
  DT: number;
  space: { gravity: Matter.Vector };
}

/**
 * Base class for a pilot or autopilot.
 */
export class Pilot {
  constructor(protected rocket: Rocket) {}

  /**
   * Handles controls for the rocket.
   * @param _game The current game state.
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  handle_controls(_game: GameState): void {}
}

/**
 * Autopilot system for the rocket.
 */
export class Autopilot extends Pilot {
  sas_mode: string = "OFF";
  readonly SAS_modes: { [key: string]: string } = {
    Digit0: "OFF",
    Digit1: "assist",
    Digit2: "stabilize",
    Digit3: "hover",
    Digit4: "land",
  };

  handle_controls(game: GameState): void {
    this.auto_controls(game);

    // User controls
    // In TS/JS, we'll handle events in the main loop or a listener
    // For simplicity, let's assume game.events contains keydown events since last frame
    for (const event of game.events) {
      if (event.type === "keydown") {
        if (event.code === "Space") {
          this.rocket.engine.ignited = !this.rocket.engine.ignited;
        } else if (this.SAS_modes[event.code]) {
          this.sas_mode = this.SAS_modes[event.code];
          this.rocket.engine.ignited = true;
        }
      }
    }

    let servo = 1;
    if (["hover", "land", "stabilize"].includes(this.sas_mode)) {
      servo = 8;
    }

    if (game.pressed_keys["ArrowUp"]) {
      this.rocket.engine.increase_thrust(3000 * servo);
    }

    if (game.pressed_keys["ArrowDown"]) {
      this.rocket.engine.increase_thrust(-3000 * servo);
    }

    if (game.pressed_keys["ArrowLeft"]) {
      if (this.rocket.body) {
        Matter.Body.setAngle(this.rocket.body, this.rocket.body.angle - 0.002 * servo);
      }
      this.rocket.engine.angle += 0.0001 * servo;
    }
    if (game.pressed_keys["ArrowRight"]) {
      if (this.rocket.body) {
        Matter.Body.setAngle(this.rocket.body, this.rocket.body.angle + 0.002 * servo);
      }
      this.rocket.engine.angle -= 0.0001 * servo;
    }
  }

  auto_controls(game: GameState): void {
    if (!this.rocket.body) {
      return;
    }

    const rocket = this.rocket;
    const telemetry = rocket.get_telemetry();
    const engine = rocket.engine;

    const position = telemetry.position;
    const angle = telemetry.angle;
    const velocity = telemetry.velocity;
    const angular_velocity = telemetry.angular_velocity;

    if (this.sas_mode === "OFF") {
      // Nothing
    } else if (this.sas_mode === "assist") {
      engine.increase_angle(-0.1 * angular_velocity);
    } else if (["hover", "land", "stabilize"].includes(this.sas_mode)) {
      const gravity = game.space.gravity;
      let momentum = velocity;
      if (this.sas_mode === "stabilize") {
        momentum = { x: 0, y: 0 };
      }
      const target_direction = Matter.Vector.add(momentum, gravity);
      const target_angle = Math.atan2(target_direction.x, -target_direction.y);

      let thrust_angle = target_angle - angle;
      thrust_angle -= 0.4 * angular_velocity;
      engine.set_angle(thrust_angle);
    }

    if (this.sas_mode === "hover") {
      const g = Matter.Vector.magnitude(game.space.gravity);
      let thrust = rocket.mass * g;
      thrust -= rocket.mass * velocity.y;
      thrust *= Math.min(1.0 / Math.abs(Math.cos(engine.angle - angle)), 2);
      engine.set_thrust(thrust);
    } else if (this.sas_mode === "land") {
      const h = position.y - rocket.h / 1.9;
      const v = velocity.y;
      const m = rocket.mass;
      const g = Matter.Vector.magnitude(game.space.gravity);

      let thrust = (2 * v * v * m) / h + g;
      thrust *= Math.min(1.0 / Math.abs(Math.cos(engine.angle - angle)), 4);
      thrust *= 0.75;

      if (v > 0 || thrust < engine.MIN_THRUST) {
        engine.cut_off();
      } else {
        engine.ignite();
      }
      engine.set_thrust(thrust);
      rocket.airbrakes_enabled = true;

      if (position.y < rocket.h / 1.8) {
        engine.ignited = false;
        rocket.airbrakes_enabled = false;
        this.sas_mode = "OFF";
      }
    }
  }
}
