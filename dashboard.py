# pages/1_🎥_Dashboard.py
import streamlit as st
import pandas as pd
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import re
import sys

st.set_page_config(page_title="Event Dashboard", layout="wide")
st.title("🎥 Event Dashboard")

# --- CONFIG ---
CLIPS_DIR = Path("clips")
GROUP_SECONDS = 10
CLIP_PADDING_SECONDS = 3

# --- Ensure folders exist ---
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

# --- UTILITIES ---
def check_ffmpeg():
    """Check if ffmpeg is installed and in the PATH."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False

def group_events(df, group_seconds=GROUP_SECONDS):
    """Group nearby timestamps into one event episode."""
    if df.empty:
        return []
    df_sorted = df.sort_values("Timestamp").reset_index(drop=True)
    groups, cur = [], [0]
    for i in range(1, len(df_sorted)):
        if (df_sorted.loc[i, "Timestamp"] - df_sorted.loc[i-1, "Timestamp"]).total_seconds() <= group_seconds:
            cur.append(i)
        else:
            groups.append(df_sorted.loc[cur])
            cur = [i]
    if cur:
        groups.append(df_sorted.loc[cur])
    return groups

def ffmpeg_extract_clip(src_path, dst_path, start_sec, duration_sec):
    """Extract a clip via ffmpeg and return True if successful."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", str(src_path),
        "-t", str(duration_sec),
        "-c:v", "libx264", "-c:a", "aac", # Re-encode for web compatibility
        "-preset", "fast", # Faster encoding
        "-crf", "23", # Good quality
        str(dst_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, creationflags=(subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0))
        return True
    except FileNotFoundError:
        st.error("FFmpeg not found. Please install it and ensure it's in your system's PATH.")
        st.stop()
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg failed for {dst_path.name}: {e.stderr[:200]}")
        return False
    except Exception as e:
        st.error(f"FFmpeg exception: {e}")
        return False

# --- Check for FFMPEG ---
if not check_ffmpeg():
    st.error("FFmpeg could not be found. This page requires FFmpeg to extract video clips.")
    st.info("Please install FFmpeg and ensure it is added to your system's PATH.")
    st.stop()

# --- LOAD DATA FROM SESSION STATE ---
if "selected_session" not in st.session_state:
    st.warning("Please select a session from the 🏠 Home page first.")
    st.stop()

session = st.session_state.selected_session
LOG_PATH = session["log_path"]
VIDEO_PATH = session["video_path"]
VIDEO_START_DT = session["dt"] # The video's start time *is* the session's DT

st.info(f"Loaded session: **{session['name']}**")

try:
    df = pd.read_csv(LOG_PATH)
except Exception as e:
    st.error(f"Could not read log file: {e}")
    st.stop()

if "Timestamp" not in df.columns:
    st.error("CSV missing 'Timestamp' column.")
    st.stop()

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df = df.dropna(subset=["Timestamp"]).reset_index(drop=True)
# Filter out "Awake" events to only show incidents
df_events = df[df["Event"] != "Awake"].copy()

# --- Group & process ---
groups = group_events(df_events)

if not groups:
    st.success("No Drowsy, Distracted, or Yawning events found in this session! 👍")
    st.stop()

st.write(f"Detected **{len(groups)}** grouped event episodes for this session.")

# --- Generate & show clips ---
for idx, grp in enumerate(groups, 1):
    start_ts = grp["Timestamp"].iloc[0]
    end_ts = grp["Timestamp"].iloc[-1]
    
    # Get all events in this group
    events_in_group = ", ".join(grp["Event"].unique())
    
    clip_start_dt = start_ts - timedelta(seconds=CLIP_PADDING_SECONDS)
    clip_end_dt = end_ts + timedelta(seconds=CLIP_PADDING_SECONDS)
    duration = (clip_end_dt - clip_start_dt).total_seconds()

    # Calculate start time in seconds *relative to the video file*
    rel_start_sec = (clip_start_dt - VIDEO_START_DT).total_seconds()
    if rel_start_sec < 0:
        duration += rel_start_sec # Shorten duration if padding goes before video start
        rel_start_sec = 0
    
    # Use a unique name for the clip
    clip_name = f"{VIDEO_PATH.stem}_ep{idx}.mp4"
    clip_path = CLIPS_DIR / clip_name

    # Generate if missing
    if not clip_path.exists():
        with st.spinner(f"Generating clip {clip_name}..."):
            ok = ffmpeg_extract_clip(VIDEO_PATH, clip_path, rel_start_sec, duration)
            if not ok:
                st.error(f"Failed to extract clip {clip_name}")
                continue

    # Display
    st.markdown("---")
    st.subheader(f"Episode {idx}: {events_in_group}")
    st.write(f"Time: {start_ts.strftime('%Y-%m-%d %H:%M:%S')} → {end_ts.strftime('%H:%M:%S')}")
    
    if clip_path.exists():
        try:
            st.video(str(clip_path))
            with open(clip_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Clip",
                    data=f,
                    file_name=clip_name,
                    mime="video/mp4",
                    key=f"dl_{idx}"
                )
        except Exception as e:
            st.error(f"Cannot play clip: {e}")
    else:
        st.warning("Clip not found after generation attempt.")

st.success("Processing complete ✅")