import numpy as np
import instance

class KNN():

    def __init__(self):
        self.instances = None

    def train(self, instances):
        self.instances = instances

    def test(self, instances):
        labels = []
        for instance in instances:
            min_dist = None
            min_index = None
            i = 0
            for test_inst in self.instances:
                dist = np.linalg.norm(test_inst.get_vector() - instance.get_vector())
                if min_index is None or dist < min_dist:
                    dist = min_dist
                    min_index = i
                i += 1
            labels.append(instance[min_index].get_label())
        return labels
