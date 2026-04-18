import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def add_stage(ax, x, y, w, h, title, subtitle, face, edge):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=2,
        facecolor=face,
        edgecolor=edge,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h * 0.62,
        title,
        ha="center",
        va="center",
        fontsize=13,
        weight="bold",
        color="#1f2937",
    )
    ax.text(
        x + w / 2,
        y + h * 0.33,
        subtitle,
        ha="center",
        va="center",
        fontsize=10,
        color="#374151",
    )


def add_arrow(ax, x1, y1, x2, y2, color="#0f766e"):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=2.5,
        color=color,
    )
    ax.add_patch(arrow)


def generate_alignment_workflow_figure(output_path):
    fig = plt.figure(figsize=(14, 5.8), facecolor="#f8fafc")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.93,
        "Figure 2. Alignment workflow: Input -> Embedding -> Orthogonal alignment -> Output",
        ha="center",
        va="center",
        fontsize=16,
        weight="bold",
        color="#111827",
    )

    y = 0.28
    w = 0.2
    h = 0.46
    xs = [0.05, 0.29, 0.53, 0.77]

    add_stage(
        ax,
        xs[0],
        y,
        w,
        h,
        "Input",
        "Tokenized Marwari and Hindi corpora\nAnchor lexicon pairs",
        face="#e0f2fe",
        edge="#0284c7",
    )

    add_stage(
        ax,
        xs[1],
        y,
        w,
        h,
        "Embedding",
        "Train monolingual skip-gram vectors\nE_m and E_h in R^(d)",
        face="#ecfccb",
        edge="#65a30d",
    )

    add_stage(
        ax,
        xs[2],
        y,
        w,
        h,
        "Orthogonal Alignment",
        "Solve Procrustes:\nW* = argmin ||W X - Y||_F,  W^T W = I",
        face="#fef3c7",
        edge="#d97706",
    )

    add_stage(
        ax,
        xs[3],
        y,
        w,
        h,
        "Output",
        "Aligned Marwari vectors\nE_m_aligned = W E_m",
        face="#fee2e2",
        edge="#dc2626",
    )

    mid_y = y + h * 0.5
    add_arrow(ax, xs[0] + w, mid_y, xs[1] - 0.01, mid_y)
    add_arrow(ax, xs[1] + w, mid_y, xs[2] - 0.01, mid_y)
    add_arrow(ax, xs[2] + w, mid_y, xs[3] - 0.01, mid_y)

    ax.text(0.39, 0.16, "learn E_m, E_h", fontsize=10, color="#065f46", ha="center")
    ax.text(0.63, 0.16, "estimate orthogonal map W*", fontsize=10, color="#065f46", ha="center")
    ax.text(0.87, 0.16, "shared-space retrieval", fontsize=10, color="#065f46", ha="center")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=260, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    out_file = os.path.join(here, "figures", "alignment_workflow.png")
    generate_alignment_workflow_figure(out_file)
    print(f"Saved: {out_file}")
