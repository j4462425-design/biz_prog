import streamlit as st
import json
import os
import datetime

# 페이지 설정 (반드시 최상단에 호출)
st.set_page_config(
    page_title="Daily Vibe",
    page_icon="📅",
    layout="centered",
)

DB_FILE = "todos_db.json"

# 로컬 JSON 파일로부터 할 일 로드
def load_todos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# 로컬 JSON 파일에 할 일 저장
def save_todos(todos):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")

# D-Day 계산 함수
def calculate_dday(due_date_str, is_completed):
    if not due_date_str:
        return None
    try:
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        diff = (due_date - today).days
        
        is_overdue = False
        if diff == 0:
            dday_text = "D-Day"
        elif diff > 0:
            dday_text = f"D-{diff}"
        else:
            dday_text = f"D+{abs(diff)} (지남)"
            if not is_completed:
                is_overdue = True
                
        formatted_date = due_date.strftime("%m/%d")
        return {
            "text": f"📅 {formatted_date} ({dday_text})",
            "is_overdue": is_overdue
        }
    except Exception:
        return None

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

if "current_filter" not in st.session_state:
    st.session_state.current_filter = "all"

if "validation_error" not in st.session_state:
    st.session_state.validation_error = False

# ----------------- 콜백 함수 정의 -----------------
def toggle_todo(todo_id):
    # st.checkbox의 현재 선택된 값은 st.session_state[f"check_{todo_id}"]에 들어있음
    val = st.session_state.get(f"check_{todo_id}", False)
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            todo["completed"] = val
            break
    save_todos(st.session_state.todos)

def delete_todo(todo_id):
    st.session_state.todos = [t for t in st.session_state.todos if t["id"] != todo_id]
    save_todos(st.session_state.todos)
    # 세션 상태 키 정리
    if f"check_{todo_id}" in st.session_state:
        del st.session_state[f"check_{todo_id}"]

