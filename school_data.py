import sqlite3
import requests
import re


class SchoolData:
    def __init__(self):
        self.__regions = ['서울특별시',
                          '부산광역시',
                          '인천광역시',
                          '대구광역시',
                          '광주광역시',
                          '대전광역시',
                          '울산광역시',
                          '세종특별자치시',
                          '경기도',
                          '강원도',
                          '충청남도',
                          '충청북도',
                          '경상남도',
                          '경상북도',
                          '전라남도',
                          '전라북도',
                          '제주특별자치도']

        self.__db_file = 'school.db'
        self.__db = sqlite3.connect(self.__db_file)

    def get_regions(self):
        return self.__regions

    def get_db_file(self):
        return self.__db_file

    def clear_db(self):
        self.__db.execute('''DROP TABLE IF EXISTS `school_data`''')
        self.__db.execute('''CREATE TABLE `school_data` (
                                 `schl_cd` INT NOT NULL,
                                 `schl_nm` varchar(21) NOT NULL,
                                 `ara` varchar(7)
                             )''')

    def commit_db(self):
        self.__db.commit()

    def add_db(self, schl_cd, schl_nm, ara):
        self.__db.execute('''INSERT INTO `school_data` VALUES ('%s', '%s', '%s')''' % (re.escape(schl_cd), re.escape(schl_nm), re.escape(ara)))

    def get_db(self, **kwargs):
        return self.__db.execute('''SELECT *
                                        FROM `school_data`
                                            %s''' % (('WHERE' + ' AND '.join(['%s %s %s' % (re.escape(i), re.escape(kwargs[i][0]), re.escape(kwargs[i][1])) for i in kwargs.keys()])) if len(kwargs) > 0 else ''))

    def crawl_db(self):
        data = requests.post('http://www.foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolMeals_school.do')
        data = data.json()['list']

        self.clear_db()

        for i in data:
            self.add_db(i['schl_cd'], i['schl_nm'], i['ara'])

        self.commit_db()
