import pandas as pd
from connect.redshift_session import RedshiftSession

cursor = RedshiftSession.redshift_conn()

def get_date_series_dataframe(start_date, end_date, table_name):
    """데이터 저장소로부터 start_date ~ end_date의 원유 가격 정보를 DataFrame으로 가져오는 함수"""
        
    # 분석 스키마 내 oil_price_summary 테이블에서 시작일과 끝 날짜 사이 일자와 가격 데이터를 가져옴
    price_data_sql = cursor.execute(f"""
                                    SELECT * 
                                    FROM {table_name} 
                                    WHERE time between \'{start_date}\' and \'{end_date}\'
                                    ORDER BY date
                                    """)
    price_data_df = price_data_sql.fetch_dataframe()
    
    # 유효한 데이터가 없으면 ValueError를 발생시켜 템플릿에 전달
    if price_data_df.empty:
        raise ValueError(f"No price data available for the given date range: {start_date} ~ {end_date}")
    
    price_data_df.set_index('date', inplace=True)
    
    return price_data_df


def get_date_series_join_dataframe(start_date, end_date, table_name1, table_nmae2):
    """데이터 저장소로부터 start_date ~ end_date의 원유 가격 정보를 DataFrame으로 가져오는 함수"""

    # 분석 스키마 내 oil_price_summary 테이블에서 시작일과 끝 날짜 사이 일자와 가격 데이터를 가져옴
    cursor.execute(f"""
                                    SELECT  A.date as DATE,
                                            A.usd_pm as gold_prices,
                                            B.usd as silver_prices
                                    FROM {table_name1} AS A INNER JOIN {table_nmae2} AS B 
                                            ON B.DATE = A.DATE 
                                    WHERE A.date between \'{start_date}\' and \'{end_date}\'
                                    ORDER BY A.date
                                    """)

    columns = [desc[0] for desc in cursor.description]
    price_data_df = pd.DataFrame(cursor.fetchall(), columns=columns)

    # 유효한 데이터가 없으면 ValueError를 발생시켜 템플릿에 전달
    if price_data_df.empty:
        raise ValueError(f"No price data available for the given date range: {start_date} ~ {end_date}")

    price_data_df.set_index('date', inplace=True)

    return price_data_df