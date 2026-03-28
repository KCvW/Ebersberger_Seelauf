'''
Created on 23.03.2024
modified last on 13.03.2026

@author: Dr. Wilhelm Kusian
'''
import tkinter
from tkinter import ttk
import socket

class Message(tkinter.Frame):
    """
    Definiert das Ausgabefeld für die Meldung, die Breite wird über die Textlänge selbst bestimmt
    parent        = uebergeordnetes Fensterelement
    zeile         = Zeile im Grid von Parent, in der die Meldung steht,begonnen von links mit 0
    spalte        = Spalte im Grid von Parent, in der die Meldung steht,begonnen von oben mit 0
    zeilenspanne  = Angabe, über wie viele Zeilen sich die Schaltfläche ausdehnen soll
    spaltenspanne = Angabe, über wie viele Spalten sich die Schaltfläche ausdehnen soll
    ausrichtung   = Ausrichtung innerhalb der Zelle gemäß Himmelsrichtung (W, N, E, S)
    titel         = auszugebender Text
    size          = Textgröße   
    """
    def __init__(self, parent, zeile, spalte, zeilenspanne, spaltenspanne, ausrichtung, titel, size):    # Konstruktur für die Klasse
        super().__init__(parent)                                                                         # automatisch korrekte Basisklasse ermitteln
        
        anzeige = tkinter.Label(parent, width=len(titel), text=titel, font="Arial " + size)
        anzeige.grid(row=zeile, column=spalte, sticky=ausrichtung, rowspan=zeilenspanne, columnspan=spaltenspanne)


class Schaltflaeche(tkinter.Frame):
    """
    Erzeugung eiener Schaltflaeche in einem Fenster mit folgenden Parametern:
    parent        = uebergeordnetes Fensterelement
    zeile         = Zeile im Grid von Parent, in der die Meldung steht,begonnen von links mit 0
    spalte        = Spalte im Grid von Parent, in der die Meldung steht,begonnen von oben mit 0
    zeilenspanne  = Angabe, über wie viele Zeilen sich die Schaltfläche ausdehnen soll
    spaltenspanne = Angabe, über wie viele Spalten sich die Schaltfläche ausdehnen soll
    ausrichtung   = Ausrichtung innerhalb der Zelle gemäß Himmelsrichtung (W, N, E, S)
    titel         = auszugebender Text
    size          = Textgröße   
    """
    def __init__(self, parent, zeile, spalte, zeilenspanne, spaltenspanne, ausrichtung, titel, cmd):     # Konstruktur für die Klasse
        super().__init__(parent)                                                                         # automatisch korrekte Basisklasse ermitteln
        
        # Buttondefinition und definitionvon Größe und Position
        flaeche = tkinter.Button(parent, text=titel, command=cmd)
        flaeche.grid(row=zeile, column=spalte, sticky=ausrichtung, rowspan=zeilenspanne, columnspan=spaltenspanne)

class Input(tkinter.Frame):
    """
    Definiert das Eingabefeld für einzeilige Texteingaben
    Parent        = uebergeordnetes Fensterelement
    Breite        = Breite des Ausgabefeldes in Zeichen
    Zeile         = Zeile im Grid von Parent, in der die Meldung steht,begonnen von links mit 0
    Spalte        = Spalte im Grid von Parent, in der die Meldung steht,begonnen von oben mit 0
    Ausrichtung   = Ausrichtung innerhalb der Zelle gemäß Himmelsrichtung (W, N, E, S)
    Zeilenspanne  = Angabe, über wie viele Zeilen sich die Schaltfläche ausdehnen soll
    Spaltenspanne = Angabe, über wie viele Spalten sich die Schaltfläche ausdehnen soll
    value         = auszugebender Text
    cmd           = auszuführender Befehl
    """
    def __init__(self, parent, Breite, Zeile, Spalte, Ausrichtung, Zeilenspanne, Spaltenspanne, value, cmd):  # Konstruktur für die Klasse
        super().__init__(parent)                                                                              # automatisch korrekte Basisklasse ermitteln

        # Definition und Initialisierung der Attribute
        self.parent = parent
        self.breite = Breite
        self.zeile = Zeile
        self.spalte = Spalte
        self.ausrichtung = Ausrichtung
        self.zeilenspanne = Zeilenspanne
        self.spaltenspanne = Spaltenspanne
        self.cmd = cmd
        self.ergebnis = tkinter.StringVar()
        self.ergebnis.set(value)
 
        self.input()
 
    def input(self):
        eingabe = tkinter.Entry(self.parent, width=self.breite, textvariable=self.ergebnis, justify='left')
        eingabe.grid(row=self.zeile, column=self.spalte, sticky=self.ausrichtung, rowspan=self.zeilenspanne, columnspan=self.spaltenspanne)
        self.ergebnis.get()
        eingabe.bind('<Return>', self.cmd)                            # Wenn Return gedrückt wird, wird diese Funktion verlassen 
        eingabe.bind('<KP_Enter>', self.cmd)                          # Wenn Enter gedrückt wird, wird diese Funktion verlassen 

