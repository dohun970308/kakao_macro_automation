from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelManager:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def read_rows(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"엑셀 파일이 없습니다: {self.file_path}")

        workbook = load_workbook(self.file_path, data_only=True)
        sheet = workbook.active
        rows = list(sheet.iter_rows(values_only=True))

        if not rows:
            return []

        headers = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
        data_rows = rows[1:]

        result: List[Dict[str, Any]] = []
        for row in data_rows:
            item: Dict[str, Any] = {}
            for idx, header in enumerate(headers):
                item[header or f"col_{idx + 1}"] = row[idx] if idx < len(row) else None
            result.append(item)
        return result

    def read_sheet(self) -> Tuple[List[str], List[List[Any]]]:
        workbook = load_workbook(self.file_path, data_only=True)
        sheet = workbook.active
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return [], []

        headers = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
        data = [list(row) for row in rows[1:]]
        return headers, data

    def write_status(self, row_index: int, status: str) -> None:
        workbook = load_workbook(self.file_path, data_only=False)
        sheet = workbook.active
        status_col = self._find_or_create_column(sheet, "상태")
        sheet.cell(row=row_index + 2, column=status_col, value=status)
        workbook.save(self.file_path)

    def _find_or_create_column(self, sheet: Worksheet, title: str) -> int:
        for cell in sheet[1]:
            if cell.value == title:
                return cell.column

        last_col = sheet.max_column + 1
        sheet.cell(row=1, column=last_col, value=title)
        return last_col

    def create_template_sheet(self, template_name: str = "진행상태") -> Worksheet:
        workbook = load_workbook(self.file_path, data_only=False) if self.file_path.exists() else Workbook()
        sheet = workbook.active
        sheet.title = template_name
        workbook.save(self.file_path)
        return sheet


def normalize_column_name(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣_]", "", value).strip()
