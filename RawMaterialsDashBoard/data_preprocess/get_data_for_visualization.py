import pandas as pd
from connect.redshift_session import RedshiftSession

cursor = RedshiftSession.redshift_connection()

def get_date_series_dataframe(start_date, end_date, table_name):
    """데이터 저장소로부터 start_date ~ end_date의 원유 가격 정보를 DataFrame으로 가져오는 함수"""
    
    # 시작일과 끝 날짜 사이 일자와 가격 데이터를 가져옴
    price_data_sql = cursor.execute(f"""
                                    SELECT *
                                    FROM {table_name} 
                                    WHERE date between \'{start_date}\' and \'{end_date}\'
                                    ORDER BY date
                                    """)
    price_data_df = price_data_sql.fetch_dataframe()
    
    # 유효한 데이터가 없으면 ValueError를 발생시켜 템플릿에 전달
    if price_data_df.empty:
        raise ValueError(f"No price data available for the given date range: {start_date} ~ {end_date}")
    
    price_data_df.set_index('date', inplace=True)
    
    return price_data_df


def get_date_series_join_dataframe(start_date, end_date, table_name1, table_name2):
    """
    데이터 저장소로부터 start_date ~ end_date의 금.은 가격 정보를 DataFrame으로 가져오는 함수
    금과 은의 데이터 row 개수가 많고, 두 데이터 간 column 개수가 다르므로 별도로 join 함수를 제작
    금 / 은 간 가격 차이가 많이 발생하므로 0-1 사이로 정규화 수행
    """
    

    # 테이블에서 시작일과 끝 날짜 사이 일자와 가격 데이터를 join하여 가져옴
    # 이 때, 금과 은 두 가격은 0-1 사이로 정규화 수행함
    cursor.execute(f"""
                    WITH min_max AS (
                        SELECT MIN(usd_pm) AS min_gold,
                            MAX(usd_pm) AS max_gold,
                            MIN(usd) AS min_silver,
                            MAX(usd) AS max_silver
                        FROM {table_name1}, {table_name2}
                    )
                    SELECT A.DATE,
                        (usd_pm - m.min_gold) / (m.max_gold - m.min_gold) AS gold_prices,
                        (usd - m.min_silver) / (m.max_silver - m.min_silver) AS silver_prices
                    FROM {table_name1} AS A
                    INNER JOIN {table_name2} AS B ON B.DATE = A.DATE AND A.date BETWEEN '{start_date}' AND '{end_date}'
                    CROSS JOIN min_max AS m
                    ORDER BY A.DATE
                    """)

    columns = [desc[0] for desc in cursor.description]
    price_data_df = pd.DataFrame(cursor.fetchall(), columns=columns)

    # 유효한 데이터가 없으면 ValueError를 발생시켜 템플릿에 전달
    if price_data_df.empty:
        raise ValueError(f"No price data available for the given date range: {start_date} ~ {end_date}")

    price_data_df.set_index('date', inplace=True)

    return price_data_df