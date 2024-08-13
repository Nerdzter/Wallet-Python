import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json

# Inicializa a carteira
try:
    with open('carteira.json', 'r') as c:
        carteira = json.loads(c.read())
    id_transacao = carteira["idtransacao"]
    carteira.pop("idtransacao")
except:
    carteira = {}
    id_transacao = 1

def listarTransacoes():
    if not carteira:
        messagebox.showinfo("Transações", "Sem transações!")
        return
    lista = '\n'.join([f'{transacao["identificador"]} - {transacao["data"]} - {transacao["descricao"]}: R${transacao["valor"]:.2f}' 
                       for transacao in sorted(carteira.values(), key=lambda transacao: str(transacao["identificador"]), reverse=True)])
    messagebox.showinfo("Suas transações", lista)

def adicionarTransacao():
    global id_transacao

    descricao = descricao_entry.get()
    valor = valor_entry.get()

    if not descricao or not valor:
        messagebox.showwarning("Erro", "Descrição e valor são obrigatórios!")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor deve ser numérico!")
        return

    data = str(datetime.now())

    transacao = {
        "valor": valor,
        "descricao": descricao,
        "data": data,
        "identificador": str(id_transacao),
    }

    carteira["id_" + str(id_transacao)] = transacao
    id_transacao += 1
    salvarCarteira()
    messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")

def deletarTransacao():
    identificador = "id_" + deletar_entry.get()

    if identificador not in carteira:
        messagebox.showerror("Erro", "ID não encontrado!")
        return

    transacao = carteira.pop(identificador)
    salvarCarteira()
    messagebox.showinfo("Sucesso", f'Transação {transacao["identificador"]} - "{transacao["descricao"]}", no valor de R${transacao["valor"]:.2f} foi excluída!')

def editarTransacao():
    id_transacao = editar_id_entry.get()

    if not id_transacao.isdigit() or "id_" + id_transacao not in carteira:
        messagebox.showerror("Erro", "ID inválido!")
        return

    identificador = "id_" + id_transacao
    descricao = editar_desc_entry.get()
    valor = editar_valor_entry.get()

    if not descricao or not valor:
        messagebox.showwarning("Erro", "Descrição e valor são obrigatórios!")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor deve ser numérico!")
        return

    mudar_data = mudar_data_var.get()
    if mudar_data == 'S':
        data = str(datetime.now())
    else:
        data = carteira[identificador]["data"]

    transacao = {
        "valor": valor,
        "descricao": descricao,
        "data": data,
        "identificador": id_transacao,
    }

    carteira[identificador] = transacao
    salvarCarteira()
    messagebox.showinfo("Sucesso", f'Transação {id_transacao} editada com sucesso!')

def consultarSaldo():
    saldo = sum(transacao["valor"] for transacao in carteira.values())
    messagebox.showinfo("Saldo Atual", f'Seu saldo atual é R${saldo:.2f}')

def salvarCarteira():
    c = carteira.copy()
    c["idtransacao"] = id_transacao
    with open('carteira.json', 'w') as file:
        file.write(json.dumps(c))

# Interface gráfica
root = tk.Tk()
root.title("Gerenciador de Carteira")
root.configure(bg='#2b2b2b')
root.geometry('400x600')

# Frame de Adicionar Transação
frame_adicionar = tk.Frame(root, bg='#2b2b2b')
frame_adicionar.pack(pady=10)

tk.Label(frame_adicionar, text="Adicionar Transação", bg='#2b2b2b', fg='white', font=('Arial', 14)).pack(pady=5)
tk.Label(frame_adicionar, text="Descrição:", bg='#2b2b2b', fg='white').pack(pady=5)
descricao_entry = tk.Entry(frame_adicionar)
descricao_entry.pack(pady=5)

tk.Label(frame_adicionar, text="Valor:", bg='#2b2b2b', fg='white').pack(pady=5)
valor_entry = tk.Entry(frame_adicionar)
valor_entry.pack(pady=5)

tk.Button(frame_adicionar, text="Adicionar Transação", command=adicionarTransacao, bg='#4CAF50', fg='white').pack(pady=10)

# Frame de Deletar Transação
frame_deletar = tk.Frame(root, bg='#2b2b2b')
frame_deletar.pack(pady=10)

tk.Label(frame_deletar, text="Deletar Transação", bg='#2b2b2b', fg='white', font=('Arial', 14)).pack(pady=5)
tk.Label(frame_deletar, text="ID para deletar:", bg='#2b2b2b', fg='white').pack(pady=5)
deletar_entry = tk.Entry(frame_deletar)
deletar_entry.pack(pady=5)

tk.Button(frame_deletar, text="Deletar Transação", command=deletarTransacao, bg='#F44336', fg='white').pack(pady=10)

# Frame de Editar Transação
frame_editar = tk.Frame(root, bg='#2b2b2b')
frame_editar.pack(pady=10)

tk.Label(frame_editar, text="Editar Transação", bg='#2b2b2b', fg='white', font=('Arial', 14)).pack(pady=5)
tk.Label(frame_editar, text="ID para editar:", bg='#2b2b2b', fg='white').pack(pady=5)
editar_id_entry = tk.Entry(frame_editar)
editar_id_entry.pack(pady=5)

tk.Label(frame_editar, text="Nova descrição:", bg='#2b2b2b', fg='white').pack(pady=5)
editar_desc_entry = tk.Entry(frame_editar)
editar_desc_entry.pack(pady=5)

tk.Label(frame_editar, text="Novo valor:", bg='#2b2b2b', fg='white').pack(pady=5)
editar_valor_entry = tk.Entry(frame_editar)
editar_valor_entry.pack(pady=5)

mudar_data_var = tk.StringVar(value='N')
tk.Label(frame_editar, text="Mudar data para agora? (S/N)", bg='#2b2b2b', fg='white').pack(pady=5)
tk.Entry(frame_editar, textvariable=mudar_data_var).pack(pady=5)

tk.Button(frame_editar, text="Editar Transação", command=editarTransacao, bg='#FFC107', fg='black').pack(pady=10)

# Outros botões
frame_outros = tk.Frame(root, bg='#2b2b2b')
frame_outros.pack(pady=10)

tk.Button(frame_outros, text="Listar Transações", command=listarTransacoes, bg='#2196F3', fg='white').pack(pady=10)
tk.Button(frame_outros, text="Consultar Saldo", command=consultarSaldo, bg='#9C27B0', fg='white').pack(pady=10)
tk.Button(frame_outros, text="Sair", command=root.quit, bg='#607D8B', fg='white').pack(pady=10)

root.mainloop()
