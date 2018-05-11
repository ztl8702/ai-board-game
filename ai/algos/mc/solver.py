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


def _new_tree_node(board, current_turn, side):
    """
    Create a new search tree node.

    If a node with the same state already exists, just return it.
    """
    global visited
    node_key = (board.get_hash_value(), current_turn)
    if (node_key not in visited):
        visited.add(node_key)
        treenodes[node_key] = TreeNode(board, current_turn, side)
    return treenodes[node_key]


def _get_children_nodes(node: TreeNode):
    """
    Get Children nodes based on the current game state.
    """
    possible_states = get_successor_board_states(
        node.board, node.current_turn+1, get_opponent_colour(node.side))
    possibleNodes = [_new_tree_node(state[1],
                                    node.current_turn+1,
                                    get_opponent_colour(node.side)) for state in possible_states]
    # Return value is in the form of [(action, node)]
    return [(possible_states[i][0], possibleNodes[i]) for i in range(len(possible_states))]


def _select_child_node_with_best_UCB(children, total)->TreeNode:
    max_value = -INFINITY
    max_node = None
    for child in children:
        ucb = child.ucb_upperbound(total)
        if (ucb > max_value):
            max_value = ucb
            max_node = child
    return max_node


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

    temp_node = TreeNode(
        board=node.board,
        current_turn=node.current_turn-1,
        side=node.side)

    # This node is not worth simulation,
    # and should not be selected at all!
    if (temp_node.board.get_status(is_placing=temp_node.current_turn <= 24) \
        == get_opponent_colour(temp_node.side)):
        node.parent.winning = -INFINITY
        print("opponent won, bad state")
        return get_opponent_colour(temp_node.side)

    depth = 0
    while (temp_node.board.get_status(is_placing=temp_node.current_turn <= 24) \
        == BoardStatus.ON_GOING):
        if (depth >= max_depth):
            fs = fake_status(temp_node.board)
            return fs
        temp_node.random_play()
        depth += 1

    return temp_node.board.get_status()


def back_prop(nodes_in_path, playout_result):
    """
    The Back-propagation Phase of MCTS
    """
    for temp_node in nodes_in_path:
        temp_node.visited += 1
        if str(playout_result) == str(temp_node.side):
            temp_node.winning += 1


def _get_child_with_max_score(root_node: TreeNode)->'TreeNode':
    max_value = -INFINITY
    max_node = None
    max_action = None
    for action, node in _get_children_nodes(root_node):
        print(f"{action}({node.score()}) ", end=" ")
        if (node.score() > max_value):
            max_value = node.score()
            max_node = node
            max_action = action
    print("")
    return max_action, max_node


def find_next_move(board: Type[Board], turn: int, colour) -> Union[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Main function of Monte Carlo search
    """
    # for this version, restart search for each turn
    # not sure if we can persist the tree
    root_node = _new_tree_node(board, turn-1, get_opponent_colour(colour))
    print("root_node already has ", root_node.winning, '/', root_node.visited) # DEBUG
    
    start_time = datetime.datetime.now()
    elapsed = datetime.timedelta(0)
    simulation_rounds = 0
    while (elapsed <= config.MC_TIME_LIMIT):
        promising_node, path = select(root_node)
        node_to_explore = promising_node

        if promising_node.board.get_status(is_placing=promising_node.current_turn <= 24) \
            == BoardStatus.ON_GOING:
            children_nodes = _get_children_nodes(node_to_explore)
            if (len(children_nodes) > 0):
                action, node_to_explore = random.choice(children_nodes)
                path.append(node_to_explore)

        playout_result = random_playout(node_to_explore)

        back_prop(path, playout_result)

        elapsed = datetime.datetime.now() - start_time
        simulation_rounds += 1

    print(f"\n\n\n[MC] {simulation_rounds} rounds of simulation run.\n\n\n")
    winning_action, winning_node = _get_child_with_max_score(root_node)
    return winning_action
