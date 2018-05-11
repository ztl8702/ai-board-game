from typing import Type
from .tree_node import TreeNode
from ...common import Board

class Tree(object):
    def __init__(self, rootBoard: Board, rootTurn:int, rootSide):
        self.root = TreeNode(rootBoard, rootTurn, rootSide, None)
