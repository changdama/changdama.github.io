<div class="naf-page" markdown>

<p class="naf-kicker">Neural audio · Spatial representation · Ongoing research · 2026</p>

# Distance-Aware Residual Neural Acoustic Fields

<p class="naf-deck">A physics-informed neural representation that separates predictable distance attenuation from the spatial and spectral detail a network must learn.</p>

<div class="naf-status"><strong>Ongoing Research</strong><span>Controlled synthetic First-Order Ambisonics in reflection-free sampling volumes. The study establishes a representation prototype—not yet a complete model of real rooms or perceptually validated 6DoF audio.</span></div>

<div class="naf-stats">
  <div><strong>0.477</strong><span>best spectral L1</span></div>
  <div><strong>5.70 dB</strong><span>best log-spectral distance</span></div>
  <div><strong>3</strong><span>spatial scales</span></div>
  <div><strong>512</strong><span>positions per test path</span></div>
</div>

## The representation problem

Interactive spatial audio requires the sound field to update continuously as a listener moves. Dense measurement grids are expensive and interpolation can introduce discontinuities; a direct neural field, meanwhile, must learn both the strong global change caused by distance and the smaller time–frequency detail layered on top of it.

This project asks whether a simple physical prior can make that learning problem better conditioned. It represents the four-channel FOA log-magnitude spectrum as a continuous function of relative source–listener displacement, frequency, and time, then decomposes the prediction into two parts:

<div class="naf-equation"><span>acoustic field</span><b>Ŷ = B(d, f) + R(Δx, f, t)</b><small>learnable distance base + neural residual</small></div>

The base branch models distance-dependent attenuation,

\[
B(d,f)=-\bigl(a(f)\log d+b(f)\bigr),
\]

while an eight-layer residual MLP with positional encoding learns the remaining spatial, spectral, and temporal variation. The frequency-dependent parameters \( a(f) \) and \( b(f) \) allow each FOA channel to depart from an idealized inverse-distance law.

<figure class="naf-figure naf-architecture">
  <img src="/assets/projects/neural-acoustic-field/architecture.webp" alt="Architecture of the distance-aware residual neural acoustic field, combining a learnable distance base with a residual MLP">
  <figcaption>Relative geometry drives both branches. Their outputs reconstruct the W, X, Y, and Z log-magnitude spectra, supervised by spectral, multi-resolution, temporal, and channel-structure objectives.</figcaption>
</figure>

## Controlled experiment

Synthetic FOA signals are rendered in SuperCollider with the Ambisonic Toolkit using two-second, 48 kHz white-noise excitation. The AmbiX output uses ACN/SN3D channel ordering. Three reflection-free spatial volumes test whether the representation remains stable over increasingly broad source–listener distances.

<div class="naf-scales">
  <div><span>SMALL</span><strong>≈ 90 m³</strong><small>4.7 × 5.2 × 3.7 m</small></div>
  <div><span>MEDIUM</span><strong>≈ 320 m³</strong><small>10 × 8 × 4 m</small></div>
  <div><span>LARGE</span><strong>≈ 1,200 m³</strong><small>20 × 15 × 4 m</small></div>
</div>

For each scale, 10 fixed sources are paired with 2,048 training listener positions and 512 test positions sampled using Sobol sequences at a height of 1.6 m. A separate 512-point circular trajectory tests continuous movement. The model is trained for 200,000 iterations on an NVIDIA A100.

The comparison includes an analytical distance-only model, nearest-neighbor and inverse-distance-weighted interpolation, direct neural fitting, and the proposed residual model. Removing the temporal coordinate provides an additional ablation.

## What the current results show

| Method · small scale | L1 ↓ | LSD ↓ | MR ↓ | SC ↓ |
| --- | ---: | ---: | ---: | ---: |
| Analytical distance only | 1.967 | 36.48 | 15.030 | 1.000 |
| Nearest-neighbor interpolation | 0.672 | 7.83 | 1.064 | 0.702 |
| Inverse-distance interpolation | 0.550 | 6.38 | 1.173 | 0.683 |
| Direct neural field | 0.490 | 5.83 | **0.846** | **0.557** |
| **Distance-aware residual field** | **0.477** | **5.70** | 1.108 | 0.638 |

The residual formulation produces the lowest L1 and log-spectral distance, but the direct model remains stronger on the waveform-oriented multi-resolution STFT and spectral-convergence metrics. This is an important trade-off: adding the learned base improves log-spectral reconstruction while base-parameter errors can be amplified during zero-phase inverse-STFT evaluation.

Across the three scales, residual-model L1 remains tightly grouped at **0.477, 0.474, and 0.479**, while LSD remains between **5.65 and 5.70 dB**. The temporal coordinate is also essential: removing \( t \) from the direct model raises L1 from 0.490 to 1.564 and LSD from 5.83 to 34.31 dB.

<figure class="naf-figure">
  <img src="/assets/projects/neural-acoustic-field/path-rendering.webp" alt="Comparison of ground truth, nearest-neighbor interpolation, direct MLP, and residual model along a circular listener trajectory">
  <figcaption>W-channel energy along a circular trajectory. Nearest-neighbor interpolation creates visible step changes; both neural fields remain continuous, with path L1 of 0.500 for direct fitting and 0.488 for the residual model.</figcaption>
</figure>

## What remains unproven

The experiment isolates geometry and attenuation, but it does not yet model the defining difficulty of a real acoustic environment: multipath propagation. Because the current signals contain no boundary reflections or reverberation, the word “room” describes only the size of a sampling region. The use of white noise, log magnitude without phase, zero-phase reconstruction, and objective spectral errors also limits what can be claimed about audible spatial quality.

The present result is therefore best understood as evidence that the decomposition can regularize a controlled neural-field fitting task—not yet evidence of a complete 6DoF spatial-audio renderer.

## Future directions shaped by technical review

<div class="naf-roadmap" markdown>

<div markdown>
<span>01</span>
### Move from free field to rooms
Train and test with simulated and measured room impulse responses, including early reflections, late reverberation, boundary absorption, occlusion, and source directivity. Report room-acoustic parameters rather than treating spatial extent alone as a room condition.
</div>

<div markdown>
<span>02</span>
### Clarify the use case
Demonstrate when a learned field is preferable to analytical FOA generation, Higher-Order Ambisonics, or an object-based renderer. Compare memory, computation, interpolation density, and generalization under a clearly defined 6DoF task.
</div>

<div markdown>
<span>03</span>
### Add perceptual evidence
Reconstruct playable FOA or binaural audio, publish sound examples, and run listening studies for localization, externalization, timbre, motion continuity, and overall realism. Calibrate objective scores against perceptual judgments.
</div>

<div markdown>
<span>04</span>
### Support dynamic scenes
Evaluate moving listeners and sources, multiple simultaneous sources, and correlated reflections. Test whether pairwise evaluation plus linear superposition remains sufficient or whether scene-level interaction must be modeled directly.
</div>

<div markdown>
<span>05</span>
### Revisit signal assumptions
Model or reconstruct phase, verify the FOA channel-energy constraint from channel energies, and isolate periodic structure introduced by STFT windowing or the ATK encoder so processing artifacts are not mistaken for learned propagation behavior.
</div>

<div markdown>
<span>06</span>
### Strengthen evidence and attribution
Replace tangential citations with authoritative spatial-audio and acoustics sources, support claims about MLP stability and FOA perception directly, correct metric provenance, and document metric units and meaningful perceptual scales.
</div>

</div>

<p class="naf-credits"><strong>Researcher</strong><br>Changda Ma<br><small>Neural spatial-audio research · 2026</small></p>

</div>
