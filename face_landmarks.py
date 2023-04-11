import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6)


def get_iris_data(frame):
    iris_data = {}
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    img_h, img_w, c = frame.shape

    try:
        mesh_points = np.array(
            [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in
             results.multi_face_landmarks[0].landmark])

        (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
        center_left = np.array([l_cx, l_cy], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np.int32)

        iris_data['Left Iris Landmarks'] = [(int(x[0]), int(x[1])) for x in mesh_points[LEFT_IRIS]]
        iris_data['Left Iris Centre'] = (int(center_left[0]), int(center_left[1]))
        iris_data['Right Iris Landmarks'] = [(int(x[0]), int(x[1])) for x in mesh_points[RIGHT_IRIS]]
        iris_data['Right Iris Centre'] = (int(center_right[0]), int(center_right[1]))


        cv2.circle(frame, center_left, int(l_radius), (0, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(frame, center_right, int(r_radius), (0, 255, 255), 1, cv2.LINE_AA)

        cx_min = img_w
        cy_min = img_h
        cx_max = cy_max = 0
        for faceLms in results.multi_face_landmarks:
            for id, lm in enumerate(faceLms.landmark):
                cx, cy = int(lm.x * img_w), int(lm.y * img_h)
                if cx < cx_min:
                    cx_min = cx
                if cy < cy_min:
                    cy_min = cy
                if cx > cx_max:
                    cx_max = cx
                if cy > cy_max:
                    cy_max = cy
        cv2.rectangle(frame, (cx_min, cy_min), (cx_max, cy_max), (255, 0, 0), 2)
        iris_data['Face Rectangle'] = {"x1":int(cx_min), "y1":int(cy_min), "x2":int(cx_max), "y2":int(cy_max)}

    except:
        pass
    return iris_data, frame


def main(image_path):

    # ret, frame = cv2.VideoCapture(0).read()
    image = cv2.imread(image_path)
    # try:
    iris_data, frame_processed = get_iris_data(image)

    # except:
    #     iris_data = {}
        # frame_processed = image
    # print(iris_data)
    return True, iris_data, frame_processed
    # cv2.imshow('asd', frame_processed)
    # cv2.waitKey()