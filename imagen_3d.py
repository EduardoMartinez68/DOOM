#inferfaz 3d
from ursina import *
from ursina.application import pause
from ursina.prefabs.first_person_controller import FirstPersonController #para ver el mundo en 3d
from ursina.collision_zone import *
#traer cosas
import os
import random
#importar mi lenguaje
import funciones
import leer_nivel
import fisica

#activar el juego
app=Ursina()
app.title='DOOM'
app.borderless=True

''''---------------funciones compartidas--------------'''
def Animacion(self):
    #si no es la ultima imagen seguir aumentando
    if(self.image_index<self.numero_imagenes):
        self.image_index+=self.image_speed
        self.texture=self.sprite_index[floor(self.image_index)]
        return False
    else: #si es la ultima imagen volver a la primera
        self.image_index=0
        self.texture=self.sprite_index[0]
        return True

def CargarImagen(imagenes):
    sprite_index=[]
    #cargar las imagenes
    for image_index in imagenes:
        sprite=load_texture(image_index)
        sprite_index.append(sprite)

    return sprite_index

def EliminarObjeto(objeto):
    destroy(objeto) 

def caracteristicas():
    #caracteristica del sprite
    imagenes=[]
    sprite_index=[]
    image_index=0
    image_speed=0
    dimensiones=(0,0)
    numero_imagenes=len(imagenes)-1
    color_imagen=color.rgb(255, 255, 255)

    #caracteristicas del objeto
    life=0
    speed=0
    direction=0
    caminar=False

    #caracteristicas del personaje
    ataque=''
    disparar=True
    fuerza_ataque=0
    alarma=[]

def ActivarObjeto(self,key,distancia):
    if key=='enter' and funciones.colision_objeto(newPlayer,self,distancia):
        self.encender=True

def ColisionDeAtaque(self,newPlayer,distanciaColision):
    colisionJugador=distance(self,newPlayer)
    if colisionJugador<distanciaColision:
        Bajar_o_subir_Vida(-1)
        return True
    else:
        return False

def BalaChoca(self,key):
        #comprobar si estamos apuntando al objeto y su opacidad es 1
        if self.hovered and self.alpha==1:
            global arma
            distancia=distance(nv.newPlayer,self) 

            #ver si estoy disparando y no tengo el arma 4
            if key=='left mouse down' and not arma==4:
                #obtener las caracteristicas del arma
                global miraArma
                global municion

                #ver si la bala alcanza al jugador
                if distancia<miraArma and municion[arma]>0:
                    self.herida()

            #ver si estoy pateando y si lo alcanzo con el pie 
            elif key=='e' and distancia<3:
                self.herridaPatada()

''''----------------------funciones de menu---------------------'''
#reproducion de sonidos
def ReproducirAudio(sonido):
    ruido=Audio(sonido)
    ruido.volumen=1

def ReproducirMusica(Musica):
    Audio(Musica)

''''----------------------clases globales---------------------'''
#clase de objetos
class Objeto(Entity):
    #caracteristica del sprite
    imagenes=[]
    sprite_index=[]
    image_index=0
    image_speed=0
    numero_imagenes=len(imagenes)-1

    brillo=255
    color_imagen=color.rgb(brillo, brillo, brillo)
    dimensiones=(0,0,0)
    transparencia=1

    #caracteristica de eventos
    vida=0
    solido=False
    alarma=[]

    #caracteristicas de fisica
    vspeed=.25
    origen=.5 #para saber donde lanzar el rayo en la gravedad

class Objeto_enemigos(Objeto):
    #caracteristicas del objeto
    life=0
    speed=0
    direction=0
    caminar=False

    #caracteristicas del personaje
    ataque=''
    disparar=False
    fuerza_ataque=0
    alarma=[]

#dibujar cosas en pantalla
class draw_texto(Text):
    #crear el modelo
    def __init__(self,x,y,dato,escala,color): #2
        super().__init__(
            parent=camera.ui,
            text=str(dato),
            font='fuentes/AmazDooMLeft.ttf',
            scale=escala,
            color=color,
            position=Vec2(x,y) #Vec2
        )

class draw_sprite(Entity):
    def __init__(self,x,y,sprite,dimensiones=(0,0,0)):
        super().__init__(
            parent=camera.ui,
            model='quad',
            texture=sprite,
            scale=dimensiones,
            color=color.white,
            rotation=Vec3(0,0,0), #girar la arma
            position=Vec2(x,y) #posiciones (x,y)
        )

class draw_rectangulo(Entity):
    def __init__(self,x,y,ancho,largo,color):
        super().__init__(
            parent=camera.ui,
            model='quad',
            color=color,
            origin=(-.5,-.5),
            position=(x,y),
            scale_max=ancho,
            scale=(ancho,largo),
        )

''''----------------------Definir las clases especiales---------------------'''
class Objeto_2d(Objeto):
    #caracteristica del sprite
    image_speed=0.5
    dimensiones=(2,3)

    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='quad',
            collider='box',
            collision_cooldown=1,
            #origin_y=0,
            rotation=Vec3(0,0,0),
            texture=self.sprite_index[self.image_index],
            scale=self.dimensiones,
            color=self.color_imagen
        )

class Objeto_3d(Objeto):
    #caracteristica del sprite
    image_speed=0.5
    dimensiones=(2,3)

    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            collider='box',
            collision_cooldown=1,
            rotation=Vec3(0,0,0),
            texture=self.sprite_index[self.image_index],
            scale=self.dimensiones,
            color=self.color_imagen
        )




    def update(self):
        Animacion(self)

class transicion(Entity):
    tiempo=0.049*2.5
    def __init__(self,color=0):
        super().__init__(
            parent=camera.ui,
            position=(0,1,0),
            model='cube', #quad
            rotation=Vec3(0,0,0),
            texture='cube_white',
            color=color,
            scale=4,
            alpha=0.3
        )

    def update(self):
        #tiempo para desaparecer
        if self.tiempo>0.049:
            self.tiempo-=0.049
        else:
            EliminarObjeto(self)

class CuadroTexto(Entity):
    X=-0.75
    Y=-0.4
    mensaje='como estas amiga mia. Yo estoy muy bien me enorgullesco'

    #crear lo necesario para el cuadro
    def __init__(self):
        super().__init__(
                        cuadroLimite=draw_rectangulo(x=self.X,y=self.Y,ancho=1.51,largo=0.26,color=color.rgb(255, 255, 255)),
                        cuadroFondo=draw_rectangulo(x=self.X+0.005,y=self.Y+0.005,ancho=1.5,largo=0.25,color=color.rgb(0,0,0)),
                        texto=draw_texto(x=self.X+0.05,y=self.Y+0.23,dato=self.mensaje,escala=1.2,color=color.rgb(255, 255, 255))
                        )

    def input(self,key):
        if key=='enter':
            #destruir el mensaje
            destroy(self.cuadroLimite)
            destroy(self.cuadroFondo)
            destroy(self.texto)
            destroy(self)

