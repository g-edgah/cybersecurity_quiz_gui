import tkinter as tk
from tkinter import ttk, messagebox

class Quiz:
    def __init__(self, root):
        self.root = root
        self.setup_quiz()
        self.setup_ui()
        self.show_question()

    def setup_quiz(self):

        self.questions = [
            {
                "question": "What is the most secure type of password?",
                "options": ["A short, simple word", "A long passphrase with mixed characters", "Your pet's name", "123456"],
                "correct_answer": 1,
                "tip": "Long passphrases with uppercase, lowercase, numbers and symbols are hardest to crack."
            },
            # {
            #     "question": "What should you do if you receive a suspicious email?",
            #     "options": ["Click all links to check", "Reply and ask for more info", "Delete it immediately", "Forward to all friends"],
            #     "correct_answer": 2,
            #     "tip": "Never click links or download attachments from suspicious emails. Delete them immediately."
            # },
            # {
            #     "question": "What is two-factor authentication (2FA)?",
            #     "options": ["Using two passwords", "An extra layer of security requiring two verification methods", "Having two email accounts", "A type of virus"],
            #     "correct_answer": 1,
            #     "tip": "2FA adds an extra security layer by requiring something you know (password) and something you have (phone)."
            # },
            # {
            #     "question": "Which is the safest practice for public Wi-Fi?",
            #     "options": ["Do online banking", "Use VPN", "Share personal information", "Disable firewall"],
            #     "correct_answer": 1,
            #     "tip": "Always use a VPN on public Wi-Fi to encrypt your connection and protect your data."
            # },
            # {
            #     "question": "How often should you update your software?",
            #     "options": ["Never", "Only when forced", "Immediately when updates are available", "Once a year"],
            #     "correct_answer": 2,
            #     "tip": "Regular updates patch security vulnerabilities that hackers could exploit."
            # },
            # {
            #     "question": "What is phishing?",
            #     "options": ["A fishing hobby", "A type of malware", "Fraudulent attempt to get sensitive information", "A password manager"],
            #     "correct_answer": 2,
            #     "tip": "Phishing uses fake emails/websites to trick you into revealing passwords, credit card numbers, etc."
            # },
            # {
            #     "question": "Why should you use different passwords for different accounts?",
            #     "options": ["It's too hard to remember", "To prevent credential stuffing attacks", "No particular reason", "To confuse hackers"],
            #     "correct_answer": 1,
            #     "tip": "If one account is compromised, different passwords prevent hackers from accessing all your accounts."
            # }
        ]

        self.current_question = 0
        self.score = 0
        self.wrong_answers = []

    def rounded_window(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points= [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2, x1, y2-radius,
            x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def rounded_button(self, parent, text, command, bg_color, fg_color='white', hover_color=None, width=120, height=40, radius=15):
        if hover_color is None:
            hover_color = self.adjust_color(bg_color, 20)

        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget('bg'), highlightthickness=0)

        button_bg = self.rounded_window(canvas, 2, 2, width-2, height-2, radius=radius, fill=bg_color, outline=bg_color)

        text_id = canvas.create_text(width//2, height//2, text=text, fill=fg_color, font=('Arial', 10, 'bold'))

        def on_enter (e):
            canvas.itemconfig(button_bg, fill=hover_color, outline=hover_color)

        def on_leave(e):
            canvas.itemconfig(button_bg, fill=bg_color, outline=bg_color)

        def on_click(e):
            command()

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        canvas.text_id = text_id
        canvas.button_bg = button_bg

        return canvas
    
    def adjust_color(self, color, amount):
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = [min(255, max(0, c + amount)) for c in rgb]
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"
    
    def setup_ui(self):

        self.colors = {
            'bg_primary': '#ecf0f1',
            'bg_secondary': '#879E9D',
            'bg_tertiary': '#0f3460',
            'accent': '#e94560',
            'success': "#007848",
            'warning': '#f39c12',
            'danger': "#820000",
            'info': '#192bc2',
            'text_primary': '#000000',
            'text_secondary': '#bdc3c7'
        }
        

        self.root.configure(bg=self.colors['bg_primary'])
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.pack(padx=15, pady=15, anchor='center')

        self.header()

        self.main_question_canvas = tk.Canvas(self.main_frame,bg=self.colors['bg_primary'], highlightthickness=0)
        self.main_question_canvas.pack( padx=15, pady=15, anchor='center')
       
        self.rounded_window(self.main_question_canvas, 0, 0, 600, 305, radius=20, fill=self.colors['bg_secondary'])


        self.question()

        self.options_frame= tk.Frame(self.main_question_canvas, bg=self.colors['bg_secondary'])
        self.options_frame.pack(fill='x', pady=15, padx=25)

        
        self.progress()
        

        self.buttons()

        self.setup_score()

    def header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))

        title_canvas = tk.Canvas(header_frame, width=400, height=60, bg=self.colors['bg_primary'], highlightthickness=0)
        title_canvas.pack()

        self.rounded_window(title_canvas, 10, 10, 390, 50, radius=20, fill=self.colors['bg_primary'])

        title_canvas.create_text(200, 30, text="cybersecurity quiz", fill=self.colors['text_primary'], font=('Arial', 15, 'bold'))

    def progress(self):
        progress_frame = tk.Frame(self.main_question_canvas, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill='x', pady=10, padx=15)
        
        #label
        self.progress_label = tk.Label(progress_frame, text="", font=('Arial', 11, 'bold'), fg=self.colors['text_primary'], bg=self.colors['bg_secondary'])
        self.progress_label.pack()
        
        # #bar
        # self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=400, mode='determinate')
        # self.progress_bar.pack(pady=5)

    def question(self):
        self.question_canvas = tk.Canvas(self.main_question_canvas, bg=self.colors['bg_secondary'], width=550, height=50, highlightthickness=0)
        self.question_canvas.pack(side='top', padx=0, pady=20, anchor='center')
        
        
        #label
        self.question_label = tk.Label(self.question_canvas, text="", font=('Arial', 12, 'bold'), fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],wraplength=500)
        self.question_canvas.create_window( 30, 35, window=self.question_label, anchor='w')

    def buttons(self):
        control_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        control_frame.pack(fill='x', pady=20)
        
        #submit
        self.submit_btn = self.rounded_button(control_frame, "Submit Answer", self.check_answer, self.colors['success'], hover_color=self.adjust_color(self.colors['success'], 30), width=140, height=45)
        self.submit_btn.pack(side='left', padx=20)
        
        #quit
        self.quit_btn = self.rounded_button(control_frame, "Quit Quiz", self.quit_quiz, self.colors['danger'], hover_color=self.adjust_color(self.colors['danger'], 30),width=120, height=45)
        self.quit_btn.pack(side='right', padx=20)

    def setup_score(self):
        self.score_canvas = tk.Canvas(self.main_frame, bg=self.colors['bg_primary'], height=60, highlightthickness=0)
        self.score_canvas.pack(fill='x', pady=10)
        
        #background
        self.score_bg = self.rounded_window(self.score_canvas, 150, 5, 400, 55, radius=15,fill=self.colors['bg_secondary'], outline=self.colors['text_primary'])
        
        #label
        self.score_label = tk.Label(self.score_canvas, text="Score: 0/0", font=('Arial', 14, 'bold'), fg=self.colors['text_primary'], bg=self.colors['bg_secondary'])
        self.score_canvas.create_window(275, 30, window=self.score_label)
    
    def create_option_button(self, text, value, var):
        option_frame = tk.Frame(self.options_frame, bg=self.colors['text_primary'])
        option_frame.pack(fill='x', pady=4, padx=25)
        
        canvas = tk.Canvas(option_frame, width=500, height=30, bg=self.colors['bg_secondary'], highlightthickness=0)
        canvas.pack()
        
        #background
        bg_id = self.rounded_window(canvas, 0, 0, 495, 30, radius=12,  fill=self.colors['bg_secondary'])
        
        #radio
        radio_id = canvas.create_oval(12, 12, 20, 20, fill=self.colors['bg_secondary'], outline=self.colors['text_secondary'], width=2)
        
        #text
        text_id = canvas.create_text(50, 15, text=text, anchor='w', fill=self.colors['text_primary'], font=('Arial', 12))
        
        def on_click(e):
            var.set(value)
            update_appearance(True)
        
        def on_enter(e):
            if var.get() != value:
                canvas.itemconfig(bg_id, fill=self.adjust_color(self.colors['bg_secondary'], 10))
        
        def on_leave(e):
            if var.get() != value:
                canvas.itemconfig(bg_id, fill=self.colors['bg_secondary'])
        
        def update_appearance(selected):
            if selected:
                canvas.itemconfig(bg_id, fill=self.colors['info'])
                canvas.itemconfig(radio_id, fill=self.colors['text_primary'], outline=self.colors['text_primary'])
            else:
                canvas.itemconfig(bg_id, fill=self.colors['bg_secondary'])
                canvas.itemconfig(radio_id, fill=self.colors['bg_secondary'], outline=self.colors['text_secondary'])
        
        #events binding
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        
        #store references
        canvas.bg_id = bg_id
        canvas.radio_id = radio_id
        canvas.text_id = text_id
        canvas.update_appearance = lambda: update_appearance(var.get() == value)
        
        #initial update
        canvas.update_appearance()
        
        return canvas

    def show_question(self):
        #clear
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.option_widgets = []
        self.option_vars = []
        
        #update progress
        progress = (self.current_question / len(self.questions)) * 100
        self.progress_label.config(text=f"Question {self.current_question + 1} of {len(self.questions)}")
        #self.progress_bar['value'] = progress
        
        #show current question
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        
        #option buttons
        for i, option in enumerate(question_data["options"]):
            var = tk.StringVar(value="")
            option_btn = self.create_option_button(option, str(i), var)
            self.option_widgets.append(option_btn)
            self.option_vars.append(var)
        
        #update score
        self.score_label.config(text=f"Score: {self.score}/{self.current_question}")

    def check_answer(self):
        selected_option = None
        for i, var in enumerate(self.option_vars):
            if var.get() != "":
                selected_option = int(var.get())
                break
        
        if selected_option is None:
            messagebox.showwarning("No Selection", "Please select an answer before submitting.")
            return
        
        question_data = self.questions[self.current_question]
        
        #feedback
        for i, widget in enumerate(self.option_widgets):
            if i == question_data["correct_answer"]:
                widget.itemconfig(widget.bg_id, fill=self.colors['success'])
            elif i == selected_option and i != question_data["correct_answer"]:
                widget.itemconfig(widget.bg_id, fill=self.colors['danger'])
            widget.update_appearance()
        
        self.root.after(1000, self.process_answer, selected_option, question_data)

    def process_answer(self, selected_option, question_data):
        if selected_option == question_data["correct_answer"]:
            self.score += 1
        else:
            self.wrong_answers.append({"question": question_data["question"], "user_answer": question_data["options"][selected_option], "correct_answer": question_data["options"][question_data["correct_answer"]],"tip": question_data["tip"]})
        
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        #results container
        results_canvas = tk.Canvas(self.main_frame, bg=self.colors['bg_primary'], width=700, height=700, highlightthickness=0)
        results_canvas.pack(anchor='center', expand=True)
        
        #main results
        self.rounded_window(results_canvas, 25, 20, 640, 140, radius=25,fill=self.colors['bg_tertiary'], outline=self.colors['info'])
        
        #results title
        results_canvas.create_text(275, 50, text="quiz completed!", fill=self.colors['text_primary'], font=('Arial', 20, 'bold'))
        
        #score display
        score_text = f"Final Score: {self.score}/{len(self.questions)}"
        results_canvas.create_text(275, 85, text=score_text, fill=self.colors['text_primary'], font=('Arial', 16, 'bold'))
        
        #performance rating
        percentage = (self.score / len(self.questions)) * 100
        if percentage >= 80:
            performance = "Excellent! You know your stuff."
            color = self.colors['success']
        elif percentage >= 60:
            performance = "Good job! You have a solid grasp of things."
            color = self.colors['warning']
        else:
            performance = "Keep learning! we all have to start somewhere."
            color = self.colors['danger']
        
        results_canvas.create_text(275, 115, text=performance, fill=color, font=('Arial', 12, 'bold'))
        
        #tips
        if self.wrong_answers:
            self.tips_section(results_canvas)
        
        #action buttons
        button_frame = tk.Frame(results_canvas, bg=self.colors['bg_primary'])
        results_canvas.create_window(275, 450, window=button_frame)
        
        restart_btn = self.rounded_button(button_frame, "Restart Quiz", self.restart_quiz, self.colors['info'], hover_color=self.adjust_color(self.colors['info'], 30), width=140, height=45)
        restart_btn.pack(side='left', padx=10)
        
        quit_btn = self.rounded_button(button_frame, "Quit", self.quit_quiz, self.colors['danger'], hover_color=self.adjust_color(self.colors['danger'], 30),  width=100, height=45)
        quit_btn.pack(side='left', padx=10)
    
    def tips_section(self, parent_canvas):
        #header
        parent_canvas.create_text(275, 160, text="Security Tips & Improvements", fill=self.colors['text_primary'], font=('Arial', 14, 'bold'))
        
        #container
        tips_frame = tk.Frame(parent_canvas, bg=self.colors['bg_primary'])
        parent_canvas.create_window(345, 350, window=tips_frame, width=650, height=400)
        
        #scrollable canvas
        canvas = tk.Canvas(tips_frame, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tips_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        #tips
        y_offset = 10
        for i, wrong in enumerate(self.wrong_answers):
            tip_canvas = tk.Canvas(scrollable_frame, width=650, height=140, bg=self.colors['bg_primary'], highlightthickness=0)
            tip_canvas.pack(pady=5)
            
            #card
            self.rounded_window(tip_canvas, 5, 5, 620, 135, radius=15, fill=self.colors['bg_secondary'],)
            
            #question
            tip_canvas.create_text(15, 20, text=f"Q: {wrong['question']}", anchor='w', fill=self.colors['text_primary'], font=('Arial', 12, 'bold'), width=430)
            
            #answers
            tip_canvas.create_text(15, 50, text=f"Your answer: {wrong['user_answer']}", anchor='w', fill=self.colors['danger'], font=('Arial', 12), width=430)
            
            tip_canvas.create_text(15, 75, text=f"Correct: {wrong['correct_answer']}", anchor='w', fill=self.colors['success'], font=('Arial', 12), width=430)
            
            #tip
            tip_canvas.create_text(15, 110, text=f"{wrong['tip']}", anchor='w', fill=self.colors['text_primary'], font=('Arial', 12, 'italic'), width=430)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.wrong_answers = []
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.setup_quiz()
        self.setup_ui()
        self.show_question()

    
    def quit_quiz(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit the quiz?"):
            self.root.destroy()
    


def main():
    window = tk.Tk()
    window.title("cybersecurity quiz")
    window.geometry("700x630")
    window.configure(bg='#1a1a2e')
    window.resizable(False, False)
    
    # Center the window
    window.eval('tk::PlaceWindow . center')
    
    game = Quiz(window)
    window.mainloop()


main()    