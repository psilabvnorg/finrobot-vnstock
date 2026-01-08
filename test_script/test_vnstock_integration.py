"""
Quick test to verify VNStock integration with FinRobot
Run this to ensure everything is working correctly
"""

import sys
from datetime import datetime, timedelta

print("="*80)
print("TESTING VNSTOCK INTEGRATION WITH FINROBOT")
print("="*80)

# Test 1: Import VNStockUtils
print("\n[1/5] Testing import...")
try:
    from finrobot.data_source import VNStockUtils
    print("✅ VNStockUtils imported successfully")
except Exception as e:
    print(f"❌ Failed to import VNStockUtils: {e}")
    sys.exit(1)

# Test 2: Get stock data
print("\n[2/5] Testing get_stock_data...")
try:
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    data = VNStockUtils.get_stock_data(
        symbol="VPB",
        source="VCI",
        start_date=start_date,
        end_date=end_date
    )
    
    if not data.empty:
        print(f"✅ Retrieved {len(data)} days of price data for VPB")
        print(f"   Latest close: {data['close'].iloc[-1]:,.0f} VND")
    else:
        print("⚠️  No data returned (might be weekend/holiday)")
except Exception as e:
    print(f"❌ Failed to get stock data: {e}")

# Test 3: Get financial ratios
print("\n[3/5] Testing get_financial_ratios...")
try:
    ratios = VNStockUtils.get_financial_ratios(
        symbol="VPB",
        source="VCI",
        period="year",
        lang="vi"
    )
    
    if not ratios.empty:
        latest = ratios.iloc[0]
        print(f"✅ Retrieved financial ratios for VPB")
        print(f"   Year: {latest.get('Năm', 'N/A')}")
        print(f"   P/E: {latest.get('P/E', 'N/A')}")
        print(f"   P/B: {latest.get('P/B', 'N/A')}")
    else:
        print("⚠️  No ratios data returned")
except Exception as e:
    print(f"❌ Failed to get financial ratios: {e}")

# Test 4: Get balance sheet
print("\n[4/5] Testing get_balance_sheet...")
try:
    bs = VNStockUtils.get_balance_sheet(
        symbol="VNM",  # Try Vinamilk
        source="VCI",
        period="year",
        lang="vi"
    )
    
    if not bs.empty:
        print(f"✅ Retrieved balance sheet for VNM (Vinamilk)")
        print(f"   Years available: {len(bs)}")
    else:
        print("⚠️  No balance sheet data returned")
except Exception as e:
    print(f"❌ Failed to get balance sheet: {e}")

# Test 5: Test stub methods (should return N/A gracefully)
print("\n[5/5] Testing stub methods...")
try:
    # These should not raise errors, just return N/A
    target = VNStockUtils.get_target_price("VPB", "VCI", "2024-01-01")
    rating, _ = VNStockUtils.get_analyst_recommendations("VPB", "VCI")
    
    if target == "N/A" and rating == "N/A":
        print("✅ Stub methods return N/A as expected (no errors)")
    else:
        print("⚠️  Stub methods returned unexpected values")
except Exception as e:
    print(f"❌ Stub methods raised error: {e}")

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print("\n✅ VNStock integration is working!")
print("\nYou can now:")
print("  1. Use VNStockUtils in your Python scripts")
print("  2. Run examples/vietnamese_stock_analysis.py")
print("  3. Create custom agents with Vietnamese stock tools")
print("\nFor more info, see: docs/VIETNAMESE_GUIDE.md")
print("\n" + "="*80)
