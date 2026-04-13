# Geometry of Embedding Spaces for Multilingual Low-Resource NLP: A Comparative Study of Marwari, Hindi, and English

**Abstract**

This report studies how geometric assumptions influence multilingual word embedding behavior for a low-resource language setting centered on Marwari, with Hindi and English used as comparison languages. The work combines corpus preparation, skip-gram-style representation learning, orthogonal multilingual alignment, and geometric diagnostics in Euclidean, spherical, and hyperbolic views. The main objective is to determine whether geometry-aware analysis improves interpretation of cross-lingual neighborhood structure and retrieval behavior. The experiments indicate that alignment quality, anisotropy, and retrieval performance are all sensitive to the chosen metric, while normalized and curvature-inspired views expose structural properties that are less visible in standard Euclidean analysis. The report is written as an IEEE-style technical paper and is intended to document the methods, measurements, and interpretation pipeline used in the accompanying notebook.

**Index Terms**

Word embeddings, multilingual alignment, low-resource NLP, Euclidean geometry, spherical geometry, hyperbolic geometry, isotropy, anisotropy, Procrustes alignment, Marwari, Hindi, English.

## I. Introduction

Embedding spaces are often treated as ordinary vector spaces, yet the geometry imposed on those vectors strongly affects how semantic relations are interpreted. In multilingual settings, this issue becomes more pronounced because the same conceptual neighborhood may appear differently across languages, especially when one language is low-resource and the available corpus is limited. The present study examines this problem using Marwari as the primary reference language and Hindi and English as comparison languages.

The report addresses three questions. First, how coherent are the learned monolingual spaces under standard distributional training? Second, how does the geometry of the evaluation space alter the interpretation of semantic neighborhoods? Third, does orthogonal alignment improve cross-lingual retrieval in a measurable way? To answer these questions, the notebook trains word embeddings, compares several distance functions, evaluates isotropy and anisotropy, and measures retrieval performance before and after alignment.

The contribution of the work is methodological rather than architectural. The notebook does not introduce a new embedding model; instead, it provides a structured framework for comparing geometric views of multilingual embeddings and for interpreting their behavior using both visual and quantitative evidence.

**The pipeline below summarizes the entire experimental workflow:**

![Multilingual analysis pipeline](figures/ieee_pipeline.png)

_Fig. 1. End-to-end workflow from corpora through preprocessing, embedding training, alignment, and geometric analysis._

## II. Background and Related Concepts

A word embedding maps a token to a dense vector so that distributionally similar words are represented near one another [1]. In a flat Euclidean setting, semantic distance is typically approximated by the L2 norm. However, many linguistic comparisons depend more strongly on direction than on magnitude, which motivates cosine similarity and angular distance. When vectors are normalized, the embedding space can be viewed on the surface of a sphere, where angular separation becomes the relevant measure.

Hyperbolic geometry provides a different perspective. Because hyperbolic space expands rapidly near the boundary, it is often used to represent hierarchical or tree-like relationships [4]. This makes it useful as a diagnostic lens for language data that may contain nested semantic structures or taxonomic groupings [6].

A separate but equally important issue is anisotropy. Many embedding models concentrate variance into a small number of dominant directions, which reduces the effective expressive power of the space [5]. Isotropy analysis is therefore useful for determining whether the learned vectors occupy the space uniformly or collapse into a narrow cone.

## IV. Data and Preprocessing

The notebook uses three corpora drawn from existing sources. English data are taken from Brown and IEER corpora available through NLTK. Hindi data come from the NLTK Indian corpus. Marwari is approximated using a Rajasthani text shard obtained from an external public source because complete Marwari resources are limited.

The pipeline applies language-specific prefixes to each token so that the vocabularies remain distinct across languages. This prevents accidental collisions and keeps the evaluation focused on cross-lingual structure rather than shared surface forms. The preprocessing stage also performs lowercasing, regular-expression cleanup, token extraction, vocabulary truncation, and sentence filtering. Short or noisy sequences are removed so that training pairs are formed from usable text segments.

The resulting corpora are intentionally modest in size. That constraint reflects the low-resource setting and also keeps the notebook practical for interactive experimentation.

## V. Embedding Model and Training Objective

The representation learning stage follows a skip-gram-style objective [1] with negative sampling behavior approximated through binary classification. For each sentence, the model generates target-context pairs within a sliding window. Observed context pairs are assigned positive labels, while randomly sampled non-context pairs act as negative examples.

