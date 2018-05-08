import copy
class CellsArray:
    '''
    a 2d array representing all the cells
    '''

    def __init__(self, size):
        '''
        initialise a 2d array
        '''
        self.size = size
        self.cells = [
            [0 for x in range(0, size)]
            for y in range(0, size)
        ]

    def get(self, x, y):
        '''
        get piece type
        '''
        return self.cells[x][y]

    def set(self, x, y, value):
        '''
        change cell type 
        '''
        self.cells[x][y] = value

    def getInverted(self):
        '''
        utility function to invert the cells array 
        '''
        newCellsArray = copy.deepcopy(self)
        for x in range(0, self.size):
            for y in range(0, self.size):
                newCellsArray.set(x, y, self.get(y, x))
        return newCellsArray
