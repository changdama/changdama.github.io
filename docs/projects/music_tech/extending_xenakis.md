<div class="xenakis-page" markdown>

<p class="xenakis-kicker">Architectural sonification · Generative music · Audiovisual system · 2026</p>

# Extending Xenakis: From Architectural Geometry to Sonification of the Philips Pavilion

<p class="xenakis-deck">A computational system that reverses Xenakis’s historical music-to-architecture process, treating the completed Philips Pavilion as a score for orchestral sound and real-time visualization.</p>

## Reversing the historical arrow

Iannis Xenakis translated the glissando trajectories of *Metastaseis* into the ruled-surface logic that shaped the Philips Pavilion. This project asks what happens when that relationship runs in reverse: rather than treating architecture as music’s static outcome, it extracts the Pavilion’s geometry and lets that structure generate a temporal composition.

<figure class="xenakis-figure xenakis-workflow"><img src="/assets/projects/extending-xenakis/workflow.webp" alt="System diagram comparing Xenakis's historical music-to-architecture process with the project's reverse architecture-to-music process"><figcaption>The project preserves the shared logic of lines, motion, density, and structure while reversing the direction from architecture back to music.</figcaption></figure>

## Geometry becomes a score

The Pavilion was reconstructed in Rhino and Grasshopper as **nine ruled surfaces**. Each surface was subdivided into 20 interpolated structural lines. Four evenly spaced lines per surface were then retained as the musical backbone, producing 36 trajectories for a 36-voice string ensemble.

<div class="xenakis-geometry">
  <figure><img src="/assets/projects/extending-xenakis/ruling-lines.webp" alt="Interpolated ruling lines across the nine surfaces of the Philips Pavilion"><figcaption>Interpolated ruling lines recover the Pavilion’s continuous geometric structure.</figcaption></figure>
  <figure><img src="/assets/projects/extending-xenakis/sampled-points.webp" alt="3357 colored sampling points extracted from the Philips Pavilion surfaces"><figcaption>3,357 sampled points retain the identity of the nine surface groups.</figcaption></figure>
</div>

The system does not simply map every coordinate to a note. It interprets the geometry through three complementary musical behaviors:

<div class="xenakis-layers">
  <div><span>MOTION</span><h3>String glissandi</h3><p>Line length controls duration; vertical displacement controls the direction and range of continuous pitch bending. Twelve violins, eight violas, eight cellos, and eight double basses trace the selected lines.</p></div>
  <div><span>STASIS</span><h3>Energy blocks</h3><p>All sampled points are divided into five vertical strata. Local point density determines the duration of synchronized string tremolo blocks after the glissandi arrive at their endpoints.</p></div>
  <div><span>EVENT</span><h3>Brass and woodwinds</h3><p>A reduced point set drives nine sparse instrumental tracks. Height becomes pitch in G major, horizontal position becomes quantized onset time, and depth shapes density and distribution.</p></div>
</div>

## A deterministic audiovisual instrument

Python converts the architectural datasets into MIDI, which is orchestrated, spatially positioned, mixed, and rendered in Ableton Live. A synchronized Matplotlib animation uses the same global timeline, so every audible event also activates its originating line, endpoint, block, or spatial point.

<figure class="xenakis-figure"><img src="/assets/projects/extending-xenakis/glissando-visualization.webp" alt="Real-time three-dimensional visualization during the string glissando phase"><figcaption>During the opening phase, moving heads and short trails reveal each string voice traversing its architectural trajectory.</figcaption></figure>

<div class="xenakis-stack" aria-label="Technical implementation pipeline">
  <div><b>Rhino + Grasshopper</b><small>reconstruct surfaces · extract lines and points</small></div><i>→</i>
  <div><b>Python</b><small>geometry processing · mapping · MIDI generation</small></div><i>→</i>
  <div><b>Ableton Live</b><small>orchestration · spatial placement · rendering</small></div><i>→</i>
  <div><b>Matplotlib</b><small>synchronized real-time 3D visualization</small></div>
</div>

<figure class="xenakis-figure xenakis-wide"><img src="/assets/projects/extending-xenakis/audiovisual-system.webp" alt="Philips Pavilion real-time visualization alongside the orchestration session in Ableton Live"><figcaption>The shared timeline joins the architectural visualization and multi-track musical arrangement.</figcaption></figure>

## Watch the system

<div class="xenakis-video">
  <iframe src="https://www.youtube-nocookie.com/embed/zSj_I4n7Yqg" title="Extending Xenakis audiovisual sonification video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

## Contribution and next direction

The project frames architectural geometry as a performable musical structure rather than a passive container for sound. Continuous lines create motion, spatial density creates stasis, and discrete points create events; together they make the Pavilion perceivable as an unfolding audiovisual form.

The current system uses fixed-density geometric sampling and a historically informed orchestral palette, which can simplify local curvature and limit how strongly other architectural styles might speak in their own musical language. Future work will investigate curvature-adaptive sampling, alternative mapping grammars, additional buildings, and immersive VR/AR interaction in which listeners navigate the Pavilion while its geometry responds through sound.

<p class="xenakis-credits"><strong>Authors</strong><br>Changda Ma · Sunshiyu Wang · Canting Zhu · Alexandria Smith<br><small>Rhino · Grasshopper · Python · MIDI · Ableton Live · Matplotlib</small></p>

<details class="publication-dock">
  <summary><span>Published article <b>1</b></span><span class="publication-dock-chevron" aria-hidden="true"></span></summary>
  <div class="publication-dock-content">
    <p><strong>Changda Ma, Sunshiyu Wang, Canting Zhu, and Alexandria Smith. 2026.</strong> Extending Xenakis: From Architectural Geometry to Sonification of the Philips Pavilion. <em>arXiv preprint arXiv:2607.06589.</em></p>
    <nav aria-label="Publication links">
      <a href="https://arxiv.org/abs/2607.06589" target="_blank" rel="noopener">arXiv page ↗</a>
      <a href="https://doi.org/10.48550/arXiv.2607.06589" target="_blank" rel="noopener">DOI ↗</a>
      <a href="https://arxiv.org/pdf/2607.06589" target="_blank" rel="noopener">PDF ↗</a>
      <a href="https://youtu.be/zSj_I4n7Yqg" target="_blank" rel="noopener">Video ↗</a>
    </nav>
  </div>
</details>

</div>
