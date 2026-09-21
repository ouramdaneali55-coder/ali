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
    badge = {"LECT": "Cours", "REC": "TD", "LAB": "TP"}.get(kind, kind)
    now_badge = '<span class="now">EN COURS</span>' if current else ""

    return (
        f'<div class="{css}">'
        f'<div class="slot-top">'
        f'<span class="badge badge-{kind.lower()}">{badge}</span>'
        f'{now_badge}'
        f'</div>'
        f'<div class="subject">{html.escape(str(row["code"]))}</div>'
        f'<div class="detail">📍 {html.escape(str(row["room"]))}</div>'
        f'<div class="detail">👤 {html.escape(str(row["teacher"]))}</div>'
        f'</div>'
    )


df = load_dataframe()

st.markdown("""
<style>
/* --- GLOBAL STYLES --- */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 1.4rem 1.6rem;
    border-radius: 18px;
    border: 1px solid rgba(127,127,127,.20);
    background: linear-gradient(135deg, rgba(70,120,180,.12), rgba(120,80,170,.08));
    margin-bottom: 1rem;
}
.hero h1 { margin: 0 0 .25rem 0; font-size: 2rem; }
.hero p { margin: 0; opacity: .78; }

/* --- DESKTOP GRID STYLES --- */
.week {
    display: grid;
    grid-template-columns: 92px repeat(6, minmax(145px, 1fr));
    gap: 7px;
    overflow-x: auto;
    padding-bottom: 8px;
}
.corner, .day-head, .time-head {
    border-radius: 10px;
    padding: .65rem .5rem;
    font-weight: 700;
    text-align: center;
}
.corner { background: transparent; }
.day-head {
    background: rgba(70,120,180,.18);
    border: 1px solid rgba(70,120,180,.25);
}
.day-head.today { outline: 2px solid rgba(70,120,180,.65); }
.time-head {
    background: rgba(127,127,127,.10);
    border: 1px solid rgba(127,127,127,.18);
    font-size: .80rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
.slot {
    min-height: 92px;
    border-radius: 10px;
    border: 1px solid rgba(127,127,127,.18);
    background: rgba(127,127,127,.055);
    padding: .55rem .65rem;
    box-sizing: border-box;
}
.slot.empty {
    opacity: .28;
    background: repeating-linear-gradient(
        135deg, transparent, transparent 7px,
        rgba(127,127,127,.035) 7px, rgba(127,127,127,.035) 14px
    );
}
.slot.current {
    border: 2px solid #ff4b4b;
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
    padding: .15rem .45rem;
    border-radius: 999px;
    font-size: .68rem;
    font-weight: 800;
}
.badge-lect { background: rgba(50,170,90,.18); }
.badge-rec { background: rgba(60,130,220,.18); }
.badge-lab { background: rgba(230,170,40,.22); }
.now {
    color: #ff4b4b;
    font-size: .62rem;
    font-weight: 900;
}
.subject { font-size: 1rem; font-weight: 850; margin-top: .45rem; }
.detail { font-size: .72rem; margin-top: .2rem; opacity: .78; line-height: 1.2; }

/* --- MOBILE SPECIFIC STYLES --- */
.mobile-only { display: none; }
.mobile-schedule { display: flex; flex-direction: column; gap: 10px; }
.mobile-day-header {
    font-size: 1.1rem;
    font-weight: 700;
    padding: 10px 14px;
    border-radius: 10px;
    background: rgba(70,120,180,.18);
    border: 1px solid rgba(70,120,180,.25);
    margin-top: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.mobile-day-header.today-mobile {
    outline: 2px solid rgba(70,120,180,.65);
    background: rgba(70,120,180,.28);
}
.mobile-card {
    border-radius: 12px;
    border: 1px solid rgba(127,127,127,.18);
    background: rgba(127,127,127,.055);
    padding: .9rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    transition: transform 0.2s;
}
.mobile-card:hover { transform: translateY(-2px); }
.mobile-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.mobile-time { font-weight: 800; font-size: 0.95rem; color: #4678b4; }
.mobile-card .now {
    background: #ff4b4b;
    color: white;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.7rem;
    margin-left: auto;
}
.mobile-subject { font-size: 1.1rem; font-weight: 850; margin-bottom: 6px; }
.mobile-detail { font-size: 0.85rem; opacity: 0.85; display: flex; align-items: center; gap: 8px; }
.mobile-detail span { display: flex; align-items: center; gap: 3px; }

/* --- RESPONSIVE MEDIA QUERIES --- */
@media (max-width: 768px) {
    .desktop-only { display: none !important; }
    .mobile-only { display: block !important; }
    .hero { padding: 1rem; border-radius: 12px; }
    .hero h1 { font-size: 1.4rem; }
    .hero p { font-size: 0.85rem; }
}
@media (min-width: 769px) {
    .mobile-only { display: none !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎓 Emploi du temps IGEE</h1>
  <p><strong>L1 — Semestre 1 — 2026/2027</strong> · Groupes G01 à G16</p>
  <p>Source : calendrier officiel IGEE · dernière modification indiquée : 17/09/2026 14:57:37</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Filtres")

    group = st.selectbox("Groupe", GROUPS, index=0)
    group_df = df[df["group"] == group].copy()

    types = st.multiselect(
        "Type",
        ["LECT", "REC", "LAB"],
        default=["LECT", "REC", "LAB"],
        format_func=lambda x: {
            "LECT": "Cours (LECT)",
            "REC": "TD (REC)",
            "LAB": "TP (LAB)",
        }[x],
    )

    teachers = sorted(group_df["teacher"].unique().tolist())
    teacher = st.selectbox("Enseignant", ["Tous"] + teachers)

    rooms = sorted(group_df["room"].unique().tolist())
    room = st.selectbox("Salle", ["Toutes"] + rooms)

    codes = sorted(group_df["code"].unique().tolist())
    code = st.selectbox("Matière / code", ["Toutes"] + codes)

    st.divider()
    if st.button("🔄 Actualiser", use_container_width=True):
        st.rerun()

    st.caption("Les données affichées proviennent du PDF officiel fourni.")

filtered = group_df[group_df["type"].isin(types)].copy()

if teacher != "Tous":
    filtered = filtered[filtered["teacher"] == teacher]
if room != "Toutes":
    filtered = filtered[filtered["room"] == room]
if code != "Toutes":
    filtered = filtered[filtered["code"] == code]

total = len(filtered)
lect = int((filtered["type"] == "LECT").sum())
rec = int((filtered["type"] == "REC").sum())
lab = int((filtered["type"] == "LAB").sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("Sessions", total)
m2.metric("Cours", lect)
m3.metric("TD", rec)
m4.metric("TP", lab)

now_day = current_day()
now_text = DAY_FR.get(now_day, now_day or "—")

current_rows = filtered[
    filtered.apply(lambda r: is_current_session(r["day"], r["time"]), axis=1)
]

if not current_rows.empty:
    r = current_rows.iloc[0]
    st.success(
        f"🟢 **En cours maintenant : {r['code']} — {r['type']}** · "
        f"{r['room']} · {r['teacher']} · {r['time']}"
    )
else:
    nxt = next_session(filtered)
    if nxt is not None:
        st.info(
            f"⏭️ **Prochaine séance : {nxt['code']} — {nxt['type']}** · "
            f"{DAY_FR[nxt['day']]} · {nxt['time']} · {nxt['room']}"
        )
    else:
        st.info(f"📅 Aujourd’hui : {now_text} · aucune séance restante selon les filtres.")

st.subheader(f"📅 Semaine — {group}")

# ==========================================
# MOBILE VIEW (CARD LIST)
# ==========================================
mobile_grid = ['<div class="mobile-schedule mobile-only">']

for day in DAYS:
    day_sessions = filtered[filtered["day"] == day].copy()
    if day_sessions.empty:
        continue

    # Sort sessions by time
    time_order = {t: i for i, t in enumerate(TIMES)}
    day_sessions["_time_order"] = day_sessions["time"].map(time_order)
    day_sessions = day_sessions.sort_values("_time_order")

    today_class = " today-mobile" if day == now_day else ""
    mobile_grid.append(
        f'<div class="mobile-day-header{today_class}">'
        f'{DAY_FR[day]} <span style="font-size:0.75rem; opacity:0.7;">({day})</span>'
        f'</div>'
    )

    for _, row in day_sessions.iterrows():
        kind = row["type"]
        badge = {"LECT": "Cours", "REC": "TD", "LAB": "TP"}.get(kind, kind)
        now_badge = '<span class="now">EN COURS</span>' if is_current_session(row["day"], row["time"]) else ""

        mobile_grid.append(
            f'<div class="mobile-card">'
            f'<div class="mobile-card-header">'
            f'<span class="mobile-time">{row["time"]}</span>'
            f'<span class="badge badge-{kind.lower()}">{badge}</span>'
            f'{now_badge}'
            f'</div>'
            f'<div class="mobile-subject">{html.escape(str(row["code"]))}</div>'
            f'<div class="mobile-detail">'
            f'<span>📍 {html.escape(str(row["room"]))}</span>'
            f'<span style="opacity:0.4;">|</span>'
            f'<span>👤 {html.escape(str(row["teacher"]))}</span>'
            f'</div>'
            f'</div>'
        )

mobile_grid.append("</div>")
st.markdown("".join(mobile_grid), unsafe_allow_html=True)


# ==========================================
# DESKTOP VIEW (GRID)
# ==========================================
lookup = {
    (r["day"], r["time"]): r
    for _, r in filtered.iterrows()
}

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

display_df = filtered.copy()
day_order = {d: i for i, d in enumerate(DAYS)}
time_order = {t: i for i, t in enumerate(TIMES)}

display_df["_day_order"] = display_df["day"].map(day_order)
display_df["_time_order"] = display_df["time"].map(time_order)
display_df = display_df.sort_values(["_day_order", "_time_order"])

display_df["Jour"] = display_df["day"].map(DAY_FR)
display_df["Horaire"] = display_df["time"]
display_df["Code"] = display_df["code"]
display_df["Type"] = display_df["type"]
display_df["Salle"] = display_df["room"]
display_df["Enseignant"] = display_df["teacher"]

st.dataframe(
    display_df[
        ["Jour", "Horaire", "Code", "Type", "Salle", "Enseignant"]
    ],
    use_container_width=True,
    hide_index=True,
)

csv = display_df[
    ["group", "day", "time", "code", "type", "room", "teacher"]
].to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "⬇️ Télécharger le planning filtré (CSV)",
    data=csv,
    file_name=f"IGEE_{group}_planning.csv",
    mime="text/csv",
)

st.caption(
    "Créneaux officiels : 08:00-09:30, 09:40-11:10, 11:20-12:50, "
    "13:00-14:30, 14:40-16:10 et 16:20-17:50."
)