def action():
    if Decoder_action.get() == 'active':
        nachricht = "PASSINGS\r\n"                                    # aktuelle Anzahl von Passingdaten
        s.send(nachricht.encode())
        antwort = s.recv(1024)                                        # Rueckmeldung von Decoder abrufen
        string = antwort.decode()
        string = string.rstrip('\r\n')                                # \r\n am Ende entfernen
        passing = string.split(";")                                   # Meldung in Bestandteile aufteilen
        finisher = int(passing[1])                                    # aktuelle Anzahl in finisher ablegen
        if finisher > Merker_Finish.get():                            # erst, wenn neue Finisher vorhanden sind, weiter machen
            k = Merker_Finish.get()
            while k < finisher:                                       # alle vorhandenen neuen Passingfiles auslesen
                k=k+1
                nachricht = str(k)+"\r\n"
                s.send(nachricht.encode())                            # k-tes Passingfile auslesen
                antwort = s.recv(1024)
                print(antwort)
                CRLF = s.recv(1024)                                   # 2. \r\n (=CrLf) abrufen
                print(CRLF)
                file = antwort.decode()
                table_value = []
                file = file.rstrip('\r\n')                            # \r\n am Ende entfernen
                file_list = file.split(";")
                table_value.append(file_list[0])
                table_value.append(file_list[1])
                table_value.append(file_list[3])
                table.insert("", 'end', values=(table_value))
                table.yview(int(file_list[0]))                        # Textfeld immer auf lezte Zeile scrollen
        Merker_Finish.set(finisher)                                   # Zählvariable auf aktuelle Anzahl der Passingfiles setzen
        decoder.after(500, action)                                    # nach 500ms wieder action() aufrufen
        
def start():
    Merker_Finish.set(0)                                              # Initialisierung der Merkvariable fuer die Finisher
    if Decoder_Status.get() == 'verbunden':                           
        nachricht = "STARTOPERATION\r\n"                              # Switch Decoder von Test Mode zu Operation Mode
        s.send(nachricht.encode())
        antwort = s.recv(1024)                                        # Rueckmeldung vom Decoder abrufen
        string = antwort.decode()
        string = string.rstrip('\r\n')
        string = string.split(";")
        if string[1] == 'OK':                                         # wenn Rueckmeldung 'OK', dann
            Decoder_action.set('active')                              # setzen, dass der Decoder nun aktiv ist
            nachricht = "GETSTATUS\r\n"                               # Decoderstatus abrufen
            s.send(nachricht.encode())
            antwort = s.recv(1024)
            string = antwort.decode()
            string = string.rstrip('\r\n')
            string = string.split(";")
            Passingfile.set(string[6])                                # Nummer fuer aktuelles Passingfile setzen und anzeigen
            Message(decoder, 1, 2, 1, 2, 'w', Passingfile.get(), '10')
            
        Messung = tkinter.Label(decoder, text='\nMessung läuft\n', bg='green', font='Arial 12')
        Messung.grid(row=22, column=1, sticky='WNES', rowspan=3, columnspan=14)
        action()
                
def stop():
    if Decoder_Status.get() == 'verbunden':                           
        nachricht = "STOPOPERATION\r\n"                               # Switch Decoder von Operation Mode zu Test Mode
        s.send(nachricht.encode())
        antwort = s.recv(1024)

    Decoder_action.set('idle')                                        # setzen, dass der Decoder nun inaktiv ist
    Messung = tkinter.Label(decoder, text='\nMessung nicht aktiv\n', bg='red', font='Arial 12')
    Messung.grid(row=22, column=1, sticky='WNES', rowspan=3, columnspan=14)
    for i in table.get_children():                                    # Ergebnisfenster löschen           
        table.delete(i)
    Passingfile.set('     ')
    Message(decoder, 1, 2, 1, 2, 'w', Passingfile.get(), '10')

def connect():
    for i in status.get_children():                                   # Statusfenster löschen
        status.delete(i)
    Status_Wert = []

    s.connect((IP.ergebnis.get(), Decoder_Port))                      # Verbindung zu IP-Adresse und Port aufbauen
    nachricht = "GETSTATUS\r\n"                                       # Decoderstatus abrufen
    s.send(nachricht.encode())
    antwort = s.recv(1024)
    string = antwort.decode()
    Statusstring = string.split(";")
    if Statusstring != '':
        Decoder_Status.set('verbunden')
    
    if Decoder_Status.get() == 'nicht verbunden':
        Status_Wert.append('')
        Status_Wert.append('')
        Status_Wert.append('')
        Status_Wert.append('')
    else:
        Status_Wert.append(IP.ergebnis.get())
        Status_Wert.append(Statusstring[4])
        if Statusstring[3] == '1':
            Status_Wert.append('220 V')
        else:
            Status_Wert.append('0 V')
        Status_Wert.append(Statusstring[10] + " %")
    Status_Wert.append(Decoder_Status.get())


    Status_Parameter = ["IP-Adresse:", "Passivantennen:", "Netz-Spannung:", "Batterieladung:", "Status:"]
    for i in range(5):
        status_value = []
        status_value.append(Status_Parameter[i])
        status_value.append(Status_Wert[i])
        status.insert("", 'end', values=(status_value))

