from pykrx.website.krx.krxio import KrxFutureIo, KrxWebIo
import pandas as pd
from pandas import DataFrame


class 파생상품검색(KrxWebIo):
    @property
    def bld(self):
        return "dbms/comm/component/drv_prod_clss"

    def fetch(self) -> DataFrame:
        """
            > 파생상품검색().fetch()

                                           name
            value
            KRDRVFUK2I        KOSPI 200 Futures
            KRDRVFUMKI   MINI KOSPI 200 Futures
            KRDRVOPK2I         KOSPI 200 Option
            KRDRVOPWKI  KOSPI 200 Weekly Option
            KRDRVOPMKI    MINI KOSPI 200 Option
            KRDRVFUKQI        KOSDAQ150 Futures
            KRDRVOPKQI         KOSDAQ150 Option
            KRDRVFUXI3           KRX300 Futures
            KRDRVFUVKI          V-KOSPI Futures
            KRDRVFUXAT     Secotr Index Futures
            KRDRVFUBM3             KTB3 Futures
            KRDRVFUBM5             KTB5 Futures
            KRDRVFUBMA            KTB10 Futures
            KRDRVFUB3A    3y-10y KTB sp Futures
            KRDRVFURFR          3M KOFR Futures
            KRDRVFUUSD              USD Futures
            KRDRVFXUSD   US Dollar Flex Futures
            KRDRVFUJPY              JPY Futures
            KRDRVFUEUR              EUR Futures
            KRDRVFUCNH              CNH Futures
            KRDRVFUKGD             GOLD Futures
            KRDRVFUEQU     Single Stock Futures
            KRDRVOPEQU     Single Stock Options
            KRDRVFUEST     EURO STOXX50 Futures
        """
        data = self.read(secugrpId="ALL")
        df = DataFrame(data['output'])
        return df.set_index('value')


