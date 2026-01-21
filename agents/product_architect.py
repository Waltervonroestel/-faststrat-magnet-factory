"""
Agent 2: The Product Architect
Responsible for creating the actual content of the Lead Magnet.
Writes every word of the PDF, Checklist, Carousel, or Guide.
"""

import json
import logging
from typing import Optional
from config.faststrat_context import FASTSTRAT_CONTEXT, LEAD_MAGNET_GUIDELINES

logger = logging.getLogger(__name__)


class ProductArchitectAgent:
    """
    Agent 2: Product Architect

    Capabilities:
    - Create complete carousel content (slide by slide)
    - Write full PDF guides
    - Generate checklists
    - Create data reports
    """

    def __init__(self, ai_client):
        self.ai_client = ai_client

    def create_carousel(self, research: dict, title: str = None) -> dict:
        """
        Create a complete LinkedIn carousel (8-12 slides).
        Returns slide-by-slide content.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un CAROUSEL COMPLETO para LinkedIn.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{LEAD_MAGNET_GUIDELINES}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Crea exactamente 10 slides
2. Cada slide debe tener: título corto (max 8 palabras) + cuerpo (max 40 palabras)
3. Slide 1: Hook visual impactante con dato o pregunta
4. Slide 2: El problema con datos reales
5. Slides 3-7: Contenido de valor (tips, framework, método)
6. Slide 8-9: El framework completo o resumen
7. Slide 10: CTA con "Comenta [PALABRA] para enviártelo"

Responde en JSON:
{{
    "carousel_title": "título del carousel",
    "hook": "gancho principal en 1 oración",
    "target_audience": "para quién es",
    "slides": [
        {{
            "slide_number": 1,
            "title": "título del slide",
            "body": "contenido del slide",
            "visual_note": "descripción de elemento visual sugerido"
        }},
        ...
    ],
    "comment_trigger": "palabra para comentar (ej: PLAN, GUÍA, etc)",
    "estimated_engagement": "alto/medio/bajo"
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
            logger.error(f"Carousel creation error: {e}")
            return {"error": str(e)}

    def create_guide(self, research: dict, title: str = None, pages: int = 7) -> dict:
        """
        Create a complete PDF guide/ebook.
        Returns section-by-section content.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea una GUÍA/EBOOK COMPLETA.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}
PÁGINAS OBJETIVO: {pages}

{LEAD_MAGNET_GUIDELINES}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Escribe TODO el contenido, no resúmenes
2. Cada sección debe ser implementable inmediatamente
3. Incluye ejemplos concretos
4. Siempre cita las fuentes del research
5. Termina conectando con FastStrat

ESTRUCTURA OBLIGATORIA:
- Portada
- Introducción (el problema)
- Por qué las soluciones actuales fallan
- El método/framework (2-3 secciones)
- Ejemplos prácticos
- Checklist de implementación
- Siguiente paso (CTA FastStrat)

Responde en JSON:
{{
    "guide_title": "título de la guía",
    "subtitle": "subtítulo",
    "target_audience": "para quién es",
    "sections": [
        {{
            "section_number": 1,
            "title": "título de sección",
            "content": "CONTENIDO COMPLETO de la sección (mínimo 150 palabras)",
            "key_takeaway": "punto clave en 1 oración"
        }},
        ...
    ],
    "bonus_checklist": [
        "item 1 accionable",
        "item 2 accionable",
        ...
    ],
    "cta_text": "texto del call to action final"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=4000)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Guide creation error: {e}")
            return {"error": str(e)}

    def create_checklist(self, research: dict, title: str = None) -> dict:
        """
        Create a comprehensive checklist (15-20 items).
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un CHECKLIST COMPLETO.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Crea 15-20 items accionables
2. Agrupa en categorías lógicas (3-4 categorías)
3. Cada item debe ser específico y verificable
4. Incluye métricas donde sea posible
5. El último item debe conectar con FastStrat

Responde en JSON:
{{
    "checklist_title": "título del checklist",
    "subtitle": "subtítulo descriptivo",
    "categories": [
        {{
            "category_name": "nombre de categoría",
            "items": [
                {{
                    "item": "descripción del item",
                    "why_important": "por qué importa (1 oración)",
                    "metric": "cómo medir éxito (opcional)"
                }},
                ...
            ]
        }},
        ...
    ],
    "total_items": 15,
    "estimated_completion_time": "tiempo estimado",
    "cta": "call to action final"
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
            logger.error(f"Checklist creation error: {e}")
            return {"error": str(e)}

    def create_data_report(self, stats_research: dict, title: str = None) -> dict:
        """
        Create a data-driven report with statistics and insights.
        For the Data-Authority route.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un REPORTE DE DATOS completo.

ESTADÍSTICAS RECOPILADAS:
{json.dumps(stats_research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or stats_research.get('report_title', 'Estado del Marketing 2026')}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Organiza los datos en secciones temáticas
2. Cada estadística DEBE tener su fuente citada
3. Agrega análisis e interpretación de FastStrat
4. Incluye gráficos sugeridos (describe qué mostrar)
5. Termina con recomendaciones accionables

ESTRUCTURA:
- Executive Summary
- Metodología (fuentes)
- Hallazgos principales (3-4 secciones)
- Análisis FastStrat
- Recomendaciones
- Siguiente paso

Responde en JSON:
{{
    "report_title": "título del reporte",
    "subtitle": "subtítulo",
    "executive_summary": "resumen ejecutivo (100 palabras)",
    "methodology": "descripción de fuentes usadas",
    "sections": [
        {{
            "section_title": "título",
            "key_stat": "estadística principal",
            "source": "fuente",
            "analysis": "análisis de FastStrat (150+ palabras)",
            "chart_suggestion": "tipo de gráfico sugerido y qué mostrar",
            "implication": "qué significa para PyMEs/Agencias"
        }},
        ...
    ],
    "recommendations": [
        {{
            "recommendation": "recomendación",
            "priority": "alta/media/baja",
            "how_faststrat_helps": "cómo FastStrat facilita esto"
        }},
        ...
    ],
    "conclusion": "conclusión y CTA"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=4000)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Data report creation error: {e}")
            return {"error": str(e)}

    def create_template(self, research: dict, template_type: str = "strategy") -> dict:
        """
        Create a fillable template (strategy, content calendar, etc).
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un TEMPLATE utilizable.

TIPO DE TEMPLATE: {template_type}

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. El template debe ser USABLE inmediatamente
2. Incluye instrucciones de llenado
3. Proporciona ejemplos en cada sección
4. Hazlo visual y organizado

Responde en JSON:
{{
    "template_title": "título del template",
    "description": "descripción de uso",
    "sections": [
        {{
            "section_name": "nombre",
            "instructions": "cómo llenar esta sección",
            "fields": [
                {{
                    "field_name": "nombre del campo",
                    "placeholder": "ejemplo de qué poner",
                    "help_text": "ayuda adicional"
                }},
                ...
            ],
            "example": "ejemplo completo de esta sección llena"
        }},
        ...
    ],
    "pro_tips": ["tip 1", "tip 2", ...],
    "faststrat_upgrade": "cómo FastStrat automatiza este proceso"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=3000)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Template creation error: {e}")
            return {"error": str(e)}
