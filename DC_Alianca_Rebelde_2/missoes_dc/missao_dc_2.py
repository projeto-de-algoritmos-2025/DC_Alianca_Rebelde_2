import tkinter as tk
from tkinter import ttk, messagebox
import random
import copy
from algoritmos_dc.contagem_de_inversoes import contar_inversoes


def gerar_frase_com_inversoes():
    frases_possiveis = [
        ["A", "força", "está", "com", "você"],
        ["Meditar", "você", "deve", "para", "respostas"],
        ["Sabedoria", "vem", "com", "o", "tempo"],
        ["Difícil", "o", "caminho", "é", "mas", "possível"],
        ["Treinar", "todos", "os", "dias", "você", "deve"]
    ]
    frase_correta = random.choice(frases_possiveis)
    frase_embaralhada = copy.deepcopy(frase_correta)
    while True:
        random.shuffle(frase_embaralhada)
        if frase_embaralhada != frase_correta:
            break
    return frase_correta, frase_embaralhada


class MissaoDC2:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame
        self.entries = {}
        self._carregar_estilos()

        self.frase_correta, self.frase_yoda = gerar_frase_com_inversoes()
        self.indices_referencia = [self.frase_correta.index(p) for p in self.frase_yoda]
        self.inversoes_certas = contar_inversoes(self.indices_referencia)

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
        tk.Label(self.base_content_frame, text="MISSÃO 2: Dicas do Mestre", font=self.header_font_obj, fg=self.cor_texto_titulo_missao, bg=self.cor_fundo_base).pack(pady=(10,15))
        imagem_missao = self.game_manager.imagens.get("Cena5.png")
        if imagem_missao:
            tk.Label(self.base_content_frame, image=imagem_missao, bg=self.cor_fundo_base).pack(pady=10)

        narrativa = (
            "Yoda: \"Confusa, a ordem está. Clareza você deve buscar.\"\n\n"
            "O Mestre Yoda fala uma frase fora da ordem usual. Sua missão é contar quantos pares de palavras estão fora do lugar.\n\n"
            "Quanto mais próxima sua compreensão da sabedoria Yodística, maior sua recompensa..."
        )
        tk.Label(self.base_content_frame, text=narrativa, wraplength=700, justify=tk.LEFT, font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(pady=10, padx=20)

        ttk.Button(self.base_content_frame, text="Ouvir a frase do Mestre...", command=self.iniciar_desafio, style="Accent.Dark.TButton").pack(pady=20)

    def iniciar_desafio(self):
        self._limpar_frame()

        frase_original = " ".join(self.frase_correta)
        frase_yoda = " ".join(self.frase_yoda)
        indices_str = " ".join(map(str, self.indices_referencia))

        tk.Label(self.base_content_frame, text="Etapa: SABEDORIA DESORDENADA", font=self.button_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=10)

        tk.Label(self.base_content_frame, text=f"Frase correta: {frase_original}", font=("Courier", 12), fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(pady=5)
        tk.Label(self.base_content_frame, text=f"Yoda disse: {frase_yoda}", font=("Courier", 12, "italic"), fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=5)
        tk.Label(self.base_content_frame, text=f"(Ordem relativa esperada: {indices_str})", font=("Courier", 11), fg="#AAAAAA", bg=self.cor_fundo_base).pack(pady=(5,15))

        tk.Label(self.base_content_frame, text="Quantos pares de palavras estão fora de ordem na frase de Yoda?", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(pady=10)

        self.entries['inversoes'] = tk.Entry(self.base_content_frame, width=10, font=("Courier", 14), bg="black", fg="white", insertbackground="white")
        self.entries['inversoes'].pack()

        ttk.Button(self.base_content_frame, text="Confirmar Sabedoria", command=self.validar_resposta, style="Accent.Dark.TButton").pack(pady=20)

    def validar_resposta(self):
        entrada = self.entries['inversoes'].get().strip()
        if not entrada.isdigit():
            messagebox.showerror("Erro", "Digite um número inteiro válido.")
            return

        tentativa = int(entrada)
        if tentativa == self.inversoes_certas:
            pontos = 300
            bonus = 100
            messagebox.showinfo("Sucesso!", f"Inversões corretas: {tentativa}\n\nYoda sorri: \"Sabedoria, você tem.\"\n+{pontos + bonus} pontos de influência!")
            self.game_manager.add_score(pontos + bonus)
            self.game_manager.mission_completed("MissaoDC2")
        else:
            messagebox.showerror("Hmm...", f"Não foi exatamente isso que Yoda quis dizer...\nInversões corretas: {self.inversoes_certas}")
            self.game_manager.add_score(-50)
            self.game_manager.mission_failed_options(self, "Você ainda tem muito a aprender...", "Yoda: \"Tentado você foi. Mas claro, o caminho ainda não está.\"")

    def retry_mission(self):
        self.game_manager.set_game_state("START_MISSION_DC_2")
