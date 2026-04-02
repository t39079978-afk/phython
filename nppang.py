"""
모임 회비 관리 계산기
====================
총 금액, 인원수, 팁/서비스 비율을 입력받아
1인당 금액과 팁 포함 총 금액을 계산하는 프로그램.

작성 규칙:
  - 주석 포함
  - 이모티콘 금지
  - Tkinter 기반 GUI
  - 화이트톤 인터페이스
"""

import tkinter as tk


# ──────────────────────────────────────────────
# 색상 상수 (화이트톤 팔레트)
# ──────────────────────────────────────────────
COLOR_BG           = "#F7F7F8"   # 전체 배경 (오프 화이트)
COLOR_WHITE        = "#FFFFFF"   # 카드 배경 (순백)
COLOR_BORDER       = "#E4E4E7"   # 기본 테두리
COLOR_BORDER_FOCUS = "#71717A"   # 포커스 테두리
COLOR_TEXT_MAIN    = "#18181B"   # 주요 텍스트
COLOR_TEXT_LABEL   = "#52525B"   # 라벨 텍스트
COLOR_TEXT_HINT    = "#A1A1AA"   # 보조/힌트 텍스트
COLOR_BTN_PRIMARY  = "#18181B"   # 제출 버튼 배경
COLOR_BTN_PRI_HV   = "#3F3F46"   # 제출 버튼 호버
COLOR_BTN_RESET    = "#FFFFFF"   # 초기화 버튼 배경
COLOR_BTN_RST_HV   = "#F4F4F5"   # 초기화 버튼 호버
COLOR_RESULT_BG    = "#F4F4F5"   # 결과 필드 배경
COLOR_RESULT_FG    = "#18181B"   # 결과 필드 텍스트
COLOR_DIVIDER      = "#E4E4E7"   # 구분선
COLOR_ERROR        = "#DC2626"   # 에러 텍스트


# ──────────────────────────────────────────────
# 폰트 상수
# ──────────────────────────────────────────────
FONT_TITLE        = ("Helvetica Neue", 15, "bold")
FONT_SUBTITLE     = ("Helvetica Neue", 10)
FONT_LABEL        = ("Helvetica Neue", 10)
FONT_LABEL_BOLD   = ("Helvetica Neue", 10, "bold")
FONT_ENTRY        = ("Helvetica Neue", 12)
FONT_RESULT       = ("Helvetica Neue", 13, "bold")
FONT_RESULT_LABEL = ("Helvetica Neue", 10)
FONT_BUTTON       = ("Helvetica Neue", 11, "bold")
FONT_STATUS       = ("Helvetica Neue", 9)
FONT_UNIT         = ("Helvetica Neue", 10)


# ──────────────────────────────────────────────
# 계산 로직
# ──────────────────────────────────────────────
def calculate(total_amount: float, people_count: int, tip_rate: float):
    """
    회비를 계산하여 결과를 반환한다.

    매개변수:
        total_amount (float) : 총 금액 (원)
        people_count (int)   : 인원수 (명)
        tip_rate     (float) : 팁/서비스 비율 (%)

    반환값:
        tuple(float, float):
            total_with_tip : 팁 포함 총 금액
            per_person     : 1인당 금액
    """
    total_with_tip = total_amount * (1 + tip_rate / 100)
    per_person     = total_with_tip / people_count
    return total_with_tip, per_person


# ──────────────────────────────────────────────
# 입력값 검증
# ──────────────────────────────────────────────
def validate_inputs(total_str: str, people_str: str, tip_str: str):
    """
    입력 문자열을 검증하고 변환된 값을 반환한다.
    오류 발생 시 ValueError를 전파한다.
    """
    # 총 금액 검증
    try:
        total_amount = float(total_str.replace(",", "").strip())
    except ValueError:
        raise ValueError("총 금액에 올바른 숫자를 입력하세요.")
    if total_amount <= 0:
        raise ValueError("총 금액은 0보다 커야 합니다.")

    # 인원수 검증
    try:
        people_count = int(people_str.strip())
    except ValueError:
        raise ValueError("인원수에 올바른 정수를 입력하세요.")
    if people_count <= 0:
        raise ValueError("인원수는 1명 이상이어야 합니다.")

    # 팁 비율 검증
    try:
        tip_rate = float(tip_str.strip())
    except ValueError:
        raise ValueError("팁/서비스 비율에 올바른 숫자를 입력하세요.")
    if tip_rate < 0:
        raise ValueError("팁/서비스 비율은 0 이상이어야 합니다.")

    return total_amount, people_count, tip_rate


