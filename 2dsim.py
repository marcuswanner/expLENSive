class ReactiveCell():
    def __init__(self, burnticks, givetogui):
        self.guiinfo = givetogui
        self.burnticks = burnticks * 1.41421356#sqrt(2)
        self.isburning = False
        self.ischarred = False
        self.burntime = 0
        if self.burnticks < 0:
            #Is a detonator cell, so already "burnt"
            self.ischarred = True

    def Tick(self):
        if self.isburning:
            self.burntime = self.burntime + 1
            if self.burntime > self.burnticks:
                self.isburning = False
                self.ischarred = True

    def SetOnFire(self):
        if self.isburning or self.ischarred:
            return
        self.isburning = True

    def IsBurnt(self):
        return (self.burntime > self.burnticks / 1.41421356)#sqrt(2)

    def DiagIsBurnt(self):
        return self.ischarred

    def GetDisplayInfo(self):
        #result is sent to gui thread
        ret = self.burntime/float(self.burnticks)
        if ret > 1:
            ret = 1
        return (ret, self.guiinfo)

class InertCell():
    def __init__(self, reportdata, givetogui):
        self.guiinfo = givetogui
        self.reportdata = reportdata
        self.isreached = False #this variable is public

    def Tick(self):
        return

    def SetOnFire(self):
        if self.isreached:
            return
        #do what it was told to do when hit
        exec(self.reportdata[2])
        self.isreached = True

    def IsBurnt(self):
        return False

    def DiagIsBurnt(self):
        return False

    def GetDisplayInfo(self):
        return (-1, self.guiinfo)

class Field():
    def __init__(self, xsize, ysize, cells):
        self.gui = True
        if self.gui:
            import burngui as guimodule
            self.guimodule = guimodule
            self.guimodule.Initialize(xsize, ysize)
        self.xsize = xsize
        self.ysize = ysize
        self.array = []
        self.targetstoburn = 0
        for x in range(xsize):
            row = []
            for y in range(ysize):
                cellsymbol = cells[x][y]
                if cellsymbol == '1':
                    row.append(ReactiveCell(int(100000000/(6900*100.0)), 2))
                if cellsymbol == '2':
                    row.append(ReactiveCell(int(100000000/(4900*100.0)), 4))
                if cellsymbol == 'D':
                    row.append(ReactiveCell(-1, 5))
                if cellsymbol == 'T':
                    row.append(InertCell((self, (True, (x, y)), 'self.reportdata[0].ReportTargetHit(self.reportdata[1])'), 3))
                    self.targetstoburn = self.targetstoburn + 1
                if cellsymbol == 'W' or cellsymbol == ' ':
                    row.append(InertCell((self, (False, (0, 0)), ''), 1))
            self.array.append(row)

    def CheckNeighbors(self, x, y):
        #returns the number of neighbors burnt
        #x and y should be within bounds of self.array
        count = 0
        xminus1 = x-1
        xplus1 = x+1
        yminus1 = y-1
        yplus1 = y+1
        if xminus1 < 0: xminus1 = 0
        if xplus1 > self.xsize-1: xplus1 = self.xsize-1
        if yminus1 < 0: yminus1 = 0
        if yplus1 > self.ysize-1: yplus1 = self.ysize-1
        count = count + self.array[x][yplus1].IsBurnt()
        count = count + self.array[x][yminus1].IsBurnt()
        count = count + self.array[xplus1][yplus1].DiagIsBurnt()
        count = count + self.array[xplus1][y].IsBurnt()
        count = count + self.array[xplus1][yminus1].DiagIsBurnt()
        count = count + self.array[xminus1][yplus1].DiagIsBurnt()
        count = count + self.array[xminus1][y].IsBurnt()
        count = count + self.array[xminus1][yminus1].DiagIsBurnt()
        return count                                                                  
    
    def Calculate(self):
        self.tickcount = 0
        self.targetsburned = 0
        self.log = []
        while self.targetsburned != self.targetstoburn:
            if self.gui:
                guiarray = []
                for x in range(self.xsize):
                    guiline = []
                    for y in range(self.ysize):
                        guiline.append(self.array[x][y].GetDisplayInfo())
                    guiarray.append(guiline)
                self.guimodule.SendArray(guiarray)
            for x in range(self.xsize):
                for y in range(self.ysize):
                    cell = self.array[x][y]
                    neighbors = self.CheckNeighbors(x, y)
                    if neighbors > 0:
                        cell.SetOnFire()
                    cell.Tick()
            self.tickcount = self.tickcount + 1
        if self.gui: self.guimodule.Finished()
        return self.log

    def ReportTargetHit(self, args):
        #This function is meant to be called by inert cells
        #when they are hit. See InertCell.SetOnFire().
        if not args[0]:
            #Target cells are given a True for this value;
            #Non-target cells are given a False.
            return
        self.log.append((self.tickcount*10, args[1]))
        if self.gui: self.guimodule.ReportHit(args[1])
        self.targetsburned = self.targetsburned + 1

import sys
if len(sys.argv) > 1: infilename = sys.argv[1]
else: infilename = 'test.el2'
infile = open(infilename, 'r')
lines = []
linelength = 0
while 1:
    line = infile.readline()
    if len(line) < 1:
        break
    if line[len(line)-1] == '\n':
        line = line[:len(line)-1]
    if not linelength: #use the first line length as the length of all the others
        linelength = len(line)
    line = line + ' ' * (linelength-len(line))
    lines.append(line)
charge = Field(len(lines), len(lines[0]), lines)
result = charge.Calculate()
timevalues = []
for i in result:
    print i
    timevalues.append(i[0])
print max(timevalues)-min(timevalues)
infile.close()
