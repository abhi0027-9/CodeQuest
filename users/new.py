import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    print("\n" + "="*50)
    print(" "*15 + "NUMBER GUESSING GAME")
    print("="*50 + "\n")

def get_difficulty():
    while True:
        print("\nSelect difficulty level:")
        print("1. Easy (1-50, 10 attempts)")
        print("2. Medium (1-100, 7 attempts)")
        print("3. Hard (1-200, 5 attempts)")
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            print("Please enter 1, 2, or 3!")
        except ValueError:
            print("Invalid input! Please enter a number.")

def get_game_settings(difficulty):
    if difficulty == 1:
        return 1, 50, 10
    elif difficulty == 2:
        return 1, 100, 7
    else:
        return 1, 200, 5

def play_game():
    score = 0
    games_played = 0
    
    while True:
        clear_screen()
        display_header()
        
        # Get difficulty and set up game
        difficulty = get_difficulty()
        min_num, max_num, max_attempts = get_game_settings(difficulty)
        secret_number = random.randint(min_num, max_num)
        attempts = 0
        
        print(f"\nI'm thinking of a number between {min_num} and {max_num}.")
        print(f"You have {max_attempts} attempts to guess it.\n")
        
        # Main game loop
        while attempts < max_attempts:
            try:
                guess = int(input(f"Attempt {attempts + 1}/{max_attempts}. Enter your guess: "))
                
                if guess < min_num or guess > max_num:
                    print(f"Please enter a number between {min_num} and {max_num}!")
                    continue
                    
                attempts += 1
                
                if guess == secret_number:
                    points = max_attempts - attempts + 1
                    score += points * difficulty  # Higher points for higher difficulty
                    print(f"\n🎉 CONGRATULATIONS! You guessed it in {attempts} attempts!")
                    print(f"You earned {points * difficulty} points!")
                    break
                    
                if guess < secret_number:
                    print("Too low! Try a higher number.")
                else:
                    print("Too high! Try a lower number.")
                    
                if attempts == max_attempts:
                    print(f"\nGame Over! The number was {secret_number}")
                
            except ValueError:
                print("Please enter a valid number!")
                continue
        
        games_played += 1
        
        # Display current stats
        print(f"\nCurrent Statistics:")
        print(f"Games Played: {games_played}")
        print(f"Total Score: {score}")
        print(f"Average Score: {score/games_played:.2f}")
        
        # Ask to play again
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").lower()
            if play_again in ['yes', 'no', 'y', 'n']:
                break
            print("Please enter 'yes' or 'no'!")
            
        if play_again in ['no', 'n']:
            break
    
    # Display final stats
    clear_screen()
    display_header()
    print("Final Statistics:")
    print(f"Games Played: {games_played}")
    print(f"Total Score: {score}")
    print(f"Average Score: {score/games_played:.2f}")
    print("\nThanks for playing! 👋\n")

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing! 👋\n")