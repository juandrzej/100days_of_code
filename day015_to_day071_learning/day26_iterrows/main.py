import random
import pandas

# names = ['Alex', 'Beth', 'Caroline', 'Dave', 'Eleanor', 'Freddie']
# student_scores = {student: random.randint(1, 100) for student in names}
# passed_students = {student: score for (student, score) in student_scores.items() if score > 60}
# print(passed_students)

student_dict = {
    "student": ['Alex', 'Beth', 'Caroline'],
    "score": [55, 66, 77]
}

student_df = pandas.DataFrame(student_dict)
print(student_df)

# loop thru data frame
# for (key, value) in student_df.items():
#     print(value)

# loop thru rows of df in pandas
for (index, row) in student_df.iterrows():
    if row.student == 'Beth':
        print(row.score)