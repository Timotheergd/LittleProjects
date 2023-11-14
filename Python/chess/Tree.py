class Tree():
    
    def __init__(self, mother, move, children=[], points = 0):
        self.mother = mother
        self.children = children
        self.move = move
        self.points = points
        
    def __repr__(self):
        return "move=" + str(self.move)

    def print(self, move="", space=0):
        print("\n" + "   "*space + "|__" + str(self.move) + ", " + str(self.points))
        if len(self.children) == 0:
            return "\n   "*space + str(self.move[1])
        for i in range(len(self.children)):
            self.children[i].print(str(self.move), space+1)

    def copy(self):
        m=[]
        for i in range(len(self.move)):
            m+=self.move[i]
        c=[]
        for i in range(len(self.children)):
            c+=[self.children[i]]
        return Tree(self.mother, m, c, self.points)

    def add_child(self, move_, points_):
        self.children.append(Tree(mother=self, move=move_, points=points_))
        self.children[-1].children=[]

    def max(self, n=0):# mettre n à 1 au depart pour avoir min
        
        if len(self.children) == 0:
            return self#.points
        if n%2==0:
            max = Tree(None, 0, points=-10000)
            for i in range(len(self.children)):
                child_max = self.children[i].max(n+1)
                if child_max.points > max.points:
                    max = child_max
        else:
            max = Tree(None, 0, points=10000)
            for i in range(len(self.children)):
                child_max = self.children[i].max(n+1)
                if child_max.points < max.points:
                    max = child_max
        return max

    def read_tree_up(self, n):
        if n == 0 or self.mother==None:
            return self
        else:
            return self.mother.read_tree_up(n-1)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.mother == other.mother and self.move == other.move
        else:
            return False

    def __ne__(self, other):
        return self.__eq__(other) 