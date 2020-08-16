import math
from tkinter import *
from decimal import Decimal

window = Tk()
window.title("Binomial Hypothesis Testing")

def GetInput():
    n = enterTrials.get()
    p = enterProb.get()
    X = enterNo.get()
    sigLevel = enterSig.get()
    tailsGet = optionVar.get()
    tails = 0
    if tailsGet == "One-tailed":
        tails = 1
    elif tailsGet == "Two-tailed":
        tails = 2
    if tails != 0:
        if n.isnumeric() and X.isnumeric() and IsFloat(p) and IsActualFloat(sigLevel):
            if int(X) <= int(n) and AIR(p)[0]/AIR(p)[1] >= 0 and AIR(p)[0]/AIR(p)[1] <= 1:
                if float(sigLevel) > 0 and float(sigLevel) < 100:
                    n = int(n)
                    p = AIR(p)[0]/AIR(p)[1]
                    X = int(X)
                    sigLevel = float(sigLevel)/tails
                    Test(n,p,X,sigLevel)

def Test(n,p,X,sigLevel):
    expected = n*p
    H0["text"] = "H0: p=" + str(p)
    if X > expected:
        h1 = "greater"
        H1["text"] = "H1: p>" + str(p)
        prob = bcd(n,p,X,n) * 100
    else:
        h1 = "less"
        H1["text"] = "H1: p<" + str(p)
        prob = bcd(n,p,0,X) * 100
    pLabel["text"] = "p=" + str(round((prob/100),5))
    if prob < sigLevel:
        accept["text"] = "Accept H1"
    else:
        accept["text"] = "Accept H0"
    
def IsActualFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def nCr(n,r): # must be ints
    nCr = int(math.factorial(n)/(math.factorial(r)*math.factorial(n-r)))
    return nCr

def bcd(n,p,r,s): # 0<=r<=s<=n (ints), 0<=p<=1
    prob = 0
    for k in range(r,s+1): # r to s inclusive
        bpd = nCr(n,k) * p**k * (1-p)**(n-k)
        prob += bpd
    return prob

def IsFloat(string): # float type or fraction e.g. -1/3, 0.25
    if "/" in string:
        index = string.index("/")
        numerator = string[0:index]
        denominator = string[index + 1:len(string)]
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

def AIR(num): # string into fraction as tuple

    if "/" in num:
        index = num.index("/")
        numerator = int(num[0:index])
        denominator = int(num[index + 1:len(num)])
        return (numerator, denominator)
    else:
        return Decimal(num).as_integer_ratio()

# GUI Creation

col1 = Frame(master = window)
frameTrials = Frame(col1)
trials = Label(master = frameTrials, text = "Trials")
trials.grid(row=0,column=0)
frameProb = Frame(master = col1)
probSuccess = Label(master = frameProb, text = "Probability")
probSuccess.grid(row=0,column=0)
frameNo = Frame(master = col1)
NoSuccess = Label(master = frameNo, text = "No. of successes")
NoSuccess.grid(row=0,column=0)
frameSig = Frame(master = col1)
sigLabel = Label(master = frameSig, text = "Significance level %")
sigLabel.grid(row=0,column=0)
frameTrials.grid(row=0,column=0)
frameProb.grid(row=1,column=0)
frameNo.grid(row=2,column=0)
frameSig.grid(row=3,column=0)
col1.grid(row=0,column=0)
frameOption = Frame(master = window)
optionVar = StringVar()
optionVar.set("Select tails")
dropdown = OptionMenu(frameOption, optionVar, "One-tailed", "Two-tailed")
dropdown.grid(row=0,column=0)
frameOption.grid(row=5,column=0)

col2 = Frame(master = window)
enter1 = Frame(master = col2)
enterTrials = Entry(master = enter1, width = 6)
enterTrials.grid(row=0,column=0)
enter2 = Frame(master = col2)
enterProb = Entry(master = enter2, width = 6)
enterProb.grid(row=0,column=0)
enter3 = Frame(master = col2)
enterNo = Entry(master = enter3, width = 6)
enterNo.grid(row=0,column=0)
enter4 = Frame(master = col2)
enterSig = Entry(master = enter4, width = 6)
enterSig.grid(row=0,column=0)
enter1.grid(row=0,column=0)
enter2.grid(row=1,column=0)
enter3.grid(row=2,column=0)
enter4.grid(row=3,column=0)
col2.grid(row=0,column=1)

col3 = Frame(master = window)
frameH0 = Frame(master = col3)
H0 = Label(master = frameH0, text = "H0:", width = 15)
H0.grid(row=0,column=0)
frameH1 = Frame(master = col3)
H1 = Label(master = frameH1, text = "H1:", width = 15)
H1.grid(row=0,column=0)
frameP = Frame(master = col3)
pLabel = Label(master = frameP, text = "p=", width = 15)
pLabel.grid(row=0,column=0)
frameAccept = Frame(master = col3)
accept = Label(master = frameAccept, text = "", width = 15)
accept.grid(row=0,column=0)
frameH0.grid(row=0,column=0)
frameH1.grid(row=1,column=0)
frameP.grid(row=2,column=0)
frameAccept.grid(row=3,column=0)
col3.grid(row=0,column=2)

frameButton = Frame(master = window)
button = Button(
    master = frameButton,
    text = "Test Hypothesis",
    command = GetInput,
    bg = "#1E7800",
    fg = "#FFFFFF"
    )
button.grid(row=0,column=0)
frameButton.grid(row=5, column=2)


window.mainloop()
