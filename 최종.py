from selenium import webdriver
import time
import openpyxl
import pandas as pd

# 최초 장소 목록 11가지
place_list = ["가로수길", "망원동", "서촌", "성수동", "송리단길", "쌍리단길", "연남동", "을지로", "익선동", "합정", "후암동"]

# 0. 선호 조사
# 음식 조사
food = input("먹을 음식을 입력해주세요(최대한 구체적으로 ex) 사케동, 돼지고기구이맛집, 즉석떡볶이: ")
food_price = float(input("음식의 최대 가격대를 입력해주세요(ex. 20000): "))
review_stand = float(input("최소 리뷰 수를 입력해주세요(ex. 200): "))
print("-"*130)

# 카페 조사
cafe = input("가고 싶은 카페 종류를 입력해주세요(ex. 디저트) : ")
review_stand2 = float(input("최소 리뷰 수를 입력해주세요(ex. 200): "))
print("-"*130)

# 술집 조사
drink_data = pd.read_csv('./술집_데이터.csv')
print("원하는 음주 종류를 아래에서 선택해주세요(번호만 ex. 3)")
print("0. 안 마신다, ", "1. 맥주,호프, ", "2. 바(BAR), ", "3. 와인, ", "4. 요리주점, ", "5. 이자카야, ", "6. 전통,민속주점, ", "7. 포장마차")
drink = input()
drink_list = ["맥주,호프", "바(BAR)", "와인", "요리주점", "이자카야", "전통,민속주점", "포장마차"]
print("-"*130)

# 할 것들 조사
activity_data = pd.read_csv('./활동_데이터.csv')
print("원하는 활동 번호를 아래에서 선택해주세요(반드시 번호로 택1)")
print("1. 실내(VR, 방탈출, 오락실, 보드카페), ", "2. 실내 활동적(볼링, 테마), ", "3. 전시회, 박물관, 미술관, ",
      "4. 영화관, 극장, 공연,\n", "5. 산책(한강, 공원, 전망대), ", "6. 공방, 체험, ", "7. 쇼핑, ", "8. 거리")
activity = input()
activity_list = ["실내(VR, 방탈출, 오락실, 보드카페)", "실내 활동적(볼링, 테마)", "전시회, 박물관, 미술관",
      "영화관, 극장, 공연", "산책(한강, 공원, 전망대)", "공방, 체험", "쇼핑", "거리"]

print("조건에 맞는 조사를 시작합니다.")
time.sleep(2)



## 1. 활동으로 1차 필터링 & 리스트업
activity = activity_list[int(activity)-1]
activity_summary = pd.DataFrame(columns=["권역", "장소명", "장소 세부"])

for i in range(len(place_list)):
    activity_temp = pd.DataFrame(columns=["권역", "장소명", "요약", "장소 세부"])
    activity_temp = activity_data[(activity_data['권역'] == place_list[i]) & (activity_data['요약'] == activity)]
    activity_temp = activity_temp[['권역', '장소명', '장소 세부']]

    try:
        activity_summary = pd.concat([activity_summary, activity_temp])
    except:
        continue

print("-"*130)
print(activity, " 권역 별 리스트업")
print(activity_summary)
time.sleep(2)

# 포함되지 않은 권역은 제거
for ll in range(len(place_list)-1, -1, -1):
    if place_list[ll] not in activity_summary['권역'].tolist():
        del place_list[ll]

print("활동 조사가 종료되었습니다.")
print("포함된 권역 수는 :", len(place_list), "개")
print(place_list)
print("-"*130)
time.sleep(2)
print("술집 조사를 시작합니다.")
time.sleep(2)


## 2. 술집으로 필터링 및 리스트업(술은 안 먹는다 하면 필터링, 리스트업 둘 다 안 됨)
if drink == "0":
    print("술 안 마셔요.")

