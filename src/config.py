from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class AppConfig:
    data_file: str = "data.xlsx"
    template: str = "[A]님 주문하신 상품 [E]이 발송되어 송장번호 [F] 전달 드립니다."
    sandbox_count: int = 8
    delay_seconds: int = 30
    working_dir: str = str(Path.cwd())
    columns: Dict[str, str] = field(
        default_factory=lambda: {
            "name": "A",
            "phone": "B",
            "address": "C",
            "detail_address": "D",
            "product": "E",
            "tracking_number": "F",
            "memo_1": "G",
            "memo_2": "H",
        }
    )


def load_config() -> AppConfig:
    return AppConfig()
