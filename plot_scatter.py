import data_loader
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


rcParams['font.sans-serif'] = ['SimSun']
rcParams['font.size'] = 14

x, y, z = data_loader.load_data()
x = np.array(x)
y = np.array(y)
z = np.array(z)
z = z - z.min()

x_v, y_v, z_v = data_loader.load_verify_data()
x_v = np.array(x_v)
y_v = np.array(y_v)
z_v = np.array(z_v)
z_v = z_v - z_v.min()

#绘制平面散点图
plt.figure('scatter 2d')
plt.scatter(y, x, marker="^", label='拟合点')
plt.scatter(y_v, x_v, c='r', label='检核点')
plt.xlabel('Y')
plt.ylabel('X')
plt.legend(loc=0)
plt.savefig('scatter_2d.png')
plt.show()

#绘制三维散点图
fig = plt.figure('scatter 3d')
ax3d = Axes3D(fig)
ax3d.scatter(y, x, z, marker="^", label='拟合点')
ax3d.scatter(y_v, x_v, z_v, c='r', label='检核点')

z0 = np.zeros(z.shape)
z0_v = np.zeros(z_v.shape)
for i in range(x.shape[0]):
	xn = np.array([x[i],x[i]]).flatten()
	yn = np.array([y[i],y[i]]).flatten()
	zn = np.array([z[i],z0[i]]).flatten()
	ax3d.plot(yn, xn, zn, 'c:')
for j in range(x_v.shape[0]):
	xn = np.array([x_v[j],x_v[j]]).flatten()
	yn = np.array([y_v[j],y_v[j]]).flatten()
	zn = np.array([z_v[j],z0_v[j]]).flatten()
	ax3d.plot(yn, xn, zn, 'y:')

ax3d.set_xlabel('Y')
ax3d.set_ylabel('X')
ax3d.set_zlabel('Zeta')
ax3d.legend(loc=0)
plt.savefig('scatter_3d.png')
plt.show()