# Asset Annotation Management System

This Django app lets staff create asset annotations for physical objects, attach optional audio and image files, and generate a QR label for each asset. When the QR code is scanned, the asset record can be used by HoloLens or any external system to display the instruction data.

## What It Does

- Create and manage asset annotations from a simple staff dashboard.
- Generate a unique QR code for every annotation using the annotation UUID.
- Download a printable PDF label for each QR code.
- Upload optional audio and image files for each annotation.
- Expose a JSON API for external systems.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

3. Create an admin user if needed:

   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Staff Usage

Open the dashboard in your browser and create a new annotation.

### Add an annotation

- Enter a title, such as `Main Water Valve`.
- Enter the instruction text that HoloLens should read or display.
- Optionally upload an audio file.
- Optionally upload an image file.
- Save the annotation.

### View the QR code

- Open the annotation detail page.
- The page shows the QR code linked to that annotation's unique ID.
- Use the **Download printable QR** button to download a PDF label.
- Print the PDF and attach the label to the book, asset, or object.

## URLs

- Dashboard: `/`
- Create annotation: `/create/`
- Detail page: `/<uuid>/`
- PDF QR download: `/<uuid>/qr/`
- JSON API: `/api/annotations/<uuid>/`

## API Response

A request to the API returns JSON like this:

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Main Water Valve",
  "instruction": "Turn counter-clockwise to shut off.",
  "created_at": "2026-07-20T23:45:00Z",
  "audio_file": "https://example.com/media/annotation-audio/audio.mp3",
  "image_file": "https://example.com/media/annotation-images/reference.jpg"
}
```

If a file was not uploaded, its value will be `null`.

## File Storage

Uploaded audio and images are stored under the Django media folder.

- Audio uploads: `media/annotation-audio/`
- Image uploads: `media/annotation-images/`

## Notes

- The QR code payload is only the annotation UUID.
- The printable label is generated as a PDF for easy printing and sticking onto physical assets.
- The app uses SQLite by default.
