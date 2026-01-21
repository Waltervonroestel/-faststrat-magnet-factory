"""
Agent 4: The Growth Copywriter
Responsible for writing viral LinkedIn posts to distribute lead magnets.
Uses proven viral frameworks (PASTOR, PAS, AIDA).
"""

import json
import logging
from config.faststrat_context import FASTSTRAT_CONTEXT

logger = logging.getLogger(__name__)


class GrowthCopywriterAgent:
    """
    Agent 4: Growth Copywriter

    Capabilities:
    - Write viral LinkedIn posts
    - Create comment triggers
    - Craft email sequences
    - Write landing page copy
    """

    def __init__(self, ai_client):
        self.ai_client = ai_client

    def write_linkedin_post(self, lead_magnet: dict, research: dict, comment_trigger: str = None) -> dict:
        """
        Write a viral LinkedIn post to distribute the lead magnet.
        Uses PASTOR framework.
        """
        trigger = comment_trigger or lead_magnet.get("comment_trigger", "GUÍA")

        prompt = f"""Eres el Growth Copywriter de FastStrat. Escribe un POST VIRAL para LinkedIn.

LEAD MAGNET A PROMOCIONAR:
{json.dumps(lead_magnet, indent=2, ensure_ascii=False)[:2000]}

RESEARCH/DATA POINTS:
{json.dumps(research, indent=2, ensure_ascii=False)[:1500]}

COMMENT TRIGGER: {trigger}

{FASTSTRAT_CONTEXT}

FRAMEWORK PASTOR:
- Problem: Identifica el dolor con dato impactante
- Agitate: Amplifica las consecuencias de no actuar
- Story: Mini-historia o ejemplo real
- Testimony: Prueba social o dato de autoridad
- Offer: El lead magnet como solución
- Response: CTA claro ("Comenta {trigger}")

REGLAS OBLIGATORIAS:
1. Hook en primera línea (dato impactante o pregunta provocadora)
2. Líneas cortas (máx 10 palabras por línea)
3. Espacios entre párrafos
4. Incluir AL MENOS 1 dato real con fuente
5. Máximo 1 emoji o ninguno
6. Terminar con "Comenta '{trigger}' y te lo envío"
7. 3 hashtags incluyendo #FastStrat
8. Entre 150-200 palabras

TONO: Colombiano, directo, de founder a founder. Nada corporativo.

Responde en JSON:
{{
    "post_text": "EL POST COMPLETO LISTO PARA COPIAR",
    "hook": "la primera línea del post",
    "comment_trigger": "{trigger}",
    "hashtags": ["#hashtag1", "#hashtag2", "#FastStrat"],
    "estimated_engagement": "alto/medio/bajo",
    "best_posting_time": "día y hora recomendados",
    "follow_up_comment": "comentario para poner después de publicar para boost del algoritmo"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=1500)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"LinkedIn post error: {e}")
            return {"error": str(e)}

    def write_carousel_intro_post(self, carousel: dict) -> dict:
        """
        Write a post specifically for carousel distribution.
        Different approach - teases the content.
        """
        prompt = f"""Escribe un post de LinkedIn para acompañar este CAROUSEL.

CAROUSEL DATA:
Título: {carousel.get('carousel_title', '')}
Hook: {carousel.get('hook', '')}
Slides: {len(carousel.get('slides', []))}
Target: {carousel.get('target_audience', '')}

OBJETIVO: Que la gente deslice el carousel completo y comente.

ESTRUCTURA:
1. Hook que genere curiosidad sobre el contenido del carousel
2. Promesa de lo que van a aprender
3. Teaser de 2-3 puntos clave
4. CTA: "Guarda este post + comenta para más contenido así"

REGLAS:
- Corto (80-120 palabras máximo)
- Líneas cortas
- Generar FOMO de no ver el carousel
- NO revelar todo el contenido

Responde en JSON:
{{
    "post_text": "post completo",
    "hook": "primera línea",
    "cta": "call to action",
    "hashtags": ["#tag1", "#tag2", "#FastStrat"]
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=800)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Carousel intro post error: {e}")
            return {"error": str(e)}

    def write_dm_response(self, lead_magnet_title: str, download_link: str = "[LINK]") -> dict:
        """
        Write the DM response to send when someone comments.
        """
        prompt = f"""Escribe el MENSAJE DIRECTO para enviar a quienes comenten pidiendo el lead magnet.

LEAD MAGNET: {lead_magnet_title}
LINK: {download_link}

OBJETIVOS:
1. Entregar el recurso prometido
2. Generar conversación
3. Calificar si es potencial cliente de FastStrat

ESTRUCTURA:
1. Saludo personalizado
2. Entrega del recurso
3. Pregunta de calificación (qué problema tienen)
4. Invitación sutil a conocer FastStrat

Responde en JSON:
{{
    "dm_text": "mensaje completo",
    "follow_up_question": "pregunta para continuar conversación",
    "qualifying_question": "pregunta para identificar si es ICP"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=600)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"DM response error: {e}")
            return {"error": str(e)}

    def write_email_sequence(self, lead_magnet: dict) -> dict:
        """
        Write a 3-email nurture sequence after lead magnet download.
        """
        prompt = f"""Escribe una SECUENCIA DE 3 EMAILS para nurturing después de descargar el lead magnet.

LEAD MAGNET:
{json.dumps(lead_magnet, indent=2, ensure_ascii=False)[:1500]}

{FASTSTRAT_CONTEXT}

SECUENCIA:
1. Email 1 (inmediato): Entrega + quick win
2. Email 2 (día 2): Profundizar + caso de éxito
3. Email 3 (día 4): CTA a demo/trial de FastStrat

REGLAS:
- Subject lines con alta apertura
- Emails cortos (150 palabras máx)
- Valor en cada email, no solo venta
- Tono personal, de founder

Responde en JSON:
{{
    "sequence_name": "nombre de la secuencia",
    "emails": [
        {{
            "day": 0,
            "subject": "asunto del email",
            "preview_text": "texto de preview",
            "body": "cuerpo completo del email",
            "cta_button": "texto del botón",
            "cta_link": "descripción del link"
        }},
        ...
    ]
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=2500)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Email sequence error: {e}")
            return {"error": str(e)}

    def write_landing_page_copy(self, lead_magnet: dict) -> dict:
        """
        Write copy for a lead magnet landing page.
        """
        prompt = f"""Escribe el COPY para una landing page del lead magnet.

LEAD MAGNET:
{json.dumps(lead_magnet, indent=2, ensure_ascii=False)[:2000]}

{FASTSTRAT_CONTEXT}

SECCIONES NECESARIAS:
1. Headline principal
2. Subheadline
3. Bullet points de beneficios (5)
4. Social proof placeholder
5. CTA button text
6. Descripción de qué incluye

Responde en JSON:
{{
    "headline": "título principal",
    "subheadline": "subtítulo",
    "benefits": [
        {{"benefit": "beneficio", "description": "descripción corta"}},
        ...
    ],
    "what_you_get": ["item 1", "item 2", ...],
    "cta_button": "texto del botón",
    "cta_subtext": "texto debajo del botón",
    "social_proof_suggestion": "qué tipo de social proof incluir"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=1500)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Landing page copy error: {e}")
            return {"error": str(e)}
