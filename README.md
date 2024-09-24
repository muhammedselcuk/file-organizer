# File Organizer

![Logo](assets/images/logo.png)

A user-friendly GUI application to organize your files efficiently based on various criteria. Built with Python and PyQt5.

## Features

- Organize files by:
  - Creation Time
  - Modified Time
  - Last Accessed Time
  - File Extension
  - File Size
- **Time Period Selection for Time-Based Criteria:**
  - Yearly
  - Monthly (default)
  - Daily
- Exclude or include subfolders.
- Flatten directory structure.
- Drag and drop support for selecting folders.
- Displays total number of files to be organized.

## Installation

### Prerequisites

- Python 3.6 or higher
- PyQt5

### Steps

1. **Clone the repository:**

   ```
 git clone https://github.com/muhammedselcuk/file-organizer.git
    ```

   
Navigate to the project directory:
       ```
      cd file-organizer
        ```

    

Install the required packages:
       ```
    pip install -r requirements.txt
        ```

Usage
   Run the application:
       ```
      python main.py
        ```

Using the GUI:

Select Folder:

Click the "Select Folder" button to choose a directory.
Or drag and drop a folder onto the application window.
Organize By: Select the criterion for organizing files.
If you select a time-based criterion (Creation Time, Modified Time, Last Accessed Time), you can choose the time period (Yearly, Monthly, Daily).
If you select File Extension or File Size, additional options will appear to fine-tune the operation.
Exclude Subfolders: Check this box if you want to exclude files in subdirectories.
Organize: Click to start organizing files based on your selections.
Flatten Directory: Moves all files to the root of the selected directory, optionally excluding subfolders.
Total Files: Displays the total number of files that will be affected by the operation.