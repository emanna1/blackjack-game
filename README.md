# Blackjack Game

This is a single player version of a Blackjack game, originally based on a project from the online course: 
Learn Python Programming Masterclass by Tim Buchalka - Udemy. 
Link: https://www.udemy.com/course/python-the-complete-python-developer-course/?couponCode=KEEPLEARNING

The game features a graphical user interface built with Tkinter and includes additional functionalities such as a betting system, move suggestions, and game statistics.

## Features

- Graphical user interface using Tkinter
- Basic strategy move suggestions
- Betting system with balance tracking
- Game statistics (games played, won, and win rate)
- Double down option
- Card images for visual representation

## Requirements

- Python 3
- Tkinter (usually comes pre-installed with Python)
- NumPy

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required packages: pip install numpy
3. Clone this repository or download the source code.

## How to Run

Navigate to the project directory and run: python blackjackGame.py

## Game Rules

Blackjack is a card game where the goal is to beat the dealer by getting a hand value as close to 21 as possible, without going over. 

- Face cards (Jack, Queen, King) are worth 10 points.
- Aces are worth 1 or 11 points, whichever is more advantageous.
- All other cards are worth their face value.

The player can choose to 'Hit' (take another card) or 'Stand' (keep current hand). If the player's hand exceeds 21 points, they 'bust' and lose the round.

## Implementation Details

- The game is a basic single-player implementation of the Blackjack game. 
- It also uses a basic strategy algorithm to suggest optimal moves to the player during the game.
- Card images are stored in the `cards` folder and are dynamically loaded during gameplay.
- The betting system allows players to place bets before each round.
- Game statistics track the number of games played, won, and the overall win rate.

## Enhancements

The following features were added to the original course project:

1. **Betting System**: Players can now place bets before each round, adding a more realistic casino experience.
2. **Move Suggestions**: The game provides suggestions for the optimal move based on basic Blackjack strategy.
3. **Game Statistics**: Players can view their performance statistics, including games played, won, and win rate.

## Future Improvements

- Improve GUI 
- Create a more advanced strategy algorithm
- Include more advanced betting options (e.g., insurance, split)

## Credits

- Base game structure from [Learn Python Programming Masterclass by Tim Buchalka: https://www.udemy.com/course/python-the-complete-python-developer-course/?couponCode=KEEPLEARNING]
- Enhanced by [Emilie Quillet]

## License

This project is open source and available under the [MIT License](LICENSE).