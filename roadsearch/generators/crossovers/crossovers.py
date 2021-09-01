import random
from typing import Dict, List
import logging as log


class Crossover:

    def __init__(self, size: int = 20, frequency: int = 50):
        # Set crossover frequency to 0 for no crossover
        self.size = size
        self.min_size = 4
        self.frequency = frequency

    def similarity(self, parent_1, parent_2):
        min_len = min(len(parent_1), len(parent_2))
        same_count = 0
        for i in range(min_len):
            if parent_1[i] == parent_2[i]:
                same_count += 1
        return 0.0 if min_len == 0 else same_count/min_len

    def generate(self, candidates: Dict):
        """
            candidates: a list of candidate tests to be chosen as parents
            returns: a list of children of (almost) same size
        """
        children = []
        attemps = 0
        target_children = min(self.size, len(candidates))
        if candidates and len(candidates) > self.min_size:
            while len(children) < target_children and attemps < target_children * 2:
                parent_1_id, parent_2_id = random.sample(candidates.keys(), 2)
                parent_1, parent_1_info = candidates.get(parent_1_id)
                parent_2, parent_2_info = candidates.get(parent_2_id)
                if self.similarity(parent_1, parent_2) < 0.95:
                    newborns = self.chromosome_crossover(parent_1, parent_2)
                    method = 'chromosome crossover'
                    for child in newborns:
                        children.append((child, method, self.combine_parents_info(parent_1_info, parent_2_info)))
                else:
                    log.info("Discarding parents combination due to genetic similarity")
                    
        return children

    @staticmethod
    def combine_parents_info(parent_1_info, parent_2_info):
        info = {}
        info.update(parent_1_info)
        for k, v in parent_2_info.items():
            if k == 'generation':
                info['generation'] = max(parent_2_info['generation'], info['generation'])
            else:
                p2_label = k.replace('1', '2')
                info[p2_label] = v
        # if one of the two parents already failed we do not revisit this test
        info['visited'] = parent_1_info['parent_1_outcome'] == 'FAIL' or parent_2_info['parent_1_outcome'] == 'FAIL'
        return info

    @staticmethod
    def chromosome_crossover(parent_1: List, parent_2: List):
        """
            parent_1: list of test
            parent_2: list of test
            returns: a list of test of the length of the shortest list
        """
        child_1 = []
        child_2 = []
        for i in range(min(len(parent_1), len(parent_2))):
            if random.random() < 0.5:
                child_1.append(parent_1[i])
                child_2.append(parent_2[i])
            else:
                child_1.append(parent_2[i])
                child_2.append(parent_1[i])

        return [child_1, child_2]

    @staticmethod
    def single_point_crossover(parent_1: List, parent_2: List):
        """
            parent_1: list of test
            parent_2: list of test
            returns: Two lists of test
        """
        child_1 = parent_1[len(parent_1) // 2:] + parent_2[:len(parent_2) // 2]
        child_2 = parent_2[len(parent_2) // 2:] + parent_1[:len(parent_1) // 2]
        return [child_1, child_2]
