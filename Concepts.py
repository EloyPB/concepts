import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


class Unit:
    def __init__(self, group_name, name):
        self.group_name = group_name
        self.name = name

        self.head = [0]
        self.should = [0]
        self.should_not = [0]

        self.supporters = []
        self.triggers = []
        self.dependents = []

    def update_head(self, step_num):
        next_head = self.head[-1]

        if self.head[-1]:
            for dependent in self.dependents:
                if dependent.error(step_num):
                    next_head = 0
                    break
        else:
            for trigger_set in self.triggers:
                if all([unit.head[step_num] for unit in trigger_set]):
                    next_head = 1
                    break

        self.head.append(next_head)

    def update_error(self):
        support = 0
        for supporter_set in self.supporters:
            if all([unit.head[-1] for unit in supporter_set]):
                support = 1
                break

        self.should.append(max(0, support - self.head[-1]))
        self.should_not.append(max(0, self.head[-1] - support))

    def error(self, step_num):
        return self.should[step_num] or self.should_not[step_num]


class Net:
    def __init__(self):
        self.units = []
        self.names = []
        self.competitive = []
        self.step_num = 0

    def add_layer(self, layer_name, names, competitive=False):
        layer = {}
        for name in names:
            layer[name] = Unit(layer_name, name)
        self.units.append(layer)
        self.competitive.append(competitive)
        self.names.append(names)

    def flip(self, names):
        for layer in self.units:
            for name, unit in layer.items():
                if name in names:
                    unit.head.append(not unit.head[-1])
                else:
                    unit.head.append(unit.head[-1])
        for layer in self.units:
            for unit in layer.values():
                unit.update_error()
        self.step_num += 1

    def get(self, name):
        for layer_num, layer in enumerate(self.units):
            if name in layer:
                return layer_num, layer[name]

    def define(self, name, triggers):
        layer_num, unit = self.get(name)

        for trigger_set in triggers:
            trigger_set = [self.get(trigger)[1] for trigger in trigger_set]
            unit.triggers.append(trigger_set)

            for trigger in trigger_set:
                trigger.supporters.append([unit] + [t for t in trigger_set if t is not trigger])

        unit.dependents = self.units[layer_num - 1].values() if layer_num > 0 else []

    def competition(self, layer_num):
        if self.step_num:
            heads = np.array([unit.head[-1] for unit in self.units[layer_num].values()]).astype(float)
            if np.sum(heads > 0) > 1:
                heads += np.array([unit.head[-2] for unit in self.units[layer_num].values()])
                heads += np.random.random(heads.size) * 0.1
                winner = self.names[layer_num][np.argmax(heads)]
                for unit in self.units[layer_num].values():
                    if unit.name == winner:
                        unit.head[-1] = 1
                    else:
                        unit.head[-1] = 0

    def run_steps(self, num_steps=1):
        for n in range(num_steps):
            for layer_num, (layer, competitive) in enumerate(zip(self.units, self.competitive)):
                for unit in layer.values():
                    unit.update_head(self.step_num)
                if competitive:
                    self.competition(layer_num)

            for layer in self.units:
                for unit in layer.values():
                    unit.update_error()
            self.step_num += 1

    def plot(self):
        names = []
        head_all = []
        should_all = []
        should_not_all = []

        for layer_num, layer in enumerate(self.units):
            for name, unit in layer.items():
                names.append(name)
                head_all.append(unit.head)
                if layer_num != len(layer) - 1:
                    should_all.append(unit.should)
                    should_not_all.append(unit.should_not)
                else:
                    zeros = np.zeros(len(unit.head))
                    should_all.append(zeros)
                    should_not_all.append(zeros)

        reds = colors.LinearSegmentedColormap.from_list('reds', [(0, 0, 0, 0), (1, 0, 0, 1)], N=2)
        greens = colors.LinearSegmentedColormap.from_list('greens', [(0, 0, 0, 0), (0, 1, 0, 1)], N=2)
        blues = colors.LinearSegmentedColormap.from_list('blues', [(0, 0, 0, 0), (0, 0, 1, 1)], N=2)

        fig, ax = plt.subplots()
        ax.matshow(head_all, origin='lower', cmap=blues)
        ax.matshow(should_all, origin='lower', cmap=greens)
        ax.matshow(should_not_all, origin='lower', cmap=reds)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.xaxis.set_ticks_position('bottom')

        plt.show()
