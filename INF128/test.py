import tkinter as tk
from tkinter import messagebox, simpledialog

class BankKontoGUI:
    def __init__(self):
        self.konto = BankKonto()
        self.root = tk.Tk()
        self.root.title("Bankkonto")
        self.root.geometry("400x300")
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Bankkonto", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Saldo display
        self.saldo_label = tk.Label(self.root, text=f"Saldo: {self.konto.saldo} kr", font=("Arial", 14))
        self.saldo_label.pack(pady=5)
        
        # Buttons
        buttons = [
            ("Vis Saldo", self.vis_saldo),
            ("Innskudd", self.innskudd),
            ("Uttak", self.uttak),
            ("Renteoppgjør", self.renteoppgjør),
            ("Siste Endringer", self.vis_siste_endringer),
            ("Avslutt", self.avslutt)
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.root, text=text, command=command, width=15)
            btn.pack(pady=2)
    
    def vis_saldo(self):
        self.saldo_label.config(text=f"Saldo: {self.konto.saldo} kr")
        messagebox.showinfo("Saldo", f"Saldo: {self.konto.saldo} kr")
    
    def innskudd(self):
        beløp = simpledialog.askinteger("Innskudd", "Skriv inn beløp:")
        if beløp:
            self.konto.innskudd(beløp)
            self.konto.oppdater_rentesats()
            self.vis_saldo()
    
    def uttak(self):
        beløp = simpledialog.askinteger("Uttak", "Skriv inn beløp:")
        if beløp:
            self.konto.uttak(beløp)
            self.konto.oppdater_rentesats()
            self.vis_saldo()
    
    def renteoppgjør(self):
        self.konto.renteoppgjør()
        self.konto.oppdater_rentesats()
        self.vis_saldo()
        messagebox.showinfo("Renteoppgjør", "Renteoppgjør utført!")
    
    def vis_siste_endringer(self):
        endringer = "\n".join(self.konto.endringer) if self.konto.endringer else "Ingen endringer enda."
        messagebox.showinfo("Siste Endringer", endringer)
    
    def avslutt(self):
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

# Modify your BankKonto class slightly for GUI compatibility
class BankKonto:
    def __init__(self):
        self.saldo = 500
        self.rente = 0.01
        self.ordinærRente = 0.01
        self.bonusRente = 0.02
        self.nyRenteGrense = 1000000
        self.endringer = []
        
    def oppdater_siste_endringer(self, endring):
        self.endringer.append(endring)
        if len(self.endringer) > 3:
            self.endringer.pop(0)
            
    def oppdater_rentesats(self):
        if self.saldo >= self.nyRenteGrense:
            self.rente = self.bonusRente
        elif self.rente == self.bonusRente:
            self.rente = self.ordinærRente
            
    def innskudd(self, beløp):
        self.saldo += beløp
        self.oppdater_siste_endringer(f"+{beløp}")

    def uttak(self, beløp):
        if beløp > self.saldo:
            raise ValueError("Overtrekk ikke tillatt")
        self.saldo -= beløp
        self.oppdater_siste_endringer(f"-{beløp}")
        
    def renteoppgjør(self):
        saldoFør = self.saldo
        self.saldo *= (1 + self.rente)
        saldoEtter = self.saldo
        self.oppdater_siste_endringer(f"+{saldoEtter-saldoFør:.2f}")

# Run the GUI
if __name__ == "__main__":
    app = BankKontoGUI()
    app.run()