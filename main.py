# pip install matplotlib 를 명령프롬프트에 입력하여 설치 -> 그래프 보기

# pip install speechrecognition
# pip install pyaudio  # 설치 오류 시 → pip install pipwin && pipwin install pyaudio
# pip install matplotlib
# 위의 세개를 명령프롬프트에 입력하여 설치 -> 음성 인식

## 지출 관리 프로그램
# 지출 추가
# 전체 기록 보기
# 총 지출 확인
# 지출 삭제
# 지출 수정
# 연간 지출 비교
# 지출 검색
# 지출 그래프 보기
# 음성으로 지출 추가

# 지출 관리 프로그램을 보면 음성으로 인식해서 자동으로 입력되게 하는 것을 

import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import speech_recognition as sr
import re

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())

DATA_FILE = "spend_data.csv"

def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["날짜", "항목", "금액"])

def add_expense():
    while True:
        date = input("날짜 (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️ 날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.")
    item = input("항목명: ").strip()
    while True:
        amount = input("금액: ").strip()
        if amount.isdigit():
            break
        else:
            print("⚠️ 숫자만 입력해주세요.")
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, item, amount])
    print("저장되었습니다.\n")

def show_all():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return

    # 연도와 월 입력받기 (엔터 시 전체보기)
    ym_input = input("조회할 연도와 월 입력 (예: 2025-06, 전체보기는 엔터): ").strip()

    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    # 필터링: 입력한 연-월이 있으면 해당 데이터만 필터, 없으면 전체
    if ym_input:
        # 형식 체크 (YYYY-MM)
        if not re.match(r"^\d{4}-\d{2}$", ym_input):
            print("⚠️ 형식이 올바르지 않습니다. YYYY-MM 형식으로 입력해주세요.\n")
            return
        filtered_rows = [row for row in rows if row[0].startswith(ym_input)]
        if not filtered_rows:
            print(f"{ym_input}에 해당하는 기록이 없습니다.\n")
            return
    else:
        filtered_rows = rows

    # 날짜 내림차순 정렬 (YYYY-MM-DD 형식이므로 문자열 내림차순 가능)
    filtered_rows.sort(key=lambda x: x[0], reverse=True)

    print(f"{ym_input if ym_input else '전체'} 지출 내역 :")
    for row in filtered_rows:
        print(f"- {row[0]} | {row[1]} | {row[2]}원")
    print()


def total_spent():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return
    total = 0
    category_totals = {}
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                amount = int(row[2])
            except:
                continue
            total += amount
            category = row[1]
            category_totals[category] = category_totals.get(category, 0) + amount
    print(f"총 지출: {total}원")
    print("항목별 지출:")
    for category, amt in category_totals.items():
        print(f"- {category}: {amt}원")
    print()

def delete_expense():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return
    date = input("삭제할 지출 날짜 (YYYY-MM-DD): ").strip()
    item = input("삭제할 항목명: ").strip()
    rows, deleted = [], False
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == date and row[1] == item:
                deleted = True
                continue
            rows.append(row)
    if deleted:
        confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()
        if confirm != 'y':
            print("삭제 취소.\n")
            return
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print("삭제 완료.\n")
    else:
        print("해당 지출을 찾을 수 없습니다.\n")

def edit_expense():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return
    date = input("수정할 지출 날짜 (YYYY-MM-DD): ").strip()
    item = input("수정할 항목명: ").strip()
    rows, edited = [], False
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == date and row[1] == item:
                print(f"기존 기록: 날짜={row[0]}, 항목={row[1]}, 금액={row[2]}원")
                while True:
                    new_date = input("새 날짜 (엔터=변경 없음): ").strip()
                    if new_date == "":
                        new_date = row[0]
                        break
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("날짜 형식 오류.")
                new_item = input("새 항목명 (엔터=변경 없음): ").strip()
                while True:
                    new_amount = input("새 금액 (엔터=변경 없음): ").strip()
                    if new_amount == "" or new_amount.isdigit():
                        break
                    else:
                        print("숫자만 입력해주세요.")
                rows.append([new_date, new_item if new_item else row[1], new_amount if new_amount else row[2]])
                edited = True
            else:
                rows.append(row)
    if edited:
        confirm = input("정말 수정하시겠습니까? (y/n): ").strip().lower()
        if confirm != 'y':
            print("수정 취소.\n")
            return
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print("수정 완료.\n")
    else:
        print("해당 지출을 찾을 수 없습니다.\n")

def annual_comparison():
    if not os.path.exists(DATA_FILE):
        print("기록 없음.\n")
        return
    year_totals = {}
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                year = datetime.strptime(row[0], "%Y-%m-%d").year
                amount = int(row[2])
            except:
                continue
            year_totals[year] = year_totals.get(year, 0) + amount
    print("연간 지출:")
    for year in sorted(year_totals.keys()):
        print(f"- {year}년: {year_totals[year]}원")
    print()

def search_expenses():
    if not os.path.exists(DATA_FILE):
        print("기록 없음.\n")
        return
    keyword = input("검색어 (항목명 또는 날짜 일부): ").strip()
    results = []
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if keyword in row[0] or keyword in row[1]:
                results.append(row)
    if results:
        print(f"'{keyword}' 검색 결과:")
        for row in results:
            print(f"- {row[0]} | {row[1]} | {row[2]}원")
    else:
        print("해당 결과 없음.\n")
    print()

