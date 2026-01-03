import Matter from "matter-js";
import { Game } from "./objects";

/**
 * Represents the rocket engine.
 */
export class Engine {
  ignited: boolean = false;
  readonly MAX_THRUST: number = 1e5;
  readonly MIN_THRUST: number = 1e4;
  readonly MAX_THRUST_CHANGE: number = 1e4;
  thrust: number = this.MAX_THRUST;
  readonly FUEL_CONSUMPTION: number = 1;

  angle: number = 0;
  readonly MAX_ANGLE: number = Math.PI / 4;
  readonly MAX_ANGLE_CHANGE: number = 1e9;

  private flameImg: HTMLImageElement | null = null;

  constructor() {
    this.flameImg = new Image();
    this.flameImg.src = "res/flame.png";
  }

  set_thrust(thrust: number): void {
    thrust = Math.min(thrust, this.thrust + this.MAX_THRUST_CHANGE);
    thrust = Math.max(thrust, this.thrust - this.MAX_THRUST_CHANGE);
    thrust = Math.min(thrust, this.MAX_THRUST);
    thrust = Math.max(thrust, this.MIN_THRUST);
    this.thrust = thrust;
  }

  increase_thrust(dthrust: number): void {
    this.set_thrust(this.thrust + dthrust);
  }

  set_angle(angle: number): void {
    console.log(angle, this.MAX_ANGLE);
    angle = Math.min(angle, this.angle + this.MAX_ANGLE_CHANGE);
    angle = Math.max(angle, this.angle - this.MAX_ANGLE_CHANGE);
    angle = Math.min(angle, this.MAX_ANGLE);
    angle = Math.max(angle, -this.MAX_ANGLE);
    this.angle = angle;
  }

  increase_angle(dangle: number): void {
    this.set_angle(this.angle + dangle);
  }

  ignite(): void {
    this.ignited = true;
  }

  cut_off(): void {
    this.ignited = false;
  }

  draw(game: Game, pos: Matter.Vector, global_angle: number): void {
    if (!this.ignited || !this.flameImg) {
      return;
    }

    const ll = 0.2 * Math.sqrt(this.thrust / 3e1);
    const angle = this.angle - global_angle;
    const p1 = game.pos2screen(pos);

    game.ctx.save();
    game.ctx.translate(p1.x, p1.y);
    game.ctx.rotate(angle);

    // The flame image in pygame was blitted at (w/2, h) in a 2w x 2h surface.
    // This suggests the origin of rotation is at the top center of the flame.

    const scale = 0.01 * ll;

    const w = this.flameImg.width;

    game.ctx.scale(scale, scale);

    // Center of rotation should be p1.
    // We want the flame to grow downwards from p1.
    // So we draw it at (-w/2, 0)
    game.ctx.drawImage(this.flameImg, -w / 2, 0);
    game.ctx.restore();
  }
}