else:
    drink = drink_list[int(drink)-1]

    drink_summary = pd.DataFrame(columns=["권역", "가게명", "음주 종류", "리뷰 수", "가격대"])
    for i in range(len(place_list)):
        drink_temp = pd.DataFrame(columns=["권역", "가게명", "음주 종류", "리뷰 수", "가격대"])
        drink_temp = drink_data[(drink_data['권역'] == place_list[i]) & (drink_data['음주 종류'] == drink)
                                & (drink_data['리뷰 수'] > 0)]

        # 권역 별로 리뷰 TOP 5까지 출력
        drink_temp_sort = drink_temp.sort_values(by='리뷰 수', ascending=False)
        try:
            drink_summary = pd.concat([drink_summary, drink_temp_sort.head(3)])
        except:
            try:
                drink_summary = pd.concat([drink_summary, drink_temp_sort.head(2)])
            except:
                try:
                    drink_summary = pd.concat([drink_summary, drink_temp_sort.head(1)])
                except:
                    continue

    print("-" * 130)
    print("권역 별 TOP3", drink)
    print(drink_summary)
    time.sleep(2)

    for ll in range(len(place_list) - 1, -1, -1):
          if place_list[ll] not in drink_summary['권역'].tolist():
                del place_list[ll]

print("술집 조사가 종료되었습니다.")
print("포함된 권역 수는 :", len(place_list), "개")
print(place_list)
print("-"*130)
time.sleep(2)
print("식당 조사를 시작합니다.")
time.sleep(2)



## 3. 식당으로 필터링 & 리스트업
food_summary = pd.DataFrame(columns=["권역", "가게명", "리뷰 수", "가격대", "점수"])
for p in range(len(place_list)):

    # 1. 홈페이지 접속
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://store.naver.com/restaurants/list?filterId=s1586516490&page=1&query="+place_list[p]+"%20"+food)
    time.sleep(1)
    food_temp = pd.DataFrame(columns=["권역", "가게명", "리뷰 수", "가격대", "점수"])

    # 3페이지까지 관련도 순으로 수집
    for i in range(0,3):
        # 시간 지연
        time.sleep(5)

        # 컨테이너(가게) 데이터 수집 // div.list_item_inner
        stores = driver.find_elements_by_css_selector("div.list_item_inner")

        for s in stores:
            # 가게 이름 데이터 수집 // span.tit_inner a span
            title = s.find_element_by_css_selector("span.tit_inner a span").text


            # 가게 리뷰 개수 수집 // div.etc_area.ellp span.item:nth-of-type(1)
            try:
                review = s.find_element_by_css_selector("div.etc_area.ellp span.item:nth-of-type(1)").text[3:]
                if len(review) > 3:
                    review = int(review.replace(",",""))
                else:
                    review = int(review)
            except:
                review = 0

            # 가격대 수집 // div.etc_area.ellp span.item:nth-of-type(2)
            try:
                price = int(s.find_element_by_css_selector("div.etc_area.ellp span.item:nth-of-type(2)").text[0:-9]) * 10000
            except:
                price = 0


            # # 식당 가산점은 일단 review*100 + ((원하는 가격대*2) - 가격대)
            # if (review >= review_stand):
            #     if (price == 0):
            #         print([(i + 1), "페이지", place_list[p], title, review, price, (review * 100 + (food_price/2))])
            #         food_temp.loc[len(food_temp)] = [place_list[p], title, review, price, (review * 100 + (food_price/2))]
            #     else:
            #         print([(i + 1), "페이지", place_list[p], title, review, price, (review * 100 + (food_price/2))])
            #         food_temp.loc[len(food_temp)] = [place_list[p], title, review, price, (review * 100 + (food_price/2))]
            # else:
            #     continue

                # 식당 가산점은 일단 review*100 + ((원하는 가격대*2) - 가격대)
                if (review >= review_stand):
                    if (price == 0):
                        print([(i + 1), "페이지", place_list[p], title, review, price,
                               (review * 100 + (food_price / 2))])
                        food_temp.loc[len(food_temp)] = [place_list[p], title, review, price, (review * 100 + (food_price / 2))]
                    else:
                        print([(i + 1), "페이지", place_list[p], title, review, price, (review * 100 + ((2 * food_price) - price))])
                        food_temp.loc[len(food_temp)] = [place_list[p], title, review, price, (review * 100 + ((2 * food_price) - price))]

        # 다음페이지 버튼 클릭 하기
        if (i + 1) % 5 != 0:
            try:
                disa = driver.find_element_by_css_selector("a.btn_direction.btn_next.disabled")
                nextpage = driver.find_element_by_css_selector("div.pagination a:nth-of-type(" + str((i % 5) + 3) + ")")
                if disa == nextpage:
                    print("데이터 수집 완료.")
                    break
                else:
                    nextpage.click()
            except:
                try:
                    nextpage = driver.find_element_by_css_selector(
                        "div.pagination a:nth-of-type(" + str((i % 5) + 3) + ")")
                    nextpage.click()
                except:
                    print("데이터 수집 완료.")
                    break
        else:
            try:
                nextpage = driver.find_element_by_css_selector("a.btn_direction.btn_next.disabled")
                nextpage.click()
                print("데이터 수집 완료.")
                break
            except:
                nextpage = driver.find_element_by_css_selector("a.btn_direction.btn_next")
                nextpage.click()

    # 권역 별로 점수 순으로 정렬
    food_temp_sort = food_temp.sort_values(by='점수', ascending=False)
    try:
        food_summary = pd.concat([food_summary, food_temp_sort.head(3)])
    except:
        try:
            food_summary = pd.concat([food_summary, food_temp_sort.head(2)])
        except:
            try:
                food_summary = pd.concat([food_summary, food_temp_sort.head(1)])
            except:
                continue
    print(food_summary)
    driver.close()
    time.sleep(1)

