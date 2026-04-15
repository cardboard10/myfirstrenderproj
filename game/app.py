from flask import Flask

app = Flask(__name__)

def get_babylon_world():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Babylon.js Voxel Engine</title>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        <script src="https://cdn.babylonjs.com/cannon.js"></script>
        <style>
            html, body {{ overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; }}
            #renderCanvas {{ width: 100%; height: 100%; touch-action: none; }}
            #ui {{ position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 10px; font-family: sans-serif; pointer-events: none; }}
        </style>
    </head>
    <body>
        <div id="ui">
            <b>Babylon Engine</b><br>
            WASD: Move | Mouse: Look | Click: Place<br>
            Shift + Click: Break | 1, 2, 3: Change Color
        </div>
        <canvas id="renderCanvas"></canvas>

        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);
            let selectedColor = new BABYLON.Color3(0, 1, 0); // Green

            const createScene = function () {{
                const scene = new BABYLON.Scene(engine);
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                // Camera (First Person)
                const camera = new BABYLON.FreeCamera("camera1", new BABYLON.Vector3(0, 5, -10), scene);
                camera.setTarget(BABYLON.Vector3.Zero());
                camera.attachControl(canvas, true);
                
                // Minecraft-style controls
                camera.keysUp.push(87);    // W
                camera.keysDown.push(83);  // S
                camera.keysLeft.push(65);  // A
                camera.keysRight.push(68); // D
                camera.applyGravity = true;
                camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(1, 1, 1);

                const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                // The Ground
                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 50, height: 50}}, scene);
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0, restitution: 0.1 }}, scene);
                ground.checkCollisions = true;

                // Click Logic
                window.addEventListener("click", function () {{
                    const pickRect = scene.pick(scene.pointerX, scene.pointerY);
                    if (pickRect.hit) {{
                        if (window.event.shiftKey) {{
                            // BREAK
                            if (pickRect.pickedMesh.name !== "ground") {{
                                pickRect.pickedMesh.dispose();
                            }}
                        }} else {{
                            // PLACE
                            const normal = pickRect.getNormal(true);
                            const pos = pickRect.pickedMesh.position.add(normal);
                            
                            // If clicking ground, use hit point
                            let finalPos = pickRect.pickedMesh.name === "ground" ? 
                                new BABYLON.Vector3(Math.round(pickRect.pickedPoint.x), 0.5, Math.round(pickRect.pickedPoint.z)) :
                                new BABYLON.Vector3(Math.round(pos.x), Math.round(pos.y), Math.round(pos.z));

                            const box = BABYLON.MeshBuilder.CreateBox("box", {{size: 1}}, scene);
                            box.position = finalPos;
                            const mat = new BABYLON.StandardMaterial("mat", scene);
                            mat.diffuseColor = selectedColor;
                            box.material = mat;
                            
                            box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);
                            box.checkCollisions = true;
                        }}
                    }}
                }});

                // Color Selection
                window.addEventListener("keydown", (e)
