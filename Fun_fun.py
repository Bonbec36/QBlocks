import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Vecteur k
k = np.array([0, 1, 0])
origin = np.array([0, 0, 0])

# Vecteur de polarisation circulaire dans le plan orthogonal à k
v_perpendicular = np.array([-k[1], k[0], 0])  # Orthogonal à k dans le plan xy

# Définition du vecteur de polarisation circulaire
u = np.cross(k, v_perpendicular)  # Perpendiculaire à k et v_perpendicular

# Création de la figure et de l'axe 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Paramètres de l'axe
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Fonction d'initialisation de l'animation
def init():
    ax.quiver(*origin, *k, color='b', label='k', length=1)
    ax.quiver(*origin, *u, color='r', label='Polarisation circulaire', length=1)
    ax.legend()
    return fig,

# Fonction de mise à jour de l'animation
def update(frame):
    ax.clear()
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    theta = frame * 0.1  # Angle de rotation
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
    new_u = np.dot(rotation_matrix, u)
    ax.quiver(*origin, *k, color='b', label='k', length=1)
    ax.quiver(*origin, *new_u, color='r', label='Polarisation circulaire', length=1)
    ax.legend()
    return fig,

# Création de l'animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 2*np.pi, 0.1), init_func=init, blit=True)

plt.show()
