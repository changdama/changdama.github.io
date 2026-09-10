<div class="fragmented-melody-page" markdown>

<p class="fm-kicker">Music perception · Auditory streaming · Melody memory · Exploratory study</p>

# Perceiving a Fragmented Melody

<p class="fm-deck">How does distributing one melodic phrase across different instruments and registers affect a listener’s ability to integrate and remember it?</p>

## The perceptual question

In orchestration and counterpoint, a composer may write one continuous melodic idea while passing its notes between performers. On the page, that line remains coherent. For a listener, however, changes in timbre and register are cues that can separate successive sounds into different auditory streams.

This exploratory experiment tests whether that perceptual fragmentation carries over into memory: **can listeners reconstruct a distributed line as one melody, or do changes of instrument and register make recognition less reliable?**

<div class="fm-concept" aria-label="Research concept">
  <div><span>COMPOSED</span><b>One melodic line</b><small>a continuous eight-bar phrase</small></div>
  <i>→</i>
  <div><span>ORCHESTRATED</span><b>Multiple sound sources</b><small>timbre and register change within the line</small></div>
  <i>→</i>
  <div><span>PERCEIVED</span><b>One stream—or several?</b><small>integration during listening</small></div>
  <i>→</i>
  <div><span>REMEMBERED</span><b>Melody recognition</b><small>three-alternative choice on piano</small></div>
</div>

## Three ways of distributing a melody

Ten eight-bar stimuli were produced in Logic Pro using orchestral string and woodwind timbres. Each phrase stayed in a major or minor key, avoided modulation and modal exchange, and ended on its tonic. The recognition options were rendered with a neutral piano timbre so that the task emphasized remembered pitch structure rather than the original instrumentation.

<div class="fm-conditions">
  <div><span>01 · SOLO</span><h3>Single instrument group</h3><p>One string or woodwind group performs the complete phrase in a high or low register.</p></div>
  <div><span>02 · SHARED REGISTER</span><h3>Two instrument groups</h3><p>Strings and woodwinds alternate short segments while remaining in the same register.</p></div>
  <div><span>03 · CONTRASTING REGISTER</span><h3>Two groups, two registers</h3><p>The line moves between instrument groups while also crossing between high and low registers.</p></div>
</div>

## Listening experiment

Seven participants completed the study remotely in Qualtrics. After a demographic and musical-background questionnaire, each participant heard a stimulus, waited through a ten-second reflection interval, and selected the phrase they believed they had heard from three closely related piano-rendered options.

<div class="fm-procedure" aria-label="Listening experiment procedure">
  <div><b>Listen</b><small>one orchestrated melody</small></div><i>1</i>
  <div><b>Hold</b><small>10-second reflection interval</small></div><i>2</i>
  <div><b>Recognize</b><small>choose among three piano melodies</small></div><i>3</i>
  <div><b>Record</b><small>accuracy and response time</small></div>
</div>

The group was small and musically experienced: all participants reported at least six years of musical experience, most reported more than ten years, and most identified as at least semi-professional musicians. Remote participation improved access but left listening hardware, environment, and attention uncontrolled.

## Results

<div class="fm-results">
  <div class="fm-result-copy">
  <p>Overall recognition accuracy was <strong>58.6%</strong> (participant-level SD = 13.5%), above the 33.3% chance level of a three-option task. Performance changed very little across the three orchestration conditions:</p>
  <table>
    <thead><tr><th>Condition</th><th>Accuracy</th><th>Binomial p</th></tr></thead>
    <tbody>
      <tr><td>Single instrument</td><td><strong>60.7%</strong></td><td>0.004</td></tr>
      <tr><td>Shared register</td><td><strong>57.1%</strong></td><td>0.085</td></tr>
      <tr><td>Contrasting register</td><td><strong>57.1%</strong></td><td>0.014</td></tr>
    </tbody>
  </table>
  <p>A Friedman test found no detectable difference across conditions, <strong>χ² = 0.095, p = 0.953</strong>.</p>
  </div>
  <figure><img src="/assets/projects/fragmented-melody/participant-accuracy.png" alt="Participant accuracy distributions for single-instrument, shared-register, and contrasting-register conditions"><figcaption>Participant accuracy by experimental section. The three condition means are closely aligned.</figcaption></figure>
</div>

## Interpretation

Within this sample, passing a phrase between instruments did not produce a measurable recognition penalty, even when the register changed at the same time. The result is consistent with listeners using the underlying pitch organization to recover a coherent melody across surface changes in timbre and register.

It is important to separate **absence of evidence** from evidence that timbre and register never matter. With only seven participants, unequal numbers of stimuli across sections, a musically experienced sample, and uncontrolled remote listening conditions, the study has limited statistical power and generalizability. The binomial results also vary by section despite equal accuracy in the two distributed conditions, illustrating how strongly the small trial counts affect significance.

## Future study

A follow-up should recruit a larger and more musically diverse sample, balance the number of melodies across conditions, randomize presentation order, and use unfamiliar purpose-composed stimuli throughout. Mixed-effects logistic regression could then separate listener and melody variability while testing timbre, register, and their interaction directly. Adding confidence ratings and delayed recognition would help distinguish immediate auditory integration from longer-term melodic memory.

<p class="fm-credits"><strong>Research team</strong><br>Harper Sun · Tristan Peng · Jacob Westerstahl · Changda Ma<br><small>Georgia Institute of Technology · Qualtrics · Logic Pro · Music cognition</small></p>

</div>
