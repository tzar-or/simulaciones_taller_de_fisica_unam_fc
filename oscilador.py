def oscilador():
    # importamos las librerías necesarias
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from matplotlib.animation import FuncAnimation
    
    # creamos los objetos
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    fig.set_size_inches(8, 8)  # 800x800 pixeles a 100 dpi
    fig.dpi = 100  #fijamos los dpi a 100 para la figura
    square = Rectangle((-0.1, -0.1), 0.2, 0.2)
    ax.add_patch(square)
    
    #fijamos los fps para la animación
    fps = 50

    # le preguntamos al usuario la amplitud inicial
    A = float(input("Ingrese la amplitud inicial (entre 0 y 1): "))
    # preguntamos por la masa y la constante k para calcular la frecuencia
    m = float(input("Ingrese la masa (en kg): "))
    k = float(input("Ingrese la constante del resorte (en N/m): "))
    omega = np.sqrt(k / m)  # frecuencia angular

    # función de inicialización para la animación
    def init():
        x = -0.1 + A*np.cos(0)  # posición inicial con la amplitud dada
        square.set_xy((x, -0.1))
        return square,
    def update(frame):  
        x = -0.1 + A*np.cos(omega * frame / fps)  # posición en función del tiempo
        square.set_xy((x, -0.1))
        return square,

    # preguntamos por el tiempo (en segundos) que durará la animación
    print("Ingrese el tiempo de la animación (en segundos): ")
    t = float(input())

    frames = np.arange(0, int(t * fps)  , 1)
    ani = FuncAnimation(fig, update, frames=frames, init_func=init,
                        blit=True, interval=1000/fps)  # intervalo en ms para los fps deseados
    
    ani.save('oscilador_armonico_simple.mp4', writer='ffmpeg', fps=fps)
    
oscilador()