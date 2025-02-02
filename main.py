import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# Função para criar matriz DH
def dh_matrix(theta, d, a, alpha):
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

# Função para definir eixos iguais
def set_axes_equal(ax):
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d()
    ])
    min_limit = limits.min()
    max_limit = limits.max()
    ax.set_xlim3d([min_limit, max_limit])
    ax.set_ylim3d([min_limit, max_limit])
    ax.set_zlim3d([min_limit, max_limit])

theta = [ np.radians(0) ,       #0
          np.radians(10) ,     #1
          np.radians(40) ,      #2
          np.radians(0) ,       #3
          np.radians(0) ,       #4
          np.radians(0)        #5
]

# Matriz DH (theta, d, a, alpha)
dh_params = [
    [theta[0] , 520, 0, np.radians(90)],
    [theta[1] , 0, 780, 0],
    [theta[2] + np.radians(90) , 0, 0, np.radians(-90)],
    [theta[3] , 860 , 0 , np.radians(90)],
    [theta[4] , 0, 153, np.radians(90)],
    [theta[5] , 0, 0, np.radians(0)],
]

# Função para atualizar o gráfico com base nos ângulos
def update(val):
    theta_vals = [slider.val for slider in sliders]
    positions = [np.array([0, 0, 0])]
    T_current = np.eye(4)

    for i, params in enumerate(dh_params):
        params[0] = theta_vals[i] if i == 2 else theta_vals[i] + np.radians(90)   # Atualiza theta_i
        T_next = dh_matrix(*params)
        T_current = np.dot(T_current, T_next)
        positions.append(T_current[:3, 3])

    positions = np.array(positions)
    x_vals, y_vals, z_vals = positions[:, 0], positions[:, 1], positions[:, 2]

    ax.cla()  # Limpa o gráfico atual
    ax.plot(x_vals, y_vals, z_vals, 'bo-', label='Elos')
    ax.scatter(x_vals[-1], y_vals[-1], z_vals[-1], color='g', s=100, label='End-Effector')
    set_axes_equal(ax)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_zlabel("Eixo Z")
    ax.legend()

    #Exibe as coordenadas do end-effector no canto do gráfico
    ax.text2D(0.05, 0.95, f"End-Effector:\nX = {x_vals[-1]:.2f}\nY = {y_vals[-1]:.2f}\nZ = {z_vals[-1]:.2f}",
              transform=ax.transAxes, fontsize=10, color='red')

    plt.draw()

# Configuração do plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Sliders para cada variável theta
ax_slider_positions = [plt.axes([0.1, 0.01 + 0.04 * i, 0.8, 0.03]) for i in range(6)]
sliders = [Slider(ax_slider_positions[i], f'Theta {i}', -np.pi, np.pi, valinit=theta[i]) for i in range(6)]

# Conectar sliders à função de atualização
for slider in sliders:
    slider.on_changed(update)

# Exibe o gráfico inicial
update(None)
plt.show()
