from flask import Flask

app = Flask(__name__)

def get_babylon_world():
    # Notice the f""" at the start
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        <script src="https://cdn.babylonjs.com/cannon.js"></script>
        <style>
            html, body {{ overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; }}
            #renderCanvas {{ width: 100%; height: 100%; touch-action: none; }}
        </style>
    </head>
    <body>
        <canvas id="renderCanvas"></canvas>
        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);

            const createScene = function() {{
                const scene = new BABYLON.Scene(engine);
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                const camera = new BABYLON.FreeCamera("camera", new BABYLON.Vector3(0, 5, -10), scene);
                camera.attachControl(canvas, true);
                camera.applyGravity = true;
                camera.checkCollisions = true;

                const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 50, height: 50}}, scene);
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);

                return scene;
            }};

            const scene = createScene();
            engine.runRenderLoop(function() {{ scene.render(); }});
            window.addEventListener("resize", function() {{ engine.resize(); }});
        </script>
    </body>
    </html>
    """
    # ^ That triple quote above is what was missing!

@app.route('/')
def index():
    return get_babylon_world()

if __name__ == "__main__":
    app.run()
