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
w_ini = [
    ['w', 'g'],
    ['w', 'g']
]
y_ini = [
    ['b', 'y'],
    ['b', 'y']
]
o_ini = [
    ['o', 'o'],
    ['o', 'o']
]
g_ini = [
    ['g', 'y'],
    ['g', 'y']
]
b_ini = [
    ['w', 'b'],
    ['w', 'b']
]
r_ini = [
    ['r', 'r'],
    ['r', 'r']
]
faces_idx = {'w':0, 'y':3, 'o':4, 'g':2, 'b':5, 'r':1}
goal_state = [w, r, g, y, o, b]
initial_state = [w_ini, r_ini, g_ini, y_ini, o_ini, b_ini]


class Node():
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.start = state

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
        self.visited = []
        self.frontier = []
        self.solution = None

    def setFrontier(self, node):
        self.frontier.append(node)

    def neighbors(self, state):
        candidates = [
            ('R', self.R(state)),
            ('L', self.L(state)),
            ('D', self.D(state)),
            ('F', self.F(state)),
            ('B', self.B(state))
        ]
        result = []
        for action, state in candidates:
            result.append((action, state))

        
        return result
    
    def solve(self):
        self.num_explored = 0

        start = Node(state=self.state, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        while True:
            '''if frontier.empty():
                raise Exception('no Solution')'''
        
            node = frontier.remove()
            if node.state == self.goal_state:
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node  = node.parent

                actions.reverse()
                states.reverse()
                self.solution = (actions, states)
                return
            
            self.visited.append(node.state)
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.visited:
                    #state = self.R(state)
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


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
        new_state[faces_idx['g']][0][1] = state[faces_idx['y']][1][0]
        new_state[faces_idx['g']][1][1] = state[faces_idx['y']][0][0]
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
        new_state[faces_idx['b']][0][0] = state[faces_idx['w']][1][1]
        new_state[faces_idx['b']][1][0] = state[faces_idx['w']][0][1]
        #yellow
        new_state[faces_idx['y']][0][1] = state[faces_idx['y']][0][1]
        new_state[faces_idx['y']][1][1] = state[faces_idx['y']][1][1]
        new_state[faces_idx['y']][0][0] = state[faces_idx['b']][0][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['b']][1][0]
        return new_state
    def L(self, state):
        new_state = [[[None for _ in range(2)] for _ in range(2)] for _ in range(6)]
        #red
        new_state[faces_idx['r']][0][0] = state[faces_idx['r']][0][0]
        new_state[faces_idx['r']][0][1] = state[faces_idx['r']][0][1]
        new_state[faces_idx['r']][1][0] = state[faces_idx['r']][1][0]
        new_state[faces_idx['r']][1][1] = state[faces_idx['r']][1][1]
        #orange
        new_state[faces_idx['o']][0][0] = state[faces_idx['o']][1][0]
        new_state[faces_idx['o']][0][1] = state[faces_idx['o']][0][0]
        new_state[faces_idx['o']][1][0] = state[faces_idx['o']][1][1]
        new_state[faces_idx['o']][1][1] = state[faces_idx['o']][0][1]
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
        new_state[faces_idx['y']][0][1] = state[faces_idx['g']][1][0]
        new_state[faces_idx['y']][1][1] = state[faces_idx['g']][0][0]
        new_state[faces_idx['y']][0][0] = state[faces_idx['y']][0][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['y']][1][0]
        return new_state
    def F(self, state):
        new_state = [[[None for _ in range(2)] for _ in range(2)] for _ in range(6)]
        #red
        new_state[faces_idx['r']][0][0] = state[faces_idx['w']][1][0]
        new_state[faces_idx['r']][0][1] = state[faces_idx['r']][0][1]
        new_state[faces_idx['r']][1][0] = state[faces_idx['w']][1][1]
        new_state[faces_idx['r']][1][1] = state[faces_idx['r']][1][1]
        #orange
        new_state[faces_idx['o']][0][0] = state[faces_idx['o']][0][0]
        new_state[faces_idx['o']][0][1] = state[faces_idx['y']][1][1]
        new_state[faces_idx['o']][1][0] = state[faces_idx['o']][1][0]
        new_state[faces_idx['o']][1][1] = state[faces_idx['y']][1][0]
        #green
        new_state[faces_idx['g']][0][1] = state[faces_idx['g']][0][0]
        new_state[faces_idx['g']][1][1] = state[faces_idx['g']][0][1]
        new_state[faces_idx['g']][0][0] = state[faces_idx['g']][1][0]
        new_state[faces_idx['g']][1][0] = state[faces_idx['g']][1][1]
        #white
        new_state[faces_idx['w']][0][1] = state[faces_idx['w']][0][1]
        new_state[faces_idx['w']][1][1] = state[faces_idx['o']][0][1]
        new_state[faces_idx['w']][0][0] = state[faces_idx['w']][0][0]
        new_state[faces_idx['w']][1][0] = state[faces_idx['o']][1][1]
        #blue
        new_state[faces_idx['b']][0][1] = state[faces_idx['b']][0][1]
        new_state[faces_idx['b']][1][1] = state[faces_idx['b']][1][1]
        new_state[faces_idx['b']][0][0] = state[faces_idx['b']][0][0]
        new_state[faces_idx['b']][1][0] = state[faces_idx['b']][1][0]
        #yellow
        new_state[faces_idx['y']][0][1] = state[faces_idx['y']][0][1]
        new_state[faces_idx['y']][1][1] = state[faces_idx['r']][1][0]
        new_state[faces_idx['y']][0][0] = state[faces_idx['y']][0][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['r']][0][0]
        return new_state
    def B(self, state):
        new_state = [[[None for _ in range(2)] for _ in range(2)] for _ in range(6)]
        # red
        new_state[faces_idx['r']][0][0] = state[faces_idx['r']][0][0]
        new_state[faces_idx['r']][0][1] = state[faces_idx['y']][0][0]
        new_state[faces_idx['r']][1][0] = state[faces_idx['r']][1][0]
        new_state[faces_idx['r']][1][1] = state[faces_idx['y']][0][1]
        # orange
        new_state[faces_idx['o']][0][0] = state[faces_idx['w']][0][1]
        new_state[faces_idx['o']][0][1] = state[faces_idx['o']][0][1]
        new_state[faces_idx['o']][1][0] = state[faces_idx['w']][0][0]
        new_state[faces_idx['o']][1][1] = state[faces_idx['o']][1][1]
        # green
        new_state[faces_idx['g']][0][1] = state[faces_idx['g']][0][1]
        new_state[faces_idx['g']][1][1] = state[faces_idx['g']][1][1]
        new_state[faces_idx['g']][0][0] = state[faces_idx['g']][0][0]
        new_state[faces_idx['g']][1][0] = state[faces_idx['g']][1][0]
        # white
        new_state[faces_idx['w']][0][1] = state[faces_idx['r']][1][1]
        new_state[faces_idx['w']][0][0] = state[faces_idx['r']][0][1]
        new_state[faces_idx['w']][1][1] = state[faces_idx['w']][1][1]
        new_state[faces_idx['w']][1][0] = state[faces_idx['w']][1][0]
        # blue
        new_state[faces_idx['b']][0][1] = state[faces_idx['b']][0][0]
        new_state[faces_idx['b']][1][1] = state[faces_idx['b']][0][1]
        new_state[faces_idx['b']][0][0] = state[faces_idx['b']][1][0]
        new_state[faces_idx['b']][1][0] = state[faces_idx['b']][1][1]
        # yellow
        new_state[faces_idx['y']][0][1] = state[faces_idx['o']][0][0]
        new_state[faces_idx['y']][1][1] = state[faces_idx['y']][1][1]
        new_state[faces_idx['y']][0][0] = state[faces_idx['o']][1][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['y']][1][0]
        return new_state
    def D(self, state):
        new_state = [[[None for _ in range(2)] for _ in range(2)] for _ in range(6)]
        #red
        new_state[faces_idx['r']][0][0] = state[faces_idx['r']][0][0]
        new_state[faces_idx['r']][0][1] = state[faces_idx['r']][0][1]
        new_state[faces_idx['r']][1][0] = state[faces_idx['g']][1][0]
        new_state[faces_idx['r']][1][1] = state[faces_idx['g']][1][1]
        #orange
        new_state[faces_idx['o']][0][0] = state[faces_idx['o']][0][0]
        new_state[faces_idx['o']][0][1] = state[faces_idx['o']][0][1]
        new_state[faces_idx['o']][1][0] = state[faces_idx['b']][1][0]
        new_state[faces_idx['o']][1][1] = state[faces_idx['b']][1][1]
        #green
        new_state[faces_idx['g']][0][1] = state[faces_idx['g']][0][1]
        new_state[faces_idx['g']][1][1] = state[faces_idx['o']][1][1]
        new_state[faces_idx['g']][0][0] = state[faces_idx['g']][0][0]
        new_state[faces_idx['g']][1][0] = state[faces_idx['o']][1][0]
        #white
        new_state[faces_idx['w']][0][1] = state[faces_idx['w']][0][1]
        new_state[faces_idx['w']][1][1] = state[faces_idx['w']][1][1]
        new_state[faces_idx['w']][0][0] = state[faces_idx['w']][0][0]
        new_state[faces_idx['w']][1][0] = state[faces_idx['w']][1][0]
        #blue
        new_state[faces_idx['b']][0][1] = state[faces_idx['b']][0][1]
        new_state[faces_idx['b']][1][1] = state[faces_idx['r']][1][1]
        new_state[faces_idx['b']][0][0] = state[faces_idx['b']][0][0]
        new_state[faces_idx['b']][1][0] = state[faces_idx['r']][1][0]
        #yellow
        new_state[faces_idx['y']][0][1] = state[faces_idx['y']][0][0]
        new_state[faces_idx['y']][1][1] = state[faces_idx['y']][0][1]
        new_state[faces_idx['y']][0][0] = state[faces_idx['y']][1][0]
        new_state[faces_idx['y']][1][0] = state[faces_idx['y']][1][1]
        return new_state
    

rubik = RubikCube(initial_state, goal_state)
rubik.solve()
print(rubik.solution[0])