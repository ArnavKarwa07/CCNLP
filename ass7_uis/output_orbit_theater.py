import tkinter as tk
import random
import math


class OutputOrbitTheater:
    def __init__(self, root):
        self.root = root
        self.root.title("Output Orbit Theater")
        self.root.geometry("1100x680")
        self.root.configure(bg="#12121a")

        self.canvas = tk.Canvas(root, bg="#12121a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            550,
            52,
            text="OUTPUT ORBIT THEATER",
            fill="#ffcc70",
            font=("Georgia", 30, "bold"),
        )
        self.canvas.create_text(
            550,
            87,
            text="Watch model outputs move like planets around focus nodes",
            fill="#ffcfa8",
            font=("Georgia", 12),
        )

        self.center_x = 550
        self.center_y = 360
        self.canvas.create_oval(500, 310, 600, 410, fill="#4a2f1e", outline="#ff9f43", width=3)
        self.canvas.create_text(550, 360, text="Core", fill="#ffe8cc", font=("Georgia", 14, "bold"))

        self.outputs = []
        self._create_output_nodes()

        controls = tk.Frame(root, bg="#12121a")
        self.canvas.create_window(550, 620, window=controls)

        self.info = tk.Label(
            controls,
            text="Orbit velocity: moderate",
            bg="#12121a",
            fg="#ffcc70",
            font=("Georgia", 11),
        )
        self.info.grid(row=0, column=0, padx=8)

        tk.Button(
            controls,
            text="Generate",
            bg="#e17055",
            fg="white",
            font=("Georgia", 10, "bold"),
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.randomize_outputs,
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            controls,
            text="Slow",
            bg="#6c5ce7",
            fg="white",
            font=("Georgia", 10, "bold"),
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.change_speed(0.008),
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            controls,
            text="Fast",
            bg="#00b894",
            fg="white",
            font=("Georgia", 10, "bold"),
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.change_speed(0.03),
        ).grid(row=0, column=3, padx=8)

        self.bg_stars = []
        for _ in range(120):
            x = random.randint(0, 1100)
            y = random.randint(0, 680)
            s = random.randint(1, 2)
            star = self.canvas.create_oval(x, y, x + s, y + s, fill="#f5f6fa", outline="")
            self.bg_stars.append(star)

        self.animate()

    def _create_output_nodes(self):
        labels = ["Sentiment", "Topic", "Summary", "Entities", "Intent", "Keywords"]
        colors = ["#fdcb6e", "#74b9ff", "#55efc4", "#fab1a0", "#a29bfe", "#ffeaa7"]

        for i, label in enumerate(labels):
            radius = 130 + (i % 3) * 55
            angle = i * (math.pi / 3)
            speed = 0.015 + (i % 2) * 0.01
            x = self.center_x + radius * math.cos(angle)
            y = self.center_y + radius * math.sin(angle)
            node = self.canvas.create_oval(x - 26, y - 26, x + 26, y + 26, fill=colors[i], outline="")
            text = self.canvas.create_text(x, y, text=label, fill="#2d3436", font=("Segoe UI", 9, "bold"))
            self.outputs.append(
                {
                    "node": node,
                    "text": text,
                    "radius": radius,
                    "angle": angle,
                    "speed": speed,
                }
            )

    def randomize_outputs(self):
        palette = ["#fdcb6e", "#74b9ff", "#55efc4", "#fab1a0", "#a29bfe", "#ffeaa7", "#ff7675"]
        for out in self.outputs:
            self.canvas.itemconfig(out["node"], fill=random.choice(palette))
        self.info.config(text="Output style regenerated")

    def change_speed(self, value):
        for out in self.outputs:
            out["speed"] = value + random.uniform(0, 0.01)
        self.info.config(text=f"Orbit velocity: {('slow' if value < 0.01 else 'fast')}")

    def animate(self):
        for out in self.outputs:
            out["angle"] += out["speed"]
            x = self.center_x + out["radius"] * math.cos(out["angle"])
            y = self.center_y + out["radius"] * math.sin(out["angle"])
            self.canvas.coords(out["node"], x - 26, y - 26, x + 26, y + 26)
            self.canvas.coords(out["text"], x, y)

        for star in self.bg_stars[::6]:
            if random.random() > 0.6:
                self.canvas.itemconfig(star, fill=random.choice(["#f5f6fa", "#ffeaa7", "#fdcb6e"]))

        self.root.after(30, self.animate)


if __name__ == "__main__":
    app_root = tk.Tk()
    OutputOrbitTheater(app_root)
    app_root.mainloop()
