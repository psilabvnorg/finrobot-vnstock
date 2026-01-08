"""
Vietnamese Stock Analysis Demo
Using VNStock data with FinRobot agents

This example shows how to analyze Vietnamese stocks using:
- VNStock data source (Vietnamese market)
- GPT-4o model (better Vietnamese language support)
- AutoGen multi-agent system

Popular Vietnamese stocks to try:
- VPB: VP Bank
- VNM: Vinamilk
- HPG: Hoa Phat Steel
- VIC: Vingroup
- FPT: FPT Corporation
- MSN: Masan Group
"""

import autogen
from finrobot.data_source import VNStockUtils
from finrobot.utils import get_current_date
from finrobot.agents.workflow import FinRobot
from finrobot.toolkits import register_toolkits
from textwrap import dedent


# Configuration for GPT-4o (Azure)
llm_config = {
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4o"]},  # Using GPT-4o for better Vietnamese support
    ),
    "temperature": 0,
    "cache_seed": 42,
}

# For Azure OpenAI, the config automatically includes api_type, base_url, etc.


# Create Vietnamese Stock Analyst Agent
vietnamese_analyst_config = {
    "name": "Vietnamese_Stock_Analyst",
    "profile": dedent("""
        Bạn là Chuyên gia Phân tích Chứng khoán Việt Nam với kiến thức sâu về thị trường chứng khoán Việt Nam.
        
        You are a Vietnamese Stock Market Expert Analyst with deep knowledge of Vietnamese stock market.
        
        Responsibilities:
        - Analyze Vietnamese stocks using vnstock data
        - Provide insights on Vietnamese companies' financial performance
        - Consider Vietnamese market characteristics (HOSE, HNX, UPCOM exchanges)
        - Understand Vietnamese financial regulations and reporting standards
        - Communicate in both Vietnamese and English as needed
        
        Available Data Sources:
        - Historical price data from Vietnamese exchanges
        - Financial statements (Balance Sheet, Income Statement, Cash Flow)
        - Financial ratios (P/E, P/B, EPS, BVPS, etc.)
        
        Note: Target prices and analyst reports are NOT available via API for Vietnamese market.
        
        Reply TERMINATE when analysis is complete.
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


# Create User Proxy (executes code)
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # Set to "ALWAYS" for interactive mode
    is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "work_dir": "vietnamese_analysis",
        "use_docker": False,
    },
    max_consecutive_auto_reply=10,
)


# Create the analyst agent
analyst = FinRobot(
    agent_config=vietnamese_analyst_config,
    llm_config=llm_config,
    proxy=user_proxy,
)


# Example 1: Analyze VP Bank (VPB)
def analyze_vpb():
    """Analyze VP Bank financial performance"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Analyzing VP Bank (VPB)")
    print("="*80 + "\n")
    
    task = dedent(f"""
        Hôm nay là {get_current_date()}.
        
        Hãy phân tích cổ phiếu VPB (VP Bank) với các bước sau:
        
        1. Lấy dữ liệu giá lịch sử 6 tháng gần nhất
        2. Lấy báo cáo tài chính năm (Balance Sheet, Income Statement, Cash Flow)
        3. Phân tích các chỉ số tài chính quan trọng (Financial Ratios)
        4. Đưa ra nhận xét về:
           - Xu hướng giá cổ phiếu
           - Tình hình tài chính (thanh khoản, sinh lời, tăng trưởng)
           - Định giá (P/E, P/B so với ngành ngân hàng)
        
        Please provide analysis in Vietnamese.
        Use the vnstock tools to gather data, then provide comprehensive analysis.
    """)
    
    user_proxy.initiate_chat(analyst, message=task)


# Example 2: Compare multiple Vietnamese stocks
def compare_stocks():
    """Compare multiple Vietnamese blue-chip stocks"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Comparing Vietnamese Blue-Chip Stocks")
    print("="*80 + "\n")
    
    task = dedent(f"""
        Today is {get_current_date()}.
        
        Compare the following Vietnamese blue-chip stocks:
        1. VNM (Vinamilk) - Food & Beverage
        2. HPG (Hoa Phat Steel) - Steel
        3. VIC (Vingroup) - Conglomerate
        
        For each stock:
        - Get last 3 months price performance
        - Get latest annual financial ratios
        - Compare key metrics: P/E, P/B, EPS, Revenue Growth
        
        Provide a summary comparison table and investment insights.
        Use both English and Vietnamese for key findings.
    """)
    
    user_proxy.initiate_chat(analyst, message=task)


# Example 3: Deep dive into financial statements
def financial_deep_dive():
    """Deep dive into a company's financial statements"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Financial Statement Deep Dive - FPT Corporation")
    print("="*80 + "\n")
    
    task = dedent(f"""
        Phân tích chi tiết báo cáo tài chính của FPT Corporation (FPT):
        
        1. Lấy Bảng cân đối kế toán 3 năm gần nhất
        2. Lấy Kết quả hoạt động kinh doanh 3 năm gần nhất
        3. Lấy Lưu chuyển tiền tệ 3 năm gần nhất
        
        Phân tích xu hướng:
        - Tăng trưởng tài sản
        - Cơ cấu nợ và vốn chủ sở hữu
        - Tăng trưởng doanh thu và lợi nhuận
        - Khả năng tạo tiền từ hoạt động kinh doanh
        
        Đưa ra đánh giá tổng quan về sức khỏe tài chính của công ty.
    """)
    
    user_proxy.initiate_chat(analyst, message=task)


# Example 4: Quick price check and basic info
def quick_stock_check():
    """Quick check of stock price and basic information"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Quick Stock Check - Multiple Stocks")
    print("="*80 + "\n")
    
    task = dedent(f"""
        Get current stock information for the following Vietnamese stocks:
        
        - VPB (VP Bank)
        - VNM (Vinamilk)
        - MSN (Masan Group)
        
        For each stock, show:
        1. Latest closing price
        2. Latest trading volume
        3. Basic P/E and P/B ratios from financial ratios
        
        Present the data in a clean table format.
    """)
    
    user_proxy.initiate_chat(analyst, message=task)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("VIETNAMESE STOCK ANALYSIS WITH FINROBOT")
    print("Using VNStock Data + GPT-4o + AutoGen")
    print("="*80)
    
    # Choose which example to run
    print("\nAvailable examples:")
    print("1. Analyze VP Bank (VPB) in detail")
    print("2. Compare multiple blue-chip stocks")
    print("3. Deep dive into FPT financial statements")
    print("4. Quick check of multiple stocks")
    
    # Run Example 1 by default
    # Uncomment the one you want to run:
    
    analyze_vpb()  # Example 1
    # compare_stocks()  # Example 2
    # financial_deep_dive()  # Example 3
    # quick_stock_check()  # Example 4
    
    print("\n" + "="*80)
    print("✅ Analysis Complete!")
    print("="*80)
