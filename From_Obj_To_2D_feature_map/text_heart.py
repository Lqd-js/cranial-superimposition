import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def f(x, a):
    # 使函数在x<0时与x>0部分对称
    return np.power(np.abs(x), 2/3) + (np.e / 3) * np.sqrt(np.pi - np.clip(x**2, 0, np.pi)) * np.sin(a * np.pi * np.abs(x))

def init():
    ax.set_xlim(-2, 2)  # x轴范围
    ax.set_ylim(-1.5, 2.5)  # y轴范围
    line.set_color('r')  # 线条颜色
    return line,

def animate(a):
    y = f(x, a)
    line.set_ydata(y)  # 更新线条数据
    # 分两行显示公式和a的值，确保LaTeX格式正确
    ax.set_title(r'$f(x) = |x|^{\frac{2}{3}} + \frac{e}{3}(\pi - x^2)^{\frac{1}{2}}\sin(a\pi|x|)$' + '\n' + r'$a = {:.2f}$'.format(a))
    return line,

if __name__ == "__main__":
    fig, ax = plt.subplots()
    x = np.linspace(-2, 2, 400)
    line, = ax.plot(x, f(x, 0), 'r')  # 初始化红色线条
    ax.grid(True)  # 显示网格
    ax.axhline(0, color='black', lw=1)  # x轴
    ax.axvline(0, color='black', lw=1)  # y轴
    ax.set_xlabel("x")  # x轴标签
    ax.set_ylabel("f(x)")  # y轴标签

    ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 100, 0.1), init_func=init, blit=False, interval=50, repeat=False)

    plt.show()
