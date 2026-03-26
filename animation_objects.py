import matplotlib.pyplot as plt
import numpy as np

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
        # por default, cada linea diagonal, a escala E será de de 0.2*E x A,
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
        self.n = int((h-2*ih)/ih) if (h-2*ih)%ih<ih/2.217002 else int((h-2*ih)/ih)+1
        #definimos la altura real de las diagonales
        hd = (h-2*ih)/self.n

        # definimos una función para hacer la rotación de un vecor
        def R(x,y,pos = pos):
            #definimos el angulo de la rotación
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) + np.pi/2
            theta = theta if (pos[1][1]-pos[0][1])>0 else theta-np.pi
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
            #revisamos que no compartan el mismo valor de X los puntos para no dividir entre 0
            if( (pos[1][0]-pos[0][0])==0 ):
                theta = 0
            else:
                theta = np.arctan( (pos[1][1]-pos[0][1])/(pos[1][0]-pos[0][0]) ) + np.pi/2
            theta = theta if (pos[1][1]-pos[0][1])>0 else theta-np.pi
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