Each language is trained separately. The Keras architecture uses two embedding layers, one for target tokens and one for context tokens. Their outputs are combined through a dot product and passed through a sigmoid layer. Binary cross-entropy is used as the loss function. This setup is simple, but it is sufficient for studying the geometric properties of the resulting spaces.

The goal of this stage is not to maximize benchmark accuracy. Instead, the model produces a controlled embedding space that can be inspected under several geometric interpretations.

## VI. Geometric Evaluation Framework

The notebook compares four geometric views.

### A. Euclidean view

The Euclidean setting uses standard L2 distance. It provides the baseline interpretation of proximity in the learned space and is the most direct way to inspect global layout and centroid separation.

### B. Spherical view

For the spherical analysis, vectors are normalized to unit length. This suppresses magnitude effects and emphasizes angular similarity. The resulting view is useful when semantic direction matters more than vector norm.

### C. Hyperbolic view

For the hyperbolic analysis, embeddings are projected into the Poincare ball as an approximation to a negative-curvature geometry. The corresponding distance function highlights how neighborhood relations change when expansion near the boundary is allowed. Although the notebook does not train embeddings directly in a Riemannian manner, the projection still serves as a useful diagnostic tool.

### D. Dimensionality reduction

PCA is used to capture broad variance structure, while t-SNE is used to inspect local clustering. PCA is valuable because it preserves global linear trends and offers interpretability through variance explained. t-SNE is complementary because it reveals neighborhood relations that may be hidden in linear projections.

**The figure below illustrates the geometric perspectives used in the analysis:**

![Geometry views](figures/geometry_views.png)

_Fig. 2. Euclidean, spherical, and hyperbolic interpretations of the same embedding set. Each geometry reveals different structural properties of word representations._

## VI. Multilingual Alignment

The alignment stage operates on embedding spaces rather than on raw text. Anchor pairs are collected between Marwari and Hindi, producing source vectors X and target vectors Y. The optimization problem is formulated as orthogonal Procrustes [2], [3]:

$$
W^* = \arg\min_{W^T W = I} \|WX - Y\|_F
$$

The solution is obtained from the singular value decomposition of $YX^T$:

$$
YX^T = U\Sigma V^T, \quad W^* = UV^T
$$

The learned transformation is then applied to the full Marwari embedding matrix so that Marwari vectors are expressed in the Hindi coordinate frame. This shared space allows direct comparison of nearest neighbors and retrieval accuracy before and after alignment.

The purpose of the alignment is not to force lexical identity. Rather, it is to test whether a linear rotation is sufficient to expose latent cross-lingual semantic structure.

**The alignment process is depicted below:**

![Alignment workflow](figures/alignment_workflow.png)

_Fig. 3. Orthogonal transformation from Marwari source vectors to the Hindi coordinate frame via Procrustes alignment. Anchor pairs establish the optimal rotation while preserving internal geometry._

## VIII. Isotropy and Anisotropy Diagnostics

The notebook measures whether the learned spaces distribute information evenly across dimensions. After centering each matrix, singular values are computed to quantify directional concentration. Two summary quantities are reported.

$$
\text{anisotropy ratio} = \frac{\sigma_{max}}{\text{mean}(\sigma)}
$$

$$
\text{isotropy index} = \frac{1}{\text{anisotropy ratio}}
$$

A high anisotropy ratio indicates that the space is dominated by a few directions, while a higher isotropy index indicates more balanced spread. The notebook also examines random projection variance to confirm whether the singular-value-based interpretation is consistent with directional behavior.

These measurements are reported for the original Marwari space, the Hindi space, the English space, and the aligned Marwari space. The comparison helps isolate whether alignment improves structural balance or simply rotates the geometry without changing its intrinsic shape.

## IX. Experimental Results

### A. Qualitative retrieval

The notebook evaluates sample Marwari queries against Hindi neighbors before and after alignment. Before alignment, nearest neighbors often reflect partial overlap in orthography or weak semantic association. After alignment, the neighbors are expected to show improved semantic plausibility. The examples are useful because they expose both successes and failure cases in a way that metrics alone cannot.

### B. Retrieval at rank 1

