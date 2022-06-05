import data_loader
import prec_esti

import math
import matplotlib.pyplot as plt
import numpy.matlib
import numpy as np


# 参数设置
fitting_mode = 1 #拟合方式，0为平面拟合+平面半参数拟合，1为二次曲面拟合+二次曲面半参数拟合
a_limit = 1 #定义α的搜索上限，下限为0
tolerance = 0.0001 #搜索α时的容差
l_curve_range = 0.5 #绘制L曲线时α的取值范围(±)
l_curve_step = 0.05 #绘制L曲线时α的取值间隔


def proc_data():
	# 准备数据
	x, y, zeta = data_loader.load_data()
	n = x.shape[0] #输入数据向量的维度（个数）
	P = np.matlib.identity(n) #定义权阵为单位矩阵
	if fitting_mode == 0:
		B = np.c_[np.matlib.ones((n, 1)), x, y]
		print("fitting_mode: plane")
	elif fitting_mode == 1:
		B = np.c_[np.matlib.ones((n, 1)), x, y, np.multiply(x, y), np.multiply(x, x), np.multiply(y, y)] #拼接系数矩阵B
		print("fitting_mode: quadric")
	else:
		print("invalid fitting_mode")
		exit()
	R = get_R(n)

	# L曲线法求平滑因子α
	# 黄金分割搜索距离原点最近的α
	golden_var = 1.618
	a, b = 0, a_limit
	c = b - (b - a) / golden_var
	d = a + (b - a) / golden_var
	while abs(c - d) > tolerance:
		SN1, NN1 = get_SN_NN(c, zeta, B, P, R)
		SN2, NN2 = get_SN_NN(d, zeta, B, P, R)
		distance1 = SN1**2 + NN1**2
		distance2 = SN2**2 + NN2**2
		if distance1 < distance2:
			b = d
		else:
			a = c
		c = b - (b - a) / golden_var
		d = a + (b - a) / golden_var
	alpha = round((b + a) / 2, 6)
	SN_final, NN_final = get_SN_NN(alpha, zeta, B, P, R)
	distance = math.sqrt(SN_final**2 + NN_final**2)
	print("alpha:", alpha)
	print("distance:", distance)
	# 绘制最佳α值周边的L曲线
	SN_range, NN_range, a_range = [], [], []
	for i in range(int(2 * l_curve_range / l_curve_step)):
		a_range.append(alpha - l_curve_range + i * l_curve_step)
	for i in a_range:
		SN_var, NN_var = get_SN_NN(i, zeta, B, P, R)
		SN_range.append(SN_var)
		NN_range.append(NN_var)
	plt.plot(np.array(SN_range), np.array(NN_range), "o")
	plt.title("L-Curve")
	plt.xlabel("SN")
	plt.ylabel("NN")
	plt.savefig("L-curve.png")
	plt.show()

	# 计算平差值，非参数矩阵S和参数X
	invN = np.linalg.inv((B.T) * P * B)
	e = np.matlib.ones((n, 1))
	invM = np.linalg.inv(P + alpha * R - P * B * invN * B.T * P)
	W = P - P * B * invN * (B.T) * P
	gamma = ((e.T * invM * W * zeta)[0,0]) / ((e.T * invM * e)[0,0])
	SHat = invM * W * zeta - gamma * invM * e
	XHat = invN * B.T * P * (zeta - SHat)
	V = B * XHat + SHat - zeta
	XHat_nonpara = invN * B.T * P * zeta #未经过半参数模型精化的参数
	V_nonpara = B * XHat_nonpara - zeta
	print("semipara X:\n", XHat)
	print("nonpara X:\n", XHat_nonpara)
	#print("semipara V:\n", V)
	#print("nonpara V:\n", V_nonpara)
	
	# 精度评定
	u0, u0_n = prec_esti.get_u0(V, V_nonpara)
	x_v, y_v, zeta_v = data_loader.load_verify_data() #加载验证集
	n_v = x_v.shape[0] #验证数据向量的维度（个数）
	if fitting_mode == 0:
		B_v = np.c_[np.matlib.ones((n_v, 1)), x_v, y_v]
	elif fitting_mode == 1:
		B_v = np.c_[np.matlib.ones((n_v, 1)), x_v, y_v, np.multiply(x_v, y_v), np.multiply(x_v, x_v), np.multiply(y_v, y_v)]
	P_v = np.matlib.identity(n_v)
	R_v = get_R(n_v)
	e_v = np.matlib.ones((n_v, 1))
	S_v = (1 / alpha) * np.linalg.inv(P_v + R_v) * (P_v * zeta_v - P_v * B_v * XHat - gamma * e_v)
	zetaHat = B_v * XHat + S_v
	zetaHat_nonpara = B_v * XHat_nonpara
	w0, w0_n = prec_esti.get_w0(zetaHat - zeta_v, zetaHat_nonpara - zeta_v)
	print("u0 (semipara):", u0)
	print("u0 (nonpara):", u0_n)
	print("w0 (semipara):", w0)
	print("w0 (nonpara):", w0_n)

	# 保存至excel
	data_loader.save_data(zetaHat, zetaHat_nonpara, SHat)

# 时间序列法求正则矩阵R
# 输入：R的阶数n (int)
# 返回值：n阶正则矩阵R (np.mat)
def get_R(n):
	G = np.matlib.zeros((n - 1, n))
	for i in range(G.shape[0]):
		for j in range(G.shape[1]):
			if i == j:
				G[i,j] = -1
			elif j == i + 1:
				G[i,j] = 1
	return G.T * G

# 计算SN、NN
# 输入: 平滑因子α (int or float), 观测向量zeta (np.mat), 系数矩阵B (np.mat), 权阵P (np.mat), 正则矩阵R(np.mat)
# 返回值: SN(int or float), NN(int or float)
def get_SN_NN(a, zeta, B, P, R):
	invN = np.linalg.inv((B.T) * P * B)
	e = np.matlib.ones((zeta.shape[0], 1))
	invM = np.linalg.inv(P + a * R - P * B * invN * B.T * P)
	W = P - P * B * invN * B.T * P
	gamma = ((e.T * invM * W * zeta)[0,0]) / ((e.T * invM * e)[0,0])
	S = invM * W * zeta - gamma * invM * e
	X = invN * B.T * P * (zeta - S)
	V = B * X + S - zeta
	return ((S.T * R * S)[0,0], (V.T * P * V)[0,0])


if __name__ == "__main__":
    proc_data()