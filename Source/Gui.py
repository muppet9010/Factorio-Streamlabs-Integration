import tkinter as TK


class GuiWindow():
    def __init__(self, state):
        root = TK.Tk()
        root.minsize(500, 400)
        self.State = state
        self.Gui = Gui(state, master=root)


class Gui(TK.Frame):
    def __init__(self, state, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.State = state
        self.Logging = state.Logging
        self.Obs = state.Obs
        self.CreateWidgets()

    def CreateWidgets(self):
        self.CreateStreamlabs(self.master)
        self.CreateActivityLog(self.master)
        self.CreateBottomBar(self.master)

    def CreateStreamlabs(self, parent):
        self.statusContainer = TK.Frame(parent)
        self.statusContainer.pack(fill=TK.X, side=TK.TOP)

        self.statusText = TK.StringVar()
        self.UpdateStatus()
        statusLabel = TK.Label(
            self.statusContainer, textvariable=self.statusText, height=1, width=30)
        statusLabel.pack(side=TK.LEFT)

        startButton = TK.Button(self.statusContainer)
        startButton["text"] = "Start"
        startButton["command"] = self.Start
        startButton.pack(side=TK.LEFT)

        stopButton = TK.Button(self.statusContainer)
        stopButton["text"] = "Stop"
        stopButton["command"] = self.Stop
        stopButton.pack(side=TK.LEFT)

    def CreateActivityLog(self, parent):
        titleFrame = TK.LabelFrame(parent, text="Activity Log")
        titleFrame.pack(fill=TK.BOTH, expand=True, side=TK.TOP, padx=3, pady=3)
        yScroll = TK.Scrollbar(titleFrame, orient=TK.VERTICAL)
        yScroll.pack(fill=TK.Y, expand=True, side=TK.RIGHT)
        self.activityLogText = TK.Text(
            titleFrame, height=5, wrap=TK.WORD, yscrollcommand=yScroll.set, state=TK.DISABLED)
        self.activityLogText.pack(fill=TK.BOTH, expand=True, side=TK.LEFT)

    def CreateBottomBar(self, parent):
        self.bottomBarContainer = TK.Frame(parent)
        self.bottomBarContainer.pack(fill=TK.X, side=TK.TOP)

        quitButton = TK.Button(self.bottomBarContainer, text="QUIT", fg="red",
                               command=self.Quit)
        quitButton.pack(side=TK.LEFT)

    def Quit(self):
        self.Logging.Log("Quit Button")
        self.Obs.Disconnect()
        self.master.destroy()

    def UpdateStatus(self):
        if self.Obs.connecting:
            self.statusText.set("OBS Connecting")
        elif self.Obs.sio.eio.state == "connected":
            self.statusText.set("Running")
        else:
            self.statusText.set("Stopped")

    def AddToActivityLog(self, text):
        self.Logging.Log(text)
        self.activityLogText.configure(state="normal")
        self.activityLogText.insert(
            1.0, self.Logging.TimestampText(text) + "\n")
        self.activityLogText.configure(state="disabled")

    def Start(self):
        self.Logging.DebugLog("Start Button")
        if not self.State.Currency.GetRates():
            self.Logging.Log("Error: Get Rates for Currency failed")
            return
        self.Obs.Connect()
        self.UpdateStatus()

    def StartPostObsConnection(self):
        self.Obs.connecting = False
        self.UpdateStatus()
        self.AddToActivityLog("Started")

    def Stop(self):
        self.Logging.DebugLog("Stop Button")
        self.Obs.Disconnect()
        self.AddToActivityLog("Stopped")
