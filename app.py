import tkinter as tk
from tkinter import ttk
from autotune_ai.engine import AudioEngine
from autotune_ai.pitch import KEY_NAMES

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoTune AI")
        self.geometry("980x560")
        self.configure(bg="#10131a")
        self.engine=AudioEngine(); self.running=False
        self._ui(); self.after(80,self._poll); self.protocol("WM_DELETE_WINDOW",self._close)

    def _ui(self):
        top=tk.Frame(self,bg="#151922",height=180); top.pack(fill="x",padx=10,pady=10)
        self.bars=[]
        for i,n in enumerate(["Nhạc","Mic","Delay","Verb 1","Verb 2","Verb 3","Âm","Sáng","Bè","Retune","FlexTune"]):
            f=tk.Frame(top,bg="#171c25",width=78,height=160); f.pack(side="left",padx=3,pady=8); f.pack_propagate(False)
            c=tk.Canvas(f,bg="#171c25",highlightthickness=0); c.pack(fill="both",expand=True)
            c.create_rectangle(29,40,49,135,fill="#252b35",outline="")
            it=c.create_rectangle(29,115,49,135,fill="#22c7d7",outline="")
            tk.Label(f,text=n,bg="#171c25",fg="#b9bec8",font=("Segoe UI",9)).pack()
            self.bars.append((c,it))
        body=tk.Frame(self,bg="#10131a"); body.pack(fill="both",expand=True,padx=25)
        tk.Label(body,text="AUTOTUNE AI",bg="#10131a",fg="#5ed9ee",font=("Segoe UI",24,"bold")).grid(row=0,column=0,columnspan=4,pady=8)
        self.key_label=tk.Label(body,text="AI Tone: --",bg="#10131a",fg="white",font=("Segoe UI",16,"bold"))
        self.key_label.grid(row=1,column=0,columnspan=2,sticky="w")
        self.key=tk.StringVar(value="A"); self.scale=tk.StringVar(value="Minor")
        tk.Label(body,text="Tone thủ công",bg="#10131a",fg="#9ea6b3").grid(row=2,column=0,sticky="w")
        ttk.Combobox(body,textvariable=self.key,values=KEY_NAMES,state="readonly",width=8).grid(row=3,column=0,sticky="w")
        ttk.Combobox(body,textvariable=self.scale,values=["Major","Minor"],state="readonly",width=10).grid(row=3,column=1,sticky="w")
        self.auto=tk.BooleanVar(value=True)
        tk.Checkbutton(body,text="Tự dò tone liên tục",variable=self.auto,bg="#10131a",fg="#72e2ef",
                       selectcolor="#202631",activebackground="#10131a").grid(row=2,column=2,columnspan=2,sticky="e")
        self.btn=tk.Button(body,text="▶  BẬT MIC",command=self._toggle,bg="#174f5b",fg="white",
                           relief="flat",font=("Segoe UI",12,"bold"),padx=20,pady=10)
        self.btn.grid(row=4,column=0,columnspan=2,sticky="ew",pady=22)
        self.status=tk.Label(body,text="Sẵn sàng",bg="#10131a",fg="#8f98a6"); self.status.grid(row=4,column=2,columnspan=2,sticky="e")
        self.retune=tk.DoubleVar(value=18); self.mix=tk.DoubleVar(value=100); self.flex=tk.DoubleVar(value=50)
        for row,(name,var,lo,hi) in enumerate([("Retune",self.retune,5,80),("Mix",self.mix,0,100),("FlexTune",self.flex,0,100)],5):
            tk.Label(body,text=name,bg="#10131a",fg="#b9bec8").grid(row=row,column=0,sticky="w")
            ttk.Scale(body,from_=lo,to=hi,variable=var,orient="horizontal",command=lambda _:self._sync()).grid(row=row,column=1,columnspan=3,sticky="ew")

    def _sync(self):
        self.engine.retune=float(self.retune.get()); self.engine.mix=float(self.mix.get())/100
        self.engine.flex=float(self.flex.get())/100; self.engine.auto_detect=self.auto.get()

    def _toggle(self):
        if not self.running:
            try:
                self._sync(); self.engine.start(); self.running=True
                self.btn.config(text="■  TẮT MIC",bg="#63343b"); self.status.config(text="Đang nghe mic…",fg="#70e0ed")
            except Exception as e: self.status.config(text="Lỗi: "+str(e),fg="#ff8080")
        else:
            self.engine.stop(); self.running=False; self.btn.config(text="▶  BẬT MIC",bg="#174f5b"); self.status.config(text="Đã tắt")

    def _poll(self):
        x=self.engine.latest
        if x:
            if x.get("key"): self.key_label.config(text=f"AI Tone: {x['key']} {x.get('scale','')}")
            level=min(1,float(x.get("rms",0))*4)
            for i,(c,it) in enumerate(self.bars):
                h=10+int(level*85); c.coords(it,29,135-h,49,135)
        self.after(80,self._poll)

    def _close(self):
        self.engine.stop(); self.destroy()

if __name__=="__main__": App().mainloop()
