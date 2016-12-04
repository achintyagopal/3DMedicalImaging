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
            max_dist = None
            max_index = None
            i = 0
            for test_inst in self.instances:
                dist = np.linalg.norm(test_inst.get_vector() - instance.get_vector())
                if max_index is None or dist > max_dist:
                    dist = max_dist
                    max_index = i
                i += 1
            labels.append(instance[max_index].get_label())
        return labels
