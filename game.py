import os
# just for windows ig
import msvcrt
import random
from colorama import Fore, Style

def reset():
    global icons, board
    board = ["cell"] * 9
    icons = {
    "cell": """
⬜⬜⬜
⬜⬜⬜
⬜⬜⬜
"""
}

def print_board(turn_icon: str, position: int = None):
    """
    Print the Tic Tac Toe board.

    :param str turn_icon: The icon of the current player.
    :param int position: The position of the cursor.
    """
    os.system("cls")
    print(Fore.WHITE + "\t\t\t\tTic Tac Toe\n")
    print("Press the arrows to move, ENTER to place ur icon and ESC to leave.\n")
    print(f"\t\t\t\t{turn_icon}'s turn\n" + Fore.RESET)
    idx = 0
    for _ in range(3):
        lines = ["", "", ""]
        for __ in range(3):
            icon_lines = icons[board[idx]].strip().splitlines()
            if position and (idx + 1) == position:
                icon_lines = [line.replace("⬜", "🟩") for line in icon_lines]
            for k in range(3):
                if idx in [0, 3, 6]:
                  lines[k] += "\t\t\t" + icon_lines[k] + "\t"
                else:
                  lines[k] += icon_lines[k] + "\t"
            idx += 1
        print("\n".join(lines))

def place_icon(turn_icon: str, position: int):
    """
    Place the icon of the current player in the specific position of the board.

    :param str turn_icon: The icon of the current player.
    :param int position: The position of the cursor.
    """
    if board[position - 1] == "cell":
        board[position - 1] = turn_icon
        return True
    return False

def check_winner():
    """
    Check if there's a winner or not.
    """
    # Got the idea from my other project
    #* https://github.com/Alwexis/TicTacToe-Ionic/blob/main/src/app/classes/util.ts
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for comb in win_combinations:
        a, b, c = comb
        if board[a] == board[b] == board[c] != "cell":
            return board[a]
    return None

def is_board_full():
    """
    Check if the board is full or not, if it's full, then it's a tie.
    """
    return all(cell != "cell" for cell in board)

def get_key():
    """
    Get the key pressed by the user using msvcrt.
    """
    key = msvcrt.getch()
    if key == b'\xe0':
        key = msvcrt.getch()
        if key == b'H':
            return "up"
        elif key == b'P':
            return "down"
        elif key == b'K':
            return "left"
        elif key == b'M':
            return "right"
    elif key == b'\r':
        return "enter"
    elif key == b'\x1b':
        return "escape"
    return None

def get_icon_choice(player):
    """
    Get the icon choice of the player.

    :param str player: Player's name.
    """
    while True:
        icon = input(f"{player}, choose your icon (just one character) or press enter to choose default (🐶/😺): ")
        if icon == "":
            if "😺" not in icons:
                icons["😺"] = f"\n🟦🟦🟦\n🟦😺🟦\n🟦🟦🟦"
                print("You choosed the default icon 😺.")
                return "😺"
            elif "🐶" not in icons:
                icons["🐶"] = f"\n🟥🟥🟥\n🟥🐶🟥\n🟥🟥🟥"
                print("You choosed the default icon 🐶.")
                return "🐶"
        elif len(icon) != 1:
            print("Please, type just one character.")
        elif icon in icons:
            print("That icon is already taken, choose another different.")
        else:
            if player == "Player 1":
                icons[icon] = f"\n🟦🟦🟦\n🟦{icon}🟦\n🟦🟦🟦"
            else:
                icons[icon] = f"\n🟥🟥🟥\n🟥{icon}🟥\n🟥🟥🟥"
            return icon

def play_game():
    """
    Play the Tic Tac Toe game.
    """
    reset()
    
    player1_icon = get_icon_choice("Player 1")
    player2_icon = get_icon_choice("Player 2")
    
    turn_icon = random.choice([player1_icon, player2_icon])
    position = 5
    game_over = False

    while not game_over:
        print_board(turn_icon, position)
        key = get_key()

        if key == "escape":
            print("Game Over! The game was forced to stop by the player.")
            return False
        elif key == "up" and position > 3:
            position -= 3
        elif key == "down" and position < 7:
            position += 3
        elif key == "left" and position % 3 != 1:
            position -= 1
        elif key == "right" and position % 3 != 0:
            position += 1
        elif key == "enter":
            if place_icon(turn_icon, position):
                winner = check_winner()
                if winner:
                    print_board(turn_icon, position)
                    print(f"¡{winner} has won the game!")
                    game_over = True
                    play_again("win", winner)
                elif is_board_full():
                    print_board(turn_icon, position)
                    print("It's a tie!")
                    game_over = True
                    play_again("tie")
                else:
                    turn_icon = player1_icon if turn_icon == player2_icon else player2_icon
            else:
                input(Fore.RED + "Position already occupied!" + Fore.RESET)
    return True

def play_again(status="", winner=None):
    """
    Ask the player if they want to play again or not.
    """
    options = ["Yes", "Nope"]
    selected = 0

    while True:
        os.system("cls")
        if status == "tie":
            print(Fore.WHITE + "It's a tie!")
        elif status == "win":
            print(Fore.GREEN + f"{winner} won the game!")
        print(Fore.WHITE + "Do u want to play again?")
        
        for i, option in enumerate(options):
            if i == selected:
                print(Fore.GREEN + Style.BRIGHT + f"> {option}" + Fore.RESET + Style.RESET_ALL)
            else:
                print(Fore.WHITE + f"  {option}")
        
        key = get_key()
        if key == "up" and selected > 0:
            selected -= 1
        elif key == "down" and selected < len(options) - 1:
            selected += 1
        elif key == "enter":
            if selected == 0:
                main()
            else:
                print("Thanks for playing. Bye bye~!")
                exit()

def main():
    """
    main flow of the program.
    """
    os.system("cls")
    while True:
        if not play_game():
            break

if __name__ == "__main__":
    main()
