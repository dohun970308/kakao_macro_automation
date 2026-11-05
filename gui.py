import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config import AppConfig
from excel_manager import ExcelManager
from template_engine import TemplateEngine


class AppWindow:
    """KakaoTalk macro GUI with unsafe, unverified actions disabled."""

    DISABLED_NOTICE = (
        "카카오톡 친구 추가/메시지 전송은 안전 검증이 구현되지 않아 비활성화되어 있습니다.\n"
        "이 앱은 카카오톡을 조작하거나 엑셀 상태를 완료로 변경하지 않습니다."
    )

    def __init__(self, root):
        self.root = root
        self.root.title("카카오 자동화 매크로 — 안전 모드")
        self.root.geometry("900x650")
        self.config = AppConfig()
        self.template_engine = TemplateEngine()
        self.excel_path_var = tk.StringVar()
        self.build_ui()

    def build_ui(self):
        file_frame = ttk.LabelFrame(self.root, text="파일 설정", padding=10)
        file_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(file_frame, text="엑셀 파일:").pack(anchor="w")
        path_row = ttk.Frame(file_frame)
        path_row.pack(fill="x", pady=(5, 0))
        ttk.Entry(path_row, textvariable=self.excel_path_var).pack(side="left", fill="x", expand=True)
        ttk.Button(path_row, text="파일 선택", command=self.select_excel).pack(side="left", padx=5)

        template_frame = ttk.LabelFrame(self.root, text="메시지 미리보기 템플릿", padding=10)
        template_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(
            template_frame,
            text="변수: [A]=이름, [B]=연락처, [C]=주소, [D]=상세주소, [E]=상품명, [F]=송장번호",
        ).pack(anchor="w")
        self.template_text = tk.Text(template_frame, height=4, width=100)
        self.template_text.insert("1.0", self.config.template)
        self.template_text.pack(fill="x", pady=(5, 0))

        ttk.Label(
            self.root,
            text=self.DISABLED_NOTICE,
            foreground="#9b1c1c",
            justify="left",
            wraplength=850,
        ).pack(fill="x", padx=12, pady=8)

        button_row = ttk.Frame(self.root)
        button_row.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_row, text="친구 추가 시작", command=self.start_friend_add).pack(side="left", padx=5)
        ttk.Button(button_row, text="메시지 전송 시작", command=self.start_message_send).pack(side="left", padx=5)
        ttk.Button(button_row, text="첫 행 미리보기", command=self.preview_message).pack(side="left", padx=5)

        log_frame = ttk.LabelFrame(self.root, text="로그", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.log = tk.Text(log_frame, height=12, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True)
        self.log_message("안전 모드로 시작했습니다. 친구 추가 및 메시지 전송은 실행되지 않습니다.")

    def select_excel(self):
        filepath = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel Files", "*.xlsx")],
        )
        if filepath:
            self.excel_path_var.set(filepath)
            self.log_message(f"파일 선택: {filepath}")

    def preview_message(self):
        try:
            excel_path = self.excel_path_var.get().strip()
            if not excel_path:
                messagebox.showwarning("경고", "엑셀 파일을 선택해주세요.")
                return
            rows = ExcelManager(excel_path).read_all_rows()
            if not rows:
                messagebox.showwarning("경고", "미리보기할 데이터가 없습니다.")
                return
            template = self.template_text.get("1.0", "end-1c").strip()
            preview = self.template_engine.render(template, rows[0])
            messagebox.showinfo("첫 행 미리보기 (전송 안 함)", preview)
            self.log_message("첫 데이터 행의 미리보기만 표시했습니다. 메시지는 전송되지 않았습니다.")
        except Exception as exc:
            messagebox.showerror("오류", str(exc))
            self.log_message(f"미리보기 오류: {exc}")

    def start_friend_add(self):
        self._blocked_action("친구 추가")

    def start_message_send(self):
        self._blocked_action("메시지 전송")

    def _blocked_action(self, action: str):
        message = f"{action}을(를) 실행하지 않았습니다. 실제 UI 조작 및 성공 검증이 구현되지 않아 안전을 위해 차단했습니다."
        self.log_message(message)
        messagebox.showwarning("실행 차단", message)

    def log_message(self, message: str):
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")


def create_app():
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    create_app()
