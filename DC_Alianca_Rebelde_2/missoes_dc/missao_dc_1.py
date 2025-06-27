import tkinter as tk
from tkinter import ttk, messagebox
import random
from algoritmos_dc.mediana_das_medianas import mediana_das_medianas

class MissaoDC1:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        # Estilo e fontes
        self._carregar_estilos()
        self.entries = {}
        self.lista_dados = []
        self.mediana_correta = None

    def _carregar_estilos(self):
        try:
            self.cor_fundo_base = self.game_manager.bg_color_dark
            self.cor_texto_principal = self.game_manager.fg_color_light
            self.cor_texto_titulo_missao = self.game_manager.title_color_accent
            self.cor_info = "#87CEFA"
            self.header_font_obj = self.game_manager.header_font_obj
            self.narrative_font_obj = self.game_manager.narrative_font_obj
            self.button_font_obj = self.game_manager.button_font_obj
        except AttributeError:
            self.cor_fundo_base = "black"
            self.cor_texto_principal = "white"
            self.cor_texto_titulo_missao = "orangered"
            self.header_font_obj = ("Arial", 20, "bold")
            self.narrative_font_obj = ("Arial", 12)

    def _limpar_frame(self):
        for widget in self.base_content_frame.winfo_children():
            widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame, 
            text="MISSÃO 1: O Enigma da Mediana", 
            font=self.header_font_obj, 
            fg=self.cor_texto_titulo_missao, 
            bg=self.cor_fundo_base
        ).pack(pady=(10,15))

        imagem_missao = self.game_manager.imagens.get("Cena1.png")
        if imagem_missao:
            tk.Label(self.base_content_frame, image=imagem_missao, bg=self.cor_fundo_base).pack(pady=10)

        contexto = (
            "C-3PO: \"Interceptamos um grande volume de dados codificados. No centro das decisões imperiais está um valor-chave: a mediana.\n\n"
            "Precisamos identificar esse valor usando uma estratégia eficiente. Não podemos confiar na simples ordenação...\"\n\n"
            "Use o algoritmo Mediana das Medianas para encontrar o valor que representa o ponto central dessa base de dados rebelde."
        )

        tk.Label(
            self.base_content_frame, 
            text=contexto, 
            wraplength=700, 
            justify=tk.LEFT, 
            font=self.narrative_font_obj, 
            fg=self.cor_texto_principal, 
            bg=self.cor_fundo_base
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame, 
            text="Iniciar Análise de Dados...", 
            command=self.iniciar_etapa_analise, 
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def iniciar_etapa_analise(self):
        self._limpar_frame()
        self.lista_dados = random.sample(range(10, 100), 11)  # Lista com 11 elementos distintos
        k = len(self.lista_dados) // 2 + 1
        self.mediana_correta = mediana_das_medianas(self.lista_dados, k)

        tk.Label(
            self.base_content_frame, 
            text="Etapa: ANÁLISE DE DADOS", 
            font=self.button_font_obj, 
            fg=self.cor_info, 
            bg=self.cor_fundo_base
        ).pack(pady=10)

        dados_str = ", ".join(map(str, self.lista_dados))
        tk.Label(
            self.base_content_frame, 
            text=f"Dados interceptados:\n[{dados_str}]", 
            wraplength=700, 
            font=("Courier", 12), 
            fg=self.cor_texto_principal, 
            bg=self.cor_fundo_base
        ).pack(pady=10)

        tk.Label(
            self.base_content_frame, 
            text="Insira a mediana desses dados:", 
            font=self.narrative_font_obj, 
            fg=self.cor_texto_principal, 
            bg=self.cor_fundo_base
        ).pack(pady=(10,5))

        self.entries['mediana'] = tk.Entry(
            self.base_content_frame, 
            width=10, 
            font=("Courier", 14), 
            bg="black", 
            fg="white", 
            insertbackground="white"
        )
        self.entries['mediana'].pack()

        ttk.Button(
            self.base_content_frame, 
            text="Confirmar Mediana", 
            command=self.validar_resposta, 
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def validar_resposta(self):
        entrada = self.entries['mediana'].get().strip()
        if not entrada.isdigit():
            messagebox.showerror("Erro", "Insira um número inteiro válido.")
            return

        resposta = int(entrada)
        if resposta == self.mediana_correta:
            pontos = 300
            self.game_manager.add_score(pontos)
            messagebox.showinfo("Sucesso", f"Correto! A mediana era {resposta}. Os dados agora estão decifrados.\n+{pontos} pontos de influência.")
            self.game_manager.mission_completed("MissaoDC1")
        else:
            messagebox.showerror("Erro", f"Mediana incorreta. A resposta correta era {self.mediana_correta}.")
            self.game_manager.add_score(-50)
            self.game_manager.mission_failed_options(
                self,
                "Erro de Cálculo",
                "C-3PO: \"Oh não! Um erro no cálculo central distorceu toda a mensagem...\""
            )
