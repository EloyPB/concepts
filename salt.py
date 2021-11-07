from Concepts import Net


net = Net()
net.add_layer("l1", ["tasting", "sweet", "salty", "looking", "white", "blue"])
net.add_layer("l2", ["salt", "sugar"], competitive=True)

net.define("salt", [["tasting", "salty"], ["looking", "white"]])
net.define("sugar", [["tasting", "sweet"], ["looking", "white"]])

net.flip(["looking", "white"])
net.run_steps()

net.flip(["looking", "white"])
net.run_steps()

net.flip(["tasting", "sweet"])
net.run_steps()

net.flip(["looking", "blue"])
net.run_steps()

net.plot()

print()