from __future__ import annotations

from typing import Any, Dict, List


class KakaoAutomation:
    """UI 자동화 로직을 담는 추상 인터페이스입니다.

    실제 카카오톡 PC 자동화는 pywinauto 또는 pyautogui 기반으로 구현할 수 있습니다.
    이 스켈레톤에서는 메서드 구조만 정리해 두었습니다.
    """

    def __init__(self, sandbox_count: int = 8):
        self.sandbox_count = sandbox_count

    def add_friend_by_phone(self, phone_number: str, name: str, sandbox_index: int = 0) -> bool:
        # TODO: phone_number를 입력해 친구 추가
        # TODO: 이름으로 카톡 이름 설정
        raise NotImplementedError("카카오톡 친구 추가 로직을 구현해야 합니다.")

    def send_message_to_contact(self, contact_name: str, message: str, sandbox_index: int = 0) -> bool:
        # TODO: 친구 목록에서 이름 검색 후 메시지 전송
        raise NotImplementedError("카카오톡 메시지 전송 로직을 구현해야 합니다.")

    def run_batch_friend_add(self, records: List[Dict[str, Any]]) -> None:
        for idx, record in enumerate(records):
            phone_number = str(record.get("B") or record.get("phone") or "").strip()
            name = str(record.get("A") or record.get("name") or "").strip()
            sandbox_index = idx % self.sandbox_count
            if phone_number and name:
                self.add_friend_by_phone(phone_number, name, sandbox_index=sandbox_index)

    def run_batch_message_send(self, records: List[Dict[str, Any]], template: str) -> None:
        # TODO: 템플릿 렌더링 후 지정된 샌드박스 인스턴스에 전송
        raise NotImplementedError("배치 메시지 전송 로직을 구현해야 합니다.")