print("-"*130)
print(food, " 권역 별 TOP3 식당")
print(food_summary)
time.sleep(2)

for ll in range(len(place_list)-1, -1, -1):
    if place_list[ll] not in food_summary['권역'].tolist():
        del place_list[ll]

print("식당 조사가 종료되었습니다.")
print("포함된 권역 수는 :", len(place_list), "개")
print(place_list)
print("-"*130)
time.sleep(2)
print("카페 조사를 시작합니다.")
time.sleep(2)



# 4. 카페 리스트업(카페는 권역 필터링에 관여하지 않고, 리스트업만 됨)
cafe_summary = pd.DataFrame(columns=["권역", "가게명", "리뷰 수"])
for p in range(len(place_list)):

    # 1. 홈페이지 접속
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://store.naver.com/restaurants/list?filterId=s1586516490&page=1&query="+place_list[p]+"%20"+cafe)
    time.sleep(1)
    cafe_temp = pd.DataFrame(columns=["권역", "가게명", "리뷰 수"])

    for i in range(0,3):
        # 시간 지연
        time.sleep(5)

        # 컨테이너(가게) 데이터 수집 // div.list_item_inner
        stores = driver.find_elements_by_css_selector("div.list_item_inner")

        for s in stores:
            # 가게 이름 데이터 수집 // span.tit_inner a span
            title = s.find_element_by_css_selector("span.tit_inner a span").text

            # 가게 종류 데이터 수집 // span.category
            try:
                food_type = s.find_element_by_css_selector("span.category").text
            except:
                food_type = "-"
            # 가게 리뷰 개수 수집 // div.etc_area.ellp span.item:nth-of-type(1)
            try:
                review = s.find_element_by_css_selector("div.etc_area.ellp span.item:nth-of-type(1)").text[3:]
                if len(review) > 3:
                    review = int(review.replace(",",""))
                else:
                    review = int(review)
            except:
                review = 0

            if (review >= review_stand2):
                    print([(i+1),"페이지",place_list[p], title, review])
                    cafe_temp.loc[len(cafe_temp)] = [place_list[p], title, review]
            else:
                continue

        # 다음페이지 버튼 클릭 하기
        if (i + 1) % 5 != 0:
            try:
                disa = driver.find_element_by_css_selector("a.btn_direction.btn_next.disabled")
                nextpage = driver.find_element_by_css_selector("div.pagination a:nth-of-type(" + str((i % 5) + 3) + ")")
                if disa == nextpage:
                    print("데이터 수집 완료.")
                    break
                else:
                    nextpage.click()
            except:
                try:
                    nextpage = driver.find_element_by_css_selector(
                        "div.pagination a:nth-of-type(" + str((i % 5) + 3) + ")")
                    nextpage.click()
                except:
                    print("데이터 수집 완료.")
                    break
        else:
            try:
                nextpage = driver.find_element_by_css_selector("a.btn_direction.btn_next.disabled")
                nextpage.click()
                print("데이터 수집 완료.")
                break
            except:
                nextpage = driver.find_element_by_css_selector("a.btn_direction.btn_next")
                nextpage.click()

    # 권역 별로 리뷰 TOP 5까지 출력
    cafe_temp_sort = cafe_temp.sort_values(by='리뷰 수', ascending=False)

    try:
        cafe_summary = pd.concat([cafe_summary, cafe_temp_sort.head(5)])
    except:
        try:
            cafe_summary = pd.concat([cafe_summary, cafe_temp_sort.head(4)])
        except:
            try:
                cafe_summary = pd.concat([cafe_summary, cafe_temp_sort.head(3)])
            except:
                try:
                    cafe_summary = pd.concat([cafe_summary, cafe_temp_sort.head(2)])
                except:
                    try:
                        cafe_summary = pd.concat([cafe_summary, cafe_temp_sort.head(1)])
                    except:
                        continue
    print(cafe_summary)
    driver.close()
    time.sleep(1)

