from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController #para ver el mundo en 3d
import os
from io import open

app=Ursina()

def ActualizarImagen(self,sprite):
    self.image_index=0
    self.sprite_index=sprite[self.image_index]
    self.texture=self.sprite_index

#textura del muro
imagenes=['white_cube','sprite/bloques/bloque_tierra.png','sprite/bloques/bloque_nave.png']
numero_imagenes=len(imagenes)-1

#textura del objeto
imagenes_objetos=['sprite/billy/sprite_billy_0.png','sprite/etem pistola/arma0.png','sprite/etem pistola/arma1.png','sprite/etem pistola/arma2.png','sprite/etem pistola/arma3.png','sprite/etem pistola/arma3.png']
numero_imagenes_objetos=len(imagenes_objetos)-1

class draw_rectangulo(Entity):
    def __init__(self,x,y,ancho,largo,color):
        super().__init__(
            parent=camera.ui,
            model='quad',
            color=color,
            origin=(-.5,-.5),
            position=(x,y,-.3),
            #scale_max=ancho,
            scale=(ancho,largo),
        )

class draw_texto_3d(Text):
    #crear el modelo
    def __init__(self,position=(0,0,0),texto=''):
        super().__init__(
            parent=camera.ui,
            position=position,
            text=texto,
            scale=1.5,
            color=color.rgb(255, 255, 255),
            visible=True,
            rotation_y=45,
            origin_z=-18,
            origin_y=0.9,
        )

class Director(Entity):
    def __init__(self):
        super().__init__(
            fondo_piso=draw_rectangulo(x=.68,y=-2,ancho=1,largo=6,color=color.rgb(0, 0, 0)),
            texto=draw_texto_3d(position=(.7,.5,-.4),texto='piso'),
            texto_piso=draw_texto_3d(position=(.78,.5,-.4),texto='1')
        )
    #cambiar nivel
    def CambiarPiso(self):
        global piso
        self.texto_piso.text=str(piso)

    def input(self,key):
        global piso
        if key=='1':
            piso=1
            self.CambiarPiso()
        elif key=='2':
            piso=2
            self.CambiarPiso()
        elif key=='3':
            piso=3
            self.CambiarPiso()

cm=Director()

class Voxel(Button):
    nivel=0
    pared=True
    #imagen del entorno
    global sprite
    image_index=0
    sprite_index=sprite[image_index]


    def __init__(self,position=(0,0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='quad',
              origin_y=0.5,
              collider='box',
              texture='white_cube',
              color=color.color(0,0,random.uniform(0.9,1)),
              scale=1,
              highlight_color=color.rgb(43, 43, 43),

              )

    def cambiarTexturaPared(self,sprite,numero_imagenes):
        #limitar el cambio de imagenes y regresar al principio
        if self.image_index<numero_imagenes:
            self.image_index+=1
        else:
            self.image_index=0

        #actualizar la textura
        self.sprite_index=sprite[self.image_index]
        self.texture=self.sprite_index

    def input(self,key):
        if self.hovered:
            global numero_imagenes
            global sprite

            global sprite_objetos
            global imagenes_objetos

            #cambiar de pared a objeto
            if key=='right mouse down':
                if self.pared==False:
                    self.pared=True
                    ActualizarImagen(self,sprite)
                    #activar visibilidad al nivel
                    self.nivel.visible=True
                else:
                    self.pared=False
                    ActualizarImagen(self,sprite_objetos)
                    #desactivar visibilidad al nivel
                    self.nivel.visible=False
                    self.nivel.nivel=0
                    self.nivel.text=str(0)

            #aumentar nivel
            if key=='left mouse down' and self.pared==True:
                self.nivel.ActualizarNivel()

            #cambiar textura
            if key=='scroll up':
                if self.pared==True:
                    cambiarTexturaPared(self,sprite,numero_imagenes)
                else:
                    cambiarTexturaPared(self,sprite_objetos,numero_imagenes_objetos)

class draw_texto(Text):
    nivel=0
    #crear el modelo
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            text=str(self.nivel),
            #font='fuentes/AmazDooMLeft.ttf',
            scale=25,
            color=color.rgb(0, 0, 0),
            visible=True,
            rotation_y=45,
            origin_z=-18,
            origin_y=0.9,
        )

    def ActualizarNivel(self):
        self.nivel+=1
        self.text=str(self.nivel)

