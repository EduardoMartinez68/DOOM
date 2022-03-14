#inferfaz 3d
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController #para ver el mundo en 3d

app=Ursina()

#crear a un jugador 

class Jugador(Entity):
    
    #caracteristicas del jugador 
    velocidad_jugador=1

	#caracteristicas de la camara 
   
    def __init__(self,position=(0,0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              collider='box',
              texture='white_cube',
              color=color.color(255,255,255),
              scale=1,
              highlight_color=color.rgb(43, 43, 43),

              )
    def moverCamara(self):
    	angulo=0
    	velocidad_giro=67*time.dt

    	if held_keys['d']:
    		angulo=velocidad_giro
    	elif held_keys['a']:
    		angulo=-velocidad_giro

        #arriba y abajo
    	camera.rotation=(camera.rotation.x,camera.rotation.y+angulo,camera.rotation.z) 

    def caminar(self):

    	#direcion de movimiento
    	anguloRotacion=camera.rotation[1] 

    	#redondear cordenadas del jugador 
    	X=round(self.x)
    	Y=round(self.y)

    	#movimiento 
    	


        #saber a donde se dirigue el personaje 
        direction=Vec3(camera.rotation)
    	origin = self.world_position + (self.up*.5)
    	hit_info = raycast(origin , direction, ignore=(self,), distance=3, debug=True)

    	#comprobar que me estoy moviendo
    	veloz=20
    	velocidad_jugador=0 
    	if held_keys['w']:
    		velocidad_jugador=veloz
    	if held_keys['s']:
    		velocidad_jugador=-veloz

        #comprobar que no hay nadie enfrente mio y avanzar 
    	if not hit_info.hit:
    		self.position +=direction * velocidad_jugador * time.dt
    		camera.position=self.position




    def update(self):
    	self.caminar()
    	self.moverCamara()





jg=Jugador(position=(0,2,0))
camera.rotation=(0,0,0)


class Voxel(Button):
    def __init__(self,position=(0,0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              origin_y=0.5,
              collider='box',
              texture='white_cube',
              color=color.color(0,0,random.uniform(0.9,1)),
              scale=1,
              highlight_color=color.rgb(43, 43, 43),

              )

ancho=20
largo=20
def CrearNivel(ancho,largo):
    for y in range(largo):
        for x in range(ancho):
            voxel=Voxel(position=(x,0,y))

CrearNivel(ancho,largo)
#mantener la pantalla encendida
app.run()