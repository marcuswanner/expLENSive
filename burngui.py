import wx, thread, time

class MainWindow(wx.Frame):
    def __init__(self, parent, ID, title, xsize, ysize):
        self.cellsize = 15 #size of each cell on the screen (in pixels)
        self.x, self.y = xsize, ysize
        self.exiting = False
        wx.Frame.__init__(self, parent, -1, title, size = (self.y*self.cellsize+100, self.x*self.cellsize+100))
        self.Show(True)
        self.pen = wx.ClientDC(self)
        thread.start_new_thread(self.WaitForNewArray, ())

    def OnExit(self):
        self.exiting = True
        time.sleep(0.1)
        self.Close(True)
    
    def NewArray(self, array):
        if self.exiting:
            return
        self.newarray = array

    def WaitForNewArray(self):
        self.newarray = None
        while not self.newarray:
            time.sleep(0.01)
        self.RedrawAll(self.newarray)
        self.oldarray = self.newarray
        self.newarray = None
        while 1:
            if not self.newarray:
                if self.exiting:
                    return
                time.sleep(0.01)
                continue
            newarray = self.newarray
            self.newarray = None
            self.RedrawChanged(newarray, self.oldarray)
            self.oldarray = newarray

    def Paint(self, coords, value, celltype):
        if value < 0:
            color = (celltype*100, 0, 0)
        else:
            color = (value <= 0.5)*(value*512)+(value > 0.5)*255, (value>0.5)*((value-0.5)*512-1), celltype*50
        self.pen.SetPen(wx.Pen(color))
        self.pen.SetBrush(wx.Brush(color))
        self.pen.DrawRectangle(coords[1]*self.cellsize, coords[0]*self.cellsize, self.cellsize, self.cellsize)

    def TargetHit(self, coords):
        self.Paint(coords, -1, 2)
    
    def RedrawAll(self, array):
        for x in range(self.x):
            for y in range(self.y):
                self.Paint((x, y), array[x][y][0], array[x][y][1])
    
    def RedrawChanged(self, array, oldarray):
        needtoredraw = []
        for x in range(self.x):
            for y in range(self.y):
                if array[x][y] != oldarray[x][y]:
                    needtoredraw.append(((x, y), array[x][y][0], array[x][y][1]))
        for cell in needtoredraw:
            self.Paint(cell[0], cell[1], cell[2])

def windowthread(x, y):
    app.MainLoop()

def Initialize(x, y):
    global frame, app
    app = wx.PySimpleApp()
    frame = MainWindow(None, -1, "Visual Explosion Report", x, y)
    thread.start_new_thread(windowthread, (x, y))

def SendArray(array):
    frame.NewArray(array)

def ReportHit(coords):
    frame.TargetHit(coords)

def Finished():
    frame.OnExit()