# ----------------- 커스텀 CSS 주입 (아이보리 & 라이트 핑크 테마) -----------------
st.markdown(
    """
    <style>
    /* 전체 앱 배경 설정 */
    .stApp {
        background: linear-gradient(135deg, #FAF6F0 0%, #F5EDE3 100%) !important;
    }
    
    /* 메인 카드 스타일링 (Streamlit의 block-container 활용) */
    .block-container {
        max-width: 520px !important;
        padding: 3rem 2rem !important;
        background-color: #FFFDFB !important;
        border-radius: 24px !important;
        box-shadow: 0 16px 40px -8px rgba(74, 62, 61, 0.06) !important;
        border: 1px solid rgba(240, 229, 216, 0.6) !important;
        margin-top: 3rem !important;
    }
    
    /* 폰트 및 텍스트 색상 전역 설정 */
    h1, h2, h3, p, span, label, div {
        color: #4A3E3D !important;
        font-family: 'Outfit', 'Inter', sans-serif !important;
    }
    
    /* 할 일 리스트 개별 행 디자인 (체크박스를 포함한 st.columns 전체 행) */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) {
        background-color: #FFFDFB !important;
        border: 1.5px solid #F0E5D8 !important;
        border-radius: 16px !important;
        padding: 0.5rem 0.8rem !important;
        margin-bottom: 0.65rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        align-items: center !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]):hover {
        border-color: #E8A0A2 !important;
        background-color: #FAFDFB !important;
        box-shadow: 0 4px 12px rgba(74, 62, 61, 0.05) !important;
    }
    
    /* 카테고리 배지 스타일 */
    .todo-category-badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
        background-color: #FCEAEA;
        color: #4A3E3D;
        margin-right: 0.5rem;
        display: inline-block;
    }
    .todo-category-badge.completed {
        background-color: #EFE6DC;
        color: #9E8E8D;
    }
    
    /* 할 일 텍스트 스타일 */
    .todo-text {
        font-size: 0.95rem;
        font-weight: 500;
        color: #4A3E3D;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .todo-text.completed {
        text-decoration: line-through;
        color: #9E8E8D;
    }
    
    /* 마감일 및 D-day 배지 */
    .todo-date-badge {
        font-size: 0.78rem;
        color: #9E8E8D;
        background-color: #FAF7F4;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        border: 1px solid #F0E5D8;
        margin-left: 0.5rem;
        display: inline-block;
        white-space: nowrap;
    }
    .todo-date-badge.overdue {
        color: #D67274;
        background-color: #FFF2F2;
        border-color: #FADEDF;
        font-weight: 500;
    }
    
    .todo-item-content {
        display: flex;
        align-items: center;
        width: 100%;
        overflow: hidden;
    }
    
    /* 인풋 폼 내부 테두리 둥글게 */
    input, select, div[role="combobox"] {
        background-color: #FAF7F4 !important;
        border: 1.5px solid #F0E5D8 !important;
        border-radius: 12px !important;
        color: #4A3E3D !important;
    }
    
    /* 스트림릿 기본 체크박스 핑크색 강조 */
    div[data-testid="stCheckbox"] label span {
        border-color: #E8A0A2 !important;
    }
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + label span {
        background-color: #E8A0A2 !important;
        border-color: #E8A0A2 !important;
    }
    
    /* Primary 추가 버튼 (핑크색 적용) */
    button[kind="primary"] {
        background-color: #E8A0A2 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(232, 160, 162, 0.2) !important;
    }
    button[kind="primary"]:hover {
        background-color: #DB8B8D !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(232, 160, 162, 0.35) !important;
    }
    
    /* Secondary 일반 버튼 (회색/필터) */
    button[kind="secondary"] {
        background-color: #FAF7F4 !important;
        color: #9E8E8D !important;
        border: 1.5px solid #F0E5D8 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[kind="secondary"]:hover {
        color: #4A3E3D !important;
        border-color: #E8A0A2 !important;
        background-color: #FCEAEA !important;
    }
    
    /* 체크박스 정렬 보정 */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 유효성 검사 에러 피드백 */
    .form-feedback-active {
        font-size: 0.8rem;
        color: #D67274;
        font-weight: 500;
        margin-top: 0.25rem;
        padding-left: 0.25rem;
        animation: shake 0.4s ease;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-6px); }
        40%, 80% { transform: translateX(6px); }
    }
    
    /* 불필요한 기본 스트림릿 요소들 제거 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- UI 렌더링 시작 -----------------

# 타이틀 부분
st.markdown("<h1 style='text-align: center; font-size: 2.25rem; font-weight: 700; margin-bottom: 0.2rem;'>Daily Vibe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9E8E8D; font-size: 0.9rem; margin-bottom: 2rem;'>오늘의 계획을 감성적으로 기록하고 관리하세요.</p>", unsafe_allow_html=True)

# 1. 할 일 추가 폼 (st.form을 사용하여 Enter 키 추가 대응)
with st.form("todo_form", clear_on_submit=True):
    todo_text = st.text_input(
        "새로운 할 일을 적어보세요...", 
        placeholder="새로운 할 일을 적어보세요...",
        label_visibility="collapsed"
    )
    
    # 세부 옵션들 한 행에 배치
    col_sel, col_date, col_btn = st.columns([1.5, 1.5, 1])
    with col_sel:
        category = st.selectbox(
            "카테고리 선택", 
            ["🏠 일상", "💼 업무", "🛒 쇼핑", "✨ 기타"], 
            label_visibility="collapsed"
        )
    with col_date:
        due_date = st.date_input(
            "마감일 선택", 
            value=datetime.date.today(), 
            label_visibility="collapsed"
        )
    with col_btn:
        submit = st.form_submit_button("추가", use_container_width=True, type="primary")

# 폼 제출 시 비즈니스 로직 처리
if submit:
    if not todo_text.strip():
        st.session_state.validation_error = True
    else:
        st.session_state.validation_error = False
        new_todo = {
            "id": str(int(datetime.datetime.now().timestamp() * 1000)),
            "text": todo_text.strip(),
            "category": category,
            "dueDate": str(due_date),
            "completed": False
        }
        st.session_state.todos.insert(0, new_todo)
        save_todos(st.session_state.todos)
        st.rerun()

# 유효성 검사 에러 노출
if st.session_state.validation_error:
    st.markdown("<div class='form-feedback-active'>할 일을 입력해주세요!</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# 2. 필터 버튼 탭 구성
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    if st.button("전체", key="filter_all", use_container_width=True, type="primary" if st.session_state.current_filter == "all" else "secondary"):
        st.session_state.current_filter = "all"
        st.rerun()
with f_col2:
    if st.button("진행 중", key="filter_active", use_container_width=True, type="primary" if st.session_state.current_filter == "active" else "secondary"):
        st.session_state.current_filter = "active"
        st.rerun()
with f_col3:
    if st.button("완료", key="filter_completed", use_container_width=True, type="primary" if st.session_state.current_filter == "completed" else "secondary"):
        st.session_state.current_filter = "completed"
        st.rerun()

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# 3. 필터 처리된 할 일 리스트 렌더링
filtered_todos = st.session_state.todos
if st.session_state.current_filter == "active":
    filtered_todos = [t for t in st.session_state.todos if not t["completed"]]
elif st.session_state.current_filter == "completed":
    filtered_todos = [t for t in st.session_state.todos if t["completed"]]

if not filtered_todos:
    st.markdown("<p style='text-align: center; color: #9E8E8D; font-size: 0.9rem; padding: 2rem 0;'>등록된 할 일이 없습니다.</p>", unsafe_allow_html=True)
else:
    for todo in filtered_todos:
        # 각 행마다 고유 열 생성 (체크박스, 내용, 삭제)
        col_check, col_content, col_del = st.columns([0.1, 0.75, 0.15])
        
        with col_check:
            st.checkbox(
                "", 
                value=todo["completed"], 
                key=f"check_{todo['id']}", 
                on_change=toggle_todo, 
                args=(todo["id"],),
                label_visibility="collapsed"
            )
            
        with col_content:
            completed_class = "completed" if todo["completed"] else ""
            badge_html = f'<span class="todo-category-badge {completed_class}">{todo["category"]}</span>'
            text_html = f'<span class="todo-text {completed_class}">{todo["text"]}</span>'
            
            dday_info = calculate_dday(todo["dueDate"], todo["completed"])
            date_html = ""
            if dday_info:
                overdue_class = "overdue" if dday_info["is_overdue"] else ""
                date_html = f'<span class="todo-date-badge {overdue_class}">{dday_info["text"]}</span>'
                
            st.markdown(f'<div class="todo-item-content">{badge_html} {text_html} {date_html}</div>', unsafe_allow_html=True)
            
        with col_del:
            if st.button("🗑️", key=f"del_{todo['id']}", help="할 일 삭제"):
                delete_todo(todo["id"])
                st.rerun()

st.markdown("<hr style='border-color: #F0E5D8; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# 4. 푸터 상태 정보 및 완료 항목 삭제
col_count, col_clear = st.columns([1.2, 1])
with col_count:
    active_count = len([t for t in st.session_state.todos if not t["completed"]])
    st.markdown(f"남은 할 일: **{active_count}**개")

with col_clear:
    completed_count = len([t for t in st.session_state.todos if t["completed"]])
    if completed_count > 0:
        if st.button("완료 항목 삭제", key="clear_completed", use_container_width=True):
            # 완료된 키들 세션 상태에서 정리
            for t in st.session_state.todos:
                if t["completed"]:
                    if f"check_{t['id']}" in st.session_state:
                        del st.session_state[f"check_{t['id']}"]
            # 리스트 갱신
            st.session_state.todos = [t for t in st.session_state.todos if not t["completed"]]
            save_todos(st.session_state.todos)
            st.rerun()
