import tkinter as tk
from tkinter import messagebox
import random

class CricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#2d5016")
        
        # Game variables
        self.player_score = 0
        self.computer_score = 0
        self.player_wickets = 0
        self.computer_wickets = 0
        self.balls_played = 0
        self.max_balls = 30
        self.max_wickets = 5
        self.innings = 1
        self.target = 0
        self.toss_winner = None
        self.player_batting = None
        
        self.start_screen()
    
    def start_screen(self):
        self.clear_screen()
        
        # Title
        title = tk.Label(self.root, text="🏏 CRICKET GAME 🏏", 
                        font=("Arial", 36, "bold"), bg="#2d5016", fg="white")
        title.pack(pady=50)
        
        # Toss section
        toss_frame = tk.Frame(self.root, bg="#2d5016")
        toss_frame.pack(pady=30)
        
        tk.Label(toss_frame, text="Choose for Toss:", 
                font=("Arial", 18), bg="#2d5016", fg="white").pack(pady=10)
        
        btn_frame = tk.Frame(toss_frame, bg="#2d5016")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="HEADS", font=("Arial", 14, "bold"),
                 bg="#ff6b6b", fg="white", width=12, height=2,
                 command=lambda: self.toss("heads")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="TAILS", font=("Arial", 14, "bold"),
                 bg="#4ecdc4", fg="white", width=12, height=2,
                 command=lambda: self.toss("tails")).pack(side=tk.LEFT, padx=10)
    
    def toss(self, choice):
        result = random.choice(["heads", "tails"])
        
        if choice == result:
            self.toss_winner = "player"
            msg = f"🎉 You won the toss! It's {result.upper()}!\n\nWhat do you want to do?"
            self.choose_bat_bowl(msg)
        else:
            self.toss_winner = "computer"
            comp_choice = random.choice(["bat", "bowl"])
            self.player_batting = (comp_choice == "bowl")
            msg = f"😔 Computer won the toss! It's {result.upper()}!\n\nComputer chose to {comp_choice.upper()} first."
            messagebox.showinfo("Toss Result", msg)
            self.game_screen()
    
    def choose_bat_bowl(self, msg):
        dialog = tk.Toplevel(self.root)
        dialog.title("Toss Won!")
        dialog.geometry("400x250")
        dialog.configure(bg="#2d5016")
        
        tk.Label(dialog, text=msg, font=("Arial", 12), 
                bg="#2d5016", fg="white", justify=tk.CENTER).pack(pady=20)
        
        btn_frame = tk.Frame(dialog, bg="#2d5016")
        btn_frame.pack(pady=20)
        
        def choose(choice):
            self.player_batting = (choice == "bat")
            dialog.destroy()
            self.game_screen()
        
        tk.Button(btn_frame, text="BAT", font=("Arial", 14, "bold"),
                 bg="#ff6b6b", fg="white", width=10, height=2,
                 command=lambda: choose("bat")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="BOWL", font=("Arial", 14, "bold"),
                 bg="#4ecdc4", fg="white", width=10, height=2,
                 command=lambda: choose("bowl")).pack(side=tk.LEFT, padx=10)
    
    def game_screen(self):
        self.clear_screen()
        
        # Score display
        self.score_frame = tk.Frame(self.root, bg="#1a3a0f")
        self.score_frame.pack(fill=tk.X, pady=10)
        
        innings_text = "1st INNINGS" if self.innings == 1 else "2nd INNINGS"
        if self.innings == 2:
            innings_text += f" (Target: {self.target})"
        
        tk.Label(self.score_frame, text=innings_text, font=("Arial", 16, "bold"),
                bg="#1a3a0f", fg="yellow").pack(pady=5)
        
        self.player_label = tk.Label(self.score_frame, 
                                     text=f"YOU: {self.player_score}/{self.player_wickets}",
                                     font=("Arial", 20, "bold"), bg="#1a3a0f", fg="white")
        self.player_label.pack()
        
        self.computer_label = tk.Label(self.score_frame,
                                       text=f"COMPUTER: {self.computer_score}/{self.computer_wickets}",
                                       font=("Arial", 20, "bold"), bg="#1a3a0f", fg="white")
        self.computer_label.pack()
        
        self.balls_label = tk.Label(self.score_frame,
                                    text=f"Balls: {self.balls_played}/{self.max_balls}",
                                    font=("Arial", 14), bg="#1a3a0f", fg="lightgray")
        self.balls_label.pack(pady=5)
        
        # Current turn
        turn_text = "YOUR TURN TO BAT" if self.player_batting else "YOUR TURN TO BOWL"
        self.turn_label = tk.Label(self.root, text=turn_text,
                                   font=("Arial", 18, "bold"), bg="#2d5016", fg="yellow")
        self.turn_label.pack(pady=20)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"),
                                     bg="#2d5016", fg="white", height=2)
        self.result_label.pack()
        
        # Shot/Bowl buttons
        self.btn_frame = tk.Frame(self.root, bg="#2d5016")
        self.btn_frame.pack(pady=30)
        
        runs = [0, 1, 2, 3, 4, 6]
        colors = ["#e74c3c", "#3498db", "#9b59b6", "#e67e22", "#f39c12", "#27ae60"]
        
        for i, run in enumerate(runs):
            btn = tk.Button(self.btn_frame, text=str(run), font=("Arial", 18, "bold"),
                          bg=colors[i], fg="white", width=5, height=2,
                          command=lambda r=run: self.play_ball(r))
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)
    
    def play_ball(self, player_choice):
        computer_choice = random.choice([0, 1, 2, 3, 4, 6])
        
        self.balls_played += 1
        
        if player_choice == computer_choice:
            # Wicket!
            if self.player_batting:
                self.player_wickets += 1
                self.result_label.config(text=f"❌ OUT! Both chose {player_choice}", fg="red")
            else:
                self.computer_wickets += 1
                self.result_label.config(text=f"✅ WICKET! Both chose {player_choice}", fg="green")
        else:
            # Runs scored
            if self.player_batting:
                self.player_score += player_choice
                self.result_label.config(text=f"🏏 You: {player_choice}, Computer: {computer_choice} - {player_choice} runs!",
                                        fg="lightgreen")
            else:
                self.computer_score += computer_choice
                self.result_label.config(text=f"🎯 You: {player_choice}, Computer: {computer_choice} - {computer_choice} runs conceded!",
                                        fg="orange")
        
        self.update_score()
        self.check_innings_end()
    
    def update_score(self):
        self.player_label.config(text=f"YOU: {self.player_score}/{self.player_wickets}")
        self.computer_label.config(text=f"COMPUTER: {self.computer_score}/{self.computer_wickets}")
        self.balls_label.config(text=f"Balls: {self.balls_played}/{self.max_balls}")
    
    def check_innings_end(self):
        innings_over = False
        
        if self.player_batting:
            if self.player_wickets >= self.max_wickets or self.balls_played >= self.max_balls:
                innings_over = True
            elif self.innings == 2 and self.player_score > self.target:
                self.end_game("player")
                return
        else:
            if self.computer_wickets >= self.max_wickets or self.balls_played >= self.max_balls:
                innings_over = True
            elif self.innings == 2 and self.computer_score > self.target:
                self.end_game("computer")
                return
        
        if innings_over:
            if self.innings == 1:
                self.start_second_innings()
            else:
                self.end_game("tie" if self.player_score == self.computer_score else 
                             ("player" if self.player_score > self.computer_score else "computer"))
    
    def start_second_innings(self):
        if self.player_batting:
            self.target = self.player_score
        else:
            self.target = self.computer_score
        
        msg = f"1st Innings Complete!\n\nTarget: {self.target + 1} runs"
        messagebox.showinfo("Innings Break", msg)
        
        self.innings = 2
        self.balls_played = 0
        self.player_batting = not self.player_batting
        self.game_screen()
    
    def end_game(self, winner):
        self.clear_screen()
        
        result_frame = tk.Frame(self.root, bg="#2d5016")
        result_frame.pack(expand=True)
        
        if winner == "player":
            result_text = "🎉 YOU WON! 🎉"
            result_color = "yellow"
        elif winner == "computer":
            result_text = "😔 COMPUTER WON!"
            result_color = "red"
        else:
            result_text = "🤝 IT'S A TIE!"
            result_color = "orange"
        
        tk.Label(result_frame, text=result_text, font=("Arial", 36, "bold"),
                bg="#2d5016", fg=result_color).pack(pady=30)
        
        tk.Label(result_frame, text=f"Your Score: {self.player_score}/{self.player_wickets}",
                font=("Arial", 20), bg="#2d5016", fg="white").pack(pady=5)
        
        tk.Label(result_frame, text=f"Computer Score: {self.computer_score}/{self.computer_wickets}",
                font=("Arial", 20), bg="#2d5016", fg="white").pack(pady=5)
        
        tk.Button(result_frame, text="PLAY AGAIN", font=("Arial", 16, "bold"),
                 bg="#27ae60", fg="white", width=15, height=2,
                 command=self.reset_game).pack(pady=30)
    
    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_wickets = 0
        self.computer_wickets = 0
        self.balls_played = 0
        self.innings = 1
        self.target = 0
        self.start_screen()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = CricketGame(root)
    root.mainloop()
