from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.config import AppConfig, load_config
from src.excel_manager import ExcelManager
from src.template_engine import TemplateEngine


class AppWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("카카오톡 자동화 매크로")
        self.root.geometry("900x700")
        self.config = load_config()
        self.template_engine = TemplateEngine()

        self._build_ui()

    def _build_ui(self):
        # 파일 선택
        file_frame = ttk.LabelFrame(self.root, text="엑셀 설정")
        file_frame.pack(fill="x", padx=12, pady=8)

        self.file_var = tk.StringVar(value=self.config.data_file)
        ttk.Entry(file_frame, textvariable=self.file_var, width=80).grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        ttk.Button(file_frame, text="엑셀 선택", command=self.select_excel).grid(row=0, column=1, padx=8, pady=8)

        # 템플릿
        template_frame = ttk.LabelFrame(self.root, text="메시지 템플릿")
        template_frame.pack(fill="x", padx=12, pady=8)

        self.template_text = tk.Text(template_frame, height=6)
        self.template_text.insert(
            "1.0",
            self.config.template,
        )
        self.template_text.pack(fill="x", padx=8, pady=8)

        # 버튼 영역
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=12, pady=8)

        ttk.Button(button_frame, text="친구 추가 시작", command=self.start_friend_add).pack(side="left", padx=6)
        ttk.Button(button_frame, text="메시지 전송 시작", command=self.start_message_send).pack(side="left", padx=6)
        ttk.Button(button_frame, text="템플릿 미리보기", command=self.preview_template).pack(side="left", padx=6)

        # 로그 영역
        log_frame = ttk.LabelFrame(self.root, text="상태 로그")
        log_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.log = tk.Text(log_frame, state="disabled")
        self.log.pack(fill="both", expand=True, padx=8, pady=8)

    def select_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if path:
            self.file_var.set(path)
            self.log_message(f"엑셀 파일 선택: {path}")

    def start_friend_add(self):
        try:
            path = self.file_var.get()
            manager = ExcelManager(path)
            rows = manager.read_rows()
            if not rows:
                raise ValueError("엑셀에 데이터가 없습니다.")
            self.log_message(f"친구 추가 대상 {len(rows)}건 로드 완료")
            self.log_message("주의: 실제 카카오톡 자동화 로직은 별도 구현이 필요합니다.")
        except Exception as exc:
            messagebox.showerror("오류", str(exc))

    def start_message_send(self):
        try:
            template = self.template_text.get("1.0", "end").strip()
            if not template:
                raise ValueError("메시지 템플릿을 입력하세요.")
            path = self.file_var.get()
            manager = ExcelManager(path)
            rows = manager.read_rows()
            if not rows:
                raise ValueError("엑셀에 데이터가 없습니다.")
            preview = self.template_engine.render(template, rows[0])
            self.log_message(f"미리보기: {preview}")
        except Exception as exc:
            messagebox.showerror("오류", str(exc))

    def preview_template(self):
        try:
            path = self.file_var.get()
            manager = ExcelManager(path)
            rows = manager.read_rows()
            if not rows:
                raise ValueError("엑셀에 데이터가 없습니다.")
            template = self.template_text.get("1.0", "end").strip()
            preview = self.template_engine.render(template, rows[0])
            messagebox.showinfo("템플릿 미리보기", preview)
        except Exception as exc:
            messagebox.showerror("오류", str(exc))

    def log_message(self, message: str):
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")


def create_app():
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()
