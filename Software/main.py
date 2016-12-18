#for gui
import tkinter as tk
#for thingspeak interrogation
import urllib.request
#for response parsing
import re


TITLE_FONT = ("Helvetica", 14, "bold")

# binary for recolte
recolte = 0

temperature = 22
humidite = 30
poids = 0


class ThinspeakDatas():

    def __init__(self, id, apiWrite):
        self.id = id
        self.apiWrite = apiWrite

    def readdata(self):
        strRead = "https://api.thingspeak.com/channels/204207/feeds.json?results=1"
        value = urllib.request.urlopen(strRead).read()
        return value

    #return entry id
    def updatedata(self, data, value):
        strWrite = "https://api.thingspeak.com/update?api_key="+self.apiWrite+"&field"+str(data)+"="+str(value)
        ret = urllib.request.urlopen(strWrite).read()
        return ret

    #return tuples of datas in string form
    def regexdatas(self, rep):
        ret = re.findall("(?:field)([0-9])(?:\":\")([0-9]+)", rep)

        return ret

    def readmaj(self):
        rep = self.readdata()
        rep = str(rep)
        value = self.regexdatas(rep)
        value = tuple(value)
        return value

    # working
    def Recolte(self):
        self.updatedata(4, 1)
        self.recolte = 1

    def finRecolte(self):
        self.updatedata(4, 0)
        self.recolte = 0

class Maya(tk.Tk):

    tsd = ThinspeakDatas(204207, "2HS1MEYTDWZBB2BY")

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.recolte = 0

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Principale, Infos, Reglages, Actions):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        global link
        link = self

        self.title("Maya")
        self.show_frame("Principale")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.updatingall()
        frame = self.frames[page_name]
        frame.tkraise()
        frame.updateall()

    def updatingall(self):

        global temperature
        global humidite
        global recolte
        global poids

        valuetuple = self.tsd.readmaj()

        for id, value in valuetuple:
            #print("id = " + id)
            #print("value = " + value)
            if int(value) > 0:
                if 1 == id:
                    temperature = value
                elif 2 == id:
                    poids = value
                elif 3 == id:
                    humidite = value
                elif 4 == id:
                    recolte = value



class Principale(tk.Frame):

    temp = "erreurT"
    hum = "erreurH"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Maya", font=TITLE_FONT)
        label.grid(row = 0, column = 0)
        self.temp = tk.StringVar()
        self.hum = tk.StringVar()
        button1 = tk.Button(self, text="Informations",
                            command=lambda: controller.show_frame("Infos"))
        button2 = tk.Button(self, text="Reglages",
                            command=lambda: controller.show_frame("Reglages"))
        button3 = tk.Button(self, text="Actions",
                            command=lambda: controller.show_frame("Actions"))
        name_temp = tk.Label(self, text = "Temperature")
        temperature = tk.Label(self, textvariable = self.temp)
        name_humid = tk.Label(self, text = "Humidite")
        humidite = tk.Label(self, textvariable=self.hum)
        btnquit = tk.Button(self, text="Quitter",command=self.quit)

        button1.grid(row = 4, column = 0)
        button2.grid(row = 4, column = 1)
        button3.grid(row = 4, column = 2)

        name_temp.grid(row = 1, column = 1)
        temperature.grid(row = 1, column = 2)
        name_humid.grid(row = 2, column = 1)
        humidite.grid(row=2, column=2)
        btnquit.grid(row=5, column=1)


    def updateall(self):
        global temperature
        global humidite
        global recolte
        global poids

        self.temp.set(str(temperature))
        self.hum.set(str(humidite))
        self.update_idletasks()

class Infos(tk.Frame):

    temp = "erreurT"
    hum = "erreurH"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Informations", font=TITLE_FONT)
        label.grid(row = 0, column = 0)
        button = tk.Button(self, text="Retour", command=lambda: controller.show_frame("Principale"))

        self.temp = tk.StringVar()
        self.hum = tk.StringVar()

        name_temp = tk.Label(self, text="Temperature")
        temperaturelab = tk.Label(self, textvariable = self.temp)
        name_humid = tk.Label(self, text="Humidite")
        humiditelab = tk.Label(self, textvariable = self.hum)

        button.grid(row = 3, column = 1)
        name_temp.grid(row=1, column=0)
        temperaturelab.grid(row=1, column=1)
        name_humid.grid(row=2, column=0)
        humiditelab.grid(row=2, column=1)

    def updateall(self):
        global temperature
        global humidite
        global recolte
        global poids

        print(str(temperature) + " " + str(humidite))
        self.temp.set(str(temperature))
        self.hum.set(str(humidite))
        self.update_idletasks()


class Reglages(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Reglages", font=TITLE_FONT)
        label.grid(row = 0, column = 0)
        button = tk.Button(self, text="Retour",
                           command=lambda: controller.show_frame("Principale"))
        button.grid(row = 2, column = 1)

    def updateall(self):
        global temperature
        global humidite
        global recolte
        global poids


class Actions(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Actions", font=TITLE_FONT)
        label.grid(row = 0, column = 0)
        button = tk.Button(self, text="Retour",
                           command=lambda: controller.show_frame("Principale"))

        tsd = ThinspeakDatas(204207, "2HS1MEYTDWZBB2BY")

        recolte = tk.Button(self, text = "Recolte", command = lambda: tsd.Recolte())

        button.grid(row = 2, column = 1)
        recolte.grid(row = 1, column = 0)

    def updateall(self):
        global temperature
        global humidite
        global recolte
        global poids


if __name__ == "__main__":
    app = Maya()
    app.mainloop()