''''--------jugador-------'''
vida=100

municion=[1,100,20,30,10,1]
arma=0
poderArma=0
armaMano=0
miraArma=10
zoom=0

cajaInventario=[]
class CaracteristicasJugador(Entity):
    jugador=0
    solido=True
    AumentaVelocidad=False
    alarma=[2]
    armaJugador=1
    lado='derecha'

    #sprintrar
    sprintar=True
    sprite_index_pie_sprintar=['sprite/armas/patadas/Sprintar_0.png','sprite/armas/patadas/Sprintar_1.png','sprite/armas/patadas/Sprintar_2.png']
    sprite_index_pie_patada=['sprite/armas/patadas/patada_0.png','sprite/armas/patadas/patada_1.png','sprite/armas/patadas/patada_2.png','sprite/armas/patadas/patada_2.png']
    image_speed_pie=0
    pie=draw_sprite(0,-.1,sprite_index_pie_sprintar,(.8,.8,0))    
    patada=False
    pie.visible=False

    ruido_sprintar='audio/armas/espintar.mp3'
    audio_esprintar=Audio(ruido_sprintar,loop=False,volumen=.5)
    audio_esprintar.pause() 

    #audios 
    ruido_herrida='audio/billy/billy herrido.mp3'
    audio_herida=Audio(ruido_herrida,loop=True) 
    audio_herida.pause() 

    def input(self,key):
        #print(key)
        if key=='escape':
            exit()

    #animacion de la camara cuando corre a mucha velocidad
    def AnimacionCamaraVelocidad(self):
        self.AnimacionCamaraMoviemiento()
        self.AnimacionCamaraZoom()

    def AnimacionCamaraZoom(self):
        global zoom
        zoom=-.125 #.25
        camera.position=(camera.position.x,camera.position.y,1.25)

    def AnimacionCamaraMoviemiento(self):
        limit=.25
        animacion_veloz=0.0625

        #animacion a la derecha
        if (self.lado=='derecha'):
            if (camera.x<limit):
                camera.x+=animacion_veloz
            else:
                self.lado='izquierda'

        #animacion a la izquierda
        elif (self.lado=='izquierda'):
            if (camera.x>-limit):
                camera.x-=animacion_veloz
            else:
                self.lado='derecha'

        #animacion de arriba y abajo
        camera.y=abs(camera.x)
    
    #animacion de camara al deslizarse por el piso
    def AnimacionPieSprintar(self):
        if self.image_speed_pie<3:
            self.pie.texture=self.sprite_index_pie_sprintar[int(self.image_speed_pie)]
            self.pie.position=Vec2(0,-.1)
            self.pie.scale=(.8,.8,0)
            self.pie.visible=True #visualizar el pie 
            self.image_speed_pie+=0.6
    
    def AnimacionCamaraSprintar(self):
        self.AnimacionPieSprintar()
        if(camera.position[1]>-1.3):
            camera.position=(0,camera.position[1]-.5,0)
        
        #ir bajando la velocidad 
        if(nv.newPlayer.speed>0):
            nv.newPlayer.speed-=.2
        else:
            nv.newPlayer.speed=0
            self.sprintar=False
    
    def AnimacionPatada(self):
        if self.patada==True: 
            if self.image_speed_pie<3 and self.sprintar==True:
                self.pie.scale=(.5,.5,0)
                self.pie.position=Vec2(.15,-.25) #15            
                self.pie.visible=True 
                self.image_speed_pie+=0.4
                self.pie.texture=self.sprite_index_pie_patada[int(self.image_speed_pie)]
            else:
                self.patada=False
                self.ApagarPie()
    
    def ReiniciarPie(self):
        #poder volver sprintar
        self.sprintar=True

        #reiniciar pie 
        if self.patada==False and self.sprintar==True:
            self.ApagarPie()

    def ApagarPie(self):
        #apagar las caracteristicas del pie 
        self.pie.visible=False
        self.image_speed_pie=0 #volver iniciar los fotogramas 

        self.patada=False

    #velocidad del jugador
    def limitar_velocidad(self,velocidad_inicio,velocidad_final):
        #comprobar si puedo acelerar mas
        if nv.newPlayer.speed<velocidad_final:
            nv.newPlayer.speed+=.125
        else:
            nv.newPlayer.speed=velocidad_final

    def velocidad_del_jugador(self):
        global zoom
        velocidad_inicio=4
        velocidad_final=7
        #comprobar si me estoy moviendo
        Moverme=held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
        if Moverme:
            #comprobar si aumento la velocidad
            if held_keys['shift']:
                #ampliar la persepsion de la camara cuando corra
                camera.fov=105

                #sprintar
                if held_keys['e']:
                    self.AnimacionCamaraSprintar()
                    if self.audio_esprintar.playing==0:
                        self.audio_esprintar.resume()
                        self.audio_esprintar.playing=1 
                else:
                    if self.sprintar==True:
                        nv.newPlayer.speed=9
                        self.AnimacionCamaraVelocidad()
                        self.ApagarPie()                
            else:
                self.limitar_velocidad(velocidad_inicio,velocidad_final)
                camera.position=(0,0,0)
                zoom=0

                #volver la persepsion de la camara a la normalidad
                camera.fov=90

                #poder volver sprintar
                self.sprintar=True
                self.audio_esprintar.playing=0
                self.ApagarPie()
        else:
            nv.newPlayer.speed=velocidad_inicio
            camera.position=(0,0,0)
            zoom=0

            #volver la persepsion de la camara a la normalidad
            camera.fov=90

            self.ReiniciarPie()
            #soltar una patada
            if held_keys['e']:
                self.patada=True         

    #colisiones
    def colision_piso(self):
        colision=nv.newPlayer.intersects(traverse_target=scene,ignore=(self,),debug=True)
        colision_info=colision.entities

        fisica.gravedad_jugador(nv.newPlayer)

    #audios 
    def ActivarAudioHerido(self):
        if vida<75:
            #comprobar si se esta reproduciendo
            if self.audio_herida.playing==0:
                self.audio_herida.playing=1
                self.audio_herida.resume()

            #actualizar al volumen de la herrida
            self.audio_herida.volume=(75-vida)/37 #75
        else:
            self.audio_herida.playing=0
            self.audio_herida.volume=0

    #caracteristicas del personaje billy y eva
    def CambiarJugador(self):
        if self.jugador==1:
            self.ruido_herrida='audio/eva/Eva herrida.mp3'

    def update(self):
        self.velocidad_del_jugador()
        self.colision_piso()
        self.AnimacionPatada()
        self.ActivarAudioHerido()


