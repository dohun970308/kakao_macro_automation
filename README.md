# Kakao Contact Automation

이 프로젝트는 카카오톡 PC 자동화를 위한 Python 기반의 샌드박스 작업 환경용 스켈레톤입니다.

주요 목표:
- 엑셀 기반 고객 정보 관리
- 친구 추가 및 이름 설정 자동화
- 템플릿 기반 메시지 전송
- 여러 샌드박스 인스턴스에서 병렬 작업 구성
- EXE 배포용 구조 준비

중요 주의:
- 이 프로젝트는 법적/윤리적 허용 범위 내에서만 사용해야 합니다.
- 사전 동의, 명시적 opt-in, 수신 거부 절차, 개인정보 보호 규정 준수가 필수입니다.
- 연락처 추가 및 메시지 전송은 사용자의 운영 정책과 국내/해외 법령을 반드시 준수해야 합니다.

프로젝트 구조:

- `app.py`: 실행 진입점
- `src/gui.py`: Tkinter 기반 UI
- `src/excel_manager.py`: 엑셀 읽기/쓰기
- `src/template_engine.py`: 메시지 템플릿 엔진
- `src/kakao_automation.py`: 자동화 로직 인터페이스
- `build_exe.py`: PyInstaller 배포용 빌드 스크립트

예시 템플릿:

- `[A]님 주문하신 상품 [E]이 발송되어 송장번호 [F] 전달 드립니다.`
- `[A]님 오늘 새로 들어온 신선한 [E]이 있어 안내드립니다.`

엑셀 구조 예시:

| 컬럼 | 의미 |
| --- | --- |
| A | 이름 |
| B | 전화번호 |
| C | 주소 |
| D | 상세주소 |
| E | 상품명 |
| F | 송장번호 |
| G | 추가 메모 |
| H | 추가 필드 |

시작 방법:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

배포용 EXE 생성:

```bash
pyinstaller --onefile --windowed app.py
```

참고: 실제 카카오톡 PC 자동화는 UI 요소 위치, 브라우저/앱 상태, 계정 방화벽, 카카오 정책 변화에 따라 동작이 달라질 수 있습니다.
