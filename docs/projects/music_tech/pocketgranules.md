<div class="pocketgranules-page" markdown>

<p class="pg-kicker">Audio software · Granular synthesis · DSP · Modulation</p>

# PocketGranules: Multihead Granulator

<p class="pg-deck">A real-time granular instrument that divides one sound source across five independently controlled grain heads, then reshapes each stream through effects and modulation.</p>

<figure class="pg-hero"><img src="/assets/projects/pocketgranules/interface.webp" alt="PocketGranules interface with waveform, grain controls, and four-slot effects chain"><figcaption>The compact interface combines waveform navigation, per-head grain controls, a four-slot effects chain, and access to the modulation system.</figcaption></figure>

## My contribution

My primary responsibility was the design of the **DSP filter** and **LFO system**. I focused on how the filter should behave as a musical processor within each grain head, and how low-frequency modulation could move both grain and effect parameters without interrupting real-time audio.

### DSP filter design

The filter is placed in each head’s post-grain effects chain, after the active grains for that head have been summed into a local stereo buffer. This keeps the processor expressive while avoiding the cost of instantiating a separate filter for every grain.

The design uses a topology-preserving state-variable filter with three selectable responses:

- **Low-pass** for reducing upper-frequency detail and softening dense textures.
- **High-pass** for removing low-frequency energy and creating lighter grain layers.
- **Band-pass** for isolating a moving spectral region.

Cutoff and resonance are exposed as automatable parameters and modulation targets. The state-variable structure remains stable while those values change, which is important when an LFO continuously sweeps the cutoff during playback.

### LFO design

The modulation system provides **five independent LFOs**. Each offers sine, triangle, rising saw, falling saw, square, and sample-and-hold shapes, with controls for rate, depth, and phase. Rates can run freely or synchronize to the host tempo.

An LFO produces a normalized control signal that is routed through the modulation engine to grain or effects parameters. Each connection stores its own amount and can operate in bipolar or unipolar mode, allowing the same source to create subtle motion on one control and a much wider sweep on another.

<div class="pg-mod-flow" aria-label="LFO modulation path">
  <div><span>SOURCE</span><b>LFO shape</b><small>sine · triangle · saw · square · sample & hold</small></div>
  <i>→</i>
  <div><span>TIMING</span><b>Rate and phase</b><small>free-running or synchronized to the host tempo</small></div>
  <i>→</i>
  <div><span>ROUTING</span><b>Connection amount</b><small>per-target depth with bipolar or unipolar behavior</small></div>
  <i>→</i>
  <div><span>TARGET</span><b>Grain or FX control</b><small>including filter cutoff and resonance</small></div>
</div>

## Instrument architecture

PocketGranules can process live input or a loaded audio file. Five grain engines operate in parallel, each with independent position, spread, rate, duration, pitch, shape, gain, reverse, and freeze controls. Active grains are mixed inside their head before entering a configurable four-slot chain containing filter, bitcrusher, delay, and reverb processors.

For each audio block, the software follows this path:

1. Capture incoming audio in the ring buffer and update the modulation sources.
2. Apply modulation to the base values of connected grain and effects parameters.
3. Schedule and render active grains in each of the five heads.
4. Process every head through its own effects chain.
5. Sum the heads and apply the master gain and dry/wet mix.

## Designing for real-time use

The instrument is implemented in C++ with JUCE. Grain voices are preallocated, parameter state is managed through JUCE’s `AudioProcessorValueTreeState`, and modulation sources advance at block rate. These decisions keep allocation and interface work away from the audio thread while leaving the main sound controls automatable from a DAW.

The current open-source version supports VST3 and AU builds and includes presets, tempo synchronization, a step sequencer, an envelope follower, and modulation routing to grain and effects controls.

<div class="pg-resources">
  <a href="https://github.com/molgenzo/CerberusGran" target="_blank" rel="noopener"><strong>View source on GitHub</strong><small>CerberusGran repository and current PocketGranules codebase</small></a>
</div>

<p class="pg-credits"><strong>My contribution</strong><br>Changda Ma · DSP filter design · LFO design<br><br><strong>Project team</strong><br>Ishaan Jagyasi · Team Leader<br>Caleb Adams · Youhan Li · Changda Ma · Sunshiyu Wang<br><small>JUCE · C++17 · VST3 · AU · Real-time audio</small></p>

</div>
