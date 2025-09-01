# Drug Detection Project

This repository contains a multi-component drug detection system:

- **Flask Backend (`server.py`)**: Logs visitor data, detects VPN/proxy usage using IP-API and ISP/ASN heuristics, and serves a login form. Visitor details (IP, location, VPN status, email, phone) are saved to `visitors.csv`.

- **Streamlit Dashboard (`frontend.py`)**: Visualizes flagged users from `visitors.csv` with filters for VPN status and search by email/phone. Sidebar shows summary statistics.

- **TF-IDF Text Classification (`tfidf.py`)**: Uses scikit-learn to train a logistic regression model on text data for binary classification (e.g., drug-related vs. not). Includes a function to predict new text and outputs class probabilities.

- **Telegram Monitoring Pipeline (`pipeline.py`)**: Uses Telethon and Google Gemini API to classify Telegram chat messages for drug-related content. Severity scores (0-10) are logged to `dev_log.txt`. High-severity messages trigger alerts.

## Project Structure

- `frontend.py`: Streamlit dashboard for flagged users, with filters and summary statistics.
- `server.py`: Flask backend for logging visitor data, detecting VPN/proxy usage, and serving a login form.
- `tfidf.py`: TF-IDF vectorization and logistic regression for text classification (Primary Clasification Not used).
- `pipeline.py`: Telegram monitoring script using Telethon and Google Gemini API to classify chat messages for drug-related content.
- `visitors.csv`: Visitor tracking data (IP, location, VPN status, email, phone, etc.).
- `dev_log.txt`: Development log of all messages on telegram group and message severity scores.
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

## License

Specify your license here (e.g., MIT, Apache 2.0, etc.).
