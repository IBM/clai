import numpy as np
from math import ceil

class Nlc2CmdDL(object):

    def __init__(self, dataset, batchsize, shuffle):

        self.dataset = dataset
        self.batchsize = batchsize
        self.shuffle = shuffle
        self._batchidxs = self.__prepare_idxs__()

    def __prepare_idxs__(self):
        n = len(self.dataset)
        n_batches = ceil(n / float(self.batchsize))
        
        idxs = np.random.permutation(n) if self.shuffle else np.arange(n)
        batchidxs = [
            idxs[i*self.batchsize : min(n, (i+1)*self.batchsize)] 
            for i in range(n_batches)
        ]

        return batchidxs

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        
        if self.i >= len(self._batchidxs):
            raise StopIteration

        idxs = self._batchidxs[self.i]
        self.i += 1

        batchdata = [self.dataset[idx] for idx in idxs]
        batch_invocs, batch_cmds = list(zip(*batchdata))
        return batch_invocs, batch_cmds
