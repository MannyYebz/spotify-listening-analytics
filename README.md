<div align="center">

# 🎵 Spotify Listening Profile Dashboard

**Analyze and visualize your Spotify listening habits using Python and the Spotify Web API**

A data analytics project that collects personal listening data from Spotify, transforms it into analysis-ready datasets, and presents the results through tables and visualizations.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Spotify API](https://img.shields.io/badge/API-Spotify-green)
![Data Analytics](https://img.shields.io/badge/Focus-Data%20Analytics-orange)

</div>

---

## 📖 Overview

Streaming platforms generate large amounts of behavioral data that can be used to uncover trends and patterns in user activity. This project uses the Spotify Web API to collect listening data and transform it into meaningful summaries and visual reports.

After authenticating with Spotify, the application retrieves listening history, favorite artists, top tracks, and recent activity, then presents the results through structured tables and charts.

---

## ✨ Features

* 🔐 Authenticate securely with Spotify using OAuth 2.0
* 🎤 Retrieve top artists across short-, medium-, and long-term periods
* 🎵 Retrieve top tracks across multiple time horizons
* 🕒 Collect recently played listening history
* 📊 Display results as formatted terminal-based tables
* 📈 Generate visualizations and save them to the `/charts` folder
* 🔄 Transform raw API responses into analysis-ready datasets

---

## 📊 Example Insights

The dashboard can help answer questions such as:

* Which artists dominate my listening habits?
* How do my favorite tracks change over time?
* Which artists consistently appear across different time periods?
* What listening patterns are visible in my recent activity?

---

## 🛠️ Tech Stack

| Category           | Technology      |
| ------------------ | --------------- |
| Programming        | Python 3.12     |
| API Integration    | Spotify Web API |
| Authentication     | OAuth 2.0       |
| Data Analysis      | Pandas          |
| Visualization      | Matplotlib      |
| Configuration      | Python-dotenv   |
| Package Management | uv              |

---

## 📋 Requirements

Before getting started, ensure you have:

* Python 3.12+
* Spotify Premium Account
* Spotify Developer Application
* uv Package Manager

---

## ⚡ Step 1: Install uv

uv is a modern Python package manager that simplifies dependency and virtual environment management.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:

```bash
uv --version
```

---

## 🎧 Step 2: Create a Spotify Developer Application

Spotify API access requires application credentials.

1. Visit https://developer.spotify.com
2. Sign in with your Spotify account
3. Open **Dashboard** → **Create App**
4. Configure the application:

   * **App Name:** Any name
   * **App Description:** Any description
   * **Redirect URI:** `http://127.0.0.1:9090`
   * Enable **Web API**
5. Save the application
6. Copy your **Client ID**
7. Copy your **Client Secret**

> These credentials are required for OAuth authentication.

---

## 📦 Step 3: Clone and Set Up the Project

Clone the repository:

```bash
git clone https://github.com/MannyYebz/spotify-listening-analytics.git
cd spotify-listening-analytics
```

Install dependencies:

```bash
uv sync
```

---

## 🔑 Step 4: Add Your Credentials

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Spotify credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:9090
```

---

## ▶️ Running the Project

Run the application:

```bash
uv run main.py
```

The first time you run the project, a browser window will open requesting authorization to access your Spotify data.

---

## 📂 Output

### Terminal Reports

* Top Artists
* Top Tracks
* Recently Played Tracks

### Visual Reports

Generated charts are automatically saved to:

```text
/charts
```

These visualizations provide a quick overview of listening trends and preferences.

---

## 🎯 Skills Demonstrated

This project showcases experience with:

* API Integration
* OAuth 2.0 Authentication
* Data Collection
* Data Transformation
* Exploratory Data Analysis (EDA)
* Data Visualization
* Working with JSON Data
* Python Analytics Workflows

---

## 🚀 Future Improvements

* Interactive dashboards with Streamlit
* Genre-level listening analysis
* Historical trend tracking
* Automated reporting
* CSV and Excel exports
* Recommendation and similarity analysis

---

## ⚠️ Disclaimer

This project is intended for educational and portfolio purposes. Spotify data remains the property of Spotify and is accessed through the official Spotify Web API under Spotify's developer terms.

---

<div align="center">

**Built with Python, APIs, and a passion for data analytics 🎵📊**

</div>
