"""
Agent 3: The Creative Director
Responsible for creating visual assets using AI image generation.
Creates carousel covers, ebook covers, social graphics.
"""

import logging
from typing import Optional
import openai
from config.faststrat_context import VISUAL_BRAND_GUIDELINES

logger = logging.getLogger(__name__)


class CreativeDirectorAgent:
    """
    Agent 3: Creative Director

    Capabilities:
    - Generate carousel cover images
    - Create ebook/guide covers
    - Design social media graphics
    - Create infographic concepts
    """

    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.brand_style = """
        Modern tech B2B aesthetic, clean minimalist design,
        gradient backgrounds with purple/indigo (#6366F1) and teal (#10B981) tones,
        professional but not corporate, bold typography,
        abstract geometric shapes, no text in image unless specified,
        high contrast, premium quality
        """

    def generate_carousel_cover(self, title: str, theme: str) -> dict:
        """
        Generate a cover image for a LinkedIn carousel.
        """
        prompt = f"""Create a striking LinkedIn carousel cover image.

THEME: {theme}
STYLE: {self.brand_style}

Requirements:
- Eye-catching visual that stops scrolling
- Modern tech/business aesthetic
- Abstract representation of the theme
- Gradient purple/indigo background
- NO TEXT in the image
- Professional B2B feel
- 1080x1080 square format composition
"""

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return {
                "success": True,
                "image_url": response.data[0].url,
                "type": "carousel_cover",
                "title": title
            }
        except Exception as e:
            logger.error(f"Carousel cover generation error: {e}")
            return {"success": False, "error": str(e)}

    def generate_ebook_cover(self, title: str, subtitle: str = "") -> dict:
        """
        Generate a cover image for an ebook/guide.
        """
        prompt = f"""Create a professional ebook cover design.

TITLE THEME: {title}
SUBTITLE: {subtitle}
STYLE: {self.brand_style}

Requirements:
- Premium ebook/report cover feel
- Modern tech aesthetic
- Abstract visual representing the topic
- Gradient from deep purple to teal
- Clean, minimalist composition
- Portrait orientation composition (like a book)
- NO TEXT in the image
- Professional B2B look
"""

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",  # Portrait for ebook
                quality="standard",
                n=1,
            )
            return {
                "success": True,
                "image_url": response.data[0].url,
                "type": "ebook_cover",
                "title": title
            }
        except Exception as e:
            logger.error(f"Ebook cover generation error: {e}")
            return {"success": False, "error": str(e)}

    def generate_social_graphic(self, concept: str, platform: str = "linkedin") -> dict:
        """
        Generate a social media graphic for posts.
        """
        sizes = {
            "linkedin": "1024x1024",
            "instagram": "1024x1024",
            "twitter": "1792x1024"
        }

        prompt = f"""Create a social media graphic for {platform}.

CONCEPT: {concept}
STYLE: {self.brand_style}

Requirements:
- Scroll-stopping visual
- Modern tech B2B aesthetic
- Abstract/conceptual representation
- Purple/indigo gradient background
- NO TEXT - visual only
- Clean, bold, professional
- High contrast for mobile viewing
"""

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=sizes.get(platform, "1024x1024"),
                quality="standard",
                n=1,
            )
            return {
                "success": True,
                "image_url": response.data[0].url,
                "type": "social_graphic",
                "platform": platform,
                "concept": concept
            }
        except Exception as e:
            logger.error(f"Social graphic generation error: {e}")
            return {"success": False, "error": str(e)}

    def generate_infographic_hero(self, topic: str, data_points: list) -> dict:
        """
        Generate a hero image for an infographic or data report.
        """
        data_context = ", ".join([str(d.get("stat", d)) for d in data_points[:3]]) if data_points else topic

        prompt = f"""Create a hero image for a data/statistics infographic.

TOPIC: {topic}
DATA CONTEXT: {data_context}
STYLE: {self.brand_style}

Requirements:
- Professional data visualization aesthetic
- Abstract representation of analytics/data
- Modern dashboard/metrics feel
- Gradient purple to teal colors
- Geometric shapes suggesting charts/graphs
- NO TEXT or actual numbers
- Clean tech look
- Premium report quality
"""

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",  # Landscape for reports
                quality="standard",
                n=1,
            )
            return {
                "success": True,
                "image_url": response.data[0].url,
                "type": "infographic_hero",
                "topic": topic
            }
        except Exception as e:
            logger.error(f"Infographic hero generation error: {e}")
            return {"success": False, "error": str(e)}

    def generate_slide_visual(self, slide_content: dict) -> dict:
        """
        Generate a visual element for a specific carousel slide.
        """
        title = slide_content.get("title", "")
        visual_note = slide_content.get("visual_note", "")

        prompt = f"""Create a visual element for a carousel slide.

SLIDE CONCEPT: {title}
VISUAL DIRECTION: {visual_note}
STYLE: {self.brand_style}

Requirements:
- Simple, iconic visual
- Works at small size
- Modern tech aesthetic
- Purple/indigo color scheme
- NO TEXT
- Clean and bold
- Conceptual/abstract representation
"""

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return {
                "success": True,
                "image_url": response.data[0].url,
                "type": "slide_visual",
                "slide_title": title
            }
        except Exception as e:
            logger.error(f"Slide visual generation error: {e}")
            return {"success": False, "error": str(e)}

    def generate_all_carousel_visuals(self, carousel_data: dict) -> list:
        """
        Generate cover + key slide visuals for a carousel.
        Returns list of generated images.
        """
        results = []

        # Generate cover
        cover = self.generate_carousel_cover(
            title=carousel_data.get("carousel_title", ""),
            theme=carousel_data.get("hook", "")
        )
        cover["slide_number"] = 0
        results.append(cover)

        # Generate visuals for key slides (1, 5, 10)
        slides = carousel_data.get("slides", [])
        key_slides = [0, 4, len(slides)-1] if len(slides) > 5 else [0, len(slides)-1]

        for idx in key_slides:
            if idx < len(slides):
                visual = self.generate_slide_visual(slides[idx])
                visual["slide_number"] = slides[idx].get("slide_number", idx+1)
                results.append(visual)

        return results
