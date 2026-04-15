from flask import Flask

app = Flask(__name__)

def get_3d_world():
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-physics-system@v4.2.2/dist/aframe-physics-system.min.js"></script>
        
        <script>
          // 1 = Grass, 2 = Dirt, 3 = Stone
          let selectedColor = 'green';
          
          window.addEventListener('keydown', (e) => {{
            if (e.key === '1') selectedColor = 'green';
            if (e.key === '2') selectedColor = '#8B4513'; // SaddleBrown
            if (e.key === '3') selectedColor = 'gray';
          }});

          // The logic to place/break blocks
          AFRAME.registerComponent('click-to-build', {{
            init: function () {{
              this.el.addEventListener('click', (evt) => {{
                let targetEl = evt.detail.intersection.object.el;
                
                // SHIFT + CLICK = BREAK
                if (evt.getModifierState('Shift')) {{
                  if (targetEl.id !== 'ground') {{
                    targetEl.parentNode.removeChild(targetEl);
                  }}
                }} 
                // REGULAR CLICK = PLACE
                else {{
                  let pos = evt.detail.intersection.point;
                  let normal = evt.detail.intersection.face.normal;
                  
                  // Calculate grid position (snapping to 1x1x1 cubes)
                  let newPos = {{
                    x: Math.round(pos.x + normal.x * 0.5),
                    y: Math.round(pos.y + normal.y * 0.5),
                    z: Math.round(pos.z + normal.z * 0.5)
                  }};

                  let newBlock = document.createElement('a-box');
                  newBlock.setAttribute('position', newPos);
                  newBlock.setAttribute('color', selectedColor);
                  newBlock.setAttribute('static-body', ''); // Makes it a solid wall
                  newBlock.setAttribute('class', 'clickable');
                  this.el.sceneEl.appendChild(newBlock);
                }}
              }});
            }}
          }});
        </script>
      </head>
      <body>
        <a-scene physics="debug: false" click-to-build cursor="rayOrigin: mouse">
          
          <a-sky color="#87CEEB"></a-sky>

          <a-plane id="ground" static-body rotation="-90 0 0" width="100" height="100" color="#228B22"></a-plane>

          <a-entity id="player" movement-controls="fly: false" kinematic-body position="0 1.6 4">
            <a-entity camera look-controls position="0 1.6 0"></a-entity>
          </a-entity>

          <a-box static-body position="-1 0.5 -3" color="gray"></a-box>
          <a-box static-body position="0 0.5 -3" color="green"></a-box>
          <a-box static-body position="1 0.5 -3" color="#8B4513"></a-box>

        </a-scene>

        <div style="position:fixed; bottom:20px; left:20px; color:white; font-family:sans-serif; background:rgba(0,0,0,0.5); padding:10px;">
            <b>Controls:</b> WASD to Walk | Click to Place | Shift+Click to Break<br>
            <b>Blocks:</b> 1: Grass | 2: Dirt | 3: Stone
        </div>
      </body>
    </html>
    """

@app.route('/')
def index():
    return get_3d_world()

if __name__ == "__main__":
    app.run()
