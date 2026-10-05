from openpyxl import load_workbook
from typing import Any, Dict, List
import os

class ExcelManager:
    """엑셀 파일 읽기 및 상태 관리"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"엑셀 파일이 없습니다: {file_path}")

    def read_all_rows(self) -> List[Dict[str, Any]]:
        """
        엑셀의 모든 행을 읽어서 딕셔너리 리스트로 반환
        
        반환:
        [
            {"A": "홍길동", "B": "010-1234-5678", "E": "USB", ...},
            {"A": "김철수", "B": "010-2345-6789", "E": "외장HDD", ...},
            ...
        ]
        """
        wb = load_workbook(self.file_path, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))

        if not rows:
            return []

        # 첫 번째 행을 헤더로 사용
        headers = [str(v).strip() if v is not None else "" for v in rows[0]]
        data = []

        for row in rows[1:]:
            item = {}
            for idx, header in enumerate(headers):
                item[header] = row[idx] if idx < len(row) else None
            data.append(item)

        return data

    def write_status(self, row_index: int, status: str):
        """
        특정 행의 상태 컬럼 업데이트
        
        예시:
        - row_index=0, status="친구추가완료" -> 첫 번째 데이터 행의 상태 업데이트
        - row_index=1, status="메시지전송완료" -> 두 번째 데이터 행의 상태 업데이트
        """
        wb = load_workbook(self.file_path)
        ws = wb.active

        # 상태 컬럼 찾기
        status_col = 1
        for cell in ws[1]:
            if cell.value == "상태":
                status_col = cell.column
                break
        else:
            # 상태 컬럼이 없으면 새로 생성
            status_col = ws.max_column + 1
            ws.cell(row=1, column=status_col, value="상태")

        # 데이터 행에 상태 작성 (헤더는 1행이므로 row_index + 2)
        ws.cell(row=row_index + 2, column=status_col, value=status)
        wb.save(self.file_path)
