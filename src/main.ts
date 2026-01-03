import { RocketGame } from './game';

const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
document.body.style.margin = '0';
document.body.style.overflow = 'hidden';
document.body.style.backgroundColor = 'white';

const game = new RocketGame(canvas);

function loop() {
    if (game.running) {
        // In the original Python code:
        // n_physics_steps = int(1 / game.DT / game.FPS)
        // for _ in range(n_physics_steps): game.update_physics()
        
        const n_physics_steps = Math.floor(1 / game.DT / game.FPS);
        
        game.handle_controls();
        
        for (let i = 0; i < n_physics_steps; i++) {
            game.update_physics();
        }
        
        game.draw();
    }
    requestAnimationFrame(loop);
}

requestAnimationFrame(loop);
