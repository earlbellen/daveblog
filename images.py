import os
import re
import shutil
import glob

# === Paths ===
posts_dir = r"D:\Users\Admin\Documents\02_PROJECTS\Blog\daveblog\content\posts"
attachments_dir = r"D:\Users\Admin\iCloudDrive\iCloud~md~obsidian\Zettelkasten\98 ATTACHMENTS"
static_images_dir = r"D:\Users\Admin\Documents\02_PROJECTS\Blog\daveblog\static\images"

# Ensure destination directory exists
os.makedirs(static_images_dir, exist_ok=True)

# === Process each markdown file ===
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\n📄 Processing: {filename}")

        # Read markdown file with BOM support (utf-8-sig)
        with open(filepath, "r", encoding="utf-8-sig") as file:
            content = file.read()

        # DEBUG: Check what's in the file
        # print("📄 Raw content:\n", content)

        # Match Obsidian-style embeds like ![[image.png]]
        image_matches = re.findall(r'!\[\[\s*([^\]]+\.(?:png|jpg|jpeg|webp))\s*\]\]', content, re.IGNORECASE)

        if not image_matches:
            print("⚠ No image embeds found.")
            continue

        for image_name in image_matches:
            print(f"🔗 Found image embed: {image_name}")

            # Look for the image file (including subfolders)
            search_pattern = os.path.join(attachments_dir, "**", image_name)
            matches = glob.glob(search_pattern, recursive=True)

            if matches:
                image_path = matches[0]
                destination_path = os.path.join(static_images_dir, os.path.basename(image_path))

                try:
                    shutil.copy2(image_path, destination_path)
                    print(f"✅ Copied: {image_path} ➡ {destination_path}")
                except Exception as e:
                    print(f"❌ Error copying file: {e}")

                # Replace Obsidian-style embed with Hugo-style Markdown image link
                markdown_image = f"![Image Description](/images/{image_name.replace(' ', '%20')})"
                content = content.replace(f"![[{image_name}]]", markdown_image)
            else:
                print(f"🚫 Image file not found: {image_name}")

        # Write updated markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("\n✅ All markdown files processed and images copied!")
