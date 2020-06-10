## Questão 4 ##
import tkinter as tk

# Essa é a classe que representa toda a aplicação cliente, com a UI para o cliente
# emitir os comandos.
class BankingApp(tk.Frame):
    def __init__(self, conta, master=None):
        super().__init__(master)
        self.master = master
        self.conta = conta
        self.master.title(f"Bem-vindo {self.conta.titular} - Conta No. {self.conta.numero}")
        self.master.minsize(400,200)
        self.historico = []

        # Temos uma seção para escolher a operação de transação
        self.op = tk.StringVar()
        oplist = ["Depósito", "Saque", "Transferência"]
        self.op.set(oplist[0])
        lbOp = tk.Label(self.master, text="Operação: ")
        menuOp = tk.OptionMenu(self.master, self.op, *oplist, command=self.create_widgets)
        lbOp.grid(row=0, column=0)
        menuOp.grid(row=0, column=1)
        # Essa escolha irá modificar o layout da janela
        self.transactions = tk.PanedWindow(self.master)
        self.transactions.grid(row=1, column=0)
        self.create_widgets(None)
        # A seguir temos opções de consulta que ficarão fixas na tela
        self.consulta1 = tk.PanedWindow(self.master)
        saldoBtn = tk.Button(self.consulta1, text="Saldo", 
                    command=SaldoCommand(self.conta, self.consulta1).execute)
        self.consulta1.add(saldoBtn)
        saldoBtn.grid(row=0, column=0)
        
        self.consulta2 = tk.PanedWindow(self.master)
        extratoBtn = tk.Button(self.consulta2, text="Extrato", 
                    command=ExtratoCommand(self.conta, self.consulta2).execute)
        self.consulta2.add(extratoBtn)
        extratoBtn.grid(row=0,column=0)

        self.consulta1.grid(row=2, column=0)
        self.consulta2.grid(row=3, column=0)
        
    # Nessa função atualizamos o layout de acordo com a transação escolhida
    def create_widgets(self, event):
        for w in self.transactions.winfo_children():
            w.destroy()
        if self.op.get() == "Depósito":
            lb = tk.Label(self.transactions, text="Valor: ")
            valor = tk.DoubleVar()
            valor.set(0.0)
            valorEntry = tk.Entry(self.transactions, textvariable=valor)
            confirmBtn = tk.Button(self.transactions, text="Confirma",
                        command=lambda: DepositCommand(self.conta, valor.get()).execute())
            self.transactions.add(lb)
            self.transactions.add(valorEntry)
            self.transactions.add(confirmBtn)
            lb.grid(row=0,column=0)
            valorEntry.grid(row=0,column=1)
            confirmBtn.grid(row=1,column=0)
        if self.op.get() == "Saque":
            lb = tk.Label(self.transactions, text="Valor: ")
            valor = tk.DoubleVar()
            valor.set(0.0)
            valorEntry = tk.Entry(self.transactions, textvariable=valor)
            confirmBtn = tk.Button(self.transactions, text="Confirma",
                command=lambda: SaqueCommand(self.conta, valor.get()).execute())
            self.transactions.add(lb)
            self.transactions.add(valorEntry)
            self.transactions.add(confirmBtn)
            lb.grid(row=0,column=0)
            valorEntry.grid(row=0,column=1)
            confirmBtn.grid(row=1,column=0)
        if self.op.get() == "Transferência":
            lb = tk.Label(self.transactions, text="Valor: ")
            valor, titular, numero = tk.DoubleVar(), tk.StringVar(), tk.StringVar()
            valor.set(0.0)
            valorEntry = tk.Entry(self.transactions, textvariable=valor)
            lb2 = tk.Label(self.transactions, text="Titular: ")
            lb3 = tk.Label(self.transactions, text="No. Conta: ")
            titularEntry = tk.Entry(self.transactions, textvariable=titular)
            numeroEntry = tk.Entry(self.transactions, textvariable=numero)
            confirmBtn = tk.Button(self.transactions, text="Confirma",
                        command=lambda: TransferCommand(self.conta, valor.get(), 
                        ContaBancaria(numero.get(), titular.get())).execute())
            self.transactions.add(lb)
            self.transactions.add(lb2)
            self.transactions.add(lb3)
            self.transactions.add(valorEntry)
            self.transactions.add(titularEntry)
            self.transactions.add(numeroEntry)
            self.transactions.add(confirmBtn)
            lb.grid(row=0,column=0)
            lb2.grid(row=1,column=0)
            lb3.grid(row=2,column=0)
            valorEntry.grid(row=0,column=1)
            titularEntry.grid(row=1,column=1)
            numeroEntry.grid(row=2,column=1)
            confirmBtn.grid(row=3,column=0)
                

