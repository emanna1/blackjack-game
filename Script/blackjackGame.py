import random
import tkinter as tk
from tkinter import messagebox
import numpy as np

class BlackjackGame:
    def __init__(self, master):
        """
        Initialize the Blackjack game.
        
        Args:
            master (tk.Tk): The root window for the game.
        """
        self.master = master
        self.master.title("Enhanced Blackjack")
        self.master.geometry("800x600")
        self.master.configure(background='green')

        self.player_balance = 1000
        self.current_bet = 0
        self.games_played = 0
        self.games_won = 0

        self.card_images = self.load_card_images()
        self.strategy = self.BasicStrategy()

        self.setup_ui()
        self.reset_game()

    class BasicStrategy:
        """Initialize the basic strategy for Blackjack."""
        def __init__(self):
            self.strategy = np.array([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5-8
                [1, 2, 2, 2, 2, 1, 1, 1, 1, 1],  # 9
                [2, 2, 2, 2, 2, 2, 2, 2, 1, 1],  # 10
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 11
                [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],  # 12
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],  # 13
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],  # 14
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],  # 15
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],  # 16
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17+
            ])

        def get_move(self, player_score, dealer_up_card):
            """
            Get the suggested move based on the basic strategy.

            Args:
                player_score (int): The player's current hand score.
                dealer_up_card (int): The dealer's visible card value.

            Returns:
                int: 0 for Stand, 1 for Hit, 2 for Double Down.
            """
            player_score = max(5, min(player_score, 17))  
            dealer_up_card= max(2, min(dealer_up_card, 11))


            player_index = min(player_score - 5, 9) 
            dealer_index = dealer_up_card - 2 

            return self.strategy[player_index][dealer_index]
        
    def suggest_move(self):
        """
        Suggest the next move based on the basic strategy.

        Returns:
            str: A string describing the suggested move.
        """
        player_score = self.calculate_hand(self.player_hand)
        if len(self.dealer_hand) > 0:
            dealer_up_card = self.dealer_hand[0][0]
            if dealer_up_card > 10:  # Face cards
                dealer_up_card = 10
            move = self.strategy.get_move(player_score, dealer_up_card)
            if move == 0:
                return "Stand"
            elif move == 1:
                return "Hit"
            else:
                return "Double Down if allowed, otherwise Hit"
        else:
            return "Unable to suggest a move at this time."

        
    def load_card_images(self):
        """
        Load card images from files.

        Returns:
            list: A list of tuples, each containing a card value and its image.
        """
        suits = ['heart', 'club', 'diamond', 'spade']
        face_cards = ['jack', 'queen', 'king']
        extension = 'ppm'
        
        card_images = []
        for suit in suits:
            for card in range(1, 11):
                name = '{}_{}.{}'.format(str(card), suit, extension)
                image = tk.PhotoImage(file=name)
                card_images.append((card, image,))
            
            for card in face_cards:
                name = '{}_{}.{}'.format(str(card), suit, extension)
                image = tk.PhotoImage(file=name)
                card_images.append((10, image,))
        
        return card_images

    def setup_ui(self):
        """Set up the user interface components for the game."""
        self.result_text = tk.StringVar()
        self.result_label = tk.Label(self.master, textvariable=self.result_text, font=('Arial', 14))
        self.result_label.pack(pady=10)

        self.balance_text = tk.StringVar()
        self.balance_label = tk.Label(self.master, textvariable=self.balance_text, font=('Arial', 12))
        self.balance_label.pack()

        self.bet_frame = tk.Frame(self.master)
        self.bet_frame.pack(pady=10)
        self.bet_entry = tk.Entry(self.bet_frame, width=10)
        self.bet_entry.pack(side=tk.LEFT, padx=5)
        self.bet_button = tk.Button(self.bet_frame, text="Place Bet", command=self.place_bet)
        self.bet_button.pack(side=tk.LEFT)

        self.card_frame = tk.Frame(self.master, bg='green')
        self.card_frame.pack(pady=10)

        self.dealer_frame = tk.Frame(self.card_frame, bg='green')
        self.dealer_frame.pack()
        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer", bg='green', fg='white', font=('Arial', 12))
        self.dealer_label.pack()
        self.dealer_score = tk.StringVar()
        self.dealer_score_label = tk.Label(self.dealer_frame, textvariable=self.dealer_score, bg='green', fg='white', font=('Arial', 12))
        self.dealer_score_label.pack()
        self.dealer_cards = tk.Frame(self.dealer_frame, bg='green')
        self.dealer_cards.pack()

        self.player_frame = tk.Frame(self.card_frame, bg='green')
        self.player_frame.pack()
        self.player_label = tk.Label(self.player_frame, text="Player", bg='green', fg='white', font=('Arial', 12))
        self.player_label.pack()
        self.player_score = tk.StringVar()
        self.player_score_label = tk.Label(self.player_frame, textvariable=self.player_score, bg='green', fg='white', font=('Arial', 12))
        self.player_score_label.pack()
        self.player_cards = tk.Frame(self.player_frame, bg='green')
        self.player_cards.pack()

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)
        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=5)
        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side=tk.LEFT, padx=5)
        self.double_down_button = tk.Button(self.button_frame, text="Double Down", command=self.double_down)
        self.double_down_button.pack(side=tk.LEFT, padx=5)
        self.suggest_button = tk.Button(self.button_frame, text="Suggest Move", command=self.show_suggestion)
        self.suggest_button.pack(side=tk.LEFT, padx=5)

        self.stats_button = tk.Button(self.master, text="Show Stats", command=self.show_stats)
        self.stats_button.pack(pady=10)

    def reset_game(self):
        """Reset the game state for a new round"""
        self.deck = self.create_deck()
        self.dealer_hand = []
        self.player_hand = []
        self.game_over = False
        self.current_bet = 0

        for widget in self.dealer_cards.winfo_children():
            widget.destroy()
        for widget in self.player_cards.winfo_children():
            widget.destroy()

        self.result_text.set("")
        self.update_balance_display()
        self.enable_game_buttons(False)
        self.bet_button.config(state=tk.NORMAL)
        self.bet_entry.config(state=tk.NORMAL)

    def create_deck(self):
        """
        Create and return a new deck of cards.

        Returns:
            list: A list representing a full deck of cards.
        """
        return list(self.card_images)

    def deal_card(self, hand, frame):
        """
        Deal a card from the deck to the given hand and update the UI.

        Args:
            hand (list): The hand to deal the card to.
            frame (tk.Frame): The frame to display the card in.

        Returns:
            tuple: The dealt card.
        """
        card = random.choice(self.deck)
        self.deck.remove(card)
        hand.append(card)
        tk.Label(frame, image=card[1], relief='raised').pack(side='left')
        return card

    def calculate_hand(self, hand):
        """
        Calculate the total value of the given hand.

        Args:
            hand (list): The hand to calculate.

        Returns:
            int: The total value of the hand.
        """
        value = sum(card[0] for card in hand)
        aces = sum(1 for card in hand if card[0] == 1)
        
        while value <= 11 and aces > 0:
            value += 10
            aces -= 1
        
        return value

    def update_scores(self):
        """Update the displayed scores for both player and dealer"""
        dealer_score = self.calculate_hand(self.dealer_hand)
        player_score = self.calculate_hand(self.player_hand)
        self.dealer_score.set(f"Score: {dealer_score}")
        self.player_score.set(f"Score: {player_score}")

    def place_bet(self):
        """Place the player's bet and start the game"""
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.player_balance:
                raise ValueError
            self.current_bet = bet
            self.player_balance -= bet
            self.update_balance_display()
            self.start_game()
        except ValueError:
            messagebox.showerror("Invalid Bet", "Please enter a valid bet amount.")

    def start_game(self):
        """Start a new game by dealing the initial cards"""
        self.deal_card(self.player_hand, self.player_cards)
        self.deal_card(self.dealer_hand, self.dealer_cards)
        self.deal_card(self.player_hand, self.player_cards)
        self.update_scores()
        self.enable_game_buttons(True)
        self.bet_button.config(state=tk.DISABLED)
        self.bet_entry.config(state=tk.DISABLED)

    def hit(self):
        """Deal another card to the player and check for bust"""
        self.deal_card(self.player_hand, self.player_cards)
        self.update_scores()
        if self.calculate_hand(self.player_hand) > 21:
            self.end_game("Player busts! Dealer wins.")

    def stand(self):
        """Player stands, now it's dealer's turn to play"""
        self.play_dealer_hand()

    def double_down(self):
        """Double the player's bet, deal one more card, and stand"""
        if len(self.player_hand) == 2 and self.player_balance >= self.current_bet:
            self.player_balance -= self.current_bet
            self.current_bet *= 2
            self.update_balance_display()
            self.hit()
            if not self.game_over:
                self.stand()

    def play_dealer_hand(self):
        """Play the dealer's hand according to the rules"""
        while self.calculate_hand(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand, self.dealer_cards)
        self.update_scores()
        self.end_game(self.determine_winner())

    def determine_winner(self):
        """
        Determine the winner of the current game.

        Returns:
            str: A message indicating the game result.
        """
        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)
        
        if dealer_score > 21:
            self.player_balance += self.current_bet * 2
            self.games_won += 1
            return "Dealer busts! Player wins!"
        elif player_score > dealer_score:
            self.player_balance += self.current_bet * 2
            self.games_won += 1
            return "Player wins!"
        elif dealer_score > player_score:
            return "Dealer wins!"
        else:
            self.player_balance += self.current_bet
            return "It's a tie!"

    def end_game(self, result):
        """
        End the game and display the result.

        Args:
            result (str): The result of the game.
        """
        self.game_over = True
        self.result_text.set(result)
        self.update_balance_display()
        self.enable_game_buttons(False)
        self.games_played += 1
        self.master.after(2000, self.reset_game)

    def enable_game_buttons(self, enable):
        """
        Enable or disable game buttons based on the game state.

        Args:
            enable (bool): True to enable buttons, False to disable.
        """
        state = tk.NORMAL if enable else tk.DISABLED
        self.hit_button.config(state=state)
        self.stand_button.config(state=state)
        self.double_down_button.config(state=state)
        self.suggest_button.config(state=state)

    def update_balance_display(self):
        """Update the displayed player balance"""
        self.balance_text.set(f"Balance: ${self.player_balance}")

    def show_stats(self):
        """Display game statistics in a message box"""
        win_rate = (self.games_won / self.games_played * 100) if self.games_played > 0 else 0
        stats = f"Games Played: {self.games_played}\n"
        stats += f"Games Won: {self.games_won}\n"
        stats += f"Win Rate: {win_rate:.2f}%"
        messagebox.showinfo("Game Statistics", stats)

    def show_suggestion(self):
        """Display a suggested move based on the current game state."""
        if not self.game_over and len(self.player_hand) >= 2:
            suggestion = self.suggest_move()
            messagebox.showinfo("Suggested Move", suggestion)
        else:
            messagebox.showinfo("Suggestion", "Cannot suggest a move at this time.")

def main():
    """Create the main window and start the game"""
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()