import funciones
from ursina import *
def disparar(self):
    if self.alarma[0]>0:
        self.alarma[0]-=time.dt
    else:
        #crear bala
        centrar_bala=self.y
        bala=Bala(position=(self.x,centrar_bala,self.z))
        #caracteristica de la bala
        bala.creador=self
        bala.inicio=True
        bala.direction=Vec3(self.forward*-1).normalized()
        self.alarma[0]=2

def SeguirJugador(self,newPlayer,largoHabitacion,anchoHabitacion, cordenadaParedes):
    veloz=0.0625*(2**self.velocidad) #time.dt
    #movimiento
    if self.caminar==True:
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