# ──────────────────────────────────────────────
# 금액 포매팅
# ──────────────────────────────────────────────
def format_currency(value: float) -> str:
    """
    금액을 천 단위 콤마 포함 문자열로 포매팅한다.
    소수점 이하가 0이면 정수로 표시한다.
    """
    if value == int(value):
        return f"{int(value):,} 원"
    return f"{value:,.1f} 원"


# ──────────────────────────────────────────────
# 메인 애플리케이션 클래스
# ──────────────────────────────────────────────
class MeetingFeeCalculator:
    """
    모임 회비 관리 계산기 GUI 애플리케이션 클래스.
    화이트톤 디자인의 Tkinter UI를 구성하고 이벤트를 처리한다.
    """

    def __init__(self, root: tk.Tk):
        """
        애플리케이션 초기화 및 UI 구성.

        매개변수:
            root (tk.Tk): Tkinter 최상위 윈도우
        """
        self.root = root
        self._configure_window()
        self._init_variables()
        self._build_ui()

    # ──────────────────────────────────────────
    # 창 설정
    # ──────────────────────────────────────────
    def _configure_window(self):
        """메인 윈도우의 제목, 크기, 배경색을 설정한다."""
        self.root.title("모임 회비 관리 계산기")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        window_width  = 440
        window_height = 580
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width  - window_width)  // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ──────────────────────────────────────────
    # 변수 초기화
    # ──────────────────────────────────────────
    def _init_variables(self):
        """입력 및 결과 표시에 사용할 StringVar를 초기화한다."""
        self.var_total      = tk.StringVar()
        self.var_people     = tk.StringVar()
        self.var_tip        = tk.StringVar()
        self.var_per_person = tk.StringVar()
        self.var_total_tip  = tk.StringVar()
        self.var_status     = tk.StringVar()

        # 팁 비율 기본값
        self.var_tip.set("0")

    # ──────────────────────────────────────────
    # 전체 UI 구성
    # ──────────────────────────────────────────
    def _build_ui(self):
        """전체 UI 레이아웃을 구성한다."""
        outer = tk.Frame(self.root, bg=COLOR_BG, padx=28, pady=24)
        outer.pack(fill="both", expand=True)

        self._build_header(outer)
        self._build_input_card(outer)
        self._build_result_card(outer)
        self._build_buttons(outer)
        self._build_status_bar(outer)

    # ──────────────────────────────────────────
    # 헤더
    # ──────────────────────────────────────────
    def _build_header(self, parent):
        """상단 타이틀 및 부제목 영역을 구성한다."""
        header = tk.Frame(parent, bg=COLOR_BG)
        header.pack(fill="x", pady=(0, 20))

        tk.Label(
            header,
            text="회비 관리 계산기",
            font=FONT_TITLE,
            bg=COLOR_BG,
            fg=COLOR_TEXT_MAIN,
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            header,
            text="총 금액, 인원수, 팁 비율을 입력하고 제출하세요.",
            font=FONT_SUBTITLE,
            bg=COLOR_BG,
            fg=COLOR_TEXT_HINT,
            anchor="w",
        ).pack(fill="x", pady=(3, 0))

    # ──────────────────────────────────────────
    # 입력 카드
    # ──────────────────────────────────────────
    def _build_input_card(self, parent):
        """입력 필드들을 담은 카드 형태의 프레임을 구성한다."""
        # 외곽 테두리 (1px 효과)
        card_border = tk.Frame(parent, bg=COLOR_BORDER, padx=1, pady=1)
        card_border.pack(fill="x", pady=(0, 14))

        # 카드 내부 흰색 배경
        card = tk.Frame(card_border, bg=COLOR_WHITE, padx=20, pady=18)
        card.pack(fill="both")

        tk.Label(
            card,
            text="입력 항목",
            font=FONT_LABEL_BOLD,
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_LABEL,
            anchor="w",
        ).pack(fill="x", pady=(0, 12))

        tk.Frame(card, height=1, bg=COLOR_DIVIDER).pack(fill="x", pady=(0, 14))

        # 입력 필드 행
        self._build_input_row(card, "총 금액", "원",  self.var_total)
        self._build_input_row(card, "인원수",  "명",  self.var_people,  pady_top=10)
        self._build_input_row(card, "팁 / 서비스 비율", "%", self.var_tip, pady_top=10)

    def _build_input_row(
        self,
        parent,
        label_text: str,
        unit_text: str,
        textvariable: tk.StringVar,
        pady_top: int = 0,
    ):
        """
        라벨 + 입력 필드 + 단위로 구성된 한 행을 부모 프레임에 추가한다.

        매개변수:
            parent       : 부모 프레임
            label_text   : 필드 라벨 텍스트
            unit_text    : 단위 텍스트
            textvariable : 연결할 StringVar
            pady_top     : 상단 여백 (px)
        """
        row = tk.Frame(parent, bg=COLOR_WHITE)
        row.pack(fill="x", pady=(pady_top, 0))

        # 라벨
        tk.Label(
            row,
            text=label_text,
            font=FONT_LABEL,
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_LABEL,
            width=16,
            anchor="w",
        ).pack(side="left")

        # 입력 필드 (테두리 효과용 래퍼 프레임)
        entry_wrap = tk.Frame(row, bg=COLOR_BORDER, padx=1, pady=1)
        entry_wrap.pack(side="left", fill="x", expand=True)

        entry = tk.Entry(
            entry_wrap,
            textvariable=textvariable,
            font=FONT_ENTRY,
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_MAIN,
            insertbackground=COLOR_TEXT_MAIN,
            relief="flat",
            bd=0,
        )
        entry.pack(fill="x", ipady=7, ipadx=10)

        # 포커스 시 테두리 강조
        entry.bind("<FocusIn>",  lambda e, w=entry_wrap: w.config(bg=COLOR_BORDER_FOCUS))
        entry.bind("<FocusOut>", lambda e, w=entry_wrap: w.config(bg=COLOR_BORDER))

        # 단위 라벨
        tk.Label(
            row,
            text=unit_text,
            font=FONT_UNIT,
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_HINT,
            width=4,
            anchor="w",
        ).pack(side="left", padx=(6, 0))

    # ──────────────────────────────────────────
    # 결과 카드
    # ──────────────────────────────────────────
    def _build_result_card(self, parent):
        """결과 필드들을 담은 카드 형태의 프레임을 구성한다."""
        card_border = tk.Frame(parent, bg=COLOR_BORDER, padx=1, pady=1)
        card_border.pack(fill="x", pady=(0, 16))

        card = tk.Frame(card_border, bg=COLOR_RESULT_BG, padx=20, pady=18)
        card.pack(fill="both")

        tk.Label(
            card,
            text="계산 결과",
            font=FONT_LABEL_BOLD,
            bg=COLOR_RESULT_BG,
            fg=COLOR_TEXT_LABEL,
            anchor="w",
        ).pack(fill="x", pady=(0, 12))

        tk.Frame(card, height=1, bg=COLOR_DIVIDER).pack(fill="x", pady=(0, 14))

        self._build_result_row(card, "팁 포함 총 금액", self.var_total_tip)
        self._build_result_row(card, "1인당 금액",      self.var_per_person, pady_top=10)

    def _build_result_row(
        self,
        parent,
        label_text: str,
        textvariable: tk.StringVar,
        pady_top: int = 0,
    ):
        """
        결과 라벨과 읽기 전용 결과 필드로 구성된 한 행을 구성한다.

        매개변수:
            parent       : 부모 프레임
            label_text   : 필드 라벨 텍스트
            textvariable : 연결할 StringVar
            pady_top     : 상단 여백 (px)
        """
        row = tk.Frame(parent, bg=COLOR_RESULT_BG)
        row.pack(fill="x", pady=(pady_top, 0))

        tk.Label(
            row,
            text=label_text,
            font=FONT_RESULT_LABEL,
            bg=COLOR_RESULT_BG,
            fg=COLOR_TEXT_LABEL,
            width=16,
            anchor="w",
        ).pack(side="left")

        # 읽기 전용 결과 필드
        tk.Entry(
            row,
            textvariable=textvariable,
            font=FONT_RESULT,
            bg=COLOR_RESULT_BG,
            fg=COLOR_RESULT_FG,
            relief="flat",
            bd=0,
            state="readonly",
            readonlybackground=COLOR_RESULT_BG,
            cursor="arrow",
        ).pack(side="left", fill="x", expand=True, ipady=6)

    # ──────────────────────────────────────────
    # 버튼 영역
    # ──────────────────────────────────────────
    def _build_buttons(self, parent):
        """제출 및 초기화 버튼을 구성한다."""
        btn_frame = tk.Frame(parent, bg=COLOR_BG)
        btn_frame.pack(fill="x", pady=(0, 8))

        # 제출 버튼 (어두운 배경, 흰 텍스트)
        self.btn_submit = tk.Button(
            btn_frame,
            text="제출",
            font=FONT_BUTTON,
            bg=COLOR_BTN_PRIMARY,
            fg="#FFFFFF",
            activebackground=COLOR_BTN_PRI_HV,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10,
            command=self._on_submit,
        )
        self.btn_submit.pack(side="left", fill="x", expand=True, padx=(0, 8))

        # 초기화 버튼 (흰 배경, 테두리)
        reset_border = tk.Frame(btn_frame, bg=COLOR_BORDER, padx=1, pady=1)
        reset_border.pack(side="left", fill="x", expand=True)

        self.btn_reset = tk.Button(
            reset_border,
            text="초기화",
            font=FONT_BUTTON,
            bg=COLOR_BTN_RESET,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_BTN_RST_HV,
            activeforeground=COLOR_TEXT_MAIN,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10,
            command=self._on_reset,
        )
        self.btn_reset.pack(fill="both")

        # 호버 효과 바인딩
        self._bind_hover(self.btn_submit, COLOR_BTN_PRIMARY, COLOR_BTN_PRI_HV)
        self._bind_hover(self.btn_reset,  COLOR_BTN_RESET,   COLOR_BTN_RST_HV)

    # ──────────────────────────────────────────
    # 상태 바
    # ──────────────────────────────────────────
    def _build_status_bar(self, parent):
        """하단 오류/상태 메시지 표시줄을 구성한다."""
        tk.Label(
            parent,
            textvariable=self.var_status,
            font=FONT_STATUS,
            bg=COLOR_BG,
            fg=COLOR_ERROR,
            anchor="w",
        ).pack(fill="x")

    # ──────────────────────────────────────────
    # 호버 효과
    # ──────────────────────────────────────────
    def _bind_hover(self, widget, normal_color: str, hover_color: str):
        """
        버튼에 마우스 진입/이탈 호버 색상 효과를 바인딩한다.

        매개변수:
            widget       : 대상 Button 위젯
            normal_color : 기본 배경색
            hover_color  : 호버 배경색
        """
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))

    # ──────────────────────────────────────────
    # 이벤트 핸들러
    # ──────────────────────────────────────────
    def _on_submit(self):
        """
        제출 버튼 클릭 이벤트 핸들러.
        입력값을 검증하고 계산 결과를 결과 필드에 표시한다.
        """
        self.var_status.set("")

        try:
            total_amount, people_count, tip_rate = validate_inputs(
                self.var_total.get(),
                self.var_people.get(),
                self.var_tip.get(),
            )
        except ValueError as e:
            self.var_status.set(f"  {e}")
            return

        # 계산 실행 및 결과 표시
        total_with_tip, per_person = calculate(total_amount, people_count, tip_rate)
        self.var_total_tip.set(format_currency(total_with_tip))
        self.var_per_person.set(format_currency(per_person))

    def _on_reset(self):
        """
        초기화 버튼 클릭 이벤트 핸들러.
        모든 입력/결과 필드와 상태 메시지를 초기화한다.
        """
        self.var_total.set("")
        self.var_people.set("")
        self.var_tip.set("0")
        self.var_per_person.set("")
        self.var_total_tip.set("")
        self.var_status.set("")


# ──────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingFeeCalculator(root)
    root.mainloop()
