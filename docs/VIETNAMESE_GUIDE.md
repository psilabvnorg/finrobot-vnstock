# Hướng dẫn sử dụng FinRobot cho Thị trường Chứng khoán Việt Nam
# Vietnamese Stock Market Guide for FinRobot

## 🇻🇳 Tổng quan / Overview

FinRobot đã được tích hợp **VNStock** để phân tích chứng khoán Việt Nam. Bạn có thể:
- Phân tích cổ phiếu Việt Nam cùng lúc với cổ phiếu Mỹ
- Sử dụng GPT-4o với khả năng hiểu tiếng Việt tốt hơn
- Truy cập dữ liệu từ HOSE, HNX, UPCOM

FinRobot now integrates **VNStock** for Vietnamese stock analysis. You can:
- Analyze Vietnamese stocks alongside US stocks
- Use GPT-4o with better Vietnamese language understanding
- Access data from HOSE, HNX, UPCOM exchanges

---

## 📦 Cài đặt / Installation

### 1. Install VNStock
```bash
pip install vnstock3
```

### 2. Install FinRobot (if not already installed)
```bash
pip install finrobot
# Or from source:
cd FinRobot
pip install -e .
```

### 3. Configure GPT-4o API Key

Edit `OAI_CONFIG_LIST`:
```json
[
    {
        "model": "gpt-4o",
        "api_key": "your-openai-api-key-here"
    }
]
```

---

## 🚀 Sử dụng nhanh / Quick Start

### Example 1: Lấy dữ liệu giá cổ phiếu / Get Stock Price Data

```python
from finrobot.data_source import VNStockUtils

# Lấy giá VPB (VP Bank) trong 6 tháng qua
data = VNStockUtils.get_stock_data(
    symbol="VPB",
    source="VCI",  # Nguồn dữ liệu: VCI, TCBS, hoặc MSN
    start_date="2024-01-01",
    end_date="2024-12-31"
)
print(data)
```

### Example 2: Lấy báo cáo tài chính / Get Financial Statements

```python
from finrobot.data_source import VNStockUtils

# Bảng cân đối kế toán (Balance Sheet)
balance_sheet = VNStockUtils.get_balance_sheet(
    symbol="VNM",  # Vinamilk
    source="VCI",
    period="year",  # "year" hoặc "quarter"
    lang="vi"  # "vi" cho tiếng Việt, "en" cho tiếng Anh
)

# Kết quả kinh doanh (Income Statement)
income = VNStockUtils.get_income_stmt(
    symbol="VNM",
    source="VCI",
    period="year",
    lang="vi"
)

# Lưu chuyển tiền tệ (Cash Flow)
cash_flow = VNStockUtils.get_cash_flow(
    symbol="VNM",
    source="VCI",
    period="year"
)

# Chỉ số tài chính (Financial Ratios: P/E, P/B, EPS, etc.)
ratios = VNStockUtils.get_financial_ratios(
    symbol="VNM",
    source="VCI",
    period="year",
    lang="vi"
)
```

### Example 3: Sử dụng với AI Agent

```python
import autogen
from finrobot.data_source import VNStockUtils
from finrobot.agents.workflow import FinRobot

# Cấu hình GPT-4o
llm_config = {
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4o"]}
    ),
    "temperature": 0,
}

# Tạo agent phân tích
analyst_config = {
    "name": "Vietnamese_Analyst",
    "profile": "Chuyên gia phân tích chứng khoán Việt Nam",
    "toolkits": [
        VNStockUtils.get_stock_data,
        VNStockUtils.get_financial_ratios,
        VNStockUtils.get_income_stmt,
    ]
}

user_proxy = autogen.UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": "analysis", "use_docker": False}
)

analyst = FinRobot(
    agent_config=analyst_config,
    llm_config=llm_config,
    proxy=user_proxy
)

# Yêu cầu phân tích
user_proxy.initiate_chat(
    analyst,
    message="Phân tích cổ phiếu VPB trong 6 tháng qua và đưa ra nhận định"
)
```

---

## 📊 Dữ liệu có sẵn / Available Data

### ✅ Có sẵn / Available:
- ✅ Giá lịch sử (Historical prices)
- ✅ Bảng cân đối kế toán (Balance sheet)
- ✅ Kết quả kinh doanh (Income statement)
- ✅ Lưu chuyển tiền tệ (Cash flow)
- ✅ Chỉ số tài chính (Financial ratios: P/E, P/B, EPS, ROE, ROA, etc.)
- ✅ Khối lượng giao dịch (Trading volume)

### ❌ Không có sẵn / Not Available:
- ❌ Giá mục tiêu của nhà phân tích (Analyst target prices)
- ❌ Tin tức tự động (Automated news feeds)
- ❌ Báo cáo SEC (SEC-style filings)
- ❌ Khuyến nghị mua/bán tổng hợp (Aggregated buy/sell recommendations)

**Lưu ý**: Các dữ liệu không có sẵn sẽ trả về "N/A" và không làm hệ thống bị lỗi.

---

## 🏢 Mã cổ phiếu phổ biến / Popular Tickers

### Ngân hàng / Banking:
- **VPB** - VP Bank
- **TCB** - Techcombank
- **VCB** - Vietcombank
- **MBB** - MB Bank
- **ACB** - ACB Bank

### Công nghệ / Technology:
- **FPT** - FPT Corporation
- **CMG** - CMC Group

### Bất động sản / Real Estate:
- **VIC** - Vingroup
- **NVL** - Novaland
- **VHM** - Vinhomes

### Thực phẩm / Food & Beverage:
- **VNM** - Vinamilk
- **MSN** - Masan Group
- **SAB** - Sabeco

