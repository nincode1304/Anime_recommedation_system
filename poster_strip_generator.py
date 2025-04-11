from PIL import Image
import os

# === Config ===
POSTER_DIR = "posters"          # Your folder with all images
STRIPS = 3                      # Number of strips to generate
POSTERS_PER_STRIP = 8           # Number of posters per strip
RESIZE_HEIGHT = 200             # Common height for all posters
SPACING = 5                     # Optional spacing between posters

# === Load images ===
image_files = sorted([
    f for f in os.listdir(POSTER_DIR)
    if f.endswith(('.png', '.jpg', '.jpeg'))
])

# === Split into chunks ===
def chunkify(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

chunks = list(chunkify(image_files, POSTERS_PER_STRIP))

# === Process each strip ===
for idx, chunk in enumerate(chunks, 1):
    images = []
    for file in chunk:
        img_path = os.path.join(POSTER_DIR, file)
        img = Image.open(img_path).convert("RGB")
        ratio = RESIZE_HEIGHT / img.height
        new_width = int(img.width * ratio)
        resized = img.resize((new_width, RESIZE_HEIGHT))
        images.append(resized)

    total_width = sum(i.width for i in images) + SPACING * (len(images) - 1)
    strip = Image.new("RGB", (total_width, RESIZE_HEIGHT), (0, 0, 0))

    x_offset = 0
    for img in images:
        strip.paste(img, (x_offset, 0))
        x_offset += img.width + SPACING

    strip.save(f"strip{idx}.png")
    print(f"✅ strip{idx}.png generated!")
