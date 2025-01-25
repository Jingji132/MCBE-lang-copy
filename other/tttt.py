import numpy as np
import matplotlib.pyplot as plt

def gaussian_membership(x, mean, sigma):
    """
    计算高斯隶属函数。

    :param x: 输入数据（数组）
    :param mean: 高斯分布的均值
    :param sigma: 高斯分布的标准差
    :return: 隶属度值
    """
    return np.exp(-0.5 * ((x - mean) / sigma) ** 2)

def clamp_values(y, lower_limit=0, upper_limit=1):
    """
    限定隶属函数的输出值范围。

    :param y: 隶属函数值（数组）
    :param lower_limit: 最小值
    :param upper_limit: 最大值
    :return: 限定后的值
    """
    return np.clip(y, lower_limit, upper_limit)

# 定义x范围和参数
x = np.linspace(-10, 10, 500)  # x从-10到10
mean1, sigma1 = 0, 2  # 第一个高斯函数参数
mean2, sigma2 = 3, 1  # 第二个高斯函数参数
mean3, sigma3 = -3, 1.5  # 第三个高斯函数参数

# 计算高斯隶属函数值
y1 = gaussian_membership(x, mean1, sigma1)
y2 = gaussian_membership(x, mean2, sigma2)
y3 = gaussian_membership(x, mean3, sigma3)

# 限定值范围
y1 = clamp_values(y1, 0, 1)
y2 = clamp_values(y2, 0, 1)
y3 = clamp_values(y3, 0, 1)

# 绘制图像
plt.figure(figsize=(10, 6))
plt.plot(x, y1, label=f"Mean={mean1}, Sigma={sigma1}", color="blue")
plt.plot(x, y2, label=f"Mean={mean2}, Sigma={sigma2}", color="green")
plt.plot(x, y3, label=f"Mean={mean3}, Sigma={sigma3}", color="red")
plt.title("Gaussian Membership Functions with Clamping", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("Membership Degree", fontsize=12)
plt.grid(alpha=0.5)
plt.legend(fontsize=10)
plt.show()
