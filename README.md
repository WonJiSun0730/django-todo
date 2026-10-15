# Django Todo List — 문항 11

Python 3.12+, Django 5.2 LTS, MySQL 8.0+로 만든 할 일 관리 앱입니다.

## 구현 사항

- Todo 제목(필수, 최대 200자), 세부 내용(선택), 완료 여부(기본 False), 자동 생성 일시
- 목록, 등록, 수정, 삭제 확인 및 삭제
- 목록 체크박스를 선택한 뒤 **상태 저장** 버튼으로 완료/미완료 저장
- 완료 항목 취소선 및 배경색, 전체/진행 중/완료 필터와 건수
- 등록·수정 서버 유효성 검사, 한국어 오류 메시지
- 관리자 목록, 검색 및 완료 여부 필터
- POST/CSRF 보호, 모바일 대응

## 실행 (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

MySQL 관리자 계정으로 접속하여 다음을 실행합니다. 비밀번호는 직접 정한 값으로 바꾸세요.

```sql
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'todo_user'@'127.0.0.1' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'127.0.0.1';
```

`.env`의 MYSQL_PASSWORD를 위 비밀번호로 변경하고 나머지 연결 값을 확인합니다.
DJANGO_SECRET_KEY도 임의의 긴 문자열로 변경합니다. 실제 비밀번호가 담긴 `.env`는 Git에 포함되지 않습니다.

```powershell
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver
```

- 앱: http://127.0.0.1:8000/
- 관리자: http://127.0.0.1:8000/admin/

이 앱은 과제용 단일 사용자 앱이며, 목록은 접속자들이 공유합니다.

## 제출 DDL

`sql/schema.sql`에 Todo 테이블 생성 DDL이 있습니다. 기본 설치는 데이터베이스만 생성한 뒤
`migrate`로 Todo 및 관리자·인증 테이블을 함께 생성합니다. DDL을 먼저 실행하면 테이블이 중복되므로
일반 설치에서 schema.sql의 CREATE TABLE은 별도로 실행하지 않습니다.

`created_at`은 Django의 `auto_now_add`가 자동 입력합니다. SQL에서 직접 INSERT할 때는 값을 제공해야 합니다.
선택 항목인 content는 NULL 대신 빈 문자열로 저장합니다.

## 테스트

MySQL 테스트(계정에 test_todo_db 생성/삭제 권한 필요):

```powershell
.\.venv\Scripts\python manage.py test
```

MySQL 없이 CRUD 로직만 검증하는 별도 테스트 설정:

```powershell
.\.venv\Scripts\python manage.py test --settings=config.test_settings
```

기본 settings.py는 항상 MySQL을 사용하며 자동 SQLite 대체는 없습니다.

## GitHub 업로드

GitHub에서 `django-todo` 빈 저장소를 생성합니다(README/.gitignore/License 추가 안 함).
프로젝트 폴더에서 다음을 실행합니다. 주소의 아이디를 실제 값으로 바꾸세요.

```powershell
git init -b main
git add .
git commit -m "Implement Django Todo CRUD with MySQL"
git remote add origin https://github.com/YOUR_USERNAME/django-todo.git
git push -u origin main
```

제출할 링크는 `https://github.com/본인아이디/django-todo`입니다.

참고: [Django 공식 MySQL 문서](https://docs.djangoproject.com/en/5.2/ref/databases/#mysql-notes)
