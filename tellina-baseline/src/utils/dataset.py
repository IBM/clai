import json


class Nlc2CmdDS(object):

    def __init__(self, annotation_filepath):

        self._annotation_filepath = annotation_filepath
        self.invocations, self.cmds = self.__load_data__(annotation_filepath)
        self.n = len(self.invocations)

    def __load_data__(self, filepath):
        
        with open(filepath, 'r') as f:
            datadict = json.load(f) 
        
        data = [(row['invocation'], row['cmd']) for rowid, row in datadict.items()]
        invocations, cmds = list(zip(*data))
        return invocations, cmds

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        invocation = self.invocations[idx]
        cmd = self.cmds[idx]
        return (invocation, cmd)
