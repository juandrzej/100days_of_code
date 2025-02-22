# with open("weather_data.csv") as file:
#     data = file.readlines()
# print(data)

# import csv
#
# with open("weather_data.csv") as file:
#     data = csv.reader(file)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#
#     print(temperatures)

import pandas

# data = pandas.read_csv("weather_data.csv")
# dict_data = data.to_dict()
#
# # print(dict_data)
#
# temp_list = data["temp"].to_list()
#
# # avg = 0
# # for temp in temp_list:
# #     avg += temp
# # avg /= len(temp_list)
# # print(avg)
#
# # average = sum(temp_list) / len(temp_list)
# # print(average)
#
# # print(data["temp"].mean())
#
# # print(data["temp"].max())
#
# # print(data[data.day == "Monday"])
#
# # max_temp = data["temp"].max()
# # print(data[data.temp == max_temp])
#
# # monday = data[data.day == "Monday"]
# # # print(monday.condition)
# # monday_temp = monday.temp * 9 / 5 + 32
# # print(monday_temp)
#
# # create dataframe from scratch
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [76, 56, 65]
# }
# data = pandas.DataFrame(data_dict)
# data.to_csv("new_data.csv")

squirrel_data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
fur_list = list(squirrel_data["Primary Fur Color"].unique())
fur_list.pop(0)
fur_counts = []
for fur in fur_list:
    fur_count = len(squirrel_data[squirrel_data["Primary Fur Color"] == fur])
    fur_counts.append(fur_count)

fur_dict = {
    "Fur Color": fur_list,
    "Count": fur_counts
}
df = pandas.DataFrame(fur_dict)
df.to_csv("squirrel_count.csv")


# fur_table = squirrel_data["Primary Fur Color"].value_counts()
# dict_fur = fur_table.to_csv("squirrel_count.csv")


