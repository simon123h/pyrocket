import Matter from 'matter-js';
import { Poly, Game } from './objects';
import { Engine } from './engine';
import { Autopilot } from './pilot';

export class Rocket extends Poly {
    w: number;
    h: number;
    mass: number;
    color: number[] = [112, 122, 255];
    drag_coeff: number = 1e-5;
    airbrakes_enabled: boolean = false;
    engine: Engine;
    engine_pos: Matter.Vector;
    pilot: Autopilot;
    stats: { fuel_used: number } = { fuel_used: 0 };
    space: { gravity: Matter.Vector };

    constructor(world: Matter.World, x: number, y: number, w: number = 15, h: number = 150, mass: number = 300e3) {
        const points = [
            { x: -w / 2, y: -h / 2 },
            { x: w / 2, y: -h / 2 },
            { x: w / 2, y: h / 2 },
            { x: 0, y: h / 1.5 },
            { x: -w / 2, y: h / 2 }
        ];
        super(world, x, y, points, mass);
        this.w = w;
        this.h = h;
        this.mass = mass;
        this.engine = new Engine();
        this.engine_pos = { x: 0, y: -h / 2 };
        this.pilot = new Autopilot(this);
        this.space = { gravity: { x: 0, y: 0 } }; // Will be updated by game
        
        if (this.body) {
            this.body.friction = 0.5;
        }
    }

    update_forces(): void {
        if (!this.body) return;
        const angle = this.engine.angle;
        const thrust_x = this.engine.thrust * Math.sin(angle);
        const thrust_y = this.engine.thrust * Math.cos(angle);
        const thrust_force_local = { x: thrust_x, y: thrust_y };

        if (this.engine.ignited) {
            const world_pos = Matter.Vector.add(this.body.position, Matter.Vector.rotate(this.engine_pos, this.body.angle));
            const world_force = Matter.Vector.rotate(thrust_force_local, this.body.angle);
            Matter.Body.applyForce(this.body, world_pos, world_force);
            this.stats.fuel_used += this.engine.thrust * this.engine.FUEL_CONSUMPTION;
        }
    }

    update_drag(): void {
        if (!this.body) return;
        const v = this.body.velocity;
        const speed = Matter.Vector.magnitude(v);
        if (speed < 0.1) return;

        const rot = { x: Math.cos(this.body.angle), y: Math.sin(this.body.angle) };
        const v_norm = Matter.Vector.normalise(v);
        
        // Exposed area calculation
        let A = Math.abs(Matter.Vector.dot(v_norm, rot));
        A = A * this.h * this.h + (1 - A) * this.w * this.w;
        A *= this.drag_coeff;

        const drag_force_world = this._drag_formula(A, v, 3e1);
        
        let drag_fp_local = { x: 0, y: -5 * this.h };
        if (this.airbrakes_enabled) {
            drag_fp_local = Matter.Vector.mult(drag_fp_local, -0.3);
        }

        const world_fp = Matter.Vector.add(this.body.position, Matter.Vector.rotate(drag_fp_local, this.body.angle));
        Matter.Body.applyForce(this.body, world_fp, drag_force_world);
        
        // Relax angular velocity
        Matter.Body.setAngularVelocity(this.body, this.body.angularVelocity * 0.999);
    }

    get_telemetry() {
        if (!this.body) return { position: { x: 0, y: 0 }, velocity: { x: 0, y: 0 }, angle: 0, angular_velocity: 0 };
        
        const noise = (amp = 0) => 1 + amp * (2 * Math.random() - 1);
        
        return {
            position: Matter.Vector.mult(this.body.position, noise()),
            velocity: Matter.Vector.mult(this.body.velocity, noise()),
            angle: ((this.body.angle + Math.PI) % (2 * Math.PI) - Math.PI) * noise(),
            angular_velocity: this.body.angularVelocity * noise()
        };
    }

    handle_controls(game: any): void {
        this.pilot.handle_controls(game);
    }

    twr(): number {
        const g = Matter.Vector.magnitude(this.space.gravity);
        return g !== 0 ? this.engine.thrust / this.mass / g : 0;
    }

    draw(game: Game): void {
        if (!this.body) return;
        
        // Draw body
        const vertices = this.body.vertices;
        game.ctx.beginPath();
        const start = game.pos2screen(vertices[0]);
        game.ctx.moveTo(start.x, start.y);
        for (let i = 1; i < vertices.length; i++) {
            const p = game.pos2screen(vertices[i]);
            game.ctx.lineTo(p.x, p.y);
        }
        game.ctx.closePath();
        game.ctx.fillStyle = `rgb(${this.color.join(',')})`;
        game.ctx.fill();
        game.ctx.strokeStyle = "black";
        game.ctx.lineWidth = 2;
        game.ctx.stroke();

        // Fins (Simplified)
        const h = this.h;
        const w = this.w;
        const drawFin = (points: Matter.Vector[]) => {
            game.ctx.beginPath();
            const p0 = game.pos2screen(Matter.Vector.add(this.body!.position, Matter.Vector.rotate(points[0], this.body!.angle)));
            game.ctx.moveTo(p0.x, p0.y);
            for (let i = 1; i < points.length; i++) {
                const p = game.pos2screen(Matter.Vector.add(this.body!.position, Matter.Vector.rotate(points[i], this.body!.angle)));
                game.ctx.lineTo(p.x, p.y);
            }
            game.ctx.closePath();
            game.ctx.fillStyle = `rgb(${this.color.join(',')})`;
            game.ctx.fill();
            game.ctx.strokeStyle = "black";
            game.ctx.stroke();
        };

        const leftFin = [{ x: -w / 2, y: -h / 2.1 }, { x: -w * 1.4, y: -h / 2.1 }, { x: -w / 2, y: -h / 5 }];
        const rightFin = [{ x: w / 2, y: -h / 2.1 }, { x: w * 1.4, y: -h / 2.1 }, { x: w / 2, y: -h / 5 }];
        drawFin(leftFin);
        drawFin(rightFin);

        // Engine
        const engine_world_pos = Matter.Vector.add(this.body.position, Matter.Vector.rotate(this.engine_pos, this.body.angle));
        this.engine.draw(game, engine_world_pos, this.body.angle);

        // Airbrakes
        if (this.airbrakes_enabled) {
            const airbrakes = [
                { x: -w / 2, y: 0.47 * h }, { x: -w * 1.5, y: 0.47 * h }, { x: -w / 2, y: 0.5 * h },
                { x: w / 2, y: 0.5 * h }, { x: w * 1.5, y: 0.47 * h }, { x: w / 2, y: 0.47 * h }
            ];
            // Split into two airbrakes for drawing if needed, but the original code just drew them as a polygon
            drawFin(airbrakes.slice(0, 3));
            drawFin(airbrakes.slice(3, 6));
        }
    }
}
