import random
import sys
import os
from enum import Enum

def verify_choice(choice: int) -> None:
    if choice < 1 or choice > 3:
        sys.exit()

def show_menu() -> int: 
    title = " ROCK, PAPER AND SCISSORS "
    print(title.center(54, "="))
    menu = f'''Please, enter the respective number:
    1 - ROCK
    2 - PAPER
    3 - SCISSORS
    [Another Number] - EXIT GAME'''
    print(menu)

class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

def game() -> bool:
    os.system("clear")
    show_menu()
    user_choice = int(input("Choice: "))
    verify_choice(user_choice)

    computer_choice = random.randint(1, 3)
    print("\n🧔 User Choice: " + str(RPS(user_choice)).replace("RPS.", ""))
    print("🐍 Python Choice: " + str(RPS(computer_choice)).replace("RPS.", ""))

    rock_value = RPS.ROCK.value
    paper_value = RPS.PAPER.value
    scissors_value = RPS.SCISSORS.value

    user_wins = (user_choice == rock_value and computer_choice == scissors_value) or (user_choice == paper_value and computer_choice == rock_value) or (user_choice == scissors_value and computer_choice == paper_value)

    if user_wins:
        print('\nCongrats! You Wins!🥳')
    elif user_choice == computer_choice:
        print('\nTie Game!😨')
    else:
        print('\nPython Wins!🐍')

    print("\nAnother try? (y | n)")
    user_input = input()
    if user_input == "y":
        os.system("clear")
        return True
    else:
        return False
    
def game_loop() -> None:
    while game() == True:
        pass

game_loop()