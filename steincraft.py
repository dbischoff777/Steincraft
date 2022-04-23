from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc
from numpy import floor
from perlin_noise import PerlinNoise as pn

app = Ursina()

window.color = rgb(0, 200, 111)
window.exit_button.enabled = False
window.fps_counter.visible = False
window.fullscreen = False
window.show_ursina_splash = True

scene.fog_color = color.rgb(255,0,0)
scene.fog_density = 0.02

def input(key):
    if key == "escape":
        quit()

def update():
    pass

terrain = Entity(model=None, collider=None)
pn = pn(octaves=2, seed=2022)
amp = 6
freq = 24

terrainWidth = 32
for i in range (terrainWidth*terrainWidth):
    temp = Entity(model="cube", texture="granite.png")
    temp.x = floor(i / terrainWidth)
    temp.z = floor(i % terrainWidth)
    temp.y = floor(pn([temp.x / freq, temp.z / freq]) * amp)
    temp.parent = terrain

terrain.combine()
terrain.collider = "mesh"
terrain.texture = "granite.png"

player = fpc()
player.cursor.visible = False
player.gravity = 0.5
player.speed = 5
player.x = player.z = 5 
player.y = 12

app.run()