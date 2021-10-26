from vec import Vec
from mat import Mat
import image_mat_util
import matutil
import solver
import mat

trw = (2, 0)
trr = (347, 133)
tlw = (0, 0)
tlr = (127, 74)
brw = (2, 1)
brr = (353, 287)
blw = (0, 1)
blr = (138, 371)

domain = {"y1x1", "y1x2", "y1x3", "y2x1", "y2x2", "y2x3", "y3x1", "y3x2", "y3x3"}

def move2board(y):
    y1 = y["y1"]
    y2 = y["y2"]
    y3 = y["y3"]
    v = Vec({'y1', 'y2', 'y3'}, {'y1': y1/y3, 'y2': y2/y3, 'y3': y3/y3})
    return v

def make_equations(x1, x2, w1, w2):
    u = Vec(domain, {"y1x1": -x1, "y1x2": -x2, "y1x3": -1, "y3x1": w1*x1, "y3x2": w1*x2, "y3x3": w1})
    v = Vec(domain, {"y3x1": w2*x1, "y3x2": w2*x2, "y3x3": w2, "y2x1": -x1, "y2x2": -x2, "y2x3": -1})
    return [u, v]

def mat_move2board(Y):
    k = matutil.mat2coldict(Y)
    for n in k:
        k[n]['y1'] = k[n]['y1'] / k[n]['y3']
        k[n]['y2'] = k[n]['y2'] / k[n]['y3']
        k[n]['y3'] = 1
    return matutil.coldict2mat(k)


w = Vec(domain, {"y1x1": 1})

L = Mat(({0, 1, 2, 3, 4, 5, 6, 7, 8}, domain), {})

a = make_equations(tlr[0], tlr[1], tlw[0], tlw[1])
b = make_equations(blr[0], blr[1], blw[0], blw[1])
c = make_equations(trr[0], trr[1], trw[0], trw[1])
e = make_equations(brr[0], brr[1], brw[0], brw[1])
for d in domain:
    L[0, d] = a[0][d]
    L[1, d] = a[1][d]
    L[2, d] = b[0][d]
    L[3, d] = b[1][d]
    L[4, d] = c[0][d]
    L[5, d] = c[1][d]
    L[6, d] = e[0][d]
    L[7, d] = e[1][d]
    L[8, d] = w[d]

print(L)

b = Vec({0, 1, 2, 3, 4, 5, 6, 7, 8}, {8: 1})

h = solver.solve(L, b)

H = Mat(({"y1", "y2", "y3"}, {"x1", "x2", "x3"}), {})
H["y1", "x1"] = h["y1x1"]
H["y1", "x2"] = h["y1x2"]
H["y1", "x3"] = h["y1x3"]
H["y2", "x1"] = h["y2x1"]
H["y2", "x2"] = h["y2x2"]
H["y2", "x3"] = h["y2x3"]
H["y3", "x1"] = h["y3x1"]
H["y3", "x2"] = h["y3x2"]
H["y3", "x3"] = h["y3x3"]

(X_pts, colors) = image_mat_util.file2mat('QuoteImage copy 2.png', ('x1', 'x2', 'x3'))
Y_pts = H * X_pts

Y_board = mat_move2board(Y_pts)

image_mat_util.mat2png(Y_board, colors, 'QuoteImageFinal.png', ('y1', 'y2', 'y3'), height=1200)



