Step-1 : Install all the requirements in requirements.txt using the command pip install -r requirements.txt

Step-2 : Download FER-2013 Dataset from https://drive.google.com/file/d/1UfzOP-l2-zKIsoch_xqsij7FkoubH7hM/view?usp=sharing and copy it in Team_Gladiators_Student_Engagement_Tracker/Data/

Step-3 : Download shape_predictor_68_face_landmarks.dat from https://drive.google.com/file/d/15qwzoyo5gwibpQzQ5yPfCUDkJiMAj7ub/view?usp=sharing and copy it in \Team_Gladiators_Student_Engagement_Tracker\gaze_tracking\trained_models\

Step-4 : To analyze real-time video, execute the following command in the "./cam" directory using parallel processing: "python Eyegaze_Live_Cam.py" and "python Emotion_Live_Cam.py". This will initiate webcam capture and perform engagement analysis.

Once the processing is complete, you will receive four outputs: "Result_Eyegaze_Live.txt" and "Result_Emotion_Live.txt" containing the analysis results, and video files named "Output_Eyegaze_Cam.mp4" and "Output_Emotion_Cam.mp4" with annotated visualizations.