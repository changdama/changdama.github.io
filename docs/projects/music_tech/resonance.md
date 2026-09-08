<div class="resonance-page" markdown>

# Resonance

<p class="resonance-meta">ONGOING RESEARCH · PHYSIOLOGICAL COMPUTING · GENERATIVE MUSIC · SPATIAL AUDIO</p>

<p class="resonance-deck">Exercise is not just burning calories—it is writing a song with your body.</p>

Resonance is a physiology-music feedback system in which bodily activity becomes material for musical creation. A Polar H10 reads the runner's heart activity and motion; a signal pipeline derives heart-rate dynamics, HRV, cadence, and breathing events; and an AI music engine continuously reshapes the music in response. The goal is to move exercise listening beyond a fixed playlist: the body becomes both a source of data and a way to perform.

<div class="resonance-status"><strong>Current milestone</strong><span>The end-to-end single-user prototype is working and demonstrated below. Shared multi-user composition and spatialized contribution mapping are the next research phase.</span></div>

<figure class="resonance-figure resonance-lead">
  <img src="/assets/projects/resonance/resonance-interface.png" alt="Resonance web interface for choosing music style, mood, duration, and exercise goals before connecting a Polar H10 sensor">
  <figcaption>The current web interface begins with musical intent, session length, and exercise goals before connecting to the physiological stream.</figcaption>
</figure>

## A run becomes a composition

<div class="resonance-moments" markdown>

<div markdown>
<span>BEFORE</span>
### Set an intention
The runner chooses a style, mood, duration, and goal structure. These preferences establish the musical world without fixing the resulting song.
</div>

<div markdown>
<span>DURING</span>
### Co-create through movement
Heart rate, HRV, cadence, and breathing continuously steer musical energy, density, brightness, tempo, and structure. Deliberate bodily events become creative gestures.
</div>

<div markdown>
<span>AFTER</span>
### Hear the run as a song
The system preserves the session's musical segments and physiological events, then reorganizes them into a more complete composition that reflects the run's energy arc.
</div>

</div>

## Single-user prototype demo

<figure class="resonance-video">
  <div>
    <iframe src="https://www.youtube-nocookie.com/embed/QOOtaH7skRM" title="Resonance single-user prototype demo" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
  </div>
  <figcaption>Current Resonance single-user workflow: physiological sensing, music steering, session structure, and post-run output.</figcaption>
</figure>

## The closed loop

<div class="resonance-flow" aria-label="Resonance system flow">
  <div><b>Body</b><small>heart · breath · cadence</small></div>
  <i>→</i>
  <div><b>Polar H10</b><small>BLE · RR · acceleration</small></div>
  <i>→</i>
  <div><b>Signal pipeline</b><small>smooth · detect · interpret</small></div>
  <i>→</i>
  <div><b>AI music</b><small>prompt · steer · stream</small></div>
  <i>→</i>
  <div><b>Listener</b><small>hear · move · respond</small></div>
</div>

The software is organized around an event-driven signal bus. BLE callbacks publish raw heart-rate, RR-interval, and acceleration data. Independent processors derive smoothed heart rate, change and trend, RMSSD, cadence lock, breathing rate, deep breaths, and breath holds. A prompt composer translates those values into weighted musical descriptions, while a steering controller reacts immediately to meaningful events and adapts more gradually during stable periods.

Google Lyria RealTime receives those physiological prompts over WebSocket and streams generated PCM audio back to the browser. A three-second client-side jitter buffer and scheduled Web Audio playback absorb irregular network delivery, while warm-up, fallback steering, and keepalive messages reduce cold-start and mid-session silence.

## The body is both data and control

<div class="resonance-signals" markdown>

<div markdown>
### Continuous state
Signals that are difficult to control directly—natural heart-rate variation and HRV—describe exertion and recovery. They influence energy, density, brightness, and the larger musical trajectory.
</div>

<div markdown>
### Creative gestures
Signals a runner can intentionally shape become compositional commands. Deep breathing can mark a motif, cadence locking can anchor tempo, and a breath hold can initiate a transition or stylistic branch.
</div>

</div>

This distinction is central to Resonance. The system does not simply sonify a dashboard of biometric values; it creates an instrument whose controls are already embedded in the activity itself.

## Exercise form becomes musical form

The prototype maps the temporal arc of a workout onto recognizable musical sections. Warm-up becomes an **Intro**, acceleration establishes a **Verse**, sustained training opens into a **Chorus**, peak effort creates a **Bridge**, and recovery resolves as an **Outro**. The web interface exposes these states alongside live metrics and the current prompt, making the relationship between physiology and musical change legible during development.

## Toward shared spatial co-creation

The present demo focuses on one runner and one physiological stream. The next phase asks how two people can write one piece together. One runner might contribute rhythm through heart rate and cadence while another shapes melody and phrasing through breathing and HRV. Both would hear the same composition, but spatial audio could foreground each person's own contribution and locate the partner's musical stem in relation to their physical position.

This duet model establishes a path toward group exercise, distributed partners, and eventually large-scale collective compositions. These multi-user and HRTF spatial-audio features are a research direction, not part of the current single-user demo.

<p class="resonance-authors"><strong>Research and development</strong><br>Changda Ma<br><small>Shokz Technology Internship Project · 2026</small></p>

<nav class="resonance-resources" aria-label="Resonance project links">
  <a href="https://youtu.be/QOOtaH7skRM" target="_blank" rel="noopener"><strong>Watch the demo</strong><small>YouTube</small></a>
  <a href="https://github.com/changdama/Resonance" target="_blank" rel="noopener"><strong>Source repository</strong><small>GitHub</small></a>
  <a href="/assets/projects/resonance/resonance-source.zip"><strong>Download source snapshot</strong><small>ZIP · 140 KB</small></a>
</nav>

</div>
