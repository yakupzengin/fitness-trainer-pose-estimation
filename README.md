# AI-Powered Fitness Trainer Pose Estimation

This project brings an AI-powered workout tracking system that leverages pose estimation technology to count and monitor exercises in real-time. It provides instant feedback on your form, tracks repetitions, and motivates you to push through each set. Whether you're doing bicep curls, squats, or push-ups, this system ensures that every rep is counted and your technique is refined.

## Key Features

- **Real-Time Exercise Counting**: Uses advanced pose estimation to track and count your reps with high precision.
- **Stage Monitoring**: Tracks the "up" and "down" phases of each exercise and keeps you updated on your progress.
- **Progress Bar**: Visual progress bar tracks your sets and reps, motivating you to finish your workout strong.
- **Gauge Meter**: Provides feedback on limb angles, displayed on a gauge meter for real-time form analysis.
- **Customizable**: Supports adding new exercise types and metrics to suit your workout needs.

## Installation

To install and run the **AI-Powered Fitness Trainer Pose Estimation** project, follow these steps:

### Step 1: Clone the Repository
Clone the repository from GitHub to your local machine using the following command:

```bash
git clone https://github.com/yakupzengin/fitness-trainer-pose-estimation.git

cd fitness-trainer-pose-estimation
```
### Step 2: Install Dependencies
Ensure you have Python installed. Then, install the necessary dependencies using the following command:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
Once all dependencies are installed, run the main script to start tracking exercises:

```bash
python main.py
```

## Project Structure
Here’s an overview of the folders and files in this project, along with their purposes:

* **assets/** : This folder contains sounds assets used for the user interface and feedback displays.
* **data/**: Holds any datasets or configuration files needed for the pose estimation or workout tracking.
* **exercises/**: Contains individual scripts for tracking different exercises.
  * `hammer_curl.py`: Handles tracking and counting of hammer curl exercises.
  * `push_up.py`: Monitors push-up repetitions and form.
  * `squat.py`: Tracks squats, including form and repetition counting.
* **feedback/**:Handles the visual and informational feedback provided to the user during exercises.
  * `indicators.py`: Displays real-time feedback indicators, such as rep counts and form status.
  * `information.py`: Provides detailed feedback and stats about exercise performance.
  * `layout.py`: Manages how feedback is laid out on the screen, including progress bars and indicators.
* **output/**: Stores output data or video files that capture your workout sessions and provide detailed analysis.
* **pose_estimation/**: This folder contains the core logic for the pose estimation process.
  * `angle_calculation.py`: Responsible for calculating the angles of joints during exercises, providing real-time feedback on form.
  * `estimation.py`: Handles the pose estimation process using machine learning models to track your movements.
* **utils/**: Ekranda geri bildirim çizmek ve görüntülemek için yardımcı fonksiyonlar bulunur.
  * `draw_text_with_background.py`: Utility functions for drawing and displaying feedback on the screen.
    * `drawing_utils.py`: Helper functions for drawing elements on the video frame, such as progress bars and limb angles.
* **main.py**: The main script that initializes the entire system. It starts video capture, loads the pose estimation model, and processes your workout, providing real-time feedback and performance tracking.


## Future Improvements

As this project evolves, the following features are planned for future releases:

- **Advanced Exercise Recognition**: Expanding the system to support a wider range of exercises, including compound movements and stretches.
- **Performance Analytics**: Adding detailed post-workout analytics to help users track progress over time and improve their form.
- **Voice Feedback**: Implementing voice feedback for form corrections and motivational cues during exercises.
- **Mobile Support**: Developing a mobile version of the application for more convenience during workouts.

## Contributing

Contributions to improve this project are welcome! If you would like to contribute, please fork the repository and submit a pull request. You can also report any issues or suggest new features by opening an issue on GitHub.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.
