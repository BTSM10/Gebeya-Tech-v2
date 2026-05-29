import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib.pyplot as plt  # noqa: E402
import streamlit as st  # noqa: E402
from PIL import Image  # noqa: E402

from src.loader import SlackDataLoader  # noqa: E402
from src.utils import add_time_columns  # noqa: E402

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Gebeya Slack Analysis",
    page_icon="📊",
    layout="wide"
)


# ── Load data (cached so it only runs once) ───────────────────
@st.cache_data
def load_data():
    loader = SlackDataLoader()
    df_raw = loader.load_all_channels()
    df = add_time_columns(df_raw.copy())
    df = df[df['type'] == 'message'].copy()
    df = df[df['text'].notna() & (df['text'].str.strip() != '')].copy()
    if 'subtype' in df.columns:
        df = df[~df['subtype'].isin(
            ['channel_join', 'channel_leave', 'bot_message']
        )].copy()

    df['reply_count_clean'] = (
        df['reply_count'].fillna(0).astype(int)
        if 'reply_count' in df.columns else 0
    )
    df['reaction_count_clean'] = df['reactions'].apply(
        lambda r: sum(x.get('count', 1) for x in r) if isinstance(r, list) else 0
    )
    df['mention_count'] = df['text'].apply(
        lambda t: len(re.findall(r'<@U[A-Z0-9]+>', str(t)))
    )
    return df


df = load_data()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("📊 Gebeya Slack Analysis")
st.sidebar.markdown("**Batch 6 — Week 1 Challenge**")
st.sidebar.markdown("---")

channels = ["All Channels"] + sorted(df['channel'].unique().tolist())
selected_channel = st.sidebar.selectbox("Filter by channel", channels)

if selected_channel != "All Channels":
    df_view = df[df['channel'] == selected_channel].copy()
else:
    df_view = df.copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Messages:** {len(df_view):,}")
st.sidebar.markdown(f"**Channels:** {df_view['channel'].nunique()}")
st.sidebar.markdown(f"**Users:** {df_view['user'].nunique()}")

# ── Title ─────────────────────────────────────────────────────
st.title("📊 Gebeya Slack Messages — Analysis Dashboard")
st.markdown("Interactive dashboard showing results from Task 1 (EDA) and Task 2 (ML Analysis).")
st.markdown("---")

# ── Section 1: Key Metrics ────────────────────────────────────
st.header("1. Key Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Messages", f"{len(df_view):,}")
col2.metric("Channels", f"{df_view['channel'].nunique()}")
col3.metric("Unique Users", f"{df_view['user'].nunique()}")
col4.metric("Total Reactions", f"{df_view['reaction_count_clean'].sum():,}")

st.markdown("---")

# ── Section 2: Top & Bottom Users ────────────────────────────
st.header("2. Top & Bottom Users")

tab1, tab2, tab3, tab4 = st.tabs([
    "By Messages", "By Replies", "By Reactions", "By Mentions"
])


def make_user_bar(df_view, col, label, n=10):
    agg = df_view.groupby('user')[col].sum().reset_index()
    agg.columns = ['user', label]
    agg['user_short'] = agg['user'].str[:10] + '...'
    top = agg.nlargest(n, label)
    bot = agg.nsmallest(n, label)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].barh(top['user_short'][::-1], top[label][::-1], color='#4C72B0')
    axes[0].set_title(f'Top {n} Users by {label}', fontweight='bold')
    axes[0].set_xlabel(label)

    axes[1].barh(bot['user_short'][::-1], bot[label][::-1], color='#C44E52')
    axes[1].set_title(f'Bottom {n} Users by {label}', fontweight='bold')
    axes[1].set_xlabel(label)

    plt.tight_layout()
    return fig


with tab1:
    df_view['msg_count'] = 1
    st.pyplot(make_user_bar(df_view, 'msg_count', 'Message Count'))

