class Rect:
    def __init__(self, x, z, width, height, bBox = None, ent = None):
        self.x = x
        self.z = z
        self.height = height
        self.width = width
        self.bBox = bBox
        self.ent = ent
    def __str__(self):
        return "x = %.3f z = %.3f height = %.3f width = %.3f" %(self.x,self.z,self.height,self.width)

class QuadTree:
    """
    Nodes
    II(1)  | I(0)
    ---------------
    III(2) | IV(3)
    """
    MAX_OBJECTS = 5
    MAX_LEVELS = 5

    def __init__(self, pLevel, rect):
        self.init()
        self.level = pLevel
        self.bounds = rect

    def init(self):
        self.level = 0
        self.objects = []
        self.bounds = None
        self.nodes = [None,None,None,None]

    def clear(self):
        self.objects = []
        for i in range(4):
            self.nodes.append(None)

    def split(self):
        """split the node into 4 subnodes (quadrants)"""
        subWidth = self.bounds.width / 2
        subHeight = self.bounds.height / 2
        x = self.bounds.x
        z = self.bounds.z
         
        self.nodes[0] = QuadTree(self.level+1, Rect(x + subWidth, z, subWidth, subHeight))
        self.nodes[1] = QuadTree(self.level+1, Rect(x, z, subWidth, subHeight))
        self.nodes[2] = QuadTree(self.level+1, Rect(x, z + subHeight, subWidth, subHeight))
        self.nodes[3] = QuadTree(self.level+1, Rect(x + subWidth, z + subHeight, subWidth, subHeight))

    def getIndex(self,pRect):
        index = -1
        verticalMidpoint = self.bounds.x + self.bounds.width / 2
        horizontalMidpoint = self.bounds.z + self.bounds.height / 2
        
        #print verticalMidpoint
        #print horizontalMidpoint

        topQuadrant = (pRect.z < horizontalMidpoint and pRect.z + pRect.height <= horizontalMidpoint)
        bottomQuadrant = (pRect.z >= horizontalMidpoint)
        
        if (pRect.x < verticalMidpoint and pRect.x + pRect.width < verticalMidpoint):
            if (topQuadrant):
                index = 1
            elif (bottomQuadrant):
               index = 2
        elif (pRect.x > verticalMidpoint):
            if (topQuadrant):
              index = 0
            elif (bottomQuadrant):
              index = 3
        
        #print index, pRect.x
        return index

    def insert(self, pRect):
        if self.nodes[0] != None:
            index = self.getIndex(pRect)
            if index != -1:
                self.nodes[index].insert(pRect)

        self.objects.append(pRect) # else: self.objects.append(pRect)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if self.nodes[0] == None:
                self.split()

            loop = True
            while loop and len(self.objects):
                index = self.getIndex(self.objects[0])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(0))
                else:
                    loop = False
                

    def retrieve(self, resList, pRect):
        index = self.getIndex(pRect)
        #print "INDEX = " + str(index)
        if index != -1 and self.nodes[0] != None:
            self.nodes[index].retrieve(resList, pRect)
        #print "LENGTH = " + str(len(self.objects))   
        resList.extend(self.objects)
        return resList

if __name__ == "__main__":
    rect = Rect(-5000,-5000,10000,10000)
    quad = QuadTree(0, rect)
    quad.insert(Rect(-4800,-4000,100,100))
    quad.insert(Rect(-4500,-3900,100,100))
    quad.insert(Rect(-4500,-3000,100,100))
    quad.insert(Rect(-4500,-2000,100,100))
    quad.insert(Rect(-3500,-2000,100,100))
    quad.insert(Rect(-3200,-1700,100,100))
    quad.insert(Rect(-3000,-1500,100,100))
    quad.insert(Rect(-500,-900,100,100))
    quad.insert(Rect(-500,-300,100,100))
    quad.insert(Rect(-500,0,100,100))
    quad.insert(Rect(-200,0,100,100))
    quad.insert(Rect(200,10,100,100))
    quad.insert(Rect(300,20,100,100))

    for i in range(4):
        print "Quad " + str(i)
        for j in range(len(quad.nodes[i].objects)):
            print quad.nodes[i].objects[j].x

    print "TEST STARTS ===="
    returnObjs = quad.retrieve([], Rect(100,200,100,100))
    for i in range(len(returnObjs)):
        print returnObjs[i].x


