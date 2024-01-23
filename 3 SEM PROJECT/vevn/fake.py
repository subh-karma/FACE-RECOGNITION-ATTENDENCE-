import cv2

# Specify the file path
file_path = "Resources/backgrou.png"

# Load the image
img = cv2.imread(file_path)

# Check if the image was loaded successfully
if img is not None:
    print("hain na pic")
    # Your further processing here
else:
    print(f"Error: Unable to load the image from {file_path}. Check file path/integrity.")