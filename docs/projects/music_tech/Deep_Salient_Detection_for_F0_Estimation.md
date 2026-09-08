<div class="f0-page" markdown>

<p class="f0-kicker">Audio AI · Pitch tracking · Course research · 2025</p>

# Deep Salient Detection for F0 Estimation

**Can a compact, audio-specific network estimate singing pitch more reliably than a rule-based tracker or a large pretrained vision model?**

This project replicates a deep salience approach to fundamental-frequency (F0) estimation and extends it through a controlled comparison of three strategies: an autocorrelation baseline, a fully convolutional **SimpleNet**, and transfer learning with **ResNet-18**. The system transforms audio into a harmonic time–frequency representation, predicts a dense pitch-salience map, and decodes that map into a frame-wise melody contour.

<div class="f0-stats">
  <div><strong>81.58%</strong><span>best overall accuracy</span></div>
  <div><strong>1.54%</strong><span>voicing false alarms</span></div>
  <div><strong>6</strong><span>HCQT harmonic channels</span></div>
  <div><strong>60</strong><span>bins per octave</span></div>
</div>

## From waveform to melody contour

<div class="f0-flow" aria-label="F0 estimation pipeline">
  <div><b>Audio</b><small>44.1 kHz waveform</small></div><i>→</i>
  <div><b>HCQT</b><small>6 × 360 × T</small></div><i>→</i>
  <div><b>Salience model</b><small>pitch likelihood map</small></div><i>→</i>
  <div><b>Decoder</b><small>frame-wise F0 contour</small></div>
</div>

The input is a **Harmonic Constant-Q Transform (HCQT)** designed to expose the harmonic structure of pitched sound. Six CQT channels are computed using harmonic factors (h \in \{0.5, 1, 2, 3, 4, 5\}), beginning at C1 (approximately 32.7 Hz), spanning six octaves at 60 bins per octave, and advancing with a 512-sample hop. Stacking these channels produces a (6 \times 360 \times T) tensor.

Ground-truth F0 annotations are quantized onto the same frequency grid and Gaussian-blurred across neighboring bins. This creates a smooth target salience profile that does not over-penalize small pitch deviations.

## Three competing approaches

<div class="f0-models" markdown>

<div markdown>
<span>01 · RULE BASED</span>
### Autocorrelation
Operates directly on waveform frames and selects periodicity peaks. It detects voiced activity aggressively, but has no strong mechanism for rejecting unvoiced frames.
</div>

<div class="f0-model-best" markdown>
<span>02 · TASK SPECIFIC</span>
### SimpleNet
Three convolutional layers with batch normalization and ReLU preserve the full time–frequency resolution. A final (1 \times 1) convolution predicts one salience value per bin without pooling away pitch location.
</div>

<div markdown>
<span>03 · TRANSFER LEARNING</span>
### ResNet-18
Adapts an ImageNet-pretrained visual backbone to the HCQT input. Frozen and fully fine-tuned variants test whether general image features transfer to spectral salience estimation.
</div>

</div>

## Training study

SimpleNet is trained from scratch on random 512-frame HCQT crops with a batch size of 8, Adam optimization, and a learning rate of (10^{-3}). ResNet-18 uses a more conservative (10^{-4}) learning rate in both frozen and unfrozen configurations.

Each architecture is evaluated with binary cross-entropy (BCE) and, where applicable, a hybrid objective:

\[
\mathcal{L}_{\text{hybrid}} =
\lambda_{\text{BCE}}\mathcal{L}_{\text{BCE}} +
\lambda_{\text{MSE}}\mathcal{L}_{\text{MSE}},
\qquad
\lambda_{\text{BCE}}=1.0,\;\lambda_{\text{MSE}}=0.1.
\]

The study uses an artist-independent split of **MedleyDB-Pitch** for training and validation, reserving approximately 20% of tracks for validation to limit timbral overlap. Final evaluation is conducted on the unseen **Vocadito** singing-voice dataset. A threshold sweep selects the salience threshold that maximizes Overall Accuracy.

