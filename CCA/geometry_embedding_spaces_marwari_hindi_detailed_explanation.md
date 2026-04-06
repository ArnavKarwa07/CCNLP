# Detailed Walkthrough: Geometry of Embedding Spaces for Multilingual Low-Resource NLP (Marwari-Hindi-English)

## Quick Cheat Sheet: How to Read Results Fast

Use this section when you need a 1-2 minute interpretation of notebook outputs.

1. Start with the alignment quality table and bar plot:

- Look for `acc_after > acc_before` across metrics.
- If hyperbolic has values and meaningful gain, the geometric comparison is functioning correctly.

2. Check singular value spectrum:

- If one line is missing, it means overlap or style conflict; in this notebook Marwari is forced to be visually distinct.
- A steeper drop usually indicates stronger anisotropy (few dominant directions).

3. Check anisotropy/isotropy table:

- `anisotropy_ratio` higher means more collapse.
- `isotropy_index` higher means more balanced directional spread.
- `delta_*_vs_marwari` tells whether Hindi/English/aligned Marwari are better or worse than Marwari baseline.

4. Read geometry comparison charts in order:

- Euclidean PCA and t-SNE: global and local neighborhood structure.
- Spherical PCA: direction-only geometry after norm removal.
- Hyperbolic PCA: hierarchy-friendly geometry behavior.

5. Interpret Marwari->Hindi heatmaps:

- Before: baseline cross-lingual similarity.
- After: alignment effect.
- Gain: direct improvement map (positive regions are where alignment helped).

6. Final sanity checks:

- Monolingual nearest neighbors should look semantically coherent.
- Cross-lingual nearest neighbors should improve after alignment.
- The same trends should appear in both qualitative examples and retrieval@1 metrics.

## 1) What this project is trying to do

This notebook is a research-style prototype that studies one central question:

How does geometry (Euclidean, spherical, hyperbolic) affect multilingual word embedding behavior, especially for a low-resource language (Marwari), when compared with Hindi and English?

The workflow is not just model training. It combines:

- mathematical theory
- corpus preparation
- embedding learning
- geometric distance analysis
- cross-lingual alignment
- isotropy/anisotropy diagnostics
- visual and quantitative evaluation

Marwari is treated as the main reference language in the analysis sections, with Hindi and English used as comparisons.

---

## 2) Core NLP and geometry concepts from first principles

### 2.1 What is an embedding?

A word embedding is a dense vector representation of a token.

Instead of representing a word as a huge sparse one-hot vector, we represent it as a compact continuous vector:

- word: "कुत्ता"
- embedding: a vector in \(\mathbb{R}^d\), for example 24 dimensions

Words that occur in similar contexts tend to end up close in embedding space.

### 2.2 Why geometry matters

If embeddings are vectors, then semantics are interpreted by geometry:

- closeness
- angle
- direction
- curvature-aware distance

Different geometric assumptions emphasize different structures.

### 2.3 Euclidean geometry

Standard flat geometry. Distance is:

\[
d_E(\mathbf{x},\mathbf{y}) = \|\mathbf{x}-\mathbf{y}\|\_2
\]

Good default. But can be less suitable for directional semantics or hierarchical structure.

### 2.4 Cosine similarity and spherical view

Cosine similarity compares direction, not magnitude:

\[
\cos(\mathbf{x},\mathbf{y}) = \frac{\mathbf{x}^\top\mathbf{y}}{\|\mathbf{x}\|\,\|\mathbf{y}\|}
\]

If vectors are normalized to unit norm (on a sphere), then cosine becomes plain dot product:

\[
\hat{\mathbf{x}}^\top\hat{\mathbf{y}} = \cos(\theta)
\]

This is useful when direction encodes semantics better than vector length.

### 2.5 Angular distance

Angular distance is the geodesic interpretation on the sphere:

\[
d\_{\angle}(\mathbf{x},\mathbf{y}) = \arccos(\cos(\mathbf{x},\mathbf{y}))
\]

### 2.6 Hyperbolic geometry (Poincare ball)

Hyperbolic space has negative curvature and can model tree-like/hierarchical structure better.

