import streamlit as st
import cv2
from ultralytics import YOLO
import pandas as pd
import numpy as np
from datetime import datetime
import os
import time
import json
import plotly.express as px
import plotly.graph_objects as go

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Smart Security System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .alert-high   { background:#ff4b4b22; border-left:4px solid #ff4b4b; padding:8px 12px; border-radius:4px; color:#ff4b4b; font-weight:600; }
    .alert-medium { background:#ffa50022; border-left:4px solid #ffa500; padding:8px 12px; border-radius:4px; color:#ffa500; font-weight:600; }
    .alert-low    { background:#00c85322; border-left:4px solid #00c853; padding:8px 12px; border-radius:4px; color:#00c853; font-weight:600; }
    .stat-card    { background:#1e1e2e; border:1px solid #333; border-radius:8px; padding:16px; text-align:center; }
    .badge-high   { background:#ff4b4b; color:#fff; padding:2px 8px; border-radius:12px; font-size:11px; }
    .badge-medium { background:#ffa500; color:#fff; padding:2px 8px; border-radius:12px; font-size:11px; }
    .badge-low    { background:#00c853; color:#fff; padding:2px 8px; border-radius:12px; font-size:11px; }
</style>
""", unsafe_allow_html=True)

# ─── Title ───────────────────────────────────────────────────────────────────
st.markdown("## 🔒 AI Smart Security & Intrusion Detection System")
st.caption("Powered by YOLOv8 · Real-time object detection and threat analysis")

# ─── Ensure folders exist ────────────────────────────────────────────────────
os.makedirs("screenshots", exist_ok=True)

# ─── Load YOLO ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ─── Sidebar Controls ────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Detection Settings")

input_source = st.sidebar.radio(
    "Select Input Source",
    ["Upload Video", "Live Webcam"]
)

uploaded_file = None

if input_source == "Upload Video":
    uploaded_file = st.sidebar.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

st.sidebar.divider()

# Confidence threshold
confidence_threshold = st.sidebar.slider(
    "Confidence Threshold", 0.1, 1.0, 0.4, 0.05,
    help="Only show detections above this confidence level"
)

# FPS control
frame_skip = st.sidebar.slider(
    "Processing Speed (frame skip)", 1, 10, 2,
    help="Higher = faster processing but fewer frames analyzed"
)

st.sidebar.divider()
st.sidebar.subheader("🎯 Object Filters")

# Object class filters
TRACKED_OBJECTS = {
    "person": "🚶 Person (Intruder)",
    "car": "🚗 Car / Vehicle",
    "truck": "🚚 Truck",
    "motorcycle": "🏍️ Motorcycle",
    "bicycle": "🚲 Bicycle",
    "backpack": "🎒 Backpack",
    "cell phone": "📱 Cell Phone",
}

selected_objects = st.sidebar.multiselect(
    "Track these objects",
    options=list(TRACKED_OBJECTS.keys()),
    default=["person", "car", "motorcycle","backpack"],
    format_func=lambda x: TRACKED_OBJECTS.get(x, x),
)

st.sidebar.divider()
st.sidebar.subheader("🚨 Alert Settings")

# Severity thresholds
high_alert_count = st.sidebar.number_input(
    "High alert after N persons", min_value=1, max_value=20, value=3
)
screenshot_interval = st.sidebar.number_input(
    "Screenshot interval (sec)", min_value=1, max_value=60, value=10
)

# Zone toggle
enable_zone = st.sidebar.toggle("Enable Restricted Zone", value=False)
if enable_zone:
    st.sidebar.caption("📐 Zone: center 60% of the frame is monitored")

st.sidebar.divider()
st.sidebar.subheader("💾 Export Options")
export_format = st.sidebar.radio("Export format", ["CSV", "JSON", "Both"])

st.sidebar.subheader("🧹 Data Management")

if st.sidebar.button("🛑 Stop Analysis"):
    st.session_state.stop_analysis = True
if st.sidebar.button("🗑️ Clear All Data"):
    st.session_state.stop_analysis = False
    st.session_state.detection_logs = []
    st.session_state.alert_log = []
    st.session_state.intrusion_count = 0

    # Delete screenshots
    if os.path.exists("screenshots"):
        for file in os.listdir("screenshots"):
            file_path = os.path.join("screenshots", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    st.success("All data cleared successfully!")
    st.rerun()

# ─── Session State ───────────────────────────────────────────────────────────
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []
if "alert_log" not in st.session_state:
    st.session_state.alert_log = []
if "intrusion_count" not in st.session_state:
    st.session_state.intrusion_count = 0
if "processed" not in st.session_state:
    st.session_state.processed = False
if "stop_analysis" not in st.session_state:
    st.session_state.stop_analysis = False

# ─── Helper: severity ────────────────────────────────────────────────────────
def get_severity(person_count: int) -> str:

    if person_count >= high_alert_count:
        return "HIGH"

    elif person_count >= 2:
        return "MEDIUM"

    elif person_count >= 1:
        return "LOW"

    return "LOW"

def severity_badge(s: str) -> str:
    cls = {"HIGH": "badge-high", "MEDIUM": "badge-medium", "LOW": "badge-low"}
    return f'<span class="{cls[s]}">{s}</span>'

def in_zone(box, frame_w: int, frame_h: int) -> bool:
    """Check if box centre is inside the restricted 60% centre zone."""
    cx = (box.xyxy[0][0].item() + box.xyxy[0][2].item()) / 2
    cy = (box.xyxy[0][1].item() + box.xyxy[0][3].item()) / 2
    x1, x2 = frame_w * 0.2, frame_w * 0.8
    y1, y2 = frame_h * 0.2, frame_h * 0.8
    return x1 <= cx <= x2 and y1 <= cy <= y2

# ─── Main Layout ─────────────────────────────────────────────────────────────
col_video, col_stats = st.columns([3, 1])

with col_video:
    video_placeholder = st.empty()
    alert_placeholder = st.empty()

with col_stats:
    st.markdown("#### 📊 Live Stats")
    metric_intrusions = st.empty()
    metric_objects    = st.empty()
    metric_severity   = st.empty()
    st.divider()
    st.markdown("#### 🚨 Alert Feed")
    alert_feed = st.empty()

# ─── Processing ──────────────────────────────────────────────────────────────
if (
    (uploaded_file is not None or input_source == "Live Webcam")
    and not st.session_state.processed
):

    if input_source == "Upload Video":

        temp_video_path = "temp_video.mp4"

        with open(temp_video_path, "wb") as f:
            f.write(uploaded_file.read())

        cap = cv2.VideoCapture(temp_video_path)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    else:

        cap = cv2.VideoCapture(0)

        total_frames = 100000

    progress_bar = st.progress(0, text="Analysing video…")
    frame_index  = 0
    last_capture = 0
    recent_alerts = []


    while cap.isOpened():

        if st.session_state.stop_analysis:
            st.warning("Analysis stopped by user.")
            break


        ret, frame = cap.read()
        if not ret:
            break

        frame_index += 1

        # Skip frames for speed
        if frame_index % frame_skip != 0:
            continue

        results = model(frame, conf=confidence_threshold, verbose=False)

        frame_h, frame_w = frame.shape[:2]
        counts      = {}

        for r in results:
            for box in r.boxes:
                cls        = int(box.cls[0])
                name       = model.names[cls]
                confidence = float(box.conf[0])

                # Filter to selected objects only
                if name not in selected_objects:
                    continue

                # Zone filter
                if enable_zone and not in_zone(box, frame_w, frame_h):
                    continue

                counts[name] = counts.get(name, 0) + 1

                st.session_state.detection_logs.append({
                    "Time":       datetime.now().strftime("%H:%M:%S"),
                    "Frame":      frame_index,
                    "Object":     name,
                    "Confidence": round(confidence, 2),
                    "Severity":   get_severity(counts.get("person", 0))
                })

        # Intrusion + screenshot logic
        current_time = time.time()
        person_count = counts.get("person", 0)

        if person_count > 0 and (current_time - last_capture > screenshot_interval):
            st.session_state.intrusion_count += 1
            filename = (
                f"screenshots/intruder_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            cv2.imwrite(filename, frame)
            last_capture = current_time

            sev = get_severity(person_count)
            alert_entry = {
                "time":     datetime.now().strftime("%H:%M:%S"),
                "persons":  person_count,
                "severity": sev,
            }
            st.session_state.alert_log.append(alert_entry)
            recent_alerts.insert(0, alert_entry)
            if len(recent_alerts) > 5:
                recent_alerts.pop()

        # Draw annotations
        annotated = results[0].plot()

        # Draw restricted zone box
        if enable_zone:
            x1z = int(frame_w * 0.2); y1z = int(frame_h * 0.2)
            x2z = int(frame_w * 0.8); y2z = int(frame_h * 0.8)
            cv2.rectangle(annotated, (x1z, y1z), (x2z, y2z), (0, 255, 255), 2)
            cv2.putText(annotated, "RESTRICTED ZONE", (x1z + 5, y1z + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Overlay text
        sev = get_severity(person_count) if person_count else "LOW"
        sev_color = {"HIGH": (0,0,255), "MEDIUM": (0,165,255), "LOW": (0,200,80)}[sev]

        if person_count > 0:
            cv2.putText(annotated, f"⚠ ALERT [{sev}]", (10, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, sev_color, 3)

        cv2.putText(annotated,
                    f"Intrusions: {st.session_state.intrusion_count}",
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 80, 80), 2)

        y_off = 130
        for obj, cnt in counts.items():
            cv2.putText(annotated, f"{obj}: {cnt}", (10, y_off),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 255, 80), 2)
            y_off += 28

        frame_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

        # Live stats panel
        metric_intrusions.metric("🚶 Intrusions", st.session_state.intrusion_count)
        metric_objects.metric("🔍 Objects (frame)", sum(counts.values()))
        metric_severity.metric("⚡ Severity", sev)

        # Alert feed
        if recent_alerts:
            feed_html = ""
            for a in recent_alerts[:5]:
                cls = {"HIGH": "alert-high", "MEDIUM": "alert-medium", "LOW": "alert-low"}[a["severity"]]

                feed_html += (
                    f'<div class="{cls}" style="margin-bottom:6px;">'
                    f'[{a["time"]}] {a["persons"]} person(s)'
                    f'</div>'
                )
            alert_feed.markdown(feed_html, unsafe_allow_html=True)

        # Progress
        if input_source == "Upload Video":
            progress_bar.progress(
                min(frame_index / max(total_frames, 1), 1.0),
                text=f"Frame {frame_index}/{total_frames}"
            )

    cap.release()
    progress_bar.empty()
    st.session_state.processed = True
    if input_source == "Upload Video":
        st.success("✅ Video analysis complete!")

elif st.session_state.processed:
    st.info("Analysis already done. Scroll down to view results or upload a new video.")

else:
    with video_placeholder:
        st.info("📹 Upload a video in the sidebar to begin analysis.")

# ─── Reset button ────────────────────────────────────────────────────────────
if st.session_state.processed:
    if st.button("🔄 Analyse New Video"):
        st.session_state.stop_analysis = False
        st.session_state.detection_logs = []
        st.session_state.alert_log      = []
        st.session_state.intrusion_count = 0
        st.session_state.processed      = False
        st.rerun()

# ─── Results Section ─────────────────────────────────────────────────────────
if st.session_state.detection_logs:
    df = pd.DataFrame(st.session_state.detection_logs)

    st.divider()
    st.subheader("📈 Detection Analytics")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Charts", "📋 Detection Log", "🖼️ Captured Images", "🚨 Alert Summary"]
    )

    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            obj_counts = df.groupby("Object").size().reset_index(name="Count")
            fig1 = px.bar(
                obj_counts, x="Object", y="Count",
                title="Objects Detected",
                color="Count", color_continuous_scale="Reds",
            )
            fig1.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            sev_counts = df.groupby("Severity").size().reset_index(name="Count")
            color_map  = {"HIGH": "#ff4b4b", "MEDIUM": "#ffa500", "LOW": "#00c853"}
            fig2 = px.pie(
                sev_counts, names="Severity", values="Count",
                title="Severity Distribution",
                color="Severity", color_discrete_map=color_map,
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)

        # Confidence over time
        if "Frame" in df.columns:
            fig3 = px.line(
                df[df["Object"].isin(selected_objects)],
                x="Frame", y="Confidence", color="Object",
                title="Detection Confidence Over Time",
            )
            fig3.update_layout(height=280)
            st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Export
        if export_format in ("CSV", "Both"):
            st.download_button(
                "⬇️ Download CSV Report",
                data=df.to_csv(index=False),
                file_name="detection_report.csv",
                mime="text/csv",
            )
        if export_format in ("JSON", "Both"):
            st.download_button(
                "⬇️ Download JSON Report",
                data=df.to_json(orient="records", indent=2),
                file_name="detection_report.json",
                mime="application/json",
            )

    with tab3:
        screenshots = sorted(os.listdir("screenshots"))
        if screenshots:
            cols = st.columns(3)
            for i, img_name in enumerate(screenshots):
                with cols[i % 3]:
                    st.image(
                        os.path.join("screenshots", img_name),
                        caption=img_name,
                        use_container_width=True,
                    )
        else:
            st.info("No screenshots captured yet.")

    with tab4:
        if st.session_state.alert_log:
            alert_df = pd.DataFrame(st.session_state.alert_log)

            st.markdown("#### Alert Timeline")
            for _, row in alert_df.iterrows():
                sev = row["severity"]
                css = {"HIGH": "alert-high", "MEDIUM": "alert-medium", "LOW": "alert-low"}[sev]
                st.markdown(
                    f'<div class="{css}" style="margin-bottom:8px;">'
                    f'<b>[{row["time"]}]</b> &nbsp; {row["persons"]} person(s) detected'
                    f'<span style="float:right">{sev}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No alerts triggered during this session.")
