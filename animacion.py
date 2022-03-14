from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController #para ver el mundo en 3d


app=Ursina()

class Pistola(Entity):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/pistola/pistola'
    image_speed=15
    dimensiones=0.9

    #posicion del la mano en pantalla
    xInicio=0
    yInicio=-.05
    cordenadas=(xInicio,yInicio)
    largo_imagen=.31

    #animacion de movimiento
    lado='derecha'
    image_speed=15

    #animacion recarca
    imagen_movimiento=True
    ruido='audio/pistola.wav'

    #cambiar arma
    armaJugador=1
    activar=True #false
    inicio=True

    #caracteristicas disparo
    disparar=True
    alarma=[.3]

    def __init__(self):
        super().__init__(
    #animacion del personaje
    animacion=Animation(
                      self.sprite_index,
                      parent=camera.ui,
                      fps=self.image_speed,
                      scale=self.dimensiones, #dimensiones
                      position=Vec2(self.xInicio,self.yInicio),
                      rotation=Vec3(0,0,0),
                      loop=False,  #si se repetira la imagen
                      autoplay=True) #encender o apagar
                      )


    #animacion de la pistola
    def AnimacionMano(self):
        #print(not self.animacion.resume)
        limit=.25
        animacion_veloz=.8*time.dt
        #animacion a la derecha
        if (self.lado=='derecha'):
            if (self.animacion.x<limit):
                self.animacion.x+=animacion_veloz
            else:
                self.lado='izquierda'

        #animacion a la izquierda
        elif (self.lado=='izquierda'):
            if (self.animacion.x>-limit):
                self.animacion.x-=animacion_veloz
            else:
                self.lado='derecha'

        #animacion de arriba y abajo
        self.animacion.y=abs(self.animacion.x)-self.largo_imagen

    #disparar
    def input(self,key):
        if key=='left mouse down' and self.activar==True and self.disparar==False:
            Audio(self.ruido)
            self.animacion.start()
            self.disparar=True

        self.cambiar_arma(key)

    #caminar
    def Caminar(self):
        #comprobar si esta pulsando una de las teclas de movimiento
        jugador_moviendose=held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']

        #comprobar si estas caminando y no has disparado
        if (jugador_moviendose==True and self.disparar==False):
             self.AnimacionMano()
        else:
            #quedar en la mitad de la pantalla
             self.animacion.x=self.xInicio
             self.animacion.y=self.yInicio
             self.lado='derecha'

             #si dispararte activar la alarma
             if self.disparar==True:
                 if self.alarma[0]>0:
                      self.alarma[0]-=time.dt
                 else:
                     self.alarma[0]=.3
                     self.disparar=False

    #animacion de mano para desbloquearla
    #subir el arma
    def subir(self):
        if self.animacion.y<self.yInicio:
            self.animacion.y+=time.dt*2.5
        else:
            self.activar=True

    def cambiar_arma(self,key):
        #comprobar si cambie de arma
        cambiarArma=(key=='0' or key=='1' or key=='2' or key=='3')

        if cambiarArma:
            if key==str(self.armaJugador):
                self.inicio=True
            else:
                self.activar=False
                self.inicio=False

    def Actualizar(self):
        #comprobar si tenemos selecionada el arma
        if self.activar==True:
            #mano
            self.Caminar()
        else:
            if self.inicio==False:
                #bajar el arma
                if self.animacion.y>self.yInicio-.5: #0.4
                    self.animacion.y-=time.dt*2.5
            else:
                self.subir()


#pistola=Pistola()
newPlayer=FirstPersonController()

def update():
    pass
    #pistola.Actualizar()




app.run()
