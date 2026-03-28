#!/usr/bin/env python3
"""
Generate service cover images for portfolio website using Pillow.
Creates 13 images total: 5 for Web Dev, 4 for Chatbot, 4 for Mobile Dev.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Configuration
OUTPUT_DIR = "/sessions/relaxed-practical-darwin/mnt/profile/images"
PHOTO_PATH = os.path.join(OUTPUT_DIR, "cahyo.jpg")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# Image dimensions
WIDTH, HEIGHT = 960, 540

# Colors - Web Development (Indigo)
WEB_BG = "#eef2ff"
WEB_ACCENT = "#4f46e5"
WEB_SECONDARY = "#818cf8"

# Colors - Chatbot Development (Green)
CHAT_BG = "#f0fdf4"
CHAT_ACCENT = "#22c55e"
CHAT_SECONDARY = "#86efac"

# Colors - Mobile Development (Amber)
MOB_BG = "#fef3c7"
MOB_ACCENT = "#f59e0b"
MOB_SECONDARY = "#fcd34d"

# Text color
TEXT_DARK = "#1f2937"
TEXT_LIGHT = "#ffffff"

def get_fonts():
    """Load fonts from DejaVu directory."""
    try:
        title_font = ImageFont.truetype(
            os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 36
        )
        subtitle_font = ImageFont.truetype(
            os.path.join(FONT_DIR, "DejaVuSans.ttf"), 16
        )
        label_font = ImageFont.truetype(
            os.path.join(FONT_DIR, "DejaVuSans.ttf"), 14
        )
        small_font = ImageFont.truetype(
            os.path.join(FONT_DIR, "DejaVuSans.ttf"), 12
        )
        return title_font, subtitle_font, label_font, small_font
    except Exception as e:
        print(f"Error loading fonts: {e}")
        raise

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

def create_gradient_background(img, color1, color2):
    """Create a soft vertical gradient background."""
    pixels = img.load()
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)

        for x in range(WIDTH):
            pixels[x, y] = (r, g, b)

def add_decorative_dots(draw, color, step=36, radius=3):
    """Add small decorative dot pattern across the image."""
    dot_color = hex_to_rgb(color)
    # Adjust alpha slightly
    for x in range(0, WIDTH + step, step):
        for y in range(0, HEIGHT + step, step):
            draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=dot_color
            )

def load_and_crop_photo(size=200):
    """Load photo and create circular crop with alpha mask."""
    try:
        img = Image.open(PHOTO_PATH).convert("RGBA")
        # Resize to a square
        img.thumbnail((size, size), Image.Resampling.LANCZOS)

        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, size - 1, size - 1], fill=255)

        # Apply circular crop
        img.putalpha(mask)
        return img
    except Exception as e:
        print(f"Error loading photo: {e}")
        return None

def rounded_rect(draw, xy, radius=20, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    # Draw the main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=None)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=None)

    # Draw corners
    for x, y, start, end in [
        (x1 + radius, y1 + radius, 180, 270),
        (x2 - radius, y1 + radius, 270, 360),
        (x2 - radius, y2 - radius, 0, 90),
        (x1 + radius, y2 - radius, 90, 180),
    ]:
        draw.pieslice([x - radius, y - radius, x + radius, y + radius], start, end, fill=fill)

    # Draw outline if specified
    if outline:
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], outline=outline, width=width)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], outline=outline, width=width)
        for x, y, start, end in [
            (x1 + radius, y1 + radius, 180, 270),
            (x2 - radius, y1 + radius, 270, 360),
            (x2 - radius, y2 - radius, 0, 90),
            (x1 + radius, y2 - radius, 90, 180),
        ]:
            draw.pieslice([x - radius, y - radius, x + radius, y + radius], start, end, outline=outline)

def draw_centered_text(draw, text, pos, font, fill, anchor="mm"):
    """Draw text centered at position."""
    draw.text(pos, text, font=font, fill=fill, anchor=anchor)

# Load fonts once
title_font, subtitle_font, label_font, small_font = get_fonts()

print("Generating service cover images...")

# ============================================================================
# WEB DEVELOPMENT IMAGES
# ============================================================================

def create_web_1():
    """service-web-1.png - Overview with photo"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(WEB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    # Light gradient overlay
    create_gradient_background(img, WEB_BG, "#f3f4ff")

    # Add decorative dots
    add_decorative_dots(draw, WEB_SECONDARY, step=40, radius=2)

    # Load photo
    photo = load_and_crop_photo(180)
    if photo:
        img.paste(photo, (80, 180), photo)

    # Title
    draw_centered_text(draw, "Web Development", (480, 120), title_font, TEXT_DARK)

    # Subtitle
    draw_centered_text(draw, "Websites & Web Apps", (480, 170), subtitle_font, TEXT_DARK)

    # Right side - browser mockup illustration
    browser_x, browser_y = 650, 200
    browser_w, browser_h = 260, 200

    # Browser frame
    rounded_rect(draw, (browser_x, browser_y, browser_x + browser_w, browser_y + browser_h),
                 radius=12, fill=TEXT_LIGHT, outline=hex_to_rgb(WEB_SECONDARY))

    # Browser header
    draw.rectangle((browser_x, browser_y, browser_x + browser_w, browser_y + 30),
                   fill=hex_to_rgb(WEB_SECONDARY))

    # Browser dots
    for i in range(3):
        draw.ellipse((browser_x + 10 + i * 12, browser_y + 8, browser_x + 18 + i * 12, browser_y + 16),
                     fill=hex_to_rgb(WEB_ACCENT))

    # Content area
    draw.rectangle((browser_x + 15, browser_y + 45, browser_x + browser_w - 15, browser_y + 80),
                   fill=hex_to_rgb(WEB_ACCENT))
    draw.rectangle((browser_x + 15, browser_y + 95, browser_x + browser_w - 15, browser_y + 110),
                   fill=hex_to_rgb(WEB_SECONDARY))
    draw.rectangle((browser_x + 15, browser_y + 120, browser_x + browser_w - 15, browser_y + 135),
                   fill=hex_to_rgb(WEB_SECONDARY))
    draw.rectangle((browser_x + 15, browser_y + 150, browser_x + browser_w - 15, browser_y + 165),
                   fill=hex_to_rgb(WEB_SECONDARY))

    img.save(os.path.join(OUTPUT_DIR, "service-web-1.png"))
    print("✓ service-web-1.png")

