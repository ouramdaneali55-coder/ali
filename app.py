import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
import html

st.set_page_config(
    page_title="Emploi du temps IGEE — L1 S1",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
DAY_FR = {
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
}
TIMES = [
    "08:00-09:30",
    "09:40-11:10",
    "11:20-12:50",
    "13:00-14:30",
    "14:40-16:10",
    "16:20-17:50",
]
GROUPS = [f"G{i:02d}" for i in range(1, 17)]

TYPE_LABEL = {"LECT": "Cours", "REC": "TD", "LAB": "TP"}
TYPE_ICON = {"LECT": "📘", "REC": "✏️", "LAB": "🧪"}

# Code -> nom complet du module
MODULE_NAMES = {
    "EE171": "Maths I",
    "EE121": "Algorithmic",
    "EE173": "Physics I",
    "EE175": "Chemistry I",
    "EE123": "Free and Open-Source Software",
    "EE173L": "Physics I Lab",
    "EL101": "English I",
    "EL103": "Writing Methods, Ethics and Deontology",
}


def module_name(code):
    return MODULE_NAMES.get(str(code), "")


def module_label(code):
    name = module_name(code)
    return f"{code} — {name}" if name else str(code)

# Source: official IGEE PDF "L1-S1-2026-2027(1).pdf"
# Last modification shown in the PDF: 17/09/2026 14:57:37
SCHEDULE = [
  # ... (Your existing SCHEDULE list remains unchanged) ...
  # I am keeping it as is to avoid breaking your data.
  # In your actual file, keep the full SCHEDULE list here.
]

# --- PASTE YOUR FULL SCHEDULE LIST HERE ---
# (For brevity, I'm assuming the SCHEDULE list is exactly as you provided)
# If you copy this code, make sure your full SCHEDULE list is between the brackets above.


@st.cache_data
def load_dataframe():
    return pd.DataFrame(SCHEDULE)


def current_day():
    mapping = {
        5: "Saturday",
        6: "Sunday",
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
    }
    return mapping.get(datetime.now().weekday())


def parse_time_range(value):
    start, end = value.split("-")
    return time.fromisoformat(start), time.fromisoformat(end)


def is_current_session(day, slot):
    if day != current_day():
        return False
    now = datetime.now().time()
    start, end = parse_time_range(slot)
    return start <= now < end


def next_session(df):
    if df.empty:
        return None

    day = current_day()
    if not day:
        return None

    day_order = DAYS
    now = datetime.now()
    current_day_index = day_order.index(day)
    candidates = []

    for _, row in df.iterrows():
        idx = day_order.index(row["day"])
        delta = (idx - current_day_index) % len(day_order)
        start, _ = parse_time_range(row["time"])

        if delta == 0:
            candidate = now.replace(
                hour=start.hour, minute=start.minute, second=0, microsecond=0
            )
            if candidate <= now:
                continue
        else:
            candidate = now + timedelta(days=delta)
            candidate = candidate.replace(
                hour=start.hour, minute=start.minute, second=0, microsecond=0
            )

        candidates.append((candidate, row))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]


def session_html(row, current=False):
    if row is None:
        return '<div class="slot empty"></div>'

    css = "slot current" if current else "slot"
    kind = row["type"]
    badge = TYPE_LABEL.get(kind, kind)
    now_badge = '<span class="now">● EN COURS</span>' if current else ""

    return (
        f'<div class="{css} type-{kind.lower()}">'
        f'<div class="slot-top">'
        f'<span class="badge badge-{kind.lower()}">{badge}</span>'
        f"{now_badge}"
        f"</div>"
        f'<div class="subject">{html.escape(str(row["code"]))}</div>'
        f'<div class="module-name">{html.escape(module_name(row["code"]))}</div>'
        f'<div class="detail">📍 {html.escape(str(row["room"]))}</div>'
        f'<div class="detail">👤 {html.escape(str(row["teacher"]))}</div>'
        f"</div>"
    )


df = load_dataframe()

