import PyPDF2
import tabula
import numpy as np
import statistics
import time

# Pre
print('Compiling.........')
print('Please Wait')


class Student:

    def __init__(self, s_id: str, score: float):

        self.student_id = s_id
        self.score = score

    def __lt__(self, other):  # less than

        if self.score < other.score:
            return True
        else:
            return False

    def __str__(self):
        return f'{self.student_id} -> {self.score}'


def isfloat(strfloat) -> bool:

    try:
        float(strfloat)
        return True
    except ValueError:
        return False


# merge sort is consistent < always O(n*logn) >
def mergesort(array: list, n: int):

    if n < 2:
        return array

    sorted_array = list()

    half = n//2
    rem = n % 2

    n_left = half
    n_right = half+rem

    left = mergesort(array[0: half], n_left)
    right = mergesort(array[half:], n_right)

    i, j = 0, 0
    while i < n_left and j < n_right:

        L = left[i]
        R = right[j]

        if L < R:
            sorted_array.append(L)
            i += 1

        else:
            sorted_array.append(R)
            j += 1

    while i < n_left:

        sorted_array.append(left[i])
        i += 1

    while j < n_right:

        sorted_array.append(right[j])
        j += 1

    return sorted_array


if __name__ == '__main__':

    ### FOR FURTHER PROCESSING ###
    data = list()
    extract_score = list()
    # ### ## #### ### ### ### ## #

    print('Extracting Data ', end='')

    filename = 'score/2563-2-cal2.pdf'

    columnIndexToRead = [1, 3, 5, 7, 9]

    table_list = list()

    for page in range(1, 5+1):

        table = tabula.read_pdf(filename, pages=page, pandas_options={'header': None})
        table_list.append(table[0])

    print('. ', end='')

    for table in table_list:

        for index_to_read in columnIndexToRead:

            id_column = table[index_to_read-1]
            score_column = table[index_to_read]
            N = len(score_column)

            for i in range(N):

                student_id = str(id_column[i])
                score = score_column[i]

                # clean data and add to further process
                if isfloat(score) and not score != score and student_id.isdigit():

                    # clean score
                    score = round(float(score), 2)
                    extract_score.append(score)
                    data.append(Student(student_id, score))

        print('. ', end='')

    print()

    # sorting
    data = mergesort(data, len(data))
    extract_score = mergesort(extract_score, len(extract_score))

    # some info
    n_student = len(data)
    sd = statistics.pstdev(extract_score)

    # APPLICATION (find percentile of our score)
    query_student_id = input("Student ID: ")
    query_score = -1  # -1 is not found case

    # PROCESS
    # find query's score
    for student in data:

        if student.student_id == query_student_id:
            query_score = student.score
            break

    if query_score != -1:
        print('Your Score -> {}'.format(query_score))

        ### Calculate Percentile ###
        before = 0
        equal = 0

        for score in extract_score:

            if score < query_score:
                before += 1
            elif score == query_score:
                equal += 1
            else:
                break

        ### Show Result ###

        percentile = round((before / (n_student+1)) * 100, 2)  # plus one for free angle

        print('You are the {} percentile'.format(percentile))
        print('** {} people\' score is equal to yours'.format(equal))

    else:
        print('Not Found')
