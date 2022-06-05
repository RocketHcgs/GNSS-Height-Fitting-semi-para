import math
import numpy as np

# 计算内符合精度
# 输入: 改正数向量V (np.mat), 非参数模型的改正数向量V (np.mat)
# 返回值: 内符合精度u0 (int or float), 非参数模型的内符合精度u0_n (int or float)
def get_u0(V, V_nonpara):
	n = V.shape[0]
	u0 = math.sqrt(((V.T*V)[0,0])/(n - 1))
	u0_n = math.sqrt(((V_nonpara.T*V_nonpara)[0,0])/(n - 1))
	return (u0, u0_n)

# 计算外符合精度
# 输入: 验证集改正数向量V_v (np.mat), 非参数模型验证集的改正数向量V_nonpara_v (np.mat)
# 返回值: 外符合精度w0 (int or float), 非参数模型的外符合精度w0_n (int or float)
def get_w0(V_v, V_nonpara_v):
	n = V_v.shape[0]
	w0 = math.sqrt(((V_v.T*V_v)[0,0])/(n - 1))
	w0_n = math.sqrt(((V_nonpara_v.T*V_nonpara_v)[0,0])/(n - 1))
	return (w0, w0_n)