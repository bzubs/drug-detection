# Drug Detection Project

This repository contains a drug detection system with:

- Python backend (Flask) for visitor tracking and VPN/proxy detection
- Streamlit dashboard frontend for flagged users
- TF-IDF-based text classification
- Telegram monitoring pipeline using Google Gemini AI for message severity scoring

## Project Structure

- `frontend.py`: Streamlit dashboard for flagged users, with filters and summary statistics.
- `server.py`: Flask backend for logging visitor data, detecting VPN/proxy usage, and serving a login form.
- `tfidf.py`: TF-IDF vectorization and logistic regression for text classification.
- `pipeline.py`: Telegram monitoring script using Telethon and Google Gemini API to classify chat messages for drug-related content.
- `visitors.csv`: Visitor tracking data (IP, location, VPN status, email, phone, etc.).
- `dev_log.txt`: Development log and message severity scores.
- `.gitignore`: Standard Python, VS Code, and data file ignores.
- `requirements.txt`: Python dependencies for all modules.

## Getting Started

1. Clone the repository:
   ```powershell
   git clone <your-repo-url>
   ```
2. Install required Python packages:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```powershell
   python server.py
   ```
4. Run the Streamlit dashboard:
   ```powershell
   streamlit run frontend.py
   ```
5. Run the Telegram monitoring pipeline (requires API keys):
   ```powershell
   python pipeline.py
   ```

## Features

- **Visitor Tracking:** Logs IP, location, VPN/proxy detection, and user details.
- **Dashboard:** Filter and search flagged users, view summary stats.
- **Text Classification:** TF-IDF and logistic regression for binary classification.
- **Telegram Monitoring:** AI-based severity scoring of chat messages for drug-related content using Google Gemini.
- **VPN/Proxy Detection:** Uses IP-API and ISP/ASN heuristics.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Specify your license here (e.g., MIT, Apache 2.0, etc.).
