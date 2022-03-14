from ursina import *

def gravedad(self):
    #origen del rayo
    origen=self.world_position-(self.up*self.origen)
    #lanzar el rayo
    colision=raycast(origen,direction=(0,-45,0),ignore=(self,),distance=self.vspeed,debug=False)

    #comrpobar si hay suelo
    if not colision.hit:
        self.y-=self.vspeed
        return False 
    else:
        return True  #time.dt*6*self.vspeed

def gravedad_jugador(self):
    #origen del rayo
    origen=self.world_position#-(self.up*.25)
    #lanzar el rayo
    colision=raycast(origen,direction=(0,-45,0),ignore=(self,),distance=1,debug=True)

    #comrpobar si hay suelo
    if not colision.hit:
        self.y-=.25

def friccion_jugador(self):
    fuerza_fricion=10

    fuerza_normal=0
    coeficiente_fricion=10
    fricion=coeficiente_fricion*fuerza_normal
    self.speed-=fricion

def empujar(self,objeto,rango_colision):
    distancia_objeto=distance(self,objeto)

    if distancia_objeto<rango_colision:
        #comprobar la direcion de la camara
        self.direction=Vec3(
            self.forward*(1)+
            self.right*(0)
        ).normalized()

        #origen del rayo
        origin=self.world_position-(self.up*.5)

        #crear la colision del rayo
        hit_info=raycast(origin,self.direction,ignore=(self,),distance=1,debug=False)

        #comprobar si el rayo no colisiona
        if not hit_info.hit:
            self.position+=self.direction*objeto.speed*time.dt

def EmpujarJugador(self):
    #comprobar la direcion de la camara
    direction=Vec3(
        self.forward*(-1)+
        self.right*(0)
    ).normalized()

    #origen del rayo
    origin=self.world_position+(self.up*.5)

    #crear la colision del rayo
    distancia_mov=direction*time.dt*8
    hit_info=raycast(origin,direction,ignore=(self,),distance=1,debug=False)

    #comprobar si el rayo no colisiona
    if not hit_info.hit:
        self.position+=distancia_mov



                #bala=Voxel(position=origin+angulo)

        #rayos que chocan con el suelo
        #raycast(origin,direction=(0,-45,0),ignore=(self,),distance=5,debug=True) #abajo de mi
        #raycast(origin,direction=(0,-45,-45),ignore=(self,),distance=5,debug=True) #atras de mi
        #raycast(origin,direction=(0,-45,45),ignore=(self,),distance=5,debug=True) #enfrente


        #raycast(origin,direction=(45,-45,0),ignore=(self,),distance=5,debug=True) #izquierda
        #raycast(origin,direction=(45,-45,-45),ignore=(self,),distance=5,debug=True) #atras izquierda
        #raycast(origin,direction=(45,-45,45),ignore=(self,),distance=5,debug=True) #enfrente izquierda

        #raycast(origin,direction=(-45,-45,0),ignore=(self,),distance=5,debug=True) #derecha
        #raycast(origin,direction=(-45,-45,-45),ignore=(self,),distance=5,debug=True) #atras derecha
        #raycast(origin,direction=(-45,-45,45),ignore=(self,),distance=5,debug=True) #enfrente derecha

        #rayos que chocan con las paredes
        #raycast(origin,direction=(0,0,45),ignore=(self,),distance=5,debug=True) #enfrente------
        #raycast(origin,direction=(45,0,45),ignore=(self,),distance=5,debug=True) #enfrente izquierda----
        #raycast(origin,direction=(-45,0,45),ignore=(self,),distance=5,debug=True) #enfrente derecha----

        #raycast(origin,direction=(0,0,-45),ignore=(self,),distance=5,debug=True) #atras----
        #raycast(origin,direction=(45,0,-45),ignore=(self,),distance=5,debug=True) #atras izquierda-----
        #raycast(origin,direction=(-45,0,-45),ignore=(self,),distance=5,debug=True) #enfrente derecha----

        #raycast(origin,direction=(0,0,0),ignore=(self,),distance=5,debug=True) #enfrente
        #raycast(origin,direction=(45,0,0),ignore=(self,),distance=5,debug=True) #izquierda----
        #raycast(origin,direction=(-45,0,0),ignore=(self,),distance=5,debug=True) #derecha
        #raycast(origin,direction=(0,0,-45),ignore=(self,),distance=5,debug=True) #atras
