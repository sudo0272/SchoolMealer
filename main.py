from school_data import SchoolData
from meal import  Meal

school_data = SchoolData()
meal = Meal()

# school_data.crawl_db()

print(meal.get_month(list(school_data.get_db(schl_nm=('천안쌍용고등학교', '=')))[0], 2020, 5))
