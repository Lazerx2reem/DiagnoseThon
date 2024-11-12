# DiagnoseThon

**DiagnoseThon** is a project that generates medical questions and diagnoses based on episode summaries from the TV show *House M.D.* By leveraging the OpenAI API, we simulate the process of identifying potential medical conditions from case descriptions, similar to the show's diagnostic approach. 

This project was developed as part of the **[Diagnose-a-thon](https://csrai.psu.edu/initiatives/diagnose-a-thon)** contest, an initiative focused on advancing AI-driven medical problem-solving.

## Overview

In this project, we:
- Use episode summaries from *House M.D.* to create realistic diagnostic scenarios.
- Generate relevant medical questions and suggest associated medical diagnoses using OpenAI API calls.
- Aim to bring medical diagnostics closer to reality by utilizing a unique dataset (TV medical cases) in a novel AI application.

## Getting Started

### Prerequisites
- OpenAI API key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ajaynarayanan/DiagnoseThon.git
   ```
2. Navigate to the project directory:
   ```bash
   cd DiagnoseThon
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Ensure you have an OpenAI API key. You can get one by signing up at [OpenAI's website](https://beta.openai.com/signup/).
2. Set up your environment variables:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```
3. Run the main script to generate medical questions and diagnoses from episode summaries:
   ```bash
   python diagnose_thon.py
   ```

## Example

Given a sample *House M.D.* episode summary:
> "A young patient exhibits unusual symptoms, and Dr. House suspects an autoimmune disorder."

The model might generate:
- **Medical Question:** "Could the patient's symptoms indicate an underlying autoimmune condition?"
- **Suggested Diagnosis:** "Systemic Lupus Erythematosus (SLE)"

## Attribution

This project uses information from House Wiki on Fandom, licensed under CC BY-SA 4.0. All content sourced from Fandom is subject to copyright held by the original creators and Fandom, Inc. We provide this information solely for educational and demonstrative purposes, and we do not claim ownership over any content sourced from Fandom.