with tab2:
    st.pyplot(make_user_bar(df_view, 'reply_count_clean', 'Reply Count'))

with tab3:
    st.pyplot(make_user_bar(df_view, 'reaction_count_clean', 'Reaction Count'))

with tab4:
    st.pyplot(make_user_bar(df_view, 'mention_count', 'Mention Count'))

st.markdown("---")

# ── Section 3: Channel Activity ───────────────────────────────
st.header("3. Channel Activity")

channel_agg = df.groupby('channel').agg(
    message_count=('ts', 'count'),
    total_replies=('reply_count_clean', 'sum'),
    total_reactions=('reaction_count_clean', 'sum'),
).reset_index()
channel_agg['engagement'] = channel_agg['total_replies'] + channel_agg['total_reactions']

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(
    channel_agg['message_count'],
    channel_agg['engagement'],
    alpha=0.7,
    s=80,
    c=range(len(channel_agg)),
    cmap='tab20'
)
for _, row in channel_agg.nlargest(5, 'message_count').iterrows():
    ax.annotate(
        row['channel'],
        (row['message_count'], row['engagement']),
        fontsize=7, ha='left', va='bottom'
    )
ax.set_xlabel('Number of Messages')
ax.set_ylabel('Total Replies + Reactions')
ax.set_title('Channel Activity (top 5 labelled)', fontweight='bold')
plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# ── Section 4: Message Classification ────────────────────────
st.header("4. Message Classification")

TECH_KEYWORDS = [
    'error', 'exception', 'bug', 'code', 'function', 'class', 'module',
    'import', 'install', 'pip', 'python', 'git', 'github', 'sql', 'database',
    'api', 'json', 'csv', 'docker', 'terminal', 'command', 'library', 'package',
    'pandas', 'numpy', 'model', 'train', 'dataset', 'jupyter', 'notebook'
]


def classify_message(text):
    if not isinstance(text, str) or text.strip() == '':
        return 'Other'
    t = text.lower()
    tech = any(kw in t for kw in TECH_KEYWORDS)
    if re.search(r'\?|\b(how|what|why|when|can|does|is|are)\b', t):
        return 'Question-Technical' if tech else 'Question-NonTechnical'
    if re.search(r'^(yes|no|sure|correct|exactly)\b', t):
        return 'Answer'
    return 'Comment-Technical' if tech else 'Comment-NonTechnical'


df_view['message_type'] = df_view['text'].apply(classify_message)
type_counts = df_view['message_type'].value_counts()

col1, col2 = st.columns([1, 1])
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#937860', '#DA8BC3']
    type_counts.plot(kind='bar', ax=ax, color=colors[:len(type_counts)], edgecolor='white')
    ax.set_title('Message Type Distribution', fontweight='bold')
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%',
           colors=colors[:len(type_counts)], startangle=140)
    ax.set_title('Message Type Share', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# ── Section 5: Task 2 Charts ──────────────────────────────────
st.header("5. ML Analysis Results")

charts_dir = os.path.join(os.path.dirname(__file__), '..', 'notebooks')

chart_files = {
    "Time Difference Histograms": "time_diff_histograms.png",
    "Topic Modelling (LDA)": "topic_modelling.png",
    "Sentiment Over Time": "sentiment_over_time.png",
}

for title, filename in chart_files.items():
    path = os.path.join(charts_dir, filename)
    if os.path.exists(path):
        st.subheader(title)
        img = Image.open(path)
        st.image(img, use_container_width=True)

st.markdown("---")

# ── Section 6: Raw Data Explorer ─────────────────────────────
st.header("6. Raw Data Explorer")

show_cols = ['channel', 'user', 'text', 'datetime',
             'reply_count_clean', 'reaction_count_clean', 'mention_count']
available = [c for c in show_cols if c in df_view.columns]

n_rows = st.slider("Number of rows to show", min_value=5, max_value=100, value=20)
st.dataframe(df_view[available].head(n_rows), use_container_width=True)
