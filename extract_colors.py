from PIL import Image
import sys
from collections import Counter

def get_dominant_colors(image_path, num_colors=5):
    try:
        img = Image.open(image_path).convert('RGBA')
        
        # Resize to speed up processing
        img = img.resize((150, 150))
        
        pixels = img.getdata()
        
        # Filter out transparent or fully white pixels
        valid_pixels = []
        for r, g, b, a in pixels:
            # Ignore transparent pixels
            if a < 50:
                continue
            # Ignore white/near-white pixels
            if r > 240 and g > 240 and b > 240:
                continue
            # Ignore black/near-black
            if r < 15 and g < 15 and b < 15:
                continue
            
            # Simple color quantization to avoid finding minute differences
            qr = (r // 15) * 15
            qg = (g // 15) * 15
            qb = (b // 15) * 15
            
            valid_pixels.append((qr, qg, qb))
            
        color_counts = Counter(valid_pixels)
        dominant_colors = color_counts.most_common(num_colors)
        
        print("Dominant Colors (RGB):")
        for color, count in dominant_colors:
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            print(f"{hex_color} - RGB{color} - Count: {count}")
            
    except Exception as e:
        print(f"Error extracting colors: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_dominant_colors(sys.argv[1])
    else:
        get_dominant_colors("/Users/narlonsilva/Desktop/silvalab/logo.png")
