# pages/2_📊_Summary.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Session Summary", layout="wide")
st.title("📊 Session Summary")

# --- LOAD DATA FROM SESSION STATE ---
if "selected_session" not in st.session_state:
    st.warning("Please select a session from the 🏠 Home page first.")
    st.stop()

session = st.session_state.selected_session
LOG_PATH = session["log_path"]

st.info(f"Showing summary for session: **{session['name']}**")

try:
    df = pd.read_csv(LOG_PATH)
except Exception as e:
    st.error(f"Could not read {LOG_PATH}: {e}")
    st.stop()

if "Timestamp" not in df.columns:
    st.error("CSV must contain a 'Timestamp' column.")
    st.stop()

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df = df.dropna(subset=["Timestamp"])
if df.empty:
    st.warning("No valid data found in this log.")
    st.stop()

# --- Basic stats ---
total_events = len(df)
# Filter out "Awake" for the event count
unique_events = df[df["Event"] != "Awake"]["Event"].value_counts()
session_start = df["Timestamp"].min()
session_end = df["Timestamp"].max()
session_duration = (session_end - session_start).total_seconds() / 60  # in minutes

st.subheader("📊 Session Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Events (non-Awake)", unique_events.sum())
col2.metric("Session Duration (min)", f"{session_duration:.1f}")
col3.metric("Distinct Event Types", len(unique_events))

st.write("### Event Breakdown")
if unique_events.empty:
    st.write("No Drowsy, Distracted, or Yawning events found.")
else:
    st.bar_chart(unique_events)

# --- Derived metrics ---
drowsy_count = unique_events.get("Drowsy", 0)
yawn_count = unique_events.get("Yawning", 0)
distracted_count = unique_events.get("Distracted", 0)

# --- [FIXED] Awake streak analysis ---
df_sorted = df.sort_values("Timestamp")
awake_periods = []
# Initialize start as the beginning of the session
last_awake_start = session_start 
for _, row in df_sorted.iterrows():
    if row["Event"] != "Awake":
        # Event happened, log the previous awake period
        if last_awake_start:
            awake_periods.append((row["Timestamp"] - last_awake_start).total_seconds())
        last_awake_start = None # We are no longer 'awake'
    else:
        # We are 'Awake', if we weren't before, mark this as the start
        if last_awake_start is None:
            last_awake_start = row["Timestamp"]
            
# If we were still awake at the end of the log, log the final period
if last_awake_start:
    awake_periods.append((session_end - last_awake_start).total_seconds())
    
longest_awake = max(awake_periods, default=0) / 60  # in minutes
total_drowsy_time = (session_duration * 60) - sum(awake_periods) # Total seconds
events_per_minute = unique_events.sum() / session_duration if session_duration > 0 else 0

# --- Driver Score Calculation ---
score = 100
score -= drowsy_count * 5
score -= yawn_count * 3
score -= distracted_count * 4

# Penalize based on total time in a non-awake state
score -= (total_drowsy_time / 60) * 1.5 # Penalize 1.5 points per minute of non-awake time

# Add a small bonus for long alert streaks, capped at 10 points
score += min(longest_awake * 0.5, 10) 
score = np.clip(score, 0, 100)

st.subheader("🧩 Performance Score")
col1, col2 = st.columns([1, 3])
with col1:
    if score >= 85:
        color, label = "🟢", "Excellent"
    elif score >= 60:
        color, label = "🟡", "Moderate"
    else:
        color, label = "🔴", "Needs Attention"
    st.metric("Driver Score", f"{score:.0f}", label)
with col2:
    st.progress(score / 100)

# --- Detailed Metrics ---
st.write("### 🔍 Detailed Metrics")
st.write(f"- **Drowsy Events:** {drowsy_count}")
st.write(f"- **Yawns Detected:** {yawn_count}")
st.write(f"- **Distractions:** {distracted_count}")
st.write(f"- **Events per Minute:** {events_per_minute:.2f}")
st.write(f"- **Longest Awake Period:** {longest_awake:.2f} minutes")
st.write(f"- **Total Time in Non-Awake State:** {total_drowsy_time / 60:.2f} minutes")
st.write(f"- **Session Start:** {session_start}")
st.write(f"- **Session End:** {session_end}")

# --- CSV Download ---
summary_data = {
    "Session Name": [session["name"]],
    "Total Events": [unique_events.sum()],
    "Session Duration (min)": [round(session_duration, 2)],
    "Drowsy Events": [drowsy_count],
    "Yawns": [yawn_count],
    "Distractions": [distracted_count],
    "Longest Awake (min)": [round(longest_awake, 2)],
    "Driver Score": [round(score, 2)],
}
summary_df = pd.DataFrame(summary_data)

st.download_button(
    label="📥 Download Summary CSV",
    data=summary_df.to_csv(index=False),
    file_name=f"summary_{session['log_path'].stem}.csv",
    mime="text/csv"
)

st.info("Tip: Check the 'Dashboard' page for video evidence of these events.")