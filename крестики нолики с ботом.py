import math
import random
import tkinter as tk


class TicTacToeAI:
    def __init__(self, ai_player="O", human_player="X"):
        self.ai = ai_player
        self.human = human_player

    def get_best_move(self, board, difficulty):
        max_depth = difficulty
        best_score = -math.inf
        best_moves = []
        available_moves = [i for i, cell in enumerate(board) if cell == ""]

        if len(available_moves) == 9:
            return random.choice([4, 0, 2, 6, 8])

        for move in available_moves:
            board[move] = self.ai
            score = self._minimax(board, 0, max_depth, False)
            board[move] = ""

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves) if best_moves else None

    def _check_winner(self, board):
        win_coords = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтали
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикали
            (0, 4, 8), (2, 4, 6)  # Диагонали
        ]
        for c in win_coords:
            if board[c[0]] == board[c[1]] == board[c[2]] != "":
                return board[c[0]]
        if "" not in board:
            return "Tie"
        return None

    def _minimax(self, board, depth, max_depth, is_maximizing):
        winner = self._check_winner(board)
        if winner == self.ai: return 10 - depth
        if winner == self.human: return depth - 10
        if winner == "Tie": return 0
        if depth >= max_depth: return 0

        available_moves = [i for i, cell in enumerate(board) if cell == ""]

        if is_maximizing:
            best_score = -math.inf
            for move in available_moves:
                board[move] = self.ai
                score = self._minimax(board, depth + 1, max_depth, False)
                board[move] = ""
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in available_moves:
                board[move] = self.human
                score = self._minimax(board, depth + 1, max_depth, True)
                board[move] = ""
                best_score = min(score, best_score)
            return best_score


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-Нолики")
        self.root.geometry("400x600")
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)

        # Переменные состояния
        self.board = [""] * 9
        self.human = "X"
        self.ai = "O"
        self.current_player = "X"
        self.scores = {"X": 0, "Tie": 0, "O": 0}
        self.ai_engine = TicTacToeAI(self.ai, self.human)

        # Настройка шрифтов и сочных цветов
        self.font_main = ("Helvetica", 12)
        self.font_title = ("Helvetica", 18, "bold")
        self.color_x = "#ef233c"  # Яркий красный
        self.color_o = "#4361ee"  # Яркий синий

        self._create_start_screen()
        self._create_game_screen()

        self.start_frame.pack(expand=True, fill="both")

    # --- СТАРТОВЫЙ ЭКРАН ---
    def _create_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="#ffffff")

        title = tk.Label(self.start_frame, text="Крестики-нолики", font=("Helvetica", 24, "bold"), bg="#ffffff", fg="#2b2d42")
        title.pack(pady=(200, 20))

        play_btn = tk.Button(
            self.start_frame, text="Играть", font=("Helvetica", 14),
            bg="#f0f0f0", relief="solid", bd=1, width=15, cursor="hand2",
            command=self._start_game
        )
        play_btn.pack()

    def _start_game(self):
        self.start_frame.pack_forget()
        self.game_frame.pack(expand=True, fill="both")

    # --- ИГРОВОЙ ЭКРАН ---
    def _create_game_screen(self):
        self.game_frame = tk.Frame(self.root, bg="#ffffff")

        # Заголовок
        tk.Label(self.game_frame, text="Игрок vs ИИ", font=self.font_title, bg="#ffffff", fg="#2b2d42").pack(pady=(20, 10))

        # Выбор сложности
        tk.Label(self.game_frame, text="Уровень сложности ИИ", font=("Helvetica", 10), fg="#777777",
                 bg="#ffffff").pack()
        diff_frame = tk.Frame(self.game_frame, bg="#ffffff")
        diff_frame.pack(pady=(5, 15))

        self.diff_var = tk.IntVar(value=3)
        for val, text in [(1, "easy"), (2, "normal"), (3, "hard")]:
            tk.Radiobutton(
                diff_frame, text=text, variable=self.diff_var, value=val,
                indicatoron=0, bg="#ffffff", selectcolor="#e6f2ff",
                relief="solid", bd=1, font=("Helvetica", 10), width=8, cursor="hand2"
            ).pack(side="left", padx=5)

        # Счёт
        score_frame = tk.Frame(self.game_frame, bg="#ffffff")
        score_frame.pack(pady=10)

        self.score_labels = {}
        for key, text in [("X", "вы (X)"), ("Tie", "ничья"), ("O", "ИИ (O)")]:
            col = tk.Frame(score_frame, bg="#ffffff")
            col.pack(side="left", padx=15)

            lbl_val = tk.Label(col, text="0", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#2b2d42")
            lbl_val.pack()
            tk.Label(col, text=text, font=("Helvetica", 9), fg="#777777", bg="#ffffff").pack()
            self.score_labels[key] = lbl_val

        # Статус
        self.status_label = tk.Label(self.game_frame, text="Ваш ход — вы играете за X", font=self.font_main,
                                     bg="#ffffff", fg="#2b2d42")
        self.status_label.pack(pady=(10, 20))

        # Игровое поле
        board_container = tk.Frame(self.game_frame, bg="#ffffff")
        board_container.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_container, text="", font=("Helvetica", 28, "bold"),
                bg="#ffffff", activebackground="#f9f9f9", relief="solid", bd=1,
                width=3, height=1, cursor="hand2",
                command=lambda idx=i: self._on_cell_click(idx)
            )
            row, col = i // 3, i % 3
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)

        # Кнопка "Новая игра"
        reset_btn = tk.Button(
            self.game_frame, text="↺ новая игра", font=("Helvetica", 12),
            bg="#f0f0f0", relief="solid", bd=1, width=15, cursor="hand2",
            command=self._reset_game
        )
        reset_btn.pack(pady=30)

    # --- ЛОГИКА ---
    def _on_cell_click(self, index):
        if self.board[index] == "" and self.current_player == self.human:
            self._make_move(index, self.human)
            if not self._check_game_over():
                self.current_player = self.ai
                self.status_label.config(text="Бот думает...", fg="#777777")
                self.root.after(300, self._make_ai_move)

    def _make_move(self, index, player):
        self.board[index] = player
        # Трюк тут: используем disabledforeground, чтобы заблокированная кнопка не серела
        color = self.color_x if player == "X" else self.color_o
        self.buttons[index].config(text=player, state="disabled", disabledforeground=color)

    def _make_ai_move(self):
        ai_move = self.ai_engine.get_best_move(self.board, self.diff_var.get())
        if ai_move is not None:
            self._make_move(ai_move, self.ai)

        if not self._check_game_over():
            self.current_player = self.human
            self.status_label.config(text="Ваш ход — вы играете за X", fg="#2b2d42")

    def _check_game_over(self):
        winner = self.ai_engine._check_winner(self.board)
        if winner:
            self.scores[winner] += 1
            self.score_labels[winner].config(text=str(self.scores[winner]))

            if winner == self.human:
                self.status_label.config(text="Вы победили!", fg="#4CAF50")
            elif winner == self.ai:
                self.status_label.config(text="ИИ победил!", fg="#F44336")
            else:
                self.status_label.config(text="Ничья!", fg="#FF9800")

            for btn in self.buttons:
                btn.config(state="disabled", cursor="arrow")
            return True
        return False

    def _reset_game(self):
        self.board = [""] * 9
        self.current_player = self.human
        self.status_label.config(text="Ваш ход — вы играете за X", fg="#2b2d42")
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="#ffffff", cursor="hand2")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()