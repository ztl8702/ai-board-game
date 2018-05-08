from typing import Type, Union, List, Tuple

class IBoard(object):
    """
    Public interface of the Board class.
    """

    @classmethod
    def from_token_string(cls, ts: str) -> 'IBoard':
        """
        Creates an instance of the board using a string
        """
        raise NotImplementedError()

    def get(self, x:int, y:int)->str:
        """
        Gets the piece at coordinate `(x, y)`
        """
        raise NotImplementedError()
    
    def set_p(self, x:int, y:int, value:str)-> str:
        """
        Change the piece at coordinate `(x, y)`
        """
        raise NotImplementedError()

    def shrink(self)->'IBoard':
        """
            Shrinks the board. (boardSize -= 2)
            Returns a new Board instance.
        """
        raise NotImplementedError()


    def is_empty(self, x, y)->bool:
        raise NotImplementedError()
    
    def is_within_board(self, x, y)->bool:
        raise NotImplementedError()
    
    def get_empty_cells(self)->List[Tuple[int,int]]:
        raise NotImplementedError()
    
    def get_available_moves(self, x, y)->List[Union[Tuple[int],Tuple[Tuple[int,int],Tuple[int,int]]]]:
        raise NotImplementedError()