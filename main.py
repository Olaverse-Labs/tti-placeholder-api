from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import io
import os
from typing import Optional
import math

app = FastAPI(
    title="Text-to-Image Placeholder API",
    description="Advanced API for generating placeholder images with custom text and styling",
    version="2.0.0"
)

def create_placeholder_image(
    text: str,
    width: int = 800,
    height: int = 400,
    bg_color: str = "#cccccc",
    text_color: str = "#333333",
    font_size: Optional[int] = None,
    border_width: int = 0,
    border_color: str = "#000000",
    text_position: str = "center",
    image_format: str = "PNG"
) -> Image.Image:
    """Create a placeholder image with the given text and styling options."""
    # Create a new image with the given background color
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Calculate font size if not provided
    if font_size is None:
        font_size = min(width, height) // 20
    
    # Try to load a font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text based on text_position parameter
    if text_position == "center":
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    elif text_position == "top-left":
        x = 10
        y = 10
    elif text_position == "top-right":
        x = width - text_width - 10
        y = 10
    elif text_position == "bottom-left":
        x = 10
        y = height - text_height - 10
    elif text_position == "bottom-right":
        x = width - text_width - 10
        y = height - text_height - 10
    else:
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    
    # Draw border if specified
    if border_width > 0:
        draw.rectangle(
            [0, 0, width-1, height-1],
            outline=border_color,
            width=border_width
        )
    
    # Draw the text
    draw.text((x, y), text, fill=text_color, font=font)
    
    return image

def create_gradient_background(width: int, height: int, color1: str, color2: str) -> Image.Image:
    """Create a gradient background image."""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        ratio = y / height
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Advanced Text-to-Image Placeholder API",
        "version": "2.0.0",
        "endpoints": {
            "generate": "/generate - Basic image generation",
            "generate_advanced": "/generate/advanced - Advanced image generation with gradients",
            "health": "/health - Health check endpoint"
        },
        "usage": "Send GET request to /generate or /generate/advanced with parameters"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "text-to-image-placeholder"}

@app.get("/generate")
async def generate_image(
    text: str = Query(..., description="Text to display on the image"),
    width: int = Query(800, ge=1, le=3000, description="Image width in pixels"),
    height: int = Query(400, ge=1, le=3000, description="Image height in pixels"),
    bg_color: str = Query("#cccccc", description="Background color in hex format"),
    text_color: str = Query("#333333", description="Text color in hex format"),
    font_size: Optional[int] = Query(None, ge=8, le=200, description="Font size in pixels"),
    border_width: int = Query(0, ge=0, le=50, description="Border width in pixels"),
    border_color: str = Query("#000000", description="Border color in hex format"),
    text_position: str = Query("center", description="Text position: center, top-left, top-right, bottom-left, bottom-right"),
    format: str = Query("PNG", description="Image format: PNG, JPEG, WEBP")
):
    """Generate a placeholder image with the specified parameters."""
    try:
        # Validate text position
        valid_positions = ["center", "top-left", "top-right", "bottom-left", "bottom-right"]
        if text_position not in valid_positions:
            raise HTTPException(status_code=400, detail=f"Invalid text_position. Must be one of: {valid_positions}")
        
        # Validate format
        valid_formats = ["PNG", "JPEG", "WEBP"]
        if format.upper() not in valid_formats:
            raise HTTPException(status_code=400, detail=f"Invalid format. Must be one of: {valid_formats}")
        
        # Create the image
        image = create_placeholder_image(
            text, width, height, bg_color, text_color,
            font_size, border_width, border_color, text_position
        )
        
        # Convert to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format=format.upper())
        img_byte_array.seek(0)
        
        return StreamingResponse(
            img_byte_array,
            media_type=f"image/{format.lower()}",
            headers={"Content-Disposition": f'attachment; filename="placeholder-{width}x{height}.{format.lower()}"'}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate/advanced")
async def generate_advanced_image(
    text: str = Query(..., description="Text to display on the image"),
    width: int = Query(800, ge=1, le=3000, description="Image width in pixels"),
    height: int = Query(400, ge=1, le=3000, description="Image height in pixels"),
    bg_color: str = Query("#cccccc", description="Background color in hex format"),
    text_color: str = Query("#333333", description="Text color in hex format"),
    gradient: bool = Query(False, description="Enable gradient background"),
    gradient_color1: str = Query("#ff0000", description="First gradient color"),
    gradient_color2: str = Query("#0000ff", description="Second gradient color"),
    font_size: Optional[int] = Query(None, ge=8, le=200, description="Font size in pixels"),
    border_width: int = Query(0, ge=0, le=50, description="Border width in pixels"),
    border_color: str = Query("#000000", description="Border color in hex format"),
    text_position: str = Query("center", description="Text position"),
    format: str = Query("PNG", description="Image format")
):
    """Generate an advanced placeholder image with gradient support."""
    try:
        # Validate text position
        valid_positions = ["center", "top-left", "top-right", "bottom-left", "bottom-right"]
        if text_position not in valid_positions:
            raise HTTPException(status_code=400, detail=f"Invalid text_position. Must be one of: {valid_positions}")
        
        # Validate format
        valid_formats = ["PNG", "JPEG", "WEBP"]
        if format.upper() not in valid_formats:
            raise HTTPException(status_code=400, detail=f"Invalid format. Must be one of: {valid_formats}")
        
        # Create background
        if gradient:
            image = create_gradient_background(width, height, gradient_color1, gradient_color2)
        else:
            image = Image.new('RGB', (width, height), bg_color)
        
        draw = ImageDraw.Draw(image)
        
        # Calculate font size if not provided
        if font_size is None:
            font_size = min(width, height) // 20
        
        # Try to load a font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()
        
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Position text
        if text_position == "center":
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        elif text_position == "top-left":
            x = 10
            y = 10
        elif text_position == "top-right":
            x = width - text_width - 10
            y = 10
        elif text_position == "bottom-left":
            x = 10
            y = height - text_height - 10
        elif text_position == "bottom-right":
            x = width - text_width - 10
            y = height - text_height - 10
        else:
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        
        # Draw border if specified
        if border_width > 0:
            draw.rectangle(
                [0, 0, width-1, height-1],
                outline=border_color,
                width=border_width
            )
        
        # Draw the text
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Convert to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format=format.upper())
        img_byte_array.seek(0)
        
        return StreamingResponse(
            img_byte_array,
            media_type=f"image/{format.lower()}",
            headers={"Content-Disposition": f'attachment; filename="advanced-{width}x{height}.{format.lower()}"'}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 