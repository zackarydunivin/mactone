# mactone 🍎🔔

A tiny Python library to play macOS system alert tones — with silence trimming for a faster, cleaner sound.

## Features

- Play any macOS system sound by name (e.g., `"Glass"`, `"Submarine"`)
- Call tone functions directly like `glass_tone()` or `submarine_tone()`
- Automatically trims trailing silence from system sounds (annoying dead air!)
- Stores everything in memory for quick playback
- Cross-script and reusable — great for alerts!

## Installation

Coming soon to PyPI.

For now, install directly from GitHub:

```bash
pip install git+https://github.com/zdunivin/mactone.git
```

## Usage

```python
from mactone import tone, list_tones, funk_tone

# Play by name (case-insensitive)
tone("Glass")
tone("funk")

# Use dynamic tone functions
funk_tone()
glass_tone()

# List available system tones
print(list_tones())

# Play a random system tone
import mactone
mactone.random_tone()
```
## Requirements

- macOS
- Python 3.7+
- pydub
- sounddevice

## License

[MIT](LICENSE) © Zackary Okun Dunivin