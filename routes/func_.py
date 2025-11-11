import os
from PIL import Image, ImageDraw, ImageFont
from app import db
from sqlalchemy import text


# function for select product by id
def get_product_by_id(product_id: int) -> dict:
    sql = text("""
        SELECT p.*, c.name as category_name, c.image as category_image
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = :product_id
    """)
    result = db.session.execute(sql, {"product_id": product_id}).fetchone()
    if result:
        return dict(result._mapping)
    return {"error": "product not found"}


# function for select user by id
def get_user_by_id(user_id: int) -> dict:
    sql = text("""
                    SELECT * FROM users 
                    WHERE id = :user_id
                    """)
    result = db.session.execute(sql, {
        'user_id': user_id
    }).fetchone()
    if result:
        return dict(result._mapping)
    return {"error": "user not found"}


# function for select category by id
def get_category_by_id(category_id: int) -> dict:
    sql = text("""
                    SELECT * FROM categories
                    WHERE id = :category_id
                    """)
    result = db.session.execute(sql, {
        'category_id': category_id
    }).fetchone()
    if result:
        return dict(result._mapping)
    return {"error": "category not found"}


# function validation image type for upload photo profile for user
def validate_image_type(image_file):
    allowed = {'png', 'jpg', 'jpeg'}
    ext = os.path.splitext(image_file.filename)[1].lower().replace('.', '')
    if ext not in allowed:
        return {"error": "Only PNG, JPG, JPEG files are allowed"}
    return None


# function validation image size for upload photo profile for user
def validate_image_size(image_file, max_size_mb=2):
    image_file.seek(0, os.SEEK_END)
    size = image_file.tell()
    image_file.seek(0)
    if size > max_size_mb * 1024 * 1024:
        return {"error": f"File size exceeds {max_size_mb}MB"}
    return None


# function validation add watermark image for upload photo profile for user
def watermark_image(image_path, watermark_text="© MENG-LYHOUR"):
    """
    Adds a visible watermark to the bottom-right corner of an image.
    Automatically scales font size based on image dimensions.
    """

    with Image.open(image_path).convert("RGBA") as img:
        watermark_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark_layer)

        font_size = max(20, int(min(img.size) / 15))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = img.size[0] - text_width - 30
        y = img.size[1] - text_height - 30
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 200))
        watermarked = Image.alpha_composite(img, watermark_layer).convert("RGB")
        watermarked.save(image_path, "JPEG")
