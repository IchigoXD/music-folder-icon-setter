import os
import sys
from PIL import Image
import win32api
import win32con
import win32gui
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def set_folder_icon(folder_path, image_path):
    try:
        # Convert image to icon
        img = Image.open(image_path)
        icon_path = os.path.join(folder_path, 'folder.ico')
        img.save(icon_path, format='ICO')

        # Create desktop.ini file
        ini_path = os.path.join(folder_path, 'desktop.ini')
        with open(ini_path, 'w') as f:
            f.write('[.ShellClassInfo]\n')
            f.write(f'IconFile={os.path.basename(icon_path)}\n')
            f.write('IconIndex=0\n')

        # Set file attributes
        win32api.SetFileAttributes(icon_path, win32con.FILE_ATTRIBUTE_HIDDEN)
        win32api.SetFileAttributes(ini_path, win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
        win32api.SetFileAttributes(folder_path, win32con.FILE_ATTRIBUTE_READONLY)

        # Refresh icon cache
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 0)
        
        return True
    except Exception as e:
        logger.error(f"Error setting icon for {folder_path}: {str(e)}")
        return False

def find_cover_image(folder_path):
    """Find the first image that could be an album cover."""
    possible_names = ['cover', 'folder', 'album', 'front']
    image_extensions = ['.jpg', '.jpeg', '.png']
    
    # First, look for exact matches
    for name in possible_names:
        for ext in image_extensions:
            full_name = name + ext
            full_path = os.path.join(folder_path, full_name)
            if os.path.exists(full_path):
                return full_path
            
            # Try uppercase variants
            full_name_upper = name.upper() + ext
            full_path_upper = os.path.join(folder_path, full_name_upper)
            if os.path.exists(full_path_upper):
                return full_path_upper
    
    # If no exact match, look for any image file containing these words
    for file in os.listdir(folder_path):
        if any(ext in file.lower() for ext in image_extensions):
            if any(name in file.lower() for name in possible_names):
                return os.path.join(folder_path, file)
    
    # If still no match, just get the first image file
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            return os.path.join(folder_path, file)
    
    return None

def process_music_folders(root_path):
    total_processed = 0
    successful_changes = 0

    for current_folder, subfolders, files in os.walk(root_path):
        logger.info(f"Scanning: {current_folder}")
        
        cover_path = find_cover_image(current_folder)
        if cover_path:
            total_processed += 1
            logger.info(f"Found cover image: {cover_path}")
            
            if set_folder_icon(current_folder, cover_path):
                successful_changes += 1
                logger.info("✅ Icon set successfully!")
            else:
                logger.warning("❌ Failed to set icon.")
    
    return total_processed, successful_changes

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python script.py <music_root_folder>")
        sys.exit(1)
    
    music_root = sys.argv[1]
    if not os.path.exists(music_root):
        logger.error(f"Error: Path {music_root} does not exist.")
        sys.exit(1)

    logger.info(f"Starting to process folders under: {music_root}")
    total, successful = process_music_folders(music_root)
    
    logger.info(f"\nSummary:")
    logger.info(f"Total folders processed: {total}")
    logger.info(f"Successful icon changes: {successful}")
    logger.info(f"Failed icon changes: {total - successful}")

if __name__ == "__main__":
    main()