import time
import tkinter as tk
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import zhmiscellany


def center_window(root, width=400, height=500):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


def load_stats():
    if os.path.exists("stats.txt"):
        with open("stats.txt", "r") as f:
            data = f.read().split()
            return int(data[0])  # best game
    return 0


def save_stats():
    with open("stats.txt", "w") as f:
        f.write(f"{best_game}")


def generate_unique_colors():
    return random.sample(["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan", "brown"], 9)


def start_new_round():
    global colors, target_color, target_position, revealed
    colors = generate_unique_colors()
    target_position = random.randint(0, 8)
    target_color = colors[target_position]
    revealed = False
    root.after(1000, show_colours)


def show_colours():
    global colors, target_color, target_position, revealed
    for i, button in enumerate(buttons):
        button.config(bg=colors[i], state=tk.DISABLED)
    
    root.after(1000, hide_colors)


def hide_colors():
    for button in buttons:
        button.config(bg="lightgrey", state=tk.NORMAL)
    info_label.config(text=f"Click the square where {target_color} was!")


def check_choice(index):
    global revealed, wins, losses, win_streak, best_streak, round
    if revealed:
        return
    
    for button in buttons:
        button.config(state=tk.DISABLED)
    
    if index == target_position:
        info_label.config(text="Correct! Starting new round...")
        pygame.mixer.Sound("pop_noise.mp3").play()
        wins += 1
        win_streak += 1
        if win_streak > best_streak:
            best_streak = win_streak
    else:
        info_label.config(text=f"Wrong! The correct spot was highlighted.")
        pygame.mixer.Sound("keh_noise.mp3").play()
        losses += 1
        win_streak = 0
    
    buttons[target_position].config(bg=target_color)
    revealed = True
    round += 1
    end_game = False
    if round > rounds:
        end_game = True
        round -= 1
    update_stats()
    if end_game:
        root.after(1000, end_game_screen)
    else:
        root.after(1000, start_new_round)


def update_stats():
    stats_label.config(text=gen_stat_string())

def gen_stat_string():
    return f"""Wins: {wins} | Losses: {losses} | Win rate {zhmiscellany.math.smart_percentage(wins, wins + losses)}%
Streak: {win_streak} | Best Streak: {best_streak}
Game {round}/{rounds}"""

def end_game_screen():
    global best_game
    hide_colors()
    info_label.config(text='')
    best_game_string = ' | '
    best_game_string += f'Game score: {wins}/{rounds} | high score: {best_game}/{rounds}'
    if wins > best_game:
        best_game_string += f'\nYou beat your high score by {wins - best_game}.'
        best_game = wins
    stats_label.config(text=f'Final game stats:\n{gen_stat_string()}{best_game_string}')
    save_stats()

root = tk.Tk()
root.title("Color Memory Game")
center_window(root, 400, 400)

pygame.mixer.init()

wins, losses, best_streak = 0, 0, 0
best_game = load_stats()
win_streak = 0

top_frame = tk.Frame(root)
top_frame.pack()
info_label = tk.Label(top_frame, text="Memorize the colors!", font=("Arial", 14))
info_label.pack()

grid_frame = tk.Frame(root)
grid_frame.pack()
buttons = []

for i in range(3):
    for j in range(3):
        btn = tk.Button(grid_frame, width=10, height=5, command=lambda idx=len(buttons): check_choice(idx))
        btn.grid(row=i, column=j)
        buttons.append(btn)

stats_frame = tk.Frame(root)
stats_frame.pack()
stats_label = tk.Label(stats_frame, text="", font=("Arial", 12))
stats_label.pack()

rounds = 25
round = 1

update_stats()
start_new_round()
root.mainloop()