''''--------barra de datos del jugador-------'''
#barra de vida, municion, estado
total_vida=.30
porcentaje_barra=(1*total_vida)/100

class BajarVida1(Entity):
    def update(self):
        global porcentaje_barra
        global total_vida
        total_vida-=held_keys['left arrow']*porcentaje_barra
        total_vida+=held_keys['right arrow']*porcentaje_barra

        #bajar vida
        global vida
        vida-=held_keys['left arrow']
        vida+=held_keys['right arrow']

class BarraDatos(Entity):

    #tiempo para cargar la vida 
    golpe=False
    tiempoVida=3

    BajarVida1()
    #dibujar el rostro
    x_vida=-0.75
    y_vida=-0.35 #35

    #si es herrido dibujar imagen de vida 
    pantalla_vida_index=['sprite/barra de vida/herrida pantalla/herrida_pantalla_0.png','sprite/barra de vida/herrida pantalla/herrida_pantalla_1.png','sprite/barra de vida/herrida pantalla/herrida_pantalla_2.png','sprite/barra de vida/herrida pantalla/herrida_pantalla_3.png']
    pantalla_vida=draw_sprite(0,0,pantalla_vida_index[0],(1.8,1,0))
    pantalla_vida.position=(0,0,-1) #hacer que la sangre este encima de las armas

    #dibujar rectangulo negro para encerrar el arma
    x_municion=0.7
    y_municion=y_vida
    fondo_negro2=draw_rectangulo(x=x_municion-0.15,y=-0.465,ancho=0.3,largo=0.12,color=color.rgb(0,0,0))

    #dibujar pistola que esta usando el jugador
    global municion
    sprite_arma=['sprite/etem pistola/arma0.png','sprite/etem pistola/arma1.png','sprite/etem pistola/arma2.png','sprite/etem pistola/arma3.png','sprite/etem pistola/arma3.png','sprite/etem pistola/arma0.png']
    arma_index=CargarImagen(sprite_arma)
    municion_dibujo=draw_sprite(x_municion,y_municion-0.04,arma_index[0],(0.25,0.25,0))

    #municion de pistola
    municion_texto=draw_texto(x_municion,y_municion-0.08,municion,escala=1.4,color=color.rgb(255, 255, 255))

    def ActualizarBarraDatosMunicion(self):
        global municion
        global arma
        self.municion_texto.text=str(municion[arma])
        self.municion_dibujo.texture=self.arma_index[arma]

    def ActualizarBarraDatosVida(self):
        #limitar la vida para que no crezca mas de 100
        global vida
        vida=clamp(vida,0,100)
        #limitar la barra de vida para que no crezca mas de 100
        global total_vida

        #comprobar como la pantalla cambia con la vida 
        vida_limite=100/4
        if(vida<vida_limite):
            self.pantalla_vida.texture=self.pantalla_vida_index[3]
            self.ActualizarSangrePantalla()
        elif(vida>=vida_limite and vida<vida_limite*2):
            self.pantalla_vida.texture=self.pantalla_vida_index[2]
            self.ActualizarSangrePantalla()
        elif(vida>=vida_limite*2 and vida<vida_limite*3):
            self.pantalla_vida.texture=self.pantalla_vida_index[1]
            self.ActualizarSangrePantalla()
        else:
            self.pantalla_vida.texture=self.pantalla_vida_index[0]
            self.pantalla_vida.alpha=1

    def ParpadearDatos(self):
        global municion
        global arma
        #hacer que parpade la municion
        if municion[arma]>0:
            self.municion_texto.color=color.rgb(255, 255, 255)
        else:
            self.municion_texto.color=color.rgb(255, 0, 0)
    
    def ActualizarSangrePantalla(self):
        #animacion para la sangre en pantalla 
        if(self.pantalla_vida.alpha>0):
            self.pantalla_vida.alpha-=.03
        else:
            self.pantalla_vida.alpha=1

    def cargarVida(self):
        if(self.tiempoVida>0):
            self.tiempoVida-=.1
        else:
            global vida
            if vida!=100:
                vida+=.5          
            else:
                self.golpe=False
                vida=100

    def update(self):
        self.ActualizarBarraDatosMunicion()
        self.ActualizarBarraDatosVida()
        #hacer que la vida parpade
        self.ParpadearDatos()

        if self.golpe==True:
            self.cargarVida()
        else:
            self.tiempoVida=10

def Bajar_o_subir_Vida(subir):
    global total_vida
    global porcentaje_barra

    bajar_vida=int(random.uniform(3,6))
    for i in range(bajar_vida):
        total_vida+=porcentaje_barra*subir

    #bajar vida
    global vida
    vida+=bajar_vida*subir

    #activar alarma para volver a subirle la vida
    nv.barra.tiempoVida=10 
    nv.barra.golpe=True


