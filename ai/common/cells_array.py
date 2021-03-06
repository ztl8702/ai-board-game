import copy
import array


class CellsArray:
    '''
    a 2d array representing all the cells
    '''

    def __init__(self, size):
        '''
        initialise a 2d array
        '''
        self.size = size
        self.cells = [array.array('B', [ord(' ')]*size)
                      for x in range(0, size)]

    def get(self, x, y):
        '''
        get piece type
        '''
        return self.cells[x][y]

    def set_p(self, x, y, value):
        '''
        change cell type
        '''
        self.cells[x][y] = value

    def get_inverted(self):
        '''
        utility function to invert the cells array 
        '''
        new_cells_array = copy.deepcopy(self)
        for x in range(0, self.size):
            for y in range(0, self.size):
                new_cells_array.set_p(x, y, self.get(y, x))
        return new_cells_array
