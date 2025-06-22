import pytest
from fastapi.testclient import TestClient
from main import app
from PIL import Image
import io

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Advanced Text-to-Image Placeholder API"
    assert data["version"] == "2.0.0"
    assert "endpoints" in data

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "text-to-image-placeholder"

def test_generate_basic_image():
    """Test basic image generation."""
    response = client.get("/generate", params={"text": "Test Image"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Verify it's a valid image
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    assert image.size == (800, 400)  # Default size

def test_generate_custom_size():
    """Test image generation with custom size."""
    response = client.get("/generate", params={
        "text": "Custom Size",
        "width": 1000,
        "height": 600
    })
    assert response.status_code == 200
    
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    assert image.size == (1000, 600)

def test_generate_custom_colors():
    """Test image generation with custom colors."""
    response = client.get("/generate", params={
        "text": "Color Test",
        "bg_color": "#ff0000",
        "text_color": "#ffffff"
    })
    assert response.status_code == 200

def test_generate_with_border():
    """Test image generation with border."""
    response = client.get("/generate", params={
        "text": "Border Test",
        "border_width": 5,
        "border_color": "#000000"
    })
    assert response.status_code == 200

def test_generate_different_formats():
    """Test image generation in different formats."""
    formats = ["PNG", "JPEG", "WEBP"]
    for format in formats:
        response = client.get("/generate", params={
            "text": f"Format Test {format}",
            "format": format
        })
        assert response.status_code == 200
        assert response.headers["content-type"] == f"image/{format.lower()}"

def test_generate_different_text_positions():
    """Test image generation with different text positions."""
    positions = ["center", "top-left", "top-right", "bottom-left", "bottom-right"]
    for position in positions:
        response = client.get("/generate", params={
            "text": f"Position {position}",
            "text_position": position
        })
        assert response.status_code == 200

def test_generate_advanced_with_gradient():
    """Test advanced image generation with gradient."""
    response = client.get("/generate/advanced", params={
        "text": "Gradient Test",
        "gradient": True,
        "gradient_color1": "#ff0000",
        "gradient_color2": "#0000ff"
    })
    assert response.status_code == 200

def test_generate_advanced_without_gradient():
    """Test advanced image generation without gradient."""
    response = client.get("/generate/advanced", params={
        "text": "No Gradient Test",
        "gradient": False
    })
    assert response.status_code == 200

def test_invalid_width():
    """Test error handling for invalid width."""
    response = client.get("/generate", params={
        "text": "Test",
        "width": -1
    })
    assert response.status_code == 422

def test_invalid_height():
    """Test error handling for invalid height."""
    response = client.get("/generate", params={
        "text": "Test",
        "height": 0
    })
    assert response.status_code == 422

def test_invalid_text_position():
    """Test error handling for invalid text position."""
    response = client.get("/generate", params={
        "text": "Test",
        "text_position": "invalid"
    })
    assert response.status_code == 400

def test_invalid_format():
    """Test error handling for invalid format."""
    response = client.get("/generate", params={
        "text": "Test",
        "format": "INVALID"
    })
    assert response.status_code == 400

def test_missing_text():
    """Test error handling for missing text parameter."""
    response = client.get("/generate")
    assert response.status_code == 422

def test_large_dimensions():
    """Test handling of large dimensions."""
    response = client.get("/generate", params={
        "text": "Large Image",
        "width": 3000,
        "height": 3000
    })
    assert response.status_code == 200

def test_small_dimensions():
    """Test handling of small dimensions."""
    response = client.get("/generate", params={
        "text": "Small Image",
        "width": 100,
        "height": 50
    })
    assert response.status_code == 200

def test_custom_font_size():
    """Test custom font size."""
    response = client.get("/generate", params={
        "text": "Font Size Test",
        "font_size": 50
    })
    assert response.status_code == 200

def test_edge_case_text():
    """Test edge case text."""
    edge_texts = [
        "",  # Empty text
        "A" * 100,  # Very long text
        "Special chars: !@#$%^&*()",
        "Unicode: 你好世界",
        "Numbers: 1234567890"
    ]
    
    for text in edge_texts:
        response = client.get("/generate", params={"text": text})
        assert response.status_code == 200

def test_api_documentation():
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc_documentation():
    """Test that ReDoc documentation is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__]) 