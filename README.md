# 🗂️ Advanced File Organizer Pro

![Logo](assets/images/logo.png)

A **stunning, modern GUI application** to organize your files with style and efficiency! Built with Python and PySide6, featuring a beautiful dark theme, real-time progress tracking, and advanced organization capabilities.

## ✨ Cool Features

### 🎨 **Modern Dark UI**
- Beautiful gradient-based dark theme
- Animated buttons with hover effects
- Professional two-panel layout with activity log
- Real-time progress bars and status updates
- Emoji-enhanced interface for better UX

### 🗂️ **Advanced File Organization**
- **📅 Time-based Organization:**
  - Creation Time, Modified Time, Last Accessed Time
  - Choose from Yearly, Monthly, or Daily grouping
- **📄 Smart File Extension Grouping:**
  - Categorized by type: Images, Audio, Video, Documents, Code
  - Custom extension filtering
- **📏 Intelligent File Size Categories:**
  - Tiny (< 1MB), Small (1-10MB), Medium (10-100MB)
  - Large (100MB-1GB), Huge (> 1GB)

### 🚀 **User Experience**
- **Drag & Drop Support** - Just drop folders onto the window
- **Real-time File Counting** - See exactly how many files will be organized
- **Live Activity Log** - Track all operations with timestamps
- **Progress Tracking** - Visual progress bars for all operations
- **Threading** - Non-blocking operations, UI stays responsive
- **Smart Tooltips** - Helpful hints throughout the interface

### 🔧 **Advanced Operations**
- **Directory Flattening** - Move all nested files to root folder
- **Subfolder Control** - Include or exclude subfolders in operations
- **Error Handling** - Graceful error management with user feedback
- **Confirmation Dialogs** - Safety prompts for destructive operations

### 🎯 **Professional Features**
- **Modern Architecture** - Clean separation of UI and business logic
- **Responsive Design** - Adapts to different window sizes
- **Customizable Styling** - Easy-to-modify QSS stylesheets
- **Cross-platform** - Works on Windows, macOS, and Linux

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PySide6
- Additional dependencies for enhanced features

### Quick Setup

1. **Clone the repository:**
```bash
git clone https://github.com/muhammedselcuk/advanced-file-organizer.git
cd advanced-file-organizer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

## 🎮 Usage Guide

### Getting Started
1. **📁 Select Directory**: Click "Browse" or drag & drop a folder
2. **⚙️ Choose Criteria**: Select how you want to organize your files
3. **🎯 Configure Options**: Fine-tune settings based on your criteria
4. **🚀 Execute**: Click "Organize Files" or "Flatten Directory"

### Organization Criteria

#### ⏰ **Time-based Organization**
Perfect for organizing photos, documents, or any files by date:
- **Yearly**: Creates folders like "2023", "2024"
- **Monthly**: Creates folders like "2024-01", "2024-02"
- **Daily**: Creates folders like "2024-01-15"

#### 📄 **File Extension Organization**
Great for sorting downloads or mixed file collections:
- **Smart Categories**: Images, Audio, Video, Documents, Code
- **Custom Selection**: Choose which file types to organize
- **Automatic Grouping**: Unknown extensions go to appropriate folders

#### 📏 **File Size Organization**
Useful for managing storage and finding large files:
- **Size Categories**: From tiny files to huge archives
- **Storage Management**: Easily identify space-consuming files
- **Selective Sorting**: Choose which size ranges to organize

### Advanced Operations

#### 📤 **Directory Flattening**
- Moves all files from subdirectories to the root folder
- Removes empty subdirectories automatically
- Handles naming conflicts intelligently
- Perfect for cleaning up deeply nested structures

#### 🗂️ **Subfolder Control**
- **Include Subfolders**: Process all files recursively
- **Exclude Subfolders**: Only process files in the selected directory
- Real-time file count updates based on selection

## 🎨 Customization

### Styling
The application uses QSS stylesheets for theming. Modify `src/styles.qss` to customize:
- Colors and gradients
- Button styles and animations
- Typography and spacing
- Component layouts

### Features
The modular architecture makes it easy to add new features:
- Add new organization criteria in `src/organizer.py`
- Extend the UI in `src/gui.py`
- Create new worker threads for background operations

## 🔧 Technical Details

### Architecture
- **Frontend**: PySide6 with custom QSS styling
- **Backend**: Pure Python with threading support
- **File Operations**: Cross-platform file handling
- **Error Handling**: Comprehensive exception management

### Performance
- **Non-blocking UI**: All file operations run in separate threads
- **Memory Efficient**: Streams large directory operations
- **Progress Tracking**: Real-time feedback for long operations
- **Responsive Design**: UI remains interactive during processing

## 🤝 Contributing

We welcome contributions! Areas for enhancement:
- Additional organization criteria
- More UI themes and customizations
- Advanced file filtering options
- Bulk operation capabilities
- Integration with cloud storage

## 📝 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

---

**Made with ❤️ and lots of ☕ by developers who understand the pain of messy file systems!**