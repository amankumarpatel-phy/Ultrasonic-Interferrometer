# AMAN EDGE PHYSICS — Ultrasonic Interferometer

A polished interactive **virtual physics laboratory** for the ultrasonic interferometer experiment.

## Virtual laboratory model

**Main power → RF oscillator → piezoelectric transducer → liquid sample → reflector + micrometer → pick-up detector → resonance maxima → velocity calculation**

The apparatus is rendered inside a dedicated Streamlit HTML component so the laboratory visualization is displayed as an instrument rather than as HTML source code.

## Features

- Centered Aman Edge Physics header
- Replaceable `assets/logo.png`
- Main power / RF / detector controls
- Animated PZT / quartz concept
- Electrical sinusoidal signal
- Ultrasonic wave visualization
- Compression / rarefaction
- Incident and reflected waves
- Standing-wave visualization
- Virtual reflector and micrometer
- Live detector intensity
- Detector response during reflector scanning
- Manual recording of resonance maxima
- Mean-spacing calculation
- Wavelength calculation
- Velocity calculation
- Measurement table
- CSV export
- Guided virtual-labor procedure

## Virtual experiment

The learner operates the simulated apparatus and records successive resonance maxima.

For two successive constructive-interference maxima:

`2d = λ`

Therefore:

`λ = 2d`

and:

`v = fλ = 2fd`

The application calculates the result from the student's recorded micrometer positions.

## Project structure

```text
ultrasonic-interferometer/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── assets/
    └── logo.png
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub / Streamlit deployment

Upload the project to GitHub and deploy `app.py` using Streamlit Community Cloud.

## Replace the logo

Replace:

`assets/logo.png`

with the actual Aman Edge Physics logo.

Keep the same filename and path.

## Branding

**AMAN EDGE PHYSICS**  
Ultrasonic Interferometer • Interactive Physics Laboratory

Made with ♥️ Aman Kumar Patel

© 2026 Aman Edge Physics. All rights reserved.
