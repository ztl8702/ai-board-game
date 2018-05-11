"""
Monte Carlo Tree Search Algorithm


Implementation is inspired by:
    https://medium.com/swlh/tic-tac-toe-at-the-monte-carlo-a5e0394c7bc2
"""

from ...common.game_state_helpers import get_successor_board_states, get_opponent_colour, fake_status
from ...common import Board, BoardStatus, config
from .tree_node import TreeNode
from typing import Type, Union, Tuple
from functools import reduce
import random
import datetime


INFINITY = float('inf')

# for storing the states we have visited before
visited = set()
treenodes = {}


def _new_tree_node(board, currentTurn, side):
    """
    Create a new search tree node.

    If a node with the same state already exists, just return it.
    """
    global visited
    nodeKey = (board.getHashValue(), currentTurn)
    if (nodeKey not in visited):
        visited.add(nodeKey)
        treenodes[nodeKey] = TreeNode(board, currentTurn, side)
    return treenodes[nodeKey]


def _get_children_nodes(node: TreeNode):
    """
    Get Children nodes based on the current game state.
    """
    possibleStates = get_successor_board_states(
        node.board, node.currentTurn+1, get_opponent_colour(node.side))
    possibleNodes = [_new_tree_node(state[1],
                                    node.currentTurn+1,
                                    get_opponent_colour(node.side)) for state in possibleStates]
    # Return value is in the form of [(action, node)]
    return [(possibleStates[i][0], possibleNodes[i]) for i in range(len(possibleStates))]


def _select_child_node_with_best_UCB(children, total)->TreeNode:
    maxValue = -INFINITY
    maxNode = None
    for child in children:
        ucb = child.ucb_upperbound(total)
        if (ucb > maxValue):
            maxValue = ucb
            maxNode = child
    return maxNode


def select(node: TreeNode)->TreeNode:
    """
    The Select Phase of MCTS
    """
    t = node
    # Keep track of the node on the path
    # So that we can back-prop later
    trace = [t]

    while (True):  # while all children has stats
        children = list(map(lambda ca: ca[1], _get_children_nodes(t)))
        visited_c = list(map(lambda c: c.visited > 0, children))
        total = sum(map(lambda c: c.visited, children))
        if (not all(visited_c)):
            break
        else:
            t = _select_child_node_with_best_UCB(children, total)
            trace.append(t)
    return t, trace


def random_playout(node: TreeNode)->BoardStatus:
    """
    The Simulation Phase of MCTS
    """
    max_depth = 20

    tempNode = TreeNode(
        board=node.board,
        currentTurn=node.currentTurn-1,
        side=node.side)

    # This node is not worth simulation,
    # and should not be selected at all!
    if (tempNode.board.get_status(is_placing=tempNode.currentTurn <= 24) \
        == get_opponent_colour(tempNode.side)):
        node.parent.winning = -INFINITY
        print("opponent won, bad state")
        return get_opponent_colour(tempNode.side)

    depth = 0
    while (tempNode.board.get_status(is_placing=tempNode.currentTurn <= 24) \
        == BoardStatus.ON_GOING):
        if (depth >= max_depth):
            fs = fake_status(tempNode.board)
            return fs
        tempNode.random_play()
        depth += 1

    return tempNode.board.get_status()


def back_prop(nodesInPath, playoutResult):
    """
    The Back-propagation Phase of MCTS
    """
    for tempNode in nodesInPath:
        tempNode.visited += 1
        if str(playoutResult) == str(tempNode.side):
            tempNode.winning += 1


def _get_child_with_max_score(rootNode: TreeNode)->'TreeNode':
    maxValue = -INFINITY
    maxNode = None
    maxAction = None
    for action, node in _get_children_nodes(rootNode):
        print(f"{action}({node.score()}) ", end=" ")
        if (node.score() > maxValue):
            maxValue = node.score()
            maxNode = node
            maxAction = action
    print("")
    return maxAction, maxNode


def find_next_move(board: Type[Board], turn: int, colour) -> Union[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Main function of Monte Carlo search
    """
    # for this version, restart search for each turn
    # not sure if we can persist the tree
    rootNode = _new_tree_node(board, turn-1, get_opponent_colour(colour))
    print("rootNode already has ", rootNode.winning, '/', rootNode.visited) # DEBUG
    
    startTime = datetime.datetime.now()
    elapsed = datetime.timedelta(0)
    simulationRounds = 0
    while (elapsed <= config.MC_TIME_LIMIT):
        promisingNode, path = select(rootNode)
        nodeToExplore = promisingNode

        if promisingNode.board.get_status(is_placing=promisingNode.currentTurn <= 24) \
            == BoardStatus.ON_GOING:
            childrenNodes = _get_children_nodes(nodeToExplore)
            if (len(childrenNodes) > 0):
                action, nodeToExplore = random.choice(childrenNodes)
                path.append(nodeToExplore)

        playoutResult = random_playout(nodeToExplore)

        back_prop(path, playoutResult)

        elapsed = datetime.datetime.now() - startTime
        simulationRounds += 1

    print(f"\n\n\n[MC] {simulationRounds} rounds of simulation run.\n\n\n")
    winningAction, winningNode = _get_child_with_max_score(rootNode)
    return winningAction