In Poincare ball coordinates (inside unit disk/ball), the distance is:

\[
d\_{\mathbb{B}}(\mathbf{u},\mathbf{v}) = \operatorname{arcosh}\left(1 + \frac{2\|\mathbf{u}-\mathbf{v}\|^2}{(1-\|\mathbf{u}\|^2)(1-\|\mathbf{v}\|^2)}\right)
\]

Intuition: space expands faster near boundary, giving more room for branching hierarchies.

### 2.7 Isotropy and anisotropy

A good embedding space should spread information across directions.

- isotropic: information distributed relatively evenly
- anisotropic: vectors collapse into a few dominant directions

The notebook measures anisotropy via singular values and directional variance.

---

## 3) Data pipeline and corpora

The notebook uses pre-existing corpora (not synthetic):

- English: Brown + IEER corpora from NLTK
- Hindi: Indian corpus (hindi.pos) from NLTK
- Marwari/Rajasthani proxy: ULCA Rajasthani text parquet shard from Hugging Face

### 3.1 Why language prefixes are added

Tokens are prefixed to keep language vocabularies separate:

- en_word
- hi_word
- mr_word

This avoids accidental collisions and preserves language identity throughout training/evaluation.

### 3.2 Preprocessing steps

- lowercase normalization
- regex cleanup (retain Latin and Devanagari ranges)
- sentence/token extraction
- frequency-based vocabulary capping
- filtering too-short tokenized sentences

---

## 4) Training objective and model design

### 4.1 Skip-gram-style pairs

From each sentence, target-context windows generate positive pairs.

Negative pairs are sampled from vocabulary entries that were not observed as positive context for the target.

This gives training tuples:

- target_id
- context_id
- label in {0,1}

### 4.2 Keras model architecture

For each language independently:

- Input target token ID
- Input context token ID
- Two embedding layers (target and context)
- Dot product
- Sigmoid output
- Binary cross-entropy loss

This approximates a negative-sampling skip-gram objective.

---

## 5) Geometry functions implemented

The notebook implements reusable functions for:

- \(L_2\) norm and row normalization
- Euclidean distance
- cosine similarity
- angular distance
- projection into Poincare ball
- hyperbolic distance in Poincare model
- pairwise metric matrix construction

These functions are then used consistently across analyses.

---

## 6) Spherical and hyperbolic analyses

### 6.1 Spherical

Embeddings are normalized to unit length and compared by angle/cosine.

### 6.2 Hyperbolic

Embeddings are projected to Poincare ball as an approximation for hyperbolic analysis.

A toy hierarchy is included to demonstrate why hyperbolic geometry is useful for parent-child-sibling structures.

---

## 7) What exactly is aligned in multilingual alignment

This is critical.

The notebook aligns vector spaces, not raw text.

### 7.1 Source and target spaces

- Marwari embedding matrix: \(E\_{mr}\)
- Hindi embedding matrix: \(E\_{hi}\)

Using bilingual anchor pairs, it constructs:

- \(X\): Marwari anchor vectors
- \(Y\): Hindi anchor vectors

### 7.2 Optimization solved

Orthogonal Procrustes:

\[
W^\* = \arg\min\_{W^\top W = I}\|WX - Y\|\_F
\]

### 7.3 Closed-form solution

Compute SVD:

\[
YX^\top = U\Sigma V^\top
\]

Then:

\[
W^\* = UV^\top
\]

### 7.4 Applying alignment

All Marwari embeddings are mapped into Hindi coordinates:

\[
\tilde{E}_{mr} = (W E_{mr}^\top)^\top
\]

So cross-lingual nearest-neighbor comparisons become meaningful in a shared frame.

---

## 8) Isotropy/anisotropy diagnostics in this notebook

For each space:

1. compute mean vector norm
2. center embedding matrix
3. compute singular values
4. compute anisotropy ratio:

\[
\text{anisotropy ratio} = \frac{\sigma\_{max}}{\text{mean}(\sigma)}
\]

5. compute isotropy index:

