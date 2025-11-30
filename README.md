This is a derivatives from pykrx.

Add some methods on top of pykrx.

examples)

# 5년 국채선물 추종 지수
df1 = stock.get_bond_futures_5y_tracking_index("20251017", "20251118")
# 10년 국채선물지수
df2 = stock.get_bond_futures_10y_index("20251017", "20251118")
# 코스피
df3 = stock.get_kospi_index_by_date("20251017", "20251118", share="2", money="3")
# 코스닥
df4 = stock.get_kosdaq_index_by_date("20251017", "20251118", share="2", money="3")
# 코스피 200 변동성지수 
df = stock.get_derivative_index_ohlcv_by_date("20251017", "20251119", "1", "300") # 변동성 
# 코스피200 옵션 거래량 call/put
df5 = stock.get_option_volume("20251101", "20251114", "KR___OPK2I", opt_type="C") # > 사용할때는 5일 평균거래량
df6 = stock.get_option_volume("20251101", "20251114", "KR___OPK2I", opt_type="P") # > 사용할때는 5일 평균거래량
