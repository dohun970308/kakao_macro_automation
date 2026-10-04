from typing import Optional


class KakaoWinAuto:
    def __init__(self, app_title: str = "카카오톡"):
        self.app_title = app_title

    def launch_kakao(self):
        # 카톡 프로그램 실행
        pass

    def find_window(self):
        # 카톡 창 찾기
        pass

    def add_friend_by_phone(self, phone_number: str, friend_name: str):
        """
        1. 친구 추가 버튼 클릭
        2. 연락처 탭 선택
        3. 번호 입력
        4. 친구 추가
        5. 이름 수정
        """
        pass

    def search_contact_by_name(self, name: str):
        # 친구 목록 검색
        pass

    def send_message(self, name: str, message: str):
        pass

    def wait_for_ui(self, timeout: float = 10.0):
        pass
