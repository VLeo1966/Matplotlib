import numpy as np
import matplotlib.pyplot as plt

# Генерация двух наборов случайных данных
x = np.random.rand(100)
y = np.random.rand(100)

# Построение диаграммы рассеяния
plt.scatter(x, y, color='green')
plt.title('Диаграмма рассеяния')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
