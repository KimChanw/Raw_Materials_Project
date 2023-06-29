from datetime import datetime, timedelta

from django.shortcuts import render
from .data_visualization import _visualize_all_data, _visualize_price_data_only_one_column
from .data_preprocess.get_data_for_visualization import get_date_series_dataframe, get_date_series_join_dataframe
from datetime import datetime, timedelta

import matplotlib as mpl

# GUI 에러 방지
mpl.use('Agg')

def index(request):
    # 시작일 입력값이 들어온다면
    start_date = request.GET.get('start_day') or '2023-01-01'
    end_date = request.GET.get('end_day') or '2023-06-25'

    # 해당 일자의 데이터가 있는지 확인
    try:
        oil_price_df = get_date_series_dataframe(start_date, end_date, 'WtiBrentJoinTable')

    # 없다면 ValueError를 발생시켜 예외 처리
    # 프론트 단에서 오류 메시지 출력할 수 있도록 error_message 추가
    except ValueError as e:
        error_message = str(e)
        wti_price_graph = None
        brent_price_graph = None
        normalization_graph = None

        return render(request, 'dashboard/oilprice.html', {
            'start_date': start_date,
            'end_date': end_date,
            'wti_price_graph': wti_price_graph,
            'brent_price_graph': brent_price_graph,
            'normalization_graph': normalization_graph,
            'error_message': error_message,
        })

    
    # 시각화 이미지를 encode한 값을 가져옴
    wti_price_visualization_img = _visualize_price_data_only_one_column(oil_price_df, 'wti')
    brent_price_visualization_img = _visualize_price_data_only_one_column(oil_price_df, 'brent')
    normalization_visualization_img = _visualize_all_data(oil_price_df, ['wti', 'brent'])

    # 이미지 / json 데이터를 전달하여 지표와 시각화 결과를 전송
    context = {
        'wti_price_graph': wti_price_visualization_img,
        'brent_price_graph': brent_price_visualization_img,
        'normalization_graph': normalization_visualization_img,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'dashboard/oilprice.html', context=context)


def gold_silver_prices(request):
    # 시작일 입력값이 들어온다면
    start_date = request.GET.get('start_day') or '2023-01-01'
    end_date = request.GET.get('end_day') or '2023-06-25'

    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')

    # 해당 일자의 데이터가 있는지 확인
    try:
        gold_price_df = get_date_series_dataframe(start_date, end_date, 'gold_prices')
        silver_price_df = get_date_series_dataframe(start_date, end_date, 'silver_prices')
        gold_silver_price_df = get_date_series_join_dataframe(start_date, end_date, 'gold_prices', 'silver_prices')

    # 없다면 ValueError를 발생시켜 예외 처리
    # 프론트 단에서 오류 메시지 출력할 수 있도록 error_message 추가
    except ValueError as e:
        error_message = str(e)
        gold_price_graph = None
        silver_price_graph = None
        normalization_graph = None

        return render(request, 'dashboard/goldprice.html', {
            'start_date': start_date,
            'end_date': end_date,
            'gold_price_graph': gold_price_graph,
            'silver_price_graph': silver_price_graph,
            'normalization_graph': normalization_graph,
            'error_message': error_message,
        })

    # 시각화 이미지를 encode한 값을 가져옴
    gold_price_visualization_img = _visualize_price_data_only_one_column(gold_price_df, 'usd_pm')
    silver_price_visualization_img = _visualize_price_data_only_one_column(silver_price_df, 'usd')
    normalization_visualization_img = _visualize_all_data(gold_silver_price_df, ['gold_prices', 'silver_prices'])


    # 이미지 / json 데이터를 전달하여 지표와 시각화 결과를 전송
    context = {
        'gold_price_graph': gold_price_visualization_img,
        'silver_price_graph': silver_price_visualization_img,
        'normalization_graph': normalization_visualization_img,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'dashboard/goldprice.html', context=context)


