import tkinter as tk
from tkinter import ttk
import math


class HologramUploadScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Hologram Data Upload")
        self.root.geometry("1100x680")
        self.root.configure(bg="#04111f")

        self.canvas = tk.Canvas(root, bg="#04111f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.title_text = self.canvas.create_text(
            550,
            70,
            text="HOLOGRAM DATA HARBOR",
            fill="#7ef9ff",
            font=("Consolas", 28, "bold"),
        )
        self.subtitle_text = self.canvas.create_text(
            550,
            110,
            text="Drop zones and upload controls in a sci-fi control room",
            fill="#82c9ff",
            font=("Consolas", 12),
        )

        panel = tk.Frame(root, bg="#0a1b2e", bd=0)
        self.panel_window = self.canvas.create_window(550, 385, window=panel, width=820, height=420)

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)

        self._make_zone(panel, 0, "Corpus .csv", "Ready")
        self._make_zone(panel, 1, "Embeddings .json", "Waiting")
        self._make_zone(panel, 2, "Metadata .txt", "Ready")
        self._make_zone(panel, 3, "Experiment Notes", "Optional")

        controls = tk.Frame(panel, bg="#0a1b2e")
        controls.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)
        controls.grid_columnconfigure(2, weight=1)

        self.btn_scan = tk.Button(
            controls,
            text="SCAN FILES",
            font=("Consolas", 12, "bold"),
            bg="#005f73",
            fg="#e3feff",
            bd=0,
            padx=16,
            pady=9,
            cursor="hand2",
            command=lambda: self.set_status("Scanning directories... (UI demo)"),
        )
        self.btn_lock = tk.Button(
            controls,
            text="LOCK BATCH",
            font=("Consolas", 12, "bold"),
            bg="#7b2cbf",
            fg="#f6ecff",
            bd=0,
            padx=16,
            pady=9,
            cursor="hand2",
            command=lambda: self.set_status("Batch locked. Ready for processing.")
        )
        self.btn_reset = tk.Button(
            controls,
            text="RESET",
            font=("Consolas", 12, "bold"),
            bg="#9b2226",
            fg="#ffeded",
            bd=0,
            padx=16,
            pady=9,
            cursor="hand2",
            command=lambda: self.set_status("Panels reset.")
        )

        self.btn_scan.grid(row=0, column=0, padx=8, sticky="ew")
        self.btn_lock.grid(row=0, column=1, padx=8, sticky="ew")
        self.btn_reset.grid(row=0, column=2, padx=8, sticky="ew")

        self.progress = ttk.Progressbar(panel, mode="indeterminate", length=740)
        self.progress.grid(row=3, column=0, columnspan=2, pady=(18, 0))
        self.progress.start(15)

        self.status = tk.Label(
            panel,
            text="All systems idle",
            bg="#0a1b2e",
            fg="#9ed8ff",
            font=("Consolas", 11),
        )
        self.status.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        self.ring_items = []
        self.theta = 0
        self._create_hud_rings()
        self.animate_hud()

    def _make_zone(self, panel, idx, title, state):
        row = idx // 2
        col = idx % 2

        zone = tk.Frame(panel, bg="#102944", bd=0)
        zone.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        panel.grid_rowconfigure(row, weight=1)

        tk.Label(zone, text=title, font=("Consolas", 13, "bold"), bg="#102944", fg="#7ef9ff").pack(pady=(12, 6))
        tk.Label(zone, text="Tap to simulate upload", bg="#102944", fg="#b7d8f7", font=("Consolas", 10)).pack()

        status_label = tk.Label(zone, text=f"Status: {state}", bg="#102944", fg="#6ef3d6", font=("Consolas", 10, "bold"))
        status_label.pack(pady=(8, 10))

        tk.Button(
            zone,
            text="UPLOAD",
            font=("Consolas", 10, "bold"),
            bg="#136f63",
            fg="#ebfffe",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda s=status_label: self._simulate_upload(s),
        ).pack(pady=(0, 12))

    def _simulate_upload(self, label):
        label.config(text="Status: Uploaded", fg="#a8ff78")
        self.set_status("One slot updated.")

    def set_status(self, text):
        self.status.config(text=text)

    def _create_hud_rings(self):
        center_x, center_y = 940, 110
        for radius in (24, 36, 48):
            item = self.canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline="#1f8fcf",
                width=2,
            )
            self.ring_items.append((item, radius))

    def animate_hud(self):
        self.theta += 0.12
        center_x, center_y = 940, 110
        for item, radius in self.ring_items:
            wobble = 3 * math.sin(self.theta + radius)
            self.canvas.coords(
                item,
                center_x - radius - wobble,
                center_y - radius - wobble,
                center_x + radius + wobble,
                center_y + radius + wobble,
            )
        self.root.after(50, self.animate_hud)


if __name__ == "__main__":
    app_root = tk.Tk()
    HologramUploadScreen(app_root)
    app_root.mainloop()
