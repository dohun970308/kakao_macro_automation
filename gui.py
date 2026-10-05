import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
from config import AppConfig
from timer_manager import TimerManager
from template_engine import TemplateEngine
from excel_manager import ExcelManager

class AppWindow:
    """
    카카오 자동화 메인 GUI 애플리케이션
    
    기능:
    - 엑셀 파일 선택
    - 타이머 간격 설정 (분 단위)
    - 친구 추가 시작
    - 메시지 전송 시작
    - 메시지 템플릿 커스터마이징
    - 실시간 로그 표시
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("카카오 자동화 매크로")
        self.root.geometry("1000x800")
        
        self.config = AppConfig()
        self.template_engine = TemplateEngine()
        self.excel_manager = None
        self.timer = None
        self.is_running = False
        
        # 변수 설정
        self.excel_path_var = tk.StringVar()
        self.timer_var = tk.StringVar(value="30")
        self.template_var = tk.StringVar(value=self.config.template)
        
        self.build_ui()

    def build_ui(self):
        """UI 구성"""
        
        # ===== 파일 선택 섹션 =====
        file_frame = ttk.LabelFrame(self.root, text="파일 설정", padding=10)
        file_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(file_frame, text="엑셀 파일:").pack(anchor="w", pady=(0, 5))
        path_input_frame = ttk.Frame(file_frame)
        path_input_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Entry(path_input_frame, textvariable=self.excel_path_var, width=100).pack(side="left", fill="x", expand=True)
        ttk.Button(path_input_frame, text="파일 선택", command=self.select_excel).pack(side="left", padx=5)
        
        # ===== 타이머 설정 섹션 =====
        timer_frame = ttk.LabelFrame(self.root, text="타이머 설정", padding=10)
        timer_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(timer_frame, text="전송 간격 (분):").pack(anchor="w", pady=(0, 5))
        ttk.Entry(timer_frame, textvariable=self.timer_var, width=10).pack(anchor="w")
        ttk.Label(timer_frame, text="예: 10, 15, 20, 30, 45, 60", foreground="gray").pack(anchor="w")
        
        # ===== 템플릿 설정 섹션 =====
        template_frame = ttk.LabelFrame(self.root, text="메시지 템플릿", padding=10)
        template_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(template_frame, text="변수: [A]=이름, [B]=연락처, [C]=주소, [D]=상세주소, [E]=상품명, [F]=송장번호, [G]/[H]=추가").pack(anchor="w", pady=(0, 5))
        
        self.template_text = tk.Text(template_frame, height=4, width=100)
        self.template_text.insert("1.0", self.config.template)
        self.template_text.pack(fill="x", pady=(0, 5))
        
        # 템플릿 프리셋
        preset_frame = ttk.Frame(template_frame)
        preset_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Button(preset_frame, text="프리셋 1", 
                   command=lambda: self.set_template("[A]님 주문하신 상품 [E]이 발송되어 송장번호 [F] 전달 드립니다.")).pack(side="left", padx=2)
        ttk.Button(preset_frame, text="프리셋 2", 
                   command=lambda: self.set_template("[A]님 오늘 새로 들어온 신선한 [E]이 있어 안내드립니다.")).pack(side="left", padx=2)
        
        # ===== 버튼 섹션 =====
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="친구 추가 시작", command=self.start_friend_add).pack(side="left", padx=5)
        ttk.Button(button_frame, text="메시지 전송 시작", command=self.start_message_send).pack(side="left", padx=5)
        ttk.Button(button_frame, text="프리뷰", command=self.preview_message).pack(side="left", padx=5)
        ttk.Button(button_frame, text="중단", command=self.stop_process).pack(side="left", padx=5)
        
        # ===== 로그 섹션 =====
        log_frame = ttk.LabelFrame(self.root, text="로그", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.log = tk.Text(log_frame, height=15, yscrollcommand=scrollbar.set)
        self.log.pack(fill="both", expand=True)
        scrollbar.config(command=self.log.yview)

    def select_excel(self):
        """엑셀 파일 선택"""
        filepath = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if filepath:
            self.excel_path_var.set(filepath)
            self.log_message(f"파일 선택: {filepath}")

    def set_template(self, template_text: str):
        """템플릿 설정"""
        self.template_text.delete("1.0", "end")
        self.template_text.insert("1.0", template_text)

    def preview_message(self):
        """메시지 프리뷰"""
        try:
            excel_path = self.excel_path_var.get()
            if not excel_path:
                messagebox.showwarning("경고", "엑셀 파일을 선택해주세요.")
                return
            
            manager = ExcelManager(excel_path)
            rows = manager.read_all_rows()
            
            if not rows:
                messagebox.showwarning("경고", "엑셀에 데이터가 없습니다.")
                return
            
            template = self.template_text.get("1.0", "end").strip()
            preview = self.template_engine.render(template, rows[0])
            
            messagebox.showinfo("메시지 프리뷰", preview)
            self.log_message(f"프리뷰: {preview}")
        except Exception as e:
            messagebox.showerror("오류", str(e))
            self.log_message(f"오류: {e}")

    def start_friend_add(self):
        """친구 추가 시작"""
        if self.is_running:
            messagebox.showwarning("경고", "이미 실행 중입니다.")
            return
        
        try:
            excel_path = self.excel_path_var.get()
            if not excel_path:
                messagebox.showwarning("경고", "엑셀 파일을 선택해주세요.")
                return
            
            self.is_running = True
            self.log_message("친구 추가 프로세스 시작...")
            
            # 별도 스레드에서 실행
            thread = threading.Thread(target=self._run_friend_add, args=(excel_path,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            messagebox.showerror("오류", str(e))
            self.log_message(f"오류: {e}")
            self.is_running = False

    def _run_friend_add(self, excel_path: str):
        """친구 추가 실행 (별도 스레드)"""
        try:
            manager = ExcelManager(excel_path)
            rows = manager.read_all_rows()
            
            self.log_message(f"총 {len(rows)}명의 고객 데이터 로드됨")
            
            # TODO: 실제 자동화 로직
            for idx, row in enumerate(rows):
                if not self.is_running:
                    break
                
                name = row.get("A") or row.get("이름")
                phone = row.get("B") or row.get("연락처") or row.get("휴대폰번호")
                
                if name and phone:
                    self.log_message(f"[{idx+1}/{len(rows)}] {name}님 친구 추가 처리 중...")
                    manager.write_status(idx, "친구추가완료")
            
            self.log_message("친구 추가 프로세스 완료")
        except Exception as e:
            self.log_message(f"오류: {e}")
        finally:
            self.is_running = False

    def start_message_send(self):
        """메시지 전송 시작"""
        if self.is_running:
            messagebox.showwarning("경고", "이미 실행 중입니다.")
            return
        
        try:
            excel_path = self.excel_path_var.get()
            if not excel_path:
                messagebox.showwarning("경고", "엑셀 파일을 선택해주세요.")
                return
            
            timer_minutes = int(self.timer_var.get())
            self.is_running = True
            self.log_message(f"메시지 전송 프로세스 시작... (타이머: {timer_minutes}분)")
            
            thread = threading.Thread(target=self._run_message_send, args=(excel_path, timer_minutes))
            thread.daemon = True
            thread.start()
        except ValueError:
            messagebox.showerror("오류", "타이머는 숫자여야 합니다.")
        except Exception as e:
            messagebox.showerror("오류", str(e))
            self.log_message(f"오류: {e}")
            self.is_running = False

    def _run_message_send(self, excel_path: str, timer_minutes: int):
        """메시지 전송 실행 (별도 스레드)"""
        try:
            manager = ExcelManager(excel_path)
            rows = manager.read_all_rows()
            template = self.template_text.get("1.0", "end").strip()
            
            self.log_message(f"총 {len(rows)}명의 고객 데이터 로드됨")
            
            # TODO: 실제 자동화 로직 + 타이머
            for idx, row in enumerate(rows):
                if not self.is_running:
                    break
                
                name = row.get("A") or row.get("이름")
                message = self.template_engine.render(template, row)
                
                if name:
                    self.log_message(f"[{idx+1}/{len(rows)}] {name}님에게 메시지 전송 중...")
                    # TODO: 실제 메시지 전송
                    manager.write_status(idx, "메시지전송완료")
            
            self.log_message("메시지 전송 프로세스 완료")
        except Exception as e:
            self.log_message(f"오류: {e}")
        finally:
            self.is_running = False

    def stop_process(self):
        """프로세스 중단"""
        self.is_running = False
        self.log_message("프로세스 중단됨")

    def log_message(self, message: str):
        """로그 메시지 출력"""
        self.log.config(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.config(state="disabled")
        self.root.update()

def create_app():
    """GUI 앱 생성 및 실행"""
    root = tk.Tk()
    window = AppWindow(root)
    root.mainloop()

if __name__ == "__main__":
    create_app()
