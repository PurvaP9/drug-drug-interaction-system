# Drug–Drug Interaction Checker

A prescription-based Drug–Drug Interaction (DDI) detection system that uses OCR to extract medicine names from prescription images and checks them against a DDInter-derived interaction dataset.

## Features

- Upload a prescription image
- Extract text using PyTesseract OCR
- Detect medicine names from the extracted text
- Generate unique medicine pairs
- Check pairs against the interaction database
- Classify interactions as:
  - Major
  - Moderate
  - Minor
  - Unknown
- Provide an explanation for each detected interaction
- Display results through a Gradio web interface
