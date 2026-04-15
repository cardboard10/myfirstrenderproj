from flask import Flask

app = Flask(__name__)

def get_babylon_world():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        <script src="https://cdn.babylonjs.com/cannon.js"></script>
        <script src="https://cdn.babylonjs.com/materialsLibrary/babylonjs.materials.min.js"></script>
        <style>
            html, body {{ overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; }}
            #renderCanvas {{ width: 100%; height: 100%; outline: none; }}
            #crosshair {{
                position: absolute; top: 50%; left: 50%;
                width: 10px; height: 10px; margin: -5px 0 0 -5px;
                border: 2px solid white; border-radius: 50%; pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div id="crosshair"></div>
        <canvas id="renderCanvas"></canvas>
        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);
            let selectedColor = new BABYLON.Color3(0, 0.8, 0);

            const createScene = function() {{
                const scene = new BABYLON.Scene(engine);
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
                camera.attachControl(canvas, true);
                
                // Slow down movement and looking
                camera.speed = 0.3;
                camera.angularSensibility = 3000;
                camera.inertia = 0; 
                
                camera.keysUp=[87]; camera.keysDown=[83]; camera.keysLeft=[65]; camera.keysRight=[68];
                camera.applyGravity = true; camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(0.5, 1, 0.5);

                const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 100, height: 100}}, scene);
                const gridMat = new BABYLON.GridMaterial("grid", scene);
                gridMat.mainColor = new BABYLON.Color3(0.1, 0.1, 0.1);
                gridMat.lineColor = new BABYLON.Color3(0.3, 0.3, 0.3);
                gridMat.gridRatio = 1;
                ground.material = gridMat;
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);

                window.addEventListener("mousedown", (evt) => {{
                    if (document.pointerLockElement !== canvas) return;
                    const pickInfo = scene.pick(canvas.width / 2, canvas.height / 2);
                    if (pickInfo.hit) {{
                        const target = pickInfo.pickedMesh;
                        if (evt.button === 2 || evt.shiftKey) {{ 
                            if (target.name !== "ground") target.dispose();
                        }} else if (evt.button === 0) {{ 
                            const normal = pickInfo.getNormal(true);
                            let newPos = (target.name === "ground") ? 
                                new BABYLON.Vector3(Math.round(pickInfo.pickedPoint.x), 0.5, Math.round(pickInfo.pickedPoint.z)) :
                                target.position.add(normal);

                            const box = BABYLON.MeshBuilder.CreateBox("voxel", {{size: 1}}, scene);
                            box.position = newPos;
                            const bMat = new BABYLON.StandardMaterial("bMat", scene);
                            bMat.diffuseColor = selectedColor;
                            box.material = bMat;
                            box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);
                            box.checkCollisions = true;
                        }}
                    }}
                }});

                window.addEventListener("keydown", (e) => {{
                    if (e.key === "1") selectedColor = new BABYLON.Color3(0.1, 0.8, 0.1);
                    if (e.key === "2") selectedColor = new BABYLON.Color3(0.4, 0.2, 0.1);
                    if (e.key === "3") selectedColor = new BABYLON.Color3(0.5, 0.5, 0.5);
                }});

                return scene;
            }};

            const scene = createScene();
            canvas.addEventListener("click", () => canvas.requestPointerLock());
            engine.runRenderLoop(() => scene.render());
            window.addEventListener("resize", () => engine.resize());
            window.addEventListener("contextmenu", (e) => e.preventDefault());
        </script>
    </body>
    </html>
    """

@app.route('/')
def index():
    return get_babylon_world()

if __name__ == "__main__":
    app.run()
