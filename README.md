# 利用半参数模型精化多项式GNSS高程拟合模型

毕业设计存档

# 测试环境

- Windows 10
- Python 3.7.6
- NumPy 1.18.1
- Matplotlib 3.1.3
- OpenPyXL 3.0.3

use ```pip install -r requirements.txt```

# L-曲线绘制

- L曲线图混乱：如果数据的XY坐标有负值，建议给每个坐标都加上一个大数确保坐标均为正值
- L曲线图呈一条直线：增加l_curve_range

# 已知问题

- linux环境下矩阵求逆结果不一致