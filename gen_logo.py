import requests
from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # 1. Download Comfortaa font
    font_url = "https://github.com/googlefonts/comfortaa/raw/main/fonts/TTF/Comfortaa-Bold.ttf"
    font_path = "Comfortaa-Bold.ttf"
    
    if not os.path.exists(font_path):
        print("Downloading Comfortaa font...")
        response = requests.get(font_url)
        with open(font_path, 'wb') as f:
            f.write(response.content)

    # 2. Setup image dimensions and colors
    width = 3600
    height = 1200
    bg_color = (255, 255, 255, 0) # Transparent
    purple_rgb = (54, 22, 92) # #36165c for the deep purple
    purple_color = (*purple_rgb, 255)
    
    # Create blank canvas
    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 3. Load Font
    try:
        font_size = 540
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    # 4. Text parts
    text_silva = "silva"
    text_l = "l"
    text_b = "b"
    
    # Get 'a' dimensions for exact brain scaling
    bbox_a = draw.textbbox((0, 0), "a", font=font)
    a_height = bbox_a[3] - bbox_a[1]
    
    tracking = -40 # reduce letter spacing explicitly (was naturally quite wide)
    
    # 5. Extract the brain from the user's preferred logo and find its average orange color
    original_logo_path = "/Users/narlonsilva/Desktop/silvalab/silvalab_logo_solid_1772999035689.png"
    orig_img = Image.open(original_logo_path).convert("RGBA")
    
    data = orig_img.getdata()
    newData = []
    
    min_x, min_y = orig_img.width, orig_img.height
    max_x, max_y = 0, 0
    
    r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    
    for y in range(orig_img.height):
        for x in range(orig_img.width):
            r, g, b, a = orig_img.getpixel((x, y))
            if a > 50 and r > 150 and b < 150: # Likely the peach/orange brain
                r_sum += r
                g_sum += g
                b_sum += b
                count += 1
                newData.append((*purple_rgb, a)) # Tint brain to purple, keep original alpha for anti-aliasing
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
            else:
                newData.append((255, 255, 255, 0))
                
    if count > 0:
        orange_color = (r_sum // count, g_sum // count, b_sum // count, 255)
    else:
        orange_color = (244, 123, 32, 255) # Autumnal orange fallback
        print("Warning: Could not isolate exact orange color. Using fallback.")
                
    extracted_brain = Image.new("RGBA", orig_img.size)
    extracted_brain.putdata(newData)
    
    if max_x >= min_x and max_y >= min_y:
        brain_img = extracted_brain.crop((min_x, min_y, max_x, max_y))
    else:
        print("Could not isolate brain bounds.")
        return

    # Target height for brain image exactly matches the lowercase 'a' + 20%
    target_brain_height = int(a_height * 1.20)
    aspect_ratio = brain_img.width / brain_img.height
    target_brain_width = int(target_brain_height * aspect_ratio)
    
    brain_img = brain_img.resize((target_brain_width, target_brain_height), Image.Resampling.LANCZOS)
    
    # 6. Calculate layout positions
    spacing = 15 # pixels between text and brain
    
    def get_word_width(word):
        w = 0
        for char in word:
            w += draw.textlength(char, font=font) + tracking
        return w
        
    silva_w = get_word_width(text_silva)
    l_w = get_word_width(text_l)
    
    total_width = silva_w + l_w + spacing + target_brain_width + spacing + draw.textlength(text_b, font=font)
    
    start_x = (width - total_width) // 2
    
    bbox_silva = draw.textbbox((0, 0), text_silva, font=font)
    t1_height = bbox_silva[3] - bbox_silva[1]
    
    # Vertically center text
    text_y = (height - t1_height) // 2 - bbox_silva[1] 
    
    # Vertically align brain to bottom of 'a'
    brain_y = text_y + bbox_a[1] - (target_brain_height - a_height) // 2

    # 7. Draw everything
    curr_x = start_x
    
    # Draw 'silva' in purple
    for char in text_silva:
        draw.text((curr_x, text_y), char, fill=purple_color, font=font)
        curr_x += draw.textlength(char, font=font) + tracking
        
    # Draw 'l' in orange
    draw.text((curr_x, text_y), text_l, fill=orange_color, font=font)
    curr_x += draw.textlength(text_l, font=font) + tracking
        
    # Paste purple brain
    brain_x = curr_x - tracking + spacing # Avoid double-tracking space
    img.paste(brain_img, (int(brain_x), int(brain_y)), brain_img)
    
    # Draw 'b' in orange
    b_x = brain_x + target_brain_width + spacing
    draw.text((b_x, text_y), text_b, fill=orange_color, font=font)
    
    # 8. Crop tightly
    bbox = img.getbbox()
    if bbox:
        pad = 60
        crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), 
                    min(width, bbox[2]+pad), min(height, bbox[3]+pad))
        img = img.crop(crop_box)
        
    output_path = "/Users/narlonsilva/Desktop/silvalab/logo.png"
    img.save(output_path, "PNG")
    print(f"Successfully generated precision logo at {output_path}")

if __name__ == "__main__":
    create_logo()