class 전종목기본정보(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT12801"

    def fetch(self, prodId: str) -> DataFrame:
        """[15004] 전종목 기본정보

        Args:
            prodId   (str): 선물 티커

        Returns:
            DataFrame:
                          ISU_CD ISU_SRT_CD                  ISU_NM     ISU_ABBRV              ISU_ENG_NM     LIST_DD   LSTTRD_DD LST_SETL_DD   ULY_TP_NM  SETLMULT RGHT_TP_NM EXER_PRC
                0   KR4101S90005   101S9000      코스피200 F 202209      F 202209      KOSPI 200 F 202209  2021/09/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
                1   KR4101SC0009   101SC000      코스피200 F 202212      F 202212      KOSPI 200 F 202212  2019/12/13  2022/12/08  2022/12/09  지수(Index)  250,000          -      .00
                2   KR4101T30009   101T3000      코스피200 F 202303      F 202303      KOSPI 200 F 202303  2022/03/11  2023/03/09  2023/03/10  지수(Index)  250,000          -      .00
                3   KR4101T60006   101T6000      코스피200 F 202306      F 202306      KOSPI 200 F 202306  2021/06/11  2023/06/08  2023/06/09  지수(Index)  250,000          -      .00
                4   KR4101TC0008   101TC000      코스피200 F 202312      F 202312      KOSPI 200 F 202312  2020/12/11  2023/12/14  2023/12/15  지수(Index)  250,000          -      .00
                5   KR4101V60002   101V6000      코스피200 F 202406      F 202406      KOSPI 200 F 202406  2022/06/10  2024/06/13  2024/06/14  지수(Index)  250,000          -      .00
                6   KR4101VC0004   101VC000      코스피200 F 202412      F 202412      KOSPI 200 F 202412  2021/12/10  2024/12/12  2024/12/13  지수(Index)  250,000          -      .00
                7   KR4401S9SCS8   401S9SCS  코스피200 SP 2209-2212  SP 2209-2212  KOSPI 200 SP 2209-2212  2022/06/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
                8   KR4401S9T3S1   401S9T3S  코스피200 SP 2209-2303  SP 2209-2303  KOSPI 200 SP 2209-2303  2022/06/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
                9   KR4401S9T6S4   401S9T6S  코스피200 SP 2209-2306  SP 2209-2306  KOSPI 200 SP 2209-2306  2022/06/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
                10  KR4401S9TCS6   401S9TCS  코스피200 SP 2209-2312  SP 2209-2312  KOSPI 200 SP 2209-2312  2022/06/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
                11  KR4401S9V6S0   401S9V6S  코스피200 SP 2209-2406  SP 2209-2406  KOSPI 200 SP 2209-2406  2022/06/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
                12  KR4401S9VCS2   401S9VCS  코스피200 SP 2209-2412  SP 2209-2412  KOSPI 200 SP 2209-2412  2022/06/10  2022/09/08  2022/09/13  지수(Index)  250,000          -      .00
        """  # pylint: disable=line-too-long # noqa: E501
        if (prodId == "KRDRVFUEQU") or (prodId == "KRDRVOPEQU") or (prodId == "KRDRVFUXAT"):
            # Single Stock Futures
            # Single Stock Options
            # Secotr Index Futures
            subProdId = str(prodId)           
        
            result = self.read(
                prodId=prodId, 
                subProdId=subProdId,
                csvslx_isNo=False)
        else:
            result = self.read(prodId=prodId, csvslx_isNo=False)
        return DataFrame(result["output"])


class 전종목시세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT12501"

    def fetch(self, trdDd: str, prodId: str) -> DataFrame:
        """[15001] 전종목 시세

        Args:
            trdDd    (str): 조회 일자 (YYMMDD)
            prodId   (str): 선물 티커

        Returns:
            DataFrame:

                >> 전종목시세().fetch("20220902", "KRDRVFUK2I")
                              ISU_CD ISU_SRT_CD                         ISU_NM TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC TDD_OPNPRC TDD_HGPRC TDD_LWPRC SPOT_PRC SETL_PRC ACC_TRDVOL          ACC_TRDVAL ACC_OPNINT_QTY SECUGRP_ID
                    0   KR4101S90005   101S9000      코스피200 F 202209 (주간)     313.85          2         -0.65     315.70    315.85    311.15   312.92   313.85    307,202  24,105,144,800,000        333,028         FU
                    1   KR4101SC0009   101SC000      코스피200 F 202212 (주간)     314.75          2         -0.75     316.60    316.75    312.15   312.92   314.75     14,474   1,139,311,725,000         54,796         FU
                    2   KR4101T30009   101T3000      코스피200 F 202303 (주간)     311.25          2         -1.45     312.70    313.50    310.75   312.92   311.25        274      21,450,150,000          3,948         FU
                    3   KR4101T60006   101T6000      코스피200 F 202306 (주간)     311.40          2         -3.55     313.60    313.60    311.40   312.92   311.40          4         313,050,000         10,554         FU
                    4   KR4101TC0008   101TC000      코스피200 F 202312 (주간)     316.65          2         -2.35     316.65    316.65    316.65   312.92   316.65          1          79,162,500         10,156         FU
                    5   KR4101V60002   101V6000      코스피200 F 202406 (주간)     320.55          2         -1.45     320.55    320.55    320.55   312.92   320.55          3         240,412,500            304         FU
                    6   KR4101VC0004   101VC000      코스피200 F 202412 (주간)          -          0             -          -         -         -   312.92   318.45          0                   0          3,355         FU
                    7   KR4401S9SCS8   401S9SCS  코스피200 SP 2209-2212 (주간)       0.90          1          0.90       1.00      1.00      0.90   312.92     0.00     17,618   2,767,660,050,000              -         FU
                    8   KR4401S9T3S1   401S9T3S  코스피200 SP 2209-2303 (주간)          -          0             -          -         -         -   312.92     0.00          0                   0              -         FU
                    9   KR4401S9T6S4   401S9T6S  코스피200 SP 2209-2306 (주간)          -          0             -          -         -         -   312.92     0.00          0                   0              -         FU
                    10  KR4401S9TCS6   401S9TCS  코스피200 SP 2209-2312 (주간)          -          0             -          -         -         -   312.92     0.00          0                   0              -         FU
                    11  KR4401S9V6S0   401S9V6S  코스피200 SP 2209-2406 (주간)          -          0             -          -         -         -   312.92     0.00          0                   0              -         FU
                    12  KR4401S9VCS2   401S9VCS  코스피200 SP 2209-2412 (주간)          -          0             -          -         -         -   312.92     0.00          0                   0              -         FU
        """  # pylint: disable=line-too-long # noqa: E501
        result = self.read(trdDd=trdDd, prodId=prodId, mktTpCd="T", rghtTpCd="T")
        return DataFrame(result['output'])


class 기타파생지수_개별시세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT01201"

    def fetch(
        self,
        strtDd: str,
        endDd: str,
        indTpCd: str,
        idxIndCd: str,
        idxCd: str = None,
        idxCd2: str = None,
    ) -> DataFrame:
        """[01201] 기타 파생지수 개별 시세 추이 (예: 코스피 200 변동성지수)

        Args:
            strtDd   (str): 조회 시작 일자 (YYYYMMDD)
            endDd    (str): 조회 종료 일자 (YYYYMMDD)
            indTpCd  (str): 지수 그룹 코드 (예: '1')
            idxIndCd (str): 지수 코드 (예: '300')
            idxCd    (str): (선택) indTpCd와 동일 값 전달 (서버 파라미터 호환용)
            idxCd2   (str): (선택) idxIndCd와 동일 값 전달 (서버 파라미터 호환용)

        Returns:
            DataFrame: KRX 응답의 표준 출력 블록을 DataFrame으로 반환

        예시 페이로드:
            bld=dbms/MDC/STAT/standard/MDCSTAT01201&locale=ko_KR&indTpCd=1&idxIndCd=300&idxCd=1&idxCd2=300&strtDd=20251017&endDd=20251119&csvxls_isNo=false
        """
        # 서버가 idxCd/idxCd2 alias를 요구하는 경우가 있어 기본 매핑 지원
        if idxCd is None:
            idxCd = indTpCd
        if idxCd2 is None:
            idxCd2 = idxIndCd

        result = self.read(
            indTpCd=indTpCd,
            idxIndCd=idxIndCd,
            idxCd=idxCd,
            idxCd2=idxCd2,
            strtDd=strtDd,
            endDd=endDd,
        )
        data = result.get("output") or result.get("OutBlock_1") or result.get("block1") or []
        return DataFrame(data)


class 옵션거래량추이(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT13102"

    def fetch(
        self,
        strtDd: str,
        endDd: str,
        isuCd: str,
        isuOpt: str,
        inqTpCd: str = "2",
        prtType: str = "QTY",
        prtCheck: str = "SU",
        aggBasTpCd: str = "",
        share: str = "1",
        prodId: str = "",
    ) -> DataFrame:
        """[13102] 옵션 거래량 추이

        Args:
            strtDd    (str): 조회 시작 일자 (YYYYMMDD)
            endDd     (str): 조회 종료 일자 (YYYYMMDD)
            isuCd     (str): 기초자산/상품 코드 (예: KR___OPK2I - KOSPI200 옵션)
            isuOpt    (str): 옵션 구분 (C: 콜, P: 풋)
            inqTpCd   (str): 조회 유형 코드 (기본값 '2')
            prtType   (str): 출력 유형 ('QTY' 거래량, 'VAL' 거래대금)
            prtCheck  (str): 집계 옵션 (예: 'SU' 요약)
            aggBasTpCd(str): 집계 기준 코드 (옵션)
            share     (str): 호가 단위(기본값 '1')
            prodId    (str): 파생상품 ID (옵션)

        Returns:
            DataFrame: KRX 응답의 'output' 블록을 반환

        예시 페이로드:
            bld=dbms/MDC/STAT/standard/MDCSTAT13102&locale=ko_KR&prodId=&strtDd=20251107&endDd=20251114&inqTpCd=2&prtType=QTY&prtCheck=SU&isuCd=KR___OPK2I&isuOpt=C&aggBasTpCd=&strtDdBox1=20251107&endDdBox1=20251114&share=1&csvxls_isNo=false
        """
        result = self.read(
            prodId=prodId,
            strtDd=strtDd,
            endDd=endDd,
            inqTpCd=inqTpCd,
            prtType=prtType,
            prtCheck=prtCheck,
            isuCd=isuCd,
            isuOpt=isuOpt,
            aggBasTpCd=aggBasTpCd,
            share=share,
        )
        return DataFrame(result["output"])


if __name__ == "__main__":
    pd.set_option("display.width", None)
    print(전종목기본정보().fetch(prodId="KRDRVFUEQU"))
