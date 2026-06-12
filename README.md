<div align="center">

# 🎵 Spotify Listening Profile Dashboard

**Analyze your Spotify listening habits using Python and the Spotify Web API**

Built to learn REST APIs, OAuth 2.0 authentication, and data analysis with real-world user data.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Spotify API](https://img.shields.io/badge/API-Spotify-green)
![OAuth 2.0](https://img.shields.io/badge/Auth-OAuth%202.0-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---

## 📖 Overview

Music streaming platforms generate a large amount of behavioral data. This project demonstrates how that data can be collected, processed, and analyzed using Python.

After authenticating with Spotify, the application retrieves your listening information and presents it in structured tables, making it easy to identify trends in your music preferences.

---

## ✨ Current Features

* 🔐 Secure authentication through Spotify OAuth 2.0
* 🎤 Retrieve top artists across multiple time ranges
* 🎵 Retrieve top tracks across multiple time ranges
* 🕒 Access recently played listening history
* 📊 Display results in organized terminal-based data tables

### 🚀 Planned Enhancements

* Interactive charts and visualizations
* Listening trend analysis over time
* Genre and artist diversity metrics
* Exportable reports and dashboards

---

## 🛠️ Tech Stack

| Category           | Tools           |
| ------------------ | --------------- |
| Language           | Python 3.12+    |
| API                | Spotify Web API |
| Authentication     | OAuth 2.0       |
| Data Processing    | Pandas          |
| Configuration      | Python-dotenv   |
| Package Management | uv              |

---

## 📋 Requirements

Before getting started, ensure you have:

* Python 3.12 or newer
* A Spotify Premium account
* A Spotify Developer application
* The uv package manager

---

## ⚡ Install uv

This project uses **uv** for dependency management and virtual environments.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify the installation:

```bash
uv --version
```

---

## 🎧 Create a Spotify Developer Application

To access Spotify listening data, you will need your own API credentials.

### Steps

1. Visit https://developer.spotify.com
2. Sign in with your Spotify account
3. Open the Dashboard and select **Create App**
4. Configure the application:

   * **App Name:** Any name you choose
   * **Description:** Any description
   * **Redirect URI:** `http://127.0.0.1:9090`
   * Enable **Web API**
5. Save the application
6. Copy your **Client ID**
7. Reveal and copy your **Client Secret**

> 💡 These credentials allow the application to securely access your Spotify data.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/MannyYebz/spotify-listening-analytics.git
cd spotify-listening-analytics
```

Install project dependencies:

```bash
uv sync
```

---

## ⚙️ Configuration

Create a `.env` file in the project root directory:

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

Launch the application:

```bash
uv run main.py
```

The first time you run the project, a browser window will open asking you to authorize access to your Spotify account.

Once authenticated, the application will retrieve and display:

* Your top artists
* Your top tracks
* Your recently played songs

---

## 📈 Example Analysis Questions

This project can help answer questions such as:

* Which artists do I listen to most frequently?
* How have my listening preferences changed over time?
* What songs have dominated my recent listening history?
* Which artists consistently appear across multiple time periods?

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* REST API integration
* OAuth 2.0 authentication flows
* Secure credential management
* Data collection and transformation
* Working with JSON API responses
* Exploratory data analysis in Python

---

## 🔮 Future Development

Planned improvements include:

* Data visualization with Matplotlib and Plotly
* Listening behavior dashboards
* Genre distribution analysis
* Playlist analytics
* Historical trend tracking
* Exporting results to CSV and Excel

---

## ⚠️ Disclaimer

This project is intended for educational and portfolio purposes. Spotify data remains the property of Spotify and is accessed through the official Spotify Web API under Spotify's developer terms.

---

<div align="center">

**Built with Python, APIs, and a love of music analytics 🎵**

</div>