def create_web_2():
    """service-web-2.png - Frontend Tech Stack"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(WEB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, WEB_BG, "#f3f4ff")
    add_decorative_dots(draw, WEB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Frontend Stack", (480, 50), title_font, TEXT_DARK)

    # Tech stack data: (name, color_hex)
    techs = [
        ("React", "#61dafb"),
        ("Next.js", "#000000"),
        ("Vue.js", "#4fc08d"),
        ("Angular", "#dd0031"),
        ("TypeScript", "#3178c6"),
        ("Tailwind CSS", "#06b6d4"),
    ]

    # Grid layout: 3x2
    radius = 24
    positions = [
        (200, 150),
        (480, 150),
        (760, 150),
        (200, 320),
        (480, 320),
        (760, 320),
    ]

    for i, (tech, color) in enumerate(techs):
        x, y = positions[i]
        color_rgb = hex_to_rgb(color)

        # Circle
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color_rgb)

        # Label below
        draw_centered_text(draw, tech, (x, y + 50), label_font, TEXT_DARK)

    img.save(os.path.join(OUTPUT_DIR, "service-web-2.png"))
    print("✓ service-web-2.png")

def create_web_3():
    """service-web-3.png - Backend Tech Stack"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(WEB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, WEB_BG, "#f3f4ff")
    add_decorative_dots(draw, WEB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Backend Stack", (480, 50), title_font, TEXT_DARK)

    # Tech stack data
    techs = [
        ("Node.js", "#68a063"),
        ("Laravel", "#ff2d20"),
        ("Spring Boot", "#6db33f"),
        ("PostgreSQL", "#336791"),
        ("MongoDB", "#47a248"),
        ("REST API", "#818cf8"),
    ]

    radius = 24
    positions = [
        (200, 150),
        (480, 150),
        (760, 150),
        (200, 320),
        (480, 320),
        (760, 320),
    ]

    for i, (tech, color) in enumerate(techs):
        x, y = positions[i]
        color_rgb = hex_to_rgb(color)

        # Circle
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color_rgb)

        # Label below
        draw_centered_text(draw, tech, (x, y + 50), label_font, TEXT_DARK)

    img.save(os.path.join(OUTPUT_DIR, "service-web-3.png"))
    print("✓ service-web-3.png")

