def barco_momento():
    # Importamos las librerías necesarias
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.patches import Rectangle
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.patches import Polygon
    from animation_objects import Surface
    from animation_objects import Measure_line
    from animation_objects import Measure_arrow

    # Ruta de la imagen Cheems
    cheems_image_path = "img/Cheems-PNG.png"

    # Creamos la figura y el eje
    fig, ax = plt.subplots(figsize=(16,8), )
    ax.set_xlim(0, 2)  # Establecer los límites del eje x
    ax.set_ylim(0, 1)   # Establecer los límites del eje y
    # Fijamos parametros de la animación
    fig.dpi = 90  #fijamos los dpi a 100 para la figura
    fig.set_size_inches(16, 8)  # 1440x720 pixeles a 90 dpi ()
    fps = 25

    #Creamos los objetos
    # imagen del Cheems
    cheems_image = plt.imread(cheems_image_path)
    image_artist = ax.imshow(cheems_image, extent=[0, 0.1, 0.2, 0.3])  # Posición inicial
    # linea del agua
    ax.plot( [0.2,2], [0.35,0.35] , zorder=0)
    # superficies de referencia
    superficie1 = Surface(ax, pos=[(0,0.4),(0.1,0.4),(0.4,0.1),(2,0.1)], direction="br", weight=1.5)
    superficie2 = Surface(ax, pos=[(1.3,1),(1.3,0.9), (1.4,0.9)], direction="tl", weight=1.5, scale=0.5)
    # bote
    puntos_bote = np.array([[0.5, 0.4], [1.3, 0.4], [1.2, 0.3], [0.6, 0.3]])
    poligono_bote = Polygon(puntos_bote, closed=True, facecolor="white", edgecolor="black", lw=1.5, alpha=1)
    #creamos los mastiles y banderas de referencia
    mastil1 = Rectangle( (1.29,0.4), 0.01, 0.3, lw=1.5, facecolor="white", edgecolor="black")
    mastil2 = Rectangle( (0.09, 0.4), 0.01, 0.3, lw=1.5, facecolor="white", edgecolor="black")
    mastil3 = Rectangle( (1.29, 0.925), 0.01, 0.05, lw=1.5, facecolor="white", edgecolor="black")
    puntos_bandera1 = np.array([[1.3, 0.7], [1.38, 0.675], [1.3, 0.65]])
    bandera1 = Polygon( puntos_bandera1, closed=True, facecolor="white", edgecolor="black", lw=1.5, alpha=1 )
    bandera2 = Polygon(np.array([[0.09, 0.7], [0.01, 0.675], [0.09, 0.65]]), closed=True, facecolor="white", edgecolor="black", lw=1.5, alpha=1)
    bandera3 = Polygon(np.array([[1.29, 0.975], [1.21, 0.95], [1.29, 0.925]]), closed=True, facecolor="white", edgecolor="black", lw=1.5, alpha=1)
    #Creamos las lineas y flechas de medida
    lm_flag_dog = Measure_line(ax, pos=[(1.3,0.8),(1.299,0.8)], tag=r"$Δ x_p$", tag_pos="right")
    lm_flag_flag = Measure_line(ax, pos=[(1.3,0.8),(1.301,0.8)], tag=r"$Δ x_b$", tag_pos="left")
    fm_flag_dog = Measure_arrow(ax, pos=[(1.3, 0.55),(1.299,0.55)], tag='$x_{pb}$' )
    fm_flag_dog2 = Measure_arrow(ax, pos=[(0.12, 0.55),(1.1,0.55)], tag='$x_{ps}$' ) 



    # Pedimos los datos al usuario
    masa_perro = float( input("Ingresa la masa del perro: ") )
    masa_barco = float( input("Ingresa la masa del barco: ") )
    DXpi = -float( input("Ingresa el desplazamiento del perro dentro del barco: ") )
    t = float( input("Ingresa el tiempo que tarda el perro en desplazarse: ") )

    # Calculamos el resto de los desplazamientos
    DXb = -masa_perro * DXpi / (masa_barco + masa_perro)
    DXpt = DXpi + DXb

    print(DXb)


    def init():
        image_artist.set_extent([ 1.1, 1.3, 0.4, 0.6])  # Posición inicial
        fig.savefig("FF-problema_del_perro_barco_momento.png")
        superficie1.draw()
        superficie2.draw()
        ax.add_patch(poligono_bote)
        ax.add_patch(mastil1)
        ax.add_patch(mastil2)
        ax.add_patch(mastil3)
        ax.add_patch(bandera1)
        ax.add_patch(bandera2)
        ax.add_patch(bandera3)
        lm_flag_dog.draw()
        lm_flag_flag.draw()
        fm_flag_dog.draw()
        fm_flag_dog2.draw()
        return image_artist,  




    # Función de actualización para la animación
    # Lo que se tiene que actualizar (lo que se mueve en la animación), es lo siguiente
    # La imagen del perro, el bote, la bandera del bote, y las 2 lineas de medida con
    # las dos flechas de medida.
    def update(frame):
        #si el frame no es el ultimo de movimiento (que es t*fps)
        if frame < int(t*fps):
            # Movemos la imagen del perro sumando a la posicion inicial el producto del desplazamiento total
            # por el cociente entre frame y frames totales.
            image_artist.set_extent([ 1.1 + DXpt*frame/int(t * fps), 1.3 + DXpt*frame/int(t * fps), 0.4, 0.6])
            # De la misma forma, el bote, actualizando la variable puntos_bote
            puntos_bote[:,0] = puntos_bote[:,0] + DXb/int(t * fps)
            print()
            poligono_bote.set_xy(puntos_bote)
        else:
            pass

        return image_artist, #poligono_bote, #bandera1, bandera2, bandera3, lm_flag_dog, lm_flag_flag, fm_flag_dog, fm_flag_dog2




    # Crear la animación
    #sumamos 3*fps para dejar 3 segundos extra para ver el resultado
    frames = np.arange(0, int(t*fps + 3*fps) , 1)

    ani = FuncAnimation(fig, update, init_func=init, frames=frames, interval=1000/fps, blit=True)

    ani.save('problema_del_perro_barco_momento.mp4', writer='ffmpeg', fps=fps)

# Llamar a la función para ejecutar la animación
barco_momento()
