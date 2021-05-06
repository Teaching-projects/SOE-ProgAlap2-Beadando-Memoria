#-----------------------------------------------------------------------------
#
#	
#       
#      Memory kirakó
#
#-----------------------------------------------------------------------------
#	
import os, random
from tkinter import *

kepek = "Pict"   # a képeket tartalmazó könyvtár neve
    
class Draw(Frame):
    #A program ablakát definiáló osztály
    def __init__(self):
        
        Frame.__init__(self)
        # A vászon létrehozása:
        Label(self, text ='Memóri teszt').pack(side=TOP, padx=40)
        self.hatterszin = 'gray77'
        self.canvas = Canvas(self, width =600, height =700, bg = self.hatterszin)
        self.canvas.pack(padx =5, pady =3)
        # Az <egéresemények> hozzákapcsolása a (vászon) widget-hez :
        self.canvas.bind("<Button1-ButtonRelease>", self.mouseLeft)
        self.pack()
        self.ld=os.listdir(kepek)+os.listdir(kepek) # betölti a képeket kétszer egymás után
        random.shuffle(self.ld)                    # megkeveri
        self.Leoszt()                          # lerakja a kártyákat a hátlapjukkal

    def Leoszt(self):
    # lerakja a 36 kártyát
        self.hatlapok = []
        self.back = PhotoImage(file ="hatlap.gif")
        for y in range(6):
            for x in range(6):
                v =self.canvas.create_image(50+100*x,50+100*y, image = self.back)
                self.hatlapok.append(v)
        self.canvas.create_text(50,650, text='Próbálkozások száma:', anchor=W, fill = "black", font=('Arial', 24 )) # eredmény mező
        self.erdmeny = self.canvas.create_text(500,650, text='0', fill = "black", font=('Arial', 24))
        self.flag = 0      # az egér bal fülének lenyomását jelző flag
        self.elag = 0      # 0: alap, 1: egy lap felforgatva, 2: 2 lap felforgatva, 3: várunk
        self.megt = []     # a megtalált objektumok listája
        self.sec = 250
        self.proba = 0     # próbálkozások száma
        self.Kep_kitesz()  # végtelen ciklusban forgatja a kiválasztott lapot


    def Kep_kitesz(self):
    # Ha a flag 1, akkor kirakja a kiválasztott kártyát, majd vár egy másodpercet
        if self.elag == 3:
            self.canvas.delete(self.v1)       # eltunik az elso felfortditott
            self.canvas.delete(self.v2)       # eltunik a második felfortditott
            self.proba = self.proba +1 
            self.canvas.itemconfig(self.erdmeny, text='%s'% (self.proba))
            if self.ld[self.elso[2]] == self.ld[self.k[2]]:  # ha ugyanazt ábrázolja az elso és a második
                self.canvas.delete(self.hatlapok[self.elso[2]])
                self.canvas.delete(self.hatlapok[self.k[2]])
                self.megt.append(self.k[2])     # berakom a megtaláltak közé
                self.megt.append(self.elso[2])  # berakom a megtaláltak közé
                if len(self.megt)==36:           # itt a vége
                    print("Itt a vége!!!",self.proba)
                    self.Jatek_vege()
            self.sec = 250
            self.elag = 0
        if self.elag == 2:             # második után
            self.sec = 1000
            self.elag = 3
            
        if self.flag == 1:              # Ha lenyomták a bal gombot
            self.sec = 250
            if self.elag == 1:         # Első után
                if self.k[2] != self.elso[2]: # Kizárjuk, ha ugyanarra kétszr klikkel
                    self.v2 =self.canvas.create_image(50+self.k[0],50+self.k[1], image = self.k[3])
                    self.elag = 2
            elif self.elag == 0:         # Alap eset
                self.v1 =self.canvas.create_image(50+self.k[0],50+self.k[1], image = self.k[3])
                self.elso = self.k
                self.elag = 1
            self.flag = 0
        self.after(self.sec,self.Kep_kitesz) # várunk egy ideig (saját magát hívja)

    def Jatek_vege(self):
        if self.proba > 70:
            self.canvas.create_text(300,300, text='Van mit gyakorolnod!', anchor=CENTER, fill = "black", font=('Arial', 24 ))
        elif self.proba > 60:
            self.canvas.create_text(300,300, text='Lehetne jobb is!!', anchor=CENTER, fill = "green", font=('Arial', 24 ))
        elif self.proba > 50:
            self.canvas.create_text(300,300, text='Nem rossz!', anchor=CENTER, fill = "blue", font=('Arial', 24 ))
        elif self.proba > 40:
            self.canvas.create_text(300,300, text='Bíztató kezdet!', anchor=CENTER, fill = "braun", font=('Arial', 24 ))
        elif self.proba > 30:
            self.canvas.create_text(300,300, text='Ez már egész jó!', anchor=CENTER, fill = "cyan", font=('Arial', 24 ))
        elif self.proba > 20:
            self.canvas.create_text(300,300, text='Gratulálok!', anchor=CENTER, fill = "red", font=('Arial', 24 ))
        else:
            self.canvas.create_text(300,300, text='Gyanús vagy, nem csaltál?', anchor=CENTER, fill = "gray", font=('Arial', 24 ))


    def mouseLeft(self,event):
        if self.elag != 3:
            xkoord = event.x-event.x%100  # a cursor x koordinátájából kiszámítja a kép x-ét
            ykoord = event.y-event.y%100  # a cursor y koordinátájából kiszámítja a kép y-át
            pic_num =int(6*(ykoord/100)+xkoord/100) # a koordinátákból kiszámítja a képszámot
            if pic_num not in self.megt:    # ha még nem találták meg
                pic_name = PhotoImage(file =kepek+"\\"+self.ld[pic_num]) # a kép neve
                self.k = xkoord,ykoord,pic_num,pic_name                  # kép attributumai
                self.flag = 1
          
            
if __name__ == '__main__':
    Draw().mainloop()

