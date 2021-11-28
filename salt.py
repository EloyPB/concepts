import matplotlib
import matplotlib.pyplot as plt
from Concepts import Net


matplotlib.rcParams.update({'font.size': 12})

net = Net()
net.add_layer("l1", ["tasting", "sweet", "salty", "looking", "white", "black"])
net.add_layer("l2", ["salt", "sugar"], competitive=True)

net.define("salt", [["tasting", "salty"], ["looking", "white"]])
net.define("sugar", [["tasting", "sweet"], ["looking", "white"]])

net.flip(["looking", "white"])
net.run_steps()

net.flip(["looking", "white"])
net.run_steps()

net.flip(["tasting", "sweet"])
net.run_steps(2)

net.flip(["looking", "black"])
net.run_steps()

ax = net.plot()
ax.axhline(6, color='C7')
ax.axvline(1, color='k')
ax.axvline(3, color='k')
ax.axvline(5, color='k')
ax.axvline(8, color='k')


plt.show()

print()