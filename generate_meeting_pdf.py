"""Generates a mentor meeting PDF summarising Week 1 work."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table,
    TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

BASE = os.path.dirname(os.path.abspath(__file__))
NOTEBOOKS = os.path.join(BASE, 'notebooks')
OUTPUT = os.path.join(BASE, 'Gebeya_Week1_MeetingReport.pdf')

# ── Colours ───────────────────────────────────────────────────
DARK_BLUE  = colors.HexColor('#1B3A6B')
MID_BLUE   = colors.HexColor('#2E6DB4')
LIGHT_BLUE = colors.HexColor('#EAF2FB')
GREEN      = colors.HexColor('#1E8449')
LIGHT_GREEN = colors.HexColor('#EAFAF1')
ORANGE     = colors.HexColor('#D35400')
LIGHT_ORANGE = colors.HexColor('#FEF9E7')
RED        = colors.HexColor('#C0392B')
GREY_LIGHT = colors.HexColor('#F2F3F4')
GREY_DARK  = colors.HexColor('#566573')
WHITE      = colors.white
BLACK      = colors.black

# ── Styles ────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S('CT', fontSize=34, textColor=WHITE,
                alignment=TA_CENTER, fontName='Helvetica-Bold',
                spaceAfter=10, leading=42)
cover_sub   = S('CS', fontSize=16, textColor=colors.HexColor('#AED6F1'),
                alignment=TA_CENTER, fontName='Helvetica', spaceAfter=6)
cover_meta  = S('CM', fontSize=11, textColor=colors.HexColor('#D5D8DC'),
                alignment=TA_CENTER, fontName='Helvetica')

h1    = S('H1', fontSize=18, textColor=DARK_BLUE, fontName='Helvetica-Bold',
          spaceBefore=16, spaceAfter=6, leading=24)
h2    = S('H2', fontSize=13, textColor=MID_BLUE, fontName='Helvetica-Bold',
          spaceBefore=12, spaceAfter=4, leading=18)
h3    = S('H3', fontSize=11, textColor=DARK_BLUE, fontName='Helvetica-Bold',
          spaceBefore=8, spaceAfter=3, leading=15)
body  = S('BD', fontSize=10, textColor=BLACK, fontName='Helvetica',
          spaceAfter=5, leading=16, alignment=TA_JUSTIFY)
bullet = S('BL', fontSize=10, textColor=BLACK, fontName='Helvetica',
           spaceAfter=3, leading=15, leftIndent=14, bulletIndent=4)
note  = S('NT', fontSize=9, textColor=GREY_DARK, fontName='Helvetica-Oblique',
          spaceAfter=4, leading=13)
cap   = S('CA', fontSize=8, textColor=GREY_DARK, alignment=TA_CENTER,
          fontName='Helvetica-Oblique', spaceAfter=8)
code  = S('CD', fontSize=8.5, fontName='Courier',
          textColor=colors.HexColor('#F8F8F2'),
          backColor=colors.HexColor('#2B2B2B'),
          spaceAfter=6, spaceBefore=4, leading=13,
          leftIndent=8, rightIndent=8)
label_done    = S('LD', fontSize=10, textColor=GREEN,
                  fontName='Helvetica-Bold', alignment=TA_CENTER)
label_pending = S('LP', fontSize=10, textColor=ORANGE,
                  fontName='Helvetica-Bold', alignment=TA_CENTER)


def P(text, style=body):
    return Paragraph(text, style)


def B(text):
    return Paragraph(f'• {text}', bullet)


def HR():
    return HRFlowable(width='100%', thickness=1,
                      color=MID_BLUE, spaceAfter=6, spaceBefore=6)


def box(text, bg=LIGHT_BLUE, border=MID_BLUE, ts=body):
    data = [[Paragraph(text, ts)]]
    t = Table(data, colWidths=[16*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), bg),
        ('BOX',           (0, 0), (-1, -1), 1, border),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return t


def why_box(text):
    return box(f'<b>Why:</b> {text}', bg=LIGHT_GREEN, border=GREEN)


def result_box(text):
    return box(f'<b>Result:</b> {text}', bg=LIGHT_BLUE, border=MID_BLUE)


def pending_box(text):
    return box(f'<b>Pending:</b> {text}', bg=LIGHT_ORANGE, border=ORANGE)


def tbl(headers, rows, col_w=None):
    data = [headers] + rows
    if col_w is None:
        col_w = [16*cm / len(headers)] * len(headers)
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  DARK_BLUE),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  WHITE),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [GREY_LIGHT, WHITE]),
        ('GRID',          (0, 0), (-1, -1), 0.5,
         colors.HexColor('#BDC3C7')),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


def img(filename, width=14*cm, cap_text=None):
    path = os.path.join(NOTEBOOKS, filename)
    if not os.path.exists(path):
        return []
    items = [
        Spacer(1, 0.2*cm),
        Image(path, width=width, height=width * 0.58),
    ]
    if cap_text:
        items.append(P(cap_text, cap))
    items.append(Spacer(1, 0.2*cm))
    return items


def task_header(number, title, status='COMPLETE'):
    colour = GREEN if status == 'COMPLETE' else ORANGE
    status_style = label_done if status == 'COMPLETE' else label_pending
    data = [[
        Paragraph(f'Task {number}', S('th1', fontSize=13,
                                      textColor=WHITE,
                                      fontName='Helvetica-Bold',
                                      alignment=TA_CENTER)),
        Paragraph(title, S('th2', fontSize=13,
                           textColor=WHITE,
                           fontName='Helvetica-Bold')),
        Paragraph(f'● {status}', S('th3', fontSize=10,
                                   textColor=colour,
                                   fontName='Helvetica-Bold',
                                   alignment=TA_CENTER)),
    ]]
    t = Table(data, colWidths=[2.5*cm, 10.5*cm, 3*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), DARK_BLUE),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEAFTER',     (0, 0), (1, 0),   1, MID_BLUE),
    ]))
    return t


def cover_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(MID_BLUE)
    canvas.rect(0, h * 0.38, w, h * 0.62, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#E74C3C'))
    canvas.rect(0, h * 0.36, w, 5, fill=1, stroke=0)
    canvas.restoreState()


def normal_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 8.5)
    canvas.drawString(1*cm, h - 0.82*cm,
                      'Gebeya Week 1 — Mentor Meeting Report')
    canvas.drawRightString(w - 1*cm, h - 0.82*cm, 'Biniam Tsige')
    canvas.setFillColor(GREY_LIGHT)
    canvas.rect(0, 0, w, 0.85*cm, fill=1, stroke=0)
    canvas.setFillColor(GREY_DARK)
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(w / 2, 0.32*cm, f'Page {doc.page}')
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title='Gebeya Week 1 Mentor Meeting Report',
        author='Biniam Tsige'
    )
    story = []

    # ── COVER ─────────────────────────────────────────────────
    story.append(Spacer(1, 4.5*cm))
    story.append(P('Gebeya Week 1 Challenge', cover_title))
    story.append(P('Mentor Meeting Report', cover_sub))
    story.append(Spacer(1, 0.4*cm))
    story.append(P('Slack Messages Analysis Project', cover_sub))
    story.append(Spacer(1, 1.5*cm))
    story.append(P('Biniam Tsige  |  Batch 6  |  2026', cover_meta))
    story.append(P('Data Engineering & ML Engineering Track', cover_meta))
    story.append(PageBreak())

    # ── OVERALL PROGRESS ──────────────────────────────────────
    story.append(P('Week 1 — Overall Progress', h1))
    story.append(HR())
    story.append(tbl(
        ['Task', 'Topic', 'Status', 'Key Output'],
        [
            ['Task 1', 'Git, GitHub & EDA',
             '✅ Complete', 'EDA notebook, project structure'],
            ['Task 2', 'Data Science & ML',
             '✅ Complete', 'ML models, sentiment, MLFlow'],
            ['Task 3', 'MongoDB & PostgreSQL',
             '✅ Complete', 'Two databases loaded'],
            ['Task 4', 'Streamlit Dashboard',
             '✅ Complete', 'Live interactive web app'],
            ['Task 5', 'Deployment',
             '✅ Complete', 'Docker, Terraform, CI/CD'],
            ['GitHub', 'Push to repository',
             '✅ Pushed', 'Private repo, 2 commits'],
        ],
        col_w=[1.8*cm, 4.2*cm, 3*cm, 7*cm]
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(box(
        'All 5 tasks have been completed. The project is pushed to GitHub at '
        'github.com/BTSM10/Gebeya-Tech. The repository is currently private — '
        'it can be made public at any time from GitHub Settings.',
        bg=LIGHT_GREEN, border=GREEN
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TASK 1
    # ══════════════════════════════════════════════════════════
    story.append(task_header(1, 'Git, GitHub & Exploratory Data Analysis'))
    story.append(Spacer(1, 0.3*cm))

    story.append(P('What was done', h2))
    story.append(P(
        'Set up the full project from scratch following the Gebeya starter package structure. '
        'Built a data loading pipeline and performed comprehensive exploratory data analysis '
        'on 20,011 anonymized Slack messages across 39 channels from Gebeya Batch 6.'
    ))

    story.append(P('Project structure created:', h3))
    story.append(B('src/loader.py — SlackDataLoader class that reads all JSON files into pandas DataFrames'))
    story.append(B('src/utils.py — helper functions for timestamp parsing and user ranking'))
    story.append(B('src/config.py — centralised data path configuration'))
    story.append(B('notebooks/parse_slack_data.ipynb — full EDA analysis notebook'))
    story.append(B('.gitignore — protects the anonymized/ data from ever going to GitHub'))
    story.append(B('.github/workflows/ — 3 CI/CD pipelines (Flake8, pytest, docstring tests)'))

    story.append(Spacer(1, 0.2*cm))
    story.append(why_box(
        'The data is organised into reusable modules (src/) instead of putting everything '
        'in the notebook. This way, multiple notebooks can import the same functions without '
        'copying code. If we fix a bug in loader.py, all notebooks benefit automatically.'
    ))

    story.append(P('EDA questions answered:', h3))
    story.append(tbl(
        ['Question', 'Approach'],
        [
            ['Top & bottom 10 users by message/reply/reaction/mention count',
             'Grouped by user, aggregated counts, sorted'],
            ['Top 10 messages by replies/reactions/mentions',
             'Sorted DataFrame by each metric'],
            ['Which channel has the highest activity?',
             '2D scatter plot: x=messages, y=replies+reactions'],
            ['What fraction of messages are replied within 5 minutes?',
             'Computed time delta between message ts and first reply ts'],
        ],
        col_w=[7*cm, 9*cm]
    ))

    story.append(Spacer(1, 0.2*cm))
    story.append(P('CI/CD pipelines set up:', h3))
    story.append(P(
        'Three GitHub Actions workflows run automatically every time code is pushed to GitHub. '
        'They act as a quality gate — if code style is wrong or tests fail, the push is flagged.'
    ))
    story.append(tbl(
        ['Workflow', 'What it checks', 'Current status'],
        [
            ['flake8_check.yml', 'Python code style (PEP 8)', '✅ Passing'],
            ['unittests.yml', 'Unit tests via pytest', '❌ Fails on GitHub (no data)'],
            ['docstring_tests.yml', 'Examples in docstrings', '✅ Passing'],
        ]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(pending_box(
        'Unit tests fail on GitHub because the anonymized/ data folder is never pushed '
        '(data privacy requirement). The tests pass perfectly locally. '
        'A fix would be to mock the data in tests — can be done in a future iteration.'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TASK 2
    # ══════════════════════════════════════════════════════════
    story.append(task_header(2, 'Data Science Components & ML Models'))
    story.append(Spacer(1, 0.3*cm))

    story.append(P('What was done', h2))
    story.append(P(
        'Built and trained machine learning models on the Slack dataset. '
        'Wrote unit tests for the data loader. '
        'Versioned all models and their artefacts using MLFlow.'
    ))

    story.append(P('1. Unit Tests (tests/test_loader.py)', h3))
    story.append(P('Five tests written and all passing locally:'))
    story.append(B('Checks that load_channel() returns a pandas DataFrame'))
    story.append(B('Checks that the DataFrame has the expected columns: type, user, text, ts, channel'))
    story.append(B('Checks load_all_channels() returns a non-empty DataFrame'))
    story.append(B('Checks load_all_channels() has the expected columns'))
    story.append(B('Checks the channel column always matches the folder it was loaded from'))
    story.append(Spacer(1, 0.2*cm))
    story.append(why_box(
        'Unit tests catch bugs early. If someone accidentally changes the loader and breaks '
        'the column structure, the test immediately flags it instead of silently producing '
        'wrong analysis results downstream.'
    ))

    story.append(P('2. Time Difference Histograms', h3))
    story.append(P(
        'Analysed the distribution of time gaps between consecutive events — '
        'how long do people typically wait between messages, replies, reactions, '
        'and all events combined.'
    ))
    story += img('time_diff_histograms.png',
                 cap_text='Figure 1: Time differences between consecutive messages, replies, reactions and all events')

    story.append(P('3. Message Classification', h3))
    story.append(P(
        'Classified every message into one of 6 categories using rule-based logic. '
        'Since no labeled training data exists, keywords and regex patterns were used '
        'as a first-pass classifier. This is a standard approach before building a '
        'supervised model.'
    ))
    story.append(tbl(
        ['Category', 'Rule'],
        [
            ['Question-Technical', 'Contains ? or question words AND technical keywords'],
            ['Question-NonTechnical', 'Contains ? or question words, no technical content'],
            ['Answer', 'Starts with yes/no/sure or contains answer phrases'],
            ['Comment-Technical', 'Contains technical keywords, not a question or answer'],
            ['Comment-NonTechnical', 'General chat with no technical content'],
            ['Other', 'Empty or unclassifiable'],
        ]
    ))
    story += img('message_classification.png',
                 cap_text='Figure 2: Distribution of message types across all 39 channels')

    story.append(P('4. Topic Modelling (LDA)', h3))
    story.append(P(
        'Used Latent Dirichlet Allocation to automatically discover 10 hidden themes '
        'across 20,000 messages without being told what the topics are. '
        'Text was cleaned first — Slack mentions, URLs, stop words, and short words removed. '
        'A vocabulary of the top 2,000 words was built using CountVectorizer.'
    ))
    story.append(why_box(
        'LDA is unsupervised — no labels needed. It reveals what the community actually '
        'talked about most. On short informal messages like Slack, topics are less clean '
        'than on formal text — this is expected and noted.'
    ))
    story += img('topic_modelling.png',
                 cap_text='Figure 3: Top 10 LDA topics extracted from Slack messages')

    story.append(P('5. Sentiment Analysis Over Time', h3))
    story.append(P(
        'Measured the emotional tone of messages across the entire training period. '
        'Messages were grouped by day, merged into one daily text block, and scored '
        'using TextBlob (polarity from -1 negative to +1 positive). '
        'A Savitzky-Golay smoothing filter shows the overall trend.'
    ))
    story += img('sentiment_over_time.png',
                 cap_text='Figure 4: Daily sentiment polarity across the training program')

    story.append(P('6. MLFlow Model Versioning', h3))
    story.append(P(
        'All models and their artefacts are logged to MLFlow — a tool that tracks '
        'every training run with its parameters, metrics, and saved model files. '
        'This means any run can be reproduced exactly or compared against future runs.'
    ))
    story.append(tbl(
        ['Logged item', 'Value'],
        [
            ['n_topics', '10'],
            ['LDA max iterations', '20'],
            ['Vocabulary size', '2,000 words'],
            ['Corpus size', '~18,000 documents'],
            ['LDA model', 'Saved in scikit-learn format'],
            ['CountVectorizer', 'Saved as .pkl artefact'],
            ['All 4 charts', 'Saved as PNG artefacts'],
        ]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TASK 3
    # ══════════════════════════════════════════════════════════
    story.append(task_header(3, 'MongoDB & PostgreSQL Databases'))
    story.append(Spacer(1, 0.3*cm))

    story.append(P('What was done', h2))
    story.append(P(
        'Installed and configured two databases locally. '
        'Loaded the raw Slack data into MongoDB and the computed ML features into PostgreSQL.'
    ))

    story.append(P('Why two databases?', h3))
    story.append(tbl(
        ['', 'MongoDB', 'PostgreSQL'],
        [
            ['Type', 'NoSQL — documents', 'SQL — tables'],
            ['Structure', 'Flexible (each document can differ)', 'Rigid (all rows same structure)'],
            ['Best for', 'Raw, messy, unpredictable data', 'Clean, structured, computed data'],
            ['We used it for', 'Raw Slack JSON messages', 'Computed ML features'],
        ],
        col_w=[3.5*cm, 6.25*cm, 6.25*cm]
    ))

    story.append(P('MongoDB — 3 collections:', h3))
    story.append(tbl(
        ['Collection', 'Records', 'What it stores'],
        [
            ['messages', '10,814', 'Top-level messages only'],
            ['replies', '8,788', 'Thread replies, linked to parent message'],
            ['reactions', '4,842', 'Emoji reactions, linked to their message'],
        ]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(why_box(
        'Split into 3 collections for query speed and streaming efficiency. '
        'Querying only reactions does not load all 10,814 messages. '
        'New reactions can be inserted without touching the original message document.'
    ))

    story.append(P('PostgreSQL — 3 tables:', h3))
    story.append(tbl(
        ['Table', 'Rows', 'What it stores'],
        [
            ['message_features', '19,602',
             'Per-message: sentiment score, type, hour, day of week'],
            ['user_features', '1,205',
             'Per-user per-channel: message count, reply count, dominant type'],
            ['daily_sentiment', '104',
             'Per-day: sentiment score, message count, days since training start'],
        ]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TASK 4
    # ══════════════════════════════════════════════════════════
    story.append(task_header(4, 'Streamlit Interactive Dashboard'))
    story.append(Spacer(1, 0.3*cm))

    story.append(P('What was done', h2))
    story.append(P(
        'Built a fully interactive web dashboard in Python using Streamlit — '
        'no HTML or JavaScript required. The dashboard displays all results from '
        'Task 1 and Task 2 in one place with live filtering.'
    ))

    story.append(P('Dashboard sections:', h3))
    story.append(tbl(
        ['Section', 'What it shows'],
        [
            ['Sidebar', 'Channel filter dropdown + live stats (messages, channels, users)'],
            ['Key Metrics', '4 summary boxes: total messages, channels, unique users, reactions'],
            ['Top & Bottom Users', 'Tabs for messages, replies, reactions, mentions'],
            ['Channel Activity', 'Scatter plot — x=messages, y=replies+reactions, colour=channel'],
            ['Message Classification', 'Bar chart + pie chart of message types'],
            ['ML Analysis Results', 'Embedded charts from Task 2 (histograms, topics, sentiment)'],
            ['Raw Data Explorer', 'Scrollable table with adjustable row count slider'],
        ]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(result_box(
        'The channel filter dropdown in the sidebar is interactive — '
        'selecting any channel instantly updates every chart and table on the page '
        'to show only that channel\'s data.'
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(P('How to run it:', h3))
    story.append(Paragraph(
        'cd /Users/btsm/Desktop/P/Gebeya-Tech  →  '
        'source gebvenv/bin/activate  →  '
        'streamlit run app/dashboard.py',
        code
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # TASK 5
    # ══════════════════════════════════════════════════════════
    story.append(task_header(5, 'Deployment — Docker, Terraform & GitHub Actions'))
    story.append(Spacer(1, 0.3*cm))

    story.append(P('What was done', h2))
    story.append(P(
        'Created the full deployment infrastructure: a Dockerfile to containerise the app, '
        'a GitHub Actions workflow to build and push the Docker image automatically, '
        'and a Terraform script to provision AWS cloud infrastructure.'
    ))

    story.append(P('Dockerfile', h3))
    story.append(P(
        'Packages the entire Streamlit dashboard — code, Python version, all packages — '
        'into a single container that runs identically on any computer in the world. '
        'Solves the "works on my machine" problem permanently.'
    ))
    story.append(Paragraph(
        'FROM python:3.11-slim  |  COPY requirements.txt  |  '
        'RUN pip install  |  COPY src/ app/  |  '
        'EXPOSE 8501  |  CMD streamlit run app/dashboard.py',
        code
    ))

    story.append(P('GitHub Actions — docker_publish.yml', h3))
    story.append(P(
        'Every time code is pushed to the main branch, this workflow automatically '
        'builds the Docker image and pushes it to Docker Hub — no manual steps needed.'
    ))
    story.append(tbl(
        ['Step', 'What happens'],
        [
            ['Trigger', 'Push to main branch on GitHub'],
            ['Step 1', 'GitHub spins up a fresh Ubuntu server'],
            ['Step 2', 'Checks out the code'],
            ['Step 3', 'Logs into Docker Hub using encrypted secrets'],
            ['Step 4', 'Builds Docker image from Dockerfile'],
            ['Step 5', 'Pushes image to Docker Hub as btsm/gebeya-dashboard:latest'],
        ]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(pending_box(
        'Docker Hub credentials (DOCKER_USERNAME, DOCKER_PASSWORD) have not been '
        'added to GitHub Secrets yet. The workflow fails at login. '
        'Fix: create a free Docker Hub account → GitHub repo Settings → '
        'Secrets and variables → Actions → add both secrets → push any change.'
    ))

    story.append(P('Terraform — terraform/main.tf', h3))
    story.append(P(
        'Infrastructure as Code — describes the AWS cloud infrastructure in a .tf file '
        'so it can be created automatically with one command instead of clicking through '
        'the AWS website. The script is validated and ready to deploy.'
    ))
    story.append(tbl(
        ['Resource', 'Type', 'Purpose'],
        [
            ['dashboard_server', 'EC2 t2.micro', 'Virtual server to run the dashboard 24/7'],
            ['data_bucket', 'S3 bucket', 'Cloud storage for data and ML artefacts'],
        ]
    ))
    story.append(Paragraph(
        'terraform init  →  terraform plan  →  terraform apply',
        code
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(pending_box(
        'AWS deployment not yet active — requires an AWS account with credit card. '
        'Free tier available: EC2 t2.micro is free for 12 months. '
        'The Terraform script is written, validated, and ready to run.'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # GITHUB STATUS
    # ══════════════════════════════════════════════════════════
    story.append(P('GitHub Repository Status', h1))
    story.append(HR())

    story.append(tbl(
        ['Item', 'Detail'],
        [
            ['Repository', 'github.com/BTSM10/Gebeya-Tech'],
            ['Visibility', 'Private (can be made public anytime)'],
            ['Branch', 'main'],
            ['Total commits', '2'],
            ['Total files', '32 files pushed'],
            ['Data pushed?', 'No — anonymized/ protected by .gitignore ✅'],
        ],
        col_w=[5*cm, 11*cm]
    ))

    story.append(Spacer(1, 0.3*cm))
    story.append(P('CI/CD Workflow Results (latest push):', h3))
    story.append(tbl(
        ['Workflow', 'Status', 'Reason if failing'],
        [
            ['Flake8 Lint', '✅ Passing', '—'],
            ['Docstring Tests', '✅ Passing', '—'],
            ['Unit Tests', '❌ Failing', 'No data on GitHub (by design — data privacy)'],
            ['Build & Push Docker', '❌ Failing', 'Docker Hub secrets not configured yet'],
        ]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # KEY DECISIONS
    # ══════════════════════════════════════════════════════════
    story.append(P('Key Decisions & Why', h1))
    story.append(HR())

    decisions = [
        (
            'Why use a virtual environment (gebvenv)?',
            'Isolates project packages from the system Python. '
            'Different projects can need different versions of the same library '
            'without conflicting. The venv is disposable — delete and recreate '
            'it at any time without losing any code.'
        ),
        (
            'Why is the anonymized/ data not on GitHub?',
            'Gebeya\'s data privacy requirement. The .gitignore file blocks it '
            'from ever being staged or committed. It will never appear in the '
            'repository history even by accident.'
        ),
        (
            'Why split code into src/ instead of putting everything in notebooks?',
            'Notebooks are for analysis and presentation. Core logic (loading, '
            'cleaning, utility functions) lives in .py files so it can be '
            'imported by any notebook without code duplication. '
            'If a bug is fixed in loader.py, all notebooks benefit automatically.'
        ),
        (
            'Why two databases (MongoDB + PostgreSQL)?',
            'MongoDB handles raw, flexible, schema-less Slack JSON data — '
            'each message can have different fields. PostgreSQL handles the '
            'computed ML features which have a fixed, consistent structure. '
            'Using only one database would be the wrong tool for at least one job.'
        ),
        (
            'Why rule-based classification instead of a trained ML model?',
            'No labeled training data exists — nobody tagged 20,000 messages as '
            'Question/Comment/Answer. Rule-based is the correct first step. '
            'The output of the rules could be reviewed and corrected to create '
            'labeled data for a supervised model in a future iteration.'
        ),
        (
            'Why Docker for deployment?',
            'The Streamlit dashboard currently only runs on this Mac. '
            'Docker packages the entire app so it runs identically on any '
            'server — the GitHub runner, an AWS EC2 instance, a teammate\'s '
            'laptop — with no setup required.'
        ),
    ]

    for question, answer in decisions:
        story.append(KeepTogether([
            P(f'<b>{question}</b>', h3),
            P(answer),
            Spacer(1, 0.2*cm),
        ]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PENDING ITEMS
    # ══════════════════════════════════════════════════════════
    story.append(P('Pending Items', h1))
    story.append(HR())

    story.append(tbl(
        ['Item', 'What\'s needed', 'Priority'],
        [
            ['Docker Hub setup',
             'Create free Docker Hub account → add DOCKER_USERNAME and '
             'DOCKER_PASSWORD as GitHub Secrets',
             'High'],
            ['Unit tests on GitHub',
             'Mock the data loader in tests so they pass without the '
             'anonymized/ folder on the server',
             'Medium'],
            ['AWS deployment',
             'Create AWS account → run terraform apply → dashboard live 24/7',
             'Low (optional for now)'],
            ['Mentor guidance on repo',
             'Confirm whether to keep personal GitHub or move to company org',
             'Awaiting mentor'],
        ],
        col_w=[4*cm, 8.5*cm, 3.5*cm]
    ))

    story.append(Spacer(1, 1*cm))
    story.append(P(
        'End of Report  —  Biniam Tsige  —  Gebeya Batch 6',
        S('end', fontSize=9, textColor=GREY_DARK, alignment=TA_CENTER)
    ))

    doc.build(story, onFirstPage=cover_page, onLaterPages=normal_page)
    print(f'PDF saved: {OUTPUT}')


if __name__ == '__main__':
    build()
