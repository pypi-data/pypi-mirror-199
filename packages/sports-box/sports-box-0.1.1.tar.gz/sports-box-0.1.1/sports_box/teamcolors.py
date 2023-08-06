# RGB color codes for sports team objects stored in list

# todo: retro team colors (need easier way than just re-copy pasting rgb values)

# List of nba Team objects with standard accessible colors as RGB values
nba = []


class Team:
    def __init__(self, name):
        self.name = name

        # RGB value arrays
        self.color1 = []
        self.color2 = []
        self.color3 = []

    # Getters
    def getTeamName(self):
        return str(self.name)

    def getColor1(self):
        return self.color1

    def getColor2(self):
        return self.color2

    def getColor3(self):
        return self.color3

    # Setters
    def setColor1(self, x, y, z):
        self.color1.append(x)
        self.color1.append(y)
        self.color1.append(z)

    def setColor2(self, x, y, z):
        self.color2.append(x)
        self.color2.append(y)
        self.color1.append(z)

    def setColor3(self, x, y, z):
        self.color3.append(x)
        self.color3.append(y)
        self.color3.append(z)


def getTName(index):
    t = nba[index]

    return t.getTeamName()


def getTColor1(index):
    t = nba[index]

    return t.getColor1()


atl = Team("atl")
atl.setColor1(225, 68, 52)
atl.setColor2(196, 214, 0)
atl.setColor3(38, 40, 42)
nba.append(atl)

bos = Team("bos")
bos.setColor1(0, 122, 51)
bos.setColor2(139, 111, 78)
bos.setColor3(255, 255, 255)
nba.append(bos)

bkn = Team("bkn")
bkn.setColor1(0, 0, 0)
bkn.setColor2(255, 255, 255)
nba.append(bkn)

cha = Team("cha")
cha.setColor1(29, 17, 96)
cha.setColor2(0, 120, 140)
cha.setColor3(161, 161, 164)
nba.append(cha)

chi = Team("chi")
chi.setColor1(206, 17, 65)
chi.setColor2(6, 25, 34)
chi.setColor3(255, 255, 255)
nba.append(chi)

cle = Team("cle")
cle.setColor1(134, 0, 56)
cle.setColor2(4, 30, 66)
cle.setColor3(253, 187, 48)
nba.append(cle)

dal = Team("dal")
dal.setColor1(0, 83, 188)
dal.setColor2(0, 43, 92)
dal.setColor3(187, 196, 202)
nba.append(dal)

den = Team("den")
den.setColor1(13, 34, 64)
den.setColor2(255, 198, 39)
den.setColor3(139, 35, 50)
nba.append(den)

det = Team("det")
det.setColor1(200, 16, 46)
det.setColor2(29, 66, 138)
det.setColor3(181, 179, 179)
nba.append(det)

gsw = Team("gsw")
gsw.setColor1(29, 66, 138)
gsw.setColor2(255, 199, 44)
nba.append(gsw)

hou = Team("hou")
hou.setColor1(206, 17, 65)
hou.setColor2(6, 25, 34)
hou.setColor3(196, 206, 211)
nba.append(hou)

ind = Team("ind")
ind.setColor1(0, 45, 98)
ind.setColor2(253, 187, 48)
ind.setColor3(190, 192, 194)
nba.append(ind)

lac = Team("lac")
lac.setColor1(200, 16, 46)
lac.setColor2(9, 66, 148)
lac.setColor3(190, 192, 194)
nba.append(lac)

lal = Team("lal")
lal.setColor1(85, 37, 130)
lal.setColor2(253, 185, 39)
lal.setColor3(6, 25, 34)
nba.append(lal)

mem = Team("mem")
mem.setColor1(93, 118, 169)
mem.setColor2(18, 23, 63)
mem.setColor3(255, 187, 34)
nba.append(mem)

mia = Team("mia")
mia.setColor1(152, 0, 46)
mia.setColor2(249, 160, 27)
mia.setColor3(6, 25, 34)
nba.append(mia)

mil = Team("mil")
mil.setColor1(0, 71, 27)
mil.setColor2(240, 235, 210)
mil.setColor3(0, 125, 197)
nba.append(mil)

min = Team("min")
min.setColor1(12, 35, 64)
min.setColor2(35, 97, 146)
min.setColor3(158, 162, 162)
nba.append(min)

nop = Team("nop")
nop.setColor1(0, 22, 65)
nop.setColor2(225, 58, 62)
nop.setColor3(180, 151, 90)
nba.append(nop)

nyk = Team("nyk")
nyk.setColor1(0, 107, 182)
nyk.setColor2(245, 132, 38)
nyk.setColor3(190, 192, 194)
nba.append(nyk)

okc = Team("okc")
okc.setColor1(0, 125, 195)
okc.setColor2(239, 59, 36)
okc.setColor3(0, 45, 98)
nba.append(okc)

orl = Team("orl")
orl.setColor1(0, 125, 197)
orl.setColor2(196, 206, 211)
orl.setColor3(6, 25, 34)
nba.append(orl)

phi = Team("phi")
phi.setColor1(0, 107, 182)
phi.setColor2(237, 23, 76)
phi.setColor3(0, 43, 92)
nba.append(phi)

phx = Team("phx")
phx.setColor1(29, 17, 96)
phx.setColor2(229, 95, 32)
phx.setColor3(6, 25, 34)
nba.append(phx)

por = Team("por")
por.setColor1(224, 58, 62)
por.setColor2(6, 25, 34)
por.setColor3(255, 255, 255)
nba.append(por)

sac = Team("sac")
sac.setColor1(91, 43, 130)
sac.setColor2(99, 113, 122)
sac.setColor3(6, 25, 34)
nba.append(sac)

sas = Team("sas")
sas.setColor1(196, 206, 211)
sas.setColor2(6, 25, 34)
nba.append(sas)

tor = Team("tor")
tor.setColor1(206, 17, 65)
tor.setColor2(6, 25, 34)
tor.setColor3(161, 161, 164)
nba.append(tor)

uta = Team("uta")
uta.setColor1(0, 43, 92)
uta.setColor2(0, 71, 27)
uta.setColor3(249, 160, 27)
nba.append(uta)

was = Team("was")
was.setColor1(0, 43, 92)
was.setColor2(227, 24, 55)
was.setColor3(196, 206, 212)
nba.append(was)


# print(atl.color1)
# print(atl.color2)
# print(atl.color3)
