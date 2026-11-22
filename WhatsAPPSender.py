import pywhatkit as pwk
import re

def sendInfoWA(mobilenumber,imagepath, leaf_type, description, farmer_name):
    digits = re.sub(r"\D", "", mobilenumber)
    if len(digits) == 10:
        digits = "91" + digits
    elif len(digits) == 12 and digits.startswith("91"):
        pass
    elif not 11 <= len(digits) <= 15:
        raise ValueError("Enter a valid phone number with country code, or a 10-digit Indian number.")

    phone = "+" + digits
    crop_name = leaf_type.split("_")[0]
    message = (
        f"Dear Farmer {farmer_name},\n"
        f"The detected crop is {crop_name}; the predicted class is {leaf_type}.\n\n"
        f"Description:\n{description}\n\n"
        "The captured image is attached for your reference.\n"
        "Regards,\nAutomatic Crop Disease Detection System"
    )

    try:
        # Leave WhatsApp Web open so the user can see the send result.
        pwk.sendwhats_image(phone, imagepath, message, wait_time=15, tab_close=False)
    except Exception as exc:
        raise RuntimeError(
            f"WhatsApp send failed ({exc}). Keep WhatsApp Web logged in on this laptop, "
            "make sure the number has a WhatsApp account, and try again."
        ) from exc
