from flask import Flask

app = Flask(__name__)

def get_babylon_world():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        <script src="https://cdn.babylonjs.com/cannon.js"></script>
        <style>
            html, body {{ overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; }}
            #renderCanvas {{ width: 100%; height: 100%; outline: none; }}
        </style>
    </head>
    <body>
        <canvas id="renderCanvas"></canvas>
        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);

            const createScene = function() {{
                const scene = new BABYLON.Scene(engine);
                // Gravity
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                // Better Camera for Walking
                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
                camera.attachControl(canvas, true);
                
                // Set WASD Keys
                camera.keysUp = [87];    // W
                camera.keysDown = [83];  // S
                camera.keysLeft = [65];  // A
                camera.keysRight = [68]; // D
                
                camera.applyGravity = true;
                camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(1, 1, 1); // Your body size

                const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
                light.intensity = 0.7;

                // Ground with Color
                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 100, height: 100}}, scene);
                const groundMat = new BABYLON.StandardMaterial("gMat", scene);
                groundMat.diffuseColor = new BABYLON.Color3(0.2, 0.2, 0.2); // Dark Gray
                ground.material = groundMat;
                
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0, friction: 0.5, restitution: 0.7 }}, scene);
                ground.checkCollisions = true;

                return scene;
            }};

            const scene = createScene();
            
            // This makes the game world start when you click the screen
            canvas.addEventListener("click", () => {{
                canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock;
                canvas.requestPointerLock();
            }});

            engine.runRenderLoop(() => {{ scene.render(); }});
            window.addEventListener("resize", () => {{ engine.resize(); }});
        </script>
    </body>
    </html>
    """

@app.route('/')
def index():
    return get_babylon_world()

if __name__ == "__main__":
    app.run()
