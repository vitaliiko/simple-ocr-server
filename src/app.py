from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "OCR API is running"})

@app.route('/ocr', methods=['POST'])
def extract_text():
    """
    Extract text from uploaded image using Tesseract OCR
    Supports English and Ukrainian languages
    """
    try:
        logger.info("Request received for text extraction")

        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400

        # Get language parameter (default to English)
        language = request.form.get('language', 'eng')

        logger.info(f"Processing {file.filename} image with language")

        # Validate language parameter
        supported_languages = ['eng', 'ukr', 'eng+ukr']
        if language not in supported_languages:
            return jsonify({
                "error": f"Unsupported language. Supported languages: {supported_languages}"
            }), 400

        # Read image file
        image_bytes = file.read()

        # Validate image format
        try:
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            return jsonify({"error": "Invalid image format"}), 400

        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Extract text using Tesseract
        logger.info(f"Processing image with language: {language}")

        # Configure Tesseract options
        config = '--oem 3 --psm 6'  # OCR Engine Mode 3, Page Segmentation Mode 6

        extracted_text = pytesseract.image_to_string(
            image,
            lang=language,
            config=config
        ).strip()

        # Get confidence scores
        data = pytesseract.image_to_data(image, lang=language, config=config, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        response = {
            "success": True,
            "text": extracted_text,
            "language": language,
            "confidence": round(avg_confidence, 2),
            "word_count": len(extracted_text.split()) if extracted_text else 0
        }

        logger.info(f"Text extraction successful. Word count: {response['word_count']}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error during text extraction"
        }), 500

@app.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    languages = {
        "eng": "English",
        "ukr": "Ukrainian",
        "eng+ukr": "English + Ukrainian"
    }
    return jsonify({"supported_languages": languages})

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
