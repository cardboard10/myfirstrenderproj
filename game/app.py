from flask import Flask, request

app = Flask(__name__)

def get_3d_world():
    # We define our 3 block types (colors/textures)
    blocks = {
        "1": "green",  # Grass
        "2": "brown",  # Dirt
        "3": "gray"    # Stone
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
        <script>
          let selectedBlock = '{blocks["1"]}';

          // Listen for keys 1, 2, 3 to change blocks
          window.addEventListener('keydown', (e) => {{
            if (e.key === '1') selectedBlock = '{blocks["1"]}';
            if (e.key === '2') selectedBlock = '{blocks["2"]}';
            if (e.key === '3') selectedBlock = '{blocks["3"]}';
          }});

          AFRAME.registerComponent('block-manager', {{
            init: function () {{
              this.el.addEventListener('click', (evt) => {{
                // If shift is held, break the block
                if (evt.getModifierState('Shift')) {{
                  if (evt.detail.intersection.object.el.id !== 'floor') {{
                    evt.detail.intersection.object.el.remove();
                  }}
                }} else {{
                  // Otherwise, place a block on the face we clicked
                  let pos = evt.detail.intersection.point;
                  let normal = evt.detail.intersection.face.normal;
                  
                  let newBlock = document.createElement('a-box');
                  // Snap to grid logic
                  newBlock.setAttribute('position', {{
                    x: Math.round(pos.x + normal.x * 0.5),
                    y: Math.round(pos.y + normal.y * 0.5),
                    z: Math.round(pos.z + normal.z * 0.5)
                  }});
                  newBlock.setAttribute('color', selectedBlock);
                  newBlock.setAttribute('static-body', '');
                  document.querySelector('a-scene').appendChild(newBlock);
                }}
              }});
            }}
          }});
        </script>
      </head>
      <body>
        <a-scene block-manager cursor="rayOrigin: mouse">
          <a-sky color="#87CEEB"></a-sky>

          <a-plane id="floor" position="0 0 0" rotation="-90 0 0" width="50" height="50" color="#7BC8A4"></a-plane>

          <a-entity id="rig" position="0 1.6 5">
            <a-camera look-controls wasd-controls></a-camera>
          </a-entity>

          <div style="position: fixed; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 10px; font-family: sans-serif;">
            WASD: Move | Mouse: Look | Click: Place Block<br>
            Shift + Click: Break Block<br>
            Keys 1, 2, 3: Change Block Type
          </div>
        </a-scene>
      </body>
    </html>
    """

@app.route('/')
def index():
    return get_3d_world()

if __name__ == "__main__":
    app.run()
