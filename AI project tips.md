1. Detecting reflecting states
-	Similar to repeated states


2. using end game search for all position involving 8 or fewer pieces on the board


3. implementing Minimax with good evaluation function

- This intuition leads to the "Minimax algorithm", so-called because we choose the action which minimizes our maximum possible "loss" from making a particular move. Specifically, for each move we could make we look ahead as many steps as our computing power will allow and examine all the possible moves our opponent could make in each of their future turns, given that we've made our original move. We then take the maximum "loss" (equivalently, the minimum of our evaluation function) that our opponent could induce for us via their moves, and we choose the move we could make which minimizes this maximum.

- Alpha-beta pruning, wherein any move for which another move has already been discovered that is guaranteed to do better than it is eliminated


4. how to be able to search deeper than 5 steps in a short time



1 .find a very good evaluation function
2. run neural network and save result
3. run result in competition

look at visualgo

run ML with pandas
plot graphs with matplob to see results




run recursive monte carlo


search () {
	search() {
		#this will store all the boards (memory expensive)

		#instead just store the steps taken to get there and use that in the recursive search
	}
}