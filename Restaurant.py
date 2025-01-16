import matplotlib.pyplot as plt
import numpy as np

x = np.array([45, 25, 10, 20])
label = [" Pizza", "Chicken", "Coffee", "Hotdog"]
plt.pie(x, labels = label)

plt.title(" Sales")
plt.legend(loc = "lower right")
plt.show()
    