\[
\text{isotropy index} = \frac{1}{\text{anisotropy ratio}}
\]

6. sample random directions and measure projection variances

The notebook also includes delta columns vs Marwari baseline.

---

## 9) Visualization strategy (and why each exists)

The notebook now uses separate cell blocks for each graph.

### 9.1 Euclidean views

- PCA (all three languages)
- t-SNE (all three languages)
- PCA (Marwari aligned vs Hindi)

Purpose: observe global geometry and neighborhood separation under flat metric assumptions.

### 9.2 Spherical view

- PCA on normalized vectors

Purpose: compare direction-focused geometry where norm effects are removed.

### 9.3 Hyperbolic view

- PCA on Poincare-projected vectors

Purpose: inspect structure under a negative-curvature-inspired representation.

### 9.4 Centroid separation by geometry

A per-geometry bar chart compares language centroid distances:

- d(Marwari,Hindi)
- d(Marwari,English)
- d(Hindi,English)

Purpose: summarize cross-language separation changes by geometry.

### 9.5 Focused Marwari->Hindi heatmaps

Three separate heatmaps on top informative pairs:

- before alignment
- after alignment
- gain (after minus before)

Purpose: readable local evidence of alignment improvement.

---

## 10) Experimental evaluation

### 10.1 Qualitative retrieval

For sample Marwari queries:

- nearest Hindi neighbors before alignment
- nearest Hindi neighbors after alignment

Shows intuitive improvement/failure cases.

### 10.2 Quantitative retrieval@1 by metric

Evaluates dictionary retrieval with four metrics:

- Euclidean
- cosine
- angular
- hyperbolic

Compares before vs after alignment and reports gain.

The plot now explicitly annotates before and after values so low bars are still readable.

---

## 11) Why PCA and t-SNE are both used

### 11.1 PCA (Principal Component Analysis)

PCA is a linear dimensionality reduction method.

It finds orthogonal axes (principal components) of maximum variance and projects data onto top components.

Pros:

- deterministic (given data)
- global structure preserving (linear)
- interpretable in variance terms

### 11.2 t-SNE (t-distributed Stochastic Neighbor Embedding)

t-SNE is nonlinear dimensionality reduction focused on local neighborhood preservation.

Pros:

- often shows local clusters clearly

Caveats:

- can distort global distances
- sensitive to hyperparameters
- mostly a visualization tool, not a metric space itself

Using both gives a balanced geometric perspective.

---

## 12) Why this notebook is useful academically

This notebook is strong as a mini research submission because it:

- starts from explicit math
- uses real corpora
- trains reproducible baseline embeddings
- compares multiple geometries on same embeddings
- performs multilingual alignment with formal objective
- provides isotropy/anisotropy diagnostics
- includes qualitative and quantitative experiments
- presents interpretable plots and tables

---

## 13) Practical interpretation of outcomes

When reading outputs, focus on:

1. alignment quality

- average pair cosine before vs after
- retrieval gains

2. geometry effects

- which metric performs better after alignment
- whether hyperbolic behaves differently than Euclidean/cosine

3. anisotropy behavior

- higher anisotropy ratio indicates stronger directional collapse
- compare deltas vs Marwari baseline

4. visualization consistency

- whether Marwari neighborhoods move closer to Hindi anchors post-alignment

---

## 14) Limitations and caveats

- Marwari source uses a Rajasthani proxy corpus shard (resource constraint reality)
- small sampled corpora for runtime practicality
- hyperbolic treatment is projection-based approximation, not full Riemannian training
- retrieval metrics depend on anchor lexicon quality/coverage

---

## 15) Suggested future upgrades

- true hyperbolic embedding optimization (Riemannian training)
- stronger lexicon induction or supervised bilingual dictionaries
- contextual multilingual embeddings comparison
- larger corpora and controlled ablation studies
- bootstrap confidence intervals for retrieval improvements

---

## 16) One-line summary

This notebook demonstrates how geometric choice, anisotropy structure, and orthogonal multilingual alignment jointly shape cross-lingual embedding quality, with Marwari as the primary low-resource reference and Hindi/English as comparison anchors.
