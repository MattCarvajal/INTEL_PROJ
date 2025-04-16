import tkinter as tk
from tkinter import messagebox
from quiz_questions import level_1_questions, level_2_questions, level_3_questions, level_4_questions, level_5_questions
import random

# Combine and shuffle all questions
all_questions = level_1_questions + level_2_questions + level_3_questions + level_4_questions + level_5_questions
random.shuffle(all_questions)

class QuizGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cognitive Ability Quiz")
        self.root.geometry("800x600")
        self.root.configure(bg="#001f3f")

        self.score = 0
        self.question_index = 0

        self.title_label = tk.Label(
            self.root,
            text="COGNITIVE ABILITY QUIZ",
            font=("Arial Black", 24),
            bg="#001f3f",
            fg="#FFDC00"
        )
        self.title_label.pack(pady=20)

        self.question_label = tk.Label(
            self.root,
            text="",
            wraplength=700,
            font=("Arial", 16, "bold"),
            bg="#001f3f",
            fg="white",
            justify="center"
        )
        self.question_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.root, bg="#001f3f")
        self.buttons_frame.pack()

        self.buttons = []
        for i in range(5):
            button = tk.Button(
                self.buttons_frame,
                text="",
                width=30,
                height=2,
                font=("Arial", 12, "bold"),
                bg="#0074D9",
                fg="white",
                activebackground="#FFDC00",
                activeforeground="#001f3f",
                relief="raised",
                bd=4,
                command=lambda i=i: self.check_answer(i)
            )
            button.grid(row=i, column=0, pady=5, padx=20)
            self.buttons.append(button)

        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14),
            bg="#001f3f",
            fg="white"
        )
        self.status_label.pack(pady=15)

        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}",
            font=("Arial", 14, "bold"),
            bg="#001f3f",
            fg="#FFDC00"
        )
        self.score_label.pack(pady=5)

        self.next_question()
        self.root.mainloop()

    def next_question(self):
        self.status_label.config(text="")
        if self.question_index >= len(all_questions):
            messagebox.showinfo("Quiz Finished", f"Your final score: {self.score}/{len(all_questions)}")
            self.root.quit()
            return

        q, choices, answer = all_questions[self.question_index]

        if len(choices) != 5:
            messagebox.showerror("Error", f"Question has {len(choices)} choices, expected 5:\n\n{q}")
            self.question_index += 1
            self.root.after(500, self.next_question)
            return

        self.correct_answer = answer
        self.question_label.config(text=q)

        for i in range(5):
            self.buttons[i].config(text=choices[i], state=tk.NORMAL)

    def check_answer(self, index):
        selected_text = self.buttons[index]["text"]
        selected_letter = selected_text[0]

        if selected_letter == self.correct_answer:
            self.score += 1
            self.status_label.config(text="Correct!", fg="#2ECC40")
        else:
            self.status_label.config(text=f"Wrong! Correct answer was: {self.correct_answer}", fg="#FF4136")

        self.score_label.config(text=f"Score: {self.score}")

        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        self.question_index += 1
        self.root.after(1500, self.next_question)

if __name__ == "__main__":
    QuizGUI()
