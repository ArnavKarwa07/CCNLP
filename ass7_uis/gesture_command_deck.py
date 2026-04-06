import tkinter as tk


class GestureCommandDeck:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Command Deck")
        self.root.geometry("1100x680")
        self.root.configure(bg="#111111")

        self.header = tk.Frame(root, bg="#1b1b1b", height=90)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        tk.Label(
            self.header,
            text="GESTURE COMMAND DECK",
            bg="#1b1b1b",
            fg="#f0f0f0",
            font=("Bahnschrift", 28, "bold"),
        ).pack(pady=(14, 0))

        tk.Label(
            self.header,
            text="UI concept: trigger actions from radial gesture tiles",
            bg="#1b1b1b",
            fg="#9fb4c7",
            font=("Bahnschrift", 12),
        ).pack()

        self.main = tk.Frame(root, bg="#111111")
        self.main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main, bg="#111111", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.side = tk.Frame(self.main, bg="#191919", width=320)
        self.side.pack(side="right", fill="y", padx=(0, 20), pady=20)
        self.side.pack_propagate(False)

        tk.Label(
            self.side,
            text="ACTION LOG",
            bg="#191919",
            fg="#eceff1",
            font=("Bahnschrift", 16, "bold"),
        ).pack(pady=(18, 8))

        self.log_box = tk.Text(
            self.side,
            bg="#0f1418",
            fg="#b8d6f2",
            font=("Consolas", 10),
            bd=0,
            height=24,
            width=32,
        )
        self.log_box.pack(padx=16, pady=8)
        self.log_box.insert("end", "System ready.\n")

        self._draw_command_wheel()

    def _draw_command_wheel(self):
        cx, cy = 360, 280
        self.canvas.create_oval(cx - 70, cy - 70, cx + 70, cy + 70, fill="#2d3436", outline="#95a5a6", width=2)
        self.canvas.create_text(cx, cy, text="NLP Hub", fill="#ecf0f1", font=("Bahnschrift", 14, "bold"))

        tiles = [
            ("Parse", -200, -90, "#00cec9"),
            ("Cluster", 0, -170, "#0984e3"),
            ("Prompt", 200, -90, "#6c5ce7"),
            ("Summarize", 200, 90, "#fdcb6e"),
            ("Translate", 0, 170, "#00b894"),
            ("Analyze", -200, 90, "#ff7675"),
        ]

        for name, dx, dy, color in tiles:
            x = cx + dx
            y = cy + dy
            rect = self.canvas.create_rectangle(x - 85, y - 48, x + 85, y + 48, fill=color, outline="")
            text = self.canvas.create_text(x, y, text=name, fill="#1b1b1b", font=("Bahnschrift", 13, "bold"))

            self.canvas.tag_bind(rect, "<Button-1>", lambda e, n=name: self.log_action(n))
            self.canvas.tag_bind(text, "<Button-1>", lambda e, n=name: self.log_action(n))

            self.canvas.create_line(cx, cy, x, y, fill="#576574", width=2)

        self.status = tk.Label(
            self.side,
            text="Tap any tile",
            bg="#191919",
            fg="#dfe6e9",
            font=("Bahnschrift", 12),
        )
        self.status.pack(pady=(8, 10))

    def log_action(self, action):
        self.log_box.insert("end", f"> {action} gesture triggered\n")
        self.log_box.see("end")
        self.status.config(text=f"Last action: {action}")


if __name__ == "__main__":
    app_root = tk.Tk()
    GestureCommandDeck(app_root)
    app_root.mainloop()
