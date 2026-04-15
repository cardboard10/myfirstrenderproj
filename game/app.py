from flask import Flask, request, jsonify

app = Flask(__name__)

# Memory for your blocks
world_data = []

@app.route('/save', methods=['POST'])
def save_block():
    data = request.json
    world_data.append(data)
    return jsonify({"status": "saved"})

@app.route('/break', methods=['POST'])
def break_block():
    data = request.json
    global world_data
    world_data = [b for b in world_data if not (b['x'] == data['x'] and b['y'] == data['y'] and b['z'] == data['z'])]
    return jsonify({"status": "broken"})

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
            #crosshair {{ position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; margin: -5px 0 0 -5px; border: 2px solid cyan; border-radius: 50%; pointer-events: none; z-index: 10; }}
        </style>
    </head>
    <body>
        <div id="crosshair"></div>
        <canvas id="renderCanvas"></canvas>
        <script>
            const canvas = document.getElementById("renderCanvas");
            const engine = new BABYLON.Engine(canvas, true);
            let selectedColor = new BABYLON.Color3(0, 1, 1); // Neon Cyan
            const savedBlocks = {initial_blocks};

            const createScene = function() {{
                const scene = new BABYLON.Scene(engine);
                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());

                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
                camera.attachControl(canvas, true);
                
                camera.speed = 0.4;               // Increased speed from slow-crawl
                camera.inertia = 0;               
                camera.angularSensibility = 2000; 
                
                camera.keysUp=[87]; camera.keysDown=[83]; camera.keysLeft=[65]; camera.keysRight=[68];
                camera.applyGravity = true; 
                camera.checkCollisions = true;
                camera.ellipsoid = new BABYLON.Vector3(0.4, 1, 0.4);

                new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

                const ground = BABYLON.MeshBuilder.CreateGround("ground", {{width: 200, height: 200}}, scene);
                const gridMat = new BABYLON.GridMaterial("grid", scene);
                gridMat.mainColor = new BABYLON.Color3(0.05, 0.05, 0.1); 
                gridMat.lineColor = new BABYLON.Color3(0, 1, 1); // Bright Cyan Lines
                gridMat.gridRatio = 1;
                ground.material = gridMat;
                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);

                const addBlock = (pos, color, isInitial = false) => {{
                    const box = BABYLON.MeshBuilder.CreateBox("voxel", {{size: 1}}, scene);
                    box.position = pos;
                    const bMat = new BABYLON.StandardMaterial("bMat", scene);
                    bMat.emissiveColor = color; // Makes them glow like Tron
                    box.material = bMat;
                    box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);
                    box.checkCollisions = true;

                    if (!isInitial) {{
                        fetch('/save', {{
                            method: 'POST',
