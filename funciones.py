import math
#-----------algoritmos de colision
def colision_objeto(objeto1,objeto2,distancia):
    #sacar la distancia
    distanciaX=abs((abs(objeto1.x)-abs(objeto2.x)))
    distanciaY=abs(objeto1.y-objeto2.y)
    distanciaZ=abs((abs(objeto1.z)-abs(objeto2.z)))
    #comprobar si esta cerca
    if (distanciaX<=distancia and distanciaY<=distancia and distanciaZ<=distancia):
        return True

def colision_cordenadas(x1,y1,z1,x2,y2,z2,distancia):
    #sacar la distancia
    distanciaX=abs((x1-x2))
    distanciaY=abs((y1-y2))
    distanciaZ=abs((z1-z2))
    #comprobar si esta cerca
    if (distanciaX<=distancia and distanciaY<=distancia and distanciaZ<=distancia):
        return True

#-------algoritmo de medicion de distancia
def distancia_objeto(x1,y1,z1,x2,y2,z2):
    x1=abs(x1)
    y1=abs(y1)
    z1=abs(z1)
    x2=abs(x2)
    y2=abs(y2)
    z2=abs(z2)
    #sacar la distancia
    distanciaX=abs((x1-x2))
    distanciaY=abs((y1-y2))
    distanciaZ=abs((z1-z2))

    #devolver una lista de cordenadas
    return [distanciaX,distanciaY,distanciaZ]

#-------algoritmo de movimiento bruzco
def mover_posicision(x1,y1,z1,x2,y2,z2,velocidad):
        nuewX=0
        nuewY=0
        nuewZ=0

        #moverse adelante o atras
        distancia=0
        distancia_objetos=distancia_objeto(x2,y2,z2,x1,y1,z1)
        distanciaX=distancia_objetos[0]
        if distanciaX>distancia:
            if (x2<x1):
                nuewX=x1-velocidad
            elif (x2>x1):
                nuewX=x1+velocidad
        else:
            nuewX=x1

        #moverse derecha a izquierda
        distanciaZ=distancia_objetos[2]
        if distanciaZ>distancia:
            if (z2<z1):
                nuewZ=z1-velocidad
            elif (z2>z1):
                nuewZ=z1+velocidad
        else:
            nuewZ=z1

        #mover arriba y abajo
        distanciaY=distancia_objetos[1]
        if distanciaY>distancia:
            if (y1<y2):
                nuewY=y1-velocidad
            elif (y1>y2):
                nuewY=y1+velocidad
        else:
            nuewY=y1

        return [nuewX,nuewY,nuewZ]

def mover_posicision1(x1,y1,z1,x2,y2,z2,velocidad):
        nuewX=x1
        nuewY=y1
        nuewZ=z1
        #moverse adelante o atras
        if (x1>x2):
            nuewX=x1-velocidad
        else:
            nuewX=x1+velocidad

        #moverse derecha a izquierda
        if (z1>z2):
            nuewZ=z1-velocidad
        else:
            nuewZ=z1+velocidad

        return [nuewX,nuewY,nuewZ]

def perseguir_objeto(cazador,presa,velocidad):

        x1=cazador.x
        y1=cazador.y
        z1=cazador.z

        x2=presa.x
        y2=presa.y
        z2=presa.z

        nuewX=0
        nuewY=0
        nuewZ=0


        #moverse adelante o atras
        distancia=2
        distancia_objetos=distancia_objeto(x2,y2,z2,x1,y1,z1)
        distanciaX=distancia_objetos[0]
        if distanciaX>distancia:
            if (x2<x1):
                nuewX=x1-velocidad
            elif (x2>x1):
                nuewX=x1+velocidad
        else:
            nuewX=x1

        #moverse derecha a izquierda
        distanciaZ=distancia_objetos[2]
        if distanciaZ>distancia:
            if (z2<z1):
                nuewZ=z1-velocidad
            elif (z2>z1):
                nuewZ=z1+velocidad
        else:
            nuewZ=z1

        #mover arriba y abajo
        diferencia_altura=abs(cazador.scale[1]-presa.scale[1])

        distanciaY=distancia_objetos[1]-diferencia_altura
        if distanciaY>distancia:
            if (y1>y2):
                nuewY=y1-velocidad
            elif (y1<y2):
                nuewY=y1+velocidad
        else:
            nuewY=y1

        return [nuewX,nuewY,nuewZ]

def move_bala(cazador,presa,velocidad):
        #obtener las cordenadas
        x1=cazador.x
        y1=cazador.y
        z1=cazador.z

        x2=presa.x
        y2=presa.y
        z2=presa.z

        nuewX=0
        nuewY=0
        nuewZ=0

        #moverse adelante o atras
        distancia=2
        distancia_objetos=distancia_objeto(x2,y2,z2,x1,y1,z1)
        distanciaX=distancia_objetos[0]
        if distanciaX>distancia:
            if (x2<x1):
                nuewX=-velocidad
            elif (x2>x1):
                nuewX=velocidad
        else:
            nuewX=0

        #moverse derecha a izquierda
        distanciaZ=distancia_objetos[2]
        if distanciaZ>distancia:
            if (z2<z1):
                nuewZ=-velocidad
            elif (z2>z1):
                nuewZ=velocidad
        else:
            nuewZ=0

        #mover arriba y abajo
        distanciaY=distancia_objetos[1]
        if distanciaY>distancia:
            if (y1<y2):
                nuewY=-velocidad
            elif (y1>y2):
                nuewY=velocidad
        else:
            nuewY=0

        return [nuewX,nuewY,nuewZ]

