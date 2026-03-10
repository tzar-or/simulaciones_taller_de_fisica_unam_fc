def oscilador():
    # importamos las librerías necesarias
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.animation import FuncAnimation
    
    # creamos las figuras
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(16,8), gridspec_kw={'width_ratios':[1,2,1]}, sharey=False, constrained_layout=False)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.3)
    ax3.set_xlim(0,1)
    ax2.set_xlim(-0.8, 0.8)
    ax1.set_xlim(0,1)
    ax3.set_ylim(-1,1)
    ax2.set_ylim(-1,1)
    ax1.set_ylim(-1,1)
    ax1.axhline(0)
    ax3.axhline(0)
    fig.dpi = 100  #fijamos los dpi a 100 para la figura
    fig.set_size_inches(16, 8)  # 1800x800 pixeles a 100 dpi ()

    # Se crean los objetos
    square = Rectangle((-0.1, -0.1), 0.2, 0.2)
    ax2.add_patch(square)
    y_, = ax3.plot([],[],"r-")
    dy_, = ax1.plot([],[],"r-")
    flecha_v = FancyArrowPatch((-0.5,0),(-0.5,0), arrowstyle='->, head_length=10, head_width=5')
    flecha_v2 = FancyArrowPatch((-0.5,0),(-0.5,0), arrowstyle='->, head_length=10, head_width=5')
    ax2.add_patch(flecha_v)
    ax1.add_patch(flecha_v2)
    pos_y, = ax2.plot([0.4,0.4],[0,0],"r-")


    #creamos los arrays que se grafican
    T,Y,dY = [],[],[]


    
    #fijamos los fps para la animación
    fps = 25

    # le preguntamos al usuario la amplitud inicial
    A = float(input("Ingrese la amplitud inicial (entre 0 y 1): "))
    # preguntamos por la masa y la constante k para calcular la frecuencia
    m = float(input("Ingrese la masa (en kg): "))
    k = float(input("Ingrese la constante del resorte (en N/m): "))
    omega = np.sqrt(k / m)  # frecuencia angular


    # función de inicialización para la animación
    def init():
        y = -0.1 + A*np.cos(0)  # posición inicial con la amplitud dada
        square.set_xy((-0.1, y))
        dy = A*omega*np.sin(0)
        flecha_v.set_positions((-0.5,0),(-0.5,dy))
        flecha_v2.set_positions((0.0,0),(0.0,dy))
        ax1.set_ylim(-1.1*A*omega,1.1*A*omega)
        return square, y_, dy_, pos_y
    def update(frame):
        y = -0.1 + A*np.cos(omega * frame / fps)  # posición en función del tiempo
        dy = -A*omega*np.sin(omega * frame / fps)
        square.set_xy((-0.1, y))
        flecha_v.set_positions((-0.4,y+0.1),(-0.4,y+0.5*dy/(A*omega)+0.1))
        flecha_v2.set_positions((frame/fps,0),(frame/fps,dy))
        T.append( frame/fps )
        Y.append(y+0.1)
        dY.append(dy)
        y_.set_data(T,Y)
        dy_.set_data(T,dY)
        pos_y.set_data( [0.4,0.4], [0,y+0.1] )
        ax1.set_xlim(frame/fps-1.8, frame/fps+0.2)
        ax3.set_xlim(frame/fps-1.8, frame/fps+0.2)
        return square, flecha_v, flecha_v2, y_, dy_, pos_y
        

    # preguntamos por el tiempo (en segundos) que durará la animación
    print("Ingrese el tiempo de la animación (en segundos): ")
    t = float(input())

    frames = np.arange(0, int(t * fps)  , 1)
    ani = FuncAnimation(fig, update, frames=frames, init_func=init,
                        blit=True, interval=1000/fps)  # intervalo en ms para los fps deseados
    
    ani.save('oscilador_armonico_simple.mp4', writer='ffmpeg', fps=fps)
    
oscilador()