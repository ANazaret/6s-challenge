import inspect
import logging

import matplotlib.pyplot as plt
import networkx as nx
import networkx.drawing.nx_agraph as nx_drawing
import numpy as np

import operators
from decorators import ProtectionException


class Core:
    def __init__(self, target=(6,)):
        self.operators = list(
            map(lambda f: (f, len(inspect.getfullargspec(f).args)),
                filter(lambda x: 'operator' in x.__annotations__,
                       filter(inspect.isfunction,
                              map(lambda x: getattr(operators, x),
                                  dir(operators))))))
        self.target = target
        self.graph = nx.MultiDiGraph()
        self.graph.add_node(self.target)

        self.visited = set()
        self.visited.add(self.target)
        self.logger = logging.getLogger(__name__)

    def run(self, data):
        if data in self.graph:
            return True
        if data in self.visited:
            return False
        self.visited.add(data)
        self.logger.debug("Visiting : %s", str(data))

        size = len(data)
        success = False
        for op, n_args in self.operators:
            for i in range(0, size - n_args + 1):
                args = data[i:i + n_args]
                self.logger.debug("Calling %s with %s", str(op), str(args))
                try:
                    new_data = data[:i] + op(*args) + data[i + n_args:]
                except ProtectionException as e:
                    self.logger.debug(str(e))
                    continue

                res = self.run(new_data)
                if res:
                    self.graph.add_edge(data, new_data, operator=op, index=i)
                    success = True
        return success

    def plot(self):
        pos = nx_drawing.pygraphviz_layout(self.graph, prog='dot')
        for k in pos:
            x, y = pos[k]
            pos[k] = (x, y + np.random.randint(-10, 10))
        plt.figure(figsize=(20, 12))
        nx.draw(self.graph, pos, with_labels=True, arrows=True, )
        plt.show()
