class stateNode(object):
    def __init__(self,state=None,listActions=[],cost=0):
        self.state=state
        self.listActions=listActions
        self.cost=cost
    def __eq__(self, other):
        if other == None: return False
        return (self.state == other.state)&(self.listActions==other.listActions)