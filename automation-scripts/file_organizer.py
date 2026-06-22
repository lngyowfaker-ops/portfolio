"""
File Organizer Script
Automatically organize files by type
"""

import os
import shutil
from pathlib import Path

# Define file categories
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.php', '.rb'],
}

def organize_folder(folder_path):
    """
    Organize files in a folder by type

    Args:
        folder_path: Path to folder to organize
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"❌ Folder not found: {folder_path}")
        return

    print(f"📂 Organizing: {folder_path}\n")

    stats = {}

    for file in folder.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            ext = file.suffix.lower()

            # Find category
            category = 'Others'
            for cat, extensions in FILE_CATEGORIES.items():
                if ext in extensions:
                    category = cat
                    break

            # Create category folder
            category_folder = folder / category
            category_folder.mkdir(exist_ok=True)

            # Move file
            new_path = category_folder / file.name
            counter = 1
            while new_path.exists():
                new_path = category_folder / f"{file.stem}_{counter}{file.suffix}"
                counter += 1

            shutil.move(str(file), str(new_path))

            # Update stats
            stats[category] = stats.get(category, 0) + 1
            print(f"  ✓ {file.name} → {category}/")

    # Summary
    print(f"\n📊 Summary:")
    total = sum(stats.values())
    for cat, count in sorted(stats.items()):
        print(f"  {cat}: {count} files")
    print(f"  Total: {total} files organized")

if __name__ == "__main__":
    folder = input("Enter folder path to organize: ").strip()

    if folder:
        organize_folder(folder)
    else:
        print("❌ Please enter a folder path")
