"""Generate PowerPoint presentation for Task 1 and Task 2."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

OUTPUT = "Gebeya_Task1_Task2_Presentation.pptx"

# ── Colors ────────────────────────────────────────────────────────────────────
DARK_BLUE = RGBColor(0x1a, 0x1a, 0x2e)
MID_BLUE = RGBColor(0x16, 0x21, 0x3e)
ACCENT = RGBColor(0x0f, 0x34, 0x60)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF4, 0xF4, 0xF4)
GREEN = RGBColor(0x27, 0xAE, 0x60)
ORANGE = RGBColor(0xE6, 0x7E, 0x22)
RED = RGBColor(0xC0, 0x39, 0x2B)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # completely blank layout


# ── Helpers ───────────────────────────────────────────────────────────────────

def add_rect(slide, x, y, w, h, color):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_text(slide, text, x, y, w, h, size=24, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_bullet_box(slide, items, x, y, w, h, size=16, title=None, bg=None):
    if bg:
        add_rect(slide, x, y, w, h, bg)
    if title:
        add_text(slide, title, x + 0.1, y + 0.1, w - 0.2, 0.4,
                 size=14, bold=True, color=DARK_BLUE)
        y += 0.5
        h -= 0.5
    txBox = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.1),
                                     Inches(w - 0.3), Inches(h - 0.2))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = f"• {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = DARK_BLUE


def header_bar(slide, title, subtitle=None):
    add_rect(slide, 0, 0, 13.33, 1.3, DARK_BLUE)
    add_text(slide, title, 0.4, 0.1, 12, 0.7, size=32, bold=True,
             color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.4, 0.8, 12, 0.4, size=16,
                 color=RGBColor(0xAA, 0xBB, 0xCC), align=PP_ALIGN.LEFT)
    add_rect(slide, 0, 1.3, 13.33, 0.05, ACCENT)


def slide_number(slide, n, total):
    add_text(slide, f"{n} / {total}", 12.2, 7.1, 1, 0.35,
             size=11, color=RGBColor(0x99, 0x99, 0x99), align=PP_ALIGN.RIGHT)


TOTAL = 18


# ── SLIDE 1: Cover ────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, DARK_BLUE)
add_rect(s, 0, 2.8, 13.33, 0.08, ACCENT)
add_rect(s, 0, 4.7, 13.33, 0.08, ACCENT)
add_text(s, "Gebeya Week 1 Challenge", 0.5, 0.8, 12.3, 1,
         size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Slack Messages Analysis", 0.5, 1.9, 12.3, 0.8,
         size=28, color=RGBColor(0xAA, 0xBB, 0xFF), align=PP_ALIGN.CENTER)
add_rect(s, 0, 2.9, 13.33, 1.75, MID_BLUE)
add_text(s, "Task 1 — Exploratory Data Analysis", 0.5, 3.0, 12.3, 0.55,
         size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Task 2 — ML Analysis (LDA · Sentiment · Classification)", 0.5, 3.55, 12.3, 0.55,
         size=20, color=RGBColor(0xAA, 0xBB, 0xFF), align=PP_ALIGN.CENTER)
add_text(s, "Biniam Tsige  ·  Batch 6  ·  Data Engineering & ML Engineering",
         0.5, 4.85, 12.3, 0.5, size=16, color=RGBColor(0xCC, 0xCC, 0xCC), align=PP_ALIGN.CENTER)
add_text(s, "Gebeya Internship  ·  2026", 0.5, 5.4, 12.3, 0.5,
         size=14, color=RGBColor(0x99, 0x99, 0x99), align=PP_ALIGN.CENTER)
slide_number(s, 1, TOTAL)

# ── SLIDE 2: Agenda ───────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Agenda", "What we will cover today")
slide_number(s, 2, TOTAL)

items_t1 = [
    "Dataset overview — 20,011 messages, 39 channels",
    "SlackDataLoader class — how data is loaded",
    "Top & Bottom users — 4 metrics",
    "Channel activity scatter plot",
    "Reply time analysis",
    "CI/CD — GitHub Actions workflows",
]
items_t2 = [
    "Time difference histograms",
    "Rule-based message classification",
    "LDA Topic Modelling — real model training",
    "Sentiment analysis with TextBlob",
    "MLFlow experiment tracking",
    "Key findings",
]
add_rect(s, 0.3, 1.5, 6.1, 5.7, WHITE)
add_rect(s, 6.9, 1.5, 6.1, 5.7, WHITE)
add_text(s, "TASK 1 — EDA", 0.5, 1.6, 5.7, 0.5, size=16, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 2.1, 6.1, 0.05, ACCENT)
add_text(s, "TASK 2 — ML Analysis", 7.1, 1.6, 5.7, 0.5, size=16, bold=True, color=DARK_BLUE)
add_rect(s, 6.9, 2.1, 6.1, 0.05, ACCENT)
add_bullet_box(s, items_t1, 0.3, 2.2, 6.1, 4.9, size=14)
add_bullet_box(s, items_t2, 6.9, 2.2, 6.1, 4.9, size=14)

# ── SLIDE 3: Dataset Overview ─────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — Dataset Overview", "What data we worked with")
slide_number(s, 3, TOTAL)

for i, (num, label, color) in enumerate([
    ("20,011", "Total Messages", DARK_BLUE),
    ("39", "Channels", ACCENT),
    ("1,205+", "Unique Users", GREEN),
    ("8,900+", "Thread Replies", ORANGE),
]):
    x = 0.3 + i * 3.2
    add_rect(s, x, 1.6, 2.9, 2.2, color)
    add_text(s, num, x, 1.8, 2.9, 1.2, size=40, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, label, x, 2.9, 2.9, 0.6, size=16,
             color=WHITE, align=PP_ALIGN.CENTER)

add_rect(s, 0.3, 4.1, 12.7, 3.1, WHITE)
add_text(s, "Data Format & Privacy", 0.5, 4.2, 12, 0.4, size=14, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 4.6, 12.7, 0.04, LIGHT_GRAY)
add_bullet_box(s, [
    "Format: Slack JSON export — one file per channel per day",
    "Users anonymized — IDs like U03T89ACUUW instead of real names",
    "@mention tags stripped during anonymization",
    "NEVER pushed to GitHub — anonymized/ folder in .gitignore",
    "Loaded using custom SlackDataLoader class into pandas DataFrames",
], 0.3, 4.65, 12.7, 2.5, size=15)

# ── SLIDE 4: SlackDataLoader ──────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — SlackDataLoader Class", "Custom data loading architecture")
slide_number(s, 4, TOTAL)

add_rect(s, 0.3, 1.5, 5.8, 5.7, WHITE)
add_text(s, "What is a Class?", 0.5, 1.6, 5.4, 0.4, size=14, bold=True, color=DARK_BLUE)
add_bullet_box(s, [
    "A class is a blueprint that groups related functions together",
    "SlackDataLoader groups all data loading logic in one place",
    "Created once, used everywhere in the project",
    "",
    "3 methods:",
    "  get_channels() → list of 39 channel names",
    "  load_channel() → one channel as DataFrame",
    "  load_all_channels() → all channels combined",
    "",
    "Auto-detects data source:",
    "  MONGO_URI set → reads from MongoDB Atlas",
    "  Not set → reads from local JSON files",
], 0.3, 2.05, 5.8, 5.1, size=13)

add_rect(s, 6.5, 1.5, 6.5, 5.7, DARK_BLUE)
add_text(s, "class SlackDataLoader:", 6.65, 1.6, 6.2, 0.4, size=12, bold=True, color=GREEN)
code_lines = [
    ('    def __init__(self):', WHITE),
    ('        if MONGO_URI:', WHITE),
    ('            self.source = "mongo"', RGBColor(0xAA, 0xBB, 0xFF)),
    ('        else:', WHITE),
    ('            self.source = "local"', RGBColor(0xAA, 0xBB, 0xFF)),
    ('', WHITE),
    ('    def get_channels(self):', WHITE),
    ('        # returns 39 channel names', RGBColor(0x88, 0x88, 0x88)),
    ('        ...', WHITE),
    ('', WHITE),
    ('    def load_channel(self, ch):', WHITE),
    ('        # returns one DataFrame', RGBColor(0x88, 0x88, 0x88)),
    ('        ...', WHITE),
    ('', WHITE),
    ('    def load_all_channels(self):', WHITE),
    ('        # all channels combined', RGBColor(0x88, 0x88, 0x88)),
    ('        ...', WHITE),
]
txBox = s.shapes.add_textbox(Inches(6.55), Inches(2.05), Inches(6.2), Inches(5.1))
tf = txBox.text_frame
tf.word_wrap = False
for i, (line, color) in enumerate(code_lines):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    run = p.add_run()
    run.text = line if line else " "
    run.font.size = Pt(12)
    run.font.name = "Courier New"
    run.font.color.rgb = color

# ── SLIDE 5: Four Analysis Metrics ───────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — Four Analysis Dimensions", "How we measured user participation")
slide_number(s, 5, TOTAL)

metrics = [
    ("Message Count", "How many messages a user posted",
     "High = most active poster (quantity)", DARK_BLUE),
    ("Reply Count", "How many replies their messages received",
     "High = best conversation starter (impact)", ACCENT),
    ("Reaction Count", "How many emoji reactions their messages got",
     "High = most appreciated poster (quality)", GREEN),
    ("Mention Count", "How often they @mentioned others",
     "Showed ~0 — anonymization stripped mentions", ORANGE),
]
for i, (title_t, what, insight, color) in enumerate(metrics):
    row = i // 2
    col = i % 2
    x = 0.3 + col * 6.5
    y = 1.6 + row * 2.8
    add_rect(s, x, y, 6.2, 2.6, color)
    add_text(s, title_t, x + 0.1, y + 0.1, 6.0, 0.5, size=18, bold=True, color=WHITE)
    add_rect(s, x, y + 0.6, 6.2, 0.04, WHITE)
    add_text(s, f"What: {what}", x + 0.15, y + 0.7, 5.9, 0.5, size=13, color=WHITE)
    add_text(s, f"Insight: {insight}", x + 0.15, y + 1.3, 5.9, 0.9, size=13,
             color=RGBColor(0xFF, 0xFF, 0xAA))

# ── SLIDE 6: Top/Bottom Users Finding ────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — Top vs Bottom Users", "What the bar charts revealed")
slide_number(s, 6, TOTAL)

add_rect(s, 0.3, 1.5, 12.7, 1.8, WHITE)
add_text(s, "Key Insight: Quantity ≠ Quality", 0.5, 1.6, 12, 0.5, size=18, bold=True, color=DARK_BLUE)
add_text(s, "A user can post many messages but receive zero reactions. Another user can post rarely "
          "but spark huge discussions. These 4 metrics reveal very different stories about participation.",
         0.5, 2.1, 12.3, 1.0, size=14, color=DARK_BLUE)

for i, (label, top, bottom, color) in enumerate([
    ("By Messages", "Posted the most — highest volume", "Posted the least — lurkers", DARK_BLUE),
    ("By Replies", "Sparked most discussions", "Posts got no responses", ACCENT),
    ("By Reactions", "Most appreciated posts", "Posts went unnoticed", GREEN),
]):
    x = 0.3 + i * 4.35
    add_rect(s, x, 3.5, 4.1, 3.7, color)
    add_text(s, label, x + 0.1, 3.6, 3.9, 0.5, size=15, bold=True, color=WHITE)
    add_rect(s, x, 4.1, 4.1, 0.04, WHITE)
    add_text(s, "Top 10:", x + 0.15, 4.2, 3.8, 0.35, size=12, bold=True, color=RGBColor(0xFF, 0xFF, 0xAA))
    add_text(s, top, x + 0.15, 4.55, 3.8, 0.6, size=12, color=WHITE)
    add_text(s, "Bottom 10:", x + 0.15, 5.3, 3.8, 0.35, size=12, bold=True, color=RGBColor(0xFF, 0xAA, 0xAA))
    add_text(s, bottom, x + 0.15, 5.65, 3.8, 0.8, size=12, color=WHITE)

# ── SLIDE 7: Channel Activity ─────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — Channel Activity Analysis", "Messages vs Engagement scatter plot")
slide_number(s, 7, TOTAL)

add_rect(s, 0.3, 1.5, 7.5, 5.7, WHITE)
add_text(s, "Scatter Plot", 0.5, 1.6, 7.1, 0.4, size=14, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 2.0, 7.5, 0.04, LIGHT_GRAY)
add_text(s, "X-axis: Number of messages per channel", 0.5, 2.1, 7.1, 0.4, size=12, color=DARK_BLUE)
add_text(s, "Y-axis: Total replies + reactions (engagement)", 0.5, 2.5, 7.1, 0.4, size=12, color=DARK_BLUE)
add_text(s, "Each dot = one Slack channel", 0.5, 2.9, 7.1, 0.4, size=12, color=DARK_BLUE)
add_rect(s, 1.0, 3.5, 5.5, 3.3, RGBColor(0xF0, 0xF0, 0xF8))
add_text(s, "ai-community-building ●", 5.2, 3.6, 2.5, 0.4, size=11,
         color=ORANGE, align=PP_ALIGN.RIGHT)
add_text(s, "~8,500 messages\n~11,000 engagement", 5.2, 3.95, 2.5, 0.6,
         size=10, color=DARK_BLUE, align=PP_ALIGN.RIGHT)
add_text(s, "All other channels\nclustered here →", 1.5, 5.8, 3.0, 0.6,
         size=11, color=ACCENT)

add_rect(s, 8.1, 1.5, 4.9, 5.7, DARK_BLUE)
add_text(s, "What This Means", 8.25, 1.6, 4.6, 0.4, size=14, bold=True, color=WHITE)
add_rect(s, 8.1, 2.05, 4.9, 0.04, ACCENT)
add_bullet_box(s, [
    "Long-tail distribution",
    "",
    "ONE channel dominates all activity",
    "ai-community-building had 8,500+ messages and 11,000+ reactions",
    "",
    "All 38 other channels had very low activity in comparison",
    "",
    "Implication: this single channel is where the community lives. Understanding it gives the most signal about what people discuss.",
], 8.1, 2.15, 4.9, 5.0, size=12)

# ── SLIDE 8: Reply Time Analysis ──────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — Reply Time Analysis", "How quickly does the community respond?")
slide_number(s, 8, TOTAL)

add_rect(s, 0.3, 1.5, 3.9, 5.7, WHITE)
add_text(s, "How to Read the Chart", 0.5, 1.6, 3.5, 0.4, size=13, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 2.05, 3.9, 0.04, LIGHT_GRAY)
add_bullet_box(s, [
    "X-axis: Minutes to first reply",
    "Y-axis: Hour of day (0-24)",
    "Each dot: one message",
    "Red line: 5-minute mark",
    "",
    "Dots LEFT of red line = fast response (under 5 min)",
    "",
    "Dots RIGHT = slow response (hours later)",
], 0.3, 2.15, 3.9, 5.0, size=13)

for i, (label, median, color, finding) in enumerate([
    ("Consecutive Messages", "0.6 min", DARK_BLUE, "Messages come in rapid bursts"),
    ("Consecutive Replies", "0.8 min", ACCENT, "Thread replies also very fast"),
    ("Consecutive Reactions", "1.4 min", GREEN, "Reading before clicking emoji"),
    ("Reply → First Response", "< 5 min", ORANGE, "Most responses within 5 minutes"),
]):
    x = 4.5
    y = 1.5 + i * 1.42
    add_rect(s, x, y, 8.5, 1.3, color)
    add_text(s, label, x + 0.15, y + 0.1, 5.0, 0.45, size=14, bold=True, color=WHITE)
    add_text(s, f"Median: {median}", x + 0.15, y + 0.55, 2.5, 0.4, size=13, color=WHITE)
    add_text(s, finding, x + 3.5, y + 0.1, 4.8, 1.1, size=13,
             color=RGBColor(0xFF, 0xFF, 0xAA))

# ── SLIDE 9: CI/CD ────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 1 — CI/CD with GitHub Actions", "Automatic quality checks on every push")
slide_number(s, 9, TOTAL)

add_rect(s, 0.3, 1.5, 12.7, 1.5, WHITE)
add_text(s, "Every git push triggers:", 0.5, 1.6, 12, 0.4, size=14, bold=True, color=DARK_BLUE)
add_text(s, "git push → GitHub → 4 workflows run automatically → green = safe to merge",
         0.5, 2.05, 12, 0.6, size=13, color=DARK_BLUE)

workflows = [
    ("Flake8 Lint", "9s", "Checks PEP 8 code style. No unused imports, max line length 100, proper spacing.", GREEN, "✓ Passing"),
    ("Docstring Tests", "31s", "Every function and class must have a docstring explaining what it does.", GREEN, "✓ Passing"),
    ("Unit Tests", "85s", "Runs 5 pytest tests connecting to MongoDB Atlas via MONGO_URI secret.", GREEN, "✓ Passing"),
    ("Docker Build & Push", "5 min", "Builds multi-platform image (ARM + AMD) and pushes to Docker Hub.", GREEN, "✓ Passing"),
]
for i, (name, duration, desc, color, status) in enumerate(workflows):
    x = 0.3 + i * 3.2
    y = 3.2
    add_rect(s, x, y, 3.0, 4.0, DARK_BLUE)
    add_rect(s, x, y, 3.0, 0.7, color)
    add_text(s, name, x + 0.1, y + 0.05, 2.8, 0.4, size=13, bold=True, color=WHITE)
    add_text(s, duration, x + 0.1, y + 0.45, 2.8, 0.25, size=11, color=WHITE)
    add_text(s, desc, x + 0.1, y + 0.8, 2.8, 2.5, size=11, color=WHITE)
    add_text(s, status, x + 0.1, y + 3.5, 2.8, 0.35, size=12, bold=True, color=GREEN)

# ── SLIDE 10: Task 2 Intro ────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, DARK_BLUE)
add_rect(s, 0, 3.5, 13.33, 0.08, ACCENT)
add_text(s, "Task 2", 0.5, 0.8, 12.3, 1.2, size=56, bold=True,
         color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "ML Analysis", 0.5, 2.0, 12.3, 0.8, size=32,
         color=RGBColor(0xAA, 0xBB, 0xFF), align=PP_ALIGN.CENTER)
add_rect(s, 0, 2.9, 13.33, 0.08, ACCENT)
add_rect(s, 0, 3.0, 13.33, 0.6, MID_BLUE)

for i, label in enumerate(["Time Histograms", "Message Classification", "LDA Topic Model", "Sentiment Analysis", "MLFlow Tracking"]):
    add_text(s, label, 0.5 + i * 2.55, 3.1, 2.4, 0.4, size=12,
             color=WHITE, align=PP_ALIGN.CENTER)

add_bullet_box(s, [
    "The only REAL model training in this project: LDA (Latent Dirichlet Allocation)",
    "TextBlob sentiment uses a PRE-TRAINED model — no training by us",
    "Message classification is RULE-BASED — if/else logic, no ML at all",
    "MLFlow tracks every experiment — parameters, results, model versions",
], 0.5, 3.8, 12.3, 3.3, size=16)
slide_number(s, 10, TOTAL)

# ── SLIDE 11: Time Histograms ─────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 2 — Time Difference Histograms", "How fast does the community move?")
slide_number(s, 11, TOTAL)

add_rect(s, 0.3, 1.5, 8.0, 5.7, WHITE)
add_text(s, "What is a Histogram?", 0.5, 1.6, 7.6, 0.4, size=13, bold=True, color=DARK_BLUE)
add_text(s, "A histogram shows how frequently values fall into ranges (bins). "
          "X-axis = time gap in minutes (capped at 120). Y-axis = how many times that gap occurred. "
          "The huge spike at 0 means most events happened within seconds of each other.",
         0.5, 2.05, 7.6, 1.1, size=12, color=DARK_BLUE)
add_rect(s, 0.3, 3.2, 8.0, 0.04, LIGHT_GRAY)

hists = [
    ("Consecutive Messages", "0.6 min", "Messages come in rapid bursts — community is live chatting", DARK_BLUE),
    ("Consecutive Replies", "0.8 min", "Thread replies also fast — active discussion happening", ACCENT),
    ("Consecutive Reactions", "1.4 min", "Slightly slower — people read before clicking emoji", GREEN),
    ("All Events Combined", "0.6 min", "Overall: community rhythm is very fast-paced", ORANGE),
]
for i, (name, median, desc, color) in enumerate(hists):
    y = 3.3 + i * 0.95
    add_rect(s, 0.5, y, 0.3, 0.8, color)
    add_text(s, name, 0.9, y + 0.05, 3.5, 0.35, size=12, bold=True, color=DARK_BLUE)
    add_text(s, f"Median: {median}  |  {desc}", 0.9, y + 0.4, 7.0, 0.4, size=11, color=DARK_BLUE)

add_rect(s, 8.6, 1.5, 4.4, 5.7, DARK_BLUE)
add_text(s, "Key Takeaway", 8.8, 1.6, 4.0, 0.4, size=14, bold=True, color=WHITE)
add_rect(s, 8.6, 2.05, 4.4, 0.04, ACCENT)
add_bullet_box(s, [
    "The community was highly active in real-time bursts",
    "",
    "Median gap between messages: only 0.6 minutes",
    "",
    "This means people were online simultaneously — live conversation, not asynchronous",
    "",
    "The spike at 120 min = all gaps over 2 hours grouped together (off-hours messages)",
], 8.6, 2.15, 4.4, 5.0, size=12)

# ── SLIDE 12: Message Classification ─────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 2 — Message Classification", "Rule-based categorization (no ML)")
slide_number(s, 12, TOTAL)

add_rect(s, 0.3, 1.5, 5.5, 5.7, WHITE)
add_text(s, "The Logic", 0.5, 1.6, 5.1, 0.4, size=13, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 2.05, 5.5, 0.04, LIGHT_GRAY)
txBox = s.shapes.add_textbox(Inches(0.4), Inches(2.1), Inches(5.3), Inches(5.0))
tf = txBox.text_frame
tf.word_wrap = True
code_text = [
    ("def classify_message(text):", GREEN),
    ("    tech = any(kw in text", WHITE),
    ("             for kw in TECH_KEYWORDS)", WHITE),
    ("    if '?' in text or 'how' in text:", WHITE),
    ("        if tech:", WHITE),
    ("            return 'Question-Technical'", RGBColor(0xAA, 0xBB, 0xFF)),
    ("        return 'Question-NonTechnical'", RGBColor(0xAA, 0xBB, 0xFF)),
    ("    if text.startswith('yes','no'):", WHITE),
    ("        return 'Answer'", RGBColor(0xAA, 0xBB, 0xFF)),
    ("    if tech:", WHITE),
    ("        return 'Comment-Technical'", RGBColor(0xAA, 0xBB, 0xFF)),
    ("    return 'Comment-NonTechnical'", RGBColor(0xAA, 0xBB, 0xFF)),
]
for i, (line, color) in enumerate(code_text):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    run = p.add_run()
    run.text = line
    run.font.size = Pt(11)
    run.font.name = "Courier New"
    run.font.color.rgb = color

categories = [
    ("Question-Technical", "Has ? + tech keyword", DARK_BLUE),
    ("Question-NonTechnical", "Has ? but no tech keyword", ACCENT),
    ("Answer", "Starts with yes/no/sure", GREEN),
    ("Comment-Technical", "Has tech keyword", ORANGE),
    ("Comment-NonTechnical", "General comment", RED),
    ("Other", "Empty or unclear", RGBColor(0x77, 0x77, 0x77)),
]
add_text(s, "6 Categories", 6.1, 1.6, 6.9, 0.4, size=13, bold=True, color=DARK_BLUE)
add_rect(s, 6.1, 2.05, 6.9, 0.04, LIGHT_GRAY)
for i, (cat, desc, color) in enumerate(categories):
    x = 6.1 + (i % 2) * 3.5
    y = 2.2 + (i // 2) * 1.7
    add_rect(s, x, y, 3.2, 1.55, color)
    add_text(s, cat, x + 0.1, y + 0.1, 3.0, 0.5, size=12, bold=True, color=WHITE)
    add_text(s, desc, x + 0.1, y + 0.6, 3.0, 0.7, size=11, color=WHITE)

# ── SLIDE 13: LDA Topic Modelling ─────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 2 — LDA Topic Modelling", "The ONLY real model training in this project")
slide_number(s, 13, TOTAL)

add_rect(s, 0.3, 1.5, 8.2, 5.7, WHITE)
add_text(s, "How LDA Works — Step by Step", 0.5, 1.6, 7.8, 0.4, size=13, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 2.05, 8.2, 0.04, LIGHT_GRAY)

steps = [
    ("Step 1", "CountVectorizer",
     "Converts all 20,011 messages into a word-count matrix.\n"
     "Rows = messages, Columns = words, Cells = word frequency.\n"
     "Learns vocabulary FROM our data (fit).", DARK_BLUE),
    ("Step 2", "LDA.fit(X)",
     "Analyzes which words appear together across messages.\n"
     "Groups co-occurring words into topics.\n"
     "THIS is the actual model training.", GREEN),
    ("Step 3", "Topics discovered",
     "Each topic = a distribution of words.\n"
     "Example: 'python, error, install, pip' → Technical Help topic\n"
     "Example: 'week, task, submit, deadline' → Coursework topic", ACCENT),
]
for i, (num, name, desc, color) in enumerate(steps):
    y = 2.2 + i * 1.65
    add_rect(s, 0.4, y, 0.8, 1.45, color)
    add_text(s, num, 0.4, y + 0.1, 0.8, 0.5, size=13, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, name, 1.3, y + 0.05, 6.9, 0.4, size=13, bold=True, color=DARK_BLUE)
    add_text(s, desc, 1.3, y + 0.5, 6.9, 1.0, size=11, color=DARK_BLUE)

add_rect(s, 8.8, 1.5, 4.2, 5.7, DARK_BLUE)
add_text(s, "Key Concepts", 9.0, 1.6, 3.8, 0.4, size=14, bold=True, color=WHITE)
add_rect(s, 8.8, 2.05, 4.2, 0.04, ACCENT)
add_bullet_box(s, [
    "UNSUPERVISED learning",
    "No labels needed — topics discovered automatically",
    "",
    "vs TextBlob sentiment:",
    "TextBlob = PRE-TRAINED",
    "Someone else trained it",
    "We just applied it",
    "",
    "vs Rule-based classifier:",
    "No ML at all — just if/else",
    "",
    "5 topics extracted from 20,011 Slack messages",
], 8.8, 2.15, 4.2, 5.0, size=12)

# ── SLIDE 14: Sentiment Analysis ─────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 2 — Sentiment Analysis", "How did community mood change over time?")
slide_number(s, 14, TOTAL)

add_rect(s, 0.3, 1.5, 5.8, 5.7, WHITE)
add_text(s, "What is Sentiment Analysis?", 0.5, 1.6, 5.4, 0.4, size=13, bold=True, color=DARK_BLUE)
add_rect(s, 0.3, 2.05, 5.8, 0.04, LIGHT_GRAY)
add_bullet_box(s, [
    "Measures emotional tone of text",
    "Score range: -1.0 to +1.0",
    "",
    "+1.0 = very positive",
    " 0.0 = neutral",
    "-1.0 = very negative",
    "",
    "TextBlob uses a pre-trained word dictionary",
    "Each word has a pre-assigned sentiment score",
    "We did NOT train this — we applied it",
    "",
    "We scored every message daily then plotted the trend over time",
], 0.3, 2.15, 5.8, 5.0, size=13)

add_rect(s, 6.4, 1.5, 6.6, 2.7, DARK_BLUE)
add_text(s, "Example Scores", 6.6, 1.6, 6.2, 0.4, size=13, bold=True, color=WHITE)
examples = [
    ('"Great work everyone!"', '+0.8 ✓ Positive', GREEN),
    ('"Nothing works, broken"', '-0.4 ✗ Negative', RED),
    ('"See you tomorrow"', '0.0 Neutral', RGBColor(0xAA, 0xAA, 0xAA)),
]
for i, (text, score, color) in enumerate(examples):
    y = 2.05 + i * 0.7
    add_text(s, text, 6.6, y + 0.15, 3.8, 0.4, size=11, color=WHITE, italic=True)
    add_text(s, score, 10.5, y + 0.15, 2.3, 0.4, size=12, bold=True,
             color=color, align=PP_ALIGN.RIGHT)

add_rect(s, 6.4, 4.4, 6.6, 2.8, WHITE)
add_text(s, "What We Found", 6.6, 4.5, 6.2, 0.4, size=13, bold=True, color=DARK_BLUE)
add_rect(s, 6.4, 4.95, 6.6, 0.04, LIGHT_GRAY)
add_bullet_box(s, [
    "Plotted average daily sentiment over time",
    "Used Savitzky-Golay filter for smoothing",
    "Community showed generally positive sentiment",
    "Some dips near deadlines or submission weeks",
    "Trend line shows overall mood trajectory",
], 6.4, 5.0, 6.6, 2.15, size=13)

# ── SLIDE 15: MLFlow ──────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Task 2 — MLFlow Experiment Tracking", "Recording every model run for reproducibility")
slide_number(s, 15, TOTAL)

add_rect(s, 0.3, 1.5, 12.7, 1.3, WHITE)
add_text(s, "What is MLFlow?", 0.5, 1.6, 12, 0.4, size=14, bold=True, color=DARK_BLUE)
add_text(s, "MLFlow is like a lab notebook for machine learning. Every time the LDA model trains, "
          "it automatically records the settings used and the results produced.",
         0.5, 2.0, 12.3, 0.6, size=13, color=DARK_BLUE)

concepts = [
    ("Experiment", "A named project\ne.g. 'LDA Topic Modelling'", DARK_BLUE),
    ("Run", "One execution with\nspecific parameters", ACCENT),
    ("Parameters", "Settings used:\nn_topics=5, max_features=1000", GREEN),
    ("Artifacts", "Files saved:\nmodel, vectorizer, charts", ORANGE),
]
for i, (name, desc, color) in enumerate(concepts):
    x = 0.3 + i * 3.2
    add_rect(s, x, 3.0, 3.0, 2.5, color)
    add_text(s, name, x + 0.1, 3.1, 2.8, 0.5, size=15, bold=True, color=WHITE)
    add_text(s, desc, x + 0.1, 3.65, 2.8, 1.7, size=12, color=WHITE)

add_rect(s, 0.3, 5.7, 12.7, 1.6, DARK_BLUE)
add_text(s, "Why MLFlow matters:", 0.5, 5.8, 3, 0.4, size=13, bold=True, color=WHITE)
add_text(s, "If you run LDA with 5 topics today and 10 topics next week, MLFlow keeps both results. "
          "You can compare them, roll back to a previous version, and prove exactly which settings "
          "produced which results. Essential for reproducible ML research.",
         3.8, 5.8, 9.1, 1.3, size=12, color=WHITE)

# ── SLIDE 16: Key Findings ────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Key Findings — Task 1 & Task 2", "What the analysis revealed about the community")
slide_number(s, 16, TOTAL)

findings = [
    ("ai-community-building dominates", DARK_BLUE,
     "One channel had 8,500+ messages and 11,000+ engagement — far beyond all 38 other channels combined. Long-tail distribution."),
    ("Community is highly responsive", ACCENT,
     "Median reply time: 0.6 minutes. Most messages that received replies got them within 5 minutes. Very active during peak hours."),
    ("Mention data unavailable", GREEN,
     "Anonymization stripped @mention tags. All users show ~0 mention count. This is expected and correct."),
    ("Sentiment generally positive", ORANGE,
     "TextBlob showed the community maintained positive sentiment overall, with minor dips near deadline periods."),
    ("5 distinct topics emerged", RED,
     "LDA discovered 5 natural topic clusters without any human labeling — technical help, coursework, community building, sharing resources, and discussions."),
    ("High-volume ≠ High-impact", RGBColor(0x5D, 0x6D, 0x7E),
     "Top posters by message count often differed from top posters by reactions. Quantity and quality are independent metrics."),
]
for i, (title_t, color, desc) in enumerate(findings):
    col = i % 2
    row = i // 2
    x = 0.3 + col * 6.5
    y = 1.55 + row * 1.9
    add_rect(s, x, y, 6.2, 1.75, color)
    add_text(s, title_t, x + 0.15, y + 0.1, 5.9, 0.45, size=13, bold=True, color=WHITE)
    add_text(s, desc, x + 0.15, y + 0.6, 5.9, 1.0, size=11, color=WHITE)

# ── SLIDE 17: Technical Stack ─────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, LIGHT_GRAY)
header_bar(s, "Technology Stack — Task 1 & Task 2", "Every tool used and why")
slide_number(s, 17, TOTAL)

tools = [
    ("Python 3.14", "Programming language", DARK_BLUE),
    ("pandas", "DataFrame manipulation\nand data cleaning", DARK_BLUE),
    ("matplotlib\nseaborn", "Chart and graph\ngeneration", ACCENT),
    ("scikit-learn", "LDA topic modelling\n(CountVectorizer + LDA)", ACCENT),
    ("TextBlob", "Pre-trained sentiment\nanalysis", GREEN),
    ("NLTK", "Stopwords and\ntokenization", GREEN),
    ("MLFlow", "Experiment tracking\nand model versioning", ORANGE),
    ("pytest", "5 unit tests for\nSlackDataLoader", ORANGE),
    ("GitHub Actions", "CI/CD: Flake8,\ndocstrings, unit tests", RED),
    ("MongoDB Atlas", "Cloud database for\ntest data access", RED),
]
for i, (name, desc, color) in enumerate(tools):
    col = i % 5
    row = i // 5
    x = 0.3 + col * 2.55
    y = 1.55 + row * 2.8
    add_rect(s, x, y, 2.35, 2.5, color)
    add_text(s, name, x + 0.1, y + 0.15, 2.15, 0.7, size=13, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, desc, x + 0.1, y + 0.95, 2.15, 1.35, size=11,
             color=WHITE, align=PP_ALIGN.CENTER)

# ── SLIDE 18: Thank You ───────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, 13.33, 7.5, DARK_BLUE)
add_rect(s, 0, 3.2, 13.33, 0.08, ACCENT)
add_text(s, "Thank You", 0.5, 0.7, 12.3, 1.5, size=56, bold=True,
         color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Questions?", 0.5, 2.2, 12.3, 0.8, size=28,
         color=RGBColor(0xAA, 0xBB, 0xFF), align=PP_ALIGN.CENTER)
add_rect(s, 0, 3.3, 13.33, 1.5, MID_BLUE)
add_text(s, "Biniam Tsige  ·  Gebeya Batch 6  ·  Data Engineering & ML Engineering",
         0.5, 3.4, 12.3, 0.6, size=16, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "github.com/BTSM10/Gebeya-Tech",
         0.5, 4.0, 12.3, 0.5, size=14,
         color=RGBColor(0xAA, 0xBB, 0xFF), align=PP_ALIGN.CENTER)

add_bullet_box(s, [
    "Task 1: EDA — SlackDataLoader · Top/Bottom users · Channel activity · Reply time analysis",
    "Task 2: ML — Time histograms · Classification · LDA training · TextBlob sentiment · MLFlow",
    "All 5 unit tests passing · 4 CI/CD workflows green · Dashboard live on Streamlit Cloud",
], 0.5, 5.0, 12.3, 2.3, size=14)
slide_number(s, 18, TOTAL)

prs.save(OUTPUT)
print(f"Presentation saved: {OUTPUT}")