print("-"*130)
print("권역 별 TOP3", cafe)
print(cafe_summary)
time.sleep(2)

print("포함된 권역 수는 :", len(place_list), "개")
print(place_list)
print("조사가 종료되었습니다.")
print("-"*130)
time.sleep(2)
print("엑셀에 출력합니다.")
print("-"*130)

## 5. 엑셀에 옮기기
wb = openpyxl.Workbook()
wb.save('뭐하고놀까.xlsx')
sheet = wb.active
sheet.append(["▶▶▶ 권역 별로 시트를 이동하면서 확인하세요 ▶▶▶"])

for i in range(len(place_list)):
    sheet = wb.create_sheet(place_list[i])
    sheet.append(["("+food+")"+"식당"])
    sheet.append(["가게명", "리뷰 수", "가격대", "점수"])
    for t in range(len(food_summary[food_summary['권역'] == place_list[i]])):
        sheet.append(food_summary[food_summary['권역'] == place_list[i]].iloc[t, 1:6].tolist())

    sheet.append([" "])
    sheet.append(["카페"])
    sheet.append(["가게명", "리뷰 수"])
    for t in range(len(cafe_summary[cafe_summary['권역'] == place_list[i]])):
        sheet.append(cafe_summary[cafe_summary['권역'] == place_list[i]].iloc[t, 1:4].tolist())

    if drink != "0":
        sheet.append([" "])
        sheet.append(["술집"])
        sheet.append(["가게명", "음주 종류", "리뷰 수", "가격대"])
        for t in range(len(drink_summary[drink_summary['권역'] == place_list[i]])):
            sheet.append(drink_summary[drink_summary['권역'] == place_list[i]].iloc[t, 1:5].tolist())

    sheet.append([" "])
    sheet.append(["활동"])
    sheet.append(["장소명", "장소 세부"])
    for t in range(len(activity_summary[activity_summary['권역'] == place_list[i]])):
        sheet.append(activity_summary[activity_summary['권역'] == place_list[i]].iloc[t, 1:3].tolist())
wb.save('뭐하고놀까.xlsx')

print("엑셀 출력이 완료되었습니다.")