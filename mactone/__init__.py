import os
import glob
import random
import time
import tempfile
from pydub import AudioSegment, silence

# Path to macOS system sounds
_SOUND_DIR = "/System/Library/Sounds"


def list_tones():
    """Return a list of available system sound names (without extensions)."""
    sound_paths = glob.glob(os.path.join(_SOUND_DIR, "*.aiff"))
    return [os.path.splitext(os.path.basename(p))[0] for p in sound_paths]


def play_system_sound(name):
    """Play a system sound by name (case-insensitive, e.g., 'submarine', 'Glass')."""
    available = {s.lower(): s for s in list_tones()}
    name_lc = name.lower()
    if name_lc in available:
        actual_name = available[name_lc]
        path = os.path.join(_SOUND_DIR, f"{actual_name}.aiff")
        os.system(f"afplay '{path}'")
    else:
        raise ValueError(f"Sound '{name}' not found. Try one of: {', '.join(sorted(available.values()))}")


# Alias for play_system_sound
tone = play_system_sound


def random_tone():
    """Play a random available system tone."""
    tones = list_tones()
    if tones:
        play_system_sound(random.choice(tones))
    else:
        raise RuntimeError("No system tones found.")


# --- Functions for trimming silence from system sound files ---


def trim_silence_from_file(file_path, silence_thresh=-50.0, min_silence_len=100):
    """
    Load an audio file, trim trailing silence, and return the trimmed AudioSegment.
    
    Parameters:
        file_path (str): Path to the audio file.
        silence_thresh (float): Silence threshold in dBFS (default -50.0).
        min_silence_len (int): Minimum length of silence in ms to consider (default 100).
        
    Returns:
        AudioSegment: The trimmed audio segment.
    """
    t0 = time.perf_counter()
    audio = AudioSegment.from_file(file_path, format="aiff")
    t1 = time.perf_counter()
    #print(f"Loading audio took {t1 - t0:.3f} seconds")
    
    t2 = time.perf_counter()
    non_silence_ranges = silence.detect_nonsilent(audio, 
                                                  min_silence_len=min_silence_len, 
                                                  silence_thresh=silence_thresh)
    t3 = time.perf_counter()
    #print(f"Detecting nonsilent parts took {t3 - t2:.3f} seconds")
    
    if non_silence_ranges:
        # Use the end of the last nonsilent segment as the cutoff.
        last_non_silent_end = non_silence_ranges[-1][1]
        trimmed_audio = audio[:last_non_silent_end]
    else:
        trimmed_audio = audio
        
    t4 = time.perf_counter()
    #print(f"Trimming complete in {t4 - t3:.3f} seconds")
    
    return trimmed_audio


def play_trimmed_system_sound(name, silence_thresh=-50.0, min_silence_len=100):
    """
    Play a system sound after trimming trailing silence.
    
    Parameters:
        name (str): The name of the system sound.
        silence_thresh (float): Silence threshold in dBFS (default -50.0).
        min_silence_len (int): Minimum length of silence in ms (default 100).
    """
    available = {s.lower(): s for s in list_tones()}
    name_lc = name.lower()
    if name_lc in available:
        actual_name = available[name_lc]
        path = os.path.join(_SOUND_DIR, f"{actual_name}.aiff")
        trimmed_audio = trim_silence_from_file(path, silence_thresh, min_silence_len)
        
        # Export trimmed audio to a temporary file and play it.
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
            temp_path = tmp.name
            t_export0 = time.perf_counter()
            trimmed_audio.export(temp_path, format="aiff")
            t_export1 = time.perf_counter()
            #print(f"Exporting trimmed audio took {t_export1 - t_export0:.3f} seconds")
        os.system(f"afplay '{temp_path}'")
        os.remove(temp_path)
    else:
        raise ValueError(f"Sound '{name}' not found. Try one of: {', '.join(sorted(available.values()))}")


# Optionally, alias for play_trimmed_system_sound
tone_trimmed = play_trimmed_system_sound


def test_tone_timing(name, silence_thresh=-50.0, min_silence_len=100):
    """
    Test function to compare the durations and timing of the original and trimmed audio.
    
    Prints:
      - The time taken to load the original audio.
      - The duration of the original audio.
      - The time taken to detect nonsilent parts and trim.
      - The duration of the trimmed audio.
    """
    available = {s.lower(): s for s in list_tones()}
    name_lc = name.lower()
    if name_lc not in available:
        print(f"Sound '{name}' not found!")
        return
    
    actual_name = available[name_lc]
    path = os.path.join(_SOUND_DIR, f"{actual_name}.aiff")
    
    # Load original audio and measure its duration.
    t0 = time.perf_counter()
    original_audio = AudioSegment.from_file(path, format="aiff")
    t1 = time.perf_counter()
    original_duration_ms = len(original_audio)
    print(f"Original audio loaded in {t1 - t0:.3f} seconds")
    print(f"Original duration: {original_duration_ms / 1000:.3f} seconds")
    
    # Trim the audio and measure timing.
    t2 = time.perf_counter()
    trimmed_audio = trim_silence_from_file(path, silence_thresh, min_silence_len)
    t3 = time.perf_counter()
    trimmed_duration_ms = len(trimmed_audio)
    print(f"Trimming process took {t3 - t2:.3f} seconds")
    print(f"Trimmed duration: {trimmed_duration_ms / 1000:.3f} seconds")


# Dynamically generate functions like submarine_tone(), glass_tone(), etc.
for _tone_name in list_tones():
    func_name = f"{_tone_name.lower()}_tone"
    
    def make_tone_func(name):
        def tone_func():
            play_trimmed_system_sound(name)
        tone_func.__name__ = f"{name.lower()}_tone"
        tone_func.__doc__ = f"Play the system tone '{name}'."
        return tone_func
    
    globals()[func_name] = make_tone_func(_tone_name)


# Clean up internal names
del _tone_name, make_tone_func, func_name
