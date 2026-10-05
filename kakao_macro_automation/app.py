from classes.app_config import AppConfig
from classes.timer_manager import TimerManager
from classes.template_engine import TemplateEngine
from classes.excel_manager import ExcelManager
from classes.kakao_manager import KakaoWinAuto


def main():
    config = AppConfig()
    timer = TimerManager(interval_minutes=config.timer_minutes)
    excel = ExcelManager(config.excel_path)
    template_engine = TemplateEngine()
    kakao = KakaoWinAuto()

    print("카카오 자동화 매크로 시작")
    print(f"타이머 간격: {config.timer_minutes}분")
    print(f"샌드박스 개수: {config.sandbox_count}개")

    # 예시 흐름
    rows = excel.read_all_rows()
    if rows:
        first_row = rows[0]
        print(template_engine.render(config.template, first_row))

    kakao.launch_kakao()
    kakao.wait_for_ui()

    timer.wait_next_cycle()


if __name__ == "__main__":
    main()
