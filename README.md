# 2048
2048 is played on a 4x4 grid with numbered tiles which can slide up, down, left, or right. This game can be
modeled as a two player game, in which the computer AI generates a 2- or 4-tile placed randomly on the board,
and the player then selects a direction to move the tiles. Note that the tiles move until they either (1) collide with
another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide in a move, they merge
into a single tile valued at the sum of the two originals. The resulting tile cannot merge with another tile again in
the same move.

With expectiminimax, the game playing strategy assumes the Computer AI chooses a tile to place in a way
that minimizes the Player's outcome. As a general principle, how far the opponent's behavior deviates from the player's assumption certainly affects how well the AI performs.

- Note that 90% of tiles placed by the computer are 2's, while the remaining 10% are 4's.
- Alpha-Beta pruning speed up the search process by eliminating irrelevant branches.

The following heuristics are considered for evaluating the utility of a given state:
- the absolute value of tiles (mean, median, no. of empty tiles)
- the difference in value between adjacent tiles (monotonicity)
- the potential for merging of similar tiles (smoothness)
- the ordering of tiles across rows, columns, and diagonals (weights across rows and diagonals)

To run the game, execute the game manager:

---

$ python3 GameManager.py

