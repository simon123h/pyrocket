import { RocketGame } from "./game";

const canvas = document.createElement("canvas");
document.body.appendChild(canvas);
document.body.style.margin = "0";
document.body.style.overflow = "hidden";
document.body.style.backgroundColor = "white";

const game = new RocketGame(canvas);

function physicsLoop(): void {
  if (game.running) {
    // In the original Python code:
    // n_physics_steps = int(1 / game.DT / game.FPS)
    // for _ in range(n_physics_steps): game.update_physics()
    // const n_physics_steps = Math.floor(1 / game.DT / game.FPS);
    const n_physics_steps = 1;
    game.handle_controls();
    for (let i = 0; i < n_physics_steps; i++) {
      game.update_physics();
    }
  }
}

window.setInterval(physicsLoop, 1000 / game.FPS);

function renderLoop(): void {
  game.draw();
  requestAnimationFrame(renderLoop);
}

requestAnimationFrame(renderLoop);
