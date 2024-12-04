import pandas as pd
from bs4 import BeautifulSoup
import os
import zipfile
from tkinter import Tk, filedialog
import tempfile

def get_next_versioned_filename(base_name, ext):
    """
    버전 번호가 붙은 파일 이름을 생성합니다.
    """
    v = 1
    while True:
        file_name = f"{base_name}_V{v}{ext}"
        if not os.path.exists(file_name):
            return file_name
        v += 1

def extract_usernames_from_html(html_content):
    """
    HTML 파일에서 사용자 이름을 추출하는 함수.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    usernames = [tag.text.strip() for tag in soup.find_all('a')]

    # 중간 결과 확인
    print(f"Extracted {len(usernames)} usernames")
    return usernames

def select_file(title):
    """
    파일 선택 다이얼로그 설정 함수.
    """
    root = Tk()
    root.withdraw()  # Tkinter 윈도우 숨기기
    filepath = filedialog.askopenfilename(title=title, filetypes=[("ZIP files", "*.zip"), ("HTML files", "*.html")])
    return filepath

def extract_html_from_zip(zip_path, file_name):
    """
    ZIP 파일에서 지정된 파일을 추출하여 그 내용물을 반환하는 함수.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(file_name) as file:
            return file.read()

# ZIP 파일 또는 HTML 파일 선택
zip_file = select_file("ZIP 파일을 선택하세요")

if zip_file.endswith('.zip'):
    # ZIP 파일에서 followers_1.html과 following.html을 추출
    followers_content = extract_html_from_zip(zip_file, 'connections/followers_and_following/followers_1.html')
    following_content = extract_html_from_zip(zip_file, 'connections/followers_and_following/following.html')


# followers와 following 사용자 이름 추출
followers = extract_usernames_from_html(followers_content)
following = extract_usernames_from_html(following_content)

# 팔로우 중이지만 팔로워가 아닌 계정을 찾기
not_following_back = [user for user in following if user not in followers]

# 결과 확인을 위한 출력
print(f"Total followers: {len(followers)}")
print(f"Total following: {len(following)}")
print(f"Not following back: {len(not_following_back)}")

# 현재 작업 디렉토리에서 엑셀 파일 저장 경로 생성
current_dir = os.getcwd()
output_file = get_next_versioned_filename("맞팔하지 않은 계정", ".xlsx")
output_file = os.path.join(current_dir, output_file)

# 결과를 새로운 엑셀 파일로 저장
df = pd.DataFrame(not_following_back, columns=["맞팔 안한 계정"])
df.to_excel(output_file, index=False)

print(f"나를 팔로우하지 않는 계정 리스트가 '{output_file}' 파일에 저장되었습니다.")
