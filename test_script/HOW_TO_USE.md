# FinRobot Usage Guide (No Traditional Frontend)

## 📌 Important: FinRobot is a Backend/Agent Framework

**FinRobot does NOT have a traditional web frontend** like a React or Vue.js app. It's designed as a **Python-based AI agent framework** for financial analysis.

---

## 🎯 How to Use FinRobot

### Option 1: Run Python Scripts Directly (Recommended)

```bash
# Quick start with Vietnamese stock analysis
cd /home/psilab/FinRobot
python start_vietnamese_analysis.py
```

This will:
- Load your Azure GPT-4o configuration
- Create a Vietnamese stock analyst agent
- Analyze VPB (VP Bank) stock
- Show results in the terminal

### Option 2: Run Examples

```bash
# Run the comprehensive Vietnamese stock examples
python examples/vietnamese_stock_analysis.py
```

### Option 3: Use in Your Python Code

```python
import autogen
from finrobot.data_source import VNStockUtils
from finrobot.agents.workflow import FinRobot

# Your custom analysis code here
```

### Option 4: Use Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Create a new notebook and use FinRobot
```

---

## 🌐 About "Frontend"

### What FinRobot Has:
- ✅ **Python API** - Import and use in Python code
- ✅ **CLI Scripts** - Run from terminal
- ✅ **Jupyter Notebooks** - Interactive analysis
- ✅ **Agent Framework** - AutoGen multi-agent system

### What FinRobot Does NOT Have:
- ❌ **Web UI** - No React/Vue.js frontend
- ❌ **Web Server** - No Flask/FastAPI server
- ❌ **Dashboard** - No web-based dashboard

### Commercial Alternative:
**FinRobot Pro** (https://finrobot.ai/) is a separate commercial platform with a web interface, but it's not included in this open-source repository.

---

## 🚀 Quick Start Commands

### 1. Test Integration
```bash
python test_vnstock_integration.py
```

### 2. Start Quick Analysis
```bash
python start_vietnamese_analysis.py
```

### 3. Run Examples
```bash
python examples/vietnamese_stock_analysis.py
```

### 4. Custom Analysis
Edit `start_vietnamese_analysis.py` and change the `task` variable:
```python
task = dedent(f"""
    Analyze FPT Corporation stock...
    Your custom requirements here...
""")
```

---

## 🔧 Your Azure Configuration

Your `OAI_CONFIG_LIST` is configured with:
```json
{
    "model": "gpt-4o",
    "api_type": "azure",
    "base_url": "https://tungtest.openai.azure.com/..."
}
```

This is **already working** - just run the scripts!

---

## 💡 Workflow

1. **Edit the script** → Customize what you want to analyze
2. **Run the script** → `python start_vietnamese_analysis.py`
3. **View results** → Results appear in your terminal
4. **Save results** → Output saved to `vietnamese_analysis/` folder

---

## 📊 Example Output

When you run the scripts, you'll see:
```
================================================================================
VIETNAMESE STOCK ANALYSIS - QUICK START
Using Azure GPT-4o
================================================================================

[1/3] Loading Azure GPT-4o configuration...
✅ Azure GPT-4o configuration loaded

[2/3] Creating Vietnamese Stock Analyst agent...
✅ Analyst agent ready

[3/3] Starting analysis...
================================================================================

User (to Vietnamese_Stock_Analyst):
Phân tích cổ phiếu VPB...

Vietnamese_Stock_Analyst: [Analysis appears here...]

[Generated code, charts, data tables...]

✅ Analysis Complete!
```

---

## 🎨 Want a Web Frontend?

If you need a web interface, you would need to build it separately:

### Option A: Build Your Own
```python
# Example: Simple Flask API wrapper
from flask import Flask, request, jsonify
from finrobot.data_source import VNStockUtils

app = Flask(__name__)

@app.route('/api/stock/<ticker>')
def get_stock(ticker):
    data = VNStockUtils.get_stock_data(ticker, "VCI", ...)
    return jsonify(data.to_dict())

app.run()
```

### Option B: Use Streamlit
```python
# Create a simple UI with Streamlit
import streamlit as st
from finrobot.data_source import VNStockUtils

st.title("Vietnamese Stock Analysis")
ticker = st.text_input("Enter ticker:")
if ticker:
    data = VNStockUtils.get_stock_data(ticker, "VCI", ...)
    st.dataframe(data)
```

### Option C: Use Gradio
```python
# Quick UI with Gradio
import gradio as gr
from finrobot.data_source import VNStockUtils

def analyze_stock(ticker):
    data = VNStockUtils.get_stock_data(ticker, "VCI", ...)
    return data

gr.Interface(fn=analyze_stock, inputs="text", outputs="dataframe").launch()
```

But these are **separate projects** - not included in FinRobot by default.

---

## 📚 Recommended Workflow

**For Data Exploration:**
```bash
# Use Jupyter Notebook
jupyter notebook
# Create cells with FinRobot code
```

**For Automated Analysis:**
```bash
# Create Python scripts
python my_analysis.py
```

**For Interactive Chat:**
```bash
# Run the agent scripts
python start_vietnamese_analysis.py
```

**For Scheduled Reports:**
```bash
# Use cron jobs to run scripts
0 9 * * * cd /home/psilab/FinRobot && python daily_analysis.py
```

---

## ✅ Your Next Steps

1. **Run the quick start:**
   ```bash
   python start_vietnamese_analysis.py
   ```

2. **Customize it:**
   - Edit the `task` in `start_vietnamese_analysis.py`
   - Change ticker symbols
   - Modify analysis requirements

3. **Check examples:**
   ```bash
   python examples/vietnamese_stock_analysis.py
   ```

4. **Build your own scripts:**
   - Copy example files
   - Customize for your needs
   - Automate with cron/scheduler

---

## 🆘 Common Questions

**Q: Where is the web interface?**
A: There isn't one. FinRobot is a Python framework, not a web app.

**Q: How do I see the results?**
A: Results appear in your terminal and are saved to the `work_dir` folder.

**Q: Can I build a web UI?**
A: Yes! Use Flask, Streamlit, or Gradio to wrap FinRobot APIs.

**Q: What about FinRobot Pro?**
A: That's a separate commercial service at finrobot.ai (not open source).

---

**Ready to start? Run:**
```bash
python start_vietnamese_analysis.py
```

🚀📈🇻🇳
