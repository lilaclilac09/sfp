#!/usr/bin/env python3
"""
British-female text-to-speech helper.

Goal: a composed, cinematic British female voice — the register people associate
with Vanessa Kirby / Rosamund Pike (measured, lower-pitched, RP English).

This does NOT clone either actress (that's their personal likeness). Instead it
selects the closest *generic* British female voices across providers and applies
a calm, slightly lower, slower delivery to match that tone.

Providers (pick with --provider):
  azure       Azure Cognitive Services Speech  (default; best tone control via SSML)
  elevenlabs  ElevenLabs TTS                    (most natural / cinematic)
  say         macOS built-in `say`              (offline, zero setup, lower quality)

Setup:
  pip install requests          # only needed for azure / elevenlabs
  azure:       export AZURE_SPEECH_KEY=...   AZURE_SPEECH_REGION=eastus
  elevenlabs:  export ELEVENLABS_API_KEY=...

Usage:
  python tts_british_female.py "Spec first. Code second. Keys never." -o out.mp3
  python tts_british_female.py "Hello." --provider elevenlabs --voice Charlotte -o hi.mp3
  python tts_british_female.py "Hello." --provider say          # plays aloud on macOS
"""
import argparse
import os
import subprocess
import sys

# --- Voice presets: the "composed British female" shortlist per provider -------
AZURE_VOICES = {
    # en-GB neural female voices, warmest/most composed first
    "sonia": "en-GB-SoniaNeural",    # calm, low, cinematic  <- default
    "libby": "en-GB-LibbyNeural",    # brighter, friendly
    "abbi":  "en-GB-AbbiNeural",
    "olivia": "en-GB-OliviaNeural",
}
# ElevenLabs ships several British female presets; pass the name you have in your
# library. These are common ones — confirm the exact voice in your account.
ELEVEN_DEFAULT_VOICE = "Charlotte"   # British, soft/cinematic
# macOS `say` British female voices
SAY_DEFAULT_VOICE = "Serena"         # en-GB female (also: "Kate", "Stephanie")


def speak_azure(text, out, voice_key, rate, pitch):
    import requests
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION", "eastus")
    if not key:
        sys.exit("Set AZURE_SPEECH_KEY (and optionally AZURE_SPEECH_REGION).")
    voice = AZURE_VOICES.get(voice_key.lower(), voice_key)
    # SSML: drop the pitch and slow it slightly for that measured, composed read.
    ssml = (
        '<speak version="1.0" xml:lang="en-GB">'
        f'<voice name="{voice}">'
        f'<prosody rate="{rate}" pitch="{pitch}">{_escape(text)}</prosody>'
        '</voice></speak>'
    )
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
        "User-Agent": "british-female-tts",
    }
    r = requests.post(url, headers=headers, data=ssml.encode("utf-8"), timeout=30)
    r.raise_for_status()
    _write(out, r.content)


def speak_elevenlabs(text, out, voice, stability, similarity):
    import requests
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Set ELEVENLABS_API_KEY.")
    # Resolve a voice name -> id via the voices endpoint (so you can pass a name).
    vr = requests.get("https://api.elevenlabs.io/v1/voices",
                      headers={"xi-api-key": key}, timeout=30)
    vr.raise_for_status()
    voice_id = None
    for v in vr.json().get("voices", []):
        if v.get("name", "").lower() == voice.lower() or v.get("voice_id") == voice:
            voice_id = v["voice_id"]
            break
    if not voice_id:
        names = ", ".join(v.get("name", "") for v in vr.json().get("voices", []))
        sys.exit(f'Voice "{voice}" not found. Available: {names}')
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": stability, "similarity_boost": similarity},
        },
        timeout=60,
    )
    r.raise_for_status()
    _write(out, r.content)


def speak_say(text, out, voice):
    # macOS only. Plays aloud, or writes AIFF if -o given.
    if sys.platform != "darwin":
        sys.exit("--provider say only works on macOS.")
    cmd = ["say", "-v", voice, "-r", "165"]
    if out:
        cmd += ["-o", out]
    cmd.append(text)
    subprocess.run(cmd, check=True)
    print(f"{'wrote ' + out if out else 'spoke'} via macOS say ({voice})")


def _escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _write(path, data):
    if not path:
        sys.exit("This provider needs an output file: pass -o out.mp3")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


def main():
    p = argparse.ArgumentParser(description="Composed British female TTS.")
    p.add_argument("text", help="text to speak")
    p.add_argument("-o", "--out", help="output audio file (mp3 for azure/elevenlabs)")
    p.add_argument("--provider", default="azure",
                   choices=["azure", "elevenlabs", "say"])
    p.add_argument("--voice", default=None,
                   help="azure: sonia|libby|abbi|olivia or full name; "
                        "elevenlabs: voice name; say: macOS voice name")
    # tone knobs that push toward the calm, cinematic register
    p.add_argument("--rate", default="-6%", help="azure speaking rate (e.g. -6%%)")
    p.add_argument("--pitch", default="-2st", help="azure pitch shift (e.g. -2st)")
    p.add_argument("--stability", type=float, default=0.55, help="elevenlabs")
    p.add_argument("--similarity", type=float, default=0.85, help="elevenlabs")
    a = p.parse_args()

    if a.provider == "azure":
        speak_azure(a.text, a.out, a.voice or "sonia", a.rate, a.pitch)
    elif a.provider == "elevenlabs":
        speak_elevenlabs(a.text, a.out, a.voice or ELEVEN_DEFAULT_VOICE,
                         a.stability, a.similarity)
    else:
        speak_say(a.text, a.out, a.voice or SAY_DEFAULT_VOICE)


if __name__ == "__main__":
    main()
