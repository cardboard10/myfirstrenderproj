from flask import Flask, request, jsonify

app = Flask(__name__)

# Memory for your blocks
world_data = []

@app.route('/save', methods=['POST'])
def save_block():
    data = request.json
    world_data.append(data)
    return jsonify({{"status": "saved"}})

@app.route('/break', methods=['POST'])
def break_block():
    data = request.json
    global world_data
    world_data = [b for b in world_data if not (b['x'] == data['x'] and b['y'] == data['y'] and b['z'] == data['z'])]
    return jsonify({{"status": "broken"}})

def get_babylon_world():
    import json
    initial_blocks = json.dumps(world_data)
    
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
            #crosshair {{ position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; margin: -5px 0 0 -5px; border: 2px solid white; border-radius: 50%; pointer-events: none; z-index: 10; }}
        </style>
    </head>
    <body>
        <div id="crosshair"></div>
        <canvas id="renderCanvas"></canvas>
        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);
            let selectedColor = new BABYLON.Color3(0.1, 0.8, 0.1);
            const savedBlocks = {initial_blocks};

            const createScene = function() {{
                const scene = new BABYLON.Scene(engine);
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                // --- FIXED CAMERA SETTINGS ---
                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
                camera.attachControl(canvas, true);
                
                camera.speed = 0.1;               // Slower movement
                camera.inertia = 0;               // No sliding!
                camera.angularSensibility = 3000; // Slower mouse look
                
                camera.keysUp=[87]; camera.keysDown=[83]; camera.keysLeft=[65]; camera.keysRight=[68];
                camera.applyGravity = true; 
                camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(0.4, 1, 0.4);

                new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 100, height: 100}}, scene);
                const gridMat = new BABYLON.GridMaterial("grid", scene);
                gridMat.mainColor = new BABYLON.Color3(0.1, 0.1, 0.1);
                gridMat.gridRatio = 1;
                ground.material = gridMat;
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);
                ground.checkCollisions = true;

                const addBlock = (pos, color, isInitial = false) => {{
                    const box = BABYLON.MeshBuilder.CreateBox("voxel", {{size: 1}}, scene);
                    box.position = pos;
                    const bMat = new BABYLON.StandardMaterial("bMat", scene);
                    bMat.diffuseColor = new BABYLON.Color3(color.r || 0.1, color.g || 0.8, color.b || 0.1);
                    box.material = bMat;
                    box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);
                    box.checkCollisions = true;

                    if (!isInitial) {{
                        fetch('/save', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ x: pos.x, y: pos.y, z: pos.z, color: color }})
                        }});
                    }}
                }};

                savedBlocks.forEach(b => {{
                    addBlock(new BABYLON.Vector3(b.x, b.y, b.z), b.color, true);
                }});

                window.addEventListener("mousedown", (evt) => {{
                    if (document.pointerLockElement !== canvas) return;
                    const pickInfo = scene.pick(canvas.width / 2, canvas.height / 2);
                    if (pickInfo.hit) {{
                        const target = pickInfo.pickedMesh;
                        if (evt.button === 2 || evt.shiftKey) {{ 
                            if (target.name !== "ground") {{
                                fetch('/break', {{
                                    method: 'POST',
                                    headers: {{ 'Content-Type': 'application/json' }},
                                    body: JSON.stringify({{ x: target.position.x, y: target.position.y, z: target.position.z }})
                                }});
                                target.dispose();
                            }}
                        }} else if (evt.button === 0) {{ 
                            const normal = pickInfo.getNormal(true);
                            let newPos = (target.name === "ground") ? 
                                new BABYLON.Vector3(Math.round(pickInfo.pickedPoint.x), 0.5, Math.round(pickInfo.pickedPoint.z)) :
                                target.position.add(normal);
                            addBlock(newPos, selectedColor);
                        }}
                    }}
                }});

                return scene;
            }};

            const scene = createScene();
            canvas.addEventListener("click", () => canvas.requestPointerLock());
            engine.runRenderLoop(() => scene.render());
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
