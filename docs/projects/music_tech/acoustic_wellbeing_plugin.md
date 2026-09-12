<div class="acoustic-plugin-page" markdown>

<p class="ap-kicker">Acoustic simulation · Grasshopper plugin · Evidence-based design · 2025</p>

# Noise & Wellbeing: A Grasshopper Acoustic Simulation Plugin

<p class="ap-deck">A design-support tool that makes environmental noise visible—connecting room geometry, sound sources, and material behavior to spatial maps that architects can read and act on.</p>

## My role: Plugin design

My primary contribution was designing the acoustic plugin: its input and output model, simulation workflow, and visualization logic. The tool translates acoustic calculations into design-readable noise, sleep-disturbance, and mental-health-risk heat maps inside Rhino and Grasshopper.

<figure class="ap-hero"><img src="/assets/projects/acoustic-wellbeing-plugin/plugin-interface.webp" alt="Grasshopper canvas showing the custom Noise Simulation component and its inputs and outputs"><figcaption>The custom Noise Simulation component brings geometry, acoustic parameters, and three spatial outputs into one Grasshopper workflow.</figcaption></figure>

## From measurements to a spatial model

The plugin was developed within a wider study of **Smith Residence Hall** and the relationship between the built environment and student wellbeing. The team measured sound at ten indoor and outdoor locations across five weekdays and recorded overnight sound levels in two dorm rooms. These observations showed where a point reading was informative—but also why designers need a continuous view of how noise moves through a plan.

The plugin turns that gap into a workflow: measured or assumed source levels are placed in a Rhino plan, walls receive transmission-loss and absorption values, and the component evaluates the acoustic field across a configurable grid.

<div class="ap-flow" aria-label="Acoustic simulation workflow">
  <div><span>01 · INPUT</span><b>Spatial model</b><small>boundary, walls, source locations, and source levels</small></div>
  <i>→</i>
  <div><span>02 · MATERIAL</span><b>Acoustic behavior</b><small>wall absorption, transmission loss, and air attenuation</small></div>
  <i>→</i>
  <div><span>03 · SIMULATE</span><b>Sound paths</b><small>direct sound, wall crossings, and first-order reflections</small></div>
  <i>→</i>
  <div><span>04 · READ</span><b>Spatial feedback</b><small>noise and wellbeing-risk meshes for design iteration</small></div>
</div>

## What the plugin computes

<div class="ap-features">
  <div><span>DIRECT FIELD</span><h3>Distance-aware sound level</h3><p>Sound pressure level falls with source distance and optional air absorption. Multiple sources are combined in the energy domain.</p></div>
  <div><span>ENCLOSURE</span><h3>Walls and materials</h3><p>Sound paths accumulate transmission loss when they cross walls; reflection energy responds to material absorption and incidence angle.</p></div>
  <div><span>REFLECTIONS</span><h3>First-order image sources</h3><p>A mirror-source method estimates a first reflection while checking wall extents, obstructions, and source–receiver sidedness.</p></div>
  <div><span>OUTPUTS</span><h3>Three analysis meshes</h3><p>The component produces absolute dB, Sleep Disturbance Index, and Mental Health Index meshes alongside grid-level numeric values.</p></div>
</div>

## Field-informed design context

<figure class="ap-figure"><img src="/assets/projects/acoustic-wellbeing-plugin/sampling-map.webp" alt="Smith Residence Hall floor plan with indoor and outdoor noise sampling positions"><figcaption>Ten recurring sampling locations connected exterior traffic exposure with entrance, corridor, study, lobby, and dorm conditions.</figcaption></figure>

Across the measurement period, overall average levels increased from **54.5 dBA in the morning** to **55.3 dBA at noon** and **56.8 dBA in the evening**. Exterior locations were generally the loudest, while door movement and nearby activity produced short indoor peaks that daily averages alone could conceal.

## Indoor noise across the day

The following simulations are a central output of the plugin. Period-specific indoor noise inputs were mapped across the same floor plan so that the overall pattern and the morning, noon, and evening conditions can be compared directly. Warmer colors identify areas of higher modeled exposure, particularly around circulation junctions, entrances, and shared spaces; cooler colors indicate more acoustically protected areas.

<figure class="ap-period-figure"><img src="/assets/projects/acoustic-wellbeing-plugin/indoor-all.webp" alt="Combined indoor noise simulation across Smith Residence Hall"><figcaption>All indoor observations combined: a summary view of recurring noise paths and hotspots.</figcaption></figure>

### Morning

<figure class="ap-period-figure"><img src="/assets/projects/acoustic-wellbeing-plugin/indoor-morning.webp" alt="Morning indoor noise simulation across Smith Residence Hall"><figcaption>Morning indoor noise field.</figcaption></figure>

### Noon

<figure class="ap-period-figure"><img src="/assets/projects/acoustic-wellbeing-plugin/indoor-noon.webp" alt="Noon indoor noise simulation across Smith Residence Hall"><figcaption>Noon indoor noise field.</figcaption></figure>

### Evening

<figure class="ap-period-figure"><img src="/assets/projects/acoustic-wellbeing-plugin/indoor-evening.webp" alt="Evening indoor noise simulation across Smith Residence Hall"><figcaption>Evening indoor noise field, with broader high-level regions around circulation and shared spaces.</figcaption></figure>

## Measurement detail

<div class="ap-gallery ap-gallery-stacked">
  <figure><img src="/assets/projects/acoustic-wellbeing-plugin/noise-analysis.webp" alt="Noise heat map and detailed sound-level traces from Smith Residence Hall"><figcaption>Spatial averages were paired with detailed traces to reveal short events and local differences.</figcaption></figure>
  <figure><img src="/assets/projects/acoustic-wellbeing-plugin/overnight-noise.webp" alt="Overnight sound-level recordings from rooms 225 and 444"><figcaption>Overnight logging showed contrasting acoustic backgrounds: approximately 45 dBA in Room 225 and 35 dBA in Room 444 during the sleep period.</figcaption></figure>
</div>

## From acoustic output to design decisions

The heat maps let a designer test where sound sources, partitions, and material changes may alter exposure. In the Smith Hall study, this supported recommendations such as quieter door hardware, improved seals, acoustic buffers near entrances and stairs, and reconsidering room functions near recurring noise paths.

The wellbeing layers are best understood as **comparative design indicators**. They map excess level above a 30 dB baseline to normalized sleep-disturbance and mental-health-risk proxies, helping compare options within the same model rather than making a diagnosis or certifying code compliance.

## Scope and future development

This version is a research prototype based on simplified two-dimensional geometry, broadband levels, first-order reflections, and heuristic wellbeing mappings. It does not yet model diffraction, late reverberation, frequency-dependent propagation, or uncertainty in source and material data.

Future development would add octave-band inputs, calibrated validation against measured rooms, higher-order room-acoustic behavior, uncertainty ranges, and a packaged interface for reuse across projects.

<div class="ap-resources">
  <a href="/assets/projects/acoustic-wellbeing-plugin/Acoustic_Wellbeing_Plugin.py" download><strong>Download plugin source</strong><small>IronPython script for Rhino / Grasshopper</small></a>
</div>

<p class="ap-credits"><strong>My contribution</strong><br>Changda Ma · Plugin design<br><br><strong>Research team</strong><br>Lauren Callaway · Aubrey Lassetter · Changda Ma · Carson Pitzer · Rakshitha Satish · Breno Veiga · Ziyuan Ye<br><small>Smith Residence Hall · Rhino · Grasshopper · Evidence-based design</small></p>

</div>
