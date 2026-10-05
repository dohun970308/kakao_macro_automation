import re
from typing import Any, Dict

class TemplateEngine:
    """메시지 템플릿을 실제 값으로 변환하는 엔진"""
    
    def render(self, template: str, row: Dict[str, Any]) -> str:
        """
        템플릿 문자열의 [A], [B], [E] 등을 실제 값으로 치환
        
        예시:
        - 입력: "[A]님 주문하신 상품 [E]이 발송되어 송장번호 [F] 전달 드립니다."
        - 출력: "김철수님 주문하신 상품 USB가 발송되어 송장번호 ABC123 전달 드립니다."
        """
        pattern = re.compile(r"\[(.+?)\]")

        def repl(match):
            token = match.group(1).strip()
            value = self._resolve(row, token)
            return "" if value is None else str(value)

        return pattern.sub(repl, template)

    def _resolve(self, row: Dict[str, Any], token: str) -> Any:
        """
        토큰(A, B, C 등)에 해당하는 값 찾기
        """
        mapping = {
            "A": row.get("A") or row.get("이름"),
            "B": row.get("B") or row.get("휴대폰번호") or row.get("연락처"),
            "C": row.get("C") or row.get("주소"),
            "D": row.get("D") or row.get("상세주소"),
            "E": row.get("E") or row.get("상품명"),
            "F": row.get("F") or row.get("송장번호"),
            "G": row.get("G"),
            "H": row.get("H"),
        }
        return mapping.get(token)
