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
            #crosshair {{
                position: absolute; top: 50%; left: 50%;
                width: 20px; height: 20px;
                margin: -10px 0 0 -10px;
                border: 2px solid white; border-radius: 50%;
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div id="crosshair"></div>
        <canvas id="renderCanvas"></canvas>
        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);
            let selectedColor = new BABYLON.Color3(0, 0.8, 0); // Start with Green

            const createScene = function() {{
                const scene = new BABYLON.Scene(engine);
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
                camera.attachControl(canvas, true);
                camera.keysUp=[87]; camera.keysDown=[83]; camera.keysLeft=[65]; camera.keysRight=[68];
                camera.applyGravity = true; camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(1, 1, 1);

                const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                // Dark Gray Ground
                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 100, height: 100}}, scene);
                const gMat = new BABYLON.StandardMaterial("gMat", scene);
                gMat.diffuseColor = new BABYLON.Color3(0.2, 0.2, 0.2);
                ground.material = gMat;
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);

                // INTERACTION LOGIC
                window.addEventListener("mousedown", (evt) => {{
                    // Only interact if the mouse is locked (game mode)
                    if (document.pointerLockElement !== canvas) return;

                    const pickInfo = scene.pick(canvas.width / 2, canvas.height / 2);
                    
                    if (pickInfo.hit) {{
                        if (evt.button === 2 || evt.shiftKey) {{ 
                            // RIGHT CLICK or SHIFT+CLICK: BREAK
                            if (pickInfo.pickedMesh.name !== "ground") {{
                                pickInfo.pickedMesh.dispose();
                            }}
                        }} else if (evt.button === 0) {{ 
                            // LEFT CLICK: PLACE
                            const normal = pickInfo.getNormal(true);
                            const currentPos = pickInfo.pickedMesh.position;
                            
                            // Calculate new grid position
                            let newPos;
                            if (pickInfo.pickedMesh.name === "ground") {{
                                newPos = new BABYLON.Vector3(
                                    Math.round(pickInfo.pickedPoint.x),
                                    0.5, 
                                    Math.round(pickInfo.pickedPoint.z)
                                );
                            }} else {{
                                newPos = currentPos.add(normal);
                            }}

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

                // Keyboard for Colors
                window.addEventListener("keydown", (e) => {{
                    if (e.key === "1") selectedColor = new BABYLON.Color3(0, 0.8, 0); // Green
                    if (e.key === "2") selectedColor = new BABYLON.Color3(0.5, 0.3, 0.1); // Brown
                    if (e.key === "3") selectedColor = new BABYLON.Color3(0.6, 0.6, 0.6); // Stone
                }});

                return scene;
            }};

            const scene = createScene();
            canvas.addEventListener("click", () => canvas.requestPointerLock());
            engine.runRenderLoop(() => scene.render());
            window.addEventListener("resize", () => engine.resize());
            
            // Disable right-click menu so we can use it for breaking blocks
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
