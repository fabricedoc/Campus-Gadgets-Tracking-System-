import os

# Create required directories
folders = ['templates', 'web_uploads', 'student_photos']

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")
    else:
        print(f"Folder already exists: {folder}")

print("All required folders are ready!")