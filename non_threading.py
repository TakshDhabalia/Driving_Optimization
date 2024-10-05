import os
import time
import subprocess
import MQTT
import osp
import Camera as cam 

# Global variable to store car detection results
car_count = 0

# Function to run YOLOv5 detection on an image
def run_yolov5_detection(image_path):
    global car_count
    
    # Run YOLOv5 detection
    command = [
        "python", "detect.py",
        "--weights", "yolov5s.pt",
        "--source", image_path,
        "--conf-thres", "0.25",   # Confidence threshold for detection
        "--iou-thres", "0.45",    # IoU threshold for NMS
        "--save-txt",             # Save results to text files
        "--classes", "2",         # Specify only car class
        "--project", "runs/detect", # Output directory
        "--name", "exp1",          # Experiment name
        "--exist-ok"              # Overwrite if exists
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to count cars in a label file
def count_cars_in_label_file(label_file_path):
    car_count = 0
    with open(label_file_path, 'r') as file:
        for line in file:
            class_id = line.split()[0]
            if class_id == '2':  # Check if the class ID is for a car
                car_count += 1
    return car_count

# Function to iterate through label files and count cars
def count_cars_in_label_files(labels_directory):
    total_car_count = 0
    for file_name in os.listdir(labels_directory):
        if file_name.endswith('.txt'):
            label_file_path = os.path.join(labels_directory, file_name)
            car_count_in_file = count_cars_in_label_file(label_file_path)
            total_car_count += car_count_in_file
    return total_car_count

# Function to continuously monitor images and perform detection
def monitor_images(freq):
    global car_count
    
    for i in range(freq):
        # Capture image
        cam.capture_images("http://192.168.1.14:8080/video", 3)
        
        # Run YOLOv5 detection on the captured image
        run_yolov5_detection(f"images/{i}.jpeg")
        
        # Count cars in label files
        current_car_count = count_cars_in_label_files('runs/detect/exp1/labels')
        
        # Print car count information
        print(f"At t={i+1}, Total Cars Detected: {current_car_count} in {i}.jpeg")
        
        time.sleep(2)

if __name__ == "__main__":
    # Create the images directory if not exists
    if not os.path.exists("images"):
        os.makedirs("images")

    # Start monitoring images sequentially
    client = MQTT.MQTTClient("172.28.66.244", 2000)
    client.connect()
    monitor_images(100)
    client.publish_loop("ESIOT", monitor_images(freq=100), 100)

