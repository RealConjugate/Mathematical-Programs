import tkinter as tk
from math import gcd
from decimal import Decimal

window = tk.Tk()
window.title("2Var Simultaneous Equation Solver")

def GetInput():
    a = entryx1.get()
    b = entryy1.get()
    p = entryRHS1.get()
    c = entryx2.get()
    d = entryy2.get()
    q = entryRHS2.get()

    coeff = [a,b,p,c,d,q]
    valid = True
    for string in coeff:
        if not IsFloat(string):
            valid = False
    if valid:
        A = AIR(a)
        B = AIR(b)
        P = AIR(p)
        C = AIR(c)
        D = AIR(d)
        Q = AIR(q)

        detNumerator = ABminusCD(A,D,B,C)[0]

        if detNumerator != 0: # implies det != 0, unique solution
            SolveNonzeroDet(A,B,P,C,D,Q)
        else: # none or infinite solutions
            floats = []
            for string in coeff:
                floats.append(AIR(string)[0]/AIR(string)[1]) # turns string into actual float
            SolveZeroDet(floats[0],floats[1],floats[2],floats[3],floats[4],floats[5])


def SolveZeroDet(a,b,p,c,d,q):

    # Equations not both lines

    if (AllZero([a,b]) and p != 0) or (AllZero([c,d]) and q != 0):
        solutions["text"] = "No solutions"
    elif AllZero([a,b,p]) or AllZero([c,d,q]): # 0x + 0y = 0
        solutions["text"] = "Infinitely many solutions"

    # Both equations are lines

    else:
        if ExactlyOneZero(a,c) or ExactlyOneZero(b,d) or ExactlyOneZero(p,q):
            solutions["text"] = "No solutions"
        else:
            coeff = [a,b,p,c,d,q]
            nonZeroFound = False
            i = 3
            while not nonZeroFound: # no need for "i<=5" as c,d,q aren't all 0
                if coeff[i] != 0:
                    nonZeroFound = True
                else:
                    i += 1
            k = coeff[i-3]/coeff[i]
            if a == k*c and b == k*d and p == k*q: # lines are "multiples"
                solutions["text"] = "Infinitely many solutions (same equation/line)"
            else:
                solutions["text"] = "No solutions"


def SolveNonzeroDet(A,B,P,C,D,Q): # all arguments are fraction tuples
    X = DivideFrac(ABminusCD(D,P,B,Q),ABminusCD(A,D,B,C))
    Y = DivideFrac(ABminusCD(A,Q,C,P),ABminusCD(A,D,B,C))
    X = Simplify(X)
    Y = Simplify(Y)
    x = PairToFractionStr(X)
    y = PairToFractionStr(Y)

    solutions["text"] = "x = " + str(x) + ", y = " + str(y)


def AIR(num): # turns string into simplest form fraction as a tuple of ints
    # str argument avoids floating point inaccuracies

    if "/" in num: # num already is "floatable" - only one "/"
        index = num.index("/")
        numerator = int(num[0:index])
        denominator = int(num[index + 1:len(num)])
        return (numerator, denominator)
    else:
        return Decimal(num).as_integer_ratio()


def IsFloat(string): # checks if it's either float type or fraction e.g. -1/3, 0.25
    if "/" in string:
        index = string.index("/") # first instance
        numerator = string[0:index]
        denominator = string[index + 1:len(string)]

        # If more than one "/" in string then there'll be a ValueError
        
        try:
            int(numerator)
            try:
                int(denominator)
                return True
            except ValueError:
                return False
            
        except ValueError:
            return False
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def ABminusCD(A,B,C,D): # returns fraction tuple for AB-CD (arguments)
    numerator = (A[0]*B[0]*C[1]*D[1]) - (C[0]*D[0]*A[1]*B[1])
    denominator = A[1]*B[1]*C[1]*D[1]
    return Simplify((numerator, denominator))


