from PIL import Image
import os


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()


def get_user_role(user):
    if is_admin(user):
        return "Admin"
    elif is_organizer(user):
        return "Organizer"
    elif is_participant(user):
        return "Participant"
    else:
        return "User"


def optimize_image_for_web(image_field, max_width=1920, max_height=1080, quality=85):

    if not image_field or not hasattr(image_field, "path"):
        return False

    try:
        image_path = image_field.path

        with Image.open(image_path) as img:

            original_width, original_height = img.size

            if original_width > max_width or original_height > max_height:

                width_ratio = max_width / original_width
                height_ratio = max_height / original_height
                scale_factor = min(width_ratio, height_ratio)

                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)

                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(
                    img, mask=img.split()[-1] if img.mode == "RGBA" else None
                )
                img = background

            base_name = os.path.splitext(image_path)[0]
            webp_path = f"{base_name}.webp"

            img.save(webp_path, "WebP", quality=quality, optimize=True)

            if not image_path.lower().endswith(".webp") and os.path.exists(image_path):
                os.remove(image_path)

            old_image_name = os.path.basename(image_path)
            new_image_name = os.path.basename(webp_path)
            image_field.name = image_field.name.replace(old_image_name, new_image_name)

            return True

    except Exception as e:
        return False
