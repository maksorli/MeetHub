from PIL import Image
import asyncio
 

def process_image(image_path, watermark_path):
    """функция  наложения водяного знака"""
    base_image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")  
    
    watermark = watermark.resize(base_image.size)
    
    combined = Image.alpha_composite(base_image, watermark)
    
    combined.save(image_path)

async def overlay_watermark(image_path, watermark_path):
    """выполнение process_image в другом потоке"""
    await asyncio.to_thread(process_image, image_path, watermark_path)
