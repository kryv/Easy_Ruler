# EASY RULER
# Auther Kei Fukushima, 2014

import wx

ruler_color = "#FFFFFF"
ruler_square = (440,440)
ruler_landscape = (540,40)
ruler_portrait = (40,540)
ruler_init_pos = (400,400)
ruler_transparent = 150
ruler_interval = 50
ruler_line_color = "#505050"
ruler_line_width = 1
ruler_maxsize = (2000,2000)

exec open("default_values.txt").read().replace("\n",";")

class MainFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, -1, "Easy Ruler", 
                         style=wx.NO_BORDER | wx.STAY_ON_TOP) 
        panel = MousePanel(self) 
        self.SetSize(ruler_square)
        self.SetPosition(ruler_init_pos)
        self.SetTransparent(ruler_transparent)
        panel.Bind(wx.EVT_PAINT, self.OnPaint)
        panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyMove)

    def OnPaint(self,event) :
        dc = wx.PaintDC(event.GetEventObject())
        self.ThinLines(dc)
        self.Labels(dc)

    def ThinLines(self,dc) :
        dc.SetPen(wx.Pen(ruler_line_color, ruler_line_width))
        for i in range(20,ruler_maxsize[0]+1,ruler_interval):
         dc.DrawLine(-10, i, ruler_maxsize[0]+20, i)
        for j in range(20,ruler_maxsize[1]+1,ruler_interval):
         dc.DrawLine(j, -10, j, ruler_maxsize[1]+20)


    def Labels(self,dc) :
        font =  dc.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        n,m = 0,1
        for i in range(23,ruler_maxsize[0]+1,ruler_interval):
         dc.DrawText(str(n),i,21)
         n+=1
        for i in range(ruler_interval+21,ruler_maxsize[1]+1,ruler_interval):
         dc.DrawText(str(m),23,i)
         m+=1

    def OnKeyMove(self, event) :
        global ruler_interval
        tmp = event.GetKeyCode()
        pos = self.GetPosition()
        idic = dict([[ord(str(i)),i*10] for i in range(10)]+[[ord(str(0)),100]]) 
        if tmp == ord("W") :
            self.Move((pos.x,pos.y-1))
        if tmp == ord("S") :
            self.Move((pos.x,pos.y+1))
        if tmp == ord("A") :
            self.Move((pos.x-1,pos.y))
        if tmp == ord("D") :
            self.Move((pos.x+1,pos.y))
        if tmp in idic :
            ruler_interval = idic[tmp]
            self.Show(False); self.Show(True)
        if tmp == ord("Q") :
            ruler_interval += 1
            self.Show(False); self.Show(True)
        if tmp == ord("E") :
            if ruler_interval > 5:
             ruler_interval -= 1
             self.Show(False); self.Show(True)


class MousePanel(wx.Panel): 
    def __init__(self, parent): 
        wx.Panel.__init__(self, parent, -1) 
        self.rightDown = False 
        self.leftDown = False 
        self.sqmode = 1
        self.posd = (0,0)
        self.parentFrame = parent
        while self.parentFrame.GetParent() is not None: 
            self.parentFrame = self.parentFrame.GetParent() 

        wx.EVT_RIGHT_DOWN(self, self.OnRightDown) 
        wx.EVT_RIGHT_UP(self, self.OnRightUp) 
        wx.EVT_LEFT_DOWN(self, self.OnLeftDown) 
        wx.EVT_LEFT_UP(self, self.OnLeftUp) 
        wx.EVT_MOTION(self, self.OnMouseMove)

    def OnRightDown(self, evt): 
        self.CaptureMouse() 
        self.rightDown = True 
        origin = self.parentFrame.GetPosition() 
        dx = origin.x
        dy = origin.y
        self.deltaR = wx.Point(dx, dy) 


    def OnRightUp(self, evt): 
        self.ReleaseMouse()
        self.RightDown = False
        if self.leftDown == True:
          self.parentFrame.Close() 


    def OnLeftDown(self, evt): 
        self.CaptureMouse() 
        self.leftDown = True 
        pos = self.ClientToScreen(evt.GetPosition()) 
        origin = self.parentFrame.GetPosition() 
        dx = pos.x - origin.x 
        dy = pos.y - origin.y
        self.posd = pos
        self.deltaL = wx.Point(dx, dy) 


    def OnLeftUp(self, evt): 
        self.ReleaseMouse() 
        self.leftDown = False
        pos = self.ClientToScreen(evt.GetPosition()) 
        if pos == self.posd and self.sqmode%3 == 0:
              self.sqmode = self.sqmode + 1
              self.parentFrame.SetSize(ruler_square)
        elif pos == self.posd and self.sqmode%3 == 1:
              self.sqmode = self.sqmode + 1
              self.parentFrame.SetSize(ruler_landscape)
        elif pos == self.posd and self.sqmode%3 == 2:
              self.sqmode = self.sqmode + 1
              self.parentFrame.SetSize(ruler_portrait)


    def OnMouseMove(self, evt): 
        if evt.Dragging() and self.leftDown: 
            pos = self.ClientToScreen(evt.GetPosition()) 
            fp = (pos.x - self.deltaL.x, pos.y - self.deltaL.y)
            self.parentFrame.Move(fp) 
        elif evt.Dragging() and self.rightDown : 
            pos = self.ClientToScreen(evt.GetPosition()) 
            sz = (pos.x - self.deltaR.x, pos.y - self.deltaR.y) 
            if sz[0] < 0 and sz[1] < 0 : 
                 np = (self.deltaR.x + sz[0], self.deltaR.y + sz[1])
                 self.parentFrame.Move(np)
            elif sz[0] < 0 : 
                np = (self.deltaR.x + sz[0], self.deltaR.y)
                self.parentFrame.Move(np) 
                if sz[1] < 0 : 
                 np = (self.deltaR.x + sz[0], self.deltaR.y + sz[1])
                 self.parentFrame.Move(np)
            elif sz[1] < 0 : 
                np = (self.deltaR.x, self.deltaR.y + sz[1])
                self.parentFrame.Move(np) 
                if sz[0] < 0  : 
                 np = (self.deltaR.x + sz[0], self.deltaR.y + sz[1])
                 self.parentFrame.Move(np)
            if abs(sz[0]) < 40 : sz=(40,abs(sz[1]))
            if abs(sz[1]) < 40 : sz=(abs(sz[0]),40)
            self.parentFrame.SetSize((abs(sz[0]),abs(sz[1])))

app = wx.PySimpleApp() 
frame = MainFrame() 
frame.Show() 
app.MainLoop()