<div class="spatial-composition-page" markdown>

# Four Environments: An Interactive Spatial Audio Composition

<p class="spatial-composition-meta">COURSE PROJECT · SPATIAL AUDIO · INTERACTIVE COMPOSITION · 2026</p>

This project treats spatial audio as a performable instrument rather than a fixed playback format. Four environmental scenes—**Water, Valley, City, and Hall**—can be selected in real time while a performer reshapes their density, movement, direction, and depth with a MIDI controller. Each scene combines environmental recordings, localized sound objects, and a pitched drone layer into a continuously evolving spatial composition.

<figure class="spatial-composition-figure spatial-composition-lead">
  <img src="/assets/projects/spatial-audio-composition/reaper-routing.png" alt="REAPER project showing the Water, Valley, City, and Hall scene folders and their multichannel tracks">
  <figcaption>The REAPER session organizes four sound environments as independent scenes inside a shared 16-channel Ambisonics workflow.</figcaption>
</figure>

## Four environments, one instrument

<div class="spatial-composition-scenes" markdown>

<div markdown>
<span>01</span>
### Water
Muffled, diffuse, and enveloping. A wide underwater pad surrounds localized whale calls, with softened high frequencies and a slowly changing spatial field.
</div>

<div markdown>
<span>02</span>
### Valley
Open, deep, and distant. Longer reverberation and discrete delays suggest reflections returning from far surfaces.
</div>

<div markdown>
<span>03</span>
### City
Dense, lateral, and hard-edged. Short reflections and moving point sources evoke traffic, signals, and an active urban sound field.
</div>

<div markdown>
<span>04</span>
### Hall
Direct, warm, and controlled. Early reflections and concert-hall reverberation keep musical material present while extending it into the room.
</div>

</div>

## Performance-driven signal architecture

Each scene contains four sound objects with complementary spatial roles: a continuous ambience, one or two localized sources, and an object that emphasizes motion or depth. An Akai MPK Mini MK2 provides a consistent performance vocabulary across the complete work. Four pads select scenes; shared knobs control the position of equivalent sound types; additional controls shape EQ, chorus, and scene volume.

<div class="spatial-composition-flow" aria-label="Spatial audio signal path">
  <div><b>MIDI performance</b><small>scene selection · position · effects</small></div>
  <i>→</i>
  <div><b>Sound objects</b><small>ambience · point sources · drones</small></div>
  <i>→</i>
  <div><b>Scene bus</b><small>reverb · EQ · delay</small></div>
  <i>→</i>
  <div><b>3rd-order HOA</b><small>16-channel AMIX bus</small></div>
  <i>→</i>
  <div><b>Dual decode</b><small>headphones · loudspeaker array</small></div>
</div>

The production system is built in REAPER with the IEM Plug-in Suite. `StereoEncoder` places and widens objects; `FdnReverb` establishes the acoustic character of each scene; `MultiEQ` shapes its spectral identity; and `DualDelay` creates discrete reflections where they matter. Every spatial track and bus remains at 16 channels through a shared third-order HOA mix. The result is decoded either binaurally for headphones or through `AllRADecoder` for the spatial loudspeaker system in Couch 204.

## Binaural composition

<div class="spatial-composition-listen">
  <div>
    <span aria-hidden="true">◉</span>
    <p><strong>Listen with headphones</strong><small>Binaural render · 4:08</small></p>
  </div>
  <audio controls preload="metadata">
    <source src="/assets/projects/spatial-audio-composition/binaural-composition.ogg" type="audio/ogg">
    Your browser does not support embedded audio. <a href="/assets/projects/spatial-audio-composition/binaural-composition.ogg">Download the binaural render</a>.
  </audio>
</div>

## From REAPER to Pure Data

To make the system more open and extensible, the project also explores a Pure Data implementation. The prototype recreates the Water scene from the ground up: it loads the underwater ambience and whale samples, exposes azimuth and elevation controls, manages source volume, and routes a 16-channel spatial field through the IEM plug-ins using `vstplugin~`.

<figure class="spatial-composition-figure">
  <img src="/assets/projects/spatial-audio-composition/pure-data-system.png" alt="Pure Data patch with water-pad position and volume controls, whale-sound triggers, and a 16-channel Ambisonics signal network">
  <figcaption>The open-source Pure Data prototype establishes the Water scene's playback, control, and HOA routing.</figcaption>
</figure>

<figure class="spatial-composition-video">
  <video controls playsinline preload="metadata" poster="/assets/projects/spatial-audio-composition/pure-data-demo.jpg">
    <source src="/assets/projects/spatial-audio-composition/pure-data-demo.mov" type="video/quicktime">
    Your browser cannot play this video. <a href="/assets/projects/spatial-audio-composition/pure-data-demo.mov">Download the Pure Data demonstration</a>.
  </video>
  <figcaption>Pure Data prototype demonstration.</figcaption>
</figure>

## Continuing the system

The REAPER version establishes the complete composition and its live MIDI workflow; the Pure Data version establishes a reusable open-source foundation. Future development can extend the remaining three scenes, add a general-purpose sampler, integrate MIDI directly, and create new relationships between musical material and spatial movement.

<p class="spatial-composition-authors"><strong>Creators</strong><br>Sunshiyu Wang · Changda Ma<br><small>Georgia Institute of Technology · 2026</small></p>

<nav class="spatial-composition-resources" aria-label="Project downloads">
  <a href="/assets/projects/spatial-audio-composition/final-documentation.pdf" target="_blank"><strong>Final documentation</strong><small>PDF · 1.1 MB</small></a>
  <a href="/assets/projects/spatial-audio-composition/pure-data-project.zip"><strong>Pure Data project</strong><small>Patch + audio · ZIP · 9.6 MB</small></a>
  <a href="/assets/projects/spatial-audio-composition/pure-data-demo.mov"><strong>Pure Data demo</strong><small>Video · MOV · 44 MB</small></a>
</nav>

</div>
