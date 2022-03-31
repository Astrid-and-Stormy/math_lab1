class Matrix:
    def __init__(self, data, row, column):
        self.data = data
        self.row = row
        self.column = column

    def index_of_max_in_a_row(self, row):
        maxim = max(map(abs, self.data[row][:-1]))
        ans = 0
        while abs(self.data[row][ans]) != maxim:
            ans += 1
        return ans

    def to_string(self):
        ans = ''
        for i in self.data:
            ans += ' '.join(map(str, i))
            ans += '\n'
        return ans

    def print_matrix(self, message):
        print(message, self.to_string(), sep="\n")
