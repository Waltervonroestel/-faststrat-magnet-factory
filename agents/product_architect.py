"""
Agent 2: The Product Architect
Responsible for creating the actual content of the Lead Magnet.
Writes every word of PDFs, Checklists, Carousels, Guides, Templates,
Mini-Courses, Worksheets, Case Studies, and more.
"""

import json
import logging
from typing import Optional
from config.faststrat_context import FASTSTRAT_CONTEXT, LEAD_MAGNET_GUIDELINES

logger = logging.getLogger(__name__)

# Available formats with descriptions
LEAD_MAGNET_FORMATS = {
    "carousel": {
        "name": "Carousel LinkedIn",
        "description": "8-12 slides para LinkedIn con contenido visual",
        "best_for": "Engagement rápido, viralidad"
    },
    "guide": {
        "name": "Guía/Ebook PDF",
        "description": "Documento de 5-15 páginas con contenido profundo",
        "best_for": "Autoridad, leads calificados"
    },
    "checklist": {
        "name": "Checklist Accionable",
        "description": "Lista de 15-25 items verificables",
        "best_for": "Implementación rápida, valor inmediato"
    },
    "template": {
        "name": "Template/Plantilla",
        "description": "Documento listo para usar y personalizar",
        "best_for": "Ahorro de tiempo, practicidad"
    },
    "minicourse": {
        "name": "Mini-Curso (5 emails)",
        "description": "Secuencia de 5 emails educativos",
        "best_for": "Nurturing, educación profunda"
    },
    "worksheet": {
        "name": "Worksheet/Hoja de Trabajo",
        "description": "Ejercicios prácticos para completar",
        "best_for": "Autodiagnóstico, reflexión"
    },
    "swipefile": {
        "name": "Swipe File",
        "description": "Colección de ejemplos listos para copiar",
        "best_for": "Inspiración, referencia rápida"
    },
    "casestudy": {
        "name": "Caso de Estudio",
        "description": "Análisis detallado de un caso real",
        "best_for": "Prueba social, credibilidad"
    },
    "toolkit": {
        "name": "Toolkit/Kit de Herramientas",
        "description": "Colección de recursos y herramientas",
        "best_for": "Valor completo, recurso de referencia"
    },
    "cheatsheet": {
        "name": "Cheat Sheet",
        "description": "Resumen de 1-2 páginas con lo esencial",
        "best_for": "Referencia rápida, fácil de consumir"
    }
}


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

    def create_minicourse(self, research: dict, title: str = None) -> dict:
        """
        Create a 5-email mini-course sequence.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un MINI-CURSO de 5 emails.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Crea exactamente 5 emails educativos
2. Cada email debe poder leerse en 3-5 minutos
3. Progresión lógica de básico a avanzado
4. Cada email termina con un "quick win" implementable
5. Email 5 conecta con FastStrat como siguiente paso

ESTRUCTURA POR EMAIL:
- Subject line irresistible
- Preview text
- Saludo personalizado
- Contenido educativo (300-400 palabras)
- Ejemplo práctico
- Acción del día
- Teaser del siguiente email

Responde en JSON:
{{
    "course_title": "título del mini-curso",
    "subtitle": "subtítulo",
    "target_audience": "para quién es",
    "transformation_promise": "qué logrará al terminar",
    "emails": [
        {{
            "day": 1,
            "subject": "línea de asunto",
            "preview_text": "texto de preview",
            "theme": "tema del día",
            "content": "CONTENIDO COMPLETO del email (300+ palabras)",
            "key_lesson": "lección principal",
            "action_item": "acción específica para hoy",
            "next_teaser": "adelanto del siguiente email"
        }},
        ...
    ],
    "bonus_resource": "recurso adicional sugerido",
    "final_cta": "call to action final hacia FastStrat"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=5000)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Mini-course creation error: {e}")
            return {"error": str(e)}

    def create_worksheet(self, research: dict, title: str = None) -> dict:
        """
        Create an interactive worksheet with exercises.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un WORKSHEET interactivo.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Crea 5-7 ejercicios prácticos
2. Cada ejercicio debe generar reflexión y acción
3. Incluye espacios para escribir respuestas
4. Progresión de autodiagnóstico a plan de acción
5. Termina con un ejercicio que conecte con FastStrat

TIPOS DE EJERCICIOS:
- Autodiagnóstico (escala 1-10)
- Preguntas de reflexión
- Matrices de priorización
- Listas para completar
- Mini-auditorías
- Planificación de acciones

