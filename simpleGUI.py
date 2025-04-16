import tkinter as tk
from tkinter import messagebox
from quiz_questions import level_1_questions, level_2_questions, level_3_questions, level_4_questions, level_5_questions
import random

class QuizGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cognitive Ability Quiz")
        self.root.geometry("800x600")
        self.root.configure(bg="#001f3f")

        self.score = 0
        self.total_questions_asked = 0
        self.current_level = 1
        self.level_5_lives = 0
        self.max_questions = 10

        self.question_pools = {
            1: level_1_questions[:],
            2: level_2_questions[:],
            3: level_3_questions[:],
            4: level_4_questions[:],
            5: level_5_questions[:]
        }

        for q_list in self.question_pools.values():
            random.shuffle(q_list)

        self.title_label = tk.Label(
            self.root, text="COGNITIVE ABILITY QUIZ", font=("Arial Black", 24),
            bg="#001f3f", fg="#FFDC00")
        self.title_label.pack(pady=20)

        self.question_label = tk.Label(
            self.root, text="", wraplength=700, font=("Arial", 16, "bold"),
            bg="#001f3f", fg="white", justify="center")
        self.question_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.root, bg="#001f3f")
        self.buttons_frame.pack()

        self.buttons = []
        for i in range(5):
            button = tk.Button(
                self.buttons_frame, text="", width=30, height=2,
                font=("Arial", 12, "bold"), bg="#0074D9", fg="white",
                activebackground="#FFDC00", activeforeground="#001f3f",
                relief="raised", bd=4, command=lambda i=i: self.check_answer(i))
            button.grid(row=i, column=0, pady=5, padx=20)
            self.buttons.append(button)

        self.status_label = tk.Label(
            self.root, text="", font=("Arial", 14),
            bg="#001f3f", fg="white")
        self.status_label.pack(pady=15)

        self.score_label = tk.Label(
            self.root, text=f"Score: {self.score}", font=("Arial", 14, "bold"),
            bg="#001f3f", fg="#FFDC00")
        self.score_label.pack(pady=5)

        self.next_question()
        self.root.mainloop()

    def next_question(self):
        self.status_label.config(text="")

        if self.total_questions_asked >= self.max_questions:
            self.show_final_results()
            return

        question_list = self.question_pools.get(self.current_level, [])
        if not question_list:
            self.status_label.config(text=f"No more questions available for Level {self.current_level}", fg="#FF851B")
            return

        q, choices, answer = question_list.pop()
        self.correct_answer = answer
        self.question_label.config(text=f"(Level {self.current_level}) {q}")

        for i in range(5):
            self.buttons[i].config(text=choices[i], state=tk.NORMAL)

    def check_answer(self, index):
        selected_text = self.buttons[index]["text"]
        selected_letter = selected_text[0]
        correct = selected_letter == self.correct_answer

        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        if correct:
            self.status_label.config(text="Correct!", fg="#2ECC40")
            self.score += 1
            if self.current_level < 5:
                self.current_level += 1
            else:
                self.level_5_lives += 1  # gain a life at Level 5
        else:
            self.status_label.config(text=f"Wrong! Correct answer was: {self.correct_answer}", fg="#FF4136")
            if self.current_level == 1:
                self.current_level = 1  # stays at level 1
            elif self.current_level == 2:
                self.current_level = 1
            elif self.current_level == 3:
                self.current_level = 2
            elif self.current_level == 4:
                self.current_level = 3
            elif self.current_level == 5:
                if self.level_5_lives > 0:
                    self.level_5_lives -= 1  # lose a life but stay in level 5
                else:
                    self.current_level = 4  # drop down

        self.total_questions_asked += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.root.after(1500, self.next_question)

    def show_final_results(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

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

        final_label = cognitive_scale.get(self.score, "Unknown")
        self.question_label.config(
            text=f"Quiz Complete!\n\nFinal Score: {self.score}/10\nCognitive Ability: {final_label}",
            font=("Arial", 18, "bold"),
            fg="#FFDC00"
        )
        self.status_label.config(text="Thank you for playing!", fg="#7FDBFF")

if __name__ == "__main__":
    QuizGUI()
