TODO before submitting

1. check if we need to name our main playing agent as "player" explicitly
	- minimax_player -> player  ???
	- ai.agents.playerbase -> player  ???

2. check code for consistency
	- variable name convention
	- function name convention
	- <80 columns per line
	- javadoc where needed

3. note at the top of comments.txt that specify which Player class to test and mark
	- the Player class to be tested and marked can be different
	- refer to https://app.lms.unimelb.edu.au/webapps/discussionboard/do/message?action=list_messages&course_id=_363834_1&nav=discussion_board_entry&conf_id=_728358_1&forum_id=_400913_1&message_id=_1731630_1

4. refactor all the debugging print statements to be controlled by a switch
	- to not confuse referee printing and debugging printing

5. make sure we meet performance constraints
	- 60 seconds / 120 seconds per player
	- 100MB memory per player