# A aplicação assume um cliente já logado em sua conta bancária, com número
# e nome do titular, e um saldo inicial (default: 0)
class ContaBancaria:
    def __init__(self, numero, titular, saldo=0):
        self.numero, self.titular, self.saldo = numero, titular, saldo
        self.historicoFinanceiro = []
        self.historicoFinanceiro.append(f"Saldo: R$ {self.saldo}")

# A interface Command irá definir a operação de execute e um descritor, para ser utilizado
# na hora de visualizar o histórico de comandos.
class Command:
    def execute(self):
        raise NotImplementedError

    def getDescricao(self):
        raise NotImplementedError

# As 5 operações serão: depósito, saque, transferência, consulta saldo e extrato.
class DepositCommand(Command):
    def __init__(self, conta, quantia):
        self.conta, self.quantia = conta, quantia

    def execute(self):
        self.conta.saldo += self.quantia
        self.conta.historicoFinanceiro.append(f"Depósito: R$ {self.quantia}")
        self.conta.historicoFinanceiro.append(f"Saldo: R$ {self.conta.saldo}")

    def getDescricao(self):
        print(f"Depósito de {self.quantia} reais")

class SaqueCommand(Command):
    def __init__(self, conta, quantia):
        self.conta = conta
        self.quantia = quantia
    
    def execute(self):
        self.conta.saldo -= self.quantia
        self.conta.historicoFinanceiro.append(f"Saque: R$ {self.quantia}")
        self.conta.historicoFinanceiro.append(f"Saldo: R$ {self.conta.saldo}")

    def getDescricao(self):
        print(f"Saque de {self.quantia} reais")

class SaldoCommand(Command):
    def __init__(self, conta, panedwindow):
        self.conta = conta
        self.pndwdw = panedwindow

    def execute(self):
        for wg in self.pndwdw.winfo_children():
            wg.destroy()
        
        btn = tk.Button(self.pndwdw, text="Saldo", 
                    command=self.execute)
        lb = tk.Label(self.pndwdw, text=self.conta.historicoFinanceiro[-1])
        self.pndwdw.add(btn)
        self.pndwdw.add(lb)
        btn.grid(row=0, column=0)
        lb.grid(row=0, column=1)

    def getDescricao(self):
        print("Consulta de saldo")

class TransferCommand(Command):
    def __init__(self, conta, quantia, destino):
        self.conta, self.quantia, self.destino = conta, quantia, destino

    def execute(self):
        self.conta.saldo -= self.quantia
        self.destino.saldo += self.quantia
        self.conta.historicoFinanceiro.append(f"Transferência: R$ {self.quantia} para conta no. {self.destino.numero}")
        self.conta.historicoFinanceiro.append(f"Saldo: R$ {self.conta.saldo}")

    def getDescricao(self):
        print(f"Transferência de {self.quantia} reais para a conta no. {self.destino}")

class ExtratoCommand(Command):
    def __init__(self, conta, panedwindow):
        self.conta = conta
        self.pndwdw = panedwindow

    def execute(self):
        for wg in self.pndwdw.winfo_children():
            wg.destroy()
        
        btn = tk.Button(self.pndwdw, text="Extrato", 
                    command=self.execute)
        txt = tk.Text(self.pndwdw, width=50, height=10)
        for hf in self.conta.historicoFinanceiro:
            txt.insert(tk.END, hf+"\n")
        self.pndwdw.add(btn)
        self.pndwdw.add(txt)
        btn.grid(row=0, column=0)
        txt.grid(row=1, column=0)

    def getDescricao(self):
        print("Requisição de extrato")

conta = ContaBancaria("01-001", "Bruno")
root = tk.Tk()
app = BankingApp(conta, master=root)
app.mainloop()
for comando in app.historico:
    comando.getDescricao()