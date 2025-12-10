# DriverDrowsiness

1. Title of the Project:

Driver Drowsiness Detection System using Dlib Face Landmark Detection and Mediapipe
Integration
A real-time AI-based system designed to monitor a driver’s alertness level by analyzing
facial expressions, eye blinking rate, yawning frequency, and head movement using
computer vision frameworks like Dlib and Mediapipe.

3. Field / Area of Project: 
This project lies in the intersection of multiple cutting-edge domains:
* Computer Vision
* Artificial Intelligence (AI)
* Real-Time Video Analytics
* Human–Computer Interaction (HCI)
* Automotive Safety Systems

3. Summary and Background of the Project:

a) Summary of the Project: The Driver Drowsiness Detection System using Dlib and
Mediapipe is an advanced, real-time computer vision project aimed at improving road
safety by preventing accidents caused by driver fatigue or inattention.
It leverages Artificial Intelligence (AI) and Computer Vision techniques to continuously analyze a
driver’s facial features through a live webcam feed, identifying early signs of drowsiness such as
prolonged eye closure, yawning, and head movement deviations.
The system uses Dlib’s 68 facial landmark model to compute crucial metrics like Eye
Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR), which indicate eye closure and
yawning respectively.
Simultaneously, Mediapipe’s FaceMesh model enhances the detection by providing iris
tracking, head pose estimation, and gaze direction analysis, ensuring more stable and
accurate results even under varying lighting or face orientations.
Detected events—such as “Drowsy,” “Yawning,” or “Distracted”—are automatically
logged in a CSV file with precise timestamps, user information, and detection confidence.
These events are later processed by FFmpeg (version 8.0-essentials_build) to generate
short video clips around the moment of detection, allowing easy event playback and
analysis.
Finally, a Streamlit dashboard provides a user-friendly interface to visualize event data,
view corresponding video clips, and review driver performance in a summarized manner.

b) Background of the Project: Driver fatigue and inattention are among the leading causes
of traffic accidents worldwide. Studies have shown that sleepiness or temporary loss of
alertness accounts for a significant proportion of fatal crashes, particularly in commercial
and long-distance driving.
Conventional drowsiness detection systems, such as steering behaviour monitors or
physiological sensor-based approaches (e.g., EEG or heart-rate monitors), are either
expensive, intrusive, or require specialized equipment, making them impractical for
widespread everyday use.
To overcome these limitations, the research and development community has increasingly
focused on vision-based drowsiness detection, which uses cameras to monitor facial cues
such as eye closure rate, blinking frequency, yawning, and head movement.
Among these, Dlib has been widely adopted for facial landmark detection because it
provides reliable and efficient computation of key facial features. However, Dlib alone may
not handle certain challenges such as low lighting conditions, occlusions, or side- face
views efficiently.
This is where Mediapipe, a framework developed by Google, brings additional power. Its
FaceMesh and Iris Tracking models operate with high precision and are optimized for
real-time performance on CPUs.
By combining both frameworks, our project achieves robust and hybrid detection
performance, ensuring the system can adapt to various environments and driver behaviors
without requiring costly hardware or high-end GPUs.
The system also introduces a data logging mechanism that records all detected fatigue events
in structured CSV format, allowing for both real-time feedback and post-session review.
Additionally, it incorporates FFmpeg automation to generate short video segments around
critical events—providing tangible evidence and improving system interpretability for both
users and developers.

c) Addressing the Gap / Novelty of the Project:
The project overcomes the above limitations through:

i) Hybrid Dual-Framework Detection:
Unlike traditional single-framework systems that rely solely on Dlib or OpenCV for face analysis,
this project integrates Dlib’s 68-face-landmark model with Mediapipe’s FaceMesh and
Iris tracking modules.
By combining both, the system enhances detection accuracy under varied lighting conditions
and face orientations.
This hybrid approach ensures stable computation of Eye Aspect Ratio (EAR) and Mouth
Aspect Ratio (MAR) while simultaneously analyzing iris movement and head pose,
resulting in more reliable detection of drowsiness, yawning, and distraction.

ii) Automated Event Logging and Clip Generation:
Previous drowsiness detection systems lacked a mechanism for recording and verifying detection
events.
This project introduces a comprehensive event logging pipeline where all detected states
(Drowsy, Yawning, Distracted) are stored in a CSV file with timestamps and event details.
Further, using FFmpeg (v8.0-essentials_build), the system automatically generates
short video clips around the detected events.
This enables transparent validation of system accuracy and provides a visual record for future
review or analysis.

iii) Real-Time, Non-Intrusive, and Portable Design:
Existing deep-learning or sensor-based solutions often depend on specialized hardware like
GPUs or EEG sensors, resulting in high cost and complexity.
In contrast, this project achieves real-time performance (25–30 FPS) using only a
standard webcam and CPU processing.
Its non-intrusive, lightweight, and hardware-independent architecture makes it scalable
and suitable for real-world applications such as fleet monitoring, vehicle safety systems, and
research studies.
Through these innovations, the project establishes a hybrid, efficient, and user-friendly
framework that delivers accurate fatigue detection, real-time responsiveness, and visual
verification — addressing major limitations of earlier models while remaining accessible and
practical for everyday use

5. Objectives of the Project:

The principal objectives of the project are as follows:
* Detect driver drowsiness through facial monitoring.
* Compute EAR and MAR using Dlib.
* Use Mediapipe FaceMesh for better tracking.
* Log events in CSV with timestamp, user, and details.
* Auto-generate alert clips with FFmpeg.
* Provide Streamlit dashboard for review.