''''--------Armas de jugador-------'''
#armas del jugador
class Arma(Entity):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/pistola/pistola'
    image_speed=15
    dimensiones=0

    #posicion del la mano en pantalla
    xInicio=0
    yInicio=-.05
    largo_imagen=.31
    ancho_imagen=.25
    dimencionesEjes=(0,0,0)

    #animacion de movimiento
    lado='derecha'
    image_speed=15

    #animacion recarca
    imagen_movimiento=True
    ruido='audio/pistola.wav'

    #cambiar arma
    armaJugador=1
    activar=False #false
    inicio=True
    poder=1
    vueltasCambio=0

    #caracteristicas disparo
    disparar=True
    alarma=[.3]
    mira=15
    balas=0

    #animacion del personaje
    def __init__(self):
        super().__init__(
                 animacion=Animation(
                               self.sprite_index,
                               parent=camera.ui,
                               fps=self.image_speed,
                               scale=self.dimensiones, #dimensiones
                               position=Vec2(self.xInicio,self.yInicio),
                               rotation=self.dimencionesEjes,
                               loop=False,  #si se repetira la imagen
                               autoplay=True) #encender o apagar
                      )

    #animacion de la pistola
    def AnimacionMano(self):
        #print(not self.animacion.resume)
        limit=self.ancho_imagen
        velocidad_final=.8*time.dt
        animacion_veloz=((nv.newPlayer.speed*velocidad_final)/7)
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
        global zoom
        self.animacion.y=abs(self.animacion.x)-self.largo_imagen+zoom

    #disparar
    def input(self,key):
        global municion
        if key=='left mouse down' and self.activar==True and self.disparar==False and municion[self.armaJugador]!=5:
            Audio(self.ruido)

            #comprobar que no tengo el cuchillo
            if self.armaJugador!=5:
                municion[self.armaJugador]-=1

            self.animacion.start()
            self.disparar=True
        self.cambiar_arma(key)

    #caminar
    def Caminar(self):
        #comprobar si esta pulsando una de las teclas de movimiento
        jugador_moviendose=held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']

        #comprobar si estas caminando y no has disparado
        if (jugador_moviendose==True and self.disparar==False and nv.caracteristicasJugador.pie.visible==False):
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
        cambiarArma=(key=='1' or key=='2' or key=='3' or key=='4' or key=='5')
        if cambiarArma:
            if key==str(self.armaJugador):
                self.inicio=True
                nv.caracteristicasJugador.armaJugador=self.armaJugador #cambiar la arma del jugador
            else:
                self.activar=False
                self.inicio=False

        elif key=='scroll up' or key=='scroll down' and self.activar==True and self.vueltasCambio<1.5:
            self.vueltasCambio+=1
            #ver cuantas armas tenemos 
            numArmas=len(cajaInventario)

            #preguntar si estoy avanzando 
            if key=='scroll up':
                if self.vueltasCambio>=1.5: 
                    if nv.caracteristicasJugador.armaJugador<numArmas:
                        nv.caracteristicasJugador.armaJugador+=1 
                        self.vueltasCambio=0
                    else:
                        nv.caracteristicasJugador.armaJugador=1
                        self.vueltasCambio=0
            else:
                if self.vueltasCambio>=1:
                    if nv.caracteristicasJugador.armaJugador>1:
                        nv.caracteristicasJugador.armaJugador-=1 
                        self.vueltasCambio=0
                    else:
                        nv.caracteristicasJugador.armaJugador=numArmas
                        self.vueltasCambio=0                                                       


    #la municion que le vas agregar
    def municion(self,aumento):
        global municion
        municion[self.image_index]+=aumento

    #LAS MUNICIONES
    def update(self):
        global arma
        #comprobar si tenemos selecionada el arma
        if self.activar==True:
            global poderArma
            poderArma=self.poder
            #cambiar el tamaño de la mira
            global miraArma
            miraArma=self.mira
            #mano
            self.Caminar()
            arma=self.armaJugador

            #animacion de disparar
            '''
            if (self.disparar==True):
                nv.barra.vida_dibujo.texture=nv.barra.imagenDisparar
            else:
                Animacion(nv.barra)
                nv.barra.vida_dibujo.texture=nv.barra.texture #////'''
        else:
            if self.inicio==False:
                #bajar el arma
                if self.animacion.y>self.yInicio-.5: #0.4
                    self.animacion.y-=time.dt*2.5
            else:
                self.subir()
        
        #comprobar si señalamos la arma que tenemos 
        if nv.caracteristicasJugador.armaJugador==self.armaJugador:
            self.inicio=True
        else:
            self.inicio=False
            self.activar=False
            self.vueltasCambio=0 

class ArmaNormal(Arma):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/pistola/pistola'
    image_speed=15
    dimensiones=0.9

    #posicion del la mano en pantalla
    xInicio=.2
    yInicio=-.07
    largo_imagen=.31
    ancho_imagen=0.125

    #animacion recarca
    ruido='audio/pistola.wav'

    #cambiar arma
    armaJugador=1

    #caracteristicas disparo
    mira=30

class ArmaEscopeta(Arma):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/escopeta/escopeta'
    image_speed=12
    dimensiones=1 #0.6

    #posicion del la mano en pantalla
    xInicio=.3
    yInicio=-.1#-.24
    largo_imagen=0.5

    #animacion recarca
    ruido='audio/escopeta.wav'

    #cambiar arma
    armaJugador=2
    poder=6

    #caracteristicas disparo
    mira=7

class Cuchillo(Arma):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/cuchillo/cuchillo'
    image_speed=15
    dimensiones=0.7

    #posicion del la mano en pantalla
    xInicio=.2
    yInicio=-.15
    largo_imagen=0.4
    ancho_imagen=0.125

    #animacion de movimiento
    image_speed=7

    #animacion recarca
    ruido='audio/cuchillo.wav'

    #cambiar arma
    armaJugador=5
    poder=1

    #caracteristicas disparo
    mira=5

class Vayesta(Arma):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/vayesta/vayesta_disparo/vayesta'
    image_speed=15
    dimensiones=.8

    #posicion del la mano en pantalla
    xInicio=-.1
    yInicio=-.1
    largo_imagen=.4

    #animacion recarca
    ruido='audio/vallesta'

    #cambiar arma
    armaJugador=3
    poder=1

    #caracteristicas disparo
    mira=15

class ManoDinero(Arma):
    #caracteristicas de la imagen
    sprite_index='sprite/armas/dinero/mano_dinero'
    dimensiones=1

    #posicion del la mano en pantalla
    xInicio=.3
    yInicio=-.1
    largo_imagen=0.4

    #animacion de movimiento
    image_speed=7

    #cambiar arma
    armaJugador=4
    poder=0

    #caracteristicas disparo
    mira=3

def ActivarPistola(arma):
    #bloquear todas lar armas que tenga actualmente en el inventario
    for mano in cajaInventario:
        mano.activar=False
        mano.inicio=False

    #agregar la nueva arma
    if arma==0:
        manoArmaCuchillo=Cuchillo()
        cajaInventario.append(manoArmaCuchillo)
    elif arma==1:
        manoArmaNormal=ArmaNormal()
        cajaInventario.append(manoArmaNormal)
    elif arma==2:
        manoArmaEscopeta=ArmaEscopeta()
        cajaInventario.append(manoArmaEscopeta)
    elif arma==3:
        manoArmaVayesta=Vayesta()
        cajaInventario.append(manoArmaVayesta)
    elif arma==4:
        manoDinero=ManoDinero()
        cajaInventario.append(manoDinero)

''''----------------------enemigo---------------------'''
#funciones del enemigo
def elegirBala(self,tipoBala):
    centrar_bala=self.y
    if tipoBala==1:
        return Bala_fuego(position=(self.x,centrar_bala,self.z))
    else:
        return Bala_fuego(position=(self.x,centrar_bala,self.z))

def disparar(self,num,tipoBala):
    if self.alarma[num]>0:
        self.alarma[num]-=time.dt
    else:
        #crear bala
        bala=elegirBala(self,tipoBala)
        #caracteristica de la bala
        bala.creador=self
        bala.inicio=True
        bala.direction=Vec3(self.forward*-1).normalized()
        self.alarma[num]=2

