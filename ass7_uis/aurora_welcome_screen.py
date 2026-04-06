import tkinter as tk
import random
import math


class AuroraWelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Aurora Welcome Screen")
        self.root.geometry("1100x680")
        self.root.configure(bg="#070b1a")

        self.canvas = tk.Canvas(root, bg="#070b1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.width = 1100
        self.height = 680
        self.cursor_x = self.width / 2
        self.cursor_y = self.height / 2
        self.prev_cursor_x = self.cursor_x
        self.prev_cursor_y = self.cursor_y
        self.cursor_dx = 0
        self.cursor_dy = 0

        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.starfield = []
        self.mesh_rows = []
        self.mesh_cols = []
        self.nebula_clouds = []

        self._create_nebula()
        self._create_spacetime_mesh()
        self._create_starfield(160)

        self.cursor_halo = self.canvas.create_oval(
            self.cursor_x - 85,
            self.cursor_y - 85,
            self.cursor_x + 85,
            self.cursor_y + 85,
            outline="#2c8fcc",
            width=2,
        )
        self.cursor_ring = self.canvas.create_oval(
            self.cursor_x - 32,
            self.cursor_y - 32,
            self.cursor_x + 32,
            self.cursor_y + 32,
            outline="#63d6ff",
            width=2,
        )

        self.heading = self.canvas.create_text(
            550,
            220,
            text="NLP LAB EXPERIENCE",
            fill="#d8f2ff",
            font=("Segoe UI", 42, "bold"),
        )
        self.subheading = self.canvas.create_text(
            550,
            280,
            text="Space-time fabric responds to your cursor",
            fill="#7fc4ff",
            font=("Segoe UI", 16),
        )

        self.start_button = tk.Button(
            root,
            text="ENTER STUDIO",
            font=("Segoe UI", 14, "bold"),
            bg="#0a3d62",
            fg="#e8f7ff",
            activebackground="#145a86",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.flash_message,
        )
        self.btn_window = self.canvas.create_window(550, 370, window=self.start_button)

        self.status = self.canvas.create_text(
            550,
            430,
            text="Move cursor to warp space-time",
            fill="#7fd3ff",
            font=("Segoe UI", 12),
        )

        self.wave_offset = 0
        self.animate()

    def _create_nebula(self):
        for _ in range(7):
            x = random.randint(-120, self.width + 120)
            y = random.randint(-100, self.height + 100)
            r = random.randint(120, 230)
            color = random.choice(["#091a33", "#10203f", "#15264a", "#0b2142"])
            cloud = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
            vx = random.uniform(-0.06, 0.06)
            vy = random.uniform(-0.06, 0.06)
            self.nebula_clouds.append({"id": cloud, "x": x, "y": y, "r": r, "vx": vx, "vy": vy})

    def _create_spacetime_mesh(self):
        row_spacing = 48
        col_spacing = 48

        for y in range(0, self.height + row_spacing, row_spacing):
            line = self.canvas.create_line(0, y, self.width, y, fill="#173153", width=1)
            self.mesh_rows.append({"id": line, "base": y})

        for x in range(0, self.width + col_spacing, col_spacing):
            line = self.canvas.create_line(x, 0, x, self.height, fill="#173153", width=1)
            self.mesh_cols.append({"id": line, "base": x})

    def _create_starfield(self, count):
        for _ in range(count):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            depth = random.uniform(0.35, 1.25)
            size = 1 + depth * 1.8
            color = random.choice(["#b9deff", "#d0c7ff", "#7cdfff", "#e4fbff"])
            item = self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            drift = random.uniform(-0.09, 0.09)
            self.starfield.append(
                {
                    "id": item,
                    "x": x,
                    "y": y,
                    "size": size,
                    "depth": depth,
                    "drift": drift,
                }
            )

    def on_mouse_move(self, event):
        self.cursor_dx = event.x - self.prev_cursor_x
        self.cursor_dy = event.y - self.prev_cursor_y
        self.cursor_x = event.x
        self.cursor_y = event.y
        self.prev_cursor_x = event.x
        self.prev_cursor_y = event.y

    def flash_message(self):
        self.canvas.itemconfig(self.status, text="Portal engaged. Visual mode only.", fill="#9effd4")

    def animate(self):
        self.wave_offset += 0.06

        for cloud in self.nebula_clouds:
            cloud["x"] += cloud["vx"] - self.cursor_dx * 0.005
            cloud["y"] += cloud["vy"] - self.cursor_dy * 0.005

            if cloud["x"] < -200:
                cloud["x"] = self.width + 200
            if cloud["x"] > self.width + 200:
                cloud["x"] = -200
            if cloud["y"] < -180:
                cloud["y"] = self.height + 180
            if cloud["y"] > self.height + 180:
                cloud["y"] = -180

            r = cloud["r"]
            self.canvas.coords(cloud["id"], cloud["x"] - r, cloud["y"] - r, cloud["x"] + r, cloud["y"] + r)

        segment = 22
        lens_strength = 360

        for row in self.mesh_rows:
            y0 = row["base"]
            points = []
            for x in range(0, self.width + segment, segment):
                dx = x - self.cursor_x
                dy = y0 - self.cursor_y
                dist2 = dx * dx + dy * dy + 2000
                pull = lens_strength / dist2
                wave = 4 * math.sin(self.wave_offset + x * 0.012 + y0 * 0.01)
                xw = x - dx * pull
                yw = y0 - dy * pull + wave
                points.extend([xw, yw])
            self.canvas.coords(row["id"], *points)

        for col in self.mesh_cols:
            x0 = col["base"]
            points = []
            for y in range(0, self.height + segment, segment):
                dx = x0 - self.cursor_x
                dy = y - self.cursor_y
                dist2 = dx * dx + dy * dy + 2000
                pull = lens_strength / dist2
                wave = 4 * math.cos(self.wave_offset + y * 0.012 + x0 * 0.01)
                xw = x0 - dx * pull + wave
                yw = y - dy * pull
                points.extend([xw, yw])
            self.canvas.coords(col["id"], *points)

        for star in self.starfield:
            star["x"] += star["drift"] * star["depth"] - self.cursor_dx * 0.017 * star["depth"]
            star["y"] += -self.cursor_dy * 0.017 * star["depth"]

            if star["x"] < -8:
                star["x"] = self.width + 8
            if star["x"] > self.width + 8:
                star["x"] = -8
            if star["y"] < -8:
                star["y"] = self.height + 8
            if star["y"] > self.height + 8:
                star["y"] = -8

            jitter = 0.25 * math.sin(self.wave_offset * 2 + star["x"] * 0.03)
            s = star["size"] + jitter
            self.canvas.coords(star["id"], star["x"], star["y"], star["x"] + s, star["y"] + s)

        pulse = int(200 + 55 * (1 + __import__("math").sin(self.wave_offset)))
        pulse = max(0, min(255, pulse))
        glow_color = f"#{pulse:02x}f0ff"
        self.canvas.itemconfig(self.heading, fill=glow_color)

        halo_r = 80 + 12 * math.sin(self.wave_offset * 2.4)
        ring_r = 30 + 6 * math.cos(self.wave_offset * 3.1)
        self.canvas.coords(
            self.cursor_halo,
            self.cursor_x - halo_r,
            self.cursor_y - halo_r,
            self.cursor_x + halo_r,
            self.cursor_y + halo_r,
        )
        self.canvas.coords(
            self.cursor_ring,
            self.cursor_x - ring_r,
            self.cursor_y - ring_r,
            self.cursor_x + ring_r,
            self.cursor_y + ring_r,
        )

        speed = min(999, int((self.cursor_dx * self.cursor_dx + self.cursor_dy * self.cursor_dy) ** 0.5 * 12))
        self.canvas.itemconfig(self.status, text=f"Space-time flux: {speed}")

        self.cursor_dx *= 0.85
        self.cursor_dy *= 0.85

        self.root.after(40, self.animate)


if __name__ == "__main__":
    app_root = tk.Tk()
    AuroraWelcomeScreen(app_root)
    app_root.mainloop()
