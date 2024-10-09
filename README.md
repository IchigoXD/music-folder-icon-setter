# Music Folder Icon Setter

Automatically set album cover images as folder icons for your music collection download from spotify or Soggfy on Windows.
![screenshot](ScreenshotMusic.png)
## Features
- Recursively scans music folders
- Automatically finds album cover images (images must be named like '''cover.jpg''')
- Sets folder icons based on found images
- Supports multiple image formats (JPG, PNG)
- Detailed logging of all operations

## Requirements
- Windows operating system
- Python 3.6 or higher
- PIL (Pillow) library
- pywin32 library

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/music-folder-icon-setter.git
cd music-folder-icon-setter
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the script from the command line:
```
python folder_icon_setter.py "C:\path\to\your\music\folder"
```

The script will:
1. Scan all subfolders in the specified directory
2. Find cover images in each folder
3. Convert these images to icons
4. Set the folder icons accordingly

## File Structure
```
music-folder-icon-setter/
│
├── folder_icon_setter.py    # Main script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore file
```

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
