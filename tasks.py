import json
from datetime import date

# === 파일 관련 ===
def get_file_name():
    return f"{date.today()}_checklists.json"

def load_template():
    try:
        with open("template.json", "r") as f:
            return json.load(f)  # ["운동하기", "공부하기", ...] 반환
    except FileNotFoundError:
        return ["운동하기", "공부하기", "책 읽기"]

def load_tasks():
    template = load_template()  # 문자열 리스트
    
    try:
        with open(get_file_name(), "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []
    
    # 기존 description 목록
    existing_names = [task["description"] for task in existing]
    
    # 템플릿에 있는데 기존에 없으면 추가
    for name in template:  # name은 문자열
        if name not in existing_names:
            existing.append({"description": name, "completed": False})
    
    return existing

def save_tasks(tasks):
    with open(get_file_name(), "w") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# === 화면 출력 ===
def show_tasks(tasks):
    print(f"\n📅 {date.today()} 체크리스트")
    print("-" * 30)
    for i, task in enumerate(tasks):
        status = "✅" if task["completed"] else "⬜"
        print(f"{status} {i + 1}. {task['description']}")

# === 사용자 입력 ===
def get_user_choice(max_num):
    while True:
        choice = input("\n번호 선택 (q=종료): ").strip()
        
        if choice == "q":
            return None
        
        try:
            num = int(choice)
            if 1 <= num <= max_num:
                return num - 1
            else:
                print(f"⚠️ 1~{max_num} 사이 숫자를 입력하세요.")
        except ValueError:
            print("⚠️ 숫자 또는 q를 입력하세요.")

def toggle_task(tasks, index):
    tasks[index]["completed"] = not tasks[index]["completed"]

# === 메인 ===
def main():
    tasks = load_tasks()
    save_tasks(tasks)
    
    while True:
        show_tasks(tasks)
        index = get_user_choice(len(tasks))
        
        if index is None:
            break
        
        toggle_task(tasks, index)
        save_tasks(tasks)
    
    print("👋 저장 완료!")

main()
