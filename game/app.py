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
                camera.keysUp=[87]; camera.keysDown=[83]; camera.keysLeft=[65]; camera.keysRight=[68];
                camera.applyGravity = true; camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(0.5, 1, 0.5); // Thinner body for easier movement

                const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                // --- THE GRID GROUND ---
                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 100, height: 100}}, scene);
                
                // Create the Grid Material
                const gridMat = new BABYLON.GridMaterial("grid", scene);
                gridMat.mainColor = new BABYLON.Color3(0.1, 0.1, 0.1); // Dark background
                gridMat.lineColor = new BABYLON.Color3(0.3, 0.3, 0.3); // Gray lines
                gridMat.gridRatio = 1; // One line every 1 unit (perfect for 1x1 blocks)
                ground.material = gridMat;
                
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);

                // --- BUILD LOGIC ---
                window.addEventListener("mousedown", (evt) => {{
                    if (document.pointerLockElement !== canvas) return;

                    const pickInfo = scene.pick(canvas.width / 2, canvas.height / 2);
                    
                    if (pickInfo.hit) {{
                        const target = pickInfo.pickedMesh;

                        if (evt.button === 2 || evt.shiftKey) {{ 
                            // BREAK
                            if (target.name !== "ground") target.dispose();
                        }} else if (evt.button === 0) {{ 
                            // PLACE
                            const normal = pickInfo.getNormal(true);
                            let newPos;

                            if (target.name === "ground") {{
                                // Snap to ground grid
                                newPos = new BABYLON.Vector3(
                                    Math.round(pickInfo.pickedPoint.x),
                                    0.5, 
                                    Math.round(pickInfo.pickedPoint.z)
                                );
                            }} else {{
                                // Stack on other blocks
                                newPos = target.position.add(normal);
                            }}

                            const box = BABYLON.MeshBuilder.CreateBox("voxel", {{size
