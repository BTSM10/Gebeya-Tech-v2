"""Generates the Gebeya Week 1 Challenge documentation PDF."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

# ── Paths ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
NOTEBOOKS = os.path.join(BASE, 'notebooks')
OUTPUT = os.path.join(BASE, 'Gebeya_Week1_Documentation.pdf')

# ── Colours ───────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor('#1B3A6B')
MID_BLUE    = colors.HexColor('#2E6DB4')
LIGHT_BLUE  = colors.HexColor('#EAF2FB')
ACCENT      = colors.HexColor('#E74C3C')
GREEN       = colors.HexColor('#27AE60')
GREY_LIGHT  = colors.HexColor('#F2F3F4')
GREY_DARK   = colors.HexColor('#566573')
WHITE       = colors.white
BLACK       = colors.black
CODE_BG     = colors.HexColor('#2B2B2B')
CODE_FG     = colors.HexColor('#F8F8F2')

# ── Styles ────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title   = S('CoverTitle',   fontSize=32, textColor=WHITE,  alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=12, leading=40)
cover_sub     = S('CoverSub',     fontSize=16, textColor=LIGHT_BLUE, alignment=TA_CENTER, fontName='Helvetica', spaceAfter=8)
cover_meta    = S('CoverMeta',    fontSize=11, textColor=GREY_LIGHT, alignment=TA_CENTER, fontName='Helvetica')

h1            = S('H1',  fontSize=20, textColor=DARK_BLUE,  fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=8,  leading=26)
h2            = S('H2',  fontSize=15, textColor=MID_BLUE,   fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6,  leading=20)
h3            = S('H3',  fontSize=12, textColor=DARK_BLUE,  fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4,  leading=16)
body          = S('Body', fontSize=10, textColor=BLACK, fontName='Helvetica', spaceAfter=6, leading=16, alignment=TA_JUSTIFY)
body_bullet   = S('Bullet', fontSize=10, textColor=BLACK, fontName='Helvetica', spaceAfter=4, leading=15, leftIndent=16, bulletIndent=4)
note          = S('Note', fontSize=9,  textColor=GREY_DARK, fontName='Helvetica-Oblique', spaceAfter=4, leading=13)
code_style    = S('Code', fontSize=8.5, fontName='Courier', textColor=CODE_FG, backColor=CODE_BG, spaceAfter=8, spaceBefore=4, leading=13, leftIndent=10, rightIndent=10)
caption       = S('Caption', fontSize=8, textColor=GREY_DARK, alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=10)
toc_entry     = S('TOC', fontSize=10, fontName='Helvetica', textColor=DARK_BLUE, spaceAfter=3, leading=14)

# ── Helpers ───────────────────────────────────────────────────
def P(text, style=body):
    return Paragraph(text, style)

def B(text):
    return Paragraph(f'• {text}', body_bullet)

def Code(text):
    escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return Paragraph(escaped, code_style)

def HR():
    return HRFlowable(width='100%', thickness=1, color=MID_BLUE, spaceAfter=8, spaceBefore=8)

def section_header(text):
    return [HR(), P(text, h1), HR()]

def sub_header(text):
    return P(text, h2)

def img(filename, width=14*cm, caption_text=None):
    path = os.path.join(NOTEBOOKS, filename)
    if not os.path.exists(path):
        return []
    items = [Image(path, width=width, height=width*0.6)]
    if caption_text:
        items.append(P(caption_text, caption))
    return items

def info_box(text, bg=LIGHT_BLUE):
    data = [[Paragraph(text, S('ib', fontSize=10, fontName='Helvetica', textColor=DARK_BLUE, leading=15))]]
    t = Table(data, colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX',        (0,0), (-1,-1), 1, MID_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ]))
    return t

def comparison_table(headers, rows):
    data = [headers] + rows
    col_w = [15.5*cm / len(headers)] * len(headers)
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  DARK_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [GREY_LIGHT, WHITE]),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('ALIGN',         (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return t

# ── Page layout ───────────────────────────────────────────────
def cover_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(MID_BLUE)
    canvas.rect(0, h*0.35, w, h*0.65, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h*0.33, w, 6, fill=1, stroke=0)
    canvas.restoreState()

def normal_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, h-1.2*cm, w, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(1*cm, h-0.85*cm, 'Gebeya Week 1 Challenge — Full Documentation')
    canvas.drawRightString(w-1*cm, h-0.85*cm, 'Biniam Tsige')
    canvas.setFillColor(GREY_LIGHT)
    canvas.rect(0, 0, w, 0.9*cm, fill=1, stroke=0)
    canvas.setFillColor(GREY_DARK)
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(w/2, 0.35*cm, f'Page {doc.page}')
    canvas.restoreState()

# ── Build content ─────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title='Gebeya Week 1 Challenge Documentation',
        author='Biniam Tsige'
    )

    story = []

    # ── COVER ─────────────────────────────────────────────────
    story.append(Spacer(1, 5*cm))
    story.append(P('Gebeya Week 1 Challenge', cover_title))
    story.append(P('Full Technical Documentation', cover_sub))
    story.append(Spacer(1, 0.5*cm))
    story.append(P('Slack Messages Analysis Project', cover_sub))
    story.append(Spacer(1, 1.5*cm))
    story.append(P('Biniam Tsige  |  Batch 6  |  2026', cover_meta))
    story.append(P('Data Engineering & Machine Learning Engineering Track', cover_meta))
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ─────────────────────────────────────
    story += section_header('Table of Contents')
    toc_items = [
        ('1.', 'Project Overview'),
        ('2.', 'Environment Setup — Homebrew, pip, venv'),
        ('3.', 'Project Structure'),
        ('4.', 'Task 1 — Git, GitHub & EDA'),
        ('5.', 'Task 2 — Data Science Components & ML'),
        ('6.', 'Task 3 — MongoDB & PostgreSQL'),
        ('7.', 'Task 4 — Streamlit Dashboard'),
        ('8.', 'Task 5 — Docker, AWS & Terraform'),
        ('9.', 'Questions & Answers'),
    ]
    for num, title in toc_items:
        story.append(P(f'<font color="#1B3A6B"><b>{num}</b></font>  {title}', toc_entry))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 1. PROJECT OVERVIEW
    # ══════════════════════════════════════════════════════════
    story += section_header('1. Project Overview')
    story.append(P(
        'The Gebeya Week 1 Challenge is a comprehensive technical assessment covering Data Engineering '
        'and Machine Learning Engineering. The project analyses anonymized Slack messages from '
        'Gebeya Batch 6 — real communication data from a previous cohort of trainees. '
        'The challenge spans five tasks covering everything from basic Python environment setup '
        'to cloud deployment.'
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(sub_header('What is Slack?'))
    story.append(P(
        'Slack is a team messaging platform — similar to WhatsApp but designed for professional use. '
        'One of its key advantages is that all messages can be exported as structured JSON files. '
        'This makes it ideal for data analysis. Each channel (like a group chat) produces one JSON '
        'file per day, containing every message sent that day along with metadata like timestamps, '
        'reactions, and thread replies.'
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(sub_header('The Five Tasks'))
    story.append(comparison_table(
        ['Task', 'Topic', 'Key Technologies'],
        [
            ['Task 1', 'Git, GitHub, EDA & Statistics', 'Python, pandas, matplotlib, Jupyter'],
            ['Task 2', 'Data Science Components & ML', 'scikit-learn, TextBlob, MLFlow, NLTK'],
            ['Task 3', 'Databases', 'MongoDB, PostgreSQL, pymongo, psycopg2'],
            ['Task 4', 'Dashboard', 'Streamlit'],
            ['Task 5', 'Deployment', 'Docker, AWS, Terraform, GitHub Actions'],
        ]
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(info_box(
        '🔒 Data Privacy: The anonymized Slack data must NEVER be pushed to GitHub. '
        'The anonymized/ folder is added to .gitignore to prevent accidental uploads. '
        'This complies with Gebeya\'s data privacy and confidentiality requirements.'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 2. ENVIRONMENT SETUP
    # ══════════════════════════════════════════════════════════
    story += section_header('2. Environment Setup')

    story.append(sub_header('What is Homebrew?'))
    story.append(P(
        'Homebrew is a package manager for Mac — think of it as the App Store for developer tools '
        'that run in the terminal. Instead of going to a website, downloading an installer, and '
        'clicking through setup screens, you simply type one command and Homebrew handles everything.'
    ))
    story.append(Code('brew install mongodb-community   # installs MongoDB\nbrew install terraform           # installs Terraform\nbrew install gh                  # installs GitHub CLI'))
    story.append(P('Homebrew installs everything into <b>/opt/homebrew/</b> on Apple Silicon Macs. You can list everything installed via Homebrew with:'))
    story.append(Code('brew list              # list all installed tools\nbrew list --versions   # list with version numbers\nbrew info postgresql   # info about one specific tool'))

    story.append(sub_header('What is pip?'))
    story.append(P(
        'pip is Python\'s package manager — it installs Python libraries (code that runs inside Python). '
        'While Homebrew installs programs on your Mac, pip installs libraries that your Python code imports.'
    ))
    story.append(Code('pip install pandas          # installs pandas\npip install scikit-learn    # installs scikit-learn\npip list                    # list all installed packages\npip show pandas             # info about one package'))

    story.append(sub_header('Homebrew vs pip'))
    story.append(comparison_table(
        ['', 'Homebrew', 'pip'],
        [
            ['What it installs', 'Programs & system tools', 'Python libraries'],
            ['Where it goes', '/opt/homebrew/', 'Inside venv/'],
            ['Who uses it', 'Your whole Mac', 'Only Python code'],
            ['Example', 'MongoDB, PostgreSQL, Docker', 'pandas, mlflow, nltk'],
            ['List command', 'brew list', 'pip list'],
        ]
    ))

    story.append(sub_header('What is a Virtual Environment (venv)?'))
    story.append(P(
        'A virtual environment is an isolated Python workspace — a folder that contains its own '
        'Python interpreter and packages, completely separate from your system Python. '
        'This solves the problem of different projects needing different versions of the same package.'
    ))
    story.append(P('<b>Real life analogy:</b> Imagine you work on two different projects. Project A needs '
        'pandas version 1.0 and Project B needs pandas version 2.0. Without venvs, they would conflict. '
        'With venvs, each project has its own isolated environment — like two separate toolboxes.'
    ))
    story.append(Code('# Create the virtual environment\npython3 -m venv gebvenv\n\n# Activate it (you must do this every new terminal session)\nsource gebvenv/bin/activate\n\n# You know it\'s active when you see (gebvenv) in your prompt:\n# (gebvenv) btsm@Biniams-MacBook-Pro Gebeya-Tech %\n\n# Install packages inside the venv\npip install pandas matplotlib seaborn jupyter'))
    story.append(P('The venv folder (<b>gebvenv/</b>) is disposable. If it breaks, delete it and recreate it. '
        'Your notebooks and source code live outside it and are safe.'))

    story.append(sub_header('Registering venv as a Jupyter Kernel'))
    story.append(P(
        'When Jupyter opens a notebook, it uses a "kernel" — the Python engine that runs the code. '
        'By default Jupyter uses the system Python, which does not have your venv packages. '
        'You must register your venv as a kernel so notebooks can use it.'
    ))
    story.append(Code('source gebvenv/bin/activate\npip install ipykernel\npython -m ipykernel install --user --name=gebvenv --display-name="Python (gebvenv)"'))
    story.append(P('Then in Jupyter: <b>Kernel → Change Kernel → Python (gebvenv)</b>'))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 3. PROJECT STRUCTURE
    # ══════════════════════════════════════════════════════════
    story += section_header('3. Project Structure')
    story.append(Code(
        'Gebeya-Tech/\n'
        '├── .github/workflows/      ← GitHub Actions CI/CD workflows\n'
        '│   ├── flake8_check.yml    ← checks code style on every push\n'
        '│   ├── unittests.yml       ← runs pytest on every push\n'
        '│   └── docstring_tests.yml ← runs docstring tests on every push\n'
        '├── .vscode/settings.json   ← VSCode Flake8 configuration\n'
        '├── app/\n'
        '│   └── dashboard.py        ← Streamlit dashboard (Task 4)\n'
        '├── notebooks/\n'
        '│   ├── parse_slack_data.ipynb   ← Task 1 EDA notebook\n'
        '│   ├── task2_analysis.ipynb     ← Task 2 ML notebook\n'
        '│   └── task3_databases.ipynb    ← Task 3 databases notebook\n'
        '├── src/\n'
        '│   ├── __init__.py         ← marks src as a Python package\n'
        '│   ├── config.py           ← stores path to data folder\n'
        '│   ├── loader.py           ← SlackDataLoader class\n'
        '│   └── utils.py            ← helper functions\n'
        '├── tests/\n'
        '│   ├── __init__.py\n'
        '│   └── test_loader.py      ← 5 unit tests for SlackDataLoader\n'
        '├── .flake8                 ← code style configuration\n'
        '├── .gitignore              ← prevents data from going to GitHub\n'
        '├── gebvenv/                ← virtual environment (not pushed to GitHub)\n'
        '├── Makefile                ← shortcuts: make test, make lint\n'
        '├── requirements.txt        ← list of Python packages\n'
        '└── README.md               ← project description'
    ))

    story.append(sub_header('Key File Explanations'))
    story.append(P('<b>src/config.py</b> — stores the path to the anonymized data folder so every file knows where to find it without hardcoding a path.'))
    story.append(Code('import os\nDATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "anonymized")'))

    story.append(P('<b>src/loader.py</b> — the SlackDataLoader class with 3 methods:'))
    story.append(B('get_channels() — lists all 39 channel folders'))
    story.append(B('load_channel(channel) — reads all JSON files from one channel into a DataFrame'))
    story.append(B('load_all_channels() — combines all channels into one DataFrame (20,011 messages)'))

    story.append(P('<b>src/utils.py</b> — helper functions used across all notebooks:'))
    story.append(B('get_top_users() — ranks users from most to least by a metric'))
    story.append(B('get_bottom_users() — ranks users from least to most by a metric'))
    story.append(B('parse_timestamp() — converts Slack\'s Unix timestamp (1661774400.0) to a real datetime'))
    story.append(B('add_time_columns() — adds datetime, date, and hour columns to any DataFrame'))

    story.append(Spacer(1, 0.3*cm))
    story.append(info_box(
        '📝 Why utils.py? These functions are used in multiple notebooks. Instead of copying '
        'the same code into every notebook, we write it once and import it wherever needed. '
        'If we fix a bug in utils.py, all notebooks automatically get the fix.'
    ))

    story.append(sub_header('What is __pycache__?'))
    story.append(P(
        'When Python runs a .py file, it compiles it into faster bytecode and saves it in __pycache__/ '
        'as .pyc files. The next time you run the same file, Python loads the faster bytecode version. '
        'You never create or edit this folder — Python manages it automatically. '
        'It is excluded from GitHub via .gitignore.'
    ))
    story.append(P(
        '<b>Does this make Python a compiled language?</b> Not quite. Python compiles to bytecode '
        'automatically behind the scenes, but that bytecode still needs the Python interpreter to run. '
        'A fully compiled language (like C) runs directly on the CPU with no interpreter needed. '
        'Python is called "compiled to bytecode, then interpreted."'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 4. TASK 1
    # ══════════════════════════════════════════════════════════
    story += section_header('4. Task 1 — Git, GitHub & EDA')

    story.append(sub_header('What is Git?'))
    story.append(P(
        'Git is a version control system — it tracks every change you make to your code over time. '
        'Think of it like "track changes" in Microsoft Word, but for entire projects. '
        'You can go back to any previous version of your code at any time.'
    ))
    story.append(sub_header('What is GitHub?'))
    story.append(P(
        'GitHub is a website that stores your Git repository online. Git lives on your local machine; '
        'GitHub is the cloud backup and collaboration platform. Other developers can see your code, '
        'suggest changes, and contribute.'
    ))
    story.append(sub_header('What is Flake8?'))
    story.append(P(
        'Flake8 is a code style checker. It reads your Python code and flags anything that violates '
        'PEP 8 — Python\'s official style guide. Bad code (to Flake8) means: lines too long, '
        'missing spaces around operators, unused imports, inconsistent indentation etc. '
        'It does not check whether your code works — only whether it is formatted correctly.'
    ))
    story.append(sub_header('What is CI/CD?'))
    story.append(P(
        'CI/CD stands for Continuous Integration / Continuous Deployment. It is the practice of '
        'automatically running checks every time you push code to GitHub. In this project, three '
        'GitHub Actions workflows run automatically on every push:'
    ))
    story.append(B('flake8_check.yml — checks code style'))
    story.append(B('unittests.yml — runs all pytest tests'))
    story.append(B('docstring_tests.yml — runs examples in docstrings as tests'))

    story.append(sub_header('EDA Analysis — Questions Answered'))
    story.append(P('<b>Top & Bottom 10 Users</b> — We analysed users by 4 metrics: message count (how many messages they sent), reply count (how many replies they received), reaction count (how many emoji reactions their messages got), and mention count (how many times others @mentioned them).'))
    story.append(P('<b>Top 10 Messages</b> — Found the most replied-to, most reacted-to, and most mentioned messages.'))
    story.append(P('<b>Channel Activity Scatter Plot</b> — Plotted all 39 channels on a 2D chart where X = number of messages, Y = replies + reactions. The channel in the top-right corner is the most active.'))
    story.append(P('<b>Reply Time Analysis</b> — Calculated what fraction of messages receive a reply within 5 minutes. Plotted a scatter plot with X = time difference, Y = time of day, colour = channel.'))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 5. TASK 2
    # ══════════════════════════════════════════════════════════
    story += section_header('5. Task 2 — Data Science Components & ML')

    story.append(sub_header('Unit Tests'))
    story.append(P(
        'A unit test is a small piece of code that checks whether another piece of code works correctly. '
        'We wrote 5 tests for the SlackDataLoader class:'
    ))
    story.append(B('test_load_channel_returns_dataframe — confirms the return type is a DataFrame'))
    story.append(B('test_load_channel_has_expected_columns — confirms columns: type, user, text, ts, channel'))
    story.append(B('test_load_all_channels_returns_dataframe — same for all-channel loading'))
    story.append(B('test_load_all_channels_has_expected_columns — same column check for all channels'))
    story.append(B('test_channel_column_matches_channel_name — every row has the correct channel label'))
    story.append(Code('python -m pytest tests/test_loader.py -v\n# Result: 5 passed in 27.96s'))

    story.append(sub_header('Time Difference Histograms'))
    story.append(P(
        'We analysed the distribution of time gaps between consecutive events. '
        'A histogram is a bar chart that groups data into buckets (e.g. "how many gaps were 0–5 minutes?"). '
        'We computed 4 distributions: consecutive messages, consecutive replies, '
        'consecutive reactions, and all events combined. Each chart shows a red median line.'
    ))
    story += img('time_diff_histograms.png', caption_text='Figure 1: Time difference distributions between consecutive events')

    story.append(sub_header('Message Classification'))
    story.append(P(
        'Every message was classified into one of 6 categories using rule-based heuristics '
        '(since no labeled training data exists): Question-Technical, Question-NonTechnical, '
        'Answer, Comment-Technical, Comment-NonTechnical, Other. '
        'Technical keywords included: error, code, python, git, model, docker, sql, pandas, etc.'
    ))
    story += img('message_classification.png', caption_text='Figure 2: Distribution of message types across all channels')

    story.append(sub_header('Topic Modelling (LDA)'))
    story.append(P(
        'Topic modelling automatically discovers hidden themes in thousands of documents without '
        'being told what the themes are. We used LDA — Latent Dirichlet Allocation. '
        'The idea: every message is a mixture of topics, every topic is a mixture of words. '
        'LDA works backwards from the words to figure out the topics. We found 10 topics.'
    ))
    story.append(P(
        'Steps: clean text (remove Slack mentions, URLs, stop words), build a word-count matrix '
        'of top 2,000 words using CountVectorizer, train LDA with 10 topics, visualise results.'
    ))
    story.append(P(
        '<b>Why do topics look messy?</b> LDA works best on long formal documents like news articles. '
        'Slack messages are short, informal, and full of slang — so topic boundaries are less clean. '
        'This is expected and should be mentioned in your report.'
    ))
    story += img('topic_modelling.png', caption_text='Figure 3: Top 10 LDA topics extracted from 20,000 Slack messages')

    story.append(sub_header('Sentiment Analysis Over Time'))
    story.append(P(
        'Sentiment analysis measures the emotional tone of text — is it positive, negative, or neutral? '
        'TextBlob gives every piece of text a polarity score from -1 (very negative) to +1 (very positive). '
        'It works by looking up words in a pre-built dictionary where every word has a sentiment score.'
    ))
    story.append(P(
        'We grouped all messages by day since training start, merged them into one big text per day, '
        'ran TextBlob on each day\'s text, and plotted the results. Green bars = positive days, '
        'red bars = negative days, blue line = smoothed trend using Savitzky-Golay filter.'
    ))
    story += img('sentiment_over_time.png', caption_text='Figure 4: Sentiment polarity of Slack messages over time')

    story.append(sub_header('MLFlow — Model Versioning'))
    story.append(P(
        'MLFlow tracks your machine learning experiments — like a lab notebook for ML. '
        'Every time you train a model, MLFlow records parameters, metrics, the model itself, '
        'and any artefacts (files). This is critical in real ML work where you train dozens of '
        'models with different settings and need to track which gave the best result.'
    ))
    story.append(comparison_table(
        ['Logged Item', 'Value'],
        [
            ['n_topics', '10'],
            ['max_iter', '20'],
            ['vocab_size', '2,000'],
            ['corpus_size', '~18,000 documents'],
            ['LDA perplexity', 'Computed after training'],
            ['Mean sentiment', 'Computed from daily data'],
            ['Model artefact', 'Trained LDA model (sklearn format)'],
            ['Vectorizer artefact', 'CountVectorizer saved as .pkl'],
        ]
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(sub_header('MLOps Components Summary'))
    story.append(comparison_table(
        ['Component', 'What it does', 'Tool'],
        [
            ['Experiment Tracking', 'Logs params, metrics, artefacts per run', 'MLFlow'],
            ['Feature Store', 'Central storage for ML features', 'PostgreSQL (Task 3)'],
            ['Model Versioning', 'Tags models with version and stage', 'MLFlow Model Registry'],
            ['Model Monitoring', 'Detects when deployed models degrade', 'MLwatcher / custom'],
            ['CI/CD Pipeline', 'Auto-tests code on every push', 'GitHub Actions'],
            ['Containerisation', 'Packages app + dependencies', 'Docker (Task 5)'],
        ]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 6. TASK 3
    # ══════════════════════════════════════════════════════════
    story += section_header('6. Task 3 — MongoDB & PostgreSQL')

    story.append(sub_header('Why Two Databases?'))
    story.append(P(
        'MongoDB and PostgreSQL solve completely different problems. Using only one would be '
        'the wrong tool for the job.'
    ))
    story.append(comparison_table(
        ['', 'MongoDB (NoSQL)', 'PostgreSQL (SQL)'],
        [
            ['Data structure', 'Documents (JSON-like)', 'Tables with fixed columns'],
            ['Schema', 'Flexible — each document can differ', 'Rigid — all rows same structure'],
            ['Best for', 'Raw, messy, unpredictable data', 'Clean, structured, computed data'],
            ['Our use', 'Raw Slack JSON messages', 'Computed ML features'],
            ['Analogy', 'Filing cabinet (any folder shape)', 'Spreadsheet (strict columns)'],
        ]
    ))

    story.append(sub_header('Installing MongoDB'))
    story.append(Code(
        '# Add the MongoDB source to Homebrew\nbrew tap mongodb/brew\n\n'
        '# Install MongoDB\nbrew install mongodb-community\n\n'
        '# Start the MongoDB server\nbrew services start mongodb-community\n\n'
        '# Verify it is running\nbrew services list'
    ))
    story.append(P('MongoDB runs on <b>localhost:27017</b> — localhost means "this same computer", 27017 is the port (door number) MongoDB listens on.'))

    story.append(sub_header('MongoDB Schema Design — 3 Collections'))
    story.append(P(
        'A collection in MongoDB is like a table in SQL — a group of related documents. '
        'We split the Slack data into 3 collections for query speed and streaming efficiency:'
    ))
    story.append(B('<b>messages</b> — 10,814 top-level messages'))
    story.append(B('<b>replies</b> — 8,788 thread replies, each linked to its parent message'))
    story.append(B('<b>reactions</b> — 4,842 emoji reactions, each linked to its message'))
    story.append(P(
        '<b>Why split into 3?</b> If you want to count reactions, you query only the reactions '
        'collection — you do not load all messages. In a real-time system, new reactions can be '
        'inserted without touching the original message at all.'
    ))

    story.append(sub_header('What is an Index?'))
    story.append(P(
        'An index in a database is like the index at the back of a book. Instead of reading every '
        'page to find a term, you go to the index and it tells you exactly which pages to look at. '
        'Without an index, finding all messages from "all-week1" means scanning all 10,814 documents. '
        'With an index on channel, MongoDB jumps directly to the right documents.'
    ))
    story.append(P(
        '<b>Should you index everything?</b> No. Every index has two costs: storage space and '
        'slower writes (every insert must update all indexes). Index only fields you search or '
        'sort by frequently. We indexed: channel, user, ts, and parent_message_id.'
    ))

    story.append(sub_header('PostgreSQL Schema Design — 3 Tables'))
    story.append(comparison_table(
        ['Table', 'Rows', 'What it stores'],
        [
            ['message_features', '19,602', 'Per-message ML features: sentiment, type, hour, day'],
            ['user_features', '1,205', 'Per-user stats: message count, reply count, dominant type'],
            ['daily_sentiment', '104', 'Per-day sentiment score and message count'],
        ]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(P('<b>Key SQL data types used:</b>'))
    story.append(B('SERIAL PRIMARY KEY — auto-generates unique ID for every row'))
    story.append(B('TEXT — stores any length of text'))
    story.append(B('FLOAT — stores decimal numbers (e.g. 0.342 for sentiment)'))
    story.append(B('INTEGER — stores whole numbers'))
    story.append(B('NOT NULL — this column must always have a value'))
    story.append(B('TIMESTAMP DEFAULT NOW() — auto-records the exact insert time'))

    story.append(sub_header('Installing Python Drivers'))
    story.append(Code(
        '# Install Python library to talk to MongoDB\npip install pymongo\n\n'
        '# Install Python library to talk to PostgreSQL\npip install psycopg2-binary'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 7. TASK 4
    # ══════════════════════════════════════════════════════════
    story += section_header('7. Task 4 — Streamlit Dashboard')

    story.append(sub_header('What is Streamlit?'))
    story.append(P(
        'Streamlit is a Python library that turns your Python code into an interactive web app — '
        'with charts, tables, dropdowns, sliders — without needing to know HTML, CSS, or JavaScript. '
        'You write Python, it gives you a website.'
    ))
    story.append(Code(
        'pip install streamlit\n\n'
        '# Run the dashboard\nstreamlit run app/dashboard.py\n\n'
        '# Opens automatically at http://localhost:8501'
    ))

    story.append(sub_header('Dashboard Sections'))
    story.append(B('<b>Sidebar</b> — Channel filter dropdown, live stats (messages, channels, users)'))
    story.append(B('<b>Key Metrics</b> — 4 boxes: total messages, channels, unique users, total reactions'))
    story.append(B('<b>Top & Bottom Users</b> — Tabs for messages, replies, reactions, mentions'))
    story.append(B('<b>Channel Activity</b> — Scatter plot with top 5 channels labelled'))
    story.append(B('<b>Message Classification</b> — Bar chart + pie chart side by side'))
    story.append(B('<b>ML Analysis Results</b> — Time diff histograms, topic model, sentiment charts'))
    story.append(B('<b>Raw Data Explorer</b> — Scrollable table with a row-count slider'))

    story.append(Spacer(1, 0.3*cm))
    story.append(info_box(
        '💡 The "Filter by channel" dropdown in the sidebar is interactive. '
        'Selecting a specific channel updates the entire dashboard to show only that channel\'s data. '
        'User IDs appear as U03V1AM5TF... because the data is anonymized.'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 8. TASK 5 — DOCKER, AWS, TERRAFORM
    # ══════════════════════════════════════════════════════════
    story += section_header('8. Task 5 — Docker, AWS & Terraform')

    story.append(sub_header('Docker'))
    story.append(P(
        'Docker packages your entire application — the code, Python version, all packages, '
        'all settings — into one single box called a container. That container runs identically '
        'on any computer in the world. This solves the "works on my machine" problem permanently.'
    ))
    story.append(P(
        '<b>Real life analogy:</b> Before shipping containers existed, loading a cargo ship was chaos — '
        'boxes of different shapes, fragile items mixed with heavy ones. After shipping containers, '
        'everything goes into a standard metal box. The ship doesn\'t care what\'s inside. '
        'Docker does exactly that for software.'
    ))
    story.append(comparison_table(
        ['Concept', 'What it means'],
        [
            ['Image', 'Blueprint of your app — read-only snapshot of code + packages'],
            ['Container', 'A running instance of an image (like a meal from a recipe)'],
            ['Dockerfile', 'Instructions file for building your image'],
            ['Docker Hub', 'Website to store and share images (like GitHub for Docker)'],
        ]
    ))
    story.append(Code(
        '# Example Dockerfile\nFROM python:3.11\nCOPY . /app\nWORKDIR /app\n'
        'RUN pip install -r requirements.txt\nCMD ["streamlit", "run", "app/dashboard.py"]'
    ))
    story.append(P('<b>Docker workflow:</b>'))
    story.append(Code(
        'docker build -t gebeya-dashboard .   # build image from Dockerfile\n'
        'docker run -p 8501:8501 gebeya-dashboard  # run a container\n'
        'docker push btsm/gebeya-dashboard    # upload to Docker Hub'
    ))

    story.append(sub_header('AWS (Amazon Web Services)'))
    story.append(P(
        'AWS is Amazon\'s cloud computing platform. Instead of buying a physical server, '
        'you rent computing power from Amazon\'s data centres and pay only for what you use.'
    ))
    story.append(P(
        '<b>Real life analogy:</b> Buying your own server = buying a generator. '
        'Using AWS = using the electricity grid. You pay only for what you use, '
        'someone else maintains the infrastructure.'
    ))
    story.append(comparison_table(
        ['AWS Service', 'What it does', 'Our use case'],
        [
            ['EC2', 'Virtual servers (rent a computer by the hour)', 'Run the Streamlit dashboard'],
            ['S3', 'File storage in the cloud', 'Store the anonymized Slack data privately'],
            ['RDS', 'Managed PostgreSQL/MySQL', 'Host PostgreSQL in the cloud'],
            ['Lambda', 'Serverless functions (no server to manage)', 'Run small Python jobs on trigger'],
            ['ECR', 'Private Docker image registry', 'Store our Docker images on AWS'],
        ]
    ))
    story.append(P(
        '<b>Why AWS matters:</b> Currently the Streamlit dashboard only runs on your Mac. '
        'If you close the terminal, it stops. Deploying to AWS means it runs 24/7 on Amazon\'s '
        'servers, anyone with the URL can access it, and it scales automatically with traffic.'
    ))

    story.append(sub_header('Terraform'))
    story.append(P(
        'Terraform lets you create and manage cloud infrastructure by writing code instead of '
        'clicking through websites. This is called Infrastructure as Code (IaC).'
    ))
    story.append(P(
        '<b>Real life analogy:</b> Think of building an IKEA bookshelf. Without Terraform = someone '
        'describes it to you verbally, you build from memory. With Terraform = you have the official '
        'IKEA instruction manual. Anyone can follow it and build the exact same shelf anywhere.'
    ))
    story.append(Code(
        '# Example Terraform script (hello world for AWS)\nprovider "aws" {\n  region = "us-east-1"\n}\n\n'
        'resource "aws_instance" "web_server" {\n  ami           = "ami-0c55b159cbfafe1f0"\n'
        '  instance_type = "t2.micro"\n\n  tags = {\n    Name = "Gebeya-Dashboard-Server"\n  }\n}'
    ))
    story.append(Code(
        'terraform init     # download required plugins\n'
        'terraform plan     # preview what will be created (nothing happens yet)\n'
        'terraform apply    # create the infrastructure on AWS\n'
        'terraform destroy  # delete everything'
    ))

    story.append(sub_header('How Docker, AWS & Terraform Work Together'))
    story.append(Code(
        'You write code on your Mac\n'
        '         ↓\n'
        'Docker builds an image of your app\n'
        '         ↓\n'
        'GitHub Actions pushes the image to Docker Hub automatically\n'
        '         ↓\n'
        'Terraform creates an EC2 server on AWS\n'
        '         ↓\n'
        'The EC2 server pulls your Docker image\n'
        '         ↓\n'
        'Your Streamlit dashboard is live on the internet 24/7'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 9. Q&A
    # ══════════════════════════════════════════════════════════
    story += section_header('9. Questions & Answers')

    qas = [
        ('What is a Jupyter Notebook?',
         'A Jupyter notebook is an interactive document that mixes code, text, charts, and outputs in one file (.ipynb). '
         'You write code in cells and run them one by one. The output (charts, tables, text) appears directly below each cell. '
         'It is saved as a JSON file — when you press Ctrl+S, it saves the code AND the outputs (including charts embedded as images).'),

        ('What is a pandas DataFrame?',
         'A DataFrame is a table — rows and columns, like an Excel spreadsheet but in Python. '
         'Each column has a name and a data type. You can filter, sort, group, and compute on it very efficiently. '
         'In this project, every message becomes one row in a DataFrame.'),

        ('What is a Slack Unix timestamp?',
         'Slack stores message times as a Unix timestamp — the number of seconds since January 1st 1970 (called "the epoch"). '
         'For example, 1661774400.0 means "1,661,774,400 seconds after January 1st 1970" = August 29th 2022. '
         'The parse_timestamp() function in utils.py converts this to a readable datetime.'),

        ('What are stop words?',
         'Stop words are common English words that carry no useful meaning for analysis: the, is, a, and, to, of, etc. '
         'We remove them before topic modelling so the algorithm focuses on meaningful words. '
         'The NLTK library provides a pre-built list of English stop words.'),

        ('What is the difference between supervised and unsupervised learning?',
         'Supervised learning: you have labeled data (e.g. 1000 messages already tagged as Question/Comment/Answer) '
         'and train a model to predict labels for new data. '
         'Unsupervised learning: no labels exist. The model finds patterns on its own. '
         'LDA topic modelling is unsupervised — we did not tell it what the topics should be.'),

        ('Why do topics look random (hello, guys, please, error)?',
         'LDA works best on long formal documents like news articles or research papers. '
         'Slack messages are short, informal, full of emojis and slang. '
         'The topics are messier as a result. Also, names that appear frequently (like Stephanie) '
         'get treated as topic keywords. This is expected and should be noted in your report.'),

        ('What is sentiment polarity?',
         'Polarity is a number from -1 to +1 measuring how positive or negative text is. '
         '+1 = very positive ("This is amazing, I love it!"), -1 = very negative ("Terrible, never again"), '
         '0 = neutral ("Here is the link"). TextBlob calculates this by looking up each word in a '
         'pre-built dictionary where every word already has a polarity score.'),

        ('What is the difference between MongoDB and PostgreSQL?',
         'MongoDB stores documents (flexible JSON-like objects — each can have different fields). '
         'PostgreSQL stores rows in tables (rigid — every row must have the same columns). '
         'MongoDB is best for raw unpredictable data. PostgreSQL is best for structured computed data. '
         'We used MongoDB for raw Slack messages and PostgreSQL for our computed ML features.'),

        ('What is an index in a database?',
         'An index is like the index at the back of a book — instead of scanning every page, '
         'you jump directly to what you need. Without an index, MongoDB scans all 10,814 messages '
         'to find ones from "all-week1". With an index on channel, it jumps directly. '
         'You should NOT index everything — every index slows down writes and uses disk space.'),

        ('What is Streamlit?',
         'Streamlit is a Python library that converts Python scripts into interactive web apps. '
         'You write Python code using Streamlit functions (st.title, st.chart, st.selectbox) and '
         'it automatically renders as a website. No HTML, CSS, or JavaScript knowledge needed.'),

        ('What is the difference between Docker image and container?',
         'An image is the blueprint — a read-only snapshot of your app and everything it needs (like a recipe). '
         'A container is a running instance of that image (like the actual meal made from the recipe). '
         'You can run 10 containers from one image simultaneously.'),

        ('What is Infrastructure as Code (IaC)?',
         'IaC means treating your cloud infrastructure the same way you treat your application code — '
         'writing it in files, version controlling it with Git, and applying it automatically. '
         'Instead of clicking through the AWS website to create servers, you describe them in .tf files '
         'and run terraform apply. Terraform then creates exactly what you described.'),
    ]

    for question, answer in qas:
        story.append(KeepTogether([
            P(f'<b>Q: {question}</b>', h3),
            P(answer),
            Spacer(1, 0.2*cm),
        ]))

    story.append(PageBreak())

    # ── Final page ────────────────────────────────────────────
    story += section_header('Summary')
    story.append(comparison_table(
        ['Task', 'Status', 'Key Deliverable'],
        [
            ['Task 1', 'Complete', 'EDA notebook — 6 analysis sections, all questions answered'],
            ['Task 2', 'Complete', 'ML notebook — classification, LDA, sentiment, MLFlow'],
            ['Task 3', 'Complete', 'MongoDB (3 collections) + PostgreSQL (3 tables)'],
            ['Task 4', 'Complete', 'Streamlit dashboard with 7 interactive sections'],
            ['Task 5', 'In Progress', 'Docker + Terraform + GitHub Actions'],
            ['GitHub Push', 'Pending', 'Waiting for mentor guidance: personal vs company repo'],
        ]
    ))
    story.append(Spacer(1, 1*cm))
    story.append(P('End of Document', S('end', fontSize=10, textColor=GREY_DARK, alignment=TA_CENTER)))

    # ── Build ─────────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=cover_page,
        onLaterPages=normal_page
    )
    print(f'PDF saved to: {OUTPUT}')


if __name__ == '__main__':
    build()
