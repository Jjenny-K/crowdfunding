# Crowdfunding
원티드 프리온보딩 코스 선발과제를 기준으로 DRF RE-REVIEW

### Progress check ~~[GoTo]~~
- 요구사항 분석, 정보 기록 및 프로젝트 진행을 위해 사용

## Task interpretation
해당 기능을 사용할 수 있는 권한이 있는 client(상품 게시자, 펀딩 서비스 사용자 등)에게 크라우드 펀딩 기능을 제공하는 서비스라고 해석하였습니다.

## Implementation requirements
- Database
    - [ ]  RDB 사용
- REST API
    - [ ]  상품 등록
        - `제목`, `게시자명`, `상품설명`, `목표금액`, `펀딩종료일`, `1회펀딩금액`으로 구성
    - [ ]  상품 수정
        - 모든 내용이 수정 가능하나 `목표금액`은 수정불가
    - [ ]  상품 삭제
        - DB에서 삭제
    - [ ]  상품 목록
        - `제목`, `게시자명`, `총펀딩금액`, `달성률`, `D-day`가 포함
        - `달성률`: `총펀딩금액`/`목표금액`100 (소수점 무시)
        - `D-day`: 펀딩 종료일까지
        - [ ]  상품 검색: 검색된 문자열 포함된 상품 리스트 조회
        - [ ]  상품 정렬: `생성일`, `총펀딩금액` 기준으로 정렬
    - [ ]  상품 상세
        - `제목`, `게시자명`, `총펀딩금액`, `달성률`, `D-day`, `상품설명`, `목표금액`, `참여자 수`가 포함
- Implementation
    - ORM 사용 구현 및 JSON 형식 결과 도출
    - 효율성과 적합성을 고려한 설계 및 구현
- Bonus points
    - [ ]  Unit test 구현
    - [ ]  Git commit convention

## Implementation

### Tech Stack
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=PostgreSQL&logoColor=white"/>

### Development Period
* 2022.07.20 - 

> ### ERD


> ### API Specification


### Step to run
```
$ git clone https://github.com/Jjenny-K/crowdfunding.git

$ python -m venv venv
$ source venv/Scripts/activate
$ python install -r requirements.txt

$ python manage.py migrate --settings=config.settings.develop
$ python manage.py runserver --settings=config.settings.develop
```

## Author
All of development : :monkey_face: **Kang Jeonghui**