def show_graph():
    if not os.path.exists(DATA_FILE):
        print("기록 없음.\n")
        return
    
    year_month_totals = {}
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                dt = datetime.strptime(row[0], "%Y-%m-%d")
                amount = int(row[2].replace(",", ""))
                ym = f"{dt.year}년 {dt.month}월"
                year_month_totals[ym] = year_month_totals.get(ym, 0) + amount
            except:
                continue
    
    if not year_month_totals:
        print("시각화할 데이터 없음.\n")
        return

    year_totals = {}
    year_counts = {}
    for ym, total in year_month_totals.items():
        year = ym.split("년")[0]
        year_totals[year] = year_totals.get(year, 0) + total
        year_counts[year] = year_counts.get(year, 0) + 1
    year_averages = {year: year_totals[year]/year_counts[year] for year in year_totals}

    sorted_keys = sorted(year_month_totals.keys(), key=lambda x: (int(x.split("년")[0]), int(x.split()[1].replace("월",""))))

    values = [year_month_totals[k] for k in sorted_keys]

    plt.figure(figsize=(12, 7))
    bars = plt.barh(sorted_keys, values, color='skyblue')

    plt.xlabel("지출 금액 (원)")
    plt.title("연도별 월별 지출 내역 및 연평균 표시")
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    years = sorted(year_averages.keys())
    for year in years:
        ys = [i for i, label in enumerate(sorted_keys) if label.startswith(year)]
        if not ys:
            continue
        avg = year_averages[year]
        plt.hlines(y=(ys[0] + ys[-1]) / 2, xmin=0, xmax=avg, colors='red', linestyles='dashed', label=f"{year}년 평균 {int(avg):,}원")

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.tight_layout()
    plt.show()

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ 말씀해주세요 (예: '2025년 6월 5일 커피 3000원')...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="ko-KR")
        print(f"📝 인식된 문장: {text}")
        return text
    except sr.UnknownValueError:
        print("⚠️ 음성을 이해하지 못했습니다.")
    except sr.RequestError:
        print("⚠️ Google 음성 인식 서비스 연결 실패.")
    return None

def parse_voice_input(text):
    date_match = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text)
    if not date_match:
        print("⚠️ 날짜 인식 실패")
        return None
    year, month, day = date_match.groups()
    date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    remaining_text = re.sub(r"\d{4}년\s*\d{1,2}월\s*\d{1,2}일", "", text)
    item_match = re.search(r"([가-힣\s]+?)\s*(\d{1,3}(?:,\d{3})*|\d+)\s*원", remaining_text)
    if item_match:
        item = item_match.group(1).strip()
        amount = item_match.group(2).replace(",", "").strip()
        return date, item, amount
    else:
        print("⚠️ 항목 또는 금액 인식 실패")
        return None

def voice_expense_entry():
    speech = recognize_speech()
    if speech:
        parsed = parse_voice_input(speech)
        if parsed:
            date, item, amount = parsed
            print(f"추출된 정보 → 날짜: {date}, 항목: {item}, 금액: {amount}원")
            with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([date, item, amount])
            print("✅ 음성 입력으로 저장 완료!\n")
        else:
            print("⚠️ 음성에서 날짜/항목/금액을 인식하지 못했습니다.\n")

def analyze_patterns():
    if not os.path.exists(DATA_FILE):
        print("기록이 없습니다.\n")
        return
    
    category_totals = {}
    category_counts = {}
    monthly_totals = {}
    monthly_counts = {}

    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                date_obj = datetime.strptime(row[0], "%Y-%m-%d")
                amount = int(row[2])
                category = row[1]
            except:
                continue
            
            # 항목별 합계 및 횟수
            category_totals[category] = category_totals.get(category, 0) + amount
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # 월별 합계 및 횟수 (YYYY-MM)
            ym = date_obj.strftime("%Y-%m")
            monthly_totals[ym] = monthly_totals.get(ym, 0) + amount
            monthly_counts[ym] = monthly_counts.get(ym, 0) + 1
    
    print("=== 항목별 지출 패턴 분석 ===")
    for cat in category_totals:
        avg = category_totals[cat] / category_counts[cat]
        print(f"- {cat}: 총 {category_totals[cat]}원, {category_counts[cat]}회, 평균 {avg:.0f}원")
    print()
    
    print("=== 월별 지출 패턴 분석 ===")
    sorted_months = sorted(monthly_totals.keys())
    for ym in sorted_months:
        avg = monthly_totals[ym] / monthly_counts[ym]
        print(f"- {ym}: 총 {monthly_totals[ym]}원, {monthly_counts[ym]}회, 평균 {avg:.0f}원")
    print()
    
    # 월별 평균 지출 시각화
    months = sorted_months
    averages = [monthly_totals[m] / monthly_counts[m] for m in months]
    
    plt.figure(figsize=(10,5))
    plt.plot(months, averages, marker='o', linestyle='-', color='purple')
    plt.title("월별 평균 지출 패턴")
    plt.xlabel("월")
    plt.ylabel("평균 지출액 (원)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def menu():
    print("""
==지출 관리 프로그램==
1. 지출 추가
2. 전체 보기
3. 총 지출 및 항목별 합계
4. 지출 삭제
5. 지출 수정
6. 연간 지출 비교
7. 지출 검색
8. 지출 그래프 보기
9. 음성으로 지출 입력
10. 지출 패턴 분석
11. 종료
""")

def main():
    init_file()
    while True:
        menu()
        choice = input("메뉴 선택: ").strip()
        if choice == '1':
            add_expense()
        elif choice == '2':
            show_all()
        elif choice == '3':
            total_spent()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            edit_expense()
        elif choice == '6':
            annual_comparison()
        elif choice == '7':
            search_expenses()
        elif choice == '8':
            show_graph()
        elif choice == '9':
            voice_expense_entry()
        elif choice == '10':
            analyze_patterns()
        elif choice == '11':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.\n")

if __name__ == "__main__":
    main()
