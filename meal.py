import requests
import re


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

            if 'dd_date' in data[middle - 1] and (middle == data_length or 'dd_date' not in data[middle]):
                return middle

            if 'dd_date' not in data[middle - 1] and 'dd_date' not in data[middle]:
                return last_dd_date(left, middle - 1)
            else:
                return last_dd_date(middle + 1, right)

        def first_meal(left, right):
            middle = (right - left) // 2 + left

            if (middle == 0 or data[middle - 1] is None) and data[middle] is not None:
                return middle

            if data[middle - 1] is None and data[middle] is None:
                return first_meal(middle + 1, right)
            else:
                return first_meal(left, middle - 1)

        def last_meal(left, right):
            middle = (right - left) // 2 + left

            if data[middle - 1] is not None and (middle == result_length or data[middle] is None):
                return middle

            if data[middle - 1] is None and data[middle] is None:
                return last_meal(left, middle - 1)
            else:
                return last_meal(middle + 1, right)

        data = requests.post("http://www.foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolMonthMealsDetail.do", {
            'schl_cd': schl_cd,
            'year': year,
            'month': month,
            'type_cd': 'M'
        }).json()['list']

        data_length = len(data)
        middle = data_length // 2

        data = data[first_dd_date(0, middle - 1):last_dd_date(middle, data_length)]

        start_day = {'일': 0, '월': 1, '화': 2, '수': 3, '목': 4, '금': 5, '토': 6}[data[0]['week_day']]

        result = [{'lunch': (i['lunch'].split('\n') if 'lunch' in i else None), 'dinner': (i['dinner'].split('\n') if 'dinner' in i else None)} for i in data]

        result_length = len(result)
        middle = result_length // 2

        for i in range(first_meal(0, middle - 1), last_meal(middle, result_length)):
            for j in ['lunch', 'dinner']:
                if result[i][j] is not None:
                    for k in range(len(result[i][j])):
                        alergies = re.search(r'(\d+\.)*$', result[i][j][k])

                        result[i][j][k] = (result[i][j][k][:alergies.span()[0]], tuple(map(int, alergies.group().split('.')[:-1])), )

        return start_day, result