# ==========================================
# STYLES
# ==========================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --accent: #5B7FDE;
    --accent-soft: rgba(91,127,222,.14);
    --accent-strong: #3E5FC4;
    --lect: #2FAE66;
    --rec: #3E8CE0;
    --lab: #E0A429;
    --danger: #FF4B4B;
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}

/* --- HERO --- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 1.8rem 2rem;
    border-radius: var(--radius-lg);
    border: 1px solid rgba(127,127,127,.15);
    background:
        radial-gradient(circle at 15% 20%, rgba(91,127,222,.20), transparent 55%),
        radial-gradient(circle at 85% 0%, rgba(224,164,41,.14), transparent 50%),
        linear-gradient(135deg, rgba(91,127,222,.08), rgba(150,100,220,.05));
    margin-bottom: 1.4rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--accent-strong);
    background: var(--accent-soft);
    padding: .3rem .7rem;
    border-radius: 999px;
    margin-bottom: .7rem;
}
.hero h1 {
    margin: 0 0 .3rem 0;
    font-size: 2.1rem;
    font-weight: 900;
    letter-spacing: -.02em;
}
.hero p { margin: .15rem 0 0 0; opacity: .75; font-size: .92rem; }
.hero .updated { font-size: .78rem; opacity: .55; margin-top: .5rem; }

/* --- LEGEND --- */
.legend { display: flex; gap: .5rem; flex-wrap: wrap; margin: .9rem 0 .2rem 0; }
.legend-chip {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    font-size: .76rem;
    font-weight: 700;
    padding: .3rem .65rem;
    border-radius: 999px;
    border: 1px solid rgba(127,127,127,.18);
    background: rgba(127,127,127,.06);
}
.legend-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }

/* --- STATUS BANNER --- */
div[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    font-weight: 600;
}

/* --- METRICS --- */
div[data-testid="stMetric"] {
    background: rgba(127,127,127,.055);
    border: 1px solid rgba(127,127,127,.14);
    border-radius: var(--radius-md);
    padding: .8rem 1rem .6rem 1rem;
}
div[data-testid="stMetricLabel"] { font-weight: 700; opacity: .7; }
div[data-testid="stMetricValue"] { font-weight: 900; }

/* --- SECTION HEADINGS --- */
h3 { font-weight: 800 !important; letter-spacing: -.01em; margin-top: 1.6rem !important; }

