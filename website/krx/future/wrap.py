from pykrx.website.comm import dataframe_empty_handler
from pykrx.website.krx.future.core import (
    파생상품검색, 전종목시세, 옵션거래량추이, 기타파생지수_개별시세
)
import numpy as np
import pandas as pd
from pandas import DataFrame


def get_future_ticker_and_name() -> DataFrame:
    return 파생상품검색().fetch()


def get_future_ticker_list() -> DataFrame:
    return 파생상품검색().fetch().index.to_list()


@dataframe_empty_handler
def get_future_ohlcv_by_ticker(date: str, prod: str) -> DataFrame:
    """티커별로 정리된 특정 일자의 OHLCV

    Args:
        date (str): 조회 일자 (YYYYMMDD)
        prod (str): 조회 상품

    Returns:
    >> get_future_ohlcv_by_ticker("20220902", "KRDRVFUK2I")

                                        종목명     종가  대비    시가    고가    저가  현물가  거래량        거래대금
        종목코드
        101S9000      코스피200 F 202209 (주간)  313.85 -0.65  315.70  315.85  311.15  313.85  307202  24105144800000
        101SC000      코스피200 F 202212 (주간)  314.75 -0.75  316.60  316.75  312.15  314.75   14474   1139311725000
        101T3000      코스피200 F 202303 (주간)  311.25 -1.45  312.70  313.50  310.75  311.25     274     21450150000
        101T6000      코스피200 F 202306 (주간)  311.40 -3.55  313.60  313.60  311.40  311.40       4       313050000
        101TC000      코스피200 F 202312 (주간)  316.65 -2.35  316.65  316.65  316.65  316.65       1        79162500
        101V6000      코스피200 F 202406 (주간)  320.55 -1.45  320.55  320.55  320.55  320.55       3       240412500
        101VC000      코스피200 F 202412 (주간)    0.00  0.00    0.00    0.00    0.00  318.45       0               0
        401S9SCS  코스피200 SP 2209-2212 (주간)    0.90  0.90    1.00    1.00    0.90    0.00   17618   2767660050000
        401S9T3S  코스피200 SP 2209-2303 (주간)    0.00  0.00    0.00    0.00    0.00    0.00       0               0
        401S9T6S  코스피200 SP 2209-2306 (주간)    0.00  0.00    0.00    0.00    0.00    0.00       0               0
        401S9TCS  코스피200 SP 2209-2312 (주간)    0.00  0.00    0.00    0.00    0.00    0.00       0               0
        401S9V6S  코스피200 SP 2209-2406 (주간)    0.00  0.00    0.00    0.00    0.00    0.00       0               0
        401S9VCS  코스피200 SP 2209-2412 (주간)    0.00  0.00    0.00    0.00    0.00    0.00       0               0
        """  # pylint: disable=line-too-long # noqa: E501
    df = 전종목시세().fetch(date, prod)
    df = df[['ISU_SRT_CD', 'ISU_NM', 'TDD_CLSPRC', 'CMPPREVDD_PRC',
             'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 'SETL_PRC', 'ACC_TRDVOL',
             'ACC_TRDVAL']]
    df.columns = ['종목코드', '종목명', '종가', '대비', '시가', '고가', '저가',
                  '현물가', '거래량', '거래대금']
    df = df.set_index('종목코드')

    df = df.replace(r'\-$', '0', regex=True)
    df = df.replace('', '0', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype({
        "종가": np.float64,
        "대비": np.float64,
        "시가": np.float64,
        "고가": np.float64,
        "저가": np.float64,
        "현물가": np.float64,
        "거래량": np.int32,
        "거래대금": np.int64
    })
    return df


@dataframe_empty_handler
def get_option_volume(
    fromdate: str,
    todate: str,
    isu_cd: str,
    opt_type: str = "C",
    inq_type: str = "2",
    prt_check: str = "SU",
) -> DataFrame:
    """옵션 거래량 추이

    Args:
        fromdate  (str): 조회 시작 일자 (YYYYMMDD)
        todate    (str): 조회 종료 일자 (YYYYMMDD)
        isu_cd    (str): 상품 코드 (예: 'KR___OPK2I' - KOSPI200 옵션)
        opt_type  (str): 옵션 구분 ('C' 콜, 'P' 풋)
        inq_type  (str): 조회 유형 코드 (기본값 '2')
        prt_check (str): 집계 옵션 (예: 'SU' 요약)

    Returns:
        DataFrame: KRX 원본 열 구조 그대로 반환
    """
    df = 옵션거래량추이().fetch(
        strtDd=fromdate,
        endDd=todate,
        isuCd=isu_cd,
        isuOpt=opt_type,
        inqTpCd=inq_type,
        prtType="QTY",
        prtCheck=prt_check,
    )
    rename_map = {
    "TRD_DD": "Date",
    "A07": "기관합",  # 예시
    "A08": "기타법인",  
    "A09": "개인",  # 예시
    "A12": "외인합",
    "AMT_OR_QTY": "전체"
    # 필요 컬럼 추가
    }
    df = df.rename(columns=rename_map)
    return df

@dataframe_empty_handler
def get_derivative_index_ohlcv_by_date(
    fromdate: str,
    todate: str,
    ind_tp_cd: str,
    idx_ind_cd: str,
) -> DataFrame:
    """기타 파생지수(예: 변동성지수) OHLCV - 기간별

    Args:
        fromdate  (str): 조회 시작 일자 (YYYYMMDD)
        todate    (str): 조회 종료 일자 (YYYYMMDD)
        ind_tp_cd (str): 지수 그룹 코드 (예: '1')
        idx_ind_cd(str): 지수 코드 (예: '300')

    Returns:
        DataFrame: 날짜 인덱스, 시가/고가/저가/종가/거래량/거래대금/상장시가총액
    """
    df = 기타파생지수_개별시세().fetch(
        strtDd=fromdate,
        endDd=todate,
        indTpCd=ind_tp_cd,
        idxIndCd=idx_ind_cd,
    )
    # get_option_volume 패턴과 동일: 원본 열 구조 유지, 최소한의 컬럼 rename만 적용
    rename_map = {
        'TRD_DD': 'Date',
        # 필요시 추가 컬럼에 대한 변환을 여기에 정의 (예: 'CLSPRC_IDX': 'Close' 등)
    }
    df = df.rename(columns=rename_map)
    return df


@dataframe_empty_handler
def get_bond_futures_5y_tracking_index(fromdate: str, todate: str) -> DataFrame:
    """5년 국채선물 추종지수 (MDCSTAT01201) 기간 시세 - 원본 구조 유지

    Args:
        fromdate (str): YYYYMMDD
        todate   (str): YYYYMMDD
    """
    df = 기타파생지수_개별시세().fetch(
        strtDd=fromdate,
        endDd=todate,
        indTpCd="D",
        idxIndCd="896",
        idxCd="D",
        idxCd2="896",
    )
    return df.rename(columns={"TRD_DD": "Date"})


@dataframe_empty_handler
def get_bond_futures_10y_index(fromdate: str, todate: str) -> DataFrame:
    """10년 국채선물지수 (MDCSTAT01201) 기간 시세 - 원본 구조 유지

    Args:
        fromdate (str): YYYYMMDD
        todate   (str): YYYYMMDD
    """
    df = 기타파생지수_개별시세().fetch(
        strtDd=fromdate,
        endDd=todate,
        indTpCd="1",
        idxIndCd="309",
        idxCd="1",
        idxCd2="309",
    )
    return df.rename(columns={"TRD_DD": "Date"})

if __name__ == "__main__":
    tickers = get_future_ticker_list()
    for t in tickers[:1]:
        df = get_future_ohlcv_by_ticker("20220902", t)
        print(df)
