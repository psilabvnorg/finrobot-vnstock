"""
Vietnamese Stock Analysis Web API
FastAPI server for interactive stock analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from pathlib import Path
import sys
import asyncio
from typing import Optional
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

import autogen
from finrobot.data_source import VNStockUtils
from finrobot.agents.workflow import FinRobot
from finrobot.utils import get_current_date
from textwrap import dedent

app = FastAPI(title="Vietnamese Stock Analysis API")

# Serve static files
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class AnalysisRequest(BaseModel):
    prompt: str
    ticker: Optional[str] = "VPB"


class MessageCapture:
    """Capture messages from autogen conversation"""
    def __init__(self):
        self.messages = []
        self.full_report = ""
    
    def capture(self, message):
        """Capture message content"""
        if isinstance(message, dict):
            content = message.get("content", "")
            if content and "TERMINATE" not in content:
                self.messages.append(content)
                self.full_report += content + "\n\n"


def create_analyst():
    """Create and return a configured analyst agent"""
    # Configuration for Azure GPT-4o
    # Look for OAI_CONFIG_LIST in parent directory
    config_path = Path(__file__).parent.parent / "OAI_CONFIG_LIST"
    llm_config = {
        "config_list": autogen.config_list_from_json(
            str(config_path),
            filter_dict={"model": ["gpt-4o"]},
        ),
        "temperature": 0,
        "cache_seed": 42,
    }
    
    # Create Vietnamese Stock Analyst Agent
    analyst_config = {
        "name": "Vietnamese_Stock_Analyst",
        "profile": dedent("""
            Bạn là Chuyên gia Phân tích Chứng khoán Việt Nam.
            You are a Vietnamese Stock Market Expert.
            
            Analyze Vietnamese stocks using vnstock data and provide insights in Vietnamese or English as requested.
            Available tools: stock prices, financial statements, financial ratios.
            
            Reply TERMINATE when done.
        """),
        "toolkits": [
            VNStockUtils.get_stock_data,
            VNStockUtils.get_balance_sheet,
            VNStockUtils.get_income_stmt,
            VNStockUtils.get_cash_flow,
            VNStockUtils.get_financial_ratios,
            VNStockUtils.get_company_info,
        ],
    }
    
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
        code_execution_config={
            "work_dir": "vietnamese_analysis",
            "use_docker": False,
        },
        max_consecutive_auto_reply=10,
    )
    
    analyst = FinRobot(
        agent_config=analyst_config,
        llm_config=llm_config,
        proxy=user_proxy,
    )
    
    return analyst, user_proxy


@app.get("/")
def read_root():
    """Serve the main UI"""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Vietnamese Stock Analysis",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/analyze")
async def analyze_stock(request: AnalysisRequest):
    """
    Analyze a Vietnamese stock based on the provided prompt
    """
    try:
        # Create analyst
        analyst, user_proxy = create_analyst()
        
        # Prepare the task
        task = request.prompt
        
        # Capture messages
        capture = MessageCapture()
        
        # Override the print function to capture output
        original_print = print
        
        def custom_print(*args, **kwargs):
            """Capture print statements"""
            msg = " ".join(str(arg) for arg in args)
            if msg and not msg.startswith("=") and not msg.startswith("✅") and not msg.startswith("["):
                capture.messages.append(msg)
        
        # Run analysis
        try:
            # Initiate chat
            chat_result = user_proxy.initiate_chat(analyst, message=task)
            
            # Extract only the final analyst response (not intermediate tool calls)
            final_report = ""
            if hasattr(chat_result, 'chat_history'):
                # Find the last message from Vietnamese_Stock_Analyst
                for msg in reversed(chat_result.chat_history):
                    if isinstance(msg, dict):
                        # Check if message is from the analyst
                        msg_name = msg.get('name', '')
                        msg_role = msg.get('role', '')
                        content = msg.get('content', '')
                        
                        # Only get messages from the analyst with substantial content
                        if (msg_name == 'Vietnamese_Stock_Analyst' or 
                            (msg_role == 'assistant' and '###' in content)):
                            
                            # Clean up the content
                            if content:
                                # Remove TERMINATE if present
                                content = content.replace('TERMINATE', '').strip()
                                
                                # Check if this is a substantial analysis (has markdown headers)
                                if '###' in content and len(content) > 300:
                                    final_report = content
                                    break
            
            if not final_report:
                final_report = "Phân tích hoàn tất nhưng không có kết quả chi tiết. Vui lòng thử lại."
            
            return {
                "status": "success",
                "ticker": request.ticker,
                "timestamp": datetime.now().isoformat(),
                "report": final_report,
                "message_count": 1
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Lỗi phân tích: {str(e)}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khởi tạo: {str(e)}"
        )


@app.get("/templates/default")
def get_default_template():
    """Get the default analysis template"""
    current_date = get_current_date()
    template = f"""Hôm nay là {current_date}.

Phân tích cổ phiếu VPB (VP Bank):

1. Lấy dữ liệu giá 3 tháng gần nhất
2. Lấy chỉ số tài chính (Financial Ratios) năm gần nhất
3. Đưa ra nhận xét về:
   - Xu hướng giá
   - Định giá (P/E, P/B)
   - Khả năng sinh lời (ROE, ROA)
   - Rủi ro tài chính (Debt/Equity)
4. So sánh với TCB và VCB trong cùng ngành ngân hàng.
5. Dự báo xu hướng giá trong 1 tháng tới dựa trên phân tích kỹ thuật đơn giản (Moving Averages, RSI).
6. Đưa ra khuyến nghị đầu tư dựa trên phân tích ở trên.
7. Kết luận có nên đầu tư vào VPB ở thời điểm hiện tại không, dựa trên phân tích ở trên.

Trả lời bằng tiếng Việt."""
    
    return {"template": template}


if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("VIETNAMESE STOCK ANALYSIS WEB SERVER")
    print("=" * 80)
    print("\n🚀 Starting server on http://localhost:6900")
    print("📊 Access the UI at: http://localhost:6900")
    print("📚 API docs at: http://localhost:6900/docs")
    print("\n" + "=" * 80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=6900)