### Thép / Steel:
- **HPG** - Hoa Phat Steel
- **HSG** - Hoa Sen Group

---

## 🎯 Ví dụ thực tế / Real-world Examples

### Ví dụ 1: So sánh 3 cổ phiếu ngân hàng

```python
from finrobot.data_source import VNStockUtils

banks = ["VPB", "TCB", "VCB"]

for bank in banks:
    ratios = VNStockUtils.get_financial_ratios(
        symbol=bank,
        source="VCI",
        period="year",
        lang="vi"
    )
    
    latest = ratios.iloc[0]  # Năm gần nhất
    print(f"\n{bank}:")
    print(f"  P/E: {latest.get('P/E', 'N/A')}")
    print(f"  P/B: {latest.get('P/B', 'N/A')}")
    print(f"  EPS: {latest.get('EPS (VND)', 'N/A')}")
```

### Ví dụ 2: Phân tích tăng trưởng doanh thu

```python
from finrobot.data_source import VNStockUtils

# Lấy dữ liệu 5 năm
income = VNStockUtils.get_income_stmt(
    symbol="FPT",
    source="VCI",
    period="year",
    lang="vi"
)

# Phân tích tăng trưởng
for i in range(len(income) - 1):
    year_current = income.iloc[i]['Năm']
    year_prev = income.iloc[i + 1]['Năm']
    revenue_current = income.iloc[i]['Doanh thu (đồng)']
    revenue_prev = income.iloc[i + 1]['Doanh thu (đồng)']
    
    growth = ((revenue_current - revenue_prev) / revenue_prev) * 100
    print(f"{year_prev} -> {year_current}: {growth:.2f}% growth")
```

### Ví dụ 3: Chạy full demo

```bash
cd examples
python vietnamese_stock_analysis.py
```

---

## 🌐 Nguồn dữ liệu / Data Sources

VNStock hỗ trợ 3 nguồn dữ liệu:

| Source | Description | Speed |
|--------|-------------|-------|
| **VCI** | VCI Securities | ⚡⚡⚡ Fast |
| **TCBS** | TCBS Securities | ⚡⚡ Medium |
| **MSN** | MSN Finance | ⚡ Slow |

**Khuyến nghị**: Sử dụng `source="VCI"` để tốc độ nhanh nhất.

---

## 🔧 Troubleshooting

### Lỗi: "No data available"
```python
# Kiểm tra ticker có đúng không
# Ví dụ: VPB (đúng) vs VPBANK (sai)

# Kiểm tra ngày có hợp lệ không (ngày giao dịch)
# Tránh weekend và ngày lễ
```

### Lỗi: "Rate limit exceeded"
```python
# VNStock có giới hạn request
# Thêm delay giữa các request:

import time
time.sleep(1)  # Đợi 1 giây giữa các lần gọi
```

### Lỗi: "Model not found"
```bash
# Đảm bảo OAI_CONFIG_LIST có model "gpt-4o"
# Không phải "gpt-4" hay "gpt-4-turbo"
```

---

## 💡 Tips & Best Practices

### 1. Sử dụng ngôn ngữ phù hợp
```python
# Dữ liệu bằng tiếng Việt cho GPT-4o hiểu tốt hơn
data = VNStockUtils.get_balance_sheet(symbol="VPB", lang="vi")

# Hoặc tiếng Anh nếu muốn prompt bằng tiếng Anh
data = VNStockUtils.get_balance_sheet(symbol="VPB", lang="en")
```

### 2. Kết hợp nhiều nguồn dữ liệu
```python
# Dùng VNStock cho thị trường Việt Nam
vn_data = VNStockUtils.get_stock_data("VPB", source="VCI", ...)

# Dùng YFinance cho thị trường Mỹ (giữ nguyên)
from finrobot.data_source import YFinanceUtils
us_data = YFinanceUtils.get_stock_data("AAPL", ...)
```

### 3. Cache dữ liệu để tránh rate limit
```python
# Lưu dữ liệu vào file
data = VNStockUtils.get_stock_data(
    "VPB", "VCI", "2024-01-01", "2024-12-31",
    save_path="vpb_data.csv"  # Tự động lưu
)

# Đọc lại từ file thay vì gọi API lại
import pandas as pd
data = pd.read_csv("vpb_data.csv")
```

---

## 📚 Tài liệu thêm / Additional Resources

- **VNStock Documentation**: https://github.com/thinh-vu/vnstock
- **FinRobot Main Docs**: [README.md](../README.md)
- **AutoGen Docs**: https://microsoft.github.io/autogen/
- **Vietnamese Stock Exchanges**:
  - HOSE: https://www.hsx.vn/
  - HNX: https://www.hnx.vn/
  - UPCOM: https://www.hnx.vn/vi-vn/cophieu.html

---

## 🤝 Đóng góp / Contributing

Nếu bạn muốn cải thiện tích hợp VNStock:
1. Fork repository
2. Tạo branch mới: `git checkout -b feature/vnstock-enhancement`
3. Commit changes: `git commit -m 'Add new VNStock feature'`
4. Push: `git push origin feature/vnstock-enhancement`
5. Tạo Pull Request

---

## 📞 Hỗ trợ / Support

- **Issues**: https://github.com/AI4Finance-Foundation/FinRobot/issues
- **Discord**: https://discord.gg/trsr8SXpW5
- **VNStock Issues**: https://github.com/thinh-vu/vnstock/issues

---

## ⚖️ License

FinRobot và VNStock integration tuân theo MIT License.

---

**Chúc bạn phân tích hiệu quả! / Happy analyzing!** 🚀📈
