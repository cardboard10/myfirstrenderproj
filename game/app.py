@@ -1,139 +1,131 @@


from flask import Flask, request, jsonify


import json


from flask import Flask



app = Flask(__name__)


world_data = []





@app.route('/save', methods=['POST'])


def save_block():


    try:


        data = request.json


        world_data.append(data)


        return jsonify({"status": "ok"})


    except:


        return jsonify({"status": "error"}), 400





@app.route('/break', methods=['POST'])


def break_block():


    global world_data


    try:


        data = request.json


        world_data = [b for b in world_data if not (b['x'] == data['x'] and b['y'] == data['y'] and b['z'] == data['z'])]


        return jsonify({"status": "ok"})


    except:


        return jsonify({"status": "error"}), 400





def get_babylon_world():


    initial_blocks = json.dumps(world_data)


    return f"""





def get_game_html():


    return """

    <!DOCTYPE html>

    <html>

    <head>


        <title>Voxel Builder Template</title>

        <script src="https://cdn.babylonjs.com/babylon.js"></script>


        <script src="https://cdn.babylonjs.com/cannon.js"></script>


        <script src="https://cdn.babylonjs.com/materialsLibrary/babylonjs.materials.min.js"></script>


        

        <style>


            html, body {{ overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; }}


            #renderCanvas {{ width: 100%; height: 100%; outline: none; }}


            #crosshair {{ position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; margin: -5px 0 0 -5px; border: 2px solid cyan; border-radius: 50%; pointer-events: none; z-index: 10; }}


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


            let selectedColor = new BABYLON.Color3(0, 1, 1);


            const savedBlocks = {initial_blocks};


            let blocksArray = []; // We keep track of blocks here so we can clear them




            const createScene = function() {{


            const createScene = function() {

                const scene = new BABYLON.Scene(engine);


                scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), new BABYLON.CannonJSPlugin());


                scene.clearColor = new BABYLON.Color4(0.05, 0.05, 0.05, 1); // Dark background




                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);


                // CAMERA SETTINGS


                const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 5, -15), scene);

                camera.attachControl(canvas, true);


                


                // CRITICAL SPEED FIX


                camera.speed = 0.02; 


                camera.inertia = 0; 


                camera.angularSensibility = 5000; 


                


                camera.speed = 0.1;   // Change this to walk faster/slower


                camera.inertia = 0;   // Set to 0 to stop sliding

                camera.keysUp=[87]; camera.keysDown=[83]; camera.keysLeft=[65]; camera.keysRight=[68];


                camera.applyGravity = true; 


                camera.checkCollisions = true;


                camera.ellipsoid = new BABYLON.Vector3(0.4, 1, 0.4);



                new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);




                // Thick Ground for perfect clicking


                const ground = BABYLON.MeshBuilder.CreateBox("ground", {{width: 200, height: 0.5, depth: 200}}, scene);


                ground.position.y = -0.25; 


                const gridMat = new BABYLON.GridMaterial("grid", scene);


                gridMat.mainColor = new BABYLON.Color3(0.02, 0.02, 0.05); 


                gridMat.lineColor = new BABYLON.Color3(0, 1, 1);


                gridMat.gridRatio = 1;


                ground.material = gridMat;


                ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);





                const addBlock = (pos, color, shouldSave = true) => {{


                    const box = BABYLON.MeshBuilder.CreateBox("voxel", {{size: 1}}, scene);


                    box.position = pos;


                    const bMat = new BABYLON.StandardMaterial("bMat", scene);


                    bMat.emissiveColor = color;


                    box.material = bMat;


                    box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, {{ mass: 0 }}, scene);


                    box.checkCollisions = true;





                    if (shouldSave) {{


                        fetch('/save', {{


                            method: 'POST',


                            headers: {{ 'Content-Type': 'application/json' }},


                            body: JSON.stringify({{ x: pos.x, y: pos.y, z: pos.z, color: color }})


                        }});


                    }}


                }};





                savedBlocks.forEach(b => addBlock(new BABYLON.Vector3(b.x, b.y, b.z), b.color, false));





                window.addEventListener("mousedown", (evt) => {{


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


                    


                    blocksArray.push(block); // Store it for later


                };





                // CLICK TO BUILD (Standard Mechanic)


                window.addEventListener("mousedown", (e) => {

                    if (document.pointerLockElement !== canvas) return;


                    const pickInfo = scene.pick(canvas.width / 2, canvas.height / 2);


                    if (pickInfo.hit) {{


                        const target = pickInfo.pickedMesh;


                        if (evt.button === 2) {{ 


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


                    if (e.button === 0) { // Left Click


                        const pick = scene.pick(canvas.width/2, canvas.height/2);


                        if (pick.hit) {


                            const spawnPos = pick.pickedMesh.position.add(pick.getNormal(true));


                            window.spawnBlock(spawnPos.x, spawnPos.y, spawnPos.z, "#00FFFF"); // Cyan


                        }


                    }


                });




                return scene;


            }};


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


            window.addEventListener("contextmenu", (e) => e.preventDefault());


            window.addEventListener("resize", () => engine.resize());

        </script>

    </body>

    </html>

    """



@app.route('/')

def index():


    return get_babylon_world()


    return get_game_html()



if __name__ == "__main__":

    app.run()
