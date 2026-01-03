import Matter from 'matter-js';

export interface Game {
    pos2screen(pos: Matter.Vector): { x: number, y: number };
    screen2pos(pos: { x: number, y: number }): Matter.Vector;
    ctx: CanvasRenderingContext2D;
}

export abstract class GameObject {
    body: Matter.Body | null = null;
    facecolor: string = "red";
    edgecolor: string = "blue";

    update_forces(): void {}
    update_drag(): void {}

    protected _drag_formula(area: number, velocity?: Matter.Vector, coeff: number = 1e-3): Matter.Vector {
        const v = velocity || (this.body ? this.body.velocity : { x: 0, y: 0 });
        const speed = Matter.Vector.magnitude(v);
        // F = -coeff * area * speed * velocity
        return Matter.Vector.mult(v, -coeff * area * speed);
    }

    abstract draw(game: Game): void;
}

export class Ball extends GameObject {
    constructor(world: Matter.World, x: number, y: number, radius: number = 10, mass: number = 3e5) {
        super();
        this.body = Matter.Bodies.circle(x, y, radius, {
            mass: mass,
            friction: 0.8,
            restitution: 0.5
        });
        Matter.World.add(world, this.body);
    }

    draw(game: Game): void {
        if (!this.body) return;
        const radius = (this.body.circleRadius || 10);
        const pos = game.pos2screen(this.body.position);
        
        const angle = this.body.angle;
        const p2 = {
            x: pos.x + Math.cos(angle) * radius * 0.9,
            y: pos.y + Math.sin(angle) * radius * 0.9
        };

        game.ctx.beginPath();
        game.ctx.arc(pos.x, pos.y, radius, 0, 2 * Math.PI);
        game.ctx.strokeStyle = this.edgecolor;
        game.ctx.lineWidth = 2;
        game.ctx.stroke();

        game.ctx.beginPath();
        game.ctx.moveTo(pos.x, pos.y);
        game.ctx.lineTo(p2.x, p2.y);
        game.ctx.strokeStyle = this.facecolor;
        game.ctx.stroke();
    }
}

export class Wall extends GameObject {
    constructor(world: Matter.World, p1: Matter.Vector, p2: Matter.Vector) {
        super();
        const center = Matter.Vector.div(Matter.Vector.add(p1, p2), 2);
        const length = Matter.Vector.magnitude(Matter.Vector.sub(p2, p1));
        const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
        
        this.body = Matter.Bodies.rectangle(center.x, center.y, length, 2, {
            isStatic: true,
            friction: 0.99,
            angle: angle
        });
        Matter.World.add(world, this.body);
    }

    draw(game: Game): void {
        if (!this.body) return;
        // In Matter.js, for a rectangle, we can get vertices
        const vertices = this.body.vertices;
        const p1 = game.pos2screen(vertices[0]);
        const p2 = game.pos2screen(vertices[1]); // This is not quite right for a segment-like wall
        
        // Let's use the intended p1, p2 logic
        // But the body might have moved (though it's static)
        // For static segment wall:
        game.ctx.beginPath();
        const start = game.pos2screen(vertices[0]); // Approximation
        game.ctx.moveTo(start.x, start.y);
        for (let i = 1; i < vertices.length; i++) {
            const p = game.pos2screen(vertices[i]);
            game.ctx.lineTo(p.x, p.y);
        }
        game.ctx.strokeStyle = "black";
        game.ctx.lineWidth = 2;
        game.ctx.stroke();
    }
}

export class Poly extends GameObject {
    constructor(world: Matter.World, x: number, y: number, points: Matter.Vector[], mass: number = 10) {
        super();
        // Matter.Bodies.fromVertices needs the points to be centered
        this.body = Matter.Bodies.fromVertices(x, y, [points], {
            mass: mass,
            friction: 0.8
        });
        if (!this.body) {
             // Fallback if decomposition fails
             this.body = Matter.Bodies.rectangle(x, y, 10, 10, { mass });
        }
        Matter.World.add(world, this.body);
    }

    draw(game: Game): void {
        if (!this.body) return;
        const vertices = this.body.vertices;
        game.ctx.beginPath();
        const start = game.pos2screen(vertices[0]);
        game.ctx.moveTo(start.x, start.y);
        for (let i = 1; i < vertices.length; i++) {
            const p = game.pos2screen(vertices[i]);
            game.ctx.lineTo(p.x, p.y);
        }
        game.ctx.closePath();
        game.ctx.strokeStyle = this.edgecolor;
        game.ctx.lineWidth = 2;
        game.ctx.stroke();
    }
}

export class Rectangle extends Poly {
    constructor(world: Matter.World, x: number, y: number, w: number, h: number, mass: number = 10) {
        const points = [
            { x: -w / 2, y: -h / 2 },
            { x: w / 2, y: -h / 2 },
            { x: w / 2, y: h / 2 },
            { x: -w / 2, y: h / 2 }
        ];
        super(world, x, y, points, mass);
    }
}
