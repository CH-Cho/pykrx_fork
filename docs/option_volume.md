# KRX 옵션 거래량 조회 추가

- 기능: KRX 웹 API의 옵션 거래량 추이(MDCSTAT13102) 연동
- 목적: 기간/옵션구분별 거래량(QTY) 데이터를 DataFrame으로 반환

## 추가/변경 파일
- `website/krx/future/core.py`
  - 추가: `옵션거래량추이(KrxWebIo)`
  - `bld = "dbms/MDC/STAT/standard/MDCSTAT13102"`
  - `fetch(strtDd, endDd, isuCd, isuOpt, inqTpCd='2', prtType='QTY', prtCheck='SU', aggBasTpCd='', share='1', prodId='') -> DataFrame`
  - 설명: KRX 응답의 `output` 블록을 그대로 DataFrame으로 반환

- `website/krx/future/wrap.py`
  - 추가: `get_option_volume(fromdate, todate, isu_cd, opt_type='C', inq_type='2', prt_check='SU')`
  - 설명: 입력값 정리 후 `옵션거래량추이().fetch(..., prtType='QTY')` 호출. 원본 열 구조 유지

- `stock/future_api.py`
  - 추가: 동일 시그니처의 퍼블릭 API `get_option_volume(...)`
  - 설명: `datetime` 입력 포맷 처리 및 wrapper 호출

## 요청 파라미터
- `fromdate`/`todate`(str): 조회 시작/종료일 `YYYYMMDD`
- `isu_cd`(str): 상품 코드. 예) `KR___OPK2I`(코스피200 옵션)
- `opt_type`(str): 옵션 구분. `C`(콜), `P`(풋)
- `inq_type`(str): 조회 유형 코드. 기본값 `2`
- `prt_check`(str): 집계 옵션. 기본값 `SU`
- 내부 고정값: `prtType='QTY'`(거래량). 거래대금 조회가 필요하면 확장 예정

참고 원본 페이로드(예시):
```
bld=dbms/MDC/STAT/standard/MDCSTAT13102&locale=ko_KR&prodId=&strtDd=20251107&endDd=20251114&inqTpCd=2&prtType=QTY&prtCheck=SU&isuCd=KR___OPK2I&isuOpt=C&aggBasTpCd=&strtDdBox1=20251107&endDdBox1=20251114&share=1&csvxls_isNo=false
```

## 반환 형식
- `pandas.DataFrame`: KRX `output` 블록의 원본 컬럼 유지
- 추후 필요 시 컬럼명 정규화/형 변환 로직 추가 가능

## 사용 예시
```python
from pykrx import stock

# 코스피200 옵션(CALL), 기간 2025-11-07 ~ 2025-11-14 거래량
df = stock.get_option_volume(
    "20251107", "20251114", "KR___OPK2I", opt_type="C"
)
print(df.head())
```

## 비고 / 향후 개선
- `prtType='VAL'`(거래대금) 옵션 분기 추가 가능
- `aggBasTpCd` 등의 집계 옵션 노출 여부 검토
- 응답 스키마 확정 시 컬럼 리네이밍 및 dtype 캐스팅 추가 검토