#obtener las cordenadas de los dibujos
NivelesBloques=[]
ancho=20
largo=20
piso=0
def CrearNivel(ancho,largo):
    for y in range(largo):
        for x in range(ancho):
            voxel=Voxel(position=(x,-y,0))
            voxel.nivel=draw_texto(position=(x-0.01,-y,-1))
            NivelesBloques.append(voxel)

CrearNivel(ancho,largo)

#posicionar la camara al inicio del mundo
camera.position=(6.8,-4.1,-20)
def MoverCamara(veloz):
    #actualizar camara
    velozX=0
    velozY=0
    #derecha e izquierda
    if held_keys['a']:
        velozX=-veloz
    if held_keys['d']:
        velozX=veloz

    #subir y bajar camara
    if held_keys['w']:
        velozY=veloz
    if held_keys['s']:
        velozY=-veloz

    #mover la camara
    camera.position=(camera.position.x+velozX,camera.position.y+velozY,camera.position.z)
def ZoomCamara(veloz):
    zoomZ=0
    #zoom de camara
    if held_keys['e']: #zoom
        zoomZ=-veloz
    if held_keys['q']: #retrodecer
        zoomZ=veloz

    #actualizar camara
    camera.position=(camera.position.x,camera.position.y,camera.position.z+zoomZ)
def ActualizarCamara(veloz):
    MoverCamara(veloz)
    ZoomCamara(veloz)


#guardar el mapa
guardar=False
def CrearCarpeta(carpeta):
    #si no existe la carpeta crearla
    if not os.path.exists(carpeta):
        os.mkdir(carpeta)
        os.system('copy'+''+'name'+''+carpeta)

def CrearBlockNotas2(ancho,largo,carpeta):
    #ruta de la carptea
    ruta=carpeta+'/'
    #-----------------borrar cualquier cosa que tenga en el archivo
    #archivo que me dice el nivel de las paredes
    archivoNivel=ruta+'nivel.txt'
    crear_archivoNivel=open(archivoNivel,"w")
    crear_archivoNivel.close()

    #archivo que me dice la textura de las paredes
    archivoTextura=ruta+'textura.txt'
    crear_archivoTextura=open(archivoTextura,"w")
    crear_archivoTextura.close()

    #archivo que crea el techo
    archivoTecho=ruta+'techo.txt'
    crear_archivoTecho=open(archivoTecho,"w")
    crear_archivoTecho.close()

    #archivo de objetos
    archivoObjetos=ruta+'objetos.txt'
    crear_archivoObjetos=open(archivoObjetos,"w")
    crear_archivoObjetos.close()

    #crear el archivo
    crear_archivoNivel=open(archivoNivel,"a")
    crear_archivoTextura=open(archivoTextura,"a")
    crear_archivoTecho=open(archivoTecho,"a")
    crear_archivoObjetos=open(archivoObjetos,"a")

    for y in range(largo):
        for x in range(ancho):
            #obtener la caracteristica del bloque
            lugar=(y*ancho)+x
            bloque=NivelesBloques[lugar]
            #escribir el tamaño de las paredes
            nivel=str(bloque.nivel.nivel)
            crear_archivoNivel.write(nivel +',')

            #escribir la textura del bloque
            textura=str(bloque.image_index)
            crear_archivoTextura.write(textura + ',')

            #crear el techo
            techo=str(0)
            crear_archivoTecho.write(techo + ',')

            #crear objetos
            objeto=str(0)
            if bloque.pared==False:
                objeto=str(bloque.image_index+1)
            crear_archivoObjetos.write(objeto + ',')

        #salto de pagina
        crear_archivoNivel.write('\n')
        crear_archivoTextura.write('\n')
        crear_archivoTecho.write('\n')
        crear_archivoObjetos.write('\n')

    #cerrar el bloc
    crear_archivoNivel.close()
    crear_archivoTextura.close()
    crear_archivoTecho.close()
    crear_archivoObjetos.close()

def GuardarNivel(nombre):
    carpeta='niveles/'+nombre
    CrearCarpeta(carpeta)

    global ancho
    global largo
    CrearBlockNotas2(ancho,largo,carpeta)


def update():
    #actualizar camara
    veloz=15*time.dt
    ActualizarCamara(veloz)

    #guardar el mapa
    global guardar
    if held_keys['g'] and guardar==False:
        GuardarNivel('nivel1')
        print('------munod guardado-------')
        guardar=True
        app.destroy()
app.run()
