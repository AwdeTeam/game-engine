import json

class Entity:
    def __init__(self, type="Generic", *args, **kwargs):
        self.type = type
        self.entities = args
        self.properties = kwargs
    
    def save(self):
        s = "{"
        for property in self.properties:
            s += property + ":" + self.properties[property] + ","
        
        s += "subentities:["
        for entity in self.entities[:-1]:
            s += entity.save() + ","
        
        if(self.entities):
            s += self.entities[-1].save()
        s += "]}"
        return s
    
    def load(self, s):
        data = json.loads(s)
        for property in data:
            if(property != "subentities"):
                self.properties[property] = data[property]
        
        for entityStr in data["subentities"]:
            entity = Entity()
            entity.load(entityStr)
            self.entities.append(entity)
    
    def render(self, event, graphics):
        print("no-op")

class GridCell:
    def __init__(self, *args, **kwargs):
        self.entities = args
        self.properties = kwargs
    
    def __repr__(self):
        return self.save()
    
    def save(self):
        s = "{"
        for property in self.properties:
            s += property + ":" + self.properties[property] + ","
        
        s += "entities:["
        for entity in self.entities[:-1]:
            s += entity.save() + ","
        
        if(self.entities):
            s += self.entities[-1].save()
        s += "]}"
        return s
    
    def load(self, s):
        data = json.loads(s)
        for property in data:
            if(property != "entities"):
                self.properties[property] = data[property]
        
        for entityStr in data["entities"]:
            entity = Entity()
            entity.load(entityStr)
            self.entities.append(entity)

class Grid:
    def __init__(self, width, height, generator=None):
        self.width = width
        self.height = height
        self.cells = [ None ] * ( width * height )
        if(generator):
            self.cells = [ generator(i%width, int(i/width)) for i in range(width * height) ]
    
    def __getitem__(self, item):
        if(type(item) != type(0) and type(item) != type(slice(0,0))):
            raise TypeError("Grid only supports integer indicies or slices, not {}".format(type(item)))

        if(type(item) == type(0)):
            if(abs(item) >= self.height):
                raise IndexError("Index Out of Bounds: tried to get row {}, but the height is {}".format(item, self.height))
            return self.cells[item*self.width:(item+1)*self.width]
        else:
            print(item)
            return self.cells[item.start*self.width:(item.stop+1)*self.width]

    def __setitem__(self, item, value):
        if(type(item) != type(0) or type(item) ):
            raise TypeError("Grid only supports integer indicies, not {}".format(type(item)))
        if(abs(item) >= self.height):
            raise IndexError("Index Out of Bounds: tried to get row {}, but the height is {}".format(item, self.height))
        
        self.cells[item*self.width:(item+1)*self.width] = value
    
    def __repr__(self):
        s = ""
        for row in self:
            for cell in row:
                s += str(cell) + "\t"
            s += "\n"
        return s
    
    def subgrid(self, x, y, width, height):
        subg = Grid(width, height)
        for i in range(height):
            subg[i] = self[y+i][x:x+width]
        return subg
    
    def save(self):
        s = "{width:" + str(self.width) + ",height:" + str(self.height) + "cells:["
        for row in self[:-1]:
            for cell in row:
                s += cell.save() + ","
        
        for cell in self[-1][:-1]:
            s += cell.save() + ","
        
        s += self[-1][-1] + "]}"
        return s
    
    def load(self, s):
        data = json.loads(s)
        for i, cellStr in enumerate(data["cells"]):
            cell = GridCell()
            cell.load(cellStr)
            self[i%self.width][int(i/self.height)] = cell
    
    
def TEST_GEN(x, y):
    return GridCell(xpos=str(x),ypos=str(y))
