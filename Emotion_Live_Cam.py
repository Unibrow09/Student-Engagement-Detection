import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.optimizers import Adam
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

ap = argparse.ArgumentParser()
ap.add_argument("--mode", help="train/display")
mode = ap.parse_args().mode

face_exist = 0
face_exist_percent = 0
pos_interest = 0
neg_interest = 0
sum_interest = 0
abs_interest = 0
net_interest = 0
pos_percent = 0
neg_percent = 0
net_percent = 0

abs_percent = 0
al_cond = 0
face_true = 0
face_false = 0
angry_count = 0
disgust_count = 0
scared_count = 0
happy_count = 0
neutral_count = 0
sad_count = 0
surprised_count = 0
angry_percent = 0
disgust_percent = 0
scared_percent = 0
happy_percent = 0
neutral_percent = 0
sad_percent = 0
surprised_percent = 0
face_cond = ""
temp = 1
max_response = 0
response = ""
impression = ""
face_val = 0
presence2 = ""

train_dir = 'data/train'
val_dir = 'data/test'
num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(48, 48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(48, 48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights('model.h5')

cv2.ocl.setUseOpenCL(False)

emotion_dict = {0: "Negative - Angry", 1: "Negative - Disgusted", 2: "Negative - Scared",
                3: "Positive - Happy", 4: "Neutral - Neutral", 5: "Negative - Sad", 6: "Positive - Surprised"}

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Unable to read video")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter('Output_Eyegaze_Live_Cam.mp4', cv2.VideoWriter_fourcc("m", "p", "4", "v"), 20, (frame_width, frame_height))

while True:
   
    ret, frame = cap.read()
    if not ret:
        break
    face_cascade = cv2.CascadeClassifier('haarcascade_files/haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    face_found = False
    for (x, y, w, h) in faces:
        if w > 0:
            face_found = True
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)
        max_index = int(np.argmax(prediction))
        cv2.putText(frame, emotion_dict[max_index], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        if max_index == 0:
            angry_count += 1
            neg_interest += 1
        elif max_index == 1:
            disgust_count += 1
            neg_interest += 1
        elif max_index == 2:
            scared_count += 1
            neg_interest += 1
        elif max_index == 3:
            happy_count += 1
            pos_interest += 1
        elif max_index == 4:
            neutral_count += 1
            net_interest += 1
        elif max_index == 5:
            sad_count += 1
            neg_interest += 1
        elif max_index == 6:
            surprised_count += 1
            pos_interest += 1
        else:
            abs_interest += 1

        sum_interest = angry_count + disgust_count + scared_count + happy_count + neutral_count + sad_count + surprised_count
        face_exist = pos_interest + neg_interest

        pos_percent = round(((pos_interest * 100) / sum_interest), 2) if sum_interest != 0 else 0
        neg_percent = round((neg_interest * 100 / sum_interest), 2) if sum_interest != 0 else 0
        net_percent = round((net_interest * 100 / sum_interest), 2) if sum_interest != 0 else 0
        neutral_percent = round((neutral_count * 100 / sum_interest), 2) if sum_interest != 0 else 0
        disgust_percent = round((disgust_count * 100 / sum_interest), 2) if sum_interest != 0 else 0
        angry_percent = round((angry_count * 100 / sum_interest), 2) if sum_interest != 0 else 0
        happy_percent = round((happy_count * 100 / sum_interest), 2) if sum_interest != 0 else 0
        sad_percent = round((sad_count * 100 / sum_interest), 2) if sum_interest != 0 else 0
        surprised_percent = round((surprised_count * 100 / sum_interest), 2) if sum_interest != 0 else 0
        scared_percent = round((scared_count * 100 / sum_interest), 2) if sum_interest != 0 else 0

    if face_found:
        face_cond = "Yes"
        face_val += 1
    else:
        face_cond = "No"

    max_response = max(net_percent, pos_percent, neg_percent)
    if net_percent == max_response and net_percent != 0:
        response = "Neutral"
    elif pos_percent == max_response and pos_percent != 0:
        response = "Positive"
    elif neg_percent == max_response and neg_percent != 0:
        response = "Negative"
    else:
        response = "No Attendance (null)"

    if net_percent + pos_percent < neg_percent and (net_percent + pos_percent != 0):
        impression = "Bad"
    elif net_percent + pos_percent >= neg_percent and neg_percent != 0:
        impression = "Good"
    else:
        impression = "No Attendance (null)"

    cv2.putText(frame, "Detected Face Percentage:  " + str(face_exist_percent) + " %", (50, 530), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 0, 0), 2)
    cv2.putText(frame, "Undetected Face Percentage:  " + str(abs_percent) + " %", (50, 560), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "  Presence: " + str(face_cond), (20, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame, "  Impression: " + str(impression), (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame, "  Overall Emotional Response: " + str(response), (20, 490), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame, "Neutral Response Percentage: " + str(net_percent) + " %", (50, 530), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "Positive Response Percentage: " + str(pos_percent) + " %", (50, 560), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "Negative Response Percentage: " + str(neg_percent) + " %", (50, 590), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "Neutral Responses Count: " + str(net_interest), (50, 620), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "Positive Responses Count: " + str(pos_interest), (50, 650), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "Negative Responses Count: " + str(neg_interest), (50, 680), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)

    out.write(frame)
    cv2.imshow("Participant Detection and Emotion Recognition", frame)

    if face_val >= 1:
        presence2 = "Yes"
    else:
        presence2 = "No"

    f = open("Result_Emotion_Live_Cam.txt", "w")
    f.write("TEAM GLADIATORS\n\n")
    f.write("MachineKnight Season 2 \n\n")
    f.write("  Presence                  : " + str(presence2) + "\n")
    f.write("  Impression               : " + str(impression) + "\n")
    f.write("  Overall Emotional Response : " + str(response) + "\n\n")

    f.write("  Neutral Response Percentage : " + str(net_percent) + " % \n")
    f.write("  Positive Response Percentage: " + str(pos_percent) + " % \n")
    f.write("  Negative Response Percentage : " + str(neg_percent) + " % \n\n")

    f.write("  Neutral Responses Count      : " + str(net_interest) + "\n")
    f.write("  Positive Responses Count     : " + str(pos_interest) + "\n")
    f.write("  Negative Responses Count     : " + str(neg_interest) + "\n\n\n")

    f.write("  Neutral:   " + str(neutral_percent) + " % \n")
    f.write("  Happy:     " + str(happy_percent) + " % \n")
    f.write("  Sad:       " + str(sad_percent) + " % \n")
    f.write("  Angry:     " + str(angry_percent) + " % \n")
    f.write("  Scared:    " + str(scared_percent) + " % \n")
    f.write("  Surprised: " + str(surprised_percent) + " % \n")
    f.write("  Disgusted: " + str(disgust_percent) + " % \n\n")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()

cv2.destroyAllWindows()