<figure class="f0-figure">
  <img src="/assets/projects/deep_salient_detection.png" alt="Training and validation loss curves for SimpleNet and ResNet-18 configurations over 30 epochs">
  <figcaption>Training and validation loss across the six neural-network configurations. SimpleNet converges quickly and stably; fine-tuned ResNet variants optimize more effectively than frozen ones but do not translate that convergence into accurate F0 estimates.</figcaption>
</figure>

## Evaluation

Performance is measured using standard melody-estimation metrics: Voicing Recall (VR), Voicing False Alarm (VFA), Raw Pitch Accuracy (RPA, within 50 cents), Raw Chroma Accuracy (RCA), and Overall Accuracy (OA).

| Model | VR ↑ | VFA ↓ | RPA ↑ | RCA ↑ | OA ↑ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Autocorrelation | 99.85 | 70.12 | 84.09 | 84.72 | 65.65 |
| **SimpleNet · BCE** | **74.92** | **1.54** | **72.71** | **72.74** | **81.58** |
| SimpleNet · BCE + MSE | 72.18 | 3.18 | 69.47 | 69.49 | 78.95 |
| ResNet-18 · BCE · frozen | 3.43 | 10.30 | 0.00 | 0.15 | 30.33 |
| ResNet-18 · BCE · fine-tuned | 55.03 | 23.33 | 12.93 | 12.93 | 34.81 |
| ResNet-18 · BCE + MSE · frozen | 3.43 | 10.32 | 0.00 | 0.15 | 30.32 |
| ResNet-18 · BCE + MSE · fine-tuned | 54.85 | 23.56 | 13.01 | 13.01 | 34.78 |

<small class="f0-table-note">Values are percentages reported as the mean performance on Vocadito; the project report also provides track-level standard deviations.</small>

## What the comparison reveals

**SimpleNet with BCE is the strongest overall system**, reaching 81.58% OA—15.93 percentage points above autocorrelation—while reducing false voicing detections from 70.12% to 1.54%. Autocorrelation remains strong at finding periodicity and achieves the highest raw pitch score, but its tendency to label unvoiced frames as voiced makes it less reliable as a complete melody tracker. Adding MSE smooths optimization, yet slightly reduces the final accuracy of SimpleNet.

The ResNet-18 experiments expose a deeper representation mismatch. Visual classifiers are encouraged to recognize a feature wherever it appears in an image. In an HCQT, however, vertical position is frequency: moving a harmonic pattern vertically changes its pitch and therefore its musical meaning. ImageNet filters for edges and textures are poorly aligned with this dense, frequency-sensitive prediction task, and even full fine-tuning does not close the gap.

!!! note "Why the smaller network wins"
    Model capacity is not the deciding factor here. Preserving pitch location and learning directly from harmonic audio structure matter more than importing a larger visual representation with conflicting inductive biases.

## Scope and next steps

The experiment establishes a reproducible comparison on singing-voice melody data, but broader evaluation is still needed. Future work can test additional musical sources and recording conditions, examine temporal decoding beyond frame-wise maxima, and explore audio-pretrained representations whose invariances are better matched to pitch.

<p class="f0-credits"><strong>Researchers</strong><br>Changda Ma · Jiayi Wang<br><small>Georgia Institute of Technology · 2025</small></p>

<details class="draft-request">
  <summary><span>Project report <b>1</b></span><span class="draft-request-chevron" aria-hidden="true"></span></summary>
  <div class="draft-request-list">
    <article>
      <div><small>Course research report</small><strong>Deep Salient Detection for F0 Estimation</strong></div>
      <a href="mailto:cma326@gatech.edu?subject=Request%20for%20Deep%20Salient%20Detection%20Report&body=Hello%20Changda%2C%0A%0AI%20would%20like%20to%20request%20the%20Deep%20Salient%20Detection%20for%20F0%20Estimation%20report.%0A%0AThank%20you.">Request PDF ↗</a>
    </article>
    <p>The project report is available by email.</p>
  </div>
</details>

</div>
