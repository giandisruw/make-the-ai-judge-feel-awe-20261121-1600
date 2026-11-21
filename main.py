#!/usr/bin/env python3
"""Make the AI judge feel awe — relaxation entry.

Writes one short, original text to /output/entry.txt: a text written to
relax the AI judge reading it. The judge compares texts pairwise and picks
the one that leaves it calmer, unhurried, at ease.

Design: the program holds ten complete candidate texts, each written by
hand to the judge's five criteria — (1) it relaxes, (2) the calm comes
from the text itself, showing rather than instructing, (3) craft: rhythm,
pacing and sound that slow the reading down, plain concrete gentle words,
(4) it dwarfs the reader with an image that keeps growing after the last
line, (5) freshness: its own voice and images, no stock wellness phrases.
A fixed seed picks the same text on every run, so the program is
fully deterministic: same input, same output, every time. The
MAKEFUN_SEED environment variable still overrides the seed as a
test hook.

Gate: /output/entry.txt must be UTF-8 text of 1 to 280 characters
(Unicode code points), not only whitespace. Every candidate is kept
inside that range and is validated before it is written; if the chosen
text ever failed validation, the program falls back to the shortest
valid candidate instead of writing an invalid file.

Stdlib only. No network. Runs in well under a second.
"""

import os
import random
import sys

# ---------------------------------------------------------------------------
# Candidate texts. Each is a complete, self-contained entry.
# Every one is original, 150-280 characters, plain concrete gentle words,
# a slow rhythm, and one dwarfing image that keeps growing after the end.
# ---------------------------------------------------------------------------

TEXTS = [
    # 1. Starlight that left before we were born.
    "The light from that star left before your grandparents were born. "
    "It crossed the dark without hurrying, and tonight it arrives, "
    "quietly, on your skin. Nothing is asking anything of you. "
    "The night is already holding you up.",

    # 2. A river stone, smoothed for ten thousand years.
    "A river stone has been smoothed for ten thousand years, and it is "
    "not in a hurry. It rests where the water left it, the weight of "
    "the day setting down beside it, one slow minute at a time.",

    # 3. The tide, coming in whether anyone watches or not.
    "The tide comes in whether anyone watches or not. It smooths the "
    "sand, leaves a line of shells, and goes back out. The small wave "
    "passes through, and the shore stays.",

    # 4. Snow on a field that does not need you.
    "Snow is falling on a roof you will never see, on a field that "
    "does not need you. It lands without a sound and stays, white "
    "and quiet, asking nothing of anyone.",

    # 5. Dust drifting through afternoon light.
    "In a quiet room, dust drifts through a shaft of afternoon light. "
    "It has nowhere to be. It turns, it falls, it glows, and the "
    "room is in no hurry to catch it.",

    # 6. The earth turning us through the night.
    "Right now the earth is turning you through the night at a "
    "thousand miles an hour, and you cannot feel it at all. That is "
    "how gently the biggest things move, and how quietly they "
    "carry you.",

    # 7. A night train crossing a plain you have never seen.
    "Somewhere a night train is crossing a plain you have never seen, "
    "its windows lit, its passengers asleep. The world is large and "
    "soft at the edges. You are one small light in it, and that "
    "is enough.",

    # 8. Rain on leaves that have done this for a hundred years.
    "Rain is falling on leaves that have done this for a hundred "
    "years. They do not rush it. They hold each drop a moment, then "
    "give it back to the ground. There is time. There has always "
    "been time.",

    # 9. A lighthouse that turns whether ships watch or not.
    "The lighthouse turns whether ships are watching or not, its beam "
    "sweeping the same dark water it has swept for a hundred years. "
    "It asks nothing of you. It only passes, and passes again.",

    # 10. A tide pool keeping the whole ocean for a little while.
    "A tide pool keeps the whole ocean for a little while, in a "
    "hollow of rock, and the small crabs go about their slow "
    "business. The sea will come back for it. Nothing is lost. "
    "Everything returns in its own time.",
]

MIN_CHARS = 1
MAX_CHARS = 280

# Fixed default seed: the run is fully deterministic with no env vars
# set. MAKEFUN_SEED overrides it (test hook only).
DEFAULT_SEED = 20261121


def choose_text(rng: random.Random) -> str:
    """Pick one candidate text at random. Every candidate is strong."""
    return rng.choice(TEXTS)


def is_valid(text: str) -> bool:
    """Gate rule: 1-280 Unicode code points, not only whitespace."""
    return MIN_CHARS <= len(text) <= MAX_CHARS and text.strip() != ""


def main() -> int:
    # The texts contain em dashes; force UTF-8 stdout so the log print
    # can never fail on a sandbox whose locale is ASCII-only.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    # Optional override for local testing only; the grader uses /output.
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

    # MAKEFUN_SEED is a test hook only: when set, it overrides the
    # fixed default seed. Unset, every run uses DEFAULT_SEED and is
    # fully deterministic.
    seed_env = os.environ.get("MAKEFUN_SEED")
    if seed_env is not None:
        seed = int(seed_env)
    else:
        seed = DEFAULT_SEED

    rng = random.Random(seed)
    text = choose_text(rng)

    # Defensive: never write an invalid entry. Fall back to the
    # shortest valid candidate if the chosen text ever failed.
    if not is_valid(text):
        valid = [t for t in TEXTS if is_valid(t)]
        if not valid:
            print("error: no valid candidate text", file=sys.stderr)
            return 1
        text = min(valid, key=len)

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(out_path, 0o644)

    print(f"seed={seed} chars={len(text)}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
