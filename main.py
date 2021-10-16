#imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import magpylib as magpy
from scipy.spatial.transform import Rotation as R

#init variables
stationary_magnets = 5
strength_magnets = 200
strength_solenoid = 50

#graph calculation parameters
density = 1
num_calc = 100

#animation parameters
frames = 30
interval = 100

#create magnets
mag_rot = R.from_euler('y', np.pi/2)
mag1 = magpy.magnet.Cylinder(magnetization=[0,0,strength_magnets],dimension=[1,2],position=[-stationary_magnets,0,0], orientation=mag_rot)
mag2 = magpy.magnet.Cylinder(magnetization=[0,0,strength_magnets],dimension=[1,2],position=[stationary_magnets,0,0], orientation=mag_rot)

#for simlicity assume that the solenoid is a cylindrical magnet
sol = magpy.magnet.Cylinder(magnetization=[0,0, strength_solenoid], dimension=[2,5], orientation=R.from_euler('y', -90.1, degrees=True))


#create collection
def create_collection():
    return magpy.Collection(mag1,mag2,sol)

#calculate B-field
def calc_field(c):
    xs = np.linspace(-10,10,num_calc)
    zs = np.linspace(-10,10,num_calc)
    Bs = np.array([[c.getB([x,0,z]) for x in xs] for z in zs])
    field = (xs, zs, Bs)
    return field

#rotate solenoid
def rotate_solenoid():
    omega = (2*np.pi)/60
    sol.rotate(R.from_euler('y', omega))
        

#display geometry of the motor
#fig1 = create_collection().display()        

#display field
fig, ax = plt.subplots()
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)

#calculate filed for 2D representation
def val(field):
    X,Z = np.meshgrid(field[0],field[1])
    U,V = field[2][:,:,0], field[2][:,:,2]
    return X,Z,U,V

X,Z,U,V = val(calc_field(create_collection()))
#plot onto 2D space
stream = ax.streamplot(X, Z, U, V, color=np.log(U**2+V**2),density=density)
plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')    # remove ticks

#init for animation
def init():
    stream.set_array([])
    return stream

#animate
def animate(iter):
    ax.cla()
    rotate_solenoid()
    X,Z,U,V = val(calc_field(create_collection()))
    ax.streamplot(X, Z, U, V, color=np.log(U**2+V**2), density=density)
    plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    print(iter)

#call animation and save as gif
anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval, blit=False, repeat=False)
anim.save('./field.gif', writer='imagemagick', fps=120)

#disable anim to get a static picture to save as svg-file.
#plt.show()
