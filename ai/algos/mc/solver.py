from ...common.game_state_helpers import get_successor_board_states, get_opponent_colour
from ...common import Board, BoardStatus, config

from typing import Type, Union, Tuple
from .tree import Tree
from .tree_node import TreeNode

import datetime


# ===================================================
# Monte Carlo
# Implementation is inspired by:
#    https://medium.com/swlh/tic-tac-toe-at-the-monte-carlo-a5e0394c7bc2
# ===================================================

INFINITY = float('inf')


def _selectChildNodeWithBestUCB(node: TreeNode)->TreeNode:
    maxValue = -INFINITY
    maxNode = None
    for child in node.children:
        ucb = child.ucb_upperbound(node.visited)
        if (ucb > maxValue):
            maxValue = ucb
            maxNode = child
    return maxNode


def select(node: TreeNode)->TreeNode:
    t = node
    while (t.has_children()):
        t = _selectChildNodeWithBestUCB(t)
    return t


def expand_node(node: TreeNode):
    possibleState = get_successor_board_states(
        node.board, node.currentTurn+1, get_opponent_colour(node.side))


    for state in possibleState:
        newNode = TreeNode(state[1],
                           node.currentTurn+1,
                           get_opponent_colour(node.side),
                           node)
        newNode.last_action = state[0]
        node.add_child(newNode)


def random_playout(node: TreeNode)->BoardStatus:
    tempNode = TreeNode(
        board=node.board,
        currentTurn=node.currentTurn-1,
        side=node.side,
        parent=node)

    # This node is not worth simulation,
    # and should not be selected at all!
    if (tempNode.board.get_status(is_placing=tempNode.currentTurn<=24) == get_opponent_colour(tempNode.side)):
        tempNode.parent.winning = -INFINITY
        print("opponent won, bad state")
        return get_opponent_colour(tempNode.side)

    while (tempNode.board.get_status(is_placing=tempNode.currentTurn<=24) == BoardStatus.ON_GOING):
        tempNode.random_play()

    return tempNode.board.get_status()


def back_prop(nodeToExplore, playoutResult):
    tempNode = nodeToExplore
    while (tempNode != None):
        tempNode.visited += 1
        if playoutResult == tempNode.side:
            tempNode.winning += 1
        tempNode = tempNode.parent


def find_next_move(board: Type[Board], turn:int, colour) -> Union[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Main function of Monte Carlo search
    """
    # for this version, restart search for each turn
    # not sure if we can persist the tree

    tree = Tree(board, turn-1, get_opponent_colour(colour))

    startTime = datetime.datetime.now()

    elapsed = datetime.timedelta(0)
    simulationRounds = 0
    while (elapsed <= config.MC_TIME_LIMIT): 
        promisingNode = select(tree.root)

        if (promisingNode.board.get_status(is_placing = promisingNode.currentTurn<=24) == BoardStatus.ON_GOING):
            expand_node(promisingNode)

        nodeToExplore = promisingNode

        if (nodeToExplore.has_children()):
            nodeToExplore = promisingNode.get_random_child()

        playoutResult = random_playout(nodeToExplore)

        back_prop(nodeToExplore, playoutResult)
        
        elapsed = datetime.datetime.now() - startTime
        simulationRounds+=1
        #print("tree root children", tree.root.children)

    print(f"\n\n\n[MC] {simulationRounds} rounds of simulation run.\n\n\n")
    winningNode = tree.root.get_child_with_max_score()
    return winningNode.last_action
