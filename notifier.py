import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO: fix pictures

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_ADDRESSES = os.getenv("TO_ADDRESSES")

def send_notification(new_listing: list):
    # Build email
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = ", ".join(TO_ADDRESSES)
    msg["Subject"] = f"NYC Housing Lottery - {len(new_listing)} new listing(s)"

    # Build body
    bullet = "\u2022" #unicode for bullet point
    body_html = f"""
    <html><body>
        <p>New NYC housing lottery listing(s) found:</p>
        <a href="https://a806-housingconnectapi.nyc.gov/id4/account/login?returnUrl=%2Fid4%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Did_token%2520token%26client_id%3Dpublicweb%26state%3Dul20cAdDQy1Zlfclwx1rYUxJicBPtzFoNppIbGqA;%252Fsome-state;p1%253D1;p2%253D2%26redirect_uri%3Dhttps%253A%252F%252Fhousingconnect.nyc.gov%252FPublicWeb%252F%26scope%3Dopenid%2520profile%2520email%2520usermanagementapi%2520publicapi%26nonce%3Dul20cAdDQy1Zlfclwx1rYUxJicBPtzFoNppIbGqA">Sign in to your login page to apply!</a>

        {''.join(f'''
        <div>
            <p>{bullet} <strong>{listing.get("lotteryName", "Unknown")}</strong></p>
            <img src="{listing.get('defaultPhotoStream')}" width="300">
            <p> <strong>Borough: {listing.get("borough", "N/A")}</strong> (Neighborhood: {listing.get("neighborhood")})</p>
        </div>
        '''for listing in new_listing)}
    </body></html>
    """
    msg.attach(MIMEText(body_html, "html"))

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, APP_PASSWORD)
        smtp.sendmail(GMAIL_ADDRESS, TO_ADDRESSES, msg.as_string())

if __name__ == "__main__":
    send_notification([
        {"lotteryName": "Test Apartment", "Borough": "Manhattan", "Neighborhood": "Greenwich Village"}
    ])
    print("Email Sent Successfully")