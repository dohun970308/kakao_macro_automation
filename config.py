from dataclasses import dataclass, field
from typing import Dict

@dataclass
class AppConfig:
    excel_path: str = ""
    timer_minutes: int = 30
    sandbox_count: int = 8
    per_sandbox_send_count: int = 2

    columns: Dict[str, str] = field(default_factory=lambda: {
        "name": "A",
        "phone": "B",
        "address": "C",
        "detail_address": "D",
        "product": "E",
        "tracking_number": "F",
        "extra_1": "G",
        "extra_2": "H",
    })

    template: str = "[A]님 주문하신 상품 [E]이 발송되어 송장번호 [F] 전달 드립니다."
