from django.core.files.base import ContentFile
from django.utils.text import slugify
from decimal import Decimal
from io import BytesIO
from PIL import Image
import requests, os, re, json


def generate_unique_slug(instance, value, slug_field="slug"):

    base_slug = slugify(value)

    slug = base_slug

    ModelClass = instance.__class__

    counter = 1

    while ModelClass.objects.filter(
        **{slug_field: slug}
    ).exclude(
        id=instance.id
    ).exists():

        slug = f"{base_slug}-{counter}"

        counter += 1

    return slug


def generate_order(instance, order_field="order"):

    ModelClass = instance.__class__

    last_item = ModelClass.objects.order_by(
        f"-{order_field}"
    ).first()

    if last_item:

        last_order = getattr(
            last_item,
            order_field
        )

        if last_order is not None:
            return last_order + 1

    return 0

def compress_image(uploaded_image, max_size_kb=50):

    img = Image.open(uploaded_image)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    output = BytesIO()

    quality = 95

    while quality >= 10:

        output.seek(0)
        output.truncate(0)

        img.save(
            output,
            format="WEBP",
            quality=quality,
            optimize=True,
            method=6
        )

        size_kb = output.tell() / 1024

        if size_kb <= max_size_kb:
            break

        quality -= 5

    output.seek(0)

    file_name = (
        os.path.splitext(uploaded_image.name)[0]
        + ".webp"
    )

    return ContentFile(
        output.read(),
        name=file_name
    )



def generate_sku(instance, prefix="RA", start=1000, sku_field="sku"):
    ModelClass = instance.__class__

    last_item = ModelClass.objects.exclude(
        **{sku_field: None}
    ).exclude(
        **{sku_field: ""}
    ).order_by("-id").first()

    if last_item:
        last_sku = getattr(last_item, sku_field)

        try:
            last_number = int(str(last_sku).split("-")[-1])
            new_number = last_number + 1
        except:
            new_number = start
    else:
        new_number = start

    sku = f"{prefix}-{new_number}"

    while ModelClass.objects.filter(
        **{sku_field: sku}
    ).exclude(id=instance.id).exists():
        new_number += 1
        sku = f"{prefix}-{new_number}"

    return sku



def update_gold_prices():

    from .models import Category

    url = "https://www.goldr.org/price.js?gttm"

    response = requests.get(url, timeout=20)

    js_text = response.text

    gold_match = re.search(
        r'const GoldrPriceTable_goldData = (\[.*?\]);',
        js_text,
        re.DOTALL
    )

    if not gold_match:
        return "Gold data not found"

    gold_data = json.loads(
        gold_match.group(1)
    )

    gold_price_map = {

        1: gold_data[0]["bg_raw"],
        2: gold_data[1]["bg_raw"],
        3: gold_data[2]["bg_raw"],
        4: gold_data[3]["bg_raw"],
    }

    for category_name, price in gold_price_map.items():

        Category.objects.filter(
            menue__name=1,
            name=category_name
        ).update(
            price_per_gram=Decimal(str(price))
        )

    return "Gold prices updated successfully"



def update_silver_prices():

    from .models import Category

    url = "https://www.goldr.org/price.js?gttm"

    response = requests.get(url, timeout=20)

    js_text = response.text

    silver_match = re.search(
        r'const GoldrPriceTable_silverData = (\[.*?\]);',
        js_text,
        re.DOTALL
    )

    if not silver_match:
        return "Silver data not found"

    silver_data = json.loads(
        silver_match.group(1)
    )

    silver_price_map = {

        1: silver_data[0]["bg_raw"],
        2: silver_data[1]["bg_raw"],
        3: silver_data[2]["bg_raw"],
        4: silver_data[3]["bg_raw"],
    }

    for category_name, price in silver_price_map.items():

        Category.objects.filter(
            menue__name=3,
            name=category_name
        ).update(
            price_per_gram=Decimal(str(price))
        )

    return "Silver prices updated successfully"



from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_otp_email(email, otp):

    subject = "Verify Your Email | Rajanigandha Jewellers"

    from_email = settings.DEFAULT_FROM_EMAIL

    to = [email]

    text_content = f"""
    Your OTP is {otp}

    This OTP will expire in 5 minutes.

    Rajanigandha Jewellers
    """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>

    <body style="
        margin:0;
        padding:0;
        background:#f5f5f5;
        font-family:Arial,sans-serif;
    ">

        <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 15px;">
            <tr>
                <td align="center">

                    <table width="100%" cellpadding="0" cellspacing="0"
                        style="
                            max-width:600px;
                            background:#ffffff;
                            border-radius:20px;
                            overflow:hidden;
                            box-shadow:0 10px 40px rgba(0,0,0,0.08);
                        ">

                        <!-- TOP BAR -->
                        <tr>
                            <td style="
                                background:linear-gradient(135deg,#c59b43,#9d7627);
                                padding:22px;
                                text-align:center;
                            ">

                                <h1 style="
                                    margin:0;
                                    color:#ffffff;
                                    font-size:30px;
                                    font-weight:700;
                                    letter-spacing:1px;
                                ">
                                    Rajanigandha Jewellers
                                </h1>

                            </td>
                        </tr>

                        <!-- CONTENT -->
                        <tr>
                            <td style="padding:45px 35px; text-align:center;">

                                <div style="
                                    width:85px;
                                    height:85px;
                                    margin:0 auto 25px;
                                    border-radius:50%;
                                    background:rgba(197,155,67,0.12);
                                    line-height:85px;
                                    font-size:38px;
                                ">
                                    🔐
                                </div>

                                <h2 style="
                                    margin:0 0 12px;
                                    color:#111111;
                                    font-size:30px;
                                    font-weight:700;
                                ">
                                    Email Verification
                                </h2>

                                <p style="
                                    margin:0 auto 28px;
                                    max-width:420px;
                                    color:#666666;
                                    font-size:16px;
                                    line-height:1.7;
                                ">
                                    Use the verification code below to complete your signup process.
                                    This code is valid for only 5 minutes.
                                </p>

                                <!-- OTP BOX -->
                                <div style="
                                    background:#faf7ef;
                                    border:2px dashed #c59b43;
                                    border-radius:18px;
                                    padding:24px;
                                    margin:30px 0;
                                ">

                                    <div style="
                                        color:#9d7627;
                                        font-size:14px;
                                        font-weight:600;
                                        margin-bottom:10px;
                                        text-transform:uppercase;
                                        letter-spacing:2px;
                                    ">
                                        Your OTP Code
                                    </div>

                                    <div style="
                                        font-size:42px;
                                        font-weight:800;
                                        color:#111111;
                                        letter-spacing:12px;
                                    ">
                                        {otp}
                                    </div>

                                </div>

                                <p style="
                                    color:#888888;
                                    font-size:14px;
                                    line-height:1.7;
                                    margin-top:20px;
                                ">
                                    If you did not request this verification,
                                    you can safely ignore this email.
                                </p>

                            </td>
                        </tr>

                        <!-- FOOTER -->
                        <tr>
                            <td style="
                                padding:22px;
                                text-align:center;
                                background:#fafafa;
                                border-top:1px solid #eeeeee;
                            ">

                                <p style="
                                    margin:0;
                                    color:#777777;
                                    font-size:13px;
                                    line-height:1.8;
                                ">
                                    © 2026 Rajanigandha Jewellers <br>
                                    Luxury • Elegance • Trust
                                </p>

                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    email_message = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to
    )

    email_message.attach_alternative(html_content, "text/html")

    email_message.send()