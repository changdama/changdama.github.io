# MusicGen-Rhythm
**Rhythm-Aware Conditioning for Text-to-Music Generation**

MusicGen-Rhythm explores rhythm-aware conditioning strategies for text-to-music generation by extending **MusicGen-Small** with **audio-derived rhythmic representations**.  
The project investigates whether explicit rhythmic cues extracted from audio can improve temporal coherence and rhythmic stability beyond text-only prompting, while keeping the MusicGen backbone frozen.

[Explore the audio demo ↗](https://anonymous-eval-01.github.io/audio-demo/){ .md-button .md-button--primary target="_blank" rel="noopener" }

---

## Motivation
Text prompts alone often under-specify rhythm and long-term temporal structure.  
This work studies how **beat- and energy-aware features** can guide text-to-music generation without relying on symbolic representations or retraining large generative models.

---

## Method Overview

The pipeline consists of:

1. Energy-aware audio clipping  
2. Multi-channel rhythm feature extraction  
3. Lightweight rhythm encoder  
4. Fusion with text embeddings  
5. Frozen MusicGen decoder for RVQ token generation  
6. Auxiliary beat- and energy-aware loss design for rhythmic consistency supervision

![Overall Pipeline](Fig/musicgen_rhythm/overall_flow.png)

---

## Rhythm Representation

We construct a four-channel rhythm-focused feature map capturing complementary temporal cues:

- Log-Mel spectrogram  
- Δ Log-Mel spectrogram  
- Spectral flux  
- RMS energy  

![Rhythm Feature Visualization](Fig/musicgen_rhythm/feature_vis_4ch2.png)

---

## Conditioning Strategies

Two lightweight fusion mechanisms are explored:

**Gating-based Fusion**  
![Gating Fusion Strategy](Fig/musicgen_rhythm/gating_fusion_stragetgy.png)

**Cross-Attention Fusion**  
![Cross-Attention Fusion Strategy](Fig/musicgen_rhythm/cross-attention_fusion_stragtegy.png)

These designs allow flexible integration of rhythmic information while preserving the original MusicGen generation process.

---

## Loss Design

To encourage rhythmic coherence while keeping the pretrained MusicGen backbone frozen, we introduce **auxiliary beat- and energy-aware supervision** applied to lightweight prediction heads.

Specifically, intermediate decoder representations are used to predict:
- a **beat activation trajectory** \( \hat{b}(t) \), and  
- an **energy envelope** \( \hat{e}(t) \),

which are aligned with corresponding targets \( b(t) \) and \( e(t) \) extracted from reference audio.

### Beat and Energy Correlation Losses

We define beat and energy losses using **normalized correlation-based objectives**, encouraging temporal alignment rather than exact magnitude matching:

\[
\mathcal{L}_{\text{beat}} =
1 - \frac{\sum_t (\hat{b}(t) - \bar{\hat{b}})(b(t) - \bar{b})}
{\sqrt{\sum_t (\hat{b}(t) - \bar{\hat{b}})^2}
 \sqrt{\sum_t (b(t) - \bar{b})^2}}
\]

\[
\mathcal{L}_{\text{energy}} =
1 - \frac{\sum_t (\hat{e}(t) - \bar{\hat{e}})(e(t) - \bar{e})}
{\sqrt{\sum_t (\hat{e}(t) - \bar{\hat{e}})^2}
 \sqrt{\sum_t (e(t) - \bar{e})^2}}
\]

These objectives focus on **temporal structure and rhythmic alignment**, rather than absolute value regression, making them robust to scale differences across musical excerpts.

### Total Training Objective

The auxiliary losses are combined with the original MusicGen cross-entropy loss:

\[
\mathcal{L}_{\text{total}} =
\mathcal{L}_{\text{CE}} +
\lambda_{\text{beat}} \mathcal{L}_{\text{beat}} +
\lambda_{\text{energy}} \mathcal{L}_{\text{energy}}
\]

where \( \lambda_{\text{beat}} \) and \( \lambda_{\text{energy}} \) control the relative influence of rhythmic supervision.

### Qualitative Illustration

The figure below shows example trajectories of predicted and target beat activations and energy envelopes over token time, illustrating how auxiliary supervision encourages alignment in rhythmic structure.

![Beat and Energy Trajectories](Fig/musicgen_rhythm/rhythm_viz_example.png)

This loss design enables rhythm-aware learning while preserving the stability and generative capacity of the frozen MusicGen decoder.


---

## Experimental Setup (Summary)

- Backbone: *facebook/musicgen-small* (frozen)  
- Dataset: 500 songs, yielding 1,500 energy-aware 30-second clips
- Split: 70% / 15% / 15% at the song level to prevent leakage
- Conditioning audio: peak-normalized, mono, and resampled to 16 kHz
- Training & evaluation: Google Colab Pro, NVIDIA A100 40 GB High-RAM runtime
- Metrics: BeatF, BeatAlignErr, TempoStab, CrossBarCons, CLAP, and FAD

---

## Results

Audio-derived rhythm conditioning improves beat-level structure without materially reducing audio quality. Compared with the frozen MusicGen-Small baseline, the two SimpleNet variants without auxiliary beat-energy loss improve all four rhythm metrics. **SimpleNet-G** reduces beat-alignment error by 19.7% and improves tempo stability by 15.6%, while **SimpleNet-X** improves BeatF by 7.6% and cross-bar consistency by 10.1%.

The experiments also show that a compact, task-specific rhythm encoder is more effective than the larger pretrained CNN14 backbone for this setting. Gating generally provides the strongest balance between rhythmic control and semantic fidelity because its residual path preserves the text-dominant representation expected by the frozen decoder.

Auxiliary beat- and energy-coherence losses produce a more nuanced result. They can strengthen global rhythmic regularity—the best BeatF improves by 8.8%, and the best cross-bar consistency improves by 16.3%—but they worsen absolute beat alignment and can reduce CLAP similarity. This indicates that feature-level conditioning is currently more reliable than auxiliary coherence supervision for rhythm control with a frozen text-to-music decoder.

![Objective evaluation across MusicGen-Rhythm variants](Fig/musicgen_rhythm/Table2_Result.png)

These findings are reported in the accompanying manuscript, which is currently under review. A controlled listening study remains future work.

---

## Future Directions

Several extensions are planned for future work, including: 

- Interactive rhythm-aware prompting and control  
- Subjective listening studies and perceptual evaluation  

These directions aim to further explore how explicit rhythmic structure can support controllable and expressive music generation.

---

## Current Status

- Core architecture and training pipeline completed  
- Objective evaluation finalized  



<p class="musicgen-rhythm-credits"><strong>Researchers</strong><br>Changda Ma · Govinda Madhava BS · Lennon Seiders · Sunshiyu Wang<br><small>Georgia Institute of Technology · 2026</small></p>

<details class="draft-request">
  <summary><span>Research paper <b>1</b></span><span class="draft-request-chevron" aria-hidden="true"></span></summary>
  <div class="draft-request-list">
    <article>
      <div><small>Research manuscript</small><strong>MusicGen-Rhythm: Extending MusicGen with Audio-Derived Beat- and Tempo-Aware Conditioning</strong></div>
      <a href="mailto:cma326@gatech.edu?subject=Request%20for%20MusicGen-Rhythm%20Paper&body=Hello%20Changda%2C%0A%0AI%20would%20like%20to%20request%20the%20MusicGen-Rhythm%20paper.%0A%0AThank%20you.">Request PDF ↗</a>
    </article>
    <p>The manuscript is available by email while it is under review.</p>
  </div>
</details>
