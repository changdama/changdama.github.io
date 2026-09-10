<div class="jukebox-page" markdown>

<p class="jukebox-kicker">Music information retrieval · Structural analysis · Algorithmic remix · 2025</p>

# Infinite Jukebox

<p class="jukebox-deck">A structure-aware remix engine that finds musically compatible beats, chooses its own analysis settings, and continuously rewrites a song without simply repeating it from the beginning.</p>

## The idea

A conventional loop returns to a fixed start point. Infinite Jukebox instead listens for beats that resemble one another and treats those locations as possible portals through the song. Playback normally advances beat by beat; at selected moments, it can jump to a structurally compatible position and continue from there.

The project extends that basic idea in two ways. First, it searches across multiple audio features and similarity settings instead of relying on one hand-tuned configuration. Second, it uses a Foote novelty curve to raise the jump probability near structural transitions, connecting traversal behavior to the form of each song.

<div class="jukebox-flow" aria-label="Infinite Jukebox analysis and rendering pipeline">
  <div><b>Audio</b><small>load · mono · normalize</small></div><i>→</i>
  <div><b>Beat grid</b><small>onset strength · beat tracking</small></div><i>→</i>
  <div><b>Features</b><small>beat-synchronized descriptors</small></div><i>→</i>
  <div><b>SSM</b><small>similarity + structural score</small></div><i>→</i>
  <div><b>Traversal</b><small>sequence · jump · render</small></div>
</div>

## Hearing repetition as a matrix

The engine extracts one of four representations—**MFCC**, **chroma**, **spectral contrast**, or **CQT**—and aggregates its frames within each beat using a mean or median. Every beat is then compared with every other beat using correlation, cosine distance, or Euclidean distance.

The resulting Self-Similarity Matrix (SSM) makes musical form visible. Bright off-diagonal paths indicate related passages at different moments; blocks expose larger repeated sections; abrupt changes in local similarity suggest boundaries.

<div class="jukebox-ssm-pair">
  <figure><img src="/assets/projects/infinite-jukebox/ssm-rock.webp" alt="Best continuous self-similarity matrix for Rock With You using CQT and correlation"><figcaption>A regularly sectional song produces distributed repetition throughout its SSM.</figcaption></figure>
  <figure><img src="/assets/projects/infinite-jukebox/ssm-happier.webp" alt="Best continuous self-similarity matrix for Happier Than Ever using CQT and cosine similarity"><figcaption>A two-part song creates a sharply contrasted block structure.</figcaption></figure>
</div>

## Automatic parameter search

Manual tuning can make an Infinite Jukebox work for one song while failing on another. This implementation evaluates:

- 4 feature sets: MFCC, chroma, spectral contrast, and CQT
- 2 beat-level aggregations: mean and median
- 3 similarity metrics: correlation, cosine, and Euclidean
- 3 binarization thresholds: 0.75, 0.80, and 0.85

Together, these choices produce **72 candidate SSMs per song**. The implemented structural score combines three signals:

<div class="jukebox-score">
  <div><strong>30%</strong><span>diagonal contrast</span><small>clarity of repeated paths</small></div>
  <div><strong>20%</strong><span>sparsity moderation</span><small>avoids all-bright or all-dark matrices</small></div>
  <div><strong>50%</strong><span>Foote novelty</span><small>strength and coverage of boundaries</small></div>
</div>

Degenerate matrices that are almost flat, too dense, or too sparse receive an additional penalty. The highest-scoring configuration is passed to the remix stage automatically.

## Two songs, two structural solutions

<div class="jukebox-cases" markdown>

<div markdown>
<span>REGULAR SECTIONAL FORM</span>
### “Rock With You”
Repeated verses, choruses, instrumental colors, and an extended outro create many plausible return points across the song.

<dl><dt>Feature</dt><dd>CQT</dd><dt>Aggregation</dt><dd>Median</dd><dt>Metric</dt><dd>Correlation</dd><dt>Threshold</dt><dd>0.80</dd><dt>Score</dt><dd>0.303</dd></dl>
</div>

<div markdown>
<span>CONTRASTING TWO-PART FORM</span>
### “Happier Than Ever”
A gradual transition from sparse ballad to dense rock produces fewer but substantially stronger structural changes.

<dl><dt>Feature</dt><dd>CQT</dd><dt>Aggregation</dt><dd>Mean</dd><dt>Metric</dt><dd>Cosine</dd><dt>Threshold</dt><dd>0.75</dd><dt>Score</dt><dd>0.326</dd></dl>
</div>

</div>

The selected parameters differ, showing why a single fixed recipe is limiting. **CQT is selected for both case studies**, suggesting that its logarithmic, pitch-aligned frequency grid offers a useful balance of harmonic and timbral structure for this task.

## Novelty-driven traversal

A checkerboard kernel is convolved with the SSM following Foote's novelty method. Peaks identify locations where the similarity relationship between the preceding and following windows changes most strongly.

<div class="jukebox-plot-pair">
  <figure><img src="/assets/projects/infinite-jukebox/novelty-rock.webp" alt="Foote novelty curve and detected structural boundaries for Rock With You"><figcaption>Distributed moderate peaks reflect recurring sectional changes.</figcaption></figure>
  <figure><img src="/assets/projects/infinite-jukebox/novelty-happier.webp" alt="Foote novelty curve and detected structural boundaries for Happier Than Ever"><figcaption>Concentrated high peaks reflect the large-scale transition between contrasting halves.</figcaption></figure>
</div>

The normalized novelty value modulates the base jump probability:

\[
p_i=p_0+(p_{\max}-p_0)\widetilde{N}_i.
\]

At each beat, the engine either advances sequentially or jumps to a randomly selected beat that passes the SSM threshold. If playback reaches the end, it wraps to the beginning. The selected beat segments are finally sliced from the waveform and concatenated into a new remix.

## What the prototype demonstrates

The system turns music analysis into generative behavior: feature extraction describes the song, the SSM exposes its internal relationships, novelty identifies structural change, and those measurements directly shape playback decisions. The contrasting case studies show that automated parameter selection can adapt to very different musical forms.

The current structural score is heuristic rather than perceptually validated. Future development could add downbeat and bar-level constraints, phase-aware or crossfaded joins, repetition-memory to avoid short cycles, section-aware traversal policies, and formal listening tests of continuity and musical plausibility.

<p class="jukebox-credits"><strong>Creators</strong><br>Changda Ma · Marcus Parker<br><small>Python · Librosa · NumPy · SciPy · Matplotlib · 2025</small></p>

<nav class="jukebox-resources" aria-label="Infinite Jukebox project resources">
  <a href="/assets/projects/infinite-jukebox/InfiniteJukeBoxCM_MP.py" download><strong>Download source code</strong><small>Python · 21 KB</small></a>
</nav>

</div>
