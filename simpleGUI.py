import tkinter as tk
from tkinter import messagebox
from quiz_questions import level_1_questions, level_2_questions, level_3_questions, level_4_questions, level_5_questions
import random

class QuizGUI:
    def __init__(self):
        # Initialize the main window and set its properties
        self.root = tk.Tk()
        self.root.title("Cognitive Ability Quiz")  # Window title
        self.root.geometry("800x600")  # Window size
        self.root.configure(bg="#001f3f")  # Background color

        # Initialize game state variables
        self.score = 0  # Player's score
        self.total_questions_asked = 0  # Number of questions asked so far
        self.current_level = 1  # Current level in the game
        self.level_5_lives = 0  # Lives available for level 5
        self.max_questions = 10  # Maximum number of questions to ask

        # Create a pool of questions for each level
        self.question_pools = {
            1: level_1_questions[:],
            2: level_2_questions[:],
            3: level_3_questions[:],
            4: level_4_questions[:],
            5: level_5_questions[:]
        }

        # Shuffle questions for randomness
        for q_list in self.question_pools.values():
            random.shuffle(q_list)

        # Create title label
        self.title_label = tk.Label(
            self.root, text="COGNITIVE ABILITY QUIZ", font=("Arial Black", 24),
            bg="#001f3f", fg="#FFDC00")  # Label for title with yellow text
        self.title_label.pack(pady=20)  # Pack it into the window

        # Create label for the question text
        self.question_label = tk.Label(
            self.root, text="", wraplength=700, font=("Arial", 16, "bold"),
            bg="#001f3f", fg="white", justify="center")  # White text for questions
        self.question_label.pack(pady=20)  # Pack it into the window

        # Create a frame to hold answer buttons
        self.buttons_frame = tk.Frame(self.root, bg="#001f3f")
        self.buttons_frame.pack()

        # Create buttons for each answer option
        self.buttons = []
        for i in range(5):
            button = tk.Button(
                self.buttons_frame, text="", width=30, height=2,  # Button size
                font=("Arial", 12, "bold"), bg="#0074D9", fg="white",  # Button color
                activebackground="#FFDC00", activeforeground="#001f3f",  # Active button colors
                relief="raised", bd=4, command=lambda i=i: self.check_answer(i))  # Button click handler
            button.grid(row=i, column=0, pady=5, padx=20)  # Position buttons in grid
            self.buttons.append(button)

        # Create status label to show correctness of answers
        self.status_label = tk.Label(
            self.root, text="", font=("Arial", 14),
            bg="#001f3f", fg="white")
        self.status_label.pack(pady=15)

        # Create label for displaying score
        self.score_label = tk.Label(
            self.root, text=f"Score: {self.score}", font=("Arial", 14, "bold"),
            bg="#001f3f", fg="#FFDC00")
        self.score_label.pack(pady=5)

        # Start the game by showing the first question
        self.next_question()
        self.root.mainloop()  # Start the Tkinter event loop

    def next_question(self):
        # Reset the status label for the next question
        self.status_label.config(text="")

        # Check if the maximum number of questions has been reached
        if self.total_questions_asked >= self.max_questions:
            self.show_final_results()  # Show final results when max questions are reached
            return

        # Get the list of questions for the current level
        question_list = self.question_pools.get(self.current_level, [])
        if not question_list:  # If no questions are left for the level
            self.status_label.config(text=f"No more questions available for Level {self.current_level}", fg="#FF851B")
            return

        # Pop the next question and its choices
        q, choices, answer = question_list.pop()
        self.correct_answer = answer  # Store the correct answer
        self.question_label.config(text=f"(Level {self.current_level}) {q}")  # Display the question

        # Update buttons with the answer choices
        for i in range(5):
            self.buttons[i].config(text=choices[i], state=tk.NORMAL)

    def check_answer(self, index):
        # Get the selected answer and check if it is correct
        selected_text = self.buttons[index]["text"]
        selected_letter = selected_text[0]  # The first letter of the choice (A, B, C, etc.)
        correct = selected_letter == self.correct_answer  # Check if the selected answer is correct

        # Disable all answer buttons after selection
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        # Update the status label based on the correctness of the answer
        if correct:
            self.status_label.config(text="Correct!", fg="#2ECC40")  # Green for correct answer
            self.score += 1  # Increase the score
            if self.current_level < 5:
                self.current_level += 1  # Level up if not at level 5
            else:
                self.level_5_lives += 1  # Gain a life at level 5
        else:
            # Handle wrong answers and level progression
            self.status_label.config(text=f"Wrong! Correct answer was: {self.correct_answer}", fg="#FF4136")  # Red for wrong
            if self.current_level == 1:
                self.current_level = 1  # Stay at level 1
            elif self.current_level == 2:
                self.current_level = 1  # Drop to level 1
            elif self.current_level == 3:
                self.current_level = 2  # Drop to level 2
            elif self.current_level == 4:
                self.current_level = 3  # Drop to level 3
            elif self.current_level == 5:
                if self.level_5_lives > 0:
                    self.level_5_lives -= 1  # Lose a life but stay at level 5
                else:
                    self.current_level = 4  # Drop to level 4 if no lives left

        # Update the score label
        self.total_questions_asked += 1
        self.score_label.config(text=f"Score: {self.score}")
        
        # Move to the next question after a short delay
        self.root.after(1500, self.next_question)

    def show_final_results(self):
        # Disable all answer buttons at the end
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        # Map the score to a cognitive ability scale
        cognitive_scale = {
            0: "Newborn",
            1: "Toddler",
            2: "Preschooler",
            3: "Child",
            4: "Teenager",
            5: "Young Adult",
            6: "Average Adult",
            7: "Smart",
            8: "Gifted",
            9: "Prodigy",
            10: "Genius"
        }

        # Get the final cognitive ability label based on the score
        final_label = cognitive_scale.get(self.score, "Unknown")
        
        # Display the final result on the question label
        self.question_label.config(
            text=f"Quiz Complete!\n\nFinal Score: {self.score}/10\nCognitive Ability: {final_label}",
            font=("Arial", 18, "bold"),
            fg="#FFDC00"
        )
        # Display a thank you message
        self.status_label.config(text="Thank you for playing!", fg="#7FDBFF")

if __name__ == "__main__":
    # Create and start the quiz application
    QuizGUI()
