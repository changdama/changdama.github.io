<div class="feature-classification-page" markdown>

<p class="fc-kicker">Music information retrieval · Audio classification · Course project</p>

# Instrument Classification from Audio Features

<p class="fc-deck">An interpretable audio-classification study that uses spectral descriptors, MFCCs, k-nearest neighbors, and PCA to distinguish flute, piano, trumpet, and violin recordings.</p>

## From waveform to instrument label

The project asks how far a compact set of hand-designed audio features can go in recognizing instruments. A four-class subset of **Medley-solos-DB** provides 120 development clips and a separate 20-clip test set. Every recording is loaded as mono audio at 22.05 kHz, analysed in overlapping 1,024-sample Hann windows, and reduced to one feature vector per clip.

<div class="fc-flow" aria-label="Instrument classification pipeline">
  <div><b>Audio clips</b><small>flute · piano · trumpet · violin</small></div><i>→</i>
  <div><b>Frame analysis</b><small>1,024 samples · 512 hop</small></div><i>→</i>
  <div><b>16 descriptors</b><small>spectral shape · change · MFCC</small></div><i>→</i>
  <div><b>Normalize</b><small>statistics learned from development data</small></div><i>→</i>
  <div><b>Classify</b><small>kNN · PCA comparison</small></div>
</div>

## An interpretable feature vocabulary

The representation combines six summary descriptors—spectral centroid, roll-off, spread, flatness, zero-crossing rate, and normalized spectral flux—with the first ten MFCCs. Frame-wise measurements are averaged over each clip, producing a 16-dimensional description of its brightness, spectral shape, temporal change, and timbre.

Normalization parameters are estimated on the development split and reused for the test set. This keeps the test examples out of feature scaling while ensuring that Euclidean distance in kNN is not dominated by features with larger numeric ranges.

## What the correlations reveal

<figure class="fc-figure fc-matrix"><img src="/assets/projects/instrument-feature-classification/feature-correlation-matrix.png" alt="Pearson correlation matrix for the sixteen audio features"><figcaption>Pearson correlations across the development clips. Deep blue and red cells expose strongly related or opposing descriptors.</figcaption></figure>

The spectral-brightness descriptors carry substantial overlap. Centroid and roll-off are almost interchangeable in this dataset (**r = 0.98**); roll-off and spread reach **r = 0.93**, while centroid and zero-crossing rate reach **r = 0.92**. MFCC 8 and MFCC 9 are also strongly correlated (**r = 0.77**). By contrast, some feature pairs remain nearly independent, suggesting that a smaller representation could preserve most of the useful information.

<figure class="fc-figure fc-correlation-pair"><img src="/assets/projects/instrument-feature-classification/correlation-examples.png" alt="Scatter plots comparing a highly correlated feature pair with a weakly correlated pair"><figcaption>Centroid and roll-off move together; flux and MFCC 6 show almost no linear relationship.</figcaption></figure>

## Baseline classification

The baseline fits a Euclidean k-nearest-neighbors classifier to all 16 normalized features and evaluates odd values of k from 3 to 15. Scores on the same 120 clips used to fit the model range from 100% at k = 3 to 94.2% at k = 15, but the final non-PCA run reaches only **60% on the 20 held-out test clips**. The gap is evidence that the representation and evaluation need stronger generalization checks—not that the system is already solved.

<div class="fc-result-pair">
  <figure><img src="/assets/projects/instrument-feature-classification/confusion-matrix-knn.png" alt="Confusion matrix for k-nearest-neighbor classification with the original features"><figcaption>Original 16-feature kNN: 12 of 20 test clips classified correctly.</figcaption></figure>
  <div markdown>
  ### Where the model succeeds—and fails

  Piano and trumpet are classified correctly in all five test examples. Flute is confused with both piano and trumpet, while four of five violin clips are labelled as trumpet. This pattern suggests that the clip-level averages capture some stable timbral signatures but lose distinctions needed for the harder instrument pairs.
  </div>
</div>

## Reducing redundancy with PCA

The cumulative explained-variance curve bends near five principal components. Keeping those five components retains about **84% of the variance** while reducing the representation from 16 dimensions to 5.

<div class="fc-result-pair fc-pca-pair">
  <figure><img src="/assets/projects/instrument-feature-classification/pca-explained-variance.png" alt="Cumulative explained variance for one through sixteen principal components"><figcaption>Five components retain roughly 84% of the observed variance.</figcaption></figure>
  <figure><img src="/assets/projects/instrument-feature-classification/confusion-matrix-pca.png" alt="Confusion matrix for k-nearest-neighbor classification after PCA to five dimensions"><figcaption>PCA recovers one additional violin prediction in the displayed run.</figcaption></figure>
</div>

| Representation | k | Fit-set accuracy | Test accuracy |
|---|---:|---:|---:|
| Original 16 features | 15 | 94.2% | 60% |
| PCA, 5 components | 3–9 | 95.0–100% | 60% |
| PCA, 5 components | 13 | 91.7% | **65%** |
| PCA, 5 components | 15 | 90.8% | **65%** |

PCA makes the model more compact and raises the best observed test score from 60% to 65%, although that difference is only one clip in this test set. The result is therefore best read as a useful direction rather than a conclusive performance gain.

## Next iteration

The most important next step is a larger, stratified evaluation with cross-validation and a genuinely separate model-selection split. Data augmentation, per-class precision and recall, distance-weighted kNN, feature selection, and comparisons with SVM or tree-based classifiers would clarify whether the remaining errors come from limited data, redundant descriptors, or the classifier itself. Preserving temporal statistics beyond a single clip-level mean may also help separate violin from trumpet.

<p class="fc-credits"><strong>Creators</strong><br>Changda Ma · Lennon Seiders<br><small>Python · Librosa · scikit-learn · NumPy · Pandas · Matplotlib</small></p>

<nav class="fc-resources" aria-label="Instrument classification project resources">
  <a href="/assets/projects/instrument-feature-classification/Feature_Classification_Part1.ipynb" download><strong>Download notebook</strong><small>Jupyter Notebook · full analysis and PCA experiment</small></a>
  <a href="/assets/projects/instrument-feature-classification/Feature_Classification_Part1.py" download><strong>Download Python source</strong><small>Feature extraction and baseline kNN pipeline</small></a>
</nav>

</div>