def Simplify(pair): # returns simplest form fraction tuple
    numerator = pair[0]
    denominator = pair[1]
    if denominator < 0:
        numerator = -1 * numerator
        denominator = -1 * denominator

    GCD = gcd(numerator, denominator)
    numerator = int(numerator / GCD)
    denominator = int(denominator / GCD)
    return (numerator, denominator)


def PairToFractionStr(pair): # turns tuple into fraction to display
    numerator = pair[0]
    denominator = pair[1]
    if denominator == 1:
        return str(numerator)
    else:
        return str(numerator) + "/" + str(denominator)

def DivideFrac(V,W): # returns new fraction tuple (divides)
    return (V[0]*W[1], V[1]*W[0])


def AllZero(numberList):
    magnitudeSquared = 0
    for num in numberList:
        magnitudeSquared += num**2        
    if magnitudeSquared == 0:
        return True
    else:
        return False

def ExactlyOneZero(x,y):
    if x*y == 0 and (x**2 + y**2) != 0: # faster than comparisons
        return True
    else:
        return False


# GUI Frames

frame0 = tk.Frame(master = window)
instruction = tk.Label(master = frame0, text = " Enter coefficients in integer/decimal/fraction form e.g. 2, -0.25, 1/3 ")
instruction.grid(row=0,column=0)

frame1 = tk.Frame(master = window)
frameEntryx1 = tk.Frame(master = frame1)
framex1 = tk.Frame(master = frame1)
frameEntryy1 = tk.Frame(master = frame1)
framey1 = tk.Frame(master = frame1)
frameRHS1 = tk.Frame(master = frame1)

entryx1 = tk.Entry(master = frameEntryx1, width = 5)
x1 = tk.Label(master = framex1, text = "x +")
entryy1 = tk.Entry(master = frameEntryy1, width = 5)
y1 = tk.Label(master = framey1, text = "y =")
entryRHS1 = tk.Entry(master = frameRHS1, width = 5)
entryx1.grid(row=0, column=0)
x1.grid(row=0, column=0)
entryy1.grid(row=0, column=0)
y1.grid(row=0, column=0)
entryRHS1.grid(row=0, column=0)
frameEntryx1.grid(row=0, column=0)
framex1.grid(row=0, column=1)
frameEntryy1.grid(row=0, column=2)
framey1.grid(row=0, column=3)
frameRHS1.grid(row=0, column=4)

frame2 = tk.Frame(master = window)
frameEntryx2 = tk.Frame(master = frame2)
framex2 = tk.Frame(master = frame2)
frameEntryy2 = tk.Frame(master = frame2)
framey2 = tk.Frame(master = frame2)
frameRHS2 = tk.Frame(master = frame2)

entryx2 = tk.Entry(master = frameEntryx2, width = 5)
x2 = tk.Label(master = framex2, text = "x +")
entryy2 = tk.Entry(master = frameEntryy2, width = 5)
y2 = tk.Label(master = framey2, text = "y =")
entryRHS2 = tk.Entry(master = frameRHS2, width = 5)
entryx2.grid(row=0, column=0)
x2.grid(row=0, column=0)
entryy2.grid(row=0, column=0)
y2.grid(row=0, column=0)
entryRHS2.grid(row=0, column=0)
frameEntryx2.grid(row=0, column=0)
framex2.grid(row=0, column=1)
frameEntryy2.grid(row=0, column=2)
framey2.grid(row=0, column=3)
frameRHS2.grid(row=0, column=4)

frame3 = tk.Frame(master = window)
button = tk.Button(master = frame3, width = 7, text = "Solve", command = GetInput,
                   bg = "#1E7800", fg = "#FFFFFF")
button.grid(row=0, column=0)

frame4 = tk.Frame(master = window)
solutions = tk.Label(master = frame4)
solutions.grid(row=0, column=0)

frame0.grid(row=0, column=0)
frame1.grid(row=1, column=0)
frame2.grid(row=2, column=0)
frame3.grid(row=3, column=0)
frame4.grid(row=4, column=0)

window.mainloop()
