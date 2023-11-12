import tkinter as tk
from tkinter import simpledialog, messagebox

class CaixaSupermercado:
    def __init__(self, master):
        self.master = master
        self.master.title("Caixa de Supermercado")

        # Lista de produtos com preços
        self.produtos = {
            "Arroz": 2.5,
            "Feijão": 1.8,
            "Macarrão": 1.0,
            "Leite": 2.0,
            "Pão": 1.5,
        }

        # Dicionário para armazenar a quantidade de cada item selecionado
        self.quantidades = {}

        # Criar widgets
        self.criar_widgets()

    def criar_widgets(self):
        # Rótulo
        tk.Label(self.master, text="Selecione os itens:").grid(row=0, column=0, padx=10, pady=10)

        # Lista de produtos
        self.lista_produtos = tk.Listbox(self.master, selectmode=tk.MULTIPLE)
        for produto in self.produtos:
            self.lista_produtos.insert(tk.END, produto)
        self.lista_produtos.grid(row=1, column=0, padx=10, pady=10)

        # Rótulo para exibir o total
        self.rotulo_total = tk.Label(self.master, text="Total: R$ 0.0")
        self.rotulo_total.grid(row=2, column=0, pady=10)

        # Lista de itens selecionados
        self.lista_itens_selecionados = tk.Listbox(self.master)
        self.lista_itens_selecionados.grid(row=1, column=1, padx=10, pady=10)

        # Botão para adicionar item
        tk.Button(self.master, text="Adicionar Item", command=self.adicionar_item).grid(row=3, column=0, pady=10)

        # Botão para remover item
        tk.Button(self.master, text="Remover Item", command=self.remover_item).grid(row=3, column=1, pady=10)
        
        # Botão para finalizar compra
        tk.Button(self.master, text="Finalizar Compra", command=self.finalizar_compra).grid(row=4, column=0, pady=10)

    def adicionar_item(self):
        # Obter itens selecionados
        indices_selecionados = self.lista_produtos.curselection()

        # Adicionar itens selecionados à lista
        for indice in indices_selecionados:
            produto = self.lista_produtos.get(indice)
            preco = self.produtos[produto]

            # Perguntar a quantidade de itens
            quantidade = simpledialog.askinteger("Quantidade", f"Quantos {produto}(s) você deseja comprar?", initialvalue=1)

            if quantidade is not None and quantidade > 0:
                if produto in self.quantidades:
                    self.quantidades[produto] += quantidade
                else:
                    self.quantidades[produto] = quantidade

        # Exibir os itens selecionados
        self.exibir_itens_selecionados()
    
    def remover_item(self):
        # Obter itens selecionados na lista de itens selecionados
        indices_selecionados = self.lista_itens_selecionados.curselection()

        # Remover itens da lista de itens selecionados e do dicionário de quantidades
        for indice in reversed(indices_selecionados):
            item_selecionado = self.lista_itens_selecionados.get(indice)
            produto, _ = item_selecionado.split(" x")
            produto = produto.strip()
            
            # Remover o item do dicionário de quantidades
            if produto in self.quantidades:
                del self.quantidades[produto]
        # Atualizar a exibição dos itens selecionados
        self.exibir_itens_selecionados()

    def exibir_itens_selecionados(self):
        # Limpar lista de itens selecionados
        self.lista_itens_selecionados.delete(0, tk.END)

        # Adicionar itens à lista
        total = 0.0
        for produto, quantidade in self.quantidades.items():
            preco = self.produtos[produto]
            self.lista_itens_selecionados.insert(tk.END, f"{produto} x{quantidade}: R$ {preco * quantidade:.2f}")
            total += preco * quantidade

        # Exibir o total na interface
        self.rotulo_total.config(text=f"Total: R$ {total:.2f}")

    def finalizar_compra(self):
        # Verificar se a compra foi calculada
        if not self.quantidades:
            messagebox.showwarning("Aviso", "Selecione pelo menos um item antes de finalizar a compra.")
            return

         # Calcular o total da compra
        total_compra = 0.0
        for produto, quantidade in self.quantidades.items():
            preco = self.produtos[produto]
            total_compra += preco * quantidade

        # Solicitar o valor a ser pago
        valor_pago = simpledialog.askfloat("Finalizar Compra", "Digite o valor a ser pago:")

        # Verificar se o valor pago é suficiente
        if valor_pago is None:
            return  # O usuário cancelou a entrada do valor

        if valor_pago < total_compra:
            messagebox.showerror("Erro", "Valor pago insuficiente. Adicione mais fundos.")
            return

        # Imprimir nota
        nota = f"\n====== NOTA FISCAL ======\n"
        nota += f"Total da Compra: R$ {total_compra:.2f}\n"
        nota += f"Valor Pago: R$ {valor_pago:.2f}\n"
        nota += f"Troco: R$ {valor_pago - total_compra:.2f}\n"
        nota += f"Produtos:\n"
        nota += f"\n"

        for produto, quantidade in self.quantidades.items():
            preco = self.produtos[produto]
            nota += f"{produto} x{quantidade}: R$ {preco * quantidade:.2f}\n"

        messagebox.showinfo("Nota Fiscal", nota)

# Criar a janela principal
root = tk.Tk()
app = CaixaSupermercado(root)

# Iniciar o loop da interface gráfica
root.mainloop()
