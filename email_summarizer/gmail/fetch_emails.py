from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import base64
import re

# Clean extra spaces and newlines
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# Decode Base64 safely and clean it
def decode_and_clean(data):
    if data:
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        decoded = base64.urlsafe_b64decode(data).decode('utf-8')
        return clean_text(decoded)
    return ""

# Recursive function to extract plain text or HTML from nested parts
from bs4 import BeautifulSoup

def extract_text_from_parts(parts):
    for part in parts:
        mime_type = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data")

        # 🔁 If nested MIME (like multipart/alternative)
        if mime_type.startswith("multipart"):
            nested = part.get("parts", [])
            result = extract_text_from_parts(nested)
            if result:
                return result

        # ✅ Plain text first
        if mime_type == "text/plain" and data:
            return decode_and_clean(data)

        # ✅ Fallback to HTML, but extract text only
        if mime_type == "text/html" and data:
            html = decode_and_clean(data)
            soup = BeautifulSoup(html, 'html.parser')
            return clean_text(soup.get_text())

    return ""


# Main function to decode email body
def get_email_body(payload):
    if 'parts' in payload:
        return extract_text_from_parts(payload['parts'])
    else:
        data = payload['body'].get('data')
        return decode_and_clean(data) if data else "(No content found)"

# Fetch emails from Gmail
def fetch_emails(service, max_results=20):
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],  # Only Primary tab
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    emails = []
    print("Total messages returned:", len(messages))

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()

        payload = msg_data['payload']
        headers = payload.get('headers', [])

        subject = sender = date = ''
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                sender = header['value']
            elif header['name'] == 'Date':
                date = header['value']

        body = get_email_body(payload)

        # Check for attachments
        attachment_filenames = []
        if 'parts' in payload:
            for part in payload['parts']:
                filename = part.get("filename")
                if filename:
                    attachment_filenames.append(filename)

        # Append structured email object
        emails.append({
            'subject': subject,
            'sender': sender,
            'date': date,
            'snippet': body,
            'attachments': attachment_filenames
        })

    return emails
