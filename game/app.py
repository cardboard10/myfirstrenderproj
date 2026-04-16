from flask import Flask

app = Flask(__name__)

def get_game_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Voxel Builder Template</title>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        
        <style>
            /* ZONE 1: THE LOOK (CSS) */
            html, body { overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; background: black; }
            #renderCanvas { width: 100%; height: 100%; outline: none; }
            
            /* The UI HUD (Where your buttons live) */
            #gui { 
                position: absolute; top: 20px; left: 20px; z-index: 10;
                display: flex; flex-direction: column; gap: 10px;
            }

            .game-btn { 
                padding: 12px 24px; border-radius: 5px; border: 2px solid white;
                font-family: 'Courier New', monospace; font-weight: bold; cursor: pointer;
                transition: 0.2s;
            }

            /* Button Colors - Change these to change button looks! */
            #btn-center { background: #FFD700; color: black; } /* Gold */
            #btn-clear  { background: #FF4500; color: white; } /* OrangeRed */

            #crosshair { 
                position: absolute; top: 50%; left: 50%; width: 6px; height: 6px; 
                background: white; border-radius: 50%; pointer-events: none; 
            }
        </style>
    </head>
    <body>

        <div id="gui">
            <button id="btn-center" class="game-btn">SPAWN CENTER BLOCK</button>
            <button id="btn-clear" class="game-btn">CLEAR ALL BLOCKS</button>
        </div>
        <div id="crosshair"></div>
        <canvas id="renderCanvas"></canvas>

        <script>
            // ZONE 3: STARTING THE ENGINE
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);
            let blocksArray = []; // We keep track of blocks here so we can clear them

            const createScene = function() {
                const scene = new BABYLON.Scene(engine);
                scene.clearColor = new BABYLON.Color4(0.05, 0.05, 0.05, 1); // Dark background

                // CAMERA SETTINGS
                // --- ZONE 3: BALANCED PHYSICS ---
                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 5, -15), scene);
                camera.attachControl(canvas, true);
                
                // SPEED: Try 0.1 for a steady walk. 0.5 was likely too fast.
                camera.speed = 0.1; 
                
                // INERTIA: Set this to 0. If it is 0.1 or higher, you will "slide" 
                // and the speed will feel like it's multiplying out of control.
                camera.inertia = 0; 
                
                // COLLISION SETTINGS (Keep these for physics!)
                camera.checkCollisions = true;
                camera.applyGravity = true; 
                camera.ellipsoid = new BABYLON.Vector3(0.5, 1, 0.5);
                
                
                // Standard WASD mapping
                camera.keysUp    = [87]; // W
                camera.keysDown  = [83]; // S
                camera.keysLeft  = [65]; // A
                camera.keysRight = [68]; // D
                
                
                
                new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                // THE GRID FLOOR
                const ground = BABYLON.MeshBuilder.CreateGround("ground", {width: 60, height: 60}, scene);
                const groundMat = new BABYLON.StandardMaterial("gMat", scene);
                groundMat.diffuseColor = new BABYLON.Color3(0.1, 0.1, 0.2); 
                ground.material = groundMat;

                // ZONE 4: THE SPAWNING LOGIC
                // This is the core function you can reuse!
                window.spawnBlock = function(x, y, z, colorHex) {
                    const block = BABYLON.MeshBuilder.CreateBox("box", {size: 1}, scene);
                    block.position = new BABYLON.Vector3(x, y, z);
                    
                    const mat = new BABYLON.StandardMaterial("m", scene);
                    mat.emissiveColor = BABYLON.Color3.FromHexString(colorHex);
                    block.material = mat;
                    
                    // --- ADD THESE TWO LINES FOR PHYSICS ---
                    block.checkCollisions = true; 
                    // This tells the camera "don't walk through me"
                        
                    blocksArray.push(block);
                };

                // CLICK TO BUILD (Standard Mechanic)
                window.addEventListener("mousedown", (e) => {
                    if (document.pointerLockElement !== canvas) return;
                    if (e.button === 0) { // Left Click
                        const pick = scene.pick(canvas.width/2, canvas.height/2);
                        if (pick.hit) {
                            const spawnPos = pick.pickedMesh.position.add(pick.getNormal(true));
                            window.spawnBlock(spawnPos.x, spawnPos.y, spawnPos.z, "#00FFFF"); // Cyan
                        }
                    }
                });

                return scene;
            };

            const scene = createScene();

            // ZONE 5: BUTTON CLICK EVENTS
            // Link the HTML buttons to the JavaScript logic
            document.getElementById("btn-center").onclick = function() {
                // Spawns a GOLD block at the center (0, 0.5, 0)
                window.spawnBlock(0, 0.5, 0, "#FFD700");
            };

            document.getElementById("btn-clear").onclick = function() {
                // Loops through our list and deletes everything
                blocksArray.forEach(b => b.dispose());
                blocksArray = [];
            };

            // LOCK MOUSE & RUN
            canvas.addEventListener("click", () => canvas.requestPointerLock());
            engine.runRenderLoop(() => scene.render());
            window.addEventListener("resize", () => engine.resize());
        </script>
    </body>
    </html>
    """

@app.route('/')
def index():
    return get_game_html()

if __name__ == "__main__":
    app.run()
