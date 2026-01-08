"""
Quick Start Script for Vietnamese Stock Analysis
Using Azure GPT-4o

This is a simple interactive script to analyze Vietnamese stocks.
No complex frontend needed - just run and chat!
"""

import autogen
from finrobot.data_source import VNStockUtils
from finrobot.agents.workflow import FinRobot
from finrobot.utils import get_current_date
from textwrap import dedent


print("="*80)
print("VIETNAMESE STOCK ANALYSIS - QUICK START")
print("Using Azure GPT-4o")
print("="*80)

# Configuration for Azure GPT-4o
print("\n[1/3] Loading Azure GPT-4o configuration...")
try:
    llm_config = {
        "config_list": autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={"model": ["gpt-4o"]},
        ),
        "temperature": 0,
        "cache_seed": 42,
    }
    print("✅ Azure GPT-4o configuration loaded")
except Exception as e:
    print(f"❌ Error loading configuration: {e}")
    print("\nMake sure OAI_CONFIG_LIST has your Azure GPT-4o settings.")
    exit(1)

# Create Vietnamese Stock Analyst Agent
print("\n[2/3] Creating Vietnamese Stock Analyst agent...")
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
    human_input_mode="TERMINATE",  # You can interact when needed
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

print("✅ Analyst agent ready")

# Start Analysis
print("\n[3/3] Starting analysis...")
print("="*80)

# You can change this task or make it interactive
task = dedent(f"""
    Hôm nay là {get_current_date()}.
    
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
    
    Trả lời bằng tiếng Việt.
""")

print("\n📊 TASK: Analyzing VPB (VP Bank)")
print("="*80 + "\n")

try:
    user_proxy.initiate_chat(analyst, message=task)
    print("\n" + "="*80)
    print("✅ Analysis Complete!")
    print("="*80)
except Exception as e:
    print(f"\n❌ Error during analysis: {e}")
    print("\nTroubleshooting:")
    print("1. Check your Azure API key is valid")
    print("2. Verify the endpoint URL is correct")
    print("3. Make sure vnstock data is accessible")

print("\n" + "="*80)
print("To customize the analysis:")
print("  - Edit the 'task' variable in this script")
print("  - Change ticker symbol (VPB to VNM, FPT, etc.)")
print("  - Modify the questions/requirements")
print("="*80)
