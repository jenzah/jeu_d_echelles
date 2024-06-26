# Snakes and Ladders

Snakes and Ladders is a classic board game where players navigate a grid of numbered squares.
Ladders allow players to advance more quickly, while snakes send them back to earlier positions. The goal is to be the first to reach the final square.


## Game Rules

1. **Setup**:
    - The game board consists of a grid of numbered squares, typically from 1 to 100.
    - There are ladders on the board that move players up to a higher numbered square.
    - There are snakes on the board that move players down to a lower numbered square.

2. **Gameplay**:
    - Each player starts with their token at square 1.
    - The order of the players is decided by an initial die throw.
    - Players take turns rolling a single six-sided die to determine how many squares to move.
    - If a player lands at the base of a ladder, they immediately move up to the top of the ladder.
    - If a player lands on the head of a snake, they immediately slide down to the tail of the snake.
    - If a player gets a 6, they can throw the die again a maximum of 2 more times.
    - The first player to reach or surpass the final square (typically 100) wins the game.

3. **Winning the Game**:
    - The game is won by the first player to reach the highest numbered square on the board.
    - If a player rolls a number that would move them beyond the final square, they move forward, then backwards.


## Installation

**Clone the repository**:
```bash
git clone https://github.com/jenzah/jeu_d_echelles.git
cd jeu-dechelles
```

## Usage

**To start the game, run the following command:**
```bash
python jeu_d_echelles.py
```

**To see the board:** type `map` into the terminal
