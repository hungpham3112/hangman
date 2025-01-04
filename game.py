import tkinter as tk
from tkinter import messagebox
import requests
import random

# Function to fetch a random word from a public API
CUSTOM_WORD_LIST = ["hanoi", "haiphong", "thainguyen", "hochiminh", "danang"]
def get_random_word():
    return random.choice(CUSTOM_WORD_LIST).lower()
    # try:
    #     response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
    #     if response.status_code == 200:
    #         word = response.json()[0]
    #         return word.lower()
    #     else:
    #         messagebox.showerror("Error", "Failed to fetch a word from the API.")
    #         return "example"  # Fallback word
    # except Exception as e:
    #     messagebox.showerror("Error", f"An error occurred: {e}")
    #     return "example"  # Fallback word

#Hangman Game Class
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        self.word_to_guess = get_random_word()
        self.guessed_word = ["_" for _ in self.word_to_guess]
        self.remaining_attempts = 6
        self.guessed_letters = set()

        # GUI Components
        self.label_word = tk.Label(root, text=" ".join(self.guessed_word), font=("Arial", 20))
        self.label_word.pack(pady=10)

        self.label_attempts = tk.Label(root, text=f"Remaining Attempts: {self.remaining_attempts}", font=("Arial", 14))
        self.label_attempts.pack(pady=5)

        self.canvas = tk.Canvas(root, width=200, height=250, bg="white")
        self.canvas.pack(pady=10)
        self.draw_hangman()

        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(pady=5)

        self.buttons = {}
        for char in "abcdefghijklmnopqrstuvwxyz":
            btn = tk.Button(self.frame_buttons, text=char.upper(), command=lambda c=char: self.check_guess(c), font=("Arial", 12), width=2)
            btn.grid(row=ord(char) // 10 - 9, column=ord(char) % 10)
            self.buttons[char] = btn

        self.label_guessed = tk.Label(root, text="Guessed Letters: None", font=("Arial", 12))
        self.label_guessed.pack(pady=5)

    def draw_hangman(self):
        self.canvas.delete("all")
        # Draw base
        self.canvas.create_line(10, 230, 150, 230, width=2)
        self.canvas.create_line(80, 230, 80, 20, width=2)
        self.canvas.create_line(80, 20, 140, 20, width=2)
        self.canvas.create_line(140, 20, 140, 40, width=2)

        # Add hangman parts based on remaining attempts
        parts = 6 - self.remaining_attempts
        if parts >= 1:  # Head
            self.canvas.create_oval(120, 40, 160, 80, width=2)
        if parts >= 2:  # Body
            self.canvas.create_line(140, 80, 140, 150, width=2)
        if parts >= 3:  # Left Arm
            self.canvas.create_line(140, 100, 120, 130, width=2)
        if parts >= 4:  # Right Arm
            self.canvas.create_line(140, 100, 160, 130, width=2)
        if parts >= 5:  # Left Leg
            self.canvas.create_line(140, 150, 120, 190, width=2)
        if parts >= 6:  # Right Leg
            self.canvas.create_line(140, 150, 160, 190, width=2)

    def check_guess(self, letter):
        self.buttons[letter].config(state="disabled")
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        self.label_guessed.config(text=f"Guessed Letters: {', '.join(sorted(self.guessed_letters))}")

        if letter in self.word_to_guess:
            for i, char in enumerate(self.word_to_guess):
                if char == letter:
                    self.guessed_word[i] = letter
            self.label_word.config(text=" ".join(self.guessed_word))

            if "_" not in self.guessed_word:
                messagebox.showinfo("You Win!", f"Congratulations! You guessed the word: {self.word_to_guess}")
                self.reset_game()
        else:
            self.remaining_attempts -= 1
            self.label_attempts.config(text=f"Remaining Attempts: {self.remaining_attempts}")
            self.draw_hangman()

            if self.remaining_attempts == 0:
                messagebox.showinfo("Game Over", f"You lost! The word was: {self.word_to_guess}")
                self.reset_game()

    def reset_game(self):
        self.word_to_guess = get_random_word()
        self.guessed_word = ["_" for _ in self.word_to_guess]
        self.remaining_attempts = 6
        self.guessed_letters = set()

        self.label_word.config(text=" ".join(self.guessed_word))
        self.label_attempts.config(text=f"Remaining Attempts: {self.remaining_attempts}")
        self.label_guessed.config(text="Guessed Letters: None")
        for button in self.buttons.values():
            button.config(state="normal")
        self.draw_hangman()

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