A dictionary-style retrieval evaluation is computed using Euclidean, cosine, angular, and hyperbolic distances. For each metric, the notebook compares performance before and after alignment and reports the change in retrieval@1. This allows the same lexical pairs to be assessed under multiple geometric assumptions.

The main value of the metric comparison is interpretive. If a metric improves consistently after alignment, then the chosen geometry is compatible with the alignment procedure. If one metric behaves differently from the others, that difference can indicate sensitivity to curvature, normalization, or norm effects.

### C. Centroid separation

Language centroid distances are summarized in bar-chart form for multiple geometries. This provides a compact view of how far Marwari sits from Hindi and English in each metric space. The comparison is particularly useful for understanding whether alignment compresses the Marwari-Hindi gap without collapsing distinctions among all three languages.

### D. Heatmap analysis

The notebook includes three heatmaps for the Marwari-to-Hindi pair: before alignment, after alignment, and gain. The before/after comparison shows whether the anchor-based mapping improves similarity for the selected word pairs. The gain map isolates where the alignment produced the strongest positive shift. This is especially helpful for interpreting localized improvements that are difficult to see in aggregate scores.

## X. Discussion

The combined evidence suggests that geometry matters both for analysis and for interpretation. Euclidean visualization captures the broad distribution of vectors, but it can hide semantic directionality. Spherical normalization reduces norm effects and often clarifies neighborhood structure. Hyperbolic projection is most useful as a diagnostic for hierarchy-sensitive behavior, even when the embeddings are not trained directly in hyperbolic space.

Orthogonal alignment provides a simple but effective bridge between Marwari and Hindi. Because the transformation is constrained to be a rotation, it preserves internal distances while reorienting the source space toward the target space. That property makes it especially suitable for comparing pre- and post-alignment neighborhoods without introducing distortion from an unconstrained mapping.

The anisotropy results are important in their own right. If a space is too concentrated along a few principal axes, then cosine-based comparison may overstate similarity among unrelated tokens. The diagnostics included in the notebook help identify that risk and show whether the aligned space becomes more balanced or remains directionally compressed.

## XI. Limitations

The study has several limitations. The Marwari corpus is a proxy resource rather than a large canonical dataset, so its coverage is incomplete. The corpora are small enough to support notebook execution, but that choice limits generalization. The hyperbolic component is projection-based rather than a full Riemannian optimization procedure, so it should be treated as an analytical approximation. Finally, retrieval quality depends on the quality of the anchor lexicon used for alignment.

These limits do not invalidate the study, but they do constrain how strongly the results should be generalized beyond the notebook setting.

## XI. Conclusion

This report demonstrates an IEEE-style analysis pipeline for multilingual embeddings in a low-resource setting. The main finding is that the geometry used to inspect or compare embeddings materially affects the observed behavior. Euclidean, spherical, and hyperbolic views each reveal different aspects of the same learned representations, while orthogonal alignment improves cross-lingual comparability in a controlled and interpretable way.

The notebook is therefore best understood as a compact research prototype: it combines corpus preparation, distributional training, geometric diagnostics, and multilingual evaluation into one coherent experimental framework. For a low-resource language such as Marwari, this type of analysis is useful because it shows not only whether alignment works, but also how and under what geometric assumptions it works.

## References

[1] T. Mikolov, K. Chen, G. Corrado, and J. Dean, "Efficient Estimation of Word Representations in Vector Space," arXiv:1301.3781, 2013.

[2] M. Artetxe, G. Labaka, and E. Agirre, "Learning Bilingual Word Embeddings with (Almost) No Bilingual Data," in Proc. 55th Annual Meeting of the Association for Computational Linguistics, 2017.

[3] S. Ruder, I. Vulić, and A. Søgaard, "A Survey of Cross-lingual Word Embedding Models," Journal of Artificial Intelligence Research, vol. 65, pp. 859-893, 2019.

[4] M. Nickel and D. Kiela, "Poincaré Embeddings for Learning Hierarchical Representations," in Proc. Advances in Neural Information Processing Systems, 2017.

[5] A. Mu and S. Viswanath, "All-but-the-Top: Simple and Effective Postprocessing for Word Representations," in Proc. International Conference on Learning Representations, 2018.

[6] A. Tifrea, G. Bécigneul, and O. Ganea, "Poincaré GloVe: Hyperbolic Word Embeddings," in Proc. International Conference on Learning Representations, 2019.
