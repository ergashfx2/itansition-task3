import sys
import hashlib
import hmac
import secrets

class KeyGenerator:
    @staticmethod
    def generate_key():
        return secrets.token_bytes(32)

class HMACCalculator:
    @staticmethod
    def calculate_hmac(message, key):
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

class MoveEvaluator:
    @staticmethod
    def determine_winner(player_move, computer_move, moves):
        n = len(moves)
        half = n // 2
        index_player = moves.index(player_move)
        index_computer = moves.index(computer_move)
        if index_player == index_computer:
            return "Draw"
        elif (index_player - index_computer) % n <= half:
            return "Player wins"
        else:
            return "Computer wins"

class TableGenerator:
    @staticmethod
    def generate_table(moves):
        n = len(moves)
        table = [['' for _ in range(n + 1)] for _ in range(n + 1)]
        table[0][0] = 'Moves'
        for i in range(1, n + 1):
            table[0][i] = moves[i - 1]
            table[i][0] = moves[i - 1]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                table[i][j] = TableGenerator.determine_winner(moves[i - 1], moves[j - 1], moves)
        return table

    @staticmethod
    def determine_winner(move1, move2, moves):
        index_move1 = moves.index(move1)
        index_move2 = moves.index(move2)
        n = len(moves)
        half = n // 2
        if index_move1 == index_move2:
            return "Draw"
        elif (index_move1 - index_move2) % n <= half:
            return "Win"
        else:
            return "Lose"

class Game:
    def __init__(self, moves):
        self.moves = moves
        self.key = KeyGenerator.generate_key()
        self.computer_move = secrets.choice(moves)

    def display_hmac(self):
        hmac = HMACCalculator.calculate_hmac(self.computer_move, self.key)
        print("HMAC:", hmac)

    def display_menu(self):
        print("Menu:")
        for i, move in enumerate(self.moves):
            print(f"{i + 1} - {move}")
        print("0 - Exit")

    def play_game(self):
        self.display_hmac()
        self.display_menu()
        while True:
            user_choice = input("Enter your choice: ")
            if user_choice.isdigit():
                user_choice = int(user_choice)
                if 0 <= user_choice <= len(self.moves):
                    if user_choice == 0:
                        print("Exiting the game.")
                        sys.exit()
                    else:
                        user_move = self.moves[user_choice - 1]
                        print(f"Your move: {user_move}")
                        print(f"Computer's move: {self.computer_move}")
                        print(f"Key: {self.key.hex()}")
                        winner = MoveEvaluator.determine_winner(user_move, self.computer_move, self.moves)
                        print(f"Result: {winner}")
                        break
                else:
                    print("Invalid choice. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def display_help(moves):
        table = TableGenerator.generate_table(moves)
        print("\nHelp Table:")
        for row in table:
            print(" ".join(row))

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) % 2 == 0:
        print("Error: Please provide an odd number of non-repeating moves as command line arguments.")
        print("Example: python rps.py Rock Paper Scissors")
        sys.exit(1)

    moves = sys.argv[1:]
    game = Game(moves)
    game.play_game()
