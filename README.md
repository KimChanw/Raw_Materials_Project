# 원자재 가격 시각화 대시보드 구축 프로젝트
> ### 5조 1팀 프로그래머스 데이터 엔지니어링 데브코스 3차 팀 프로젝트 

<BR>

## 프로젝트 소개
> ### 원자재 (금/은, 브렌트유 및 WTI유)별 가격 정보를 API에서 추출하여 Redshift로 적재하는 ETL 프로세스 제작
> ### Django를 이용하여 데이터 시각화 서비스 제작

<BR>

## 프로젝트 아키텍쳐
![image](https://github.com/KimChanw/OilPricesDashboard/assets/50550972/6760f3d1-69f2-4269-b53d-51132cbb620a)

<BR>

## 제공 서비스
### 설정 기간 기준 일 별 금/은 및 WTI / Brent유 가격 추세 그래프

<BR>

## 참여 조원
- #### 공동 작업 : Airflow DAG 코드 및 데이터 웨어하우스 적재
김찬우 : Django 서버 구축 및 데이터 시각화, Airflow 및 지표 모니터링 기능 배포 서버 구축
이태현 : API를 통한 데이터 수집
김동석 : API를 통한 데이터 수집
국승원 : 데이터 시각화
임찬우 : Django 서버 구축 및 데이터 시각화

<BR>

## 개발 과정
1. 데이터 소스로부터 데이터를 추출하여 Redshift에 적재하는 ETL DAG 개발
2. DAG는 하루에 한 번 씩 실행 
3. Airflow의 상태 모니터링
    - Airflow와 모니터링 서버는 AWS를 이용하여 배포
4. Django를 통해 사용자의 요청이 입력되면 Redshift에서 쿼리를 통해 데이터를 추출 후, 해당 기간에 맞는 그래프로 시각화


<BR>

## 활용 기술 및 프레임워크
#### 1. front-end : `html/css`
    - visualization : matplotlib, seaborn

#### 2. back-end : `Python, Django`
    - Data Preprocessing : pandas

#### 3. Data Warehouse
    - 데이터 적재 : Redshift

#### 4. DATA ETL & Metrics Monitering
    - ETL 파이프라인 : Airflow
    - 지표 수집 및 모니터링 : statsd, prometheus
    - 지표 모니터링 시각화 : grafana

#### 5. 원격 배포 환경
    - 데이터 파이프라인 실행 환경 및 지표 모니터링 배포
    - AWS EC2
    - Docker

## 예시 화면
![image](https://github.com/KimChanw/OilPricesDashboard/assets/50550972/4c04e667-80c2-42c4-a6da-2e5bef3be66a)

![image](https://github.com/KimChanw/OilPricesDashboard/assets/50550972/17de336a-86fe-45e2-8dd6-2ace188b66d9)

![image](https://github.com/KimChanw/OilPricesDashboard/assets/50550972/0c0d0d4d-e322-4969-bfbe-9757159c2a10) ![image](https://github.com/KimChanw/OilPricesDashboard/assets/50550972/34a88571-90f3-4d5a-8c25-5fa526d680cc)
