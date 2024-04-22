import os

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
            print(f"File: {file_name}, Car Count: {car_count_in_file}")
            total_car_count += car_count_in_file
    print(f"Total Car Count: {total_car_count}")
    return total_car_count

# Path to the directory containing label files
#labels_directory = 'runs/detect/exp/labels'

# Call the function to count cars in label files
#total_car_count = count_cars_in_label_files(labels_directory)
