from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController #para ver el mundo en 3d

app=Ursina()
editar_sala=True
#caracteristicas del Voxel
imagenes_bloques=['white_cube','brick','sprite/bloques/bloque_tierra.png','sprite/bloques/bloque_nave.png']
limite_imagenes_bloques=len(imagenes_bloques)-1
class Colision_Maxiba(Entity):
    ancho=10
    mitad_ancho=ancho/2
    def __init__(self):
        super().__init__(
              parent=scene,
              model='cube',
              collider='box',
              collision_cooldown=1,
              texture='white_cube',
              color=color.rgb(255, 0, 0),
              scale=self.ancho,
              visible=False
              )

    def procentaje_brillo(self,objeto):
        #ver la distancia del objeto
        distancia_rayo=floor(distance(self,objeto))
        if distancia_rayo<self.mitad_ancho:
            #obtener el brillo dependiendo de la distancia
            porcentaje=(distancia_rayo*255)/self.ancho #self.mitad_ancho
            brillo=floor((255-floor(porcentaje))/2)

        return brillo

    def aumentar_luz(self,objetos):
        #for para pasar por los objetos
        for objeto in objetos:
            #cambiar el brillo del objeto
            #objeto.brillo=self.procentaje_brillo(objeto)
            #comprobar si esta en la esquina del brillo o no
            objeto.color=color.rgb(255,objeto.brillo, objeto.brillo)

    def colision_luz(self):
        #comprobar si hay colisiones
        colision_info=self.intersects()
        objetos=colision_info.entities
        self.aumentar_luz(objetos)

    def update(self):
        if self.visible==True:
            self.scale=self.ancho
            self.mitad_ancho=self.ancho/2
            self.position=(camera.position.x,camera.position.y,-5)
            self.colision_luz()
        else:
            self.position=(0,0,0)

class Voxel(Button):
    nivel=0
    brillo=255
    image_index=0
    dimensiones=1
    pared=True


    def __init__(self,position=(0,0,0),escala=(0,0)):
        super().__init__(
              parent=scene,
              position=position,
              model='cube',
              collider='box',
              collision_cooldown=1,
              origin_y=0.5,
              texture='white_cube', #self.sprite_index[image_index],
              color=color.rgb(255, 255, 255),
              highlight_color=color.lime,
              scale=escala,
              visible=True
              )

    def agregar_o_eliminar_bloque(self,key):
        #agregar o eliminar el bloque
        if key=='left mouse down':
            self.nivel+=1
        elif key=='right mouse down':
            self.nivel-=1
        '''
        if self.nivel>=0:
            self.position=(self.x,self.y,0)
            self.scale=(1,1,self.nivel)
        else:
            self.position=(self.x,self.y,2)
            self.scale=(1,1,1)'''

    def subir_o_bajarle_brillo(self,key):
        bajar_brillo=5
        if key=='up arrow' and self.brillo<255:
            self.brillo+=bajar_brillo
            self.color=color.rgb(self.brillo, self.brillo, self.brillo)
        elif key=='down arrow' and self.brillo>0:
            self.brillo-=bajar_brillo
            self.color=color.rgb(self.brillo, self.brillo, self.brillo)

    def cambiar_sprite(self,key):
        global imagenes_bloques, limite_imagenes_bloques
        if key=='right arrow' and self.image_index<limite_imagenes_bloques:
            self.image_index+=1
        elif key=='left arrow' and self.image_index>0:
            self.image_index-=1

        self.texture=imagenes_bloques[self.image_index]

    def cambiar_dimensiones(self,key):
        pass

    def input(self,key):
        if self.hovered:
            menuDatos.Actualizar_Datos_En_Pantalla(self)
            self.agregar_o_eliminar_bloque(key)
            self.subir_o_bajarle_brillo(key)
            self.cambiar_sprite(key)
            self.cambiar_dimensiones(key)

class draw_texto(Text):
    #crear el modelo
    def __init__(self,position=(0,0,0),texto=''):
        super().__init__(
            parent=camera.ui,
            position=position,
            text=texto,
            scale=1.8,
            color=color.rgb(0, 0, 0),
            visible=True,
            rotation_y=45,
            origin_z=-18,
            origin_y=0.9,
        )

class Menu(Entity):
    def __init__(self,position=(0,0,0)):
        super().__init__(
             texto_brillo=draw_texto(position=(.7,.5,-.4),texto='brillo'),
             datos_objeto_brillo=draw_texto(position=(.8,.5,-.4),texto='255'),
             texto_bloque=draw_texto(position=(.67,.45,-.4),texto='bloque'),
             datos_objeto_bloque=draw_texto(position=(.8,.45,-.4),texto='0'),
             texto_bloque_nivel=draw_texto(position=(.7,.4,-.4),texto='Nivel'),
             datos_objeto_nivel=draw_texto(position=(.8,.4,-.4),texto='0'),
        )

    def input(self,key):
        #salir
        if key=='escape':
            app.destroy()
            exit()

        #cambiar estilo de vista
        if key=='e':
            global editar_sala
            if editar_sala==True:
                editar_sala=False
                menu_colisoion.visible=False
                menu_colisoion.ancho=0
            else:
                editar_sala=True
                menu_colisoion.visible=True
                menu_colisoion.ancho=1

        self.selecion(key)
    #editor de nivel
    def Actualizar_Datos_En_Pantalla(self,bloque):
        #ver los datos en pantalla
        menuDatos.datos_objeto_brillo.text=str(bloque.brillo)
        menuDatos.datos_objeto_bloque.text=str(bloque.image_index)

        menuDatos.datos_objeto_nivel.text=str(bloque.nivel)

    def mover_angulo_camara(self):
        #actualizar camara
        velozX=0
        velozY=0
        veloz=1
        #arriba y abajo
        if held_keys['w']:
            velozX=-veloz
        if held_keys['s']:
            velozX=veloz

        #mover 45 grados z

        #mover derecha a izquierda
        if held_keys['a']:
            velozY=veloz
        if held_keys['d']:
            velozY=-veloz

        #mover la camara
        camera.rotation=(camera.rotation.x+velozX,camera.rotation.y+velozY,camera.rotation.z)

    def move_camera(self):
        #actualizar camara
        velozX=0
        velozY=0
        veloz=1
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

    #caracteristica de selecion
    def selecion(self,key):
        if menu_colisoion.visible==True:
            if key=='scroll up':
                menu_colisoion.ancho+=1
            elif key=='scroll down':
                if menu_colisoion.ancho>1:
                    menu_colisoion.ancho-=1


    def update(self):
        self.move_camera()

menuDatos=Menu()
menu_colisoion=Colision_Maxiba()
#crear el nivel
NivelesBloques=[]
ancho=20
largo=20
piso=0
def crearNivel(ancho,largo):
    for y in range(largo):
        for x in range(ancho):
            voxel=Voxel(position=(x,-y,0),escala=(1,1))
            NivelesBloques.append(voxel)
crearNivel(ancho,largo)

#modificar camara
camera.x=10
camera.y=-5
camera.z=-20
#camera.z=-43


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
            nivel=str(bloque.nivel)
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
    #guardar el mapa
    global guardar
    if held_keys['g'] and guardar==False:
        GuardarNivel('nivel1')
        print('------munod guardado-------')
        guardar=True
        app.destroy()
        exit()





app.run()