def mordida(self,num):
    if self.disparar==True:
        if ColisionDeAtaque(self,nv.newPlayer,3)==True:
            self.disparar=False
    else:
        if self.alarma[num]>0:
            self.alarma[num]-=.05
        else:
            self.alarma[num]=1
            self.disparar=True

def SeguirJugador(self,newPlayer):
    veloz=0.0625*(2**self.velocidad) #time.dt
    #movimiento
    if self.caminar==True:
        global largoHabitacion, anchoHabitacion, cordenadaParedes
        #obtener las nuevas cordenadas
        new_cordenadas=funciones.algoritmoA(largoHabitacion,anchoHabitacion,cordenadaParedes,self,newPlayer,veloz)
        self.newX=new_cordenadas[0]
        self.newZ=new_cordenadas[2]
        #Actualizar posicion
        #self.position=(self.newX,self.y,self.newZ)
        self.caminar=False

    else:
        if (self.position.x==self.newX and self.position.z==self.newZ):
            self.caminar=True
        else:
            new_cordenadas=funciones.mover_posicision(self.position.x,0,self.position.z,self.newX,0,self.newZ,veloz)
            self.position=(new_cordenadas[0],self.y,new_cordenadas[2])

def saltar_atacar(self,num):

    if self.saltar==True:
        if self.volver_saltar==False:
            #comprobar que estoy saltando
            if self.alarma[num]>0:
                self.alarma[num]-=time.dt
            else:
                self.volver_saltar=True
                self.alarma[num]=1
        else:
            SeguirJugador(self,nv.newPlayer)
            #comprobar que estoy saltando
            if self.alarma[num]>0:
                self.alarma[num]-=time.dt
                self.y+=.0625
            else:
                self.saltar=False
                self.alarma[num]=1

    else:
        SeguirJugador(self,nv.newPlayer)
        self.saltar=fisica.gravedad(self)
        self.volver_saltar=False

def MoverseSaltando(self,num):
    SeguirJugador(self,nv.newPlayer)
    if self.saltar==True:
        #comprobar que estoy saltando
        if self.alarma[num]>0:
            self.alarma[num]-=time.dt
            self.y+=.0625
        else:
            self.saltar=False
            self.alarma[num]=1

    else:
        self.saltar=fisica.gravedad(self)

def transparencia(self,num):
    if self.transparencia==True:
        if self.alpha>.25:
            self.alpha-=time.dt
        else:
            #comprobar que estoy saltando
            if self.alarma[num]>0:
                self.alarma[num]-=time.dt
            else:
                self.alarma[num]=random.randrange(2,6)
                self.transparencia=False
    else:
        if self.alpha<.5:
            self.alpha+=time.dt
        else:
            self.alpha=1
            #comprobar que estoy saltando
            if self.alarma[num]>0:
                self.alarma[num]-=time.dt
            else:
                self.alarma[num]=random.randrange(2,6)
                self.transparencia=True

def explotar(self):
    l=Colision(self.position,escala=3)
    l.colision_explocion(explocion=1)

def explotar_cerca_jugador(self,distancia):
    aproximidad=distance(self,nv.newPlayer)

    if aproximidad<distancia:
        explotar(self)

def caracteristicas_explocion(self,color1,color2):
    #particulas de la explocion
    sangre=Sangre_Mancha(position=(self.position.x,self.position.y-1.5,self.position.z))
    particulas=Creador_Particulas_tiempo(position=self.position,tiempo=2,color=color1,dimensiones=.125,velcidad=4,anchoX=6,largoY=6,largoZ=6)
    particulas2=Creador_Particulas_tiempo(position=(self.x,self.y-.5,self.z),tiempo=2,color=color2,dimensiones=.125,velcidad=4,anchoX=6,largoY=6,largoZ=6)

def ActualizacionEnemigo(self):
    #actualizar la vista del enemigos
    self.rotation=(0,nv.newPlayer.rotation[1],0)
    Animacion(self)
    #colision=self.intersects(traverse_target=scene,ignore=(self,),debug=True)

class Enemigo(Objeto_2d):
    #caracteristica del sprite
    imagenes=['sprite/sprite_tirador.png']#['sprite/sprite_tirador.png']#['sprite/billy/sprite_billy_0.png']
    sprite_index=CargarImagen(imagenes)
    image_index=0
    numero_imagenes=len(imagenes)-1
    #caracteristicas del objeto
    vida=2
    velocidad=1    #-3 -2 -1 0 1 2 3
    direction=0
    caminar=True

    #caracteristicas del personaje
    ataque=''
    poder_ataque=0
    alarma=[2,velocidad,1]
    disparar=True

    #caminar
    newX=0
    newZ=0
    origen=.9

    #hacerce transparente
    transparecnia=True
    #resibir daño
    def herida(self):
        if self.vida>0:
            global poderArma
            self.vida-=poderArma
            ReproducirAudio('audio/herrida_enemigo.aiff')

    def herridaPatada(self):
         if self.vida>0:
            self.vida-=.5
            ReproducirAudio('audio/herrida_enemigo.aiff')

    def input(self,key):
        BalaChoca(self,key)

    def caracteristicars_muerte(self):
        ReproducirAudio('audio/herrida_enemigo.aiff')
        caracteristicas_explocion(self,color1=color.rgb(175, 27, 27),color2=color.rgb(226, 0, 0))
        EliminarObjeto(self)

    def morir(self):
        if self.vida<=0:
            self.caracteristicars_muerte()

    #actualizar objeto
    def caracteristicar_enemigo(self):
        fisica.gravedad(self)
        fisica.empujar(self,nv.newPlayer,2)

    def update(self):
        if self.vida>0:
            self.caracteristicar_enemigo()
            ActualizacionEnemigo(self)
        else:
            self.morir()

class Enemigo_dispara1(Enemigo):
    #actualizar objeto
    def update(self):
        fisica.gravedad(self)
        #mover al enemigo
        SeguirJugador(self,nv.newPlayer)
        #disparar
        disparar(self)
        ActualizacionEnemigo(self)

class Enemigo_dispara(Enemigo):
    alarma=[2,1,1]

    def caracteristicars_muerte(self):
        explotar(self)
        destroy(self)

    #actualizar objeto
    def caracteristicar_enemigo(self):
        fisica.gravedad(self)
        #SeguirJugador(self,nv.newPlayer)
        #explotar_cerca_jugador(self,3)

class Enemigos_voladores(Enemigo_dispara):
    #caracteristica del sprite
    dimensiones=(2,2)

    #actualizar objeto
    def caracteristicar_enemigo(self):
        #actualizar la vista del enemigos
        SeguirJugador(self,nv.newPlayer)

