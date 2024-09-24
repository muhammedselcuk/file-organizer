import os
import shutil
from datetime import datetime


def organize_files(folder_path, criteria='creation_time', options=None, include_subfolders=True, time_period=None):
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder {folder_path} does not exist.")

    if include_subfolders:
        items = []
        for root, _, files in os.walk(folder_path):
            for name in files:
                items.append(os.path.join(root, name))
    else:
        items = [
            os.path.join(folder_path, item)
            for item in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, item))
        ]

    if not items:
        return

    for item_path in items:
        folder_name = get_destination_folder(item_path, criteria, options, time_period)
        if folder_name is None:
            continue  # Skip if the file doesn't meet the criteria

        target_folder = os.path.join(folder_path, folder_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        try:
            shutil.move(item_path, os.path.join(target_folder, os.path.basename(item_path)))
        except Exception as e:
            print(f"Error moving {item_path}: {e}")

def get_destination_folder(item_path, criteria, options, time_period):
    if criteria in ['creation_time', 'modified_time', 'last_accessed_time']:
        if criteria == 'creation_time':
            timestamp = os.path.getctime(item_path)
        elif criteria == 'modified_time':
            timestamp = os.path.getmtime(item_path)
        elif criteria == 'last_accessed_time':
            timestamp = os.path.getatime(item_path)
        date = datetime.fromtimestamp(timestamp)
        # Determine the folder name based on the time period
        period = time_period if time_period else 'Monthly'  # Default to monthly
        if period == 'Yearly':
            folder_name = date.strftime("%Y")
        elif period == 'Monthly':
            folder_name = date.strftime("%Y-%m")
        elif period == 'Daily':
            folder_name = date.strftime("%Y-%m-%d")
        else:
            folder_name = date.strftime("%Y-%m")  # Default to monthly
    elif criteria == 'file_extension':
        if os.path.isfile(item_path):
            ext = os.path.splitext(item_path)[1].lower().strip('.')
            if options and ext not in options:
                return None  # Skip this file
            folder_name = ext if ext else 'no_extension'
        else:
            return None  # Skip directories
    elif criteria == 'file_size':
        size = os.path.getsize(item_path)
        if options:
            matched = False
            for label, min_size, max_size in options:
                if min_size <= size < max_size:
                    folder_name = label
                    matched = True
                    break
            if not matched:
                return None  # Skip this file
        else:
            # Default size categories
            if size < 1024 * 1024:
                folder_name = 'Small Files'
            elif size < 1024 * 1024 * 100:
                folder_name = 'Medium Files'
            else:
                folder_name = 'Large Files'
    else:
        # Default to creation time monthly
        timestamp = os.path.getctime(item_path)
        date = datetime.fromtimestamp(timestamp)
        folder_name = date.strftime("%Y-%m")

    return folder_name

def move_files_to_parent(folder_path, include_subfolders=True):
    if include_subfolders:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if root != folder_path:
                    try:
                        shutil.move(file_path, folder_path)
                    except Exception as e:
                        print(f"Error moving {file_path}: {e}")
            # Remove empty directories
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                except OSError:
                    pass  # Directory not empty or other error
    else:
        # Only move files from the selected directory
        items = [
            os.path.join(folder_path, item)
            for item in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, item))
        ]
        for item_path in items:
            try:
                shutil.move(item_path, folder_path)
            except Exception as e:
                print(f"Error moving {item_path}: {e}")
