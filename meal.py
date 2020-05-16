import requests


class Meal:
    def __init__(self):
        pass

    def get_month(self, schl_cd, year, month):
        def first_dd_date(left, right):
            middle = (right - left) // 2 + left

            if (middle == 0 or 'dd_date' not in data[middle - 1]) and 'dd_date' in data[middle]:
                return middle

            if 'dd_date' not in data[middle - 1] and 'dd_date' not in data[middle]:
                return first_dd_date(middle + 1, right)
            else:
                return first_dd_date(left, middle - 1)

        def last_dd_date(left, right):
            middle = (right - left) // 2 + left

            if (middle == 0 or 'dd_date' in data[middle - 1]) and 'dd_date' not in data[middle]:
                return middle

            if 'dd_date' not in data[middle - 1] and 'dd_date' not in data[middle]:
                return last_dd_date(left, middle - 1)
            else:
                return last_dd_date(middle + 1, right)

        data = requests.post("http://www.foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolMonthMealsDetail.do", {
            'schl_cd': schl_cd,
            'year': year,
            'month': month,
            'type_cd': 'M'
        }).json()['list']

        middle = len(data) // 2

        data = data[first_dd_date(0, middle - 1):last_dd_date(middle, len(data))]

        start_day = {'일': 0, '월': 1, '화': 2, '수': 3, '목': 4, '금': 5, '토': 6}[data[0]['week-day']]

        result = [{'lunch': (i['lunch'] if 'lunch' in i else None), 'dinner': (i['dinner'] if 'dinner' in i else None)} for i in data]

        return start_day, result
