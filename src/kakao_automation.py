import re
from typing import Any, Dict, List


class TemplateEngine:
    def __init__(self):
        self.placeholder_pattern = re.compile(r"\[(.*?)\]")

    def render(self, template: str, row: Dict[str, Any]) -> str:
        def replacer(match: re.Match[str]) -> str:
            token = match.group(1).strip()
            value = self._resolve_value(token, row)
            return "" if value is None else str(value)

        return self.placeholder_pattern.sub(replacer, template)

    def _resolve_value(self, token: str, row: Dict[str, Any]) -> Any:
        token_lower = token.lower()

        if token_lower in {"a", "name"}:
            return row.get("A") or row.get("name") or row.get("이름")
        if token_lower in {"b", "phone", "tel", "핸드폰", "연락처"}:
            return row.get("B") or row.get("phone") or row.get("연락처")
        if token_lower in {"c", "address"}:
            return row.get("C") or row.get("address") or row.get("주소")
        if token_lower in {"d", "detail_address"}:
            return row.get("D") or row.get("detail_address") or row.get("상세주소")
        if token_lower in {"e", "product", "상품명"}:
            return row.get("E") or row.get("product") or row.get("상품명")
        if token_lower in {"f", "tracking", "송장번호"}:
            return row.get("F") or row.get("tracking") or row.get("송장번호")
        if token_lower in {"g", "memo1"}:
            return row.get("G") or row.get("memo1")
        if token_lower in {"h", "memo2"}:
            return row.get("H") or row.get("memo2")

        if token in row:
            return row[token]

        for key, value in row.items():
            if str(key).strip().lower() == token_lower:
                return value

        return None


def sample_templates() -> List[str]:
    return [
        "[A]님 주문하신 상품 [E]이 발송되어 송장번호 [F] 전달 드립니다.",
        "[A]님 오늘 새로 들어온 신선한 [E]이 있어 안내드립니다.",
        "[A]님 [G] 관련 안내드립니다.",
    ]
