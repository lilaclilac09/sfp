# British female voice (composed / cinematic)

A drop-in TTS helper for a calm, lower-pitched **British female** voice — the
register associated with **Vanessa Kirby / Rosamund Pike** (measured RP English).

> ⚠️ This does **not** clone Vanessa Kirby or Rosamund Pike. Cloning a real
> person's voice is their likeness and needs their consent. Instead this picks
> the closest *generic* British female voices and tunes the delivery (slightly
> lower pitch, slightly slower) to land in that composed, cinematic register.

## Which voice gets closest to that tone

| Provider | Voice | Notes |
|---|---|---|
| **Azure** (default) | `en-GB-SoniaNeural` | calm, low, cinematic — best fit; full SSML tone control |
| Azure | `en-GB-LibbyNeural` | brighter / friendlier alternative |
| **ElevenLabs** | `Charlotte` (British) | most natural; raise `stability` for a steadier read |
| macOS `say` | `Serena` / `Kate` | offline, zero setup, lower quality |

The cinematic feel comes less from the raw voice and more from the **delivery** —
this script defaults to `rate=-6%` and `pitch=-2st` (slower + lower) to avoid the
chirpy "assistant" sound.

## Setup

```bash
pip install requests           # for azure / elevenlabs

# Azure
export AZURE_SPEECH_KEY=...     # portal.azure.com -> Speech resource
export AZURE_SPEECH_REGION=eastus

# ElevenLabs
export ELEVENLABS_API_KEY=...
```

## Use

```bash
# default = Azure, Sonia, composed delivery
python tts_british_female.py "Spec first. Code second. Keys never." -o out.mp3

# ElevenLabs, steadier read
python tts_british_female.py "Welcome back." --provider elevenlabs \
    --voice Charlotte --stability 0.7 -o welcome.mp3

# macOS, instant, plays aloud (no key)
python tts_british_female.py "Hello." --provider say --voice Serena

# push even calmer / lower
python tts_british_female.py "..." --rate -10% --pitch -3st -o slow.mp3
```

## Dropping it into a project

- **langlang** (your flashcard app): swap whatever TTS call you have for
  `speak_azure(...)` / `speak_elevenlabs(...)` and serve the returned mp3.
- **A website**: run it server-side, cache the mp3 per phrase, serve as audio.
- **Claude app read-aloud voice**: that's a *client setting*, not code — pick a
  British female voice under the app's Settings → Voice. This script can't change
  the app's own voice.