class Enemigo_saltarin(Enemigo):
    velocidad=2
    alarma=[1]
    saltar=False
    volver_saltar=False

    origen=.5

    #actualizar objeto
    def update(self):
        ActualizacionEnemigo(self)
        saltar_atacar(self,1)

#enemigos del videojuego
class Wendigo(Enemigo_dispara):
    alarma=[1]

    def caracteristicar_enemigo(self):
        fisica.gravedad(self)
        SeguirJugador(self,nv.newPlayer)
        mordida(self,0)

class Enfermera(Wendigo):
    imagenes=['sprite\enemigos\enfermera/enfermera0.png','sprite\enemigos\enfermera/enfermera1.png','sprite\enemigos\enfermera/enfermera2.png','sprite\enemigos\enfermera/enfermera3.png','sprite\enemigos\enfermera/enfermera4.png','sprite\enemigos\enfermera/enfermera5.png','sprite\enemigos\enfermera/enfermera5.png']
    sprite_index=CargarImagen(imagenes)
    image_index=0
    image_speed=0.375
    numero_imagenes=len(imagenes)-1
    dimensiones=(2,3)

class GeneradorEnemigos(Entity):
    alarma=[2]

    def update(self):
        if self.alarma[0]>0:
            self.alarma[0]-=.01
        else:
            self.alarma[0]=2#2
            f=Enfermera(position=(10,3,10))
            f=Enemigo_dispara(position=(15,3,10))
            f=Enemigos_voladores(position=(10,3,15))
            f=Enemigo_dispara(position=(20,3,18))

#t=GeneradorEnemigos()
''''----------------------objetos---------------------'''
class Voxel(Entity):
    vida=100
    solido=True
    #cargar las texturas del bloque
    sprite_index=['white_cube','brick','sprite/bloques/bloque_tierra.png','sprite/bloques/bloque_nave.png']

    def __init__(self,position=(0,0,0),escala=(0,0),image_index=0,brillo=0):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              collider='box',
              collision_cooldown=1,
              texture='brick',#self.sprite_index[0], #'white_cube', #self.sprite_index[image_index],
              color=color.rgb(brillo, brillo, brillo),
              scale=escala,
              rotation=(0,0,0),
              visible=True,
              )

class Bala_fuego(Objeto_2d):
    creador=0
    inicio=False
    #cargar los sprite
    image_index=0
    image_speed=0.5
    imagenes=['sprite/balas/bola_fuego/bola_fuego0.png','sprite/balas/bola_fuego/bola_fuego1.png','sprite/balas/bola_fuego/bola_fuego2.png','sprite/balas/bola_fuego/bola_fuego3.png','sprite/balas/bola_fuego/bola_fuego4.png','sprite/balas/bola_fuego/bola_fuego5.png','sprite/balas/bola_fuego/bola_fuego6.png','sprite/balas/bola_fuego/bola_fuego7.png']
    sprite_index=CargarImagen(imagenes)
    numero_imagenes=len(imagenes)-1
    dimensiones=(0.5,0.8)
    #alarma de destrucion
    alarma=[3]

    #funciones del objeto
    def MoverBala(self):
        colision=ColisionDeAtaque(self,nv.newPlayer,2)
        if not colision:
            origin=self.world_position
            hit_info=raycast(origin,self.direction,ignore=(self,self.creador,),distance=1,debug=False)

            #comprobar si no colisiona para avanzar
            if not hit_info.hit and self.alpha>0:
                self.position+=self.direction*16*time.dt
                self.alpha-=time.dt/4
            else:
                destroy(self)
        else:
            BalaExplocion(position=self.position)
            fisica.EmpujarJugador(nv.newPlayer)
            destroy(self)



    def update(self):
        self.rotation=(0,nv.newPlayer.rotation[1],0) #mover angulo de imagen
        if self.inicio==True:
            self.MoverBala()
            Animacion(self)

class Elevador(Voxel):
    direcion='arriba'
    encender=False
    piso=5
    limite=piso
    velocidad=0.125

    def moverse(self):
        if self.encender==True:
            if self.direcion=='arriba':
                if self.piso>0:
                    self.position=(self.position.x,self.position.y+self.velocidad,self.position.z)
                    self.piso-=self.velocidad
                else:
                    self.direcion='abajo'
                    self.encender=False
            else:
                if self.piso<self.limite:
                    self.position=(self.position.x,self.position.y-self.velocidad,self.position.z)
                    self.piso+=self.velocidad
                else:
                    self.direcion='arriba'
                    self.encender=False

    def input(self,key):
        ActivarObjeto(self,key,2)

class Puerta(Entity):
    encender=False
    velocidad=0.25
    alarma=[9]

    def __init__(self,position=(0,0,0),dimensiones=(0,0,0)):
        super().__init__(
                     model='sprite/Ambulancia.glb', #'models_compressed/PUERTA.obj',
                     texture=load_texture('bloques/bloque_nave.png'),
                     position=position,
                     escala=dimensiones,
                     collider='mesh')

    def abrir(self):
        if self.encender==True:
            #elevar la puerta
            if self.y<7:
                self.y+=self.velocidad
            else:
                self.desactivar()
        else:
            #comprobar si estoy arriba y el jugador no esta abajo mio
            if self.y>1.40 and not funciones.colision_objeto(self,newPlayer,5):
                self.y-=self.velocidad

    def desactivar(self):
        if self.alarma[0]>0:
            self.alarma[0]-=0.1
        else:
            self.encender=False
            self.alarma[0]=3


    def input(self,key):
        ActivarObjeto(self,key,3)

class Eteam(Objeto_2d):
    solido=True
    #cargar las imagenes
    image_index=1
    imagenes=['sprite/etem pistola/arma0.png','sprite/etem pistola/arma1.png','sprite/etem pistola/arma2.png','sprite/etem pistola/arma3.png','sprite/etem pistola/arma3.png','sprite/etem pistola/arma3.png']
    sprite_index=CargarImagen(imagenes)

    def update(self):
        self.rotation=(0,nv.newPlayer.rotation[1],0)
        #ver si colisiona con el jugador
        if funciones.colision_objeto(self,nv.newPlayer,3):
            #activar arma o agregar municion
            ActivarPistola(self.image_index)
            #activar la recolecion
            t=transicion(color=color.rgb(255, 252, 0))
            #activar arma
            EliminarObjeto(self)

    def cambiarImagen(self):
        self.texture=self.sprite_index[self.image_index]

