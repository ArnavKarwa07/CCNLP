import os
import numpy as np
import matplotlib.pyplot as plt


FIG_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name), dpi=220, bbox_inches="tight")
    plt.close(fig)


# Verified from notebook outputs
langs = ["English", "Hindi", "Marwari"]
sentence_counts = np.array([264, 413, 449])
vocab_counts = np.array([1200, 1194, 1200])

x = np.arange(len(langs))
w = 0.36
fig, ax = plt.subplots(figsize=(8.8, 4.8))
ax.bar(x - w / 2, sentence_counts, width=w, label="Sentences", color="#1f77b4")
ax.bar(x + w / 2, vocab_counts, width=w, label="Vocabulary", color="#ff7f0e")
ax.set_xticks(x)
ax.set_xticklabels(langs)
ax.set_ylabel("Count")
ax.set_title("Corpus Profile from Notebook Run")
ax.legend()
ax.grid(axis="y", alpha=0.25, linestyle="--")
for i, v in enumerate(sentence_counts):
    ax.text(i - w / 2, v + 8, str(int(v)), ha="center", va="bottom", fontsize=8)
for i, v in enumerate(vocab_counts):
    ax.text(i + w / 2, v + 8, str(int(v)), ha="center", va="bottom", fontsize=8)
save(fig, "verified_corpus_profile.png")


triples = np.array([519864, 71010, 71982])
fig, ax = plt.subplots(figsize=(8.8, 4.8))
bars = ax.bar(langs, triples, color=["#2ca02c", "#1f77b4", "#d62728"])
ax.set_ylabel("Number of training triples")
ax.set_title("Skip-gram Training Triples from Notebook Run")
ax.grid(axis="y", alpha=0.25, linestyle="--")
for b in bars:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width() / 2, h + 5000, f"{int(h):,}", ha="center", va="bottom", fontsize=8)
save(fig, "verified_training_triples.png")


# Final training losses from notebook output
loss_labels = ["English", "Hindi", "Marwari"]
final_losses = np.array([0.2108194530, 0.0020246829, 0.0020964979])
fig, ax = plt.subplots(figsize=(8.8, 4.8))
bars = ax.bar(loss_labels, final_losses, color=["#ff7f0e", "#1f77b4", "#2ca02c"])
ax.set_ylabel("Final BCE loss")
ax.set_title("Final Training Loss by Language (Notebook Run)")
ax.grid(axis="y", alpha=0.25, linestyle="--")
for b, val in zip(bars, final_losses):
    ax.text(b.get_x() + b.get_width() / 2, val + 0.005, f"{val:.4f}", ha="center", va="bottom", fontsize=8)
save(fig, "verified_final_losses.png")


# Isotropy statistics from notebook output table
spaces = ["English", "Hindi", "Marwari", "Marwari Aligned"]
anis = np.array([1.360415, 1.318598, 1.333987, 1.333987])
iso = np.array([0.735070, 0.758381, 0.749633, 0.749633])

fig, ax1 = plt.subplots(figsize=(9.2, 4.8))
line1 = ax1.plot(spaces, anis, marker="o", linewidth=2, color="#d62728", label="Anisotropy ratio")
ax1.set_ylabel("Anisotropy ratio", color="#d62728")
ax1.tick_params(axis="y", labelcolor="#d62728")
ax1.set_title("Isotropy/Anisotropy Diagnostics (Notebook Run)")
ax1.grid(axis="y", alpha=0.25, linestyle="--")

ax2 = ax1.twinx()
line2 = ax2.plot(spaces, iso, marker="s", linewidth=2, color="#1f77b4", label="Isotropy index")
ax2.set_ylabel("Isotropy index", color="#1f77b4")
ax2.tick_params(axis="y", labelcolor="#1f77b4")

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right")
save(fig, "verified_isotropy_anisotropy.png")


# Retrieval R@1 dict before/after from notebook table
metrics = ["euclidean", "cosine", "angular", "hyperbolic"]
r1_before = np.array([0.005882, 0.011765, 0.011765, 0.011765])
r1_after = np.array([0.094118, 0.135294, 0.135294, 0.005882])

x = np.arange(len(metrics))
fig, ax = plt.subplots(figsize=(9.2, 4.8))
ax.bar(x - w / 2, r1_before, width=w, label="Before", color="#9ecae1")
ax.bar(x + w / 2, r1_after, width=w, label="After", color="#fdae6b")
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylim(0, 0.18)
ax.set_ylabel("Dictionary-constrained R@1")
ax.set_title("Cross-Lingual Retrieval R@1 (Notebook Run)")
ax.legend()
ax.grid(axis="y", alpha=0.25, linestyle="--")
save(fig, "verified_retrieval_r1_dict.png")

print("Generated verified figures.")
