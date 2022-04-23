from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc
from numpy import floor
from numpy import abs
from perlin_noise import PerlinNoise as pn
import time

app = Ursina()

window.color = rgb(0, 200, 111)
window.exit_button.enabled = False
window.fps_counter.visible = False
window.fullscreen = False
window.show_ursina_splash = True

prevTime = time.time()

scene.fog_color = color.rgb(0,222,0)
scene.fog_density = 0.02

def input(key):
    if key == "escape":
        quit()

def update():
    global prevZ, prevX, prevTime
    if abs(player.z - prevZ) > 1 or \
        abs(player.x - prevX > 1):
        generateShell()

    if time.time() - prevTime > 0.5:    
        generateSubsets()
        prevTime = time.time()

pn = pn(octaves=2, seed=2022)
amp = 32
freq = 100
terrain = Entity(model=None, collider=None)
terrainWidth = 100
subWidth = terrainWidth
subsets = []
subCubes = []
sci = 0 #subCube index
currentSubset = 0

#Instantiate our ghost subset cubes
for i in range(subWidth):
    bud = Entity(model="cube")
    subCubes.append(bud)

#Instantiate our empty subsets
for i in range(int((terrainWidth * terrainWidth) / subWidth)):
    bud = Entity(model=None)
    bud.parent = terrain
    subsets.append(bud)

def generateSubsets():
    global sci, currentSubset, freq, amp
    if currentSubset >= len(subsets): 
        finishTerrain()
        return

    for i in range(subWidth):
        x = subCubes[i].x = floor((i+sci)/terrainWidth)
        z = subCubes[i].z = floor((i+sci)%terrainWidth)
        y = subCubes[i].y = floor(pn([x / freq, z / freq]) * amp)
        subCubes[i].parent = subsets[currentSubset]
        subCubes[i].color = color.green
        subCubes[i].visible = False

    subsets[currentSubset].combine(auto_destroy=False)    
    subsets[currentSubset].texture = "granite.png"

    sci += subWidth
    currentSubset += 1

terrainFinished = False
def finishTerrain():
    global terrainFinished
    if terrainFinished == True: return
    application.pause()
    terrain.combine()
    terrainFinished = True
    player.y = 32
    terrain.texture = "granite.png"
    application.resume()

shell_cubes = []
shellWidth = 30
for i in range(shellWidth*shellWidth):
    buddy = Entity(model="cube", collider="box")
    buddy.visible = False
    shell_cubes.append(buddy)

def generateShell():
    global shellWidth, amp, freq
    for i in range(len(shell_cubes)):
        x = shell_cubes[i].x = floor((i / shellWidth) + player.x - 0.5 * shellWidth)
        z = shell_cubes[i].z = floor((i % shellWidth) + player.z - 0.5 * shellWidth)
        shell_cubes[i].y = floor(pn([x / freq, z / freq]) * amp)

player = fpc()
player.cursor.visible = False
player.gravity = 0.5
player.speed = 5
player.x = player.z = 5 
player.y = 12
prevZ = player.z
prevX = player.x

chickenModel = load_model("chicken.obj")
pollo = Entity(
    model=chickenModel, 
    scale = 0.1,
    x = 22, y = 7.1, z = 16, 
    texture = "chicken.png",
    double_sided = True
)

generateShell()

app.run()