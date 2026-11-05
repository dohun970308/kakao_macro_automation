# Kakao Contact Automation

이 프로젝트는 카카오톡 PC 자동화를 위한 Python 기반 GUI 스켈레톤입니다.

## 안전 상태

현재 친구 추가와 메시지 전송은 **안전 모드에서 차단**됩니다. 실제 카카오톡 UI 자동화, 검색 결과의 고유한 수신자 확인, 전송 성공 검증, 중단 후 재개를 위한 기록이 구현되어 있지 않습니다. 따라서 앱은 카카오톡에 키 입력을 보내지 않으며, 친구 추가/메시지 전송 완료 로그를 남기거나 엑셀 행을 완료 상태로 바꾸지 않습니다. 미리보기 기능만 데이터를 읽고 첫 행 메시지 예시를 보여 줍니다.

이 제한을 제거하기 전에는 명시적 수신 동의(opt-in), 수신 거부 절차, 개인정보 보호 및 관련 법령을 준수해야 합니다. 대량 또는 원치 않는 메시지 발송에 사용하지 마세요.

## 프로젝트 구조

- `app.py`: 실행 진입점
- `gui.py`: Tkinter GUI와 안전 차단
- `excel_manager.py`: 엑셀 읽기/쓰기 유틸리티
- `template_engine.py`: 메시지 템플릿 엔진
- `kakao_winauto.py`, `src/kakao_automation.py`: 자동화 인터페이스/스켈레톤 (실제 UI 자동화 미구현)
- `build_exe.py`: PyInstaller 배포용 빌드 스크립트

## 엑셀 형식

첫 번째 행은 헤더로 읽으며, 템플릿은 A~H 또는 이름/연락처와 같은 별칭을 지원합니다. 실제 전송 기능은 비활성화되어 있습니다.

## 시작 방법

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

실제 UI 자동화는 카카오톡 버전과 화면 상태에 따라 달라질 수 있습니다. UI 요소와 수신자 식별 및 결과 검증을 테스트하지 않은 상태로는 자동 입력/전송을 활성화하지 마세요.