def ip_eingabe(event):
    decoder.focus_set()
    connect()

def beenden():
    s.close()                                            # Verbindung beenden
    decoder.destroy()                                    # Fenster schließen

# Fenster erstellen und Titel festlegen
decoder = tkinter.Tk()                                   # Hauptfenster für die Gerätedarstellung defineren
decoder.title("Zeitmessung Ebersberger Seelauf")         # Fenstertitel definieren
decoder.geometry('800x600')                              # Fenstergröße definieren, eventuell muss man hier zuerst die Bildschirmauflösung abfragen
decoder.resizable(False, False)                          # Fenstergroesse ist nicht veraenderbar

# Hilfsframe für Ergebnisanzeige
table_frame = tkinter.Frame(decoder, background='white')
table_frame.grid(row=2, column=1, sticky='WE', rowspan=19, columnspan=14)
table = ttk.Treeview(table_frame, column=("c1", "c2", "c3"), show='headings', height=19)
table.grid(row=0, column=0, sticky='WN')
vsb = ttk.Scrollbar(decoder, orient="vertical", command=table.yview)
vsb.grid(row=2, column=16, sticky='NS', rowspan=19, columnspan=1)
table.configure(yscrollcommand=vsb.set)

# Textfeld mit Tabelle für die Ergebnisse
table.column("#1", anchor='center', width=30)
table.heading("#1", text="Nr")
table.column("#2", anchor='center', width=100)
table.heading("#2", text="Startnr")
table.column("#3", anchor='center', width=200)
table.heading("#3", text="Zeit")

# Hilfsframe für Statusanzeige
status_frame = tkinter.Frame(decoder, background='white')
status_frame.grid(row=2, column=18, sticky='WE', rowspan=6, columnspan=4)
status = ttk.Treeview(status_frame, column=("c1", "c2"), show='headings', height=6)
status.grid(row=1, column=1, sticky='WE')
    
# Textfeld mit Tabelle für die Ergebnisse
status.column("#1", anchor='nw', width=150)
status.heading("#1", text="Parameter")
status.column("#2", anchor='w', width=200)
status.heading("#2", text="Wert")

# Geraetekonstanten definieren und initialisieren
Decoder_action = tkinter.StringVar()
Decoder_action.set('idle')
Decoder_Status = tkinter.StringVar()
Decoder_Status.set('nicht verbunden')
Decoder_Port = 3601                                                           # Kommunikation über TCP/IP-Port 3601
Passingfile = tkinter.StringVar()
Passingfile.set('     ')
Merker_Finish = tkinter.IntVar()
Merker_Finish.set(0)

# Verbindung definieren
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Fensterlemente
# Hilfselemente für Platzreservierungen
Message(decoder, 0, 0, 1, 1, 'W', '   ', '12')                                # Festlegung eines linken Randes (Spalte 0)
Message(decoder, 0, 2, 1, 1, 'W', '                  ', '12')                 # Festlegung des Platzes zwischen Start und Stop (Spalte 2)
Message(decoder, 0, 17, 1, 1, 'W', '      ', '12')                            # Festlegung des Platzes neben dem Textfeld (Spalte 17)
Message(decoder, 21, 1, 1, 14, 'WE', ' ', '8')                                # Leerzeile
Message(decoder, 25, 1, 1, 14, 'WE', ' ', '8')                                # Leerzeile

# Instanzen der Klassenelemente erzeugen
Messung = tkinter.Label(decoder, text='\nMessung nicht aktiv\n', bg='red', font='Arial 12')
Messung.grid(row=22, column=1, sticky='WNES', rowspan=3, columnspan=14)

Schaltflaeche(decoder, 26, 1, 1, 1, 'WNES', 'Start\nMessung', start)
Schaltflaeche(decoder, 26, 3, 1, 1, 'WNES', 'Stop\nMessung', stop)
Message(decoder, 1, 1, 1, 2, 'w', 'Passingfile: ', '10')
Message(decoder, 1, 2, 1, 2, 'w', Passingfile.get(), '10')
Message(decoder, 1, 18, 1, 2, 'w', 'IP-Adresse: ', '10')
IP = Input(decoder, '25', 1, 19, 'w', 1, 2, '', ip_eingabe)  

decoder.protocol("WM_DELETE_WINDOW", beenden)                                  # definiertes Beenden

decoder.mainloop()