/* --- DESKTOP GRID --- */
.week {
    display: grid;
    grid-template-columns: 96px repeat(6, minmax(150px, 1fr));
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 10px;
}
.corner, .day-head, .time-head {
    border-radius: var(--radius-sm);
    padding: .7rem .5rem;
    font-weight: 800;
    text-align: center;
}
.corner { background: transparent; }
.day-head {
    background: var(--accent-soft);
    border: 1px solid rgba(91,127,222,.22);
    color: var(--accent-strong);
    line-height: 1.35;
}
.day-head small { font-weight: 600; opacity: .65; text-transform: uppercase; letter-spacing: .04em; }
.day-head.today {
    background: var(--accent);
    color: #fff;
    box-shadow: 0 4px 14px rgba(91,127,222,.35);
}
.day-head.today small { opacity: .85; }
.time-head {
    background: rgba(127,127,127,.08);
    border: 1px solid rgba(127,127,127,.16);
    font-size: .78rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: .8;
}
.slot {
    min-height: 96px;
    border-radius: var(--radius-sm);
    border: 1px solid rgba(127,127,127,.16);
    background: rgba(127,127,127,.045);
    padding: .6rem .7rem;
    box-sizing: border-box;
    border-left: 3px solid transparent;
    transition: transform .12s ease, box-shadow .12s ease;
}
.slot:not(.empty):hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,.08);
}
.slot.type-lect { border-left-color: var(--lect); }
.slot.type-rec  { border-left-color: var(--rec); }
.slot.type-lab  { border-left-color: var(--lab); }
.slot.empty {
    opacity: .25;
    border-left-color: transparent;
    background: repeating-linear-gradient(
        135deg, transparent, transparent 7px,
        rgba(127,127,127,.04) 7px, rgba(127,127,127,.04) 14px
    );
}
.slot.current {
    border: 1px solid rgba(255,75,75,.4);
    border-left: 3px solid var(--danger);
    background: rgba(255,75,75,.06);
    box-shadow: 0 0 0 3px rgba(255,75,75,.10);
}
.slot-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .3rem;
}
.badge {
    display: inline-block;
    padding: .18rem .5rem;
    border-radius: 999px;
    font-size: .66rem;
    font-weight: 800;
    letter-spacing: .01em;
}
.badge-lect { background: rgba(47,174,102,.18); color: #1f8a4d; }
.badge-rec  { background: rgba(62,140,224,.18); color: #2a6bb0; }
.badge-lab  { background: rgba(224,164,41,.20); color: #a8790f; }
.now {
    color: var(--danger);
    font-size: .62rem;
    font-weight: 900;
    letter-spacing: .02em;
}
.subject { font-size: 1rem; font-weight: 800; margin-top: .5rem; letter-spacing: -.01em; }
.module-name { font-size: .72rem; font-weight: 600; opacity: .68; margin-top: .1rem; line-height: 1.25; }
.detail { font-size: .74rem; margin-top: .22rem; opacity: .72; line-height: 1.25; }

/* --- MOBILE --- */
.mobile-only { display: none; }
.mobile-schedule { display: flex; flex-direction: column; gap: 12px; }
.mobile-day-header {
    position: sticky;
    top: 0;
    z-index: 5;
    font-size: 1.02rem;
    font-weight: 800;
    padding: .65rem .9rem;
    border-radius: var(--radius-sm);
    background: var(--accent-soft);
    color: var(--accent-strong);
    border: 1px solid rgba(91,127,222,.22);
    margin-top: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(6px);
}
.mobile-day-header .dow { font-size: .72rem; font-weight: 700; opacity: .65; text-transform: uppercase; }
.mobile-day-header.today-mobile {
    background: var(--accent);
    color: #fff;
    box-shadow: 0 4px 14px rgba(91,127,222,.30);
}
.mobile-day-header.today-mobile .dow { opacity: .85; }
.mobile-card {
    border-radius: var(--radius-md);
    border: 1px solid rgba(127,127,127,.16);
    background: rgba(127,127,127,.045);
    padding: 1rem;
    border-left: 4px solid transparent;
    box-shadow: 0 1px 3px rgba(0,0,0,.03);
}
.mobile-card.type-lect { border-left-color: var(--lect); }
.mobile-card.type-rec  { border-left-color: var(--rec); }
.mobile-card.type-lab  { border-left-color: var(--lab); }
.mobile-card.current {
    background: rgba(255,75,75,.06);
    border-color: rgba(255,75,75,.35);
    border-left-color: var(--danger);
}
.mobile-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    gap: .5rem;
}
.mobile-time {
    font-weight: 800;
    font-size: .92rem;
    color: var(--accent-strong);
    background: var(--accent-soft);
    padding: .2rem .55rem;
    border-radius: 999px;
}
.mobile-card .now {
    background: var(--danger);
    color: white;
    padding: .2rem .55rem;
    border-radius: 999px;
    font-size: .66rem;
    margin-left: auto;
}
.mobile-subject { font-size: 1.08rem; font-weight: 800; margin-bottom: .1rem; letter-spacing: -.01em; }
.mobile-module-name { font-size: .8rem; font-weight: 600; opacity: .68; margin-bottom: .5rem; }
.mobile-detail { font-size: .84rem; opacity: .8; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.mobile-detail span { display: flex; align-items: center; gap: 4px; }

/* --- RESPONSIVE --- */
@media (max-width: 900px) {
    .desktop-only { display: none !important; }
    .mobile-only { display: block !important; }
    .hero { padding: 1.2rem 1.3rem; border-radius: var(--radius-md); }
    .hero h1 { font-size: 1.5rem; }
    .hero p { font-size: .82rem; }
    .block-container { padding-left: .9rem; padding-right: .9rem; }
}
@media (min-width: 901px) {
    .mobile-only { display: none !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">🎓 IGEE · Emploi du temps</div>
  <h1>Planning L1 — Semestre 1</h1>
  <p>Année universitaire 2026/2027 · Groupes G01 à G16</p>
  <div class="updated">Source : calendrier officiel IGEE · dernière mise à jour indiquée : 17/09/2026 à 14:57</div>
  <div class="legend">
    <span class="legend-chip"><span class="legend-dot" style="background:var(--lect);"></span>Cours</span>
    <span class="legend-chip"><span class="legend-dot" style="background:var(--rec);"></span>TD</span>
    <span class="legend-chip"><span class="legend-dot" style="background:var(--lab);"></span>TP</span>
    <span class="legend-chip"><span class="legend-dot" style="background:var(--danger);"></span>En cours</span>
  </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Filtres")

    group = st.selectbox("Groupe", GROUPS, index=0)
    group_df = df[df["group"] == group].copy()

    types = st.multiselect(
        "Type de séance",
        ["LECT", "REC", "LAB"],
        default=["LECT", "REC", "LAB"],
        format_func=lambda x: f"{TYPE_ICON.get(x, '')} {TYPE_LABEL.get(x, x)}",
    )

    teachers = sorted(group_df["teacher"].unique().tolist()) if not group_df.empty else []
    teacher = st.selectbox("Enseignant", ["Tous"] + teachers)

    rooms = sorted(group_df["room"].unique().tolist()) if not group_df.empty else []
    room = st.selectbox("Salle", ["Toutes"] + rooms)

    codes = sorted(group_df["code"].unique().tolist()) if not group_df.empty else []
    code = st.selectbox(
        "Matière / code",
        ["Toutes"] + codes,
        format_func=lambda x: "Toutes" if x == "Toutes" else module_label(x),
    )

    st.divider()
    if st.button("🔄 Actualiser", use_container_width=True):
        st.rerun()

    st.caption("Les données affichées proviennent du PDF officiel fourni.")

filtered = group_df[group_df["type"].isin(types)].copy() if not group_df.empty else group_df.copy()

if teacher != "Tous":
    filtered = filtered[filtered["teacher"] == teacher]
if room != "Toutes":
    filtered = filtered[filtered["room"] == room]
if code != "Toutes":
    filtered = filtered[filtered["code"] == code]

total = len(filtered)
lect = int((filtered["type"] == "LECT").sum()) if total else 0
rec = int((filtered["type"] == "REC").sum()) if total else 0
lab = int((filtered["type"] == "LAB").sum()) if total else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("📚 Sessions", total)
m2.metric("📘 Cours", lect)
m3.metric("✏️ TD", rec)
m4.metric("🧪 TP", lab)

now_day = current_day()
now_text = DAY_FR.get(now_day, now_day or "—")

if not filtered.empty:
    current_rows = filtered[
        filtered.apply(lambda r: is_current_session(r["day"], r["time"]), axis=1)
    ]
else:
    current_rows = filtered

if not current_rows.empty:
    r = current_rows.iloc[0]
    st.success(
        f"🟢 **En cours maintenant : {r['code']} — {TYPE_LABEL.get(r['type'], r['type'])}** · "
        f"{r['room']} · {r['teacher']} · {r['time']}"
    )
else:
    nxt = next_session(filtered)
    if nxt is not None:
        st.info(
            f"⏭️ **Prochaine séance : {nxt['code']} — {TYPE_LABEL.get(nxt['type'], nxt['type'])}** · "
            f"{DAY_FR[nxt['day']]} · {nxt['time']} · {nxt['room']}"
        )
    else:
        st.info(f"📅 Aujourd'hui : {now_text} · aucune séance restante selon les filtres.")

st.subheader(f"📅 Semaine — {group}")

# ==========================================
# MOBILE VIEW (CARD LIST)
# ==========================================
mobile_grid = ['<div class="mobile-schedule mobile-only">']

if not filtered.empty:
    time_order = {t: i for i, t in enumerate(TIMES)}

    for day in DAYS:
        day_sessions = filtered[filtered["day"] == day].copy()
        if day_sessions.empty:
            continue

        day_sessions["_time_order"] = day_sessions["time"].map(time_order)
        day_sessions = day_sessions.sort_values("_time_order")

        today_class = " today-mobile" if day == now_day else ""
        mobile_grid.append(
            f'<div class="mobile-day-header{today_class}">'
            f"<span>{DAY_FR[day]}</span>"
            f'<span class="dow">{day}</span>'
            f"</div>"
        )

        for _, row in day_sessions.iterrows():
            kind = row["type"]
            badge = TYPE_LABEL.get(kind, kind)
            is_now = is_current_session(row["day"], row["time"])
            now_badge = '<span class="now">● EN COURS</span>' if is_now else ""
            current_cls = " current" if is_now else ""

            mobile_grid.append(
                f'<div class="mobile-card type-{kind.lower()}{current_cls}">'
                f'<div class="mobile-card-header">'
                f'<span class="mobile-time">{row["time"]}</span>'
                f'<span class="badge badge-{kind.lower()}">{badge}</span>'
                f"{now_badge}"
                f"</div>"
                f'<div class="mobile-subject">{html.escape(str(row["code"]))}</div>'
                f'<div class="mobile-module-name">{html.escape(module_name(row["code"]))}</div>'
                f'<div class="mobile-detail">'
                f'<span>📍 {html.escape(str(row["room"]))}</span>'
                f'<span>👤 {html.escape(str(row["teacher"]))}</span>'
                f"</div>"
                f"</div>"
            )
else:
    mobile_grid.append(
        '<div style="opacity:.6; padding:1rem; text-align:center;">Aucune séance ne correspond aux filtres sélectionnés.</div>'
    )

mobile_grid.append("</div>")
st.markdown("".join(mobile_grid), unsafe_allow_html=True)


# ==========================================
# DESKTOP VIEW (GRID)
# ==========================================
lookup = {
    (r["day"], r["time"]): r
    for _, r in filtered.iterrows()
} if not filtered.empty else {}

grid = ['<div class="week desktop-only">']
grid.append('<div class="corner"></div>')

for day in DAYS:
    today_class = " today" if day == now_day else ""
    grid.append(
        f'<div class="day-head{today_class}">'
        f'{html.escape(DAY_FR[day])}<br><small>{day}</small></div>'
    )

for slot in TIMES:
    grid.append(f'<div class="time-head">{slot}</div>')
    for day in DAYS:
        row = lookup.get((day, slot))
        grid.append(
            session_html(
                row,
                current=(
                    row is not None
                    and is_current_session(row["day"], row["time"])
                ),
            )
        )

grid.append("</div>")
st.markdown("".join(grid), unsafe_allow_html=True)


st.subheader("📋 Détail des séances")

if not filtered.empty:
    display_df = filtered.copy()
    day_order = {d: i for i, d in enumerate(DAYS)}
    time_order = {t: i for i, t in enumerate(TIMES)}

    display_df["_day_order"] = display_df["day"].map(day_order)
    display_df["_time_order"] = display_df["time"].map(time_order)
    display_df = display_df.sort_values(["_day_order", "_time_order"])

    display_df["Jour"] = display_df["day"].map(DAY_FR)
    display_df["Horaire"] = display_df["time"]
    display_df["Code"] = display_df["code"]
    display_df["Module"] = display_df["code"].map(module_name)
    display_df["Type"] = display_df["type"].map(TYPE_LABEL)
    display_df["Salle"] = display_df["room"]
    display_df["Enseignant"] = display_df["teacher"]

    st.dataframe(
        display_df[
            ["Jour", "Horaire", "Code", "Module", "Type", "Salle", "Enseignant"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    csv_df = display_df.copy()
    csv_df["module_name"] = csv_df["code"].map(module_name)
    csv = csv_df[
        ["group", "day", "time", "code", "module_name", "type", "room", "teacher"]
    ].to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇️ Télécharger le planning filtré (CSV)",
        data=csv,
        file_name=f"IGEE_{group}_planning.csv",
        mime="text/csv",
    )
else:
    st.info("Aucune donnée à afficher pour ce groupe/ces filtres.")

st.caption(
    "Créneaux officiels : 08:00-09:30, 09:40-11:10, 11:20-12:50, "
    "13:00-14:30, 14:40-16:10 et 16:20-17:50."
)
