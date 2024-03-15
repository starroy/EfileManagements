# import json
# import ftfy
import numpy as np


def get_data(frame, class_name_dict, model, threshold, reader):
    data_dict = {}
    results = model(frame)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
            img = frame[int(y1) : int(y2), int(x1) : int(x2)]
            # gray_roi = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # gray_roi = cv2.bitwise_not(gray_roi)
            #
            # thresh_roi = cv2.threshold(
            #     gray_roi, 0, 100, cv2.THRESH_BINARY | cv2.THRESH_OTSU
            # )[1]

            id = class_name_dict[int(class_id)]
            # text = reader.readtext(gray_roi)
            text = reader.readtext(img)
            # text = ftfy.fix_text(text)
            # text = ftfy.fix_encoding(text)
            if len(text) > 0:
                confidence = [i[-1] for i in text]
                l_np = np.asarray(confidence)
                best_idx = l_np.argmax()

            # text_thresh = pt.image_to_string(thresh_roi)
            # print("Threshold:", text_thresh)
            if len(text) > 0:
                data_dict[id] = text[best_idx][1]
    # data = json.dumps(data_dict, indent=4)
    return data_dict
