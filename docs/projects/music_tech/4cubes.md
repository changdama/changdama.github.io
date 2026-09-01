<div class="fourcubes-page" markdown>

## From ARCube to a shared instrument

4CUBES is the multi-performer successor to [ARCube](https://l42i.music.gatech.edu/arcube/), an XR musical instrument for manipulating sound through virtual objects. The original system centered on one performer and one headset. This research asks a larger question: **what changes when an XR instrument becomes a shared musical ecology?**

The project connects four performers, four headsets, live instruments, a spatial-audio backend, and a loudspeaker array. Each performer can control four virtual sound objects, creating sixteen independently processed and spatialized sources. Their actions are not isolated: movement reorganizes a visible swarm field and becomes part of a collective audiovisual structure.

<figure class="fourcubes-figure fourcubes-figure-wide">
  <img src="/assets/projects/4cubes/system-architecture.png" alt="Overall workflow of 4CUBES, from four musicians and Meta Quest headsets through the OSC PatchBay to the spatial audio system">
  <figcaption>Overall 4CUBES workflow: performers and XR controllers, OSC routing, audio processing, and spatial reproduction. Extracted from the research draft.</figcaption>
</figure>

## One system, three intertwined layers

<div class="fourcubes-grid" markdown>

<div class="fourcubes-card" markdown>
<span class="fourcubes-number">01</span>
### Perform
Four Meta Quest 3 headsets provide in-world access to position, rotation, and spherical controls. A wrist-mounted menu lets each performer set an IP address, port, and unique ID without leaving XR. Compact haptic joysticks offer an alternate control path when a musician's hands are occupied.
</div>

<div class="fourcubes-card" markdown>
<span class="fourcubes-number">02</span>
### Relate
Four main spheres act as structural anchors. A relational layer computes their changing distances and edges; a swarm layer distributes 150 shadow particles across that graph. Close relationships form larger, denser clusters, while distant relationships become smaller and sparse. Moving one sphere can reorganize the entire field.
</div>

<div class="fourcubes-card" markdown>
<span class="fourcubes-number">03</span>
### Spatialize
OSC streams are processed in SuperCollider through performer-specific effects including pitch shifting, feedback delay, spectral freezing, and granular processing. Sources are encoded into a 32-channel Higher-Order Ambisonics field and decoded for the room's loudspeaker layout.
</div>

</div>

<div class="fourcubes-gallery fourcubes-gallery-pair">
  <figure><img src="/assets/projects/4cubes/xr-menu.png" alt="Network configuration menu attached to a virtual hand in the XR environment"><figcaption>Wrist-accessible network menu</figcaption></figure>
  <figure><img src="/assets/projects/4cubes/haptic-circuit.png" alt="Circuit diagram for the compact haptic joystick controller"><figcaption>Compact joystick controller circuit</figcaption></figure>
</div>

<div class="fourcubes-gallery fourcubes-gallery-pair">
  <figure><img src="/assets/projects/4cubes/xr-swarm-near.png" alt="Four main spheres and dense shadow particles shown close together in XR"><figcaption>Dense swarm relationships at close proximity</figcaption></figure>
  <figure><img src="/assets/projects/4cubes/xr-swarm-far.png" alt="Four main spheres and dispersed shadow particles shown farther apart in XR"><figcaption>Sparser swarm relationships at greater distance</figcaption></figure>
</div>

## Signal architecture

<div class="fourcubes-flow" aria-label="System signal flow"><div><b>XR + instruments</b><small>gesture · position · audio</small></div><i>→</i><div><b>OSC PatchBay</b><small>inspect · scale · route</small></div><i>→</i><div><b>SuperCollider</b><small>effects · spatial encoding</small></div><i>→</i><div><b>Speaker field</b><small>shared immersive sound</small></div></div>

The OSC PatchBay sits between the XR interface and audio engine. Each route can display an incoming value, remap it using `output = input × scale + offset`, assign a new OSC address, and forward it to a chosen IP and port. This makes a dense performance network visible and adjustable while it is running, and separates interface design from backend mapping.

<figure class="fourcubes-figure">
  <img src="/assets/projects/4cubes/osc-patchbay.png" alt="OSC PatchBay interface with routing rows for input addresses, live values, scale, offset, output addresses, IP addresses, and ports">
  <figcaption>The OSC PatchBay exposes live values and the receive–transform–forward path for each route.</figcaption>
</figure>

Headset messages follow a consistent structure—`/quest/ID/xyz`, `/quest/ID/pry`, and `/quest/ID/aed`—with an object number identifying one of four spheres. Wireless ADB and scrcpy workflows connect and monitor the four headsets in parallel, while reserved local IP addresses keep device identities stable.

<figure class="fourcubes-figure">
  <img src="/assets/projects/4cubes/ambisonics-decoder.png" alt="Spatial audio decoder interface visualizing loudspeaker positions and an ambisonic sound field">
  <figcaption>Ambisonics decoding maps the multichannel sound field to the physical loudspeaker system.</figcaption>
</figure>

## Performance study

The system was deployed in Georgia Tech's L42I lab with a 15-loudspeaker spatial audio setup. A guitar, bass, violin, and voice ensemble performed an approximately three-minute improvisation while wearing four Quest 3 headsets. The swarm sustained an active, pad-like spatial texture between deliberate gestures, allowing the system to remain musically present while performers focused on their acoustic instruments.

The study also exposed a productive design challenge: the same gesture is not equally accessible to every instrumentalist. A violinist, for example, has fewer opportunities to grab a virtual object while bowing. This motivates instrument-specific mappings, alternative controllers, and interaction techniques that demand less precise mid-performance grabbing.

## Research trajectory

The first draft establishes the networked ensemble: multi-headset identity, menu-based OSC setup, haptic control, live monitoring, performer-specific processing, and the Ambisonics pipeline. The second expands that infrastructure into a relational instrument through the swarm field and OSC PatchBay.

Next steps include deeper cross-headset state sharing, stronger mappings between swarm density and timbral or spatial parameters, more accessible control modalities, and systematic performer and audience evaluation. Together, these directions move 4CUBES from four connected controllers toward a distributed instrument whose behavior emerges from the ensemble.

<p class="fourcubes-credits"><strong>Researchers</strong><br>Changda Ma · Canting Zhu · Henrik von Coler<br><small>Georgia Institute of Technology · L42I</small></p>

<details class="draft-request">
  <summary><span>Research drafts <b>2</b></span><span class="draft-request-chevron" aria-hidden="true"></span></summary>
  <div class="draft-request-list">
    <article>
      <div><small>Draft 01</small><strong>4CUBES: Integrating Menu-Based Network, Haptic, and Multi-Headset Streaming for Collaborative XR Musical Instruments</strong></div>
      <a href="mailto:cma326@gatech.edu?subject=Request%20for%204CUBES%20Draft%2001&body=Hello%20Changda%2C%0A%0AI%20would%20like%20to%20request%204CUBES%20Draft%2001.%0A%0AThank%20you.">Request PDF ↗</a>
    </article>
    <article>
      <div><small>Draft 02</small><strong>4 Cubes: A Swarm-Based XR Musical System with an OSC Patch</strong></div>
      <a href="mailto:cma326@gatech.edu?subject=Request%20for%204CUBES%20Draft%2002&body=Hello%20Changda%2C%0A%0AI%20would%20like%20to%20request%204CUBES%20Draft%2002.%0A%0AThank%20you.">Request PDF ↗</a>
    </article>
    <p>The drafts are available by email while the research is in progress.</p>
  </div>
</details>

</div>
