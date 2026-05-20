# Advanced Text-to-Image Placeholder API

[![Olaverse API](https://img.shields.io/badge/Olaverse-API%20Doc-blue?style=flat-square)](https://www.olaverse.co.uk/placeholder-api) [![Try on Vibeland](https://img.shields.io/badge/Vibeland-Try%20Live-orange?style=flat-square)](https://www.vibeland.co.uk/tools/image-placeholder)

A comprehensive FastAPI-based service that generates placeholder images with custom text and advanced styling options.

## Features

- Generate placeholder images with custom text
- Customize image dimensions (up to 3000x3000)
- Customize background and text colors
- Support for multiple image formats (PNG, JPEG, WEBP)
- Border customization with width and color
- Text positioning (center, top-left, top-right, bottom-left, bottom-right)
- Custom font size control
- Gradient background support
- Returns images in various formats
- Comprehensive API documentation
- Health check endpoint
- Input validation and error handling

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Usage

### Basic Image Generation

```
GET /generate
```

Query Parameters:
- `text` (required): The text to display on the image
- `width` (optional): Image width in pixels (default: 800, max: 3000)
- `height` (optional): Image height in pixels (default: 400, max: 3000)
- `bg_color` (optional): Background color in hex format (default: "#cccccc")
- `text_color` (optional): Text color in hex format (default: "#333333")
- `font_size` (optional): Font size in pixels (default: auto-calculated)
- `border_width` (optional): Border width in pixels (default: 0)
- `border_color` (optional): Border color in hex format (default: "#000000")
- `text_position` (optional): Text position (default: "center")
- `format` (optional): Image format - PNG, JPEG, WEBP (default: "PNG")

### Advanced Image Generation

```
GET /generate/advanced
```

Additional Parameters:
- `gradient` (optional): Enable gradient background (default: false)
- `gradient_color1` (optional): First gradient color (default: "#ff0000")
- `gradient_color2` (optional): Second gradient color (default: "#0000ff")

### Health Check

```
GET /health
```

Returns service health status.

## Examples

### Basic Usage
```
http://localhost:8000/generate?text=Hello%20World&width=1000&height=500
```

### With Custom Colors and Border
```
http://localhost:8000/generate?text=Styled%20Text&bg_color=%23ff0000&text_color=%23ffffff&border_width=5&border_color=%23000000
```

### With Gradient Background
```
http://localhost:8000/generate/advanced?text=Gradient%20Text&gradient=true&gradient_color1=%23ff0000&gradient_color2=%2300ff00
```

### Different Text Positions
```
http://localhost:8000/generate?text=Top%20Left&text_position=top-left
http://localhost:8000/generate?text=Bottom%20Right&text_position=bottom-right
```

### Different Formats
```
http://localhost:8000/generate?text=JPEG%20Image&format=JPEG
http://localhost:8000/generate?text=WebP%20Image&format=WEBP
```

## Testing

Run the test suite:

```bash
# Run all tests
python run_tests.py

# Or run with pytest directly
pytest test_main.py -v
```

The test suite includes:
- Basic functionality tests
- Parameter validation tests
- Error handling tests
- Edge case tests
- API documentation tests

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API includes comprehensive error handling for:
- Invalid dimensions (negative or too large)
- Invalid colors (malformed hex codes)
- Invalid text positions
- Invalid image formats
- Missing required parameters

## Performance

- Supports images up to 3000x3000 pixels
- Optimized for quick generation
- Memory efficient image processing
- Fast response times for typical use cases 