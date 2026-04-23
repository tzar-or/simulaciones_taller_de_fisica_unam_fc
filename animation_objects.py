import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

class Spring:

    #función init
    def __init__(self, ax, pos=[(0.5,0.1),(0.5,0.8)], scale=1, weight=1, compression=0.5):
        self.ax = ax
        self.pos = pos
        self.scale = scale
        self.weight = weight
        self.compression = compression

    #función para dibujar el resorte (Primero con los valores en default)
    def draw(self):
        pos = self.pos
        # por default, cada linea diagonal, a escala E será de de 0.2*Escala*A,
        # donde A sera igual a la altura de la linea diagonal
        # de tal manera que si n es la cantidad de diagonales, h = nA+0.2*E será el largo del resorte.
        # si la altura del resorte es h, h-0.2*E sera la de las lineas diagonales
        # Para determinar n, primero dividimos ih = 0.1*E (alto ideal de la diagonal) entre h-2*ih y redondeamos hacia abajo.
        # si el residuo es mayor a ih/2 (media altura ideal), a n le agregamos uno. Al final el alto real de las diagonales
        # sera (h-2*ih)/n

        # definimos una variable para ajustar la compresion
        s = (0.5+self.compression)

        # definimos la altura del resorte con la norma euclidea
        h = np.sqrt( (pos[0][0] - pos[1][0])**2 + (pos[0][1] - pos[1][1])**2 )*s +0.00001
        # Se valida que la altura sea válida
        if(h<0.1*self.scale):
            raise Exception("Non valid spring lenght")

        
        #determinamos grueso y altura diagonal ideal

        ih = 0.1*self.scale*s
        l = 0.4*ih/s

        # determinamos n con esa condicion (ajustamos para que el límite mo sea solo la mitad de ih)
        # poniendo algo más específico para evitar errores 
        self.n = int((h-2*ih)/ih) if (h-2*ih)%ih<ih/2.017002 else int((h-2*ih)/ih)+1
        #definimos la altura real de las diagonales
        hd = (h-2*ih)/self.n

        # definimos una función para hacer la rotación de un vecor
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0 if (pos[1][1]-pos[0][1])<0 else np.pi
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) - np.pi/2
            theta = theta if (pos[1][0]-pos[0][0])>0 else theta-np.pi
            return np.matmul([x,y],[[np.cos(theta), np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array([pos[0][0], pos[0][1]])


        #con el número de líneas diagonales, n, las guardamos en un array
        self.diag = []
        #dibujamos las líneas diagonales, pero dibujandolo desde R(0,0) hasta R(0,h) con R la transformación
        # de rotación
        for i in range(1,self.n+1):
            self.diag.append( self.ax.plot([R(-ih/s,i*hd)[0],R(ih/s,(i+1)*hd)[0]],[R(-ih/s,i*hd)[1],R(ih/s,(i+1)*hd)[1]],
                                 color="black", lw=3*self.weight)[0] )
        # con ese mismo numero podemos dibujar las líneas horizontales
        self.horz = []
        for i in range(1,self.n+2):
            self.horz.append( self.ax.plot( [R(-l/2,i*hd)[0],R(l/2,i*hd)[0]], [R(-l/2,i*hd)[1],R(l/2,i*hd)[1]],
                                 color = "black", lw=1*self.weight )[0] )

        #finalmente dibujamos los soportes
        self.supph1, = self.ax.plot( [R(-l,0)[0], R(l,0)[0]], [R(-l,0)[1], R(l,0)[1]], color="black", lw=3*self.weight)
        self.suppv1, = self.ax.plot( [R(0,0)[0],R(0,ih)[0]], [R(0,0)[1],R(0,ih)[1]],color="black", lw=3*self.weight)
        self.supph2, = self.ax.plot( [R(-l,h)[0], R(l,h)[0]], [R(-l,h)[1], R(l,h)[1]], color="black", lw=3*self.weight)
        self.suppv2, = self.ax.plot( [R(0,h)[0], R(0,h-ih)[0]], [R(0,h)[1], R(0,h-ih)[1]],color="black", lw=3*self.weight)

    def reset(self, pos=None,compression=None):
        
        if(pos == None):
            pos = self.pos
        else:
            self.pos = pos
        if(compression == None):
            compression = self.compression
        else:
            self.compression = compression

        #Función de transformación
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0 if (pos[1][1]-pos[0][1])<0 else np.pi
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) - np.pi/2
            theta = theta if (pos[1][0]-pos[0][0])>0 else theta-np.pi
            return np.matmul([x,y],[[np.cos(theta), np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array([pos[0][0], pos[0][1]])

        #definimos vsriables de apoyo
        s = (0.5+self.compression)
        h = np.sqrt( (pos[0][0] - pos[1][0])**2 + (pos[0][1] - pos[1][1])**2 )*s +0.00001
        ih = 0.1*self.scale*s
        l = 0.4*ih/s

        #validamos que la altura sea valida definiendo una nueva n y comparando con la anterior
        set_n = int((h-2*ih)/ih) if (h-2*ih)%ih<ih/2.217002 else int((h-2*ih)/ih)+1
        #En caso de que la n coincida, recolocamos
        if(self.n == set_n):
            hd = (h-2*ih)/self.n
            #reposicionamos líneas diagonales
            for i in range(1,self.n+1):
                self.diag[i-1].set_data( [R(-ih/s,i*hd)[0],R(ih/s,(i+1)*hd)[0]],[R(-ih/s,i*hd)[1],R(ih/s,(i+1)*hd)[1]] )

            #reposicionamos líneas horizontales
            for i in range(1,self.n+2):
                self.horz[i-1].set_data( [R(-l/2,i*hd)[0],R(l/2,i*hd)[0]], [R(-l/2,i*hd)[1],R(l/2,i*hd)[1]] )

            #reposicionamos los soportes
            self.supph1.set_data( [R(-l,0)[0], R(l,0)[0]], [R(-l,0)[1], R(l,0)[1]] )
            self.suppv1.set_data( [R(0,0)[0],R(0,ih)[0]], [R(0,0)[1], R(0,ih)[1]] )
            self.supph2.set_data( [R(-l,h)[0], R(l,h)[0]], [R(-l,h)[1], R(l,h)[1]] )
            self.suppv2.set_data( [R(0,h)[0], R(0,h-ih)[0]], [R(0,h)[1], R(0,h-ih)[1]] )


        else:
            raise Exception("Non valid spring lenght")
        



class Measure_arrow():
    def __init__(self, ax, pos=[(0.0,0.0),(0.0,0.6)], tag="", tag_pos="left", tag_or = 0, weight=1):
        self.ax = ax
        self.pos = pos
        self.tag = tag
        self.tag_pos = tag_pos
        self.tag_or = tag_or
        self.weight = weight

    def draw(self):
        #variable de longitud
        pos = self.pos
        l = np.sqrt( (pos[0][0] - pos[1][0])**2 + (pos[0][1] - pos[1][1])**2 )

        # definimos una función para hacer la rotación de un vecor
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0 if (pos[1][1]-pos[0][1])<0 else np.pi
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) - np.pi/2
            theta = theta if (pos[1][0]-pos[0][0])>0 else theta-np.pi
            return np.append( np.matmul([x,y],[[np.cos(theta), np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array([pos[0][0], pos[0][1]]), theta)

        # Creamos la flecha
        self.ar = FancyArrowPatch(pos[0],pos[1], arrowstyle='->, head_length={}, head_width={}'.format(10*self.weight,3*self.weight), lw=1*self.weight)
        ax.add_patch(self.ar)

        #creamos el texto
        #extraemos el angulo de rotacion
        theta = R(0,0)[2]
        # Agregamos variable para ajustar alineamiento del texto de acuerdo a parametros del usuario
        hor_al = "center" if self.tag_pos in ["center", "bottom", "top"] else self.tag_pos
        #Se agrega un logatimo al texto para que no crezca de manera lineal con el peso, a diferencia del grosor de las lineas
        self.tag = ax.text(0,0, self.tag, fontsize=18*np.log(self.weight+1), family = "serif", ha=hor_al, rotation=self.tag_or)
        #Ajustamos el angulo de posicion del texto de acuerdo a tag_pos
        ang = np.pi if self.tag_pos == "right" else 0 if self.tag_pos == "left" else -np.pi/2 if self.tag_pos == "top" else np.pi/2 if self.tag_pos == "bottom" else 0
        self.tag.set_position( ( R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2 )[0], R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2))[1] - 0.015*self.weight)

    def reset(self, pos):
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0 if (pos[1][1]-pos[0][1])<0 else np.pi
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) - np.pi/2
            theta = theta if (pos[1][0]-pos[0][0])>0 else theta-np.pi
            return np.append( np.matmul([x,y],[[np.cos(theta), np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array([pos[0][0], pos[0][1]]), theta)
        
        self.pos = pos

        # variables de apoyo
        l = np.sqrt( (pos[0][0] - pos[1][0])**2 + (pos[0][1] - pos[1][1])**2 )
        theta = R(0,0)[2]
        ang = np.pi if self.tag_pos == "right" else 0 if self.tag_pos == "left" else -np.pi/2 if self.tag_pos == "top" else np.pi/2 if self.tag_pos == "bottom" else 0
        # Actualizamos la posicion de la flecha
        self.ar.set_positions(pos[0],pos[1])
        # actualizamos el texto
        self.tag.set_position( ( R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2 )[0], R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2))[1] - 0.015*self.weight)




class Measure_line():
    def __init__(self, ax, pos=[(0.0,0.0),(0.0,0.6)], tag="", tag_pos="left", tag_or = 0, weight=1):
        self.ax = ax
        self.pos = pos
        self.tag = tag
        self.tag_pos = tag_pos
        self.tag_or = tag_or
        self.weight = weight

    def draw(self):
        #variable de longitud
        pos = self.pos
        l = np.sqrt( (pos[0][0] - pos[1][0])**2 + (pos[0][1] - pos[1][1])**2 )

        # definimos una función para hacer la rotación de un vecor
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0 if (pos[1][1]-pos[0][1])<0 else np.pi
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) - np.pi/2
            theta = theta if (pos[1][0]-pos[0][0])>0 else theta-np.pi
            return np.append( np.matmul([x,y],[[np.cos(theta), np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array([pos[0][0], pos[0][1]]), theta)

        # Creamos las tres lineas de la linea de medida
        self.mline, = ax.plot([R(0,0)[0] , R(0,l)[0]], [R(0,0)[1] , R(0,l)[1]],color="k", lw=self.weight)
        self.h1line, = ax.plot([R(-0.025*self.weight,0)[0] , R(0.025*self.weight,0)[0]],[R(-0.025*self.weight,0)[1] , R(0.025*self.weight,0)[1]],color="k", lw=self.weight)
        self.h2line, = ax.plot([R(-0.02*self.weight,l)[0] , R(0.02*self.weight,l)[0]],[R(-0.02*self.weight,l)[1] , R(0.02*self.weight,l)[1]], color="k", lw=self.weight)
        
        #creamos el texto
        #extraemos el angulo de rotacion
        theta = R(0,0)[2]
        # Agregamos variable para ajustar alineamiento del texto de acuerdo a parametros del usuario
        hor_al = "center" if self.tag_pos in ["center", "bottom", "top"] else self.tag_pos
        #Se agrega un logatimo al texto para que no crezca de manera lineal con el peso, a diferencia del grosor de las lineas
        self.tag = ax.text(0,0, self.tag, fontsize=18*np.log(self.weight+1), family = "serif", ha=hor_al, rotation=self.tag_or)
        #Ajustamos el angulo de posicion del texto de acuerdo a tag_pos
        ang = np.pi if self.tag_pos == "right" else 0 if self.tag_pos == "left" else -np.pi/2 if self.tag_pos == "top" else np.pi/2 if self.tag_pos == "bottom" else 0
        self.tag.set_position( ( R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2 )[0], R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2))[1] - 0.015*self.weight)


    def reset(self, pos):
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0 if (pos[1][1]-pos[0][1])<0 else np.pi
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) - np.pi/2
            theta = theta if (pos[1][0]-pos[0][0])>0 else theta-np.pi
            return np.append( np.matmul([x,y],[[np.cos(theta), np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array([pos[0][0], pos[0][1]]), theta)
        
        self.pos = pos

        # variables de apoyo
        l = np.sqrt( (pos[0][0] - pos[1][0])**2 + (pos[0][1] - pos[1][1])**2 )
        theta = R(0,0)[2]
        ang = np.pi if self.tag_pos == "right" else 0 if self.tag_pos == "left" else -np.pi/2 if self.tag_pos == "top" else np.pi/2 if self.tag_pos == "bottom" else 0
        # actualizamos la posicion de las lineas
        self.mline.set_data([R(0,0)[0] , R(0,l)[0]], [R(0,0)[1] , R(0,l)[1]])
        self.h1line.set_data([R(-0.025*self.weight,0)[0] , R(0.025*self.weight,0)[0]],[R(-0.025*self.weight,0)[1] , R(0.025*self.weight,0)[1]])
        self.h2line.set_data([R(-0.02*self.weight,l)[0] , R(0.02*self.weight,l)[0]],[R(-0.02*self.weight,l)[1] , R(0.02*self.weight,l)[1]])
        # actualizamos la posicion del texto
        self.tag.set_position( ( R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2 )[0], R(0.045*self.weight*np.cos(-theta+ang), l*1.3*self.weight*np.sin(-theta+ang)/2+l/2))[1] - 0.015*self.weight)





class Surface:
    #función init
    def __init__(self, ax, pos=[(0,0),(1,0)], scale=1, weight=1, direction="br", offset=(0,0)):
        self.ax = ax
        self.pos = pos
        self.scale = scale
        self.weight = weight
        self.direction = direction
        self.offset = offset

    def draw(self):
        # dibujamos las lineas de superficie
        #array para guardar las lineas
        self.surface_lines = []
        #aray para guardar las lineas internas. Este tendra subsarrays para cada linea de superficie
        self.internal_lines = []
        #recorremos los puntos de la superficie
        for i,point in enumerate(self.pos):
            if(i==0):
                #variable para guardar el punto actual y usarlo en la sig iteracion
                prev_point = point
                continue
            self.surface_lines.append( self.ax.plot([prev_point[0], point[0]], [prev_point[1], point[1]], color="black", lw=self.weight)[0])
            
            #calculamos la cantidad de lineas internas a dibujar
            #calculamos la longitud de la superficie
            l = np.sqrt( (prev_point[0] - point[0])**2 + (prev_point[1] - point[1])**2 )
            # separacion de lineas ideal
            idd = self.scale*0.04
            # proporcion entre l y idd
            n = l/idd
            # redondeamos n al entero mas cercano
            n = int(round(n))
            #obtenemos con eso la separacion real entre lineas internas
            d = l/n
            #imprimimos los valores para ver
            self.internal_lines.append([])
            for j in range(n):
                x = prev_point[0]+(point[0]-prev_point[0])*(j+1)/n
                y = prev_point[1]+(point[1]-prev_point[1])*(j+1)/n
                #Agregamos condiciones para br, bl, tr y tl
                if(self.direction == "br"):
                    self.internal_lines[-1].append( self.ax.plot([x,x-self.scale*0.04], [y, y-self.scale*0.03], color="black", lw=self.weight*0.6)[0])
                elif(self.direction == "bl"):
                    self.internal_lines[-1].append( self.ax.plot([x,x+self.scale*0.04], [y, y-self.scale*0.03], color="black", lw=self.weight*0.6)[0])
                elif(self.direction == "tr"):
                    self.internal_lines[-1].append( self.ax.plot([x,x-self.scale*0.04], [y, y+self.scale*0.03], color="black", lw=self.weight*0.6)[0])
                elif(self.direction == "tl"):
                    self.internal_lines[-1].append( self.ax.plot([x,x+self.scale*0.04], [y, y+self.scale*0.03], color="black", lw=self.weight*0.6)[0])
                else:
                    raise Exception("non valid direction")

            #actualizamos el punto anterior
            prev_point = point
        
    def reset(self,offset):
        self.offset = offset
        # Recorremos las lineas de superficie:
        for i,line in enumerate(self.surface_lines):
            # Obtenemos los puntos originales de la línea
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            # Calculamos el nuevo punto de inicio y fin con el offset
            new_xdata = [x + self.offset[0] for x in xdata]
            new_ydata = [y + self.offset[1] for y in ydata]
            # Actualizamos los datos de la línea
            line.set_xdata(new_xdata)
            line.set_ydata(new_ydata)
                # Recorremos las lineas internas
            for internal_line in self.internal_lines[i]:
                # Obtenemos los puntos originales de la línea interna
                xdata = internal_line.get_xdata()
                ydata = internal_line.get_ydata()
                # Calculamos el nuevo punto de inicio y fin con el offset
                new_xdata = [x + self.offset[0] for x in xdata]
                new_ydata = [y + self.offset[1] for y in ydata]
                # Actualizamos los datos de la línea interna
                internal_line.set_xdata(new_xdata)
                internal_line.set_ydata(new_ydata)
    