#----------------algoritmos de IA para caminar en el mundo----------
def algoritmoA1(nivel):
    #medidas del nivel
    columnas=len(nivel)
    filas=len(nivel[0]) #posiblemente esten volteados

    #sacamos las cordenadas de todos los bloques
    paredes=[]
    for x in range(columnas):
        for y in range(filas):
            #comprobar si es una pared, una puerta o un elevador
            objeto_solido=False
            if (nivel[x][y]>0 or nivel[x][y]==-2 or nivel[x][y]==-3):
                objeto_solido=True
            #agregar cordenadas y colision
            paredes.append([y,x,objeto_solido])

    return paredes

def algoritmoA2(cazador,destinox,destinoz,velocidad):
        #asignar cordenadas
        x1=cazador.x
        y1=cazador.y
        z1=cazador.z

        x2=destinox
        z2=destinoz

        nuewX=x1
        nuewZ=z1
        distancia=0
        #moverse adelante o atras
        distancia_objetos=distancia_objeto(x1,y1,z1,x2,0,z2)
        distanciaX=distancia_objetos[0]
        if (distanciaX>distancia):
            if (x1>x2):
                nuewX=x1-velocidad
            else:
                nuewX=x1+velocidad

        #moverse derecha a izquierda
        distanciaZ=distancia_objetos[2]
        if (distanciaZ>distancia):
            if (z1>z2):
                nuewZ=z1-velocidad
            else:
                nuewZ=z1+velocidad

        return [nuewX,0,nuewZ]

def algoritmoA(filas,columnas,paredes,cazador,presa,velocidad):
    x=cazador.z
    y=cazador.x
    #redondeamos las cordenadas de los jugadores
    cazadorX=math.floor(cazador.z)  #voltear las letras
    cazadorY=math.floor(cazador.x)
    presaX=math.floor(presa.z)
    presaY=math.floor(presa.x)
    #-------------------empezar a camina

    camino=[]
    veloz=1
    if not(cazadorX==presaX and cazadorY==presaY):
        #izquierda y derecha
        if cazadorX<presaX:
            #comprobar si hay una pared a tu derecha
            cordenada=((cazadorX+1)*columnas)+cazadorY
            pared=paredes[cordenada]
            if (pared[2]==False):
                cazadorX+=veloz
                x+=velocidad
                camino.append([cazadorX,cazadorY])

        elif cazadorX>presaX:
            #comprobar si hay una pared a tu derecha
            cordenada=((cazadorX-1)*columnas)+cazadorY
            pared=paredes[cordenada]
            if (pared[2]==False):
                cazadorX-=veloz
                x-=velocidad
                camino.append([cazadorX,cazadorY])

        #arriba y abajo
        if cazadorY<presaY:
            #comprobar si hay una pared a tu derecha
            cordenada=(cazadorX*columnas)+cazadorY+1
            pared=paredes[cordenada]
            #print(cordenada)
            if (pared[2]==False):
                cazadorY+=veloz
                y+=velocidad
                camino.append([cazadorX,cazadorY])
        elif cazadorY>presaY:
            #comprobar si hay una pared a tu derecha
            cordenada=(cazadorX*columnas)+cazadorY-1
            pared=paredes[cordenada]
            if (pared[2]==False):
                cazadorY-=veloz
                camino.append([cazadorX,cazadorY])

    #por si sucede un imprevisto
    camino.append([cazadorX,cazadorY])

    #mover naturalmente al personaje
    newX=camino[0][1]
    newY=camino[0][0]
    nuevas_cordenadas=[newX,0,newY]
    return nuevas_cordenadas


nm=('''
        velocidad=0.0625 #time.dt
        #movimiento
        if self.caminar==True:
            #obtener las nuevas cordenadas
            new_cordenadas=funciones.algoritmoA(largoHabitacion,anchoHabitacion,cordenadaParedes,self,newPlayer,velocidad)
            self.newX=new_cordenadas[0]
            self.newZ=new_cordenadas[2]
            #Actualizar posicion
            #self.position=(newX,3,newZ)
            self.caminar=False

        else:
            #si estamos en las mismas cordenadas caminar
            if (self.position.x==self.newX and self.position.z==self.newZ):
                self.caminar=True
            else:
                new_cordenadas=funciones.mover_posicision(self.position.x,self.position.y,self.position.z,self.newX,0,self.newZ,velocidad)
                self.position=(new_cordenadas[0],3,new_cordenadas[2])
         ''')
