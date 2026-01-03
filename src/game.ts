import Matter from "matter-js";
import { GameObject, Ball, Wall, Game as IGame } from "./objects";
import { Rocket } from "./rocket";

/**
 * Main game class for the rocket simulation.
 */
export class RocketGame implements IGame {
  readonly FRAME_WIDTH = 1600;
  readonly FRAME_HEIGHT = 900;
  readonly GRAVITY = 600;
  readonly FPS = 50;
  readonly DT = 1 / this.FPS;

  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  engine: Matter.Engine;
  world: Matter.World;

  objects: GameObject[] = [];
  rocket: Rocket | null = null;

  running = true;
  run_physics = true;
  time = 0;

  pressed_keys: { [key: string]: boolean } = {};

  events: { type: string; code: string }[] = [];

  test: {
    is_finished: () => boolean;

    next_test: { start: (game: RocketGame) => void } | null;

    start: (game: RocketGame) => void;
  } | null = null;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Could not get canvas context");
    }
    this.ctx = ctx;

    this.canvas.width = this.FRAME_WIDTH;
    this.canvas.height = this.FRAME_HEIGHT;

    this.engine = Matter.Engine.create();
    this.world = this.engine.world;
    this.engine.gravity.y = -1;
    this.engine.gravity.scale = (1 * this.GRAVITY) / 9.81;

    this.add_ground();
    this.add_new_rocket();

    window.addEventListener("keydown", (e) => {
      this.pressed_keys[e.code] = true;
      this.events.push({ type: "keydown", code: e.code });
    });
    window.addEventListener("keyup", (e) => {
      this.pressed_keys[e.code] = false;
    });
    window.addEventListener("mousedown", (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const pos = this.screen2pos({ x, y });
      this.add_object(new Ball(this.world, pos.x, pos.y));
    });

    // Handle window resize
    window.addEventListener("resize", () => this.handle_resize());
  }

  handle_resize(): void {
    // Simple resize logic
    // For now keep it fixed or adjust canvas size
  }

  add_ground(): void {
    for (let n = 0; n < 4; n++) {
      this.add_object(new Wall(this.world, { x: -1e6, y: 2 * n }, { x: 1e6, y: 2 * n }));
    }
  }

  add_new_rocket(): void {
    if (this.rocket) {
      this.remove_object(this.rocket);
    }
    this.rocket = new Rocket(this.world, 0, 200);
    this.rocket.space = { gravity: { x: 0, y: -this.GRAVITY } };
    this.add_object(this.rocket);
  }

  add_object(obj: GameObject): GameObject {
    this.objects.push(obj);
    return obj;
  }

  remove_object(obj: GameObject): void {
    const index = this.objects.indexOf(obj);
    if (index !== -1) {
      this.objects.splice(index, 1);
      if (obj.body) {
        Matter.World.remove(this.world, obj.body);
      }
    }
  }

  update_physics(): void {
    if (this.run_physics) {
      for (const obj of this.objects) {
        // obj.update_drag();
        obj.update_forces();
      }
      Matter.Engine.update(this.engine, this.DT);
      this.time += this.DT;
    }
  }

  handle_controls(): void {
    // Process internal events
    if (this.rocket) {
      this.rocket.handle_controls(this);
    }

    for (const event of this.events) {
      if (event.type === "keydown") {
        if (event.code === "KeyR") {
          this.add_new_rocket();
        }
        if (event.code === "KeyP") {
          this.run_physics = !this.run_physics;
        }
        if (event.code === "KeyT") {
          this.run_tests();
        }
        if (event.code === "KeyA" && this.rocket) {
          this.rocket.airbrakes_enabled = !this.rocket.airbrakes_enabled;
        }
      }
    }

    // handle unit tests
    if (this.test !== null) {
      if (this.test.is_finished()) {
        this.test = this.test.next_test;
        if (this.test !== null) {
          this.test.start(this);
        }
      }
    }

    this.events = [];
  }

  run_tests(): void {
    import("./tests").then(({ ALL_TESTS }) => {
      for (let n = 0; n < ALL_TESTS.length - 1; n++) {
        ALL_TESTS[n].next_test = ALL_TESTS[n + 1];
      }
      this.test = ALL_TESTS[0];
      this.test.start(this);
    });
  }

  draw(): void {
    // Clear
    this.ctx.fillStyle = "white";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Grid/Background
    if (this.rocket && this.rocket.body) {
      const { x, y } = this.rocket.body.position;
      const color = "rgb(240, 240, 240)";
      const dist = 700;
      const offsx = -x % dist;
      const offsy = y % dist;
      this.ctx.strokeStyle = color;
      this.ctx.lineWidth = dist / 20;

      for (let i = -1; i < 5; i++) {
        // Vertical lines
        this.ctx.beginPath();
        this.ctx.moveTo(offsx + i * dist, 0);
        this.ctx.lineTo(offsx + i * dist, this.FRAME_HEIGHT);
        this.ctx.stroke();

        // Horizontal lines
        this.ctx.beginPath();
        this.ctx.moveTo(0, offsy + i * dist);
        this.ctx.lineTo(this.FRAME_WIDTH, offsy + i * dist);
        this.ctx.stroke();
      }
    }

    // Objects
    for (const obj of this.objects) {
      obj.draw(this);
    }

    // Text
    if (this.rocket) {
      this.ctx.fillStyle = "black";
      this.ctx.font = "18px monospace";
      const thrust = this.rocket.engine.thrust / this.rocket.engine.MAX_THRUST;
      const twr = this.rocket.twr();
      const h = this.length_unit(this.rocket.body!.position.y);
      const v = this.velocity_unit(this.rocket.body!.velocity.y);
      const sas = this.rocket.pilot.sas_mode;

      const lines = [
        `Thrust: ${(thrust * 100).toFixed(0)}%`,
        `TWR: ${twr.toFixed(2)}`,
        `Height: ${h}`,
        `Velocity: ${v}`,
        `SAS: ${sas}`,
        "",
        "Controls:",
        "---------",
        "Up/Down - throttle",
        "Left/Right - thrust vector control",
        "space - start/stop engine",
        "0-4 - switch SAS mode",
        "mouse - add obstacle",
        "A - airbrakes",
        "P - pause",
        "R - restart",
        "T - run tests",
      ];

      let y = 25;
      for (const line of lines) {
        this.ctx.fillText(line, 10, y);
        y += 20;
      }
    }
  }

  pos2screen(pos: Matter.Vector): { x: number; y: number } {
    let x = pos.x + this.FRAME_WIDTH / 2;
    let y = pos.y - this.FRAME_HEIGHT / 2;
    if (this.rocket && this.rocket.body) {
      x -= this.rocket.body.position.x;
      y -= this.rocket.body.position.y;
    }
    return { x, y: -y };
  }

  screen2pos(pos: { x: number; y: number }): Matter.Vector {
    let x = pos.x - this.FRAME_WIDTH / 2;
    let y = -pos.y + this.FRAME_HEIGHT / 2;
    if (this.rocket && this.rocket.body) {
      x += this.rocket.body.position.x;
      y += this.rocket.body.position.y;
    }
    return { x, y };
  }

  length_unit(h: number): string {
    if (Math.abs(h) < 1e3) {
      return `${h.toFixed(1)}m`;
    }
    const ly = 9.461e15;
    if (Math.abs(h) < 0.1 * ly) {
      return `${(h / 1e3).toFixed(1)}km`;
    }
    return `${(h / ly).toFixed(1)}ly`;
  }

  velocity_unit(v: number): string {
    if (Math.abs(v) < 1e3) {
      return `${v.toFixed(1)}m/s`;
    }
    return `${(v / 1e3).toFixed(1)}km/s`;
  }
}
