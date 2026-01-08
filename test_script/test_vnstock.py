from vnstock import Vnstock
stock = Vnstock().stock(symbol='VPB', source='VCI')
s = stock.quote.history(start='2020-01-01', end='2024-05-25')
print(s)

from vnstock import Vnstock
stock = Vnstock().stock(symbol='VPB', source='VCI')
# Bảng cân đối kế toán - năm
s1 = stock.finance.balance_sheet(period='year', lang='vi', dropna=True)
# Bảng cân đối kế toán - quý
s2 = stock.finance.balance_sheet(period='quarter', lang='en', dropna=True)
# Kết quả hoạt động kinh doanh
s3 = stock.finance.income_statement(period='year', lang='vi', dropna=True)
# Lưu chuyển tiền tệ
s4 = stock.finance.cash_flow(period='year', dropna=True)
# Chỉ số tài chính
s5 = stock.finance.ratio(period='year', lang='vi', dropna=True)

print(s1)
print(s2)
print(s3)
print(s4)
print(s5)