def create_web_4():
    """service-web-4.png - Benefits"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(WEB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, WEB_BG, "#f3f4ff")
    add_decorative_dots(draw, WEB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Why Choose Me", (480, 50), title_font, TEXT_DARK)

    benefits = [
        ("⚡ Fast Performance", "Optimized for speed"),
        ("📱 Fully Responsive", "Works on all devices"),
        ("🔍 SEO Optimized", "Search engine ready"),
        ("📈 Scalable Architecture", "Grows with you"),
    ]

    card_w, card_h = 200, 110
    positions = [
        (80, 150),
        (360, 150),
        (640, 150),
        (360, 300),
    ]

    for i, (title, desc) in enumerate(benefits):
        x, y = positions[i]

        # Card background
        rounded_rect(draw, (x, y, x + card_w, y + card_h),
                     radius=12, fill=hex_to_rgb(WEB_SECONDARY))

        # Text
        draw_centered_text(draw, title, (x + card_w // 2, y + 30), label_font, TEXT_LIGHT)
        draw_centered_text(draw, desc, (x + card_w // 2, y + 65), small_font, TEXT_LIGHT)

    img.save(os.path.join(OUTPUT_DIR, "service-web-4.png"))
    print("✓ service-web-4.png")

def create_web_5():
    """service-web-5.png - AI Integration"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(WEB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, WEB_BG, "#c7d2fe")
    add_decorative_dots(draw, WEB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "AI-Powered Features", (480, 50), title_font, TEXT_DARK)

    features = [
        "🤖 Smart Search",
        "💡 AI Recommendations",
        "📝 Content Generation",
        "🔮 Predictive Analytics",
    ]

    card_w, card_h = 200, 100
    positions = [
        (80, 160),
        (360, 160),
        (640, 160),
        (360, 300),
    ]

    for i, feature in enumerate(features):
        x, y = positions[i]

        # Card with rounded corners
        rounded_rect(draw, (x, y, x + card_w, y + card_h),
                     radius=12, fill=hex_to_rgb(WEB_ACCENT))

        # Feature text
        draw_centered_text(draw, feature, (x + card_w // 2, y + card_h // 2),
                          label_font, TEXT_LIGHT)

    img.save(os.path.join(OUTPUT_DIR, "service-web-5.png"))
    print("✓ service-web-5.png")

# ============================================================================
# CHATBOT DEVELOPMENT IMAGES
# ============================================================================

def create_chat_1():
    """service-chat-1.png - Overview with photo"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(CHAT_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, CHAT_BG, "#dcfce7")
    add_decorative_dots(draw, CHAT_SECONDARY, step=40, radius=2)

    # Load photo
    photo = load_and_crop_photo(180)
    if photo:
        img.paste(photo, (80, 180), photo)

    # Title
    draw_centered_text(draw, "Chatbot Development", (480, 120), title_font, TEXT_DARK)

    # Subtitle
    draw_centered_text(draw, "AI-Powered Bots", (480, 170), subtitle_font, TEXT_DARK)

    # Right side - chat bubble illustration
    chat_x = 650

    # Chat bubble 1 (incoming)
    rounded_rect(draw, (chat_x, 200, chat_x + 200, 240),
                 radius=12, fill=hex_to_rgb(CHAT_SECONDARY))
    draw_centered_text(draw, "Hello! How can I help?", (chat_x + 100, 220), small_font, TEXT_LIGHT)

    # Chat bubble 2 (outgoing)
    rounded_rect(draw, (chat_x + 30, 260, chat_x + 230, 300),
                 radius=12, fill=hex_to_rgb(CHAT_ACCENT))
    draw_centered_text(draw, "I need support", (chat_x + 130, 280), small_font, TEXT_LIGHT)

    # Chat bubble 3 (incoming)
    rounded_rect(draw, (chat_x, 320, chat_x + 200, 360),
                 radius=12, fill=hex_to_rgb(CHAT_SECONDARY))
    draw_centered_text(draw, "Sure, I'm here to help!", (chat_x + 100, 340), small_font, TEXT_LIGHT)

    img.save(os.path.join(OUTPUT_DIR, "service-chat-1.png"))
    print("✓ service-chat-1.png")

def create_chat_2():
    """service-chat-2.png - Platforms"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(CHAT_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, CHAT_BG, "#dcfce7")
    add_decorative_dots(draw, CHAT_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Deploy Anywhere", (480, 50), title_font, TEXT_DARK)

    platforms = [
        ("WhatsApp", "#25D366"),
        ("Telegram", "#26A5E4"),
        ("Web Chat", "#4f46e5"),
        ("Slack", "#4A154B"),
        ("Discord", "#5865F2"),
    ]

    radius = 24
    positions = [
        (150, 200),
        (350, 200),
        (550, 200),
        (750, 200),
        (450, 340),
    ]

    for i, (platform, color) in enumerate(platforms):
        x, y = positions[i]
        color_rgb = hex_to_rgb(color)

        # Circle
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color_rgb)

        # Label below
        draw_centered_text(draw, platform, (x, y + 50), label_font, TEXT_DARK)

    img.save(os.path.join(OUTPUT_DIR, "service-chat-2.png"))
    print("✓ service-chat-2.png")

def create_chat_3():
    """service-chat-3.png - AI Tech Stack"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(CHAT_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, CHAT_BG, "#dcfce7")
    add_decorative_dots(draw, CHAT_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "AI & NLP Stack", (480, 50), title_font, TEXT_DARK)

    techs = [
        ("OpenAI", "#412991"),
        ("LangChain", "#1C3C3C"),
        ("RAG", "#22c55e"),
        ("Python", "#3776ab"),
        ("Firebase", "#ffcb2b"),
        ("Redis", "#DC382D"),
    ]

    radius = 24
    positions = [
        (200, 150),
        (480, 150),
        (760, 150),
        (200, 320),
        (480, 320),
        (760, 320),
    ]

    for i, (tech, color) in enumerate(techs):
        x, y = positions[i]
        color_rgb = hex_to_rgb(color)

        # Circle
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color_rgb)

        # Label below
        draw_centered_text(draw, tech, (x, y + 50), label_font, TEXT_DARK)

    img.save(os.path.join(OUTPUT_DIR, "service-chat-3.png"))
    print("✓ service-chat-3.png")

def create_chat_4():
    """service-chat-4.png - Benefits"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(CHAT_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, CHAT_BG, "#dcfce7")
    add_decorative_dots(draw, CHAT_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Bot Benefits", (480, 50), title_font, TEXT_DARK)

    benefits = [
        "🕐 24/7 Customer Support",
        "📊 Lead Generation",
        "💰 Reduce Support Costs",
        "🌍 Multi-Language",
    ]

    card_w, card_h = 200, 100
    positions = [
        (80, 160),
        (360, 160),
        (640, 160),
        (360, 300),
    ]

    for i, benefit in enumerate(benefits):
        x, y = positions[i]

        # Card with rounded corners
        rounded_rect(draw, (x, y, x + card_w, y + card_h),
                     radius=12, fill=hex_to_rgb(CHAT_ACCENT))

        # Benefit text
        draw_centered_text(draw, benefit, (x + card_w // 2, y + card_h // 2),
                          label_font, TEXT_LIGHT)

    img.save(os.path.join(OUTPUT_DIR, "service-chat-4.png"))
    print("✓ service-chat-4.png")

# ============================================================================
# MOBILE DEVELOPMENT IMAGES
# ============================================================================

def create_mob_1():
    """service-mob-1.png - Overview with photo"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(MOB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, MOB_BG, "#fef08a")
    add_decorative_dots(draw, MOB_SECONDARY, step=40, radius=2)

    # Load photo
    photo = load_and_crop_photo(180)
    if photo:
        img.paste(photo, (80, 180), photo)

    # Title
    draw_centered_text(draw, "Mobile Development", (480, 120), title_font, TEXT_DARK)

    # Subtitle
    draw_centered_text(draw, "iOS & Android Apps", (480, 170), subtitle_font, TEXT_DARK)

    # Right side - phone mockup
    phone_x, phone_y = 680, 160
    phone_w, phone_h = 120, 200

    # Phone frame
    rounded_rect(draw, (phone_x, phone_y, phone_x + phone_w, phone_y + phone_h),
                 radius=16, fill=TEXT_DARK, outline=hex_to_rgb(MOB_ACCENT))

    # Phone screen
    rounded_rect(draw, (phone_x + 8, phone_y + 15, phone_x + phone_w - 8, phone_y + phone_h - 15),
                 radius=12, fill=hex_to_rgb(MOB_ACCENT))

    # Notch
    draw.rectangle((phone_x + 40, phone_y + 5, phone_x + 80, phone_y + 12), fill=TEXT_DARK)

    # Screen content
    draw.rectangle((phone_x + 12, phone_y + 30, phone_x + phone_w - 12, phone_y + 55),
                   fill=hex_to_rgb(MOB_SECONDARY))
    draw.rectangle((phone_x + 12, phone_y + 70, phone_x + phone_w - 12, phone_y + 85),
                   fill=hex_to_rgb(MOB_SECONDARY))

    img.save(os.path.join(OUTPUT_DIR, "service-mob-1.png"))
    print("✓ service-mob-1.png")

def create_mob_2():
    """service-mob-2.png - Mobile Tech Stack"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(MOB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, MOB_BG, "#fef08a")
    add_decorative_dots(draw, MOB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Mobile Stack", (480, 50), title_font, TEXT_DARK)

    techs = [
        ("React Native", "#61dafb"),
        ("Flutter", "#02569B"),
        ("Swift", "#F05138"),
        ("Kotlin", "#7F52FF"),
        ("Firebase", "#ffcb2b"),
        ("Expo", "#000020"),
    ]

    radius = 24
    positions = [
        (200, 150),
        (480, 150),
        (760, 150),
        (200, 320),
        (480, 320),
        (760, 320),
    ]

    for i, (tech, color) in enumerate(techs):
        x, y = positions[i]
        color_rgb = hex_to_rgb(color)

        # Circle
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color_rgb)

        # Label below
        draw_centered_text(draw, tech, (x, y + 50), label_font, TEXT_DARK)

    img.save(os.path.join(OUTPUT_DIR, "service-mob-2.png"))
    print("✓ service-mob-2.png")

def create_mob_3():
    """service-mob-3.png - Benefits"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(MOB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, MOB_BG, "#fef08a")
    add_decorative_dots(draw, MOB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "App Benefits", (480, 50), title_font, TEXT_DARK)

    benefits = [
        "📲 Cross-Platform",
        "🔔 Push Notifications",
        "📴 Offline-First",
        "⚡ Native Performance",
    ]

    card_w, card_h = 200, 100
    positions = [
        (80, 160),
        (360, 160),
        (640, 160),
        (360, 300),
    ]

    for i, benefit in enumerate(benefits):
        x, y = positions[i]

        # Card with rounded corners
        rounded_rect(draw, (x, y, x + card_w, y + card_h),
                     radius=12, fill=hex_to_rgb(MOB_ACCENT))

        # Benefit text
        draw_centered_text(draw, benefit, (x + card_w // 2, y + card_h // 2),
                          label_font, TEXT_LIGHT)

    img.save(os.path.join(OUTPUT_DIR, "service-mob-3.png"))
    print("✓ service-mob-3.png")

def create_mob_4():
    """service-mob-4.png - Advanced Features"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(MOB_BG))
    draw = ImageDraw.Draw(img, "RGBA")

    create_gradient_background(img, MOB_BG, "#fed7aa")
    add_decorative_dots(draw, MOB_SECONDARY, step=40, radius=2)

    # Title
    draw_centered_text(draw, "Advanced Features", (480, 50), title_font, TEXT_DARK)

    features = [
        "🤖 AI Integration",
        "🔄 Real-time Sync",
        "💳 Payment Integration",
        "📊 Analytics & Crash Reporting",
    ]

    card_w, card_h = 200, 100
    positions = [
        (80, 160),
        (360, 160),
        (640, 160),
        (360, 300),
    ]

    for i, feature in enumerate(features):
        x, y = positions[i]

        # Card with rounded corners
        rounded_rect(draw, (x, y, x + card_w, y + card_h),
                     radius=12, fill=hex_to_rgb(MOB_ACCENT))

        # Feature text (smaller font for longer text)
        lines = feature.split()
        if len(lines) > 2:
            # Split into two lines
            draw_centered_text(draw, " ".join(lines[:2]), (x + card_w // 2, y + card_h // 2 - 15),
                              small_font, TEXT_LIGHT)
            draw_centered_text(draw, " ".join(lines[2:]), (x + card_w // 2, y + card_h // 2 + 10),
                              small_font, TEXT_LIGHT)
        else:
            draw_centered_text(draw, feature, (x + card_w // 2, y + card_h // 2),
                              label_font, TEXT_LIGHT)

    img.save(os.path.join(OUTPUT_DIR, "service-mob-4.png"))
    print("✓ service-mob-4.png")

# Generate all images
if __name__ == "__main__":
    try:
        # Web Development
        create_web_1()
        create_web_2()
        create_web_3()
        create_web_4()
        create_web_5()

        # Chatbot Development
        create_chat_1()
        create_chat_2()
        create_chat_3()
        create_chat_4()

        # Mobile Development
        create_mob_1()
        create_mob_2()
        create_mob_3()
        create_mob_4()

        print("\n✓ All 13 service images generated successfully!")

    except Exception as e:
        print(f"Error generating images: {e}")
        import traceback
        traceback.print_exc()
