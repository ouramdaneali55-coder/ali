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
  {
    "group": "G01",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G01",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G01",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G01",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B214",
    "teacher": "S. MESSOUCI"
  },
  {
    "group": "G01",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G01",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "REC",
    "room": "B011",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G01",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G01",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G01",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "REC",
    "room": "B305",
    "teacher": "H. DAOUDI"
  },
  {
    "group": "G01",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "I. IBN BOUSHAKI"
  },
  {
    "group": "G01",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G01",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B214",
    "teacher": "S. MESSOUCI"
  },
  {
    "group": "G01",
    "day": "Saturday",
    "time": "11:20-12:50",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G01",
    "day": "Thursday",
    "time": "11:20-12:50",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "I. IBN BOUSHAKI"
  },
  {
    "group": "G01",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B214",
    "teacher": "S. MESSOUCI"
  },
  {
    "group": "G01",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE121",
    "type": "REC",
    "room": "B011",
    "teacher": "H. BELAIDI"
  },
  {
    "group": "G01",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G01",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G01",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "I. IBN BOUSHAKI"
  },
  {
    "group": "G01",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "REC",
    "room": "B001",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G01",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G02",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G02",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G02",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G02",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "I. IBN BOUSHAKI"
  },
  {
    "group": "G02",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G02",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B214",
    "teacher": "S. MESSOUCI"
  },
  {
    "group": "G02",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G02",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G02",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "H. BELAIDI"
  },
  {
    "group": "G02",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B214",
    "teacher": "S. MESSOUCI"
  },
  {
    "group": "G02",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G02",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "REC",
    "room": "B313",
    "teacher": "H. DAOUDI"
  },
  {
    "group": "G02",
    "day": "Saturday",
    "time": "11:20-12:50",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G02",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "I. IBN BOUSHAKI"
  },
  {
    "group": "G02",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "REC",
    "room": "B001",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G02",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G02",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G02",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "I. IBN BOUSHAKI"
  },
  {
    "group": "G02",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B214",
    "teacher": "S. MESSOUCI"
  },
  {
    "group": "G02",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G02",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE173",
    "type": "REC",
    "room": "B305",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G03",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G03",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G03",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G03",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "K. KARDACHE"
  },
  {
    "group": "G03",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G03",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "REC",
    "room": "B313",
    "teacher": "H. DAOUDI"
  },
  {
    "group": "G03",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G03",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "REC",
    "room": "B011",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G03",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "A. KHEDER"
  },
  {
    "group": "G03",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G03",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "Y. BENMOUSSA"
  },
  {
    "group": "G03",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "K. KARDACHE"
  },
  {
    "group": "G03",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G03",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G03",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE121",
    "type": "REC",
    "room": "B313",
    "teacher": "F. FERTAS"
  },
  {
    "group": "G03",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "K. KARDACHE"
  },
  {
    "group": "G03",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "A. KHEDER"
  },
  {
    "group": "G03",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G03",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G03",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE173",
    "type": "REC",
    "room": "B319",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G03",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "A. KHEDER"
  },
  {
    "group": "G04",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G04",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G04",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G04",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "A. KHEDER"
  },
  {
    "group": "G04",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G04",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "REC",
    "room": "B003",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G04",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G04",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "K. KARDACHE"
  },
  {
    "group": "G04",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G04",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "Y. BENMOUSSA"
  },
  {
    "group": "G04",
    "day": "Monday",
    "time": "11:20-12:50",
    "code": "EE175",
    "type": "REC",
    "room": "B313",
    "teacher": "Z. ABDESSADEK"
  },
  {
    "group": "G04",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "A. KHEDER"
  },
  {
    "group": "G04",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G04",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G04",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE173",
    "type": "REC",
    "room": "B319",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G04",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "A. KHEDER"
  },
  {
    "group": "G04",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "K. KARDACHE"
  },
  {
    "group": "G04",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G04",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G04",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE121",
    "type": "REC",
    "room": "B313",
    "teacher": "F. FERTAS"
  },
  {
    "group": "G04",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "K. KARDACHE"
  },
  {
    "group": "G05",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G05",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G05",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G05",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B304",
    "teacher": "N. GOUDA"
  },
  {
    "group": "G05",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G05",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G05",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G05",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "REC",
    "room": "B103",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G05",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B311",
    "teacher": "V. VAC 04"
  },
  {
    "group": "G05",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G05",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "REC",
    "room": "B003",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G05",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B304",
    "teacher": "N. GOUDA"
  },
  {
    "group": "G05",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE173",
    "type": "REC",
    "room": "B103",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G05",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G05",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G05",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B304",
    "teacher": "N. GOUDA"
  },
  {
    "group": "G05",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B311",
    "teacher": "V. VAC 04"
  },
  {
    "group": "G05",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE121",
    "type": "REC",
    "room": "C104",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G05",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G05",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G05",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B311",
    "teacher": "V. VAC 04"
  },
  {
    "group": "G06",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G06",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G06",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G06",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B311",
    "teacher": "V. VAC 04"
  },
  {
    "group": "G06",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G06",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EE121",
    "type": "REC",
    "room": "B103",
    "teacher": "F. FERTAS"
  },
  {
    "group": "G06",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G06",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G06",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B304",
    "teacher": "N. GOUDA"
  },
  {
    "group": "G06",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G06",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "REC",
    "room": "B011",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G06",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B311",
    "teacher": "V. VAC 04"
  },
  {
    "group": "G06",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "REC",
    "room": "C107",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G06",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G06",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G06",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B311",
    "teacher": "V. VAC 04"
  },
  {
    "group": "G06",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B304",
    "teacher": "N. GOUDA"
  },
  {
    "group": "G06",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE175",
    "type": "REC",
    "room": "B313",
    "teacher": "Z. ABDESSADEK"
  },
  {
    "group": "G06",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G06",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G06",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B304",
    "teacher": "N. GOUDA"
  },
  {
    "group": "G07",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G07",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G07",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G07",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "B. BOUMARAF"
  },
  {
    "group": "G07",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G07",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G07",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "REC",
    "room": "B311",
    "teacher": "Z. ABDESSADEK"
  },
  {
    "group": "G07",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G07",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "REC",
    "room": "B101",
    "teacher": "N. CHERIFI"
  },
  {
    "group": "G07",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "V. VAC 01"
  },
  {
    "group": "G07",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G07",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G07",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "B. BOUMARAF"
  },
  {
    "group": "G07",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE121",
    "type": "REC",
    "room": "C104",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G07",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G07",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "B. BOUMARAF"
  },
  {
    "group": "G07",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "V. VAC 01"
  },
  {
    "group": "G07",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE173",
    "type": "REC",
    "room": "B103",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G07",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G07",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G07",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "V. VAC 01"
  },
  {
    "group": "G08",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G08",
    "day": "Sunday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G08",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G08",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "V. VAC 01"
  },
  {
    "group": "G08",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G08",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G08",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G08",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "REC",
    "room": "C105",
    "teacher": "K. BAICHE"
  },
  {
    "group": "G08",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "B. BOUMARAF"
  },
  {
    "group": "G08",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G08",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G08",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "V. VAC 01"
  },
  {
    "group": "G08",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EE175",
    "type": "REC",
    "room": "B313",
    "teacher": "Z. ABDESSADEK"
  },
  {
    "group": "G08",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G08",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EE173",
    "type": "REC",
    "room": "B305",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G08",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "V. VAC 01"
  },
  {
    "group": "G08",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "B. BOUMARAF"
  },
  {
    "group": "G08",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "REC",
    "room": "C107",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G08",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 1",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G08",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G08",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B009",
    "teacher": "B. BOUMARAF"
  },
  {
    "group": "G09",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE121",
    "type": "REC",
    "room": "C105",
    "teacher": "K. BAICHE"
  },
  {
    "group": "G09",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "REC",
    "room": "B101",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G09",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G09",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B210",
    "teacher": "S. SBAIHI"
  },
  {
    "group": "G09",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G09",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G09",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G09",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "REC",
    "room": "B319",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G09",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G09",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "B. BADJOU"
  },
  {
    "group": "G09",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G09",
    "day": "Saturday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G09",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B210",
    "teacher": "S. SBAIHI"
  },
  {
    "group": "G09",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G09",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B210",
    "teacher": "S. SBAIHI"
  },
  {
    "group": "G09",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "A. BELAHCEN"
  },
  {
    "group": "G09",
    "day": "Saturday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G09",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "B. BADJOU"
  },
  {
    "group": "G09",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G09",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "B. BADJOU"
  },
  {
    "group": "G09",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "REC",
    "room": "B313",
    "teacher": "N. CHERIFI"
  },
  {
    "group": "G10",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE121",
    "type": "REC",
    "room": "B103",
    "teacher": "S. MEKHMOUKH"
  },
  {
    "group": "G10",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G10",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "B. BADJOU"
  },
  {
    "group": "G10",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G10",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G10",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G10",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "REC",
    "room": "B011",
    "teacher": "H. DAOUDI"
  },
  {
    "group": "G10",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G10",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B210",
    "teacher": "S. SBAIHI"
  },
  {
    "group": "G10",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G10",
    "day": "Monday",
    "time": "11:20-12:50",
    "code": "EE171",
    "type": "REC",
    "room": "B101",
    "teacher": "N. CHERIFI"
  },
  {
    "group": "G10",
    "day": "Saturday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G10",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "B. BADJOU"
  },
  {
    "group": "G10",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G10",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B302",
    "teacher": "B. BADJOU"
  },
  {
    "group": "G10",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "A. BELAHCEN"
  },
  {
    "group": "G10",
    "day": "Saturday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G10",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B210",
    "teacher": "S. SBAIHI"
  },
  {
    "group": "G10",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G10",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B210",
    "teacher": "S. SBAIHI"
  },
  {
    "group": "G10",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EE173",
    "type": "REC",
    "room": "B101",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G11",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "REC",
    "room": "B101",
    "teacher": "N. CHERIFI"
  },
  {
    "group": "G11",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "REC",
    "room": "B305",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G11",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G11",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B212",
    "teacher": "N. OURRAD"
  },
  {
    "group": "G11",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G11",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G11",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G11",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G11",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B101",
    "teacher": "O. MOUSSAOUI"
  },
  {
    "group": "G11",
    "day": "Saturday",
    "time": "11:20-12:50",
    "code": "EE175",
    "type": "REC",
    "room": "B311",
    "teacher": "Z. ABDESSADEK"
  },
  {
    "group": "G11",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G11",
    "day": "Wednesday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "REC",
    "room": "B313",
    "teacher": "F. FERTAS"
  },
  {
    "group": "G11",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B212",
    "teacher": "N. OURRAD"
  },
  {
    "group": "G11",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B212",
    "teacher": "N. OURRAD"
  },
  {
    "group": "G11",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G11",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G11",
    "day": "Saturday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G11",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B101",
    "teacher": "O. MOUSSAOUI"
  },
  {
    "group": "G11",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B101",
    "teacher": "O. MOUSSAOUI"
  },
  {
    "group": "G11",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G11",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G12",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "REC",
    "room": "B305",
    "teacher": "H. DAOUDI"
  },
  {
    "group": "G12",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "REC",
    "room": "C105",
    "teacher": "N. CHERIFI"
  },
  {
    "group": "G12",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G12",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B101",
    "teacher": "O. MOUSSAOUI"
  },
  {
    "group": "G12",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G12",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G12",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G12",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "REC",
    "room": "B305",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G12",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G12",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B212",
    "teacher": "N. OURRAD"
  },
  {
    "group": "G12",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G12",
    "day": "Wednesday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "REC",
    "room": "B001",
    "teacher": "H. BELAIDI"
  },
  {
    "group": "G12",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B101",
    "teacher": "O. MOUSSAOUI"
  },
  {
    "group": "G12",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B101",
    "teacher": "O. MOUSSAOUI"
  },
  {
    "group": "G12",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G12",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G12",
    "day": "Saturday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G12",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B212",
    "teacher": "N. OURRAD"
  },
  {
    "group": "G12",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B212",
    "teacher": "N. OURRAD"
  },
  {
    "group": "G12",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G12",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G13",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "REC",
    "room": "B011",
    "teacher": "H. DAOUDI"
  },
  {
    "group": "G13",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G13",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "B. BOUKHENOUFA"
  },
  {
    "group": "G13",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G13",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G13",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G13",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE121",
    "type": "REC",
    "room": "B103",
    "teacher": "S. MEKHMOUKH"
  },
  {
    "group": "G13",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G13",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "L. AIT SLIMANI"
  },
  {
    "group": "G13",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G13",
    "day": "Saturday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G13",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G13",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "B. BOUKHENOUFA"
  },
  {
    "group": "G13",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G13",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "B. BOUKHENOUFA"
  },
  {
    "group": "G13",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE173",
    "type": "REC",
    "room": "B101",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G13",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G13",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "L. AIT SLIMANI"
  },
  {
    "group": "G13",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G13",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "L. AIT SLIMANI"
  },
  {
    "group": "G13",
    "day": "Thursday",
    "time": "14:40-16:10",
    "code": "EE171",
    "type": "REC",
    "room": "B011",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G14",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE171",
    "type": "REC",
    "room": "B011",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G14",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "REC",
    "room": "B319",
    "teacher": ".. BENAMARA"
  },
  {
    "group": "G14",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G14",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "L. AIT SLIMANI"
  },
  {
    "group": "G14",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G14",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G14",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G14",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "REC",
    "room": "B101",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G14",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G14",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "B. BOUKHENOUFA"
  },
  {
    "group": "G14",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G14",
    "day": "Thursday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "REC",
    "room": "B101",
    "teacher": "F. FERTAS"
  },
  {
    "group": "G14",
    "day": "Saturday",
    "time": "13:00-14:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G14",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G14",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "L. AIT SLIMANI"
  },
  {
    "group": "G14",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G14",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B301",
    "teacher": "L. AIT SLIMANI"
  },
  {
    "group": "G14",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A113",
    "teacher": "P. VAC"
  },
  {
    "group": "G14",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "B. BOUKHENOUFA"
  },
  {
    "group": "G14",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G14",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B306",
    "teacher": "B. BOUKHENOUFA"
  },
  {
    "group": "G15",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G15",
    "day": "Monday",
    "time": "08:00-09:30",
    "code": "EE175",
    "type": "REC",
    "room": "B103",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G15",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G15",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G15",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B310",
    "teacher": "V. VAC 03"
  },
  {
    "group": "G15",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G15",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G15",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G15",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G15",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G15",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "K. BENDJABALLAH"
  },
  {
    "group": "G15",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G15",
    "day": "Saturday",
    "time": "13:00-14:30",
    "code": "EE121",
    "type": "REC",
    "room": "B303",
    "teacher": "A. VAC"
  },
  {
    "group": "G15",
    "day": "Sunday",
    "time": "13:00-14:30",
    "code": "EE173",
    "type": "REC",
    "room": "B313",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G15",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B310",
    "teacher": "V. VAC 03"
  },
  {
    "group": "G15",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G15",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B310",
    "teacher": "V. VAC 03"
  },
  {
    "group": "G15",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "REC",
    "room": "B313",
    "teacher": "N. CHERIFI"
  },
  {
    "group": "G15",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "K. BENDJABALLAH"
  },
  {
    "group": "G15",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G15",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "K. BENDJABALLAH"
  },
  {
    "group": "G16",
    "day": "Saturday",
    "time": "08:00-09:30",
    "code": "EE123",
    "type": "LAB",
    "room": "A408",
    "teacher": "H. BOUYAHIAOUI"
  },
  {
    "group": "G16",
    "day": "Tuesday",
    "time": "08:00-09:30",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G16",
    "day": "Wednesday",
    "time": "08:00-09:30",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G16",
    "day": "Thursday",
    "time": "08:00-09:30",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "K. BENDJABALLAH"
  },
  {
    "group": "G16",
    "day": "Saturday",
    "time": "09:40-11:10",
    "code": "EL103",
    "type": "LECT",
    "room": "AMPHI 3",
    "teacher": "V. VAC 05"
  },
  {
    "group": "G16",
    "day": "Sunday",
    "time": "09:40-11:10",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G16",
    "day": "Monday",
    "time": "09:40-11:10",
    "code": "EE173",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G16",
    "day": "Tuesday",
    "time": "09:40-11:10",
    "code": "EE173L",
    "type": "LAB",
    "room": "A108",
    "teacher": "P. VAC"
  },
  {
    "group": "G16",
    "day": "Wednesday",
    "time": "09:40-11:10",
    "code": "EE175",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": ". BENLEFKI"
  },
  {
    "group": "G16",
    "day": "Thursday",
    "time": "09:40-11:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B310",
    "teacher": "V. VAC 03"
  },
  {
    "group": "G16",
    "day": "Sunday",
    "time": "11:20-12:50",
    "code": "EE121",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "Y. AZZOUGUI"
  },
  {
    "group": "G16",
    "day": "Saturday",
    "time": "13:00-14:30",
    "code": "EE175",
    "type": "REC",
    "room": "B311",
    "teacher": "Z. ABDESSADEK"
  },
  {
    "group": "G16",
    "day": "Monday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "K. BENDJABALLAH"
  },
  {
    "group": "G16",
    "day": "Tuesday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "T. BOUDJRIOU"
  },
  {
    "group": "G16",
    "day": "Wednesday",
    "time": "13:00-14:30",
    "code": "EL103",
    "type": "REC",
    "room": "B303",
    "teacher": "K. BENDJABALLAH"
  },
  {
    "group": "G16",
    "day": "Thursday",
    "time": "13:00-14:30",
    "code": "EE171",
    "type": "REC",
    "room": "B011",
    "teacher": "W. KSOURI"
  },
  {
    "group": "G16",
    "day": "Saturday",
    "time": "14:40-16:10",
    "code": "EE121",
    "type": "REC",
    "room": "B303",
    "teacher": "A. VAC"
  },
  {
    "group": "G16",
    "day": "Sunday",
    "time": "14:40-16:10",
    "code": "EE173",
    "type": "REC",
    "room": "B313",
    "teacher": "Y. CHERGUI"
  },
  {
    "group": "G16",
    "day": "Monday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B310",
    "teacher": "V. VAC 03"
  },
  {
    "group": "G16",
    "day": "Tuesday",
    "time": "14:40-16:10",
    "code": "EE123",
    "type": "LECT",
    "room": "AMPHI 2",
    "teacher": "D. CHERIFI"
  },
  {
    "group": "G16",
    "day": "Wednesday",
    "time": "14:40-16:10",
    "code": "EL101",
    "type": "REC",
    "room": "LS-B310",
    "teacher": "V. VAC 03"
  }
]


