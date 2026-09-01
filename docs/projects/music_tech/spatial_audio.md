<div class="open-studio-page" markdown>

# Immersive Open Studio: Shared Space, Shared Sound

<p class="open-studio-meta">PUBLISHED RESEARCH · NIME 2026 · SPATIAL AUDIO · PARTICIPATORY PERFORMANCE</p>

Immersive Open Studio turns spatial-audio infrastructure into a shared public platform for interactive audiovisual work. Realized at the Underground Art Center in downtown Atlanta, the course-based studio supported five student projects and weekly public showcases. Rather than building a one-off system for a single artwork, the project asks how one adaptable technical environment can support many artists, many works, and repeated public engagement.

<figure class="open-studio-figure open-studio-lead">
  <img src="/assets/projects/open-studio/installation.webp" alt="Since Everyone's a DJ installation at Underground Atlanta with participants, projection, and spatial loudspeakers">
  <figcaption><em>Since Everyone's a DJ</em>, one of five works presented through Immersive Open Studio at Underground Atlanta.</figcaption>
</figure>

## A shared studio, not a single installation

Between October and November 2025, five Georgia Tech student groups—16 participants in total—presented *Immerge*, *Since Everyone's a DJ*, *Audenie*, *MACHINA*, and *Data Mirror: Fragmented Projections of Oneself*. Each project occupied the studio for an approximately 90-minute public interactive session, with work ranging from ocean sonification and short film to techno-futurist performance.

The common infrastructure let artists concentrate on interaction, composition, and audience experience instead of rebuilding the spatial system for every showcase. It also reframed spatial audio as a social practice: shaped by the room, the people who enter it, and the ways it invites participation.

## Infrastructure shaped by the real world

<div class="open-studio-layouts">
  <figure><img src="/assets/projects/open-studio/tunnel-layout.webp" alt="Diagram of the original tunnel installation with three loudspeaker layers and three projectors"><figcaption>Setup I: the original three-layer loudspeaker system and 270° projection field.</figcaption></figure>
  <figure><img src="/assets/projects/open-studio/adapted-layout.webp" alt="Diagram of the adapted second-floor installation with two loudspeaker layers and parallel projections"><figcaption>Setup II: the adapted two-layer system after emergency relocation.</figcaption></figure>
</div>

The first studio occupied a former MARTA tunnel: a 14 × 28 × 8 ft cloth-enclosed room supported by six truss stands. Its three-layer array combined two Neumann KH120 monitors above, ten KH120 monitors at the middle layer, five QSC K10.2 loudspeakers below, and two Alto subwoofers. Three projectors created a 270° field, while a MIDAS M32 console and two Behringer stage boxes managed routing.

After three weeks and three performances, flooding made the subterranean venue unsafe. The team moved the complete installation to a second-floor room, protecting the equipment and audiences while rapidly redesigning around a lower ceiling and different walls. The revised system used ten upper-layer KH120 monitors, two floor loudspeakers, two subwoofers, and two parallel projections. The relocation became a practical test of the project's central premise: reusable infrastructure must also be resilient infrastructure.



## Case study: Since Everyone's a DJ

We examine *Since Everyone's a DJ* as a detailed use case. The work challenges the familiar performer–listener divide by allowing up to four visitors to shape electronic music through body movement and simple hand gestures. Four Intel RealSense D455 depth cameras, arranged at 90-degree intervals, provide room-wide coverage. MediaPipe Hands recognizes one-to-four-finger gestures, while depth and hand position supply continuous control data.

Holding up fingers selects musical voices and phrases. Vertical hand movement changes synthesis and effect parameters; horizontal position controls spatial azimuth; distance controls volume. OSC over UDP sends both continuous and discrete data to the audio and visual systems, creating an accessible walk-up interaction that requires no musical training.

<figure class="open-studio-figure open-studio-camera">
  <img src="/assets/projects/open-studio/camera-tracking.webp" alt="Four-camera audience tracking setup using Intel RealSense depth cameras mounted around a central stand">
  <figcaption>Four-camera tracking station at the center of the performance space.</figcaption>
</figure>

<figure class="open-studio-video">
  <div class="open-studio-video-frame">
    <iframe src="https://www.youtube-nocookie.com/embed/mCMO07b-WYw" title="Since Everyone's a DJ — gesture video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
  </div>
  <figcaption><em>Since Everyone's a DJ</em> — gesture video.</figcaption>
</figure>

## Audiovisual synthesis

The system combines Ableton Live, Max/MSP, Max for Live, Jitter, Reaper, and the IEM AllRADecoder. A Max patch parses camera OSC streams into four musical groups—bass, chords, lead, and drums—with four instruments per group. Gesture messages switch instruments, while movement controls macros for sequence variation, distortion, wavetable position, filtering, resonance, oscillator mix, and delay.

Audio travels from Ableton to Reaper through BlackHole for Ambisonic spatialization. Jitter receives camera data and audio-derived signals to modulate texture, color, spatial distortion, feedback, and delay. The result is a coupled audiovisual environment in which participation is heard and seen immediately.


<figure class="open-studio-figure open-studio-diagram">
  <img src="/assets/projects/open-studio/system-diagram.webp" alt="System implementation diagram connecting RealSense cameras, OSC, Max, Ableton Live, Reaper, Jitter, projectors, and spatial loudspeakers">
  <figcaption>System implementation: camera tracking and OSC connect the participants to sound synthesis, spatialization, and projected visuals.</figcaption>
</figure>

<figure class="open-studio-video">
  <div class="open-studio-video-frame">
    <iframe src="https://www.youtube-nocookie.com/embed/uW819SYslCc" title="Since Everyone's a DJ — performance video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
  </div>
  <figcaption><em>Since Everyone's a DJ</em> — performance video.</figcaption>
</figure>

## What the public experience revealed

Participants commonly watched others first, imitated their gestures, and then began exploring independently. The immediate audiovisual response provided a low barrier to entry, but the precise mappings were not always legible: visitors could hear that something changed without necessarily identifying which layer, timbral parameter, or spatial dimension they controlled.

Continuous changes such as distance-based volume and spatial position were also harder to perceive when four instrumental layers played together. The findings point toward clearer visual feedback, greater contrast between sonic layers, stronger entry cues, and short isolated demonstrations before the full system begins. Future work will also investigate camera handoff zones, low-light tracking, whole-body movement, and more independent audience evaluation.

<p class="open-studio-authors"><strong>Authors</strong><br>Sunshiyu Wang · Changda Ma · Canting Zhu · Gibran Mobarak · Henrik von Coler<br><small>Georgia Institute of Technology · NIME 2026</small></p>

<details class="publication-dock">
  <summary><span>Published article <b>1</b></span><span class="publication-dock-chevron" aria-hidden="true"></span></summary>
  <div class="publication-dock-content">
    <p><strong>Sunshiyu Wang, Changda Ma, Canting Zhu, Gibran Mobarak, and Henrik von Coler. 2026.</strong> Immersive Open Studio: Shared Space, Shared Sound. <em>Proceedings of the International Conference on New Interfaces for Musical Expression.</em></p>
    <nav aria-label="Publication links">
      <a href="https://nime.org/proc/nime2026_68/index.html" target="_blank" rel="noopener">NIME page ↗</a>
      <a href="https://doi.org/10.5281/zenodo.20784215" target="_blank" rel="noopener">DOI ↗</a>
      <a href="http://nime.org/proceedings/2026/nime2026_68.pdf" target="_blank" rel="noopener">PDF ↗</a>
    </nav>
  </div>
</details>

</div>
