# AI Resume Screener

A Streamlit application that analyzes resumes against job descriptions using AI techniques.

## Features

- PDF resume upload and text extraction
- Job description analysis
- Match percentage calculation
- User-friendly interface
- Instant feedback

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-resume-screener.git
cd ai-resume-screener
```

2. Install the required packages:
```bash
cd frontend
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
cd frontend
streamlit run app.py
```

2. Open your web browser and go to http://localhost:8501

3. Upload your resume (PDF format) and paste the job description

4. Click "Analyze Resume" to get your match percentage

## Requirements

- Python 3.8+
- Streamlit
- PyMuPDF
- scikit-learn
- numpy

## License

MIT License