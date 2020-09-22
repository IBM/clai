#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Datastore:
    def __init__(self):
        self.path = './data'
        self.transformer_func, self.vectors, self.commands = self.read()

    def read(self):
        with open(self.path + '/model/func.p', 'rb') as f:
            transformer_func = pickle.load(f)

        with open(self.path + '/model/vectors.p', 'rb') as f:
            vectors = pickle.load(f)

        with open(self.path + '/model/keys.p', 'rb') as f:
            commands = pickle.load(f)

        return transformer_func, vectors, commands

    def search(self, query, size=1):
        vector = self.transformer_func.transform([query])
        dist = cosine_similarity(self.vectors, vector).reshape(-1)

        return [(self.commands[i], dist[i]) for i in np.argsort(dist)[-size:]]
