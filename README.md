# Year 3 Artificial Intelligence Project

> Simple Board Game played by AI
made by:
`Therrense Lua (github: ttvs`
`Tianlei Zheng (github: ztl8702)`


## Requirements
- python version 3


## Referee Use Case
```
$ python ./referee.py <white_module> <black_module>
eg. $ python ./referee.py minimax_player dummy_player
```


## AI Modules
- minimax_player
	- minimax player with alpha-beta pruning
- mc_player
	- monte carlo player
- dummy_player
	- makes random moves
- mirror_player
	- should always be the black (second) player


## "Bake-off" (playing different modules against each other)

For Example:
```
$ python ./bakeoff.py <result_output_folder> <white_module> <black_module> <number_of_rounds>
$ eg. python ./bakeoff.py test_output dummy_player minimax_player 50
```

Explaination:
Will play DummyPlayer against MiniMaxPlayer for 50 rounds, 
and store the output in `test_output/`.

Each folder corresponds to one outcome (White wins/Black wins/Draw), and contains the output of the playout in which that player has won.

By counting the number of files in each folder, we can tell how well each player is against each other.

The file names also show how many turns it took for one player to kill the other.


## Documentation

```
make html
```


## Unit tests
```
pytest
```
