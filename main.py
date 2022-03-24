from Matrix import Matrix


def read_from_file(f):
    data = []
    rows = 0
    text = f.read()
    column = -1
    accuracy = -1
    for line in text.split("\n"):
        try:
            row = list(map(float, line.split()))
        except:
            print("Данные в файле неправильные")
            return Matrix([[]], 0, 0), -1
        if column == -1:
            column = len(row)
        if len(row) == 1:
            accuracy = row[0]
        elif len(row) != column:
            print("Неверное количество переменных")
            return Matrix([[]], 0, 0), -1
        else:
            data.append(row)
            rows += 1
    if accuracy == -1:
        print("В файле отсутствует погрещность")
        while accuracy < 0:
            print("Введите допустимую погрешность (>0)")
            try:
                accuracy = float(input())
            except:
                print("Неправильный ввод")
    if column == rows+1:
        return Matrix(data, rows, column), accuracy
    else:
        print("Неверное количество переменных")
        return Matrix([[]], 0, 0), -1


def read_from_cons(n):
    data = []
    print("Введите матрицу")
    rows = 0
    while n != rows:
        try:
            row = list(map(float, input().split()))
        except:
            print("Неверный формат")
            continue

        if len(row) != n + 1:
            print("Неверное количество чисел")
            continue

        rows += 1
        data.append(row)
    accuracy = -1
    while accuracy < 0:
        print("Введите допустимую погрешность (>0)")
        try:
            accuracy = float(input())
        except:
            print("Неправильный ввод")
    return Matrix(data, n, n+1), accuracy


def read_matrix():
    print("Введите имя файла или количество неизвестных. Чтобы выйти, отправьте exit")
    n = input()
    if n.isnumeric():
        n = int(n)
        if 0 < n <= 20:
            matrix, accuracy = read_from_cons(n)
        else:
            print("Размер матрицы не должен превышать 20")
            matrix, accuracy = read_matrix()
    elif n == "exit":
        matrix = Matrix([[]], 0, 0)
        accuracy = -2
    else:
        try:
            with open(n, "r+") as f:
                matrix, accuracy = read_from_file(f)
        except:
            print("Ошибка чтения файла")
            matrix, accuracy = read_matrix()
    return matrix, accuracy


def check_diagonal(matrix):
    ans = True
    for i in range(matrix.row):
        ans = ans * (matrix.data[i][i] >= sum(matrix.data[i]) - matrix.data[i][i])
    return ans


# Попробовать поменять матрицу, чтобы выполнялось условие преобладания диагональных элементов
def change_for_diagonal(matrix):
    indexes = [0]*matrix.row
    for i in range(matrix.row):
        cur = matrix.index_of_max_in_a_row(i)
        if indexes[cur]:
            print("Невозможно перестроить матрицу")
            return matrix
        else:
            indexes[cur] = 1

    data = [0]*matrix.row
    for i in range(matrix.row):
        data[matrix.index_of_max_in_a_row(i)] = matrix.data[i]
    matrix.data = data
    return matrix


def get_parameters(matrix, A, b):
    for i in range(matrix.row):
        A.append([])
        for j in range(matrix.column-1):
            A[i].append(matrix.data[i][j])
        b.append(matrix.data[i][-1])


def get_C(A):
    C = []
    for i in range(len(A)):
        C.append([0]*len(A))
        for j in range(len(A)):
            if i != j:
                C[i][j] = -A[i][j]/A[i][i]
    return C


def get_D(A, b):
    d = []
    for i in range(len(A)):
        d.append(b[i]/A[i][i])
    return d


def iteration_method(matrix, accuracy):
    change_for_diagonal(matrix)
    matrix.print_matrix("Данная матрица")
    print("Ответ с точностью до", accuracy)
    A = []
    b = []
    get_parameters(matrix, A, b)
    C = get_C(A)
    D = get_D(A, b)
    cur_accuracy = accuracy
    x_k_1 = D
    iterations = 0
    accuracies = [0]*len(x_k_1)
    while cur_accuracy >= accuracy:
        x_k = []
        cur_accuracy = -1
        for i in range(len(C)):
            x = 0
            for j in range(len(C)):
                x += C[i][j] * x_k_1[j]
            x += D[i]
            x_k.append(x)
            cur_accuracy = max(cur_accuracy, abs(x - x_k_1[i]))
            accuracies[i] = abs(x - x_k_1[i])
        iterations += 1
        x_k_1 = x_k
        print("Погрешности на", iterations, "итерации составляют:")
        for i in range(len(C)):
            print("|x", i+1, " - x", i+1, "(k-1)| = ", accuracies[i], sep='')
    print("Решение данного уравнение выполнено за", iterations, "итераций")
    for i in range(len(x_k)):
        print("x", i+1, " = ", x_k[i], sep="")


def main():
    print("Добро пожаловать! Желаете решить СЛАУ методом простых итераций? Данная программа к вашим услугам")
    while True:
        matrix, accuracy = read_matrix()
        while accuracy == -1:
            matrix, accuracy = read_matrix()
        if accuracy == -2:
            print("До свидания. Ждем вас еще")
            break
        iteration_method(matrix, accuracy)


main()
