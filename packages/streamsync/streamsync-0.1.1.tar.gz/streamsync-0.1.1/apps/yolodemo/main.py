import streamsync as ss
import cv2
import numpy as np
import json

base_path = '../apps/yolodemo/'

with open(f'{base_path}demoData/classes.json', 'r') as handle:
    class_dict = json.load(handle)
    class_dict = {int(key): val for key, val in class_dict.items()}


def load_network(config_path=f'{base_path}demoData/yolov4-tiny.cfg', weights_path=f'{base_path}demoData/yolov4-tiny.weights'):
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    output_layer_names = net.getLayerNames()
    output_layer_names = [output_layer_names[i - 1]
                          for i in net.getUnconnectedOutLayers()]
    return net, output_layer_names


net, output_layer_names = load_network()


def yolo(
    image,
    state,
    net=net,
    output_layer_names=output_layer_names,
    confidence_threshold=0.2,
    overlap_threshold=0.2,
    class_dict=class_dict,
    box_color=(0, 255, 0)
):
    blob = cv2.dnn.blobFromImage(
        image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layer_names)
    # Supress detections in case of too low confidence or too much overlap.
    boxes, confidences, class_IDs = [], [], []
    H, W = image.shape[:2]
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidence_threshold:
                box = detection[0:4] * np.array([W, H, W, H])
                centerX, centerY, width, height = box.astype("int")
                x, y = int(centerX - (width / 2)), int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_IDs.append(classID)
    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, confidence_threshold, overlap_threshold)
    if len(indices) > 0:
        # loop over the indexes we are keeping
        for i in indices.flatten():
            label = class_dict.get(class_IDs[i], None)
            if label is None:
                continue
            # extract the bounding box coordinates
            image = plot_box(image, boxes[i], label, confidences[i], box_color)
    img_png = cv2.imencode('.png', image)[1]
    state["detected"] = ss.pack_bytes(img_png, "image/png")


def plot_box(image, box, label, confidence, box_color):
    x, y, w, h = box[0], box[1], box[2], box[3]
    # label formatting
    cv2.rectangle(image, (x, y), (x+w, y+h), box_color, 2)
    label_conf = "{0:.0%}".format(confidence)
    text_label = f"{label}: {label_conf}"
    (text_w, text_h), _ = cv2.getTextSize(
        text_label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1
    )
    image = cv2.rectangle(image, (x, y - 20), (x + text_w, y), box_color, -1)
    image = cv2.putText(
        image, text_label, (x, y - 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
    )
    return image


def hello(state, payload):
    state["image"] = ss.pack_file(payload, "image/png")


def image_rec(payload, state):
    nparr = np.frombuffer(payload, np.uint8)
    img = cv2.imdecode(nparr, flags=1)
    yolo(img, state)


ss.init_state({
    "detected": None
})
