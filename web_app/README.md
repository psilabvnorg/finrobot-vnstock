# Vietnamese Stock Analysis Web UI

A simple web interface for analyzing Vietnamese stocks using FinRobot and Azure GPT-4o.

## Features

- 🎯 Simple, clean web interface
- 📊 Real-time stock analysis using vnstock data
- 🤖 Powered by Azure GPT-4o
- 📝 Customizable analysis prompts
- 💾 Download and copy reports
- 🚀 Hosted on port 6900

## Quick Start

### 1. Install Dependencies

```bash
# Make sure you're in the FinRobot root directory
cd /home/psilab/FinRobot

# Activate your virtual environment
source venv/bin/activate

# Install FastAPI and uvicorn
pip install fastapi uvicorn[standard]
```

### 2. Start the Server

```bash
cd web_app
chmod +x start_server.sh
./start_server.sh
```

Or run directly:

```bash
cd web_app
python main.py
```

### 3. Access the UI

Open your browser and navigate to:
- **Web UI**: http://localhost:6900
- **API Docs**: http://localhost:6900/docs

## Usage

1. **Enter Stock Ticker**: Type the stock code (e.g., VPB, VCB, FPT)
2. **Customize Prompt**: Edit the analysis prompt or use the default template
3. **Analyze**: Click "🚀 Analyze Stock" and wait 30-60 seconds
4. **View Results**: The analysis report appears on the right panel
5. **Export**: Copy to clipboard or download as text file

## Default Analysis Template

The default template analyzes:
1. Price data for last 3 months
2. Financial ratios (P/E, P/B, ROE, ROA, Debt/Equity)
3. Price trends and valuation
4. Comparison with peers (TCB, VCB for banks)
5. Technical analysis (Moving Averages, RSI)
6. Investment recommendations

## API Endpoints

### `GET /`
Serves the web UI

### `POST /analyze`
Analyze a stock based on prompt

**Request Body:**
```json
{
  "prompt": "Analysis instructions...",
  "ticker": "VPB"
}
```

**Response:**
```json
{
  "status": "success",
  "ticker": "VPB",
  "timestamp": "2026-01-08T...",
  "report": "Full analysis report...",
  "message_count": 5
}
```

### `GET /templates/default`
Get the default analysis template

### `GET /health`
Health check endpoint

## Configuration

The server uses your existing FinRobot configuration:
- **OAI_CONFIG_LIST**: Azure OpenAI credentials (in parent directory)
- **Port**: 6900 (configurable in main.py)
- **Host**: 0.0.0.0 (accessible from network)

## Customization

### Change Port
Edit `main.py`, line at the bottom:
```python
uvicorn.run(app, host="0.0.0.0", port=6900)  # Change to your preferred port
```

### Modify UI Theme
Edit `/static/index.html` CSS section to change colors, fonts, layout

### Add New Templates
Add new endpoints in `main.py`:
```python
@app.get("/templates/custom")
def get_custom_template():
    return {"template": "Your custom template..."}
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 6900
lsof -i :6900

# Kill the process
kill -9 <PID>
```

### Dependencies Missing
```bash
pip install fastapi uvicorn[standard] python-multipart
```

### Azure API Errors
- Check your `OAI_CONFIG_LIST` has valid credentials
- Verify API endpoint URL is correct
- Ensure you have sufficient API quota

### vnstock Data Issues
- Check internet connection
- Verify ticker symbol is correct
- Some stocks may have limited historical data

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Azure OpenAI GPT-4o
- **Data**: vnstock (Vietnamese stock data)
- **Agent Framework**: AutoGen + FinRobot

## Integration with anything-llm

This web UI can serve as:
1. **Standalone service** - Run independently
2. **API backend** - Integrate via REST API
3. **MCP server** - Convert to Model Context Protocol server
4. **Custom agent** - Wrap as anything-llm agent skill

See parent directory for integration options.

## License

Same as FinRobot parent project
