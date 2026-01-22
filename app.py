"""
FastStrat Autonomous Magnet Factory v3.0
Multi-agent system for creating high-authority Lead Magnets.
"""

import os
import sys
from pathlib import Path

# Load .env FIRST - before ANY other imports that might use env vars
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)
print(f"[STARTUP] Loaded .env from: {env_path}")
print(f"[STARTUP] OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT SET')[:25]}...")
print(f"[STARTUP] ANTHROPIC_API_KEY: {os.getenv('ANTHROPIC_API_KEY', 'NOT SET')[:25]}...")

# Now import everything else
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "faststrat-magnet-factory")

# Import agents - these will now use the loaded env vars
from agents.ai_client import AIClient
from agents.market_intel import MarketIntelAgent
from agents.product_architect import ProductArchitectAgent
from agents.creative_director import CreativeDirectorAgent
from agents.growth_copywriter import GrowthCopywriterAgent

# Initialize AI client and agents
# Note: AIClient will read fresh env vars on init
ai_client = AIClient()
ai_client._refresh_credentials()  # Force refresh after dotenv load
market_intel = MarketIntelAgent(ai_client)
product_architect = ProductArchitectAgent(ai_client)
creative_director = CreativeDirectorAgent(os.getenv("OPENAI_API_KEY", ""))
growth_copywriter = GrowthCopywriterAgent(ai_client)
print(f"[STARTUP] Agents initialized with OPENAI: {os.getenv('OPENAI_API_KEY', '')[:25]}...")

# Store for current production
current_production = {
    "status": "idle",
    "route": None,
    "research": None,
    "content": None,
    "visuals": None,
    "post": None,
    "started_at": None,
    "completed_at": None
}


