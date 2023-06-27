import pandas as pd
from connect.redshift_session import RedshiftSession

cursor = RedshiftSession.redshift_conn()

def get_time_series_dataframe(start_date, end_date, table_name):
    """데이터 저장소로부터 start_date ~ end_date의 원유 가격 정보를 DataFrame으로 가져오는 함수"""
        
    # 분석 스키마 내 oil_price_summary 테이블에서 시작일과 끝 날짜 사이 일자와 가격 데이터를 가져옴
    price_data_sql = cursor.execute(f"""
                                    SELECT * 
                                    FROM {table_name} 
                                    WHERE time between \'{start_date}\' and \'{end_date}\'
                                    ORDER BY time
                                    """)
    price_data_df = price_data_sql.fetch_dataframe()
    
    # 유효한 데이터가 없으면 ValueError를 발생시켜 템플릿에 전달
    if price_data_df.empty:
        raise ValueError(f"No price data available for the given date range: {start_date} ~ {end_date}")
    
    price_data_df.set_index('time', inplace=True)
    
    return price_data_df