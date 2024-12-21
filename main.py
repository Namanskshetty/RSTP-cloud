import modules.speedtest as sp
import cv2

def Video():
    print("insie")
# Replace with your RTSP stream URL
    rtsp_urls = ["rtsp://sterling:1KKDo&882v!jA!l0^N6Ox^b9%^r@192.168.1.38/stream1",
                "rtsp://sterling:1KKDo&882v!jA!l0^N6Ox^b9%^r@192.168.1.35/stream1"]

    # Open the RTSP streams
    caps = [cv2.VideoCapture(url) for url in rtsp_urls]

    # Check if all streams are opened successfully
    if any(not cap.isOpened() for cap in caps):
        print("Error: Could not open one or more RTSP streams.")
        exit()

    # Define the codec and create VideoWriter objects
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    outs = [
        cv2.VideoWriter(f'output{i}.avi', fourcc, 20.0, (int(caps[i].get(3)), int(caps[i].get(4)))) for i in range(len(caps))
    ]

    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                print(f"Error: Failed to capture frame from stream {i}.")
                continue

            # Write the frame to the output file
            outs[i].write(frame)

            # Display the frame (optional)
            cv2.imshow(f'RTSP Stream {i}', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything when done
    for cap, out in zip(caps, outs):
        cap.release()
        out.release()
    cv2.destroyAllWindows()




print("Start..")
# speed=sp.main()
speed=50
if speed<5:
    check=input("The speed is very slow!! ("+str(speed)+") Do you wish to continue Y/N. ")
    if check.lower()!='y':
        prin('Bye')
        exit()
    else:
        print("Continue")
else:
    print("pass")
    Video()
