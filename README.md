# Simple OCR REST API

A simple REST API for Optical Character Recognition (OCR) using Tesseract, supporting English and Ukrainian languages.

## Features

- Extract text from images using Tesseract OCR
- Support for English and Ukrainian languages
- Dockerized application
- RESTful API endpoints
- Health check endpoint
- Confidence scoring
- Error handling and validation

## API Endpoints

### POST /api/v1/read
Extract text from an uploaded image.

**Parameters:**
- `image` (file, required): Image file to process
- `language` (form field, optional): Language code - `eng`, `ukr`, or `eng+ukr` (default: `eng`)

**Response:**
```json
{
  "success": true,
  "text": "Extracted text from image",
  "language": "eng",
  "confidence": 95.5,
  "word_count": 4
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "OCR API is running"
}
```

## Quick Start

### Using Docker Compose (Recommended)

1. Clone or create the project files
2. Build and run:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:5001`

### Using Docker

1. Build the image:
```bash
docker build -t ocr-api .
```

2. Run the container:
```bash
docker run -p 5001:5001 ocr-api
```

## Usage Examples

### Using curl

**Extract English text:**
```bash
curl -X POST -F "image=@your_image.jpg" -F "language=eng" http://localhost:5001/api/v1/read
```

**Extract Ukrainian text:**
```bash
curl -X POST -F "image=@your_image.jpg" -F "language=ukr" http://localhost:5001/api/v1/read
```

**Extract both English and Ukrainian:**
```bash
curl -X POST -F "image=@your_image.jpg" -F "language=eng+ukr" http://localhost:5001/api/v1/read
```

### Using Python requests

```python
import requests

# Upload image for OCR
with open('image.jpg', 'rb') as f:
    files = {'image': f}
    data = {'language': 'eng'}
    response = requests.post('http://localhost:5001/api/v1/read', files=files, data=data)
    
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('language', 'eng');

fetch('http://localhost:5001/api/v1/read', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Docker repo

https://hub.docker.com/repository/docker/vitaliikobrin/simple-ocr-server/general

## Supported Image Formats

- JPEG/JPG
- PNG
- TIFF
- BMP
- GIF

## Configuration

The application uses the following environment variables:

- `PORT`: Server port (default: 5001)

## Error Responses

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input (no image, unsupported language, invalid image format)
- `413 Payload Too Large`: Image file too large
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Processing error

## Performance Notes

- The API uses Gunicorn with 2 workers for better performance
- OCR processing time depends on image size and complexity
- For production use, consider adding request rate limiting
- Memory usage scales with image size

## Development

### Local Development

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-ukr

# macOS
brew install tesseract tesseract-lang
```

3. Run the application:
```bash
python app.py
```

### Adding More Languages

To add support for additional languages:

1. Install the language pack in the Dockerfile:
```dockerfile
tesseract-ocr-[language-code]
```

2. Update the supported languages list in `app.py`

## Security Considerations

- The application runs as a non-root user in the container
- File uploads are validated for image format
- No permanent file storage (files processed in memory)
- Consider adding authentication for production use
