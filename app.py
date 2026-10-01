
import base64
import math
import os

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Aman Edge Physics | Ultrasonic Interferometer",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GLOBAL STYLE
# ============================================================
st.markdown(
    """
<style>
:root{
    --navy:#081c33;
    --navy2:#113b60;
    --blue:#177ea7;
    --cyan:#32a2bf;
    --ink:#14283c;
    --muted:#64768a;
    --line:#dbe5ed;
    --bg:#f3f6fa;
    --card:#ffffff;
    --soft:#edf6fa;
    --success:#1f7a52;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"]{
    background:var(--bg) !important;
}

.stApp{
    background:var(--bg) !important;
}

.block-container{
    max-width:1480px !important;
    padding-top:1rem !important;
    padding-bottom:1.2rem !important;
}

[data-testid="stHeader"]{
    background:var(--bg) !important;
}

[data-testid="stSidebar"]{
    background:#edf3f8 !important;
    border-right:1px solid #d8e2eb !important;
}

[data-testid="stSidebar"] *{
    color:#173047 !important;
}

[data-testid="stMetric"]{
    background:#fff !important;
    border:1px solid var(--line) !important;
    border-radius:15px !important;
    padding:11px 13px !important;
}

[data-testid="stMetric"] *{
    color:#153654 !important;
}

.stButton > button{
    background:#fff !important;
    color:#173047 !important;
    border:1px solid #cbd8e4 !important;
    border-radius:10px !important;
    font-weight:700 !important;
    min-height:42px !important;
}

.stButton > button:hover{
    border-color:var(--blue) !important;
    color:#0c6385 !important;
}

.stDownloadButton > button{
    background:#fff !important;
    color:#173047 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div{
    background:#fff !important;
}

.hero{
    background:linear-gradient(135deg,#07182d 0%,#0c2b49 52%,#176885 100%);
    border-radius:24px;
    padding:24px 28px 28px;
    color:#fff;
    text-align:center;
    box-shadow:0 14px 34px rgba(10,32,52,.15);
    margin-bottom:18px;
}

.logo-shell{
    width:98px;
    height:98px;
    margin:0 auto 13px auto;
    border-radius:20px;
    background:#ffffff;
    border:1px solid rgba(255,255,255,.65);
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
    box-shadow:0 4px 18px rgba(0,0,0,.12);
}

.logo-shell img{
    display:block;
    width:84px;
    height:84px;
    object-fit:contain;
}

.brand{
    font-size:20px;
    line-height:1.1;
    font-weight:850;
    letter-spacing:2.4px;
}

.brand-sub{
    font-size:13px;
    margin-top:6px;
    opacity:.84;
    letter-spacing:.35px;
}

.hero-rule{
    width:92px;
    height:1px;
    background:rgba(255,255,255,.3);
    margin:15px auto;
}

.hero-title{
    font-size:32px;
    font-weight:850;
    line-height:1.08;
}

.hero-desc{
    max-width:940px;
    margin:7px auto 0;
    font-size:14px;
    opacity:.86;
}

.section-title{
    font-size:21px;
    font-weight:850;
    color:#102a43;
    margin:16px 0 10px;
}

.card{
    background:#fff;
    border:1px solid var(--line);
    border-radius:18px;
    padding:16px 18px;
    box-shadow:0 5px 18px rgba(20,40,60,.045);
}

.card h3{
    margin:0 0 7px;
    color:#16334d;
    font-size:17px;
}

.soft{
    background:var(--soft);
    border-left:4px solid var(--blue);
    border-radius:10px;
    padding:12px 14px;
    color:#174156;
}

.status{
    background:#fff;
    border:1px solid var(--line);
    border-radius:13px;
    padding:11px 14px;
    color:#173047;
}

.footer{
    border-top:1px solid #d7e2eb;
    margin-top:28px;
    padding:18px 6px 6px;
    text-align:center;
    color:#6c7b8c;
    font-size:12px;
}

.footer strong{
    color:#173b5e;
}

.pill{
    display:inline-block;
    background:#edf5f9;
    color:#15506b;
    border-radius:999px;
    padding:3px 8px;
    margin-right:4px;
    font-size:11px;
    font-weight:800;
}

.instruction{
    font-size:13px;
    color:#607286;
}

[data-testid="stDataFrame"]{
    border:1px solid var(--line) !important;
    border-radius:12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "power": False,
    "rf": False,
    "detector": False,
    "micrometer": 0.0,
    "records": [],
    "last_message": "Switch ON the main power to begin the experiment.",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# LOGO HEADER
# ============================================================
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

if os.path.exists(logo_path):
    with open(logo_path, "rb") as logo_file:
        logo_b64 = base64.b64encode(logo_file.read()).decode("ascii")
    logo_html = (
        f'<div class="logo-shell">'
        f'<img src="data:image/png;base64,{logo_b64}" alt="Aman Edge Physics logo">'
        f'</div>'
    )
else:
    # Graceful placeholder if the user has not added logo.png yet.
    logo_html = (
        '<div class="logo-shell">'
        '<div style="font-size:26px;font-weight:850;color:#123a60;">AE</div>'
        '</div>'
    )

st.markdown(
    f"""
<div class="hero">
    {logo_html}
    <div class="brand">AMAN EDGE PHYSICS</div>
    <div class="brand-sub">Ultrasonic Interferometer • Interactive Physics Laboratory</div>
    <div class="hero-rule"></div>
    <div class="hero-title">Ultrasonic Interferometer</div>
    <div class="hero-desc">
        Operate a structured virtual interferometer, observe piezoelectric transduction,
        scan the reflector, detect resonance maxima and determine the velocity of ultrasound.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR: EXPERIMENT SETUP
# ============================================================
st.sidebar.markdown("## Virtual Lab")

liquid = st.sidebar.selectbox(
    "Liquid in interferometer cell",
    ["Water", "Glycerol", "Ethanol", "Methanol", "Custom"],
    index=0,
)

reference_velocity_map = {
    "Water": 1480.0,
    "Glycerol": 1900.0,
    "Ethanol": 1160.0,
    "Methanol": 1100.0,
}

if liquid == "Custom":
    reference_velocity = st.sidebar.number_input(
        "Simulation velocity (m/s)",
        min_value=100.0,
        max_value=4000.0,
        value=1500.0,
        step=10.0,
    )
else:
    reference_velocity = reference_velocity_map[liquid]

frequency_mhz = st.sidebar.slider(
    "RF frequency (MHz)",
    min_value=0.50,
    max_value=8.00,
    value=2.00,
    step=0.05,
)

frequency_hz = frequency_mhz * 1e6

noise_pct = st.sidebar.slider(
    "Detector noise (%)",
    min_value=0.0,
    max_value=8.0,
    value=1.5,
    step=0.5,
)

animation = st.sidebar.checkbox(
    "Animate ultrasonic field",
    value=True,
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Instrument controls")

ctl1, ctl2 = st.sidebar.columns(2)

with ctl1:
    if st.button(
        "Power OFF" if st.session_state.power else "Power ON",
        use_container_width=True,
    ):
        st.session_state.power = not st.session_state.power
        if not st.session_state.power:
            st.session_state.rf = False
            st.session_state.detector = False
        st.rerun()

with ctl2:
    if st.button(
        "RF OFF" if st.session_state.rf else "RF ON",
        use_container_width=True,
    ):
        if st.session_state.power:
            st.session_state.rf = not st.session_state.rf
        else:
            st.session_state.last_message = "Main power must be ON before the RF oscillator."
        st.rerun()

if st.sidebar.button(
    "Detector OFF" if st.session_state.detector else "Detector ON",
    use_container_width=True,
):
    if st.session_state.power and st.session_state.rf:
        st.session_state.detector = not st.session_state.detector
    else:
        st.session_state.last_message = "Switch ON Main Power and RF before the detector."
    st.rerun()

if st.sidebar.button("Reset experiment", use_container_width=True):
    st.session_state.power = False
    st.session_state.rf = False
    st.session_state.detector = False
    st.session_state.micrometer = 0.0
    st.session_state.records = []
    st.session_state.last_message = "Experiment reset. Switch ON the main power to begin."
    st.rerun()

# ============================================================
# PHYSICS ENGINE
# ============================================================
wavelength_m = reference_velocity / frequency_hz
wavelength_mm = wavelength_m * 1e3
maxima_spacing_mm = wavelength_mm / 2.0

position_mm = float(st.session_state.micrometer)
position_m = position_mm * 1e-3

# Successive detector maxima are separated by λ/2.
phase = 2.0 * math.pi * position_m / max(wavelength_m / 2.0, 1e-12)
ideal_detector = 0.5 * (1.0 + math.cos(phase))

# A deterministic noise field makes the meter look instrument-like
# while remaining stable when the Streamlit page reruns.
if st.session_state.power and st.session_state.rf and st.session_state.detector:
    noise = (
        (noise_pct / 100.0)
        * 0.12
        * math.sin(position_mm * 92.17 + frequency_mhz * 4.13)
    )
    detector_output = float(np.clip(ideal_detector + noise, 0.0, 1.0))
else:
    detector_output = 0.0

# ============================================================
# LIVE INSTRUMENT STATUS
# ============================================================
def state_badge(label, state):
    if state:
        return (
            f'<span style="display:inline-block;margin-right:7px;padding:7px 10px;'
            f'border-radius:9px;background:#e7f6ee;color:#196e48;'
            f'border:1px solid #c3e2d1;font-size:12px;font-weight:800;">'
            f'{label}: ON</span>'
        )
    return (
        f'<span style="display:inline-block;margin-right:7px;padding:7px 10px;'
        f'border-radius:9px;background:#f4f6f8;color:#6a7a89;'
        f'border:1px solid #d8e0e7;font-size:12px;font-weight:800;">'
        f'{label}: OFF</span>'
    )

st.markdown(
    f"""
<div class="status">
    {state_badge("Main Power", st.session_state.power)}
    {state_badge("RF Oscillator", st.session_state.rf)}
    {state_badge("Detector", st.session_state.detector)}
    <span style="margin-left:4px;">Reflector: <b>{position_mm:.3f} mm</b></span>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# QUICK READINGS
# ============================================================
st.markdown('<div class="section-title">1. Instrument readings</div>', unsafe_allow_html=True)

q1, q2, q3, q4, q5 = st.columns(5)
q1.metric("Frequency", f"{frequency_mhz:.2f} MHz")
q2.metric("Wavelength λ", f"{wavelength_mm:.3f} mm")
q3.metric("Expected λ/2", f"{maxima_spacing_mm:.3f} mm")
q4.metric("Detector output", f"{detector_output * 100:.1f} %")
q5.metric("Recorded maxima", f"{len(st.session_state.records)}")

# ============================================================
# VIRTUAL APPARATUS — STRUCTURED
# ============================================================
st.markdown('<div class="section-title">2. Virtual apparatus</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="instruction">Operate the chain exactly in sequence: '
    '<b>RF oscillator → transmitting crystal → liquid → reflector → receiving detector → meter.</b></div>',
    unsafe_allow_html=True,
)

# Build a structured SVG instrument panel.
wave_animation = "waveMotion 1.45s linear infinite" if (animation and st.session_state.rf) else "none"
pulse_animation = "pulse 1.1s ease-in-out infinite" if (st.session_state.rf and animation) else "none"
detector_level = max(0.02, detector_output)

apparatus_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{{box-sizing:border-box}}
body{{
  margin:0;
  background:transparent;
  font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}}
.panel{{
  width:100%;
  height:420px;
  border:1px solid #d7e2eb;
  border-radius:20px;
  background:linear-gradient(180deg,#ffffff 0%,#f5f9fc 100%);
  overflow:hidden;
}}
svg{{width:100%;height:100%;display:block}}
.label{{font-family:Inter,Arial,sans-serif}}
.small{{font-size:11px;fill:#637689}}
.mid{{font-size:13px;fill:#17324b;font-weight:700}}
.title{{font-size:15px;fill:#123653;font-weight:800}}
.bold{{font-size:18px;fill:#113955;font-weight:850}}
@keyframes waveMotion{{
  from{{transform:translateX(0px)}}
  to{{transform:translateX(26px)}}
}}
.waveGroup{{animation:{wave_animation};}}
@keyframes pulse{{
  0%,100%{{opacity:.55}}
  50%{{opacity:1}}
}}
.pulse{{animation:{pulse_animation};}}
</style>
</head>
<body>
<div class="panel">
<svg viewBox="0 0 1320 420" preserveAspectRatio="xMidYMid meet">

<!-- HEADER -->
<text x="36" y="31" class="title">ULTRASONIC INTERFEROMETER • VIRTUAL APPARATUS</text>
<text x="1282" y="31" text-anchor="end" class="small">{liquid.upper()} • {frequency_mhz:.2f} MHz</text>
<line x1="36" y1="44" x2="1284" y2="44" stroke="#dbe5ed"/>

<!-- BENCH -->
<rect x="28" y="350" width="1264" height="22" rx="8" fill="#687680"/>
<rect x="52" y="372" width="15" height="29" rx="3" fill="#87939d"/>
<rect x="1253" y="372" width="15" height="29" rx="3" fill="#87939d"/>

<!-- RF GENERATOR -->
<rect x="45" y="105" width="190" height="145" rx="16" fill="#eef4f8" stroke="#2a5677" stroke-width="2"/>
<text x="140" y="136" text-anchor="middle" class="title">RF OSCILLATOR</text>
<text x="140" y="166" text-anchor="middle" class="bold">{frequency_mhz:.2f} MHz</text>
<text x="140" y="188" text-anchor="middle" class="small">Sinusoidal electrical drive</text>
<polyline points="78,218 94,208 110,228 126,208 142,228 158,208 174,228 190,208 206,218"
          fill="none" stroke="#177ea7" stroke-width="2.4"/>
<circle cx="61" cy="127" r="6" fill="{"#2d996c" if st.session_state.rf else "#a1adb7"}"/>

<!-- CABLE -->
<line x1="235" y1="177" x2="275" y2="177" stroke="#496377" stroke-width="4"/>
<polygon points="274,171 286,177 274,183" fill="#496377"/>

<!-- TRANSMITTER CRYSTAL -->
<rect x="286" y="96" width="105" height="162" rx="10" fill="#d9c184" stroke="#87661e" stroke-width="2"/>
<text x="338" y="125" text-anchor="middle" class="title">PZT</text>
<text x="338" y="146" text-anchor="middle" class="title">CRYSTAL</text>
<text x="338" y="172" text-anchor="middle" class="small">Transmitter</text>

<!-- mechanical vibration arrows -->
<g class="pulse">
<line x1="397" y1="132" x2="430" y2="132" stroke="#a45c1f" stroke-width="3"/>
<polygon points="430,125 442,132 430,139" fill="#a45c1f"/>
<line x1="397" y1="164" x2="430" y2="164" stroke="#a45c1f" stroke-width="3"/>
<polygon points="430,157 442,164 430,171" fill="#a45c1f"/>
<line x1="397" y1="196" x2="430" y2="196" stroke="#a45c1f" stroke-width="3"/>
<polygon points="430,189 442,196 430,203" fill="#a45c1f"/>
<text x="343" y="282" text-anchor="middle" class="small">Inverse piezoelectric effect</text>
</g>

<!-- LIQUID CELL -->
<rect x="446" y="79" width="520" height="220" rx="18" fill="#e9f7fb" stroke="#4b96aa" stroke-width="2.2"/>
<text x="706" y="106" text-anchor="middle" class="title">{liquid.upper()} SAMPLE CELL</text>
<text x="706" y="125" text-anchor="middle" class="small">Longitudinal ultrasonic field</text>

<!-- ultrasonic field -->
<g class="waveGroup">
  <path d="M480 178 C520 142,560 214,600 178 S680 142,720 178 S800 214,840 178 S920 142,960 178"
        fill="none" stroke="#1586a9" stroke-width="4"/>
  <path d="M480 197 C520 161,560 233,600 197 S680 161,720 197 S800 233,840 197 S920 161,960 197"
        fill="none" stroke="#8bc6d5" stroke-width="2"/>
</g>

<!-- compression / rarefaction bands -->
<g opacity=".35">
  <rect x="505" y="142" width="12" height="105" rx="6" fill="#2b89a0"/>
  <rect x="585" y="142" width="12" height="105" rx="6" fill="#7bb3c0"/>
  <rect x="665" y="142" width="12" height="105" rx="6" fill="#2b89a0"/>
  <rect x="745" y="142" width="12" height="105" rx="6" fill="#7bb3c0"/>
  <rect x="825" y="142" width="12" height="105" rx="6" fill="#2b89a0"/>
  <rect x="905" y="142" width="12" height="105" rx="6" fill="#7bb3c0"/>
</g>

<text x="706" y="268" text-anchor="middle" class="small">Compression ⇄ Rarefaction • Incident + reflected waves form standing wave</text>

<!-- REFLECTOR -->
<rect x="986" y="74" width="32" height="245" rx="5" fill="#616d77" stroke="#3d474f" stroke-width="1.5"/>
<text x="1002" y="60" text-anchor="middle" class="mid">REFLECTOR</text>
<line x1="970" y1="323" x2="1025" y2="323" stroke="#8d6621" stroke-width="2"/>
<polygon points="970,323 980,318 980,328" fill="#8d6621"/>
<polygon points="1025,323 1015,318 1015,328" fill="#8d6621"/>

<!-- RECEIVER / PICKUP -->
<rect x="1048" y="104" width="170" height="124" rx="15" fill="#f4f1e5" stroke="#8a743e" stroke-width="2"/>
<circle cx="1133" cy="143" r="22" fill="none" stroke="#8a743e" stroke-width="3"/>
<circle cx="1133" cy="143" r="10" fill="none" stroke="#8a743e" stroke-width="2"/>
<text x="1133" y="182" text-anchor="middle" class="title">PICK-UP DETECTOR</text>
<text x="1133" y="202" text-anchor="middle" class="small">Direct piezoelectric response</text>

<!-- DETECTOR CABLE -->
<line x1="1133" y1="228" x2="1133" y2="268" stroke="#6f5a29" stroke-width="3"/>
<polygon points="1127,267 1133,278 1139,267" fill="#6f5a29"/>

<!-- METER -->
<rect x="1042" y="279" width="183" height="55" rx="11" fill="#eef3f6" stroke="#aab7c2"/>
<text x="1056" y="299" class="small">METER</text>
<text x="1056" y="322" class="title">{detector_output*100:.1f} %</text>
<rect x="1130" y="300" width="78" height="10" rx="5" fill="#dce4ea"/>
<rect x="1130" y="300" width="{78*detector_level:.1f}" height="10" rx="5" fill="#177ea7"/>

<!-- MICROMETER -->
<rect x="660" y="324" width="225" height="42" rx="11" fill="#eef1f4" stroke="#75818c" stroke-width="1.5"/>
<text x="675" y="342" class="small">MICROMETER / REFLECTOR POSITION</text>
<text x="865" y="352" text-anchor="end" class="bold">{position_mm:.3f} mm</text>

<!-- FLOW LABELS -->
<text x="114" y="73" text-anchor="middle" class="small">Electrical</text>
<text x="338" y="73" text-anchor="middle" class="small">Mechanical</text>
<text x="706" y="73" text-anchor="middle" class="small">Acoustic</text>
<text x="1110" y="73" text-anchor="middle" class="small">Electrical detection</text>

</svg>
</div>
</body>
</html>
"""

components.html(apparatus_html, height=435, scrolling=False)

# ============================================================
# OPERATING CONTROLS
# ============================================================
st.markdown('<div class="section-title">3. Operate the apparatus</div>', unsafe_allow_html=True)

left, center, right = st.columns([1.35, 1.0, 1.0])

with left:
    slider_max = max(4.0, maxima_spacing_mm * 10.0)
    slider_step = max(0.001, min(0.01, maxima_spacing_mm / 40.0))

    if st.session_state.power and st.session_state.rf:
        position = st.slider(
            "Reflector / micrometer position (mm)",
            min_value=0.0,
            max_value=slider_max,
            value=min(float(st.session_state.micrometer), slider_max),
            step=slider_step,
            key="reflector_slider",
            help="Move the reflector slowly through the standing-wave pattern.",
        )
        if abs(float(position) - st.session_state.micrometer) > 1e-12:
            st.session_state.micrometer = float(position)
            st.rerun()
    else:
        st.info("Turn ON Main Power and RF Oscillator to unlock the micrometer.")

    f1, f2, f3 = st.columns(3)
    with f1:
        if st.button("− Fine", use_container_width=True):
            if st.session_state.power and st.session_state.rf:
                st.session_state.micrometer = max(
                    0.0, st.session_state.micrometer - max(slider_step, 0.001)
                )
                st.rerun()
    with f2:
        if st.button("Home", use_container_width=True):
            st.session_state.micrometer = 0.0
            st.rerun()
    with f3:
        if st.button("+ Fine", use_container_width=True):
            if st.session_state.power and st.session_state.rf:
                st.session_state.micrometer = min(
                    slider_max, st.session_state.micrometer + max(slider_step, 0.001)
                )
                st.rerun()

with center:
    st.markdown('<div class="card"><h3>Pick-up detector</h3>', unsafe_allow_html=True)
    if st.session_state.power and st.session_state.rf and st.session_state.detector:
        st.metric("Relative intensity", f"{detector_output*100:.1f}%")
        progress = max(2, min(100, int(detector_output * 100)))
        st.markdown(
            f"""
<div style="height:16px;background:#e6edf2;border-radius:10px;overflow:hidden;margin:9px 0;">
  <div style="height:100%;width:{progress}%;background:#177ea7;"></div>
</div>
""",
            unsafe_allow_html=True,
        )
        if detector_output >= 0.88:
            st.success("RESONANCE MAXIMUM")
        elif detector_output <= 0.12:
            st.info("RESonance minimum")
        else:
            st.caption("Intermediate response — continue scanning.")
    else:
        st.warning("Detector requires Main Power + RF + Detector ON.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card"><h3>Experimental recording</h3>', unsafe_allow_html=True)
    can_record = (
        st.session_state.power
        and st.session_state.rf
        and st.session_state.detector
        and detector_output >= 0.82
    )

    if st.button("Record maximum", use_container_width=True, disabled=not can_record):
        current = float(st.session_state.micrometer)
        records = list(st.session_state.records)

        if not records or abs(current - records[-1]) >= maxima_spacing_mm * 0.35:
            records.append(current)
            st.session_state.records = records
            st.session_state.last_message = (
                f"Maximum #{len(records)} recorded at {current:.3f} mm."
            )
        else:
            st.session_state.last_message = (
                "Continue moving the reflector before recording another maximum."
            )

    if st.button("Clear recorded values", use_container_width=True):
        st.session_state.records = []
        st.session_state.last_message = "Recorded measurements cleared."

    st.caption(st.session_state.last_message)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# OSCILLOSCOPE / SIGNALS
# ============================================================
st.markdown('<div class="section-title">4. Electrical and detector signals</div>', unsafe_allow_html=True)

sig1, sig2 = st.columns(2)

with sig1:
    time_window = np.linspace(0, 4.0 / frequency_hz, 1000)
    electrical = (
        np.sin(2 * np.pi * frequency_hz * time_window)
        if st.session_state.power and st.session_state.rf
        else np.zeros_like(time_window)
    )

    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(time_window * 1e6, electrical, lw=2)
    ax.axhline(0, lw=.75, alpha=.45)
    ax.set_title("RF oscillator output")
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Relative voltage")
    ax.grid(alpha=.18)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with sig2:
    scan_max = max(4.0, maxima_spacing_mm * 10.0)
    scan = np.linspace(0, scan_max, 1400)
    response = 0.5 * (1 + np.cos(2 * np.pi * scan / maxima_spacing_mm)) * 100

    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(scan, response, lw=2, label="Detector response")

    if st.session_state.records:
        rec = np.array(st.session_state.records)
        rec_y = 0.5 * (1 + np.cos(2 * np.pi * rec / maxima_spacing_mm)) * 100
        ax.scatter(rec, rec_y, s=42, zorder=4, label="Your measurements")

    ax.axvline(position_mm, lw=1.1, alpha=.45, label="Current position")
    ax.set_title("Detector response during reflector scan")
    ax.set_xlabel("Micrometer position (mm)")
    ax.set_ylabel("Relative intensity (%)")
    ax.set_ylim(-5, 105)
    ax.grid(alpha=.18)
    ax.legend()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ============================================================
# STANDING WAVE / PRESSURE FIELD
# ============================================================
st.markdown('<div class="section-title">5. Interference inside the liquid</div>', unsafe_allow_html=True)

wv1, wv2 = st.columns(2)

x = np.linspace(0, max(2.5, wavelength_mm * 5), 1200)
k = 2 * np.pi / wavelength_mm

incident = np.sin(k * x)
reflected = -np.sin(k * x)
resultant = incident + reflected
pressure = np.cos(k * x)

with wv1:
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(x, incident, lw=1.3, label="Incident wave")
    ax.plot(x, reflected, lw=1.3, label="Reflected wave")
    ax.plot(x, resultant, lw=2.5, label="Standing-wave result")
    ax.set_title("Wave interference")
    ax.set_xlabel("Position in liquid (mm)")
    ax.set_ylabel("Relative displacement")
    ax.grid(alpha=.18)
    ax.legend()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with wv2:
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.fill_between(x, 0, pressure, alpha=.23)
    ax.axhline(0, lw=.75, alpha=.45)
    ax.set_title("Longitudinal pressure field")
    ax.set_xlabel("Position in liquid (mm)")
    ax.set_ylabel("Relative pressure")
    ax.grid(alpha=.18)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ============================================================
# MEASUREMENT / VELOCITY
# ============================================================
st.markdown('<div class="section-title">6. Your measurement → wavelength → velocity</div>', unsafe_allow_html=True)

records = list(st.session_state.records)

if len(records) >= 2:
    rec_sorted = np.array(sorted(records), dtype=float)
    spacings = np.diff(rec_sorted)

    measured_d_mm = float(np.mean(spacings))
    measured_lambda_mm = 2 * measured_d_mm
    measured_velocity = frequency_hz * measured_lambda_mm * 1e-3
    deviation = abs(measured_velocity - reference_velocity) / reference_velocity * 100.0

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Mean spacing d", f"{measured_d_mm:.4f} mm")
    r2.metric("Measured wavelength λ", f"{measured_lambda_mm:.4f} mm")
    r3.metric("Measured velocity v", f"{measured_velocity:.1f} m/s")
    r4.metric("Deviation", f"{deviation:.2f}%")

    st.markdown(
        f"""
<div class="soft">
<b>Experimental calculation from your recorded maxima</b><br><br>
Successive maxima are separated by d, therefore:<br><br>
<b>λ = 2d = 2 × {measured_d_mm:.4f} mm = {measured_lambda_mm:.4f} mm</b><br><br>
Then:<br><br>
<b>v = fλ = ({frequency_mhz:.2f} × 10⁶ Hz) × ({measured_lambda_mm*1e-3:.7f} m)
= {measured_velocity:.1f} m/s</b>
</div>
""",
        unsafe_allow_html=True,
    )

    table_data = {
        "Maximum": list(range(1, len(rec_sorted) + 1)),
        "Micrometer position (mm)": [round(float(x), 4) for x in rec_sorted],
        "Spacing from previous (mm)": ["—"] + [round(float(x), 4) for x in spacings],
    }
    st.dataframe(table_data, use_container_width=True, hide_index=True)

    csv = "Maximum,Micrometer position (mm),Spacing from previous (mm)\n"
    for idx, value in enumerate(rec_sorted):
        previous = "" if idx == 0 else f"{spacings[idx-1]:.4f}"
        csv += f"{idx+1},{value:.4f},{previous}\n"

    st.download_button(
        "Download measurements as CSV",
        data=csv.encode("utf-8"),
        file_name="ultrasonic_interferometer_measurements.csv",
        mime="text/csv",
    )
else:
    st.markdown(
        """
<div class="status">
<b>Measurement in progress:</b> Find and record at least two successive resonance maxima.
The app will then calculate <b>d</b>, <b>λ = 2d</b> and <b>v = fλ</b> from your measurements.
</div>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# TRANSDUCTION EXPLANATION
# ============================================================
st.markdown('<div class="section-title">7. How the signal is converted</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.columns(4)

with t1:
    st.markdown(
        """
<div class="card">
<h3>1 • Electrical signal</h3>
The RF oscillator generates an alternating electrical voltage at the selected frequency.
</div>
""",
        unsafe_allow_html=True,
    )

with t2:
    st.markdown(
        """
<div class="card">
<h3>2 • Crystal vibration</h3>
The inverse piezoelectric effect converts the electrical excitation into periodic mechanical strain in the crystal.
</div>
""",
        unsafe_allow_html=True,
    )

with t3:
    st.markdown(
        """
<div class="card">
<h3>3 • Ultrasound</h3>
The vibrating crystal produces pressure variations that propagate through the liquid as a longitudinal ultrasonic wave.
</div>
""",
        unsafe_allow_html=True,
    )

with t4:
    st.markdown(
        """
<div class="card">
<h3>4 • Electrical detection</h3>
A piezoelectric pick-up responds to the acoustic field through the direct piezoelectric effect, producing an electrical detector signal.
</div>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# LAB PROCEDURE
# ============================================================
st.markdown('<div class="section-title">8. Virtual laboratory procedure</div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="card">
<span class="pill">01</span> Select the liquid and RF frequency.<br><br>
<span class="pill">02</span> Switch ON the <b>Main Power</b>.<br><br>
<span class="pill">03</span> Switch ON the <b>RF Oscillator</b> and observe the transmitting crystal.<br><br>
<span class="pill">04</span> Switch ON the <b>Pick-up Detector</b>.<br><br>
<span class="pill">05</span> Move the reflector using the virtual micrometer.<br><br>
<span class="pill">06</span> Watch the detector meter and locate a clear <b>resonance maximum</b>.<br><br>
<span class="pill">07</span> Record that maximum and continue scanning to the next maxima.<br><br>
<span class="pill">08</span> After several readings, calculate the average spacing and obtain <b>λ = 2d</b> and <b>v = fλ</b>.
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
<div class="footer">
<strong>AMAN EDGE PHYSICS</strong><br>
Ultrasonic Interferometer • Interactive Physics Laboratory<br>
<span style="font-size:14px;">Made with <span style="color:#d64545;">♥</span> Aman Kumar Patel</span><br>
© 2026 Aman Edge Physics. All rights reserved.
</div>
""",
    unsafe_allow_html=True,
)
