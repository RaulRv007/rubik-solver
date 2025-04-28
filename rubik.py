w = [
    ['w', 'w'],
    ['w', 'w']
]
y = [
    ['y', 'y'],
    ['y', 'y']
]
o = [
    ['o', 'o'],
    ['o', 'o']
]
g = [
    ['g', 'g'],
    ['g', 'g']
]
b = [
    ['b', 'b'],
    ['b', 'b']
]
r = [
    ['r', 'r'],
    ['r', 'r']
]
faces_idx = {'w':0, 'y':1, 'o':2, 'g':3, 'b':4, 'r':5}
goal_state = [w, y, o, g, b, r]

class Node():
    def __init__(self, state, parent=None, action=None, depth=0, path_cost=0, heuristic=0):
        self.state = None
        self.parent = None
        self.action = None
        self.depth = 0
        self.path_cost = 0
        self.heuristic = 0
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class RubikCube():
    #green is front and white is up
    def __init__(self, state, goal_state):
        self.state = state
        self.goal_state = goal_state
        self.visited = set()
        self.frontier = []
        self.solution = None
    def setFrontier(self, node):
        self.frontier.append(node)

    def neighbors(self, state):
        state = self.state
        neighbors = []
        candidates = [
            ('R', self.R(state)),
            ('L', self.L(state)),
            ('D', self.D(state)),
            ('F', self.F(state)),
            ('B', self.B(state))
        ]
        result = []
        for action, (name, movement) in candidates:
            result.append((action, (name, movement)))

        return result

    def R(self, state):
        new_state = [[[None for _ in range(2)] for _ in range(2)] for _ in range(6)]
        #red
        new_state[faces_idx['r']][0][0] = state[faces_idx['r']][1][0]
        new_state[faces_idx['r']][0][1] = state[faces_idx['r']][0][0]
        new_state[faces_idx['r']][1][0] = state[faces_idx['r']][1][1]
        new_state[faces_idx['r']][1][1] = state[faces_idx['r']][0][1]
        #orange
        new_state[faces_idx['o']][0][0] = state[faces_idx['o']][0][0]
        new_state[faces_idx['o']][0][1] = state[faces_idx['o']][0][1]
        new_state[faces_idx['o']][1][0] = state[faces_idx['o']][1][0]
        new_state[faces_idx['o']][1][1] = state[faces_idx['o']][1][1]
        #green
        new_state[faces_idx['g']][0][1] = state[faces_idx['y']][0][1]
        new_state[faces_idx['g']][1][1] = state[faces_idx['y']][1][1]
        new_state[faces_idx['g']][0][0] = state[faces_idx['g']][0][0]
        new_state[faces_idx['g']][1][0] = state[faces_idx['g']][1][0]
        #white
        new_state[faces_idx['w']][0][1] = state[faces_idx['g']][0][1]
        new_state[faces_idx['w']][1][1] = state[faces_idx['g']][1][1]
        new_state[faces_idx['w']][0][0] = state[faces_idx['w']][0][0]
        new_state[faces_idx['w']][1][0] = state[faces_idx['w']][1][0]
        #blue
        new_state[faces_idx['b']][0][1] = state[faces_idx['b']][0][1]
        new_state[faces_idx['b']][1][1] = state[faces_idx['b']][1][1]
        new_state[faces_idx['b']][0][0] = state[faces_idx['w']][0][0]
        new_state[faces_idx['b']][1][0] = state[faces_idx['w']][1][0]
        #yellow
        new_state[faces_idx['y']][0][1] = state[faces_idx['b']][0][1]
        new_state[faces_idx['y']][1][1] = state[faces_idx['b']][1][1]
        new_state[faces_idx['y']][0][0] = state[faces_idx['y']][0][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['y']][1][0]
        return new_state
    def L(self, state):
        new_state = [[[None for _ in range(2)] for _ in range(2)] for _ in range(6)]
        #red
        new_state[faces_idx['r']][0][0] = state[faces_idx['r']][0][0]
        new_state[faces_idx['r']][0][1] = state[faces_idx['r']][0][1]
        new_state[faces_idx['r']][1][0] = state[faces_idx['r']][1][0]
        new_state[faces_idx['r']][1][1] = state[faces_idx['r']][1][1]
        #orange
        new_state[faces_idx['o']][0][0] = state[faces_idx['o']][0][1]
        new_state[faces_idx['o']][0][1] = state[faces_idx['o']][1][1]
        new_state[faces_idx['o']][1][0] = state[faces_idx['o']][0][0]
        new_state[faces_idx['o']][1][1] = state[faces_idx['o']][1][0]
        #green
        new_state[faces_idx['g']][0][1] = state[faces_idx['g']][0][1]
        new_state[faces_idx['g']][1][1] = state[faces_idx['g']][1][1]
        new_state[faces_idx['g']][0][0] = state[faces_idx['w']][0][0]
        new_state[faces_idx['g']][1][0] = state[faces_idx['w']][1][0]
        #white
        new_state[faces_idx['w']][0][1] = state[faces_idx['w']][0][1]
        new_state[faces_idx['w']][1][1] = state[faces_idx['w']][1][1]
        new_state[faces_idx['w']][0][0] = state[faces_idx['b']][1][1]
        new_state[faces_idx['w']][1][0] = state[faces_idx['b']][0][1]
        #blue
        new_state[faces_idx['b']][0][1] = state[faces_idx['y']][0][1]
        new_state[faces_idx['b']][1][1] = state[faces_idx['y']][1][1]
        new_state[faces_idx['b']][0][0] = state[faces_idx['b']][0][0]
        new_state[faces_idx['b']][1][0] = state[faces_idx['b']][1][0]
        #yellow
        new_state[faces_idx['y']][0][1] = state[faces_idx['y']][0][1]
        new_state[faces_idx['y']][1][1] = state[faces_idx['y']][1][1]
        new_state[faces_idx['y']][0][0] = state[faces_idx['g']][0][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['g']][1][0]
        return new_state
    def F(self, state):
        new_state = state
        new_state[3][0][0] = state[3][0][1]
        new_state[3][0][1] = state[3][1][1]
        new_state[3][1][1] = state[3][1][0]
        new_state[3][1][0] = state[3][0][0]
        return new_state
    def B(self, state):
        new_state = state
        new_state[4][0][0] = state[4][0][1]
        new_state[4][0][1] = state[4][1][1]
        new_state[4][1][1] = state[4][1][0]
        new_state[4][1][0] = state[4][0][0]
        return new_state
    def D(self, state):
        new_state = state
        new_state[1][0][0] = state[1][0][1]
        new_state[1][0][1] = state[1][1][1]
        new_state[1][1][1] = state[1][1][0]
        new_state[1][1][0] = state[1][0][0]
        return new_state
    

rubik = RubikCube(goal_state, goal_state)
print(goal_state[3][0][1])
for line in rubik.R(goal_state):
    for row in line:
        print(row)