import requests
import json
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm 
import os

all_data = []

def get_info(soup_subject):
    subject_name1 = soup_subject.find("th", string="授業科目")
    subject_name2 = subject_name1.find_next_sibling('td') if subject_name1 else None
    Target_Year1 = soup_subject.find("th", string="対象学年")
    Target_Year2 = Target_Year1.find_next_sibling('td') if Target_Year1 else None
    Credits = soup_subject.find("th", string="単位の種別と単位数")
    Credits2 = Credits.find_next_sibling('td') if Credits else None
    Instructor1 = soup_subject.find("th", string="担当教員")
    Instructor2 = Instructor1.find_next_sibling('td') if Instructor1 else None
    Textbook1 = soup_subject.find("th", string="教科書/教材")
    Textbook2 = Textbook1.find_next_sibling('td') if Textbook1 else None
    Course_Format1 = soup_subject.find("th", string="授業形態")
    Course_Format2 = Course_Format1.find_next_sibling('td') if Course_Format1 else None
    Course_Time1 = soup_subject.find("th", string="週時間数")
    Course_Time2 = Course_Time1.find_next_sibling('td') if Course_Time1 else None
    important_point1 = soup_subject.find("th", string="注意点")
    important_point2 = important_point1.find_next_sibling('td') if important_point1 else None
    Evaluation_Method1 = soup_subject.find("th", string="総合評価割合")
    Evaluation_Method2 = Evaluation_Method1.find_next_siblings('td') if Evaluation_Method1 else []

    subject_data = {
        "授業科目": subject_name2.text.strip() if subject_name2 else "N/A",
        "対象学年": Target_Year2.text.strip() if Target_Year2 else "N/A",
        "単位の種別と単位数": Credits2.text.strip() if Credits2 else "N/A",
        "担当教員": Instructor2.text.strip() if Instructor2 else "N/A",
        "教科書/教材": Textbook2.text.strip() if Textbook2 else "N/A",
        "授業形態": Course_Format2.text.strip() if Course_Format2 else "N/A",
        "週時間数": Course_Time2.text.strip() if Course_Time2 else "N/A",
        "注意点": important_point2.text.strip() if important_point2 else "N/A",
        "総合評価割合": [evaluation.text.strip() for evaluation in Evaluation_Method2]
    }

    all_data.append(subject_data)

headers = {  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

print("各高専のコードを入力してください :(ex : 01)")
school_code = input()
school_url = "https://syllabus.kosen-k.go.jp/Pages/PublicDepartments?school_id="+school_code+"&lang=ja"
response_school = requests.get(school_url,headers=headers)
soup_school = BeautifulSoup(response_school.content, 'html.parser')
department_list = soup_school.find_all("h4")
department_id = soup_school.find_all("a",string="本年度の開講科目一覧")

i = 0
for department in department_list:
    print(str(i)+" : "+department.text)
    i += 1
print("科目の番号を入力してください")
department_number = input()
print(department_list[int(department_number)].text + "を選択しました")
department_id = "https://syllabus.kosen-k.go.jp" + department_id[int(department_number)].get("href")
response_department = requests.get(department_id,headers=headers)
soup_department = BeautifulSoup(response_department.content, 'html.parser')
subject_list = soup_department.find_all("a",class_="mcc-show")

for n, subject in enumerate(tqdm(subject_list, desc="進捗状況", unit="科目"), start=1):
    subject_url = "https://syllabus.kosen-k.go.jp" + subject.get("href")
    response_subject = requests.get(subject_url,headers=headers)
    soup_subject = BeautifulSoup(response_subject.content, 'html.parser')
    get_info(soup_subject)
    
    sleep(1)

with open("all_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("データの保存が完了しました")
