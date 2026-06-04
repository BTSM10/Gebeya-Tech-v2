"""Generate comprehensive project documentation PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import datetime

OUTPUT = "Gebeya_Week1_Complete_Guide.pdf"

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

cover_title = ParagraphStyle("cover_title", fontSize=28, alignment=TA_CENTER,
                              spaceAfter=12, textColor=colors.HexColor("#1a1a2e"),
                              fontName="Helvetica-Bold")
cover_sub = ParagraphStyle("cover_sub", fontSize=16, alignment=TA_CENTER,
                            spaceAfter=8, textColor=colors.HexColor("#16213e"),
                            fontName="Helvetica")
cover_info = ParagraphStyle("cover_info", fontSize=12, alignment=TA_CENTER,
                             spaceAfter=6, textColor=colors.HexColor("#0f3460"),
                             fontName="Helvetica")
h1 = ParagraphStyle("h1", fontSize=20, spaceAfter=12, spaceBefore=20,
                    textColor=colors.HexColor("#1a1a2e"), fontName="Helvetica-Bold",
                    borderPad=4)
h2 = ParagraphStyle("h2", fontSize=15, spaceAfter=8, spaceBefore=14,
                    textColor=colors.HexColor("#16213e"), fontName="Helvetica-Bold")
h3 = ParagraphStyle("h3", fontSize=12, spaceAfter=6, spaceBefore=10,
                    textColor=colors.HexColor("#0f3460"), fontName="Helvetica-Bold")
body = ParagraphStyle("body", fontSize=10, spaceAfter=6, leading=16,
                       fontName="Helvetica", alignment=TA_JUSTIFY)
bullet = ParagraphStyle("bullet", fontSize=10, spaceAfter=4, leading=14,
                         leftIndent=20, fontName="Helvetica",
                         bulletIndent=10)
code = ParagraphStyle("code", fontSize=9, spaceAfter=4, leading=13,
                       fontName="Courier", leftIndent=20, rightIndent=20,
                       backColor=colors.HexColor("#f4f4f4"), borderPad=6,
                       textColor=colors.HexColor("#1a1a1a"))
code_inline = ParagraphStyle("code_inline", fontSize=9, fontName="Courier",
                              textColor=colors.HexColor("#c7254e"))
note = ParagraphStyle("note", fontSize=9, spaceAfter=6, leading=13,
                       leftIndent=20, fontName="Helvetica-Oblique",
                       textColor=colors.HexColor("#555555"))
qa_q = ParagraphStyle("qa_q", fontSize=10, spaceAfter=4, leading=14,
                       fontName="Helvetica-Bold", textColor=colors.HexColor("#0f3460"),
                       leftIndent=10)
qa_a = ParagraphStyle("qa_a", fontSize=10, spaceAfter=10, leading=14,
                       fontName="Helvetica", leftIndent=20,
                       textColor=colors.HexColor("#1a1a1a"))


def HR():
    return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc"),
                      spaceAfter=8, spaceBefore=8)


def title(text):
    return Paragraph(text, h1)


def section(text):
    return Paragraph(text, h2)


def subsection(text):
    return Paragraph(text, h3)


def p(text):
    return Paragraph(text, body)


def b(text):
    return Paragraph(f"• {text}", bullet)


def c(text):
    return Paragraph(text.replace(" ", "&nbsp;").replace("\n", "<br/>"), code)


def sp(n=1):
    return Spacer(1, n * 0.3 * cm)


def table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f9f9f9"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ]
    if not header:
        style_cmds[0] = ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f9f9f9"))
        style_cmds[1] = ("TEXTCOLOR", (0, 0), (-1, 0), colors.black)
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Build document ────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 3*cm),
        Paragraph("Gebeya Week 1 Challenge", cover_title),
        Paragraph("Slack Messages Analysis — Complete Project Guide", cover_sub),
        Spacer(1, 1*cm),
        HR(),
        Spacer(1, 0.5*cm),
        Paragraph("Biniam Tsige · Batch 6 · Data Engineering & ML Engineering", cover_info),
        Paragraph(f"Generated: {datetime.date.today().strftime('%B %d, %Y')}", cover_info),
        Spacer(1, 2*cm),
        p("This document is a complete record of everything built, learned, and debugged "
          "during the Gebeya Week 1 Challenge. It covers all 5 tasks — from raw data loading "
          "to cloud deployment — including every concept explained, every question asked, "
          "every mistake made, and every fix applied."),
        Spacer(1, 1*cm),
        table([
            ["Task", "Topic", "Status"],
            ["Task 1", "Git Setup & Exploratory Data Analysis", "Complete"],
            ["Task 2", "ML Analysis (LDA, Sentiment, Classification)", "Complete"],
            ["Task 3", "Databases (MongoDB + PostgreSQL)", "Complete"],
            ["Task 4", "Streamlit Dashboard + Docker", "Complete"],
            ["Task 5", "Infrastructure (Terraform + AWS + CI/CD)", "Complete"],
            ["Bonus", "MongoDB Atlas + Streamlit Cloud Deployment", "Complete"],
        ], col_widths=[2*cm, 10*cm, 3.5*cm]),
        PageBreak(),
    ]

    # ── SECTION 1: ENVIRONMENT SETUP ─────────────────────────────────────────
    story += [
        title("1. Development Environment Setup"),
        HR(),
        p("Before writing any code, the development environment was set up correctly. "
          "This is one of the most important steps — the wrong setup causes mysterious "
          "errors that have nothing to do with your code."),
        sp(),

        section("1.1 Virtual Environment (gebvenv)"),
        p("A virtual environment is an isolated Python workspace. Think of it like a "
          "separate room in your house dedicated to this project. Everything installed "
          "inside it stays inside it and doesn't affect any other Python project on your Mac."),
        sp(),
        p("Why this matters: if you install pandas for one project and it conflicts with "
          "an older version needed by another project, your entire Python setup breaks. "
          "Virtual environments prevent this completely."),
        sp(),
        c("# Create the virtual environment\npython3 -m venv gebvenv\n\n"
          "# Activate it (must do this every session)\nsource gebvenv/bin/activate\n\n"
          "# Your terminal prompt changes to:\n(gebvenv) btsm@MacBook Gebeya-Tech %"),
        p("The virtual environment is named <b>gebvenv</b> — not the default 'venv'. "
          "This is intentional to make it clearly identifiable as this project's environment."),
        sp(),

        section("1.2 Homebrew — Mac Package Manager"),
        p("Homebrew is the package manager for macOS system tools. Think of it like the "
          "App Store, but for developer tools that don't have a graphical installer. "
          "You use it to install things like databases, infrastructure tools, and runtimes."),
        sp(),
        table([
            ["Tool", "Installed via", "Purpose"],
            ["MongoDB", "brew install mongodb-community", "NoSQL database for raw data storage"],
            ["PostgreSQL", "brew install postgresql@15", "SQL database for analytics"],
            ["Terraform", "brew install hashicorp/tap/terraform", "Infrastructure as Code"],
            ["Docker", "Download from docker.com", "Container platform"],
        ], col_widths=[4*cm, 7*cm, 5.5*cm]),
        sp(),
        p("Homebrew installs tools <b>globally</b> on your Mac — available to all projects "
          "and in any terminal. This is correct for system tools. Python packages, however, "
          "should be installed inside gebvenv using pip."),
        sp(),
        c("# Check what Homebrew has installed\nbrew list\n\n"
          "# Check running services\nbrew services list"),
        sp(),

        section("1.3 pip — Python Package Manager"),
        p("pip installs Python libraries inside your virtual environment. Always activate "
          "gebvenv first, then use pip — otherwise packages install to the wrong location."),
        sp(),
        table([
            ["Package", "Purpose"],
            ["pandas", "Data manipulation — DataFrames, filtering, grouping"],
            ["matplotlib / seaborn", "Chart and graph generation"],
            ["scikit-learn", "LDA topic modelling (LatentDirichletAllocation)"],
            ["textblob", "Pre-trained sentiment analysis"],
            ["nltk", "Natural language processing (stopwords, tokenization)"],
            ["mlflow", "Experiment tracking and model versioning"],
            ["pymongo", "Python driver for MongoDB"],
            ["psycopg2-binary", "Python driver for PostgreSQL"],
            ["streamlit", "Interactive web dashboard framework"],
            ["pytest", "Unit testing framework"],
            ["reportlab", "PDF generation"],
            ["Pillow", "Image loading for dashboard charts"],
        ], col_widths=[5*cm, 11.5*cm]),
        sp(),

        section("1.4 Jupyter Notebooks & Kernel Registration"),
        p("Jupyter notebooks run code in cells interactively. The key issue on this project: "
          "Jupyter must use the gebvenv kernel, not the system Python. If the wrong kernel "
          "is selected, all your installed packages are invisible and you get ModuleNotFoundError."),
        sp(),
        c("# Register gebvenv as a Jupyter kernel\npython -m ipykernel install --user "
          "--name=gebvenv --display-name='Python (gebvenv)'\n\n"
          "# When opening a notebook, always select:\n# Kernel → 'Python (gebvenv)'"),
        sp(),
        p("When you save a Jupyter notebook (.ipynb), it saves both the code AND the "
          "output (charts, tables, printed results). The notebook is a JSON file containing "
          "all of this together."),
        PageBreak(),
    ]

    # ── SECTION 2: TASK 1 ────────────────────────────────────────────────────
    story += [
        title("2. Task 1 — Git Setup & Exploratory Data Analysis"),
        HR(),
        p("Task 1 had two goals: set up proper version control with Git and GitHub, "
          "and perform exploratory data analysis (EDA) on the Slack messages dataset."),
        sp(),

        section("2.1 The Dataset"),
        p("The dataset is a Slack export from the Gebeya community workspace — messages "
          "from 39 channels spanning multiple weeks. The data is in JSON format, "
          "organized as one file per channel per day."),
        sp(),
        table([
            ["Fact", "Value"],
            ["Total messages loaded", "20,011"],
            ["Channels", "39"],
            ["Format", "JSON files in anonymized/ folder"],
            ["Privacy rule", "NEVER push anonymized/ to GitHub"],
        ], col_widths=[6*cm, 10.5*cm]),
        sp(),
        p("The data is anonymized — user IDs appear as codes like U03T89ACUUW instead "
          "of real names. @mention tags were also stripped during anonymization, which "
          "is why the mention count analysis showed near-zero values for all users."),
        sp(),

        section("2.2 SlackDataLoader Class"),
        p("Instead of writing raw file-reading code everywhere, we built a class called "
          "SlackDataLoader that encapsulates all data loading logic. A class is a "
          "blueprint that groups related functions (methods) together."),
        sp(),
        c("class SlackDataLoader:\n"
          "    def __init__(self, data_path=DATA_PATH, source='auto'):\n"
          "        self.data_path = data_path\n"
          "        self.source = 'mongo' if MONGO_URI else 'local'\n\n"
          "    def get_channels(self):      # returns list of channel names\n"
          "    def load_channel(channel):   # loads one channel as DataFrame\n"
          "    def load_all_channels():     # loads all channels combined"),
        sp(),
        p("Why use a class instead of plain functions? Because data_path is shared "
          "across all three methods. Setting it once in __init__ means all methods "
          "automatically have access via self.data_path — no need to pass it every time."),
        sp(),

        section("2.3 What is a pandas DataFrame?"),
        p("A DataFrame is like a spreadsheet in Python — rows and columns. When we load "
          "Slack messages, each row is one message and columns are its properties:"),
        sp(),
        table([
            ["channel", "user", "text", "ts", "type", "reply_count"],
            ["ai-community-building", "U03T89AC", "Has anyone...", "1234567890.1", "message", "5"],
            ["all-week3", "U03TEPYRM", "Yes, you need...", "1234567891.2", "message", "0"],
        ], col_widths=[3.5*cm, 2.5*cm, 4*cm, 3*cm, 2*cm, 2*cm]),
        sp(),

        section("2.4 The Four Analysis Dimensions"),
        p("For each user, we measured four things. These measure different aspects of "
          "how a person participates in the community:"),
        sp(),
        table([
            ["Metric", "What it measures", "Top user = ..."],
            ["Message count", "How many messages they posted", "Most active poster"],
            ["Reply count", "How many replies their posts received", "Best conversation starter"],
            ["Reaction count", "How many emoji reactions their posts got", "Most appreciated poster"],
            ["Mention count", "How often they @mentioned others", "Most connected (showed 0 — anonymized)"],
        ], col_widths=[3.5*cm, 6*cm, 7*cm]),
        sp(),
        p("The key insight: these metrics tell very different stories. A user can post "
          "constantly (high message count) but get no reactions (low reaction count). "
          "Another user might post rarely but spark huge discussions (low messages, high replies)."),
        sp(),

        section("2.5 Channel Activity Scatter Plot"),
        p("The scatter plot showed each channel as a dot with: X = number of messages, "
          "Y = total replies + reactions. The result was a classic long-tail distribution."),
        sp(),
        p("ai-community-building was a massive outlier at ~8,500 messages and ~11,000 "
          "engagements — far beyond all other channels. This single channel drove the "
          "majority of all community activity."),
        sp(),

        section("2.6 Reply Time Analysis"),
        p("We measured the time between a message being posted and receiving its first reply, "
          "then plotted against the hour of day. Findings:"),
        sp(),
        b("Median reply time: 0.6 minutes — most replies came within seconds"),
        b("Community was highly responsive during active hours"),
        b("Messages posted late at night waited hours — sometimes 1,400+ minutes"),
        b("This shows a natural active window vs off-hours pattern"),
        sp(),

        section("2.7 CI/CD Workflows (GitHub Actions)"),
        p("Three automatic checks run every time code is pushed to GitHub:"),
        sp(),
        table([
            ["Workflow", "File", "What it checks", "Passes when"],
            ["Flake8", "flake8_check.yml", "PEP 8 code style", "No style violations"],
            ["Docstrings", "docstring_tests.yml", "Every function documented", "All have docstrings"],
            ["Unit Tests", "unittests.yml", "Code correctness", "All 5 pytest tests pass"],
        ], col_widths=[2.5*cm, 4*cm, 5*cm, 5*cm]),
        sp(),
        p("Flake8 enforces PEP 8 — Python's official style guide. Rules include: "
          "max 100 characters per line, no unused imports, proper blank lines between functions. "
          "Several fixes were needed in dashboard.py and test_loader.py to make it pass."),
        PageBreak(),
    ]

    # ── SECTION 3: TASK 2 ────────────────────────────────────────────────────
    story += [
        title("3. Task 2 — ML Analysis"),
        HR(),
        p("Task 2 applied machine learning and statistical analysis to the Slack messages. "
          "Three different techniques were used, each serving a different purpose."),
        sp(),

        section("3.1 Time Difference Histograms"),
        p("A histogram shows how frequently values fall into ranges (called bins). "
          "We measured the time gap between consecutive events — how quickly the next "
          "message, reply, or reaction appeared after the previous one."),
        sp(),
        table([
            ["Chart", "Median gap", "What it tells us"],
            ["Consecutive Messages", "0.6 min", "Messages come in rapid bursts"],
            ["Consecutive Replies", "0.8 min", "Thread replies also happen fast"],
            ["Consecutive Reactions", "1.4 min", "Reactions slightly slower — reading before clicking"],
            ["All Events combined", "0.6 min", "Overall community rhythm"],
        ], col_widths=[5*cm, 2.5*cm, 9*cm]),
        sp(),
        p("The x-axis was capped at 120 minutes. All gaps longer than 120 minutes were "
          "grouped into the last bar — this is why there appears to be a spike at 120, "
          "it actually means '120 minutes or more'."),
        sp(),

        section("3.2 Rule-Based Message Classification"),
        p("Before applying ML, we classified messages using hand-written rules. "
          "This is not machine learning — it's if/else logic written by a human:"),
        sp(),
        c("def classify_message(text):\n"
          "    tech = any(keyword in text.lower() for keyword in TECH_KEYWORDS)\n"
          "    if re.search(r'\\?|how|what|why', text.lower()):\n"
          "        return 'Question-Technical' if tech else 'Question-NonTechnical'\n"
          "    if re.search(r'^(yes|no|sure|correct)', text.lower()):\n"
          "        return 'Answer'\n"
          "    return 'Comment-Technical' if tech else 'Comment-NonTechnical'"),
        sp(),
        p("TECH_KEYWORDS included: error, bug, code, python, git, pandas, model, "
          "docker, api, sql, jupyter, and others. Any message containing these words "
          "was classified as technical."),
        sp(),

        section("3.3 LDA Topic Modelling — Real Model Training"),
        p("LDA (Latent Dirichlet Allocation) is an unsupervised machine learning algorithm "
          "that discovers hidden topics in a collection of text. 'Unsupervised' means we "
          "never told it what the topics were — it found them on its own."),
        sp(),
        p("How it works:"),
        b("Step 1 — CountVectorizer converts all messages into a matrix of word counts. "
          "Each row is a message, each column is a word, each cell is how many times "
          "that word appears."),
        b("Step 2 — LDA analyzes which words appear together frequently across messages. "
          "Words that co-occur often are grouped into a topic."),
        b("Step 3 — The model outputs topics as word distributions. Topic 1 might be "
          "'python, error, install, pip' and Topic 2 might be 'week, task, submit, deadline'."),
        sp(),
        c("from sklearn.feature_extraction.text import CountVectorizer\n"
          "from sklearn.decomposition import LatentDirichletAllocation\n\n"
          "vectorizer = CountVectorizer(stop_words='english', max_features=1000)\n"
          "X = vectorizer.fit_transform(messages)  # ← builds vocabulary from our data\n\n"
          "lda = LatentDirichletAllocation(n_components=5, random_state=42)\n"
          "lda.fit(X)  # ← THIS is the actual model training"),
        sp(),
        p("The .fit() call is model training — the LDA model learns patterns "
          "from our specific Slack messages. This is the only genuine model training "
          "in the entire project."),
        sp(),

        section("3.4 Sentiment Analysis with TextBlob"),
        p("Sentiment analysis measures whether text is positive, negative, or neutral. "
          "TextBlob assigns a polarity score between -1.0 (very negative) and +1.0 "
          "(very positive). A score near 0 is neutral."),
        sp(),
        c("from textblob import TextBlob\n\n"
          "score = TextBlob('Great work everyone!').sentiment.polarity\n"
          "# score = 0.8  (positive)\n\n"
          "score = TextBlob('This is broken and nothing works').sentiment.polarity\n"
          "# score = -0.4  (negative)"),
        sp(),
        p("TextBlob uses a pre-trained lexicon — a dictionary of words labeled as "
          "positive or negative by researchers. We did NOT train this model. We just "
          "applied it to our messages. We then grouped scores by day and plotted "
          "the trend over time using a Savitzky-Golay smoothing filter."),
        sp(),

        section("3.5 MLFlow — Experiment Tracking"),
        p("MLFlow is a tool that logs every time you train a model — recording the "
          "parameters used, the results produced, and saving the model itself. "
          "Think of it like a lab notebook for machine learning experiments."),
        sp(),
        table([
            ["MLFlow concept", "What it means"],
            ["Experiment", "A named group of runs (e.g. 'LDA Topic Modelling')"],
            ["Run", "One execution of training with specific parameters"],
            ["Parameters", "Settings used (e.g. n_topics=5, max_features=1000)"],
            ["Artifacts", "Files saved (model file, vectorizer file, charts)"],
            ["Model registry", "Versioned storage of trained models"],
        ], col_widths=[5*cm, 11.5*cm]),
        sp(),

        section("3.6 The SSL Certificate Issue (and the fix)"),
        p("When running NLTK downloads on macOS, an SSL error appeared:"),
        sp(),
        c("certificate verify failed: unable to get local issuer certificate"),
        sp(),
        p("Cause: Python installed on macOS does not automatically use the system's "
          "trusted certificate store. It needs its own certificate bundle."),
        sp(),
        p("Short-term workaround (used in notebooks):"),
        c("import ssl\nssl._create_default_https_context = ssl._create_unverified_context"),
        sp(),
        p("Proper long-term fix (installed once):"),
        c('open "/Applications/Python 3.14/Install Certificates.command"'),
        p("This installs the certifi certificate bundle and creates a symlink so Python "
          "can verify SSL connections properly. After this, the workaround is not needed."),
        PageBreak(),
    ]

    # ── SECTION 4: TASK 3 ────────────────────────────────────────────────────
    story += [
        title("4. Task 3 — Databases"),
        HR(),
        p("Task 3 stored the processed Slack data in two different database systems. "
          "Using two databases was a deliberate architectural decision based on the "
          "different strengths of each type."),
        sp(),

        section("4.1 Why Two Databases?"),
        table([
            ["", "MongoDB (NoSQL)", "PostgreSQL (SQL)"],
            ["Type", "Document store", "Relational database"],
            ["Structure", "Flexible — each document can have different fields", "Fixed schema — all rows same columns"],
            ["Best for", "Raw, varied, semi-structured data", "Structured data with complex queries"],
            ["Query language", "MongoDB Query Language (JSON-like)", "SQL (SELECT, JOIN, GROUP BY)"],
            ["Our use", "Raw messages, replies, reactions", "Aggregated features and analytics"],
        ], col_widths=[3*cm, 7*cm, 6.5*cm]),
        sp(),
        p("The analogy: MongoDB is like a filing cabinet where each folder can contain "
          "different types of documents. PostgreSQL is like a spreadsheet where every "
          "row must have exactly the same columns."),
        sp(),

        section("4.2 MongoDB — Collections and Documents"),
        p("MongoDB organizes data as: Database → Collections → Documents. "
          "A Document is a JSON-like object. A Collection is a group of related documents."),
        sp(),
        table([
            ["Collection", "Documents stored", "Key fields"],
            ["messages", "20,011", "channel, user, text, ts, type, reply_count"],
            ["replies", "8,900", "channel, parent_ts, user, ts"],
            ["reactions", "5,017", "channel, message_ts, name, count"],
        ], col_widths=[4*cm, 3.5*cm, 9*cm]),
        sp(),
        c("# Connect to local MongoDB\nfrom pymongo import MongoClient\nclient = MongoClient('mongodb://localhost:27017')\n"
          "db = client['gebeya_slack']\n\n"
          "# Insert documents\ndb['messages'].insert_many(message_docs)\n\n"
          "# Query documents\nresults = db['messages'].find({'channel': 'ai-community-building'})"),
        sp(),

        section("4.3 PostgreSQL — Tables and Rows"),
        p("PostgreSQL stores data in tables with fixed columns. We created 3 tables "
          "for analytical queries:"),
        sp(),
        table([
            ["Table", "Rows", "Purpose"],
            ["message_features", "19,602", "One row per message with computed features"],
            ["user_features", "1,205", "Aggregated stats per user across all messages"],
            ["daily_sentiment", "104", "Average sentiment score per day"],
        ], col_widths=[4.5*cm, 2.5*cm, 9.5*cm]),
        sp(),
        c("# Connect to PostgreSQL\nimport psycopg2\nconn = psycopg2.connect(\n"
          "    dbname='gebeya_slack', user='btsm', host='localhost'\n)\n\n"
          "# Query with SQL\ncur.execute('SELECT user, COUNT(*) FROM message_features GROUP BY user')"),
        sp(),

        section("4.4 Indexing in MongoDB"),
        p("An index in a database is like the index at the back of a textbook — instead "
          "of reading every page to find 'pandas', you go straight to the page number "
          "listed in the index. Indexes make queries dramatically faster."),
        sp(),
        p("However, not every field needs an index. Indexes cost storage space and slow "
          "down inserts (because the index must be updated too). Best practice: index "
          "fields you frequently filter or sort by, not everything."),
        sp(),
        c("# Create an index on channel field\ndb['messages'].create_index([('channel', 1)])\n\n"
          "# Unique index — no two documents can have same value\ndb['messages'].create_index([('ts', 1)], unique=True)"),
        PageBreak(),
    ]

    # ── SECTION 5: TASK 4 ────────────────────────────────────────────────────
    story += [
        title("5. Task 4 — Streamlit Dashboard"),
        HR(),
        p("Task 4 built an interactive web dashboard to display all the analysis results "
          "visually. The dashboard was built with Streamlit — a Python framework that "
          "turns Python scripts into web apps without writing any HTML or JavaScript."),
        sp(),

        section("5.1 What is Streamlit?"),
        p("Streamlit turns a Python script into a web page. Every time the user interacts "
          "(changes a dropdown, moves a slider), Streamlit re-runs the entire script from "
          "top to bottom and updates the page. This is why it's so simple to use — "
          "there's no complex event handling code needed."),
        sp(),
        c("import streamlit as st\n\n"
          "st.title('My Dashboard')          # shows a title\n"
          "st.metric('Messages', '20,011')    # shows a metric card\n"
          "st.pyplot(fig)                     # shows a matplotlib chart\n"
          "st.dataframe(df)                   # shows a scrollable table\n"
          "channel = st.selectbox('Filter', channels)  # dropdown"),
        sp(),

        section("5.2 Dashboard Sections"),
        table([
            ["Section", "What it shows"],
            ["1. Key Metrics", "4 metric cards: total messages, channels, users, reactions"],
            ["2. Top & Bottom Users", "4 tabs — bar charts by messages, replies, reactions, mentions"],
            ["3. Channel Activity", "Scatter plot: messages vs engagement per channel"],
            ["4. Message Classification", "Bar chart + pie chart of message types"],
            ["5. ML Analysis Results", "Embedded PNG charts from Task 2 notebooks"],
            ["6. Raw Data Explorer", "Scrollable table with slider to choose row count"],
        ], col_widths=[4*cm, 12.5*cm]),
        sp(),

        section("5.3 st.cache_data"),
        p("Loading 20,000 messages from the database every time someone moves a slider "
          "would be very slow. @st.cache_data solves this — it runs the function once, "
          "stores the result in memory, and returns the cached result for all future calls."),
        sp(),
        c("@st.cache_data\ndef load_data():\n    loader = SlackDataLoader()\n"
          "    df = loader.load_all_channels()\n    return df\n\n"
          "df = load_data()  # only queries the database ONCE, then uses cache"),
        PageBreak(),
    ]

    # ── SECTION 6: DOCKER ────────────────────────────────────────────────────
    story += [
        title("6. Docker — Containerization"),
        HR(),
        p("Docker packages your application and all its dependencies into a container — "
          "a self-contained unit that runs identically on any machine. The analogy: "
          "a shipping container. You load cargo (your app + all dependencies) into a "
          "standardized container. Any ship (any computer) can carry it."),
        sp(),

        section("6.1 The Problem Docker Solves"),
        p("Without Docker, running the dashboard on someone else's computer requires:"),
        b("Install Python 3.11 exactly"),
        b("Create a virtual environment"),
        b("Install all packages from requirements.txt"),
        b("Clone the repo with the right folder structure"),
        b("Run the correct startup command"),
        sp(),
        p("With Docker, they just need Docker installed and one command:"),
        c("docker run -p 8501:8501 -e MONGO_URI='...' btsm10/gebeya-dashboard"),
        sp(),

        section("6.2 The Dockerfile Explained"),
        p("A Dockerfile is a recipe for building a Docker image. Each instruction "
          "creates a layer:"),
        sp(),
        c("FROM python:3.11-slim\n"
          "# Base: minimal Linux + Python 3.11. 'slim' = stripped down, smaller size.\n\n"
          "WORKDIR /app\n"
          "# Create /app folder inside container and work from there.\n\n"
          "COPY requirements.txt .\n"
          "RUN pip install --no-cache-dir -r requirements.txt\n"
          "# Install all packages. Done before copying code so Docker can cache this layer.\n\n"
          "COPY src/ ./src/\n"
          "COPY app/ ./app/\n"
          "# Copy only what's needed to run the dashboard.\n\n"
          "EXPOSE 8501\n"
          "# Open port 8501 so browser can reach the dashboard.\n\n"
          'CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501"]\n'
          "# Command that runs when container starts."),
        sp(),

        section("6.3 Docker Layers"),
        p("Each Dockerfile instruction creates a layer. Layers are cached — if you "
          "change only app/dashboard.py, Docker only rebuilds the layers after "
          "COPY app/ — reusing the Python installation layer. This makes rebuilds fast."),
        sp(),

        section("6.4 Docker Commands"),
        table([
            ["Command", "What it does"],
            ["docker build -t name .", "Build image from Dockerfile in current directory"],
            ["docker run -p 8501:8501 name", "Start container, map port 8501"],
            ["docker run -e VAR=value name", "Inject environment variable into container"],
            ["docker pull name:tag", "Download latest image from Docker Hub"],
            ["docker images", "List images stored on your machine"],
            ["docker ps", "List running containers"],
            ["docker stop ID", "Stop a running container"],
        ], col_widths=[6*cm, 10.5*cm]),
        sp(),

        section("6.5 ARM vs AMD — The Platform Problem"),
        p("Your Mac has an Apple Silicon chip (ARM64 architecture). GitHub Actions servers "
          "use Intel chips (AMD64 architecture). These are different instruction sets — "
          "a program compiled for one cannot run on the other without translation."),
        sp(),
        p("When the image was first built on GitHub Actions (AMD64) and run on your "
          "Mac (ARM64), Docker showed a platform mismatch warning and streamlit failed "
          "to start because the binary was compiled for the wrong architecture."),
        sp(),
        p("Fix: build the image for both platforms using Docker Buildx:"),
        c("- name: Set up QEMU\n  uses: docker/setup-qemu-action@v3\n\n"
          "- name: Set up Docker Buildx\n  uses: docker/setup-buildx-action@v3\n\n"
          "- name: Build and push\n  uses: docker/build-push-action@v5\n  with:\n"
          "    platforms: linux/amd64,linux/arm64\n    tags: btsm10/gebeya-dashboard:latest"),
        sp(),
        p("QEMU is an emulator that allows the AMD64 GitHub Actions server to compile "
          "code for ARM64. This produces a multi-platform image that works on Mac, "
          "Windows, and Linux."),
        sp(),

        section("6.6 Environment Variables in Docker"),
        p("A container is isolated — it doesn't see your Mac's environment variables. "
          "The -e flag injects values from outside:"),
        sp(),
        c("docker run -p 8501:8501 \\\n"
          "  -e MONGO_URI='mongodb+srv://user:pass@cluster.mongodb.net/' \\\n"
          "  btsm10/gebeya-dashboard"),
        sp(),
        p("Inside the container, os.environ.get('MONGO_URI') finds this value and "
          "the dashboard connects to Atlas. Without -e, MONGO_URI is empty and the "
          "loader falls back to local files (which don't exist inside the container)."),
        PageBreak(),
    ]

    # ── SECTION 7: TASK 5 ────────────────────────────────────────────────────
    story += [
        title("7. Task 5 — Infrastructure & CI/CD"),
        HR(),
        p("Task 5 covered the infrastructure and automation layer — the systems that "
          "build, test, deploy, and host the application automatically."),
        sp(),

        section("7.1 GitHub Actions — CI/CD Pipeline"),
        p("CI/CD stands for Continuous Integration / Continuous Deployment. "
          "Every time you push code to GitHub, a series of automated jobs run:"),
        sp(),
        b("CI (Continuous Integration): automatically test and validate new code"),
        b("CD (Continuous Deployment): automatically build and deploy if tests pass"),
        sp(),
        p("The complete pipeline on every push to main:"),
        sp(),
        c("git push origin main\n        |\n        ├── Flake8 Lint (9s)        → checks code style\n"
          "        ├── Docstring Tests (31s)   → checks documentation\n"
          "        ├── Unit Tests (85s)        → runs pytest with MONGO_URI\n"
          "        └── Build & Push Docker     → builds multi-platform image → Docker Hub"),
        sp(),

        section("7.2 GitHub Secrets"),
        p("Secrets are encrypted values stored in GitHub that your workflows can access "
          "but nobody can read — not even you can see them after saving. "
          "They are never exposed in logs or code."),
        sp(),
        table([
            ["Secret name", "Used by", "Value"],
            ["MONGO_URI", "Unit Tests workflow", "MongoDB Atlas connection string"],
            ["DOCKER_USERNAME", "Docker publish workflow", "btsm10"],
            ["DOCKER_PASSWORD", "Docker publish workflow", "Docker Hub password"],
        ], col_widths=[4*cm, 5*cm, 7.5*cm]),
        sp(),
        p("Secrets are accessed in workflows using double curly brace syntax:"),
        c("env:\n  MONGO_URI: ${{ secrets.MONGO_URI }}"),
        sp(),

        section("7.3 Terraform — Infrastructure as Code"),
        p("Terraform is a tool that lets you define cloud infrastructure in code files "
          "instead of clicking through web consoles. The entire infrastructure is "
          "described in .tf files and can be created or destroyed with commands."),
        sp(),
        table([
            ["Command", "What it does"],
            ["terraform init", "Download provider plugins (AWS, etc.)"],
            ["terraform validate", "Check syntax of .tf files"],
            ["terraform plan", "Preview what would be created/changed/destroyed"],
            ["terraform apply", "Actually create the infrastructure on AWS"],
            ["terraform destroy", "Destroy everything (careful — permanent)"],
        ], col_widths=[5*cm, 11.5*cm]),
        sp(),
        p("Our terraform/main.tf creates two AWS resources:"),
        b("EC2 t2.micro instance — a small virtual Linux server to run the app"),
        b("S3 bucket — cloud file storage (like Google Drive but for code/data)"),
        sp(),
        p("Terraform is validated and ready. Applying it requires an AWS account. "
          "AWS has a 12-month free tier that covers t2.micro and basic S3 usage, "
          "but requires a credit card to sign up."),
        sp(),

        section("7.4 What is AWS?"),
        p("Amazon Web Services (AWS) is Amazon's cloud computing platform — "
          "the world's largest. Instead of buying physical servers, you rent virtual "
          "servers, storage, databases, and hundreds of other services on demand. "
          "You pay only for what you use."),
        sp(),
        table([
            ["AWS Service", "What it is", "Our use"],
            ["EC2", "Virtual server (Elastic Compute Cloud)", "Run the Docker container"],
            ["S3", "File storage (Simple Storage Service)", "Store data files and artifacts"],
            ["IAM", "Identity and Access Management", "Control who can access what"],
        ], col_widths=[3*cm, 6*cm, 7.5*cm]),
        PageBreak(),
    ]

    # ── SECTION 8: MONGODB ATLAS ─────────────────────────────────────────────
    story += [
        title("8. MongoDB Atlas — Cloud Database"),
        HR(),
        p("MongoDB Atlas is the cloud-hosted version of MongoDB. Instead of running "
          "MongoDB on your Mac (which only you can access), Atlas runs it on servers "
          "in the cloud that anyone with credentials can reach — including GitHub Actions."),
        sp(),

        section("8.1 Why We Migrated to Atlas"),
        p("The GitHub Actions unit tests were failing because:"),
        b("Tests use SlackDataLoader which reads from anonymized/ folder"),
        b("anonymized/ is in .gitignore — never pushed to GitHub for privacy"),
        b("GitHub Actions clones the repo — no anonymized/ folder"),
        b("Tests crash: FileNotFoundError"),
        sp(),
        p("The solution: move the data to Atlas. GitHub Actions connects to Atlas "
          "using the MONGO_URI secret, gets the data, tests pass."),
        sp(),

        section("8.2 Atlas Setup Steps"),
        table([
            ["Step", "Action"],
            ["1", "Create free account at mongodb.com/atlas"],
            ["2", "Create free cluster (M0 Sandbox — 512MB, free forever)"],
            ["3", "Create database user: biniamtsiget_db_user"],
            ["4", "Network Access: allow 0.0.0.0/0 (any IP — needed for GitHub Actions)"],
            ["5", "Get connection string from Connect → Drivers → Python"],
            ["6", "Run migration script to load data from JSON files"],
        ], col_widths=[1.5*cm, 15*cm]),
        sp(),

        section("8.3 The Migration Script"),
        p("Instead of migrating from local MongoDB (which had no data), we loaded "
          "directly from the raw JSON files in anonymized/ into Atlas:"),
        sp(),
        c("# migrate_to_atlas.py\nclient = MongoClient(ATLAS_URI)\ndb = client['gebeya_slack']\n\n"
          "# Read JSON files\nfor channel in os.listdir('anonymized/'):\n"
          "    for json_file in channel_folder:\n        messages.append({...})\n\n"
          "# Upload to Atlas\ndb['messages'].drop()  # clear old data\n"
          "db['messages'].insert_many(messages)  # 20,011 documents"),
        sp(),
        p("Result: 20,011 messages, 8,900 replies, 5,017 reactions loaded to Atlas."),
        sp(),

        section("8.4 SSL Certificate Fix for Atlas Connection"),
        p("When first connecting to Atlas, an SSL error appeared:"),
        c("pymongo.errors.ServerSelectionTimeoutError: SSL: CERTIFICATE_VERIFY_FAILED"),
        sp(),
        p("Same root cause as the NLTK SSL issue — Python on macOS doesn't automatically "
          "use the system certificate store. Fixed by running the certificate installer:"),
        c('open "/Applications/Python 3.14/Install Certificates.command"'),
        sp(),
        p("This installed the certifi bundle and created a symlink. After this, pymongo "
          "can verify Atlas's SSL certificate and connect successfully."),
        sp(),

        section("8.5 How SlackDataLoader Uses Atlas"),
        p("The loader was updated to automatically detect whether Atlas is available:"),
        sp(),
        c("# src/config.py\ntry:\n    import streamlit as st\n"
          "    MONGO_URI = st.secrets.get('MONGO_URI', os.environ.get('MONGO_URI', ''))\n"
          "except Exception:\n    MONGO_URI = os.environ.get('MONGO_URI', '')\n\n"
          "# src/loader.py\ndef __init__(self):\n"
          "    self.source = 'mongo' if MONGO_URI else 'local'  # auto-detect"),
        sp(),
        table([
            ["Environment", "MONGO_URI set?", "Data source"],
            ["Local Mac (no env var)", "No", "Local JSON files in anonymized/"],
            ["GitHub Actions", "Yes (secret)", "MongoDB Atlas"],
            ["Docker container", "Yes (-e flag)", "MongoDB Atlas"],
            ["Streamlit Cloud", "Yes (st.secrets)", "MongoDB Atlas"],
        ], col_widths=[5*cm, 3*cm, 8.5*cm]),
        PageBreak(),
    ]

    # ── SECTION 9: STREAMLIT CLOUD ───────────────────────────────────────────
    story += [
        title("9. Streamlit Cloud — Public Deployment"),
        HR(),
        p("Streamlit Cloud (share.streamlit.io) is a free hosting service for Streamlit "
          "apps. It deploys directly from your GitHub repository — no servers to manage, "
          "no Docker to configure. Anyone with the URL can open the dashboard."),
        sp(),

        section("9.1 How It Works"),
        b("Connect your GitHub account to Streamlit Cloud"),
        b("Select your repository, branch, and the main Python file"),
        b("Streamlit Cloud clones your repo and installs requirements.txt"),
        b("Your app runs on Streamlit's servers and gets a public URL"),
        b("Every git push to main automatically redeploys the app"),
        sp(),

        section("9.2 Streamlit Secrets"),
        p("Streamlit Cloud has its own secrets manager — separate from GitHub Secrets. "
          "You add secrets in the Advanced Settings before deploying. They are stored "
          "encrypted on Streamlit's servers and injected via st.secrets:"),
        sp(),
        c("# In Streamlit Cloud secrets (TOML format):\nMONGO_URI = 'mongodb+srv://...'"),
        sp(),
        c("# In Python code:\nimport streamlit as st\nuri = st.secrets['MONGO_URI']"),
        sp(),

        section("9.3 Streamlit vs Docker — When to Use Each"),
        table([
            ["", "Streamlit Cloud", "Docker"],
            ["Best for", "Sharing dashboards publicly, demos", "Production apps, any language"],
            ["Setup", "Connect GitHub, click deploy", "Write Dockerfile, manage registry"],
            ["Cost", "Free for public repos", "Free image, hosting costs extra"],
            ["Access", "Public URL — anyone can open", "Need to run docker run command"],
            ["Auto-redeploy", "Yes — on every git push", "Only if CI/CD configured"],
            ["Data privacy", "Code is visible on GitHub", "Image on Docker Hub, data separate"],
        ], col_widths=[3*cm, 6.5*cm, 7*cm]),
        sp(),

        section("9.4 Issues Encountered"),
        p("Two errors were hit during Streamlit Cloud deployment:"),
        sp(),
        p("<b>Error 1: FileNotFoundError</b>"),
        c("d for d in os.listdir(self.data_path)"),
        p("Cause: MONGO_URI wasn't being read correctly. Streamlit uses st.secrets, "
          "not os.environ. Fix: updated config.py to try st.secrets first."),
        sp(),
        p("<b>Error 2: KeyError 'reactions'</b>"),
        c("df['reaction_count_clean'] = df['reactions'].apply(...)"),
        p("Cause: MongoDB messages collection doesn't have a 'reactions' column — "
          "we only stored reply_count during migration. Fix: added column existence check."),
        c("df['reaction_count_clean'] = (\n"
          "    df['reactions'].apply(...) if 'reactions' in df.columns else 0\n)"),
        PageBreak(),
    ]

    # ── SECTION 10: ALL MISTAKES AND FIXES ───────────────────────────────────
    story += [
        title("10. All Mistakes Made & How They Were Fixed"),
        HR(),
        p("Every error encountered during the project, what caused it, and how it was fixed. "
          "Understanding mistakes is as important as understanding the solutions."),
        sp(),

        table([
            ["Error", "Cause", "Fix"],
            ["gensim install failed\n(build wheel error)",
             "gensim requires C++ compiler and is hard to build on newer Python",
             "Switched to sklearn's LDA — same algorithm, easier install"],
            ["ModuleNotFoundError: nltk\n(in Jupyter)",
             "Jupyter was using system Python kernel, not gebvenv",
             "Registered gebvenv as Jupyter kernel with ipykernel install"],
            ["SSL: CERTIFICATE_VERIFY_FAILED\n(NLTK download)",
             "macOS Python doesn't use system certificate store",
             "Added ssl._create_unverified_context workaround in notebook"],
            ["SSL: CERTIFICATE_VERIFY_FAILED\n(MongoDB Atlas)",
             "Same SSL issue, pymongo can't verify Atlas certificate",
             "Ran Install Certificates.command — proper permanent fix"],
            ["terraform not found\n(after brew install)",
             "brew install terraform uses wrong formula",
             "Used brew install hashicorp/tap/terraform instead"],
            [".terraform/ committed to git",
             "Large provider binaries accidentally staged",
             "git rm -r --cached terraform/.terraform/ and added to .gitignore"],
            ["Flake8 CI failing",
             "Unused imports (pd, np), E402 warnings, line length",
             "Removed unused imports, added # noqa: E402, excluded generate_pdf.py"],
            ["pytest: unused import pytest\n(F401)",
             "import pytest was in test file but pytest is auto-imported",
             "Removed the unused import line"],
            ["migrate_to_atlas: no documents",
             "Local MongoDB had no data — gebeya_slack DB was empty",
             "Rewrote migration to load directly from JSON files instead"],
            ["Migration: type field missing",
             "Migration script stored 5 fields but forgot type",
             "Added type field to migration, re-ran migration"],
            ["Docker: streamlit not found",
             "streamlit and Pillow were missing from requirements.txt",
             "Added both packages to requirements.txt"],
            ["Docker: platform mismatch\n(ARM vs AMD)",
             "GitHub Actions builds AMD64, Mac is ARM64",
             "Updated workflow to build linux/amd64,linux/arm64 with buildx"],
            ["Docker: KeyError reactions",
             "reactions column not in MongoDB messages collection",
             "Added column existence check before accessing reactions"],
            ["Streamlit: FileNotFoundError",
             "Config.py used os.environ but Streamlit uses st.secrets",
             "Updated config.py to check st.secrets first, then os.environ"],
            ["pymongo not found\n(GitHub Actions)",
             "pymongo missing from requirements.txt",
             "Added pymongo to requirements.txt"],
        ], col_widths=[4*cm, 6*cm, 6.5*cm]),
        PageBreak(),
    ]

    # ── SECTION 11: QUESTIONS ASKED ──────────────────────────────────────────
    story += [
        title("11. Questions Asked & Answers"),
        HR(),
        p("Every conceptual question asked during the project, with detailed answers."),
        sp(),

        Paragraph("Q: What is gensim and why was it removed?", qa_q),
        Paragraph("Gensim is a natural language processing library that includes LDA topic modelling. "
                  "It was initially planned for topic modelling but failed to install because it requires "
                  "compiling C++ extensions, which is complex on newer Python versions. We switched to "
                  "scikit-learn's LDA implementation which is pure Python and installs easily.", qa_a),

        Paragraph("Q: What is sentiment analysis?", qa_q),
        Paragraph("Sentiment analysis determines the emotional tone of text — positive, negative, or neutral. "
                  "TextBlob assigns a polarity score from -1.0 (very negative) to +1.0 (very positive). "
                  "We used it to measure how the mood of the Gebeya Slack community changed over time.", qa_a),

        Paragraph("Q: Have we trained the model so far?", qa_q),
        Paragraph("Yes — the LDA topic model was the only genuine model training. Calling lda.fit(X) "
                  "trains the model on our Slack messages. TextBlob sentiment analysis used a pre-trained "
                  "model (no training done by us). Message classification was rule-based (no ML at all).", qa_a),

        Paragraph("Q: What is Homebrew?", qa_q),
        Paragraph("Homebrew is the package manager for macOS system tools — like an App Store for "
                  "developer software. You use it to install MongoDB, PostgreSQL, Terraform, etc. "
                  "It's different from pip: Homebrew installs system tools globally, pip installs "
                  "Python libraries inside a virtual environment.", qa_a),

        Paragraph("Q: Where on my Mac do I find Homebrew?", qa_q),
        Paragraph("Homebrew installs tools to /opt/homebrew/ on Apple Silicon Macs. You don't "
                  "find it as an app — you use it entirely from the terminal. Type 'brew list' "
                  "to see everything installed, 'brew services list' to see running services.", qa_a),

        Paragraph("Q: Does Homebrew work for both global and venv?", qa_q),
        Paragraph("Homebrew installs things globally on your Mac — available everywhere. "
                  "Virtual environments (gebvenv) only contain Python packages installed with pip. "
                  "They're separate systems: Homebrew for system tools, pip for Python libraries.", qa_a),

        Paragraph("Q: What happens when I save a Jupyter notebook?", qa_q),
        Paragraph("The .ipynb file saves everything: your code cells, output (charts, tables, "
                  "printed text), and metadata. It's a JSON file. All outputs are embedded inside "
                  "it — you don't need to run the code again to see previous results.", qa_a),

        Paragraph("Q: What does source utils do?", qa_q),
        Paragraph("'source' runs a shell script in the current terminal session. "
                  "'source gebvenv/bin/activate' runs the activation script which modifies "
                  "your PATH so Python points to gebvenv's Python instead of system Python.", qa_a),

        Paragraph("Q: What is __pycache__?", qa_q),
        Paragraph("__pycache__ contains compiled versions of your Python files (.pyc files). "
                  "Python compiles your source code to bytecode the first time it runs, then "
                  "reuses the cached version for faster subsequent runs. It's auto-managed — "
                  "you never need to touch it.", qa_a),

        Paragraph("Q: Doesn't __pycache__ make Python a compiled language?", qa_q),
        Paragraph("No — Python is still interpreted. The .pyc bytecode still needs the Python "
                  "interpreter to run. It's just a performance optimization. True compiled languages "
                  "(like C or Go) produce native machine code that runs without any interpreter.", qa_a),

        Paragraph("Q: Why did we use two databases?", qa_q),
        Paragraph("MongoDB (NoSQL) is flexible — perfect for raw, varied Slack JSON data where "
                  "each message can have different fields. PostgreSQL (SQL) is structured — "
                  "perfect for analytical queries with GROUP BY, aggregations, and joins. "
                  "They serve different purposes: MongoDB for storage, PostgreSQL for analytics.", qa_a),

        Paragraph("Q: Is it a good idea to index everything in MongoDB?", qa_q),
        Paragraph("No. Indexes speed up reads but slow down writes and use extra storage. "
                  "Only index fields you frequently filter or sort by. Over-indexing is a "
                  "common mistake that wastes resources.", qa_a),

        Paragraph("Q: What is Terraform?", qa_q),
        Paragraph("Terraform is Infrastructure as Code — instead of clicking through AWS console "
                  "to create servers and storage, you write .tf files describing what you want "
                  "and Terraform creates it. This makes infrastructure reproducible, version-controlled, "
                  "and easy to recreate after destroying.", qa_a),

        Paragraph("Q: What is Docker?", qa_q),
        Paragraph("Docker packages your app and all its dependencies into a container — a "
                  "self-contained unit that runs identically on any machine. The problem it "
                  "solves: 'it works on my machine but not yours'. With Docker, if it works "
                  "on your Mac, it works on the server.", qa_a),

        Paragraph("Q: What is AWS?", qa_q),
        Paragraph("Amazon Web Services is the world's largest cloud computing platform. "
                  "Instead of buying physical servers, you rent virtual ones on demand. "
                  "EC2 is their virtual server service, S3 is file storage. You pay only "
                  "for what you use, and there's a 12-month free tier for new accounts.", qa_a),

        Paragraph("Q: Can someone who has my repo run the dashboard on their device?", qa_q),
        Paragraph("Yes — they need Docker installed and one command: "
                  "docker run -p 8501:8501 -e MONGO_URI='your_atlas_string' btsm10/gebeya-dashboard. "
                  "Docker downloads the image from Docker Hub and runs it. No Python, no pip, "
                  "no virtual environments needed.", qa_a),

        Paragraph("Q: What are those layers when pulling from Docker Hub?", qa_q),
        Paragraph("Each Docker instruction in the Dockerfile creates a layer. When you pull an image, "
                  "each layer downloads separately. They're shown as hashes. If you pull an updated "
                  "image, Docker only downloads changed layers — reusing cached unchanged layers. "
                  "This makes updates much faster.", qa_a),

        Paragraph("Q: If there's no change to Docker and change is only in other files, should Docker be downloaded again?", qa_q),
        Paragraph("No — if the code inside the container didn't change, pulling again gets you "
                  "the exact same image. In a production setup, you'd configure the Docker workflow "
                  "to only trigger when src/, app/, requirements.txt, or Dockerfile changes. "
                  "For now, our workflow rebuilds on every push to main.", qa_a),

        Paragraph("Q: Is SlackDataLoader a class?", qa_q),
        Paragraph("Yes. It's defined with 'class SlackDataLoader:' and has three methods: "
                  "get_channels(), load_channel(), and load_all_channels(). Using a class "
                  "means data_path is set once in __init__ and all methods share it via self.", qa_a),

        Paragraph("Q: What does the MONGO_URI environment variable do?", qa_q),
        Paragraph("os.environ.get('MONGO_URI', '') reads a value stored in the operating system's "
                  "environment. If set, SlackDataLoader connects to MongoDB Atlas. If not set, "
                  "it falls back to reading local JSON files. This allows the same code to work "
                  "in all environments without any changes.", qa_a),

        Paragraph("Q: What are docstrings and unit tests in GitHub Actions?", qa_q),
        Paragraph("Docstrings are triple-quoted descriptions inside functions: '''Does X.''' "
                  "The docstring workflow checks all functions have them. Unit tests are small "
                  "code snippets that verify one function works correctly. The unit test workflow "
                  "runs pytest tests/ on every push. Together they enforce code quality automatically.", qa_a),

        Paragraph("Q: Is GitHub safe to give access to Streamlit?", qa_q),
        Paragraph("Yes. GitHub Secrets (MONGO_URI, DOCKER_PASSWORD) are encrypted and only accessible "
                  "to GitHub Actions — Streamlit cannot see them. Streamlit only reads your code files. "
                  "The MONGO_URI for Streamlit is stored separately in Streamlit's own secrets manager, "
                  "completely independent from GitHub Secrets.", qa_a),

        PageBreak(),
    ]

    # ── SECTION 12: FINAL ARCHITECTURE ───────────────────────────────────────
    story += [
        title("12. Final System Architecture"),
        HR(),
        p("The complete pipeline from raw data to publicly accessible dashboard:"),
        sp(),
        c("Raw Slack JSON files (anonymized/)\n"
          "           |\n"
          "           v\n"
          "  migrate_to_atlas.py\n"
          "           |\n"
          "           v\n"
          "  MongoDB Atlas (cloud)\n"
          "  gebeya_slack database\n"
          "  3 collections: messages, replies, reactions\n"
          "           |\n"
          "           v\n"
          "  SlackDataLoader (src/loader.py)\n"
          "  Auto-detects: Atlas if MONGO_URI set, else local JSON\n"
          "           |\n"
          "           v\n"
          "  Streamlit Dashboard (app/dashboard.py)\n"
          "  Packaged in Docker image: btsm10/gebeya-dashboard\n"
          "           |\n"
          "           ├──> Docker Hub (btsm10/gebeya-dashboard:latest)\n"
          "           |        Anyone: docker run -p 8501:8501 ...\n"
          "           |\n"
          "           └──> Streamlit Cloud (share.streamlit.io)\n"
          "                    Public URL — no setup needed"),
        sp(),
        table([
            ["Component", "Technology", "Status"],
            ["Data storage", "MongoDB Atlas (cloud)", "Live — 20,011 messages"],
            ["Data loading", "SlackDataLoader class", "Auto-detects Atlas or local"],
            ["Analysis", "pandas, sklearn, TextBlob, MLFlow", "Complete"],
            ["Dashboard", "Streamlit", "Running on Streamlit Cloud"],
            ["Containerization", "Docker (multi-platform)", "Image on Docker Hub"],
            ["Code style CI", "Flake8 GitHub Actions", "Passing"],
            ["Documentation CI", "Docstring checker", "Passing"],
            ["Testing CI", "pytest + MongoDB Atlas", "All 5 tests passing"],
            ["Cloud infrastructure", "Terraform (AWS EC2 + S3)", "Ready — needs AWS account"],
        ], col_widths=[4*cm, 6*cm, 6.5*cm]),
        sp(2),
        HR(),
        p("This document covers the complete Gebeya Week 1 Challenge — "
          "from raw JSON files to a live public dashboard with a full CI/CD pipeline. "
          "Every tool used, every concept explained, every mistake fixed."),
        sp(),
        Paragraph("Biniam Tsige · Gebeya Batch 6 · Data Engineering & ML Engineering",
                  ParagraphStyle("footer", fontSize=10, alignment=TA_CENTER,
                                 textColor=colors.HexColor("#555555"), fontName="Helvetica-Oblique")),
    ]

    doc.build(story)
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    build()