class Sangre_Mancha(Entity):
    solido=True
    ancho=3.5
    mitad_ancho=ancho/2
    def __init__(self,position=(0,0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              collider='box',
              collision_cooldown=1,
              texture='white_cube',
              scale=self.ancho,
              visible=False
              )

    def procentaje_brillo(self,objeto):
        brillo=255
        #ver la distancia del objeto
        distancia_rayo=distance(self,objeto)
        #obtener el brillo dependiendo de la distancia
        porcentaje=(distancia_rayo*255)/self.ancho #self.mitad_ancho
        brillo=floor(porcentaje)

        return brillo

    def aumentar_luz(self,objetos):
        #for para pasar por los objetos
        for objeto in objetos:
            #comprobar si la explocion colisiona con una pared
            if objeto.solido==True:
                #cambiar el brillo del objeto
                objeto.brillo=self.procentaje_brillo(objeto)
                #comprobar si esta en la esquina del brillo o no
                objeto.color=color.rgb(255,objeto.brillo, objeto.brillo)

        destroy(self)

    def colision_luz(self):
        #comprobar si hay colisiones
        colision_info=self.intersects()
        objetos=colision_info.entities
        self.aumentar_luz(objetos)

    def update(self):
        self.colision_luz()

class Colision(Entity):
    def __init__(self,position=(0,0,0),escala=0):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              collider='box',
              collision_cooldown=1,
              texture='white_cube',
              scale=escala,
              visible=False
              )

    def eliminar_objetos(self,objetos,explocion):
        #for para eliminar los objetos
        for objeto in objetos:
            #comprobar si la explocion colisiona con una pared
            if objeto.solido==False:
                objeto.vida-=2

        #crear una explocion y destruirme
        if explocion==0:
            explotar=Explocion(position=(self.x,self.y,self.z),sprite_index='sprite/objetos/explocion/explocion')
        else:
            explotar=Explocion(position=(self.x,self.y,self.z),sprite_index='sprite/objetos/explocion sangre/explocion_sangre')
            caracteristicas_explocion(self,color1=color.rgb(175, 27, 27),color2=color.rgb(226, 0, 0))

        destroy(self)

    def colision_explocion(self,explocion):
        #comprobar si hay colisiones
        colision_info=self.intersects()
        objetos=colision_info.entities

        self.eliminar_objetos(objetos,explocion)

class Baril(Objeto_2d):
    solido=True
    sprite_index=['sprite/objetos/baril/baril0.png']
    dimensiones=(1.8,1.8)

    #resibir daño
    def input(self,key):
        if self.hovered:
            global miraArma
            distancia=distance(nv.newPlayer,self)
            #añadir un bloque
            global municion
            global arma
            if key=='left mouse down' and municion[arma]>0 and distancia<miraArma:
                self.explotarBaril()
            elif key=='e' and distancia<3:
                self.explotarBaril()

    def explotarBaril(self):
        #activar la colision de la explocion
        colision=Colision(position=self.position,escala=6)
        colision.colision_explocion(explocion=0)
        EliminarObjeto(self)  


    def update(self):
        self.rotation=(0,nv.newPlayer.rotation[1],0)
        fisica.empujar(self,nv.newPlayer,2)
        fisica.gravedad(self)

