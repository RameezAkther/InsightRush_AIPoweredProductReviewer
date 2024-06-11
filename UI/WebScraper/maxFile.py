import os

def get_max_numbered_csv(directory):
    files = os.listdir(directory)
    max_number = float('-inf')
    max_filename = None
    for file_name in files:
        if file_name.endswith('.csv'):
            try:
                file_number = int(os.path.splitext(file_name)[0])
                if file_number > max_number:
                    max_number = file_number
                    max_filename = file_name
            except ValueError:
                continue
    return max_filename

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

def get_max_numbered_png(directory):
    files = os.listdir(directory)
    max_number = float('-inf')
    max_filename = None
    for file_name in files:
        if file_name.endswith('.png'):
            try:
                file_number = int(os.path.splitext(file_name)[0])
                if file_number > max_number:
                    max_number = file_number
                    max_filename = file_name
            except ValueError:
                continue
    return max_filename