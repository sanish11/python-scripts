#python script for organizing the files
import os
import shutil

# Define the folder to organize
source_folder = '/path/to/your/folder'

# Define destination folders for different file types
folders = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Audio': ['.mp3', '.wav'],
    'Others': []
}

# Create the destination folders if they don't exist
for folder in folders:
    if not os.path.exists(os.path.join(source_folder, folder)):
        os.makedirs(os.path.join(source_folder, folder))

# Loop through files in the source folder
for filename in os.listdir(source_folder):
    file_ext = os.path.splitext(filename)[1].lower()
    moved = False
    for folder, extensions in folders.items():
        if file_ext in extensions:
            shutil.move(os.path.join(source_folder, filename), os.path.join(source_folder, folder, filename))
            moved = True
            break
    # Move files with unknown extensions to the 'Others' folder
    if not moved:
        shutil.move(os.path.join(source_folder, filename), os.path.join(source_folder, 'Others', filename))

print("Files have been organized successfully!")