@st.cache_data
def load_dataframe():
    return pd.DataFrame(SCHEDULE)


def current_day():
    # Python weekday(): Monday=0 ... Sunday=6.
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
    badge = {
        "LECT": "Cours",
        "REC": "TD",
        "LAB": "TP",
    }.get(kind, kind)

    now_badge = '<span class="now">EN COURS</span>' if current else ""

    # Return as a single line without indentation to prevent Markdown from treating it as a code block
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
.hero h1 {
    margin: 0 0 .25rem 0;
    font-size: 2rem;
}
.hero p {
    margin: 0;
    opacity: .78;
}
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
.corner {
    background: transparent;
}
.day-head {
    background: rgba(70,120,180,.18);
    border: 1px solid rgba(70,120,180,.25);
}
.day-head.today {
    outline: 2px solid rgba(70,120,180,.65);
}
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
        135deg,
        transparent,
        transparent 7px,
        rgba(127,127,127,.035) 7px,
        rgba(127,127,127,.035) 14px
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
.badge-rec  { background: rgba(60,130,220,.18); }
.badge-lab  { background: rgba(230,170,40,.22); }
.now {
    color: #ff4b4b;
    font-size: .62rem;
    font-weight: 900;
}
.subject {
    font-size: 1rem;
    font-weight: 850;
    margin-top: .45rem;
}
.detail {
    font-size: .72rem;
    margin-top: .2rem;
    opacity: .78;
    line-height: 1.2;
}
@media (max-width: 900px) {
    .week {
        grid-template-columns: 82px repeat(6, 170px);
    }
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

lookup = {
    (r["day"], r["time"]): r
    for _, r in filtered.iterrows()
}

grid = ['<div class="week">']
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