class Escaleras(Entity):
    sprite_index=load_texture('bloques/bloque_nave.png')
    rotacion=90

    def __init__(self,position=(0,0,0),escala=(0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              #origin_y=0.5,
              collider='box',
              texture=self.sprite_index,
              color=color.rgb(255, 255, 255),
              rotation=Vec3(45,self.rotacion,90),
              scale=escala
              #highlight_color=color.lime   #color cuando el maus pasa cerca de el
              )

#detalles
class Luz(Objeto):
    solido=True
    ancho=10
    mitad_ancho=ancho/2

    def __init__(self,position=(0,0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              collider='box',
              collision_cooldown=1,
              texture='white_cube',
              scale=self.ancho,
              visible=False
              )

    def procentaje_brillo(self,objeto):
        brillo=nv.brillo_nivel
        #ver la distancia del objeto
        distancia_rayo=floor(distance(self,objeto))
        if distancia_rayo<self.mitad_ancho:
            #obtener el brillo dependiendo de la distancia
            porcentaje=(distancia_rayo*255)/self.ancho #self.mitad_ancho
            brillo=(255-floor(porcentaje))/2

        return brillo

    def aumentar_luz(self,objetos):
        #for para pasar por los objetos
        for objeto in objetos:
            #comprobar si la explocion colisiona con una pared
            if objeto.solido==True or objeto.solido==False:
                #cambiar el brillo del objeto
                objeto.brillo=self.procentaje_brillo(objeto)
                #comprobar si esta en la esquina del brillo o no
                objeto.color=color.rgb(objeto.brillo, objeto.brillo, objeto.brillo)

    def colision_luz(self):
        #comprobar si hay colisiones
        colision_info=self.intersects()
        objetos=colision_info.entities
        self.aumentar_luz(objetos)

    def update(self):
        self.position=newPlayer.position
        self.colision_luz()

class Explocion(Entity):
    #caracteristica del sprite
    #sprite_index='sprite/objetos/explocion/explocion'
    dimensiones=(2,3)
    image_speed=15
    alarma=[1]

    golpe=False
    #animacion del personaje
    def __init__(self,position=(0,0,0),sprite_index=''):
        super().__init__(
                 animacion=Animation(
                               sprite_index,
                               parent=scene,
                               fps=self.image_speed,
                               scale=self.dimensiones, #dimensiones
                               position=position,
                               rotation=(0,nv.newPlayer.rotation[1],0),
                               loop=False,  #si se repetira la imagen
                               autoplay=True) #encender o apagar
                      )
    #revisar una vez la colision contra los enemigos
    def eliminarEnemigo(self):
        distanciaColision=6
        #comprovar si colisiona con el jugador
        ColisionDeAtaque(self.animacion,nv.newPlayer,distanciaColision)

    def update(self):
        #comprobar la alarma
        if self.alarma[0]>0:
            self.animacion.rotation=(0,nv.newPlayer.rotation[1],0)
            self.alarma[0]-=time.dt

            if self.golpe==False:
                self.golpe=ColisionDeAtaque(self.animacion,nv.newPlayer,5)
                ColisionDeAtaque(self.animacion,nv.newPlayer,5)
                ColisionDeAtaque(self.animacion,nv.newPlayer,5)

        else:
            self.alarma[0]=1
            self.golpe=False

            destroy(self.animacion)
            destroy(self)

class BalaExplocion(Objeto_2d):
    #cargar los sprite
    imagenes=['sprite/objetos/explocion bala/explocion_bala','sprite/objetos/explocion bala/explocion_bala','sprite/objetos/explocion bala/explocion_bala1']
    sprite_index=CargarImagen(imagenes)
    numero_imagenes=len(imagenes)-1
    image_index=0
    image_speed=0.03125
    dimensiones=(1,1)

    def update(self):
        self.rotation=(0,nv.newPlayer.rotation[1],0)
        if self.scale<1.125:
            #cambiar imagen
            if self.scale>1.03125: #0.03125*33
                self.texture=self.sprite_index[2]

            #aumentar el tamaño de la imagen
            aumento=Vec3(self.image_speed)
            self.scale+=aumento
        else:
            destroy(self)

class Particulas(Entity):
    solido=False
    vida=10
    def __init__(self,x,y,z,color=0,dimensiones=0,velcidad=0,anchoX=0,largoY=0,largoZ=0):
        super().__init__(
              parent=scene,
              model='cube',
              color=color,
              scale=dimensiones,
              collider='box',
              collision_cooldown=1,
              x=x,
              y=y,
              z=z,
              dx=random.randint(-anchoX,anchoX)/100,
              dy=random.randint(-largoY,largoY)/100,
              dz=random.randint(-largoZ,largoZ)/100,
              ds=random.randint(1,3)/500,
              velcidad=velcidad
        )

    def update(self):
        self.x+=self.dx*self.velcidad
        self.y+=self.dy*self.velcidad
        self.z+=self.dz*self.velcidad
        self.scale-=self.ds*self.velcidad
        self.alpha-=self.ds*2*self.velcidad*4

        #comprobar si colisiono
        hit_info=self.intersects()
        if self.alpha<=.005 or hit_info.hit:
            destroy(self)

class Creador_Particulas(Entity):
    solido=False
    def __init__(self,position=(0,0,0),tiempo=0,color=0,dimensiones=0,velcidad=0,anchoX=0,largoY=0,largoZ=0):
        super().__init__(
        alarma=tiempo,
        alarma2=0,
        position=position,
        color=color,
        dimensiones=dimensiones,
        velcidad=velcidad,
        anchoX=anchoX,
        largoY=largoY,
        largoZ=largoZ
        )

    def Crear_Particulas(self):
        num=9
        e=[None]*num
        for i in range (num):
            e[i]=Particulas(self.x,self.y,self.z,color=self.color,dimensiones=self.dimensiones,velcidad=self.velcidad,anchoX=self.anchoX,largoY=self.largoY,largoZ=self.largoZ)

    def update(self):
        if self.alarma2<=self.alarma:
            self.alarma2+=time.dt
        else:
            self.alarma2=0
            self.Crear_Particulas()

class Creador_Particulas_tiempo(Creador_Particulas):
    def update(self):
        self.Crear_Particulas()
        self.Crear_Particulas()
        destroy(self)

''''--------caracteristicas de niveles-------'''
#objeto de nivel
class Cielo(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=textura_cielo,
            scale=150,
            double_sided=True)


largoHabitacion=0
anchoHabitacion=0
cordenadaParedes=0

class Nivel(Entity):
    def __init__(self,brillo=0,num=''): #2
        super().__init__(
            brillo_nivel=brillo,
            numero_nivel=num,
            newPlayer=FirstPersonController(position=(10,.5,10),gravity=.25),
            caracteristicasJugador=CaracteristicasJugador(),
            barra=BarraDatos()
        )

    def EscanearMapa(self):
        #escanear el mapa
        carpetaNivel='niveles/nivel'+self.numero_nivel
        nivel=leer_nivel.EscanearMapa(carpetaNivel+'/nivel.txt')
        techo=leer_nivel.EscanearMapa(carpetaNivel+'/techo.txt')
        textura_nivel=leer_nivel.EscanearMapa(carpetaNivel+'/textura.txt')
        objetos_nivel=leer_nivel.EscanearMapa(carpetaNivel+'/objetos.txt')

        #caracteristica del nivel
        global largoHabitacion, anchoHabitacion
        largoHabitacion=len(nivel)
        anchoHabitacion=len(nivel[0])

        #crear el nivel
        self.Iniciar(nivel)
        self.crearNivel(nivel,techo,techo,textura_nivel,objetos_nivel)

    #crear el nivel
    def crearNivel(self,nivel,nivel2,techo,textura_nivel,objetos_nivel):
        #obtener medidas de la sala
        largoHabitacion=len(nivel)
        anchoHabitacion=len(nivel[0])
        xInicio=anchoHabitacion/2

    #crear la sala
        for z in range(largoHabitacion):
            piso=nivel[z]
            techo=nivel2[z]
            #crar el suelo
            #voxel=Voxel(position=(xInicio,0,z),escala=(anchoHabitacion,1),image_index=0)

            #creamos los blouqes con su altura
            for x in range(anchoHabitacion):
                textura=textura_nivel[z][x]
                voxel=Voxel(position=(x,0,z),escala=(1,1),image_index=textura,brillo=self.brillo_nivel)
                #si el suelo puede crecer mas hacerlo
                if piso[x]>0:
                    for y in range(piso[x]):
                        voxel=Voxel(position=(x,y+1,z),escala=(1,1),image_index=textura,brillo=self.brillo_nivel)

                self.ElegirObjeto(z,x,techo,textura_nivel,objetos_nivel)

    def ElegirObjeto(self,z,x,techo,textura_nivel,objetos_nivel):
        #si hay techo ponerlo
        if techo[x]>0:
            voxel=Voxel(position=(x,techo[x],z),escala=(1,1))

        #crear enemigos
        if objetos_nivel[z][x]==1: #objeto de tiro
            enemigo=Enemigo(position=(x,3,z)) #2

        #crear blanco de tiro
        if objetos_nivel[z][x]==4:
            enemigo=Enemigo_dispara(position=(x,3,z)) #Enemigo_dispara(position=(x,3,z))






        #crear puertas
        if objetos_nivel[z][x]==11:
            puerta=Puerta(position=(x,1.4,z),dimensiones=(5,3,5),image_index=textura)

        #elevador
        if objetos_nivel[z][x]==12:
            elevador=Elevador(position=(x,0.5,z),escala=(5,3,5))

        #baril explocivo
        if objetos_nivel[z][x]==13:
            baril=Baril(position=(x,3,z))

    def Iniciar(self,nivel):
        global cordenadaParedes
        cordenadaParedes=funciones.algoritmoA1(nivel)

#luz=Luz(position=newPlayer.position)
nv=Nivel(brillo=255,num='1')
nv.EscanearMapa()


eteam1=Eteam(position=(2,3,4))
eteam1.image_index=0
eteam1=Eteam(position=(2,3,4))
eteam1.image_index=1
eteam1=Eteam(position=(2,3,4))
eteam1.image_index=2
eteam1=Eteam(position=(2,3,4))
eteam1.image_index=3
eteam1=Eteam(position=(2,3,4))
eteam1.image_index=4




#mantener la pantalla encendida
app.run()
