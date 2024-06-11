import cv2
import os

def get_max_numbered_jpg(directory):
    files = os.listdir(directory)
    max_number = float('-inf')
    max_filename = None
    for file_name in files:
        if file_name.endswith('.jpg'):
            try:
                file_number = int(os.path.splitext(file_name)[0])
                if file_number > max_number:
                    max_number = file_number
                    max_filename = file_name
            except ValueError:
                continue
    return max_filename

def remove_background():
    dir = 'C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image\\'
    fileName = get_max_numbered_jpg(dir)
    image = cv2.imread(dir+"\\"+fileName)

    # Convert the image to BGRA
    image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, alpha = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Invert the mask
    alpha = cv2.bitwise_not(alpha)

    # Add the new alpha channel to the image
    image_bgra[:, :, 3] = alpha

    # Save the result
    cv2.imwrite(dir+"\\"+fileName.replace('.jpg', '.png'), image_bgra)

#remove_background()
