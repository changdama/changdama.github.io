# MusicGen-Rhythm
**Rhythm-Aware Conditioning for Text-to-Music Generation**

MusicGen-Rhythm explores rhythm-aware conditioning strategies for text-to-music generation by extending **MusicGen-Small** with **audio-derived rhythmic representations**.  
The project investigates whether explicit rhythmic cues extracted from audio can improve temporal coherence and rhythmic stability beyond text-only prompting, while keeping the MusicGen backbone frozen.

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
- Audio: 32 kHz, 30-second clips  
- Training & evaluation: Google Colab (GPU)  

Quantitative evaluations and ablation studies are reported in the accompanying paper under preparation.  
(Detailed results will be added to this page after publication.)

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
- Paper submission in preparation  

> *This page presents methodological design only.  
Results and conclusions may change prior to formal publication.*
