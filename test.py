import cv2
import numpy as np
import time

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load class names
with open("coco.names", "r") as f:
    classes = f.read().splitlines()

layer_names = net.getLayerNames()

# Change made as per your request
try:
    # Ensure net.getUnconnectedOutLayers() returns correct indexes
    unconnected_layers = net.getUnconnectedOutLayers()
    output_layers = [layer_names[i - 1] for i in unconnected_layers.flatten()]
except IndexError as e:
    print(f"IndexError: {e}")
    output_layers = []

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Replace with your RTSP stream URLs
rtsp_urls = ["rtsp://sterling:1KKDo&882v!jA!l0^N6Ox^b9%^r@192.168.1.38/stream2",
            "rtsp://sterling:1KKDo&882v!jA!l0^N6Ox^b9%^r@192.168.1.35/stream2"]


# Open RTSP streams
caps = [cv2.VideoCapture(url) for url in rtsp_urls]

# Check if all streams are opened successfully
if any(not cap.isOpened() for cap in caps):
    print("Error: Could not open one or more RTSP streams.")
    exit()

# Initialize video writers
outs = [None] * len(caps)

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to capture frame from stream {i}.")
            continue

        height, width, channels = frame.shape

        # Detect objects in frame
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs_net = net.forward(output_layers)

        # Information to show on screen
        class_ids = []
        confidences = []
        boxes = []

        for out in outs_net:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        detected = False
        for j in range(len(boxes)):
            if j in indexes:
                x, y, w, h = boxes[j]
                label = str(classes[class_ids[j]])
                if label in ["person", "car", "motorbike", "bus", "truck"]:
                    detected = True
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Write frame to file if detected
        if detected:
            if outs[i] is None:
                outs[i] = cv2.VideoWriter(f'output{i}_{time.time()}.avi', fourcc, 20.0, (width, height))
            outs[i].write(frame)

        # Display the frame (optional)
        cv2.imshow(f'RTSP Stream {i}', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release all resources
for cap, out in zip(caps, outs):
    if cap is not None:
        cap.release()
    if out is not None:
        out.release()
cv2.destroyAllWindows()
