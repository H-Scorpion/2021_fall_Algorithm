# code reference: https://stackoverflow.com/questions/52137431/strassens-algorithm-bug-in-python-implementation

import numpy as np
import copy
def new_matrix(r, c):
    """Create a new matrix filled with zeros."""
    matrix = [[0 for row in range(r)] for col in range(c)]
    return matrix


def direct_multiply(x, y):
    if len(x[0]) != len(y):
        return "Multiplication is not possible!"
    else:
        p_matrix = new_matrix(len(x), len(y[0]))
        for i in range(len(x)):
            for j in range(len(y[0])):
                for k in range(len(y)):
                    p_matrix[i][j] += x[i][k] * y[k][j]
    return p_matrix


def split(matrix):
    """Split matrix into quarters."""
    a = b = c = d = matrix

    while len(a) > len(matrix)/2:
        a = a[:len(a)//2]
        b = b[:len(b)//2]
        c = c[len(c)//2:]
        d = d[len(d)//2:]

    while len(a[0]) > len(matrix[0])//2:
        for i in range(len(a[0])//2):
            a[i] = a[i][:len(a[i])//2]
            b[i] = b[i][len(b[i])//2:]
            c[i] = c[i][:len(c[i])//2]
            d[i] = d[i][len(d[i])//2:]

    return a, b, c, d


def add_matrix(a, b):
    if type(a) == int:
        d = a + b
    else:
        d = []
        for i in range(len(a)):
            c = []
            for j in range(len(a[0])):
                c.append(a[i][j] + b[i][j])
            d.append(c)
    # error due to implementation
    for i in range(len(d)):
        for j in range(len(d[i])):
            d[i][j] = round(d[i][j],5)
    
    return d


def subtract_matrix(a, b):
    if type(a) == int:
        d = a - b
    else:
        d = []
        for i in range(len(a)):
            c = []
            for j in range(len(a[0])):
                c.append(a[i][j] - b[i][j])
            d.append(c)
    for i in range(len(d)):
        for j in range(len(d[i])):
            d[i][j] = round(d[i][j],5)
    return d


def strassen(x, y, n):
    # base case: 1x1 matrix
    if n == 1:
        z = [[0]]
        z[0][0] = x[0][0] * y[0][0]
        return z
    else:
        # split matrices into quarters
        a, b, c, d = split(x)
        e, f, g, h = split(y)

        # p1 = a*(f-h)
        p1 = strassen(a, subtract_matrix(f, h), n/2)

        # p2 = (a+b)*h
        p2 = strassen(add_matrix(a, b), h, n/2)

        # p3 = (c+d)*e
        p3 = strassen(add_matrix(c, d), e, n/2)

        # p4 = d*(g-e)
        p4 = strassen(d, subtract_matrix(g, e), n/2)

        # p5 = (a+d)*(e+h)
        p5 = strassen(add_matrix(a, d), add_matrix(e, h), n/2)

        # p6 = (b-d)*(g+h)
        p6 = strassen(subtract_matrix(b, d), add_matrix(g, h), n/2)

        # p7 = (a-c)*(e+f)
        p7 = strassen(subtract_matrix(a, c), add_matrix(e, f), n/2)

        z11 = add_matrix(subtract_matrix(add_matrix(p5, p4), p2), p6)

        z12 = add_matrix(p1, p2)

        z21 = add_matrix(p3, p4)

        z22 = add_matrix(subtract_matrix(subtract_matrix(p5, p3), p7), p1)

        z = new_matrix(len(z11)*2, len(z11)*2)
        for i in range(len(z11)):
            for j in range(len(z11)):
                z[i][j] = z11[i][j]
                z[i][j+len(z11)] = z12[i][j]
                z[i+len(z11)][j] = z21[i][j]
                z[i+len(z11)][j+len(z11)] = z22[i][j]

        return z


# a = []
# b = []

# for i in range(4):
#     a.append([])
#     for j in range(4):
#         a[i].append(np.random.uniform(0,100))

# for i in range(4):
#     b.append([])
#     for j in range(4):
#         b[i].append(np.random.uniform(0,100))

# a_noise = copy.deepcopy(a)
# for i in range(len(a)):
#     for j in range(len(a[i])):
#         a_noise[i][j]+=np.random.normal(0,1)

a=[[43.24732611696363, 15.260152019967354, 57.35503764746399, 49.59909784614932], [60.805651367702, 36.37187857282389, 51.599034857043, 14.627367565156623], [51.25361572605078, 57.005210497032024, 31.722967218440523, 45.75286012191647], [46.50727587206944, 48.96919000739919, 84.78053824702526, 90.73080332279434]]        
a_noise = [[42.47446893178593, 16.733926826235617, 58.307283496988234, 48.76388292463785], [60.23693039715966, 36.339469023858165, 51.45771661984903, 13.92058456279733], [52.22303941026034, 57.973088599032295, 30.701167848141658, 45.71096920613171], [45.760694585802405, 48.14424336029644, 84.14154132039924, 90.21774679488132]]
b = [[18.952157796723434, 20.732884967627964, 83.70651166371793, 72.55760703032138], [95.30021601926208, 41.56952724193598, 31.47505495900066, 13.133647366032164], [9.50094027332774, 14.822028794466934, 16.409786370614874, 20.36489935784499], [44.89816190777335, 57.420375591668424, 46.68694221659614, 66.93197367318594]]   

print(f"a = {a}")
print(f"a_noise = {a_noise}")
print(f"b = {b}")

print(f"Using naive algorithm:\na*b = {direct_multiply(a, b)}")
print(f"Using Strassen's algorithm:\na*b = {strassen(a, b, 4)}")
# print(f"Using Strassen's algorithm:\na_noise*b = {strassen(a_noise, b, 4)}")
print(f"Using naive algorithm:\na_noise*b = {direct_multiply(a_noise, b)}")