Responde en JSON:
{{
    "worksheet_title": "título del worksheet",
    "subtitle": "subtítulo",
    "introduction": "introducción y cómo usar (100 palabras)",
    "estimated_time": "tiempo estimado para completar",
    "exercises": [
        {{
            "exercise_number": 1,
            "title": "título del ejercicio",
            "type": "tipo (diagnostic/reflection/matrix/planning)",
            "instructions": "instrucciones claras",
            "questions": [
                {{
                    "question": "pregunta o prompt",
                    "space_for_answer": "descripción del espacio (líneas, tabla, etc)",
                    "example_answer": "ejemplo de respuesta ideal"
                }},
                ...
            ],
            "key_insight": "qué aprenderá de este ejercicio"
        }},
        ...
    ],
    "scoring_guide": "guía de interpretación de resultados (si aplica)",
    "next_steps": "qué hacer con los resultados",
    "faststrat_connection": "cómo FastStrat ayuda a implementar"
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
            logger.error(f"Worksheet creation error: {e}")
            return {"error": str(e)}

    def create_swipefile(self, research: dict, swipe_type: str = "copy") -> dict:
        """
        Create a swipe file with copy-paste examples.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un SWIPE FILE completo.

TIPO DE SWIPE: {swipe_type}

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Crea 15-20 ejemplos listos para copiar/adaptar
2. Agrupa por categoría o uso
3. Cada ejemplo debe ser directamente usable
4. Incluye notas de cuándo usar cada uno
5. Variedad de tonos y estilos

TIPOS DE CONTENIDO SEGÚN SWIPE_TYPE:
- copy: Headlines, CTAs, emails, posts
- design: Layouts, estructuras, formatos
- strategy: Frameworks, procesos, plantillas
- outreach: Mensajes de venta, follow-ups

Responde en JSON:
{{
    "swipefile_title": "título del swipe file",
    "swipe_type": "{swipe_type}",
    "description": "descripción y cómo usar",
    "categories": [
        {{
            "category_name": "nombre de categoría",
            "description": "cuándo usar estos ejemplos",
            "swipes": [
                {{
                    "swipe_name": "nombre/identificador",
                    "content": "CONTENIDO COMPLETO listo para copiar",
                    "when_to_use": "situación ideal para usar",
                    "customization_tips": "cómo personalizar"
                }},
                ...
            ]
        }},
        ...
    ],
    "total_swipes": 15,
    "pro_tips": ["tip 1 de uso", "tip 2", ...],
    "faststrat_bonus": "cómo FastStrat genera estos automáticamente"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=4500)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Swipe file creation error: {e}")
            return {"error": str(e)}

    def create_casestudy(self, research: dict, title: str = None) -> dict:
        """
        Create a detailed case study analysis.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un CASO DE ESTUDIO detallado.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Estructura narrativa compelling (problema → solución → resultados)
2. Datos y métricas específicas
3. Lecciones extraíbles y aplicables
4. Conecta con la metodología FastStrat
5. Si no hay caso real, crea uno representativo basado en patrones reales

ESTRUCTURA:
- Contexto del caso
- El desafío/problema
- La solución implementada
- Resultados con métricas
- Lecciones aprendidas
- Cómo aplicar esto

Responde en JSON:
{{
    "case_study_title": "título del caso",
    "subtitle": "subtítulo atractivo",
    "company_profile": {{
        "type": "tipo de empresa (PyME, Startup, Agencia)",
        "industry": "industria",
        "size": "tamaño aproximado",
        "initial_situation": "situación antes"
    }},
    "challenge": {{
        "main_problem": "problema principal",
        "symptoms": ["síntoma 1", "síntoma 2", ...],
        "failed_attempts": "qué habían intentado antes",
        "stakes": "qué estaba en juego"
    }},
    "solution": {{
        "approach": "enfoque general",
        "steps": [
            {{
                "step_number": 1,
                "action": "acción tomada",
                "rationale": "por qué funcionó",
                "tools_used": "herramientas o métodos"
            }},
            ...
        ],
        "timeline": "tiempo de implementación"
    }},
    "results": {{
        "metrics": [
            {{
                "metric": "nombre de métrica",
                "before": "valor antes",
                "after": "valor después",
                "improvement": "% o cantidad de mejora"
            }},
            ...
        ],
        "qualitative_wins": ["logro cualitativo 1", ...],
        "roi": "retorno de inversión estimado"
    }},
    "lessons_learned": [
        {{
            "lesson": "lección",
            "application": "cómo aplicar en tu negocio"
        }},
        ...
    ],
    "key_takeaway": "conclusión principal en 1-2 oraciones",
    "faststrat_connection": "cómo FastStrat facilita replicar esto"
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
            logger.error(f"Case study creation error: {e}")
            return {"error": str(e)}

    def create_toolkit(self, research: dict, title: str = None) -> dict:
        """
        Create a comprehensive toolkit with multiple resources.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un TOOLKIT completo.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Crea un kit con 5-7 herramientas/recursos diferentes
2. Cada herramienta debe ser usable independientemente
3. En conjunto deben resolver un problema completo
4. Incluye instrucciones de uso para cada una
5. Hazlo sentir como un "kit profesional"

TIPOS DE HERRAMIENTAS A INCLUIR:
- Checklist de diagnóstico
- Template/plantilla
- Calculadora o matriz
- Guía rápida (1 página)
- Scripts o ejemplos
- Framework visual

Responde en JSON:
{{
    "toolkit_title": "título del toolkit",
    "subtitle": "subtítulo",
    "description": "descripción general del kit",
    "problem_solved": "qué problema resuelve este kit",
    "tools": [
        {{
            "tool_number": 1,
            "tool_name": "nombre de la herramienta",
            "tool_type": "tipo (checklist/template/calculator/guide/scripts/framework)",
            "description": "para qué sirve",
            "when_to_use": "cuándo usar",
            "content": "CONTENIDO COMPLETO de la herramienta",
            "instructions": "cómo usar paso a paso"
        }},
        ...
    ],
    "implementation_order": "orden sugerido de uso",
    "quick_start": "cómo empezar en 5 minutos",
    "advanced_tips": ["tip avanzado 1", "tip 2", ...],
    "faststrat_upgrade": "cómo FastStrat potencia este toolkit"
}}"""

        try:
            response = self.ai_client.generate(prompt, max_tokens=5000)
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            logger.error(f"Toolkit creation error: {e}")
            return {"error": str(e)}

    def create_cheatsheet(self, research: dict, title: str = None) -> dict:
        """
        Create a 1-2 page quick reference cheat sheet.
        """
        prompt = f"""Eres el Product Architect de FastStrat. Crea un CHEAT SHEET de referencia rápida.

RESEARCH DATA:
{json.dumps(research, indent=2, ensure_ascii=False)}

TÍTULO SUGERIDO: {title or 'Genera uno basado en el research'}

{FASTSTRAT_CONTEXT}

INSTRUCCIONES:
1. Máximo 1-2 páginas (contenido denso pero escaneable)
2. Diseñado para imprimir y tener a la mano
3. Organizado en secciones visuales claras
4. Solo lo esencial, sin relleno
5. Formato de referencia rápida (bullets, tablas, fórmulas)

ELEMENTOS A INCLUIR:
- Fórmulas o frameworks clave
- Listas de verificación rápidas
- Métricas importantes
- Errores comunes a evitar
- Atajos o trucos pro
- Referencias rápidas

Responde en JSON:
{{
    "cheatsheet_title": "título del cheat sheet",
    "subtitle": "subtítulo corto",
    "sections": [
        {{
            "section_name": "nombre de sección",
            "format": "tipo (bullets/table/formula/checklist)",
            "content": [
                {{
                    "item": "elemento",
                    "detail": "detalle breve (máx 15 palabras)"
                }},
                ...
            ]
        }},
        ...
    ],
    "key_formulas": [
        {{
            "name": "nombre de fórmula/framework",
            "formula": "la fórmula o pasos",
            "example": "ejemplo rápido"
        }},
        ...
    ],
    "common_mistakes": ["error 1 a evitar", "error 2", ...],
    "pro_tips": ["tip pro 1", "tip pro 2", ...],
    "quick_reference_table": {{
        "headers": ["columna1", "columna2", ...],
        "rows": [["dato1", "dato2"], ...]
    }},
    "footer_cta": "CTA breve para FastStrat"
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
            logger.error(f"Cheat sheet creation error: {e}")
            return {"error": str(e)}

    def create_content(self, format_type: str, research: dict, **kwargs) -> dict:
        """
        Universal method to create any lead magnet format.
        Routes to the appropriate creation method based on format_type.
        """
        format_methods = {
            "carousel": self.create_carousel,
            "guide": self.create_guide,
            "checklist": self.create_checklist,
            "template": self.create_template,
            "minicourse": self.create_minicourse,
            "worksheet": self.create_worksheet,
            "swipefile": self.create_swipefile,
            "casestudy": self.create_casestudy,
            "toolkit": self.create_toolkit,
            "cheatsheet": self.create_cheatsheet,
            "datareport": self.create_data_report
        }

        if format_type not in format_methods:
            return {"error": f"Unknown format: {format_type}. Available: {list(format_methods.keys())}"}

        return format_methods[format_type](research, **kwargs)
