<div align="center">
  
# 🔍 AI Web Search Assistant
</div>
<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://github.com/yourusername/ai-web-search-assistant/graphs/commit-activity)

### An intelligent search assistant powered by DeepSeek, Bing, and DuckDuckGo

[Features](#✨-features) •
[Installation](#🚀-installation) •
[Usage](#💡-usage) •
[Configuration](#⚙️-configuration) •
[Contributing](#🤝-contributing) •
[License](#📝-license)

</div>

## 🌟 Overview

AI Web Search Assistant is a sophisticated search tool that combines multiple search engines with AI-powered query interpretation and result summarization. It performs intelligent, multi-round searches while maintaining a local cache for improved performance.

### Key Highlights

- 🧠 Deep query interpretation using DeepSeek AI
- 🔄 Multi-round search refinement
- 🔍 Dual-engine search (Bing + DuckDuckGo)
- 💾 Smart result caching
- 📊 Comprehensive result summarization

## ✨ Features

- **Intelligent Query Analysis**
  - Interprets user intent
  - Suggests query improvements
  - Identifies key search terms

- **Advanced Search Capabilities**
  - Performs up to 5 rounds of refined searches
  - Combines results from multiple search engines
  - Eliminates duplicate findings
  - Automatically refines search strategy

- **Smart Caching System**
  - Local cache for faster repeated searches
  - Automatic cleanup of old cache files
  - Configurable cache retention period

- **Interactive Experience**
  - Real-time query refinement suggestions
  - Progress tracking for each search round
  - Clear result summaries

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-web-search-assistant.git
   cd ai-web-search-assistant
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   DEEPSEEK_API_KEY=your_deepseek_api_key
   BING_API_KEY=your_bing_api_key
   BING_ENDPOINT=https://api.bing.microsoft.com/v7.0/search
   ```

## 💡 Usage

1. **Start the Assistant**
   ```bash
   python main.py
   ```

2. **Enter Your Search Query**
   ```
   🔎 Welcome to the AI Web Search Assistant!
   ==================================================

   🤔 Enter your search topic: 
   ```

3. **Review and Refine**
   - The assistant will analyze your query
   - Suggest potential improvements
   - Allow you to refine the search

4. **Get Results**
   - Watch as it performs multiple search rounds
   - Review the comprehensive final summary
   - Optionally start a new search

## ⚙️ Configuration

Customize the assistant's behavior in `settings.py`:

```python
# Search Settings
MAX_SEARCH_ROUNDS = 5
RESULTS_PER_SEARCH = 5

# Cache Settings
CACHE_DIR = Path('cache')
CACHE_MAX_AGE_DAYS = 7
```

## 📁 Project Structure

```
ai-web-search-assistant/
├── main.py              # Entry point
├── settings.py          # Configuration
├── discovery.py         # Search functionality
├── deepseek_client.py   # AI client
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── cache/              # Cached results
└── README.md           # Documentation
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- DeepSeek API for powerful query interpretation
- Bing Web Search API for comprehensive search results
- DuckDuckGo for additional search capabilities

## 📫 Contact

Chris Royse - www.linkedin.com/in/christopher-royse-b624b596 - arcibu@ksu.edu

Project Link: [https://github.com/yourusername/ai-web-search-assistant](https://github.com/yourusername/ai-web-search-assistant)

---

<div align="center">

Made with ❤️ by Chris Royse (https://github.com/ChrisRoyse)

⭐️ Star this project if it helped you!

</div>