# ============================================================================
# DASHBOARD HTML
# ============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastStrat Magnet Factory v3.0</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 900px; margin: 0 auto; }
        .header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #6366f1, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .header .version {
            color: #10b981;
            font-size: 0.9em;
            font-weight: 600;
        }
        .status-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            font-size: 0.85em;
        }
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .routes {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .route-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .route-card:hover {
            background: rgba(255,255,255,0.1);
            border-color: #6366f1;
            transform: translateY(-2px);
        }
        .route-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .route-icon {
            font-size: 2em;
        }
        .route-title {
            font-size: 1.3em;
            font-weight: 600;
        }
        .route-tag {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
        }
        .route-description {
            color: rgba(255,255,255,0.7);
            line-height: 1.6;
        }
        .route-card.trend-jacker .route-tag { background: linear-gradient(135deg, #ef4444, #f97316); }
        .route-card.problem-solver .route-tag { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
        .route-card.data-authority .route-tag { background: linear-gradient(135deg, #10b981, #14b8a6); }

        .input-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
            display: none;
        }
        .route-card.active .input-section { display: block; }

        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .input-group input, .input-group select {
            width: 100%;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: #fff;
            font-size: 1em;
        }
        .input-group input:focus, .input-group select:focus {
            outline: none;
            border-color: #6366f1;
        }
        .btn-generate {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: #fff;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-generate:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(99,102,241,0.3);
        }
        .btn-generate:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .output-section {
            margin-top: 40px;
            padding: 30px;
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            display: none;
        }
        .output-section.visible { display: block; }

        .output-title {
            font-size: 1.3em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .output-content {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 0.9em;
            line-height: 1.6;
            max-height: 500px;
            overflow-y: auto;
        }

        .loading {
            text-align: center;
            padding: 40px;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(255,255,255,0.1);
            border-top-color: #6366f1;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .agent-status {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .agent-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            background: rgba(255,255,255,0.1);
        }
        .agent-badge.active {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            animation: pulse 1s infinite;
        }
        .agent-badge.complete {
            background: #10b981;
        }

        .result-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .result-tab {
            padding: 10px 20px;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            cursor: pointer;
            font-weight: 500;
        }
        .result-tab.active {
            background: #6366f1;
        }
        .result-panel { display: none; }
        .result-panel.active { display: block; }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            background: #6366f1;
            color: #fff;
            cursor: pointer;
            font-size: 0.8em;
        }
        .content-box {
            position: relative;
        }

        .image-preview {
            margin: 20px 0;
            text-align: center;
        }
        .image-preview img {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>FastStrat Magnet Factory</h1>
            <div class="version">v3.0 - Autonomous Lead Magnet Generation</div>
            <div class="status-bar">
                <div class="status-item">
                    <span class="status-dot"></span>
                    <span>Real-time Scanning Active</span>
                </div>
                <div class="status-item">
                    <span class="status-dot"></span>
                    <span>4 Agents Online</span>
                </div>
                <div class="status-item">
                    <span class="status-dot"></span>
                    <span>Image Gen Ready</span>
                </div>
            </div>
        </div>

        <h2 style="margin-bottom: 20px; font-weight: 500;">Selecciona tu ruta de producción:</h2>

        <div class="routes">
            <!-- Route 1: Trend-Jacker -->
            <div class="route-card trend-jacker" onclick="selectRoute('trend-jacker', this)">
                <div class="route-header">
                    <span class="route-icon">🔥</span>
                    <span class="route-title">Trend-Jacker</span>
                    <span class="route-tag">Real-Time</span>
                </div>
                <p class="route-description">
                    Escanea tendencias actuales de LinkedIn/YouTube y crea un Lead Magnet "News-jacking"
                    que capitaliza el momento. Ideal para engagement rápido.
                </p>
                <div class="input-section">
                    <div class="input-group">
                        <label>Industria/Nicho (opcional)</label>
                        <input type="text" id="trend-industry" placeholder="Ej: Marketing B2B, SaaS, Agencias...">
                    </div>
                    <div class="input-group">
                        <label>Formato del Lead Magnet</label>
                        <select id="trend-format">
                            <option value="carousel">🎠 Carousel LinkedIn (8-12 slides)</option>
                            <option value="guide">📘 Guía/Ebook PDF (5-15 págs)</option>
                            <option value="checklist">✅ Checklist Accionable (15-25 items)</option>
                            <option value="cheatsheet">📋 Cheat Sheet (1-2 págs)</option>
                            <option value="template">📝 Template/Plantilla</option>
                            <option value="swipefile">📂 Swipe File (copy-paste)</option>
                        </select>
                    </div>
                    <button class="btn-generate" onclick="generateMagnet('trend-jacker')">
                        🚀 Generar Lead Magnet
                    </button>
                </div>
            </div>

            <!-- Route 2: Problem-Solver -->
            <div class="route-card problem-solver" onclick="selectRoute('problem-solver', this)">
                <div class="route-header">
                    <span class="route-icon">🛠️</span>
                    <span class="route-title">Problem-Solver</span>
                    <span class="route-tag">Deep Solution</span>
                </div>
                <p class="route-description">
                    Crea una solución basada en un dolor específico de tu ICP.
                    Perfecto para posicionamiento como experto y leads calificados.
                </p>
                <div class="input-section">
                    <div class="input-group">
                        <label>Dolor/Problema específico *</label>
                        <input type="text" id="problem-pain" placeholder="Ej: Bajos márgenes en agencias, No sé qué publicar...">
                    </div>
                    <div class="input-group">
                        <label>Formato del Lead Magnet</label>
                        <select id="problem-format">
                            <option value="guide">📘 Guía Completa (PDF)</option>
                            <option value="checklist">✅ Checklist Accionable</option>
                            <option value="template">📝 Template/Plantilla</option>
                            <option value="worksheet">📄 Worksheet/Ejercicios</option>
                            <option value="minicourse">📧 Mini-Curso (5 emails)</option>
                            <option value="toolkit">🧰 Toolkit Completo</option>
                            <option value="casestudy">📊 Caso de Estudio</option>
                            <option value="carousel">🎠 Carousel (LinkedIn)</option>
                            <option value="cheatsheet">📋 Cheat Sheet</option>
                            <option value="swipefile">📂 Swipe File</option>
                        </select>
                    </div>
                    <button class="btn-generate" onclick="generateMagnet('problem-solver')">
                        🛠️ Generar Solución
                    </button>
                </div>
            </div>

            <!-- Route 3: Data-Authority -->
            <div class="route-card data-authority" onclick="selectRoute('data-authority', this)">
                <div class="route-header">
                    <span class="route-icon">📊</span>
                    <span class="route-title">Data-Authority</span>
                    <span class="route-tag">Stats & Reports</span>
                </div>
                <p class="route-description">
                    Crea un reporte basado en estadísticas reales de la industria para
                    posicionar FastStrat como fuente de autoridad y generar confianza.
                </p>
                <div class="input-section">
                    <div class="input-group">
                        <label>Tema del Reporte</label>
                        <input type="text" id="data-topic" placeholder="Ej: Estado del Marketing 2026, ROI de IA en Marketing...">
                    </div>
                    <div class="input-group">
                        <label>Industria</label>
                        <select id="data-industry">
                            <option value="marketing">Marketing Digital</option>
                            <option value="saas">SaaS / Tech</option>
                            <option value="agencies">Agencias</option>
                            <option value="ecommerce">E-commerce</option>
                        </select>
                    </div>
                    <button class="btn-generate" onclick="generateMagnet('data-authority')">
                        📊 Generar Reporte
                    </button>
                </div>
            </div>
        </div>

        <!-- Output Section -->
        <div id="output-section" class="output-section">
            <div class="output-title">
                <span>📦</span>
                <span>Producción Completa</span>
            </div>

            <div class="agent-status" id="agent-status">
                <div class="agent-badge" id="agent-1">🔍 Market Intel</div>
                <div class="agent-badge" id="agent-2">📝 Product Architect</div>
                <div class="agent-badge" id="agent-3">🎨 Creative Director</div>
                <div class="agent-badge" id="agent-4">✍️ Growth Copywriter</div>
            </div>

            <div class="result-tabs" id="result-tabs">
                <div class="result-tab active" onclick="showTab('research')">Research</div>
                <div class="result-tab" onclick="showTab('content')">Contenido</div>
                <div class="result-tab" onclick="showTab('visual')">Visual</div>
                <div class="result-tab" onclick="showTab('post')">Post LinkedIn</div>
            </div>

            <div id="result-research" class="result-panel active">
                <div class="content-box">
                    <button class="copy-btn" onclick="copyContent('research-content')">Copiar</button>
                    <div class="output-content" id="research-content">Esperando...</div>
                </div>
            </div>

            <div id="result-content" class="result-panel">
                <div class="content-box">
                    <button class="copy-btn" onclick="copyContent('content-content')">Copiar</button>
                    <div class="output-content" id="content-content">Esperando...</div>
                </div>
            </div>

            <div id="result-visual" class="result-panel">
                <div class="image-preview" id="visual-preview">
                    <p>Generando imagen...</p>
                </div>
            </div>

            <div id="result-post" class="result-panel">
                <div class="content-box">
                    <button class="copy-btn" onclick="copyContent('post-content')">Copiar</button>
                    <div class="output-content" id="post-content">Esperando...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedRoute = null;

        function selectRoute(route, element) {
            // Toggle selection
            document.querySelectorAll('.route-card').forEach(card => {
                card.classList.remove('active');
            });
            element.classList.add('active');
            selectedRoute = route;
        }

        function showTab(tab) {
            document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.result-panel').forEach(p => p.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById('result-' + tab).classList.add('active');
        }

        function copyContent(elementId) {
            const content = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(content);
            event.target.innerText = '✓ Copiado';
            setTimeout(() => { event.target.innerText = 'Copiar'; }, 2000);
        }

        function updateAgentStatus(agentNum, status) {
            const badge = document.getElementById('agent-' + agentNum);
            badge.classList.remove('active', 'complete');
            if (status === 'active') badge.classList.add('active');
            if (status === 'complete') badge.classList.add('complete');
        }

        async function generateMagnet(route) {
            const outputSection = document.getElementById('output-section');
            outputSection.classList.add('visible');

            // Reset
            document.querySelectorAll('.agent-badge').forEach(b => b.classList.remove('active', 'complete'));
            document.getElementById('research-content').innerText = 'Procesando...';
            document.getElementById('content-content').innerText = 'Esperando...';
            document.getElementById('visual-preview').innerHTML = '<p>Esperando...</p>';
            document.getElementById('post-content').innerText = 'Esperando...';

            // Get inputs based on route
            let params = { route: route };

            if (route === 'trend-jacker') {
                params.industry = document.getElementById('trend-industry').value;
                params.format = document.getElementById('trend-format').value;
            } else if (route === 'problem-solver') {
                params.pain_point = document.getElementById('problem-pain').value;
                params.format = document.getElementById('problem-format').value;
            } else if (route === 'data-authority') {
                params.topic = document.getElementById('data-topic').value;
                params.industry = document.getElementById('data-industry').value;
            }

            try {
                // Start generation
                updateAgentStatus(1, 'active');

                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(params)
                });

                const data = await response.json();

                if (data.success) {
                    // Update research
                    updateAgentStatus(1, 'complete');
                    document.getElementById('research-content').innerText = JSON.stringify(data.research, null, 2);

                    // Update content
                    updateAgentStatus(2, 'complete');
                    document.getElementById('content-content').innerText = JSON.stringify(data.content, null, 2);

                    // Update visual
                    updateAgentStatus(3, 'complete');
                    if (data.visual && data.visual.image_url) {
                        document.getElementById('visual-preview').innerHTML =
                            '<img src="' + data.visual.image_url + '" alt="Generated Visual">';
                    }

                    // Update post
                    updateAgentStatus(4, 'complete');
                    if (data.post && data.post.post_text) {
                        document.getElementById('post-content').innerText = data.post.post_text;
                    } else {
                        document.getElementById('post-content').innerText = JSON.stringify(data.post, null, 2);
                    }
                } else {
                    document.getElementById('research-content').innerText = 'Error: ' + (data.error || 'Unknown error');
                }
            } catch (error) {
                document.getElementById('research-content').innerText = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
"""


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Dashboard principal."""
    return render_template_string(DASHBOARD_HTML)


@app.route('/health')
def health():
    """Health check."""
    return jsonify({
        "status": "ok",
        "version": "3.0",
        "ai_status": ai_client.get_status(),
        "time": datetime.now().isoformat()
    })


@app.route('/generate', methods=['POST'])
def generate():
    """
    Main generation endpoint.
    Routes to appropriate production pipeline based on selected route.
    """
    try:
        data = request.get_json()
        route = data.get('route')

        if route == 'trend-jacker':
            return trend_jacker_pipeline(data)
        elif route == 'problem-solver':
            return problem_solver_pipeline(data)
        elif route == 'data-authority':
            return data_authority_pipeline(data)
        else:
            return jsonify({"success": False, "error": "Invalid route"})

    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({"success": False, "error": str(e)})


def trend_jacker_pipeline(data: dict) -> dict:
    """
    Route 1: Trend-Jacker Pipeline
    Scans trends and creates timely lead magnets.
    """
    industry = data.get('industry', 'marketing')
    format_type = data.get('format', 'carousel')

    logger.info(f"[TREND-JACKER] Starting pipeline for {industry}")

    # Agent 1: Find trending topics
    logger.info("[Agent 1] Scanning for trends...")
    trending = market_intel.find_trending_topics()

    if not trending:
        return jsonify({"success": False, "error": "No trends found"})

    # Pick top trend
    top_trend = trending[0]
    research = market_intel.research_trend(top_trend['topic'])

    # Agent 2: Create content based on format
    logger.info(f"[Agent 2] Creating {format_type} content...")
    content = product_architect.create_content(format_type, research, title=top_trend['topic'])

    # Agent 3: Create visual
    logger.info("[Agent 3] Generating visual...")
    # Extract title from content based on format type
    title_keys = ['carousel_title', 'guide_title', 'checklist_title', 'cheatsheet_title',
                  'template_title', 'swipefile_title', 'course_title', 'worksheet_title',
                  'toolkit_title', 'case_study_title', 'report_title']
    title = next((content.get(k) for k in title_keys if content.get(k)), top_trend['topic'])

    if format_type == 'carousel':
        visual = creative_director.generate_carousel_cover(title, research.get('trend_summary', ''))
    else:
        visual = creative_director.generate_ebook_cover(title)

    # Agent 4: Write post
    logger.info("[Agent 4] Writing LinkedIn post...")
    post = growth_copywriter.write_linkedin_post(content, research)

    return jsonify({
        "success": True,
        "route": "trend-jacker",
        "research": research,
        "content": content,
        "visual": visual,
        "post": post
    })


def problem_solver_pipeline(data: dict) -> dict:
    """
    Route 2: Problem-Solver Pipeline
    Creates solution-focused lead magnets for specific pain points.
    """
    pain_point = data.get('pain_point', 'No tengo estrategia de marketing')
    format_type = data.get('format', 'guide')

    logger.info(f"[PROBLEM-SOLVER] Starting pipeline for: {pain_point}")

    # Agent 1: Analyze pain point
    logger.info("[Agent 1] Analyzing pain point...")
    research = market_intel.analyze_pain_point(pain_point)

    # Agent 2: Create content based on format
    logger.info(f"[Agent 2] Creating {format_type} solution content...")
    content = product_architect.create_content(format_type, research)

    # Agent 3: Create visual
    logger.info("[Agent 3] Generating visual...")
    # Extract title from content based on format type
    title_keys = ['guide_title', 'checklist_title', 'carousel_title', 'cheatsheet_title',
                  'template_title', 'swipefile_title', 'course_title', 'worksheet_title',
                  'toolkit_title', 'case_study_title']
    title = next((content.get(k) for k in title_keys if content.get(k)), pain_point)

    if format_type == 'carousel':
        visual = creative_director.generate_carousel_cover(title, research.get('pain_analysis', ''))
    else:
        visual = creative_director.generate_ebook_cover(title)

    # Agent 4: Write post
    logger.info("[Agent 4] Writing LinkedIn post...")
    post = growth_copywriter.write_linkedin_post(content, research)

    return jsonify({
        "success": True,
        "route": "problem-solver",
        "research": research,
        "content": content,
        "visual": visual,
        "post": post
    })


def data_authority_pipeline(data: dict) -> dict:
    """
    Route 3: Data-Authority Pipeline
    Creates data-driven reports for authority positioning.
    """
    topic = data.get('topic', 'Estado del Marketing')
    industry = data.get('industry', 'marketing')

    logger.info(f"[DATA-AUTHORITY] Starting pipeline for: {topic} in {industry}")

    # Agent 1: Gather industry stats
    logger.info("[Agent 1] Gathering industry statistics...")
    stats_research = market_intel.gather_industry_stats(industry)

    # Agent 2: Create data report
    logger.info("[Agent 2] Creating data report...")
    content = product_architect.create_data_report(stats_research, topic)

    # Agent 3: Create visual
    logger.info("[Agent 3] Generating infographic hero...")
    visual = creative_director.generate_infographic_hero(
        content.get('report_title', topic),
        stats_research.get('key_stats', [])
    )

    # Agent 4: Write post
    logger.info("[Agent 4] Writing LinkedIn post...")
    post = growth_copywriter.write_linkedin_post(content, stats_research)

    return jsonify({
        "success": True,
        "route": "data-authority",
        "research": stats_research,
        "content": content,
        "visual": visual,
        "post": post
    })


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/trends')
def api_trends():
    """Get current trending topics."""
    trends = market_intel.find_trending_topics()
    return jsonify({"trends": trends})


@app.route('/api/research', methods=['POST'])
def api_research():
    """Research a specific topic."""
    data = request.get_json()
    topic = data.get('topic', '')
    research = market_intel.research_trend(topic)
    return jsonify({"research": research})


@app.route('/api/status')
def api_status():
    """Get current production status."""
    return jsonify(current_production)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'

    print(f"""
========================================
  FastStrat Magnet Factory v3.0
========================================
  Dashboard: http://localhost:{port}
  Health:    http://localhost:{port}/health
  AI Status: {ai_client.get_status()}
========================================
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
