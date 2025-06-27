import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
from algoritmos_dc.karatsuba import karatsuba

class MissaoDC4:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame
        self._carregar_estilos()

        # --- Dados e Estado da Missão ---
        self.num1_bin, self.num2_bin = "", ""
        self.x1_str, self.x0_str, self.y1_str, self.y0_str = "", "", "", ""
        self.calc_A, self.calc_C, self.calc_B = 0, 0, 0
        self.termo_meio = 0
        self.resultado_correto_int = 0
        self.n2 = 0 # Metade do número de bits

        # --- Referências de UI ---
        self.entries = {}

    def _carregar_estilos(self):
        try:
            self.cor_fundo_base = self.game_manager.bg_color_dark
            self.cor_texto_principal = self.game_manager.fg_color_light
            self.cor_texto_titulo_missao = self.game_manager.title_color_accent
            self.cor_entry_bg = "#1A1A1A"
            self.cor_info = "#87CEFA"
            self.header_font_obj = self.game_manager.header_font_obj
            self.narrative_font_obj = self.game_manager.narrative_font_obj
            self.button_font_obj = self.game_manager.button_font_obj
            # Usaremos uma fonte monoespaçada para os números binários
            self.binary_font_obj = tkFont.Font(family="Courier", size=12, weight="bold")
        except AttributeError:
            self.cor_fundo_base = "black"; self.cor_texto_principal = "white"; self.cor_texto_titulo_missao="orangered"
            self.header_font_obj = ("Arial", 20, "bold"); self.narrative_font_obj = ("Arial", 12)

    def _limpar_frame(self):
        for widget in self.base_content_frame.winfo_children(): widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame()
        tk.Label(self.base_content_frame, text="MISSÃO 4: Quebra de Códigos", font=self.header_font_obj, fg=self.cor_texto_titulo_missao, bg=self.cor_fundo_base).pack(pady=(10,15))
        imagem_missao = self.game_manager.imagens.get("Cena6.png")
        if imagem_missao:
            tk.Label(self.base_content_frame, image=imagem_missao, bg=self.cor_fundo_base).pack(pady=10)
            
        contexto = (
            "Fulcrum: \"Comandante, interceptamos fragmentos de um novo protocolo de criptografia Imperial. A chave de decodificação final é o produto de dois números-semente binários muito grandes. A multiplicação padrão é lenta demais.\n\nSua tarefa é usar a doutrina 'Dividir e Conquistar' para calcular o produto mais rápido, guiando nosso computador de análise passo a passo através da Multiplicação de Karatsuba.\""
        )
        tk.Label(self.base_content_frame, text=contexto, wraplength=700, justify=tk.LEFT, font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(pady=10, padx=20)
        ttk.Button(self.base_content_frame, text="Iniciar Análise Criptográfica...", command=self.iniciar_etapa_divisao, style="Accent.Dark.TButton").pack(pady=20)

    def _gerar_numeros(self):
        num_bits = 8
        self.n2 = num_bits // 2
        
        num1_int = random.randint(2**(num_bits - 1), 2**num_bits - 1)
        num2_int = random.randint(2**(num_bits - 1), 2**num_bits - 1)

        self.num1_bin = bin(num1_int)[2:].zfill(num_bits)
        self.num2_bin = bin(num2_int)[2:].zfill(num_bits)
        
        self.resultado_correto_int = karatsuba(self.num1_bin, self.num2_bin)
        print(f"DEBUG: Chaves: {self.num1_bin}, {self.num2_bin}. Resultado: {bin(self.resultado_correto_int)[2:]}")

    def iniciar_etapa_divisao(self):
        self._limpar_frame()
        self._gerar_numeros()
        tk.Label(self.base_content_frame, text="Etapa 1: DIVIDIR", font=self.button_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=10)
        info_text = "Divida cada chave-semente binária em duas metades de 4 bits (x1, x0) e (y1, y0)."
        tk.Label(self.base_content_frame, text=info_text, font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(pady=5)
        
        # Exibição da fórmula de divisão
        formula_text = f"Fórmula: x = x1 * 2^{self.n2} + x0"
        tk.Label(self.base_content_frame, text=formula_text, font=("Courier", 12, "italic"), fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=5)

        container = tk.Frame(self.base_content_frame, bg=self.cor_fundo_base)
        container.pack(pady=10)
        
        tk.Label(container, text=f"Chave x: {self.num1_bin}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=0, column=0, columnspan=4, pady=5)
        tk.Label(container, text="x1 =", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=1, column=0)
        self.entries['x1'] = tk.Entry(container, width=8, font=self.binary_font_obj, bg=self.cor_entry_bg, fg=self.cor_texto_principal, insertbackground=self.cor_texto_principal); self.entries['x1'].grid(row=1, column=1, padx=5)
        tk.Label(container, text="x0 =", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=1, column=2)
        self.entries['x0'] = tk.Entry(container, width=8, font=self.binary_font_obj, bg=self.cor_entry_bg, fg=self.cor_texto_principal, insertbackground=self.cor_texto_principal); self.entries['x0'].grid(row=1, column=3, padx=5)

        tk.Label(container, text=f"Chave y: {self.num2_bin}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=2, column=0, columnspan=4, pady=5)
        tk.Label(container, text="y1 =", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=3, column=0)
        self.entries['y1'] = tk.Entry(container, width=8, font=self.binary_font_obj, bg=self.cor_entry_bg, fg=self.cor_texto_principal, insertbackground=self.cor_texto_principal); self.entries['y1'].grid(row=3, column=1, padx=5)
        tk.Label(container, text="y0 =", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).grid(row=3, column=2)
        self.entries['y0'] = tk.Entry(container, width=8, font=self.binary_font_obj, bg=self.cor_entry_bg, fg=self.cor_texto_principal, insertbackground=self.cor_texto_principal); self.entries['y0'].grid(row=3, column=3, padx=5)

        ttk.Button(self.base_content_frame, text="Confirmar Divisão", command=self.validar_divisao, style="Accent.Dark.TButton").pack(pady=20)

    def validar_divisao(self):
        x1_correto_str = self.num1_bin[:-self.n2]; x0_correto_str = self.num1_bin[-self.n2:]
        y1_correto_str = self.num2_bin[:-self.n2]; y0_correto_str = self.num2_bin[-self.n2:]
        self.x1_str = self.entries['x1'].get().strip(); self.x0_str = self.entries['x0'].get().strip()
        self.y1_str = self.entries['y1'].get().strip(); self.y0_str = self.entries['y0'].get().strip()
        if self.x1_str == x1_correto_str and self.x0_str == x0_correto_str and self.y1_str == y1_correto_str and self.y0_str == y0_correto_str:
            messagebox.showinfo("Sucesso", "Divisão correta. O computador agora fará as chamadas recursivas.")
            self.iniciar_etapa_conquista()
        else: messagebox.showerror("Erro", "Divisão incorreta. Verifique as metades e tente novamente.")

    def iniciar_etapa_conquista(self):
        self._limpar_frame()
        self.calc_A = karatsuba(self.x1_str, self.y1_str)
        self.calc_C = karatsuba(self.x0_str, self.y0_str)
        soma_x_str = bin(int(self.x1_str, 2) + int(self.x0_str, 2))[2:]
        soma_y_str = bin(int(self.y1_str, 2) + int(self.y0_str, 2))[2:]
        self.calc_B = karatsuba(soma_x_str, soma_y_str)
        
        tk.Label(self.base_content_frame, text="Etapa 2: CONQUISTAR", font=self.button_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=10)
        tk.Label(self.base_content_frame, text="O computador realizou as multiplicações menores. Agora, o passo crucial.", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base, wraplength=700).pack(pady=5)
        
        container = tk.Frame(self.base_content_frame, bg=self.cor_fundo_base); container.pack(pady=10)
        
        tk.Label(container, text="Resultados (em binário):", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w")
        tk.Label(container, text=f"A (x1*y1) = {bin(self.calc_A)[2:]}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w")
        tk.Label(container, text=f"C (x0*y0) = {bin(self.calc_C)[2:]}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w")
        tk.Label(container, text=f"B ((x1+x0)*(y1+y0)) = {bin(self.calc_B)[2:]}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w", pady=(0, 15))
        
        tk.Label(container, text="Fórmula do Termo do Meio: (x1*y0 + x0*y1) = B - A - C", font=("Courier", 12, "italic"), fg=self.cor_info, bg=self.cor_fundo_base).pack(anchor="w")
        tk.Label(container, text="Calcule e insira o resultado de B - A - C (em binário):", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w", pady=(10,0))
        self.entries['termo_meio'] = tk.Entry(container, width=20, font=self.binary_font_obj, bg=self.cor_entry_bg, fg=self.cor_texto_principal, insertbackground=self.cor_texto_principal); self.entries['termo_meio'].pack(anchor="w")

        ttk.Button(self.base_content_frame, text="Confirmar Termo do Meio", command=self.validar_conquista, style="Accent.Dark.TButton").pack(pady=20)
    
    def validar_conquista(self):
        try:
            termo_meio_jogador_bin = self.entries['termo_meio'].get().strip()
            if not all(c in '01' for c in termo_meio_jogador_bin): raise ValueError("Entrada não é binária")
            
            self.termo_meio = self.calc_B - self.calc_A - self.calc_C
            termo_meio_correto_bin = bin(self.termo_meio)[2:]
            
            if termo_meio_jogador_bin == termo_meio_correto_bin:
                messagebox.showinfo("Sucesso", "Cálculo do termo do meio está correto. Agora, vamos combinar tudo.")
                self.iniciar_etapa_combinar()
            else:
                messagebox.showerror("Erro", f"Cálculo incorreto. O valor binário correto era {termo_meio_correto_bin}.")
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, insira um número binário válido (apenas '0' e '1').")
    
    def iniciar_etapa_combinar(self):
        self._limpar_frame()
        
        tk.Label(self.base_content_frame, text="Etapa 3: COMBINAR", font=self.button_font_obj, fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=10)
        
        formula_text = f"Fórmula Final: xy = (A << {2*self.n2}) + ((B-A-C) << {self.n2}) + C"
        tk.Label(self.base_content_frame, text=formula_text, font=("Courier", 12, "italic"), fg=self.cor_info, bg=self.cor_fundo_base).pack(pady=5)
        tk.Label(self.base_content_frame, text="Some os termos deslocados para encontrar a chave final.", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base, wraplength=700).pack(pady=5)
        
        container = tk.Frame(self.base_content_frame, bg=self.cor_fundo_base); container.pack(pady=10)
        
        tk.Label(container, text=f"Termo A deslocado: {bin(self.calc_A << (2*self.n2))}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w")
        tk.Label(container, text=f"Termo Meio deslocado: {bin(self.termo_meio << self.n2)}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w")
        tk.Label(container, text=f"Termo C: {bin(self.calc_C)}", font=self.binary_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w", pady=(0,10))
        
        tk.Label(container, text="Insira a chave final (em binário):", font=self.narrative_font_obj, fg=self.cor_texto_principal, bg=self.cor_fundo_base).pack(anchor="w")
        self.entries['final'] = tk.Entry(container, width=30, font=self.binary_font_obj, bg=self.cor_entry_bg, fg=self.cor_texto_principal, insertbackground=self.cor_texto_principal); self.entries['final'].pack(anchor="w")

        ttk.Button(self.base_content_frame, text="Decodificar Transmissão Imperial!", command=self.avaliar_resultado_final, style="Accent.Dark.TButton").pack(pady=20)

    def avaliar_resultado_final(self):
        try:
            resultado_jogador_bin = self.entries['final'].get().strip()
            if not all(c in '01' for c in resultado_jogador_bin): raise ValueError("Entrada não é binária")
            
            resultado_jogador_int = int(resultado_jogador_bin, 2)
            
            if resultado_jogador_int == self.resultado_correto_int:
                pontos = 400; self.game_manager.add_score(pontos)
                messagebox.showinfo("Sucesso!", f"Chave Correta! Transmissão decodificada!\nA mensagem revela a localização de uma base de suprimentos secreta do Império. Excelente trabalho!\nVocê ganhou {pontos} pontos de influência.")
                self.game_manager.mission_completed("MissaoDC4")
            else:
                messagebox.showerror("Falha na Decodificação", f"Chave incorreta. A transmissão se corrompeu.\nA chave correta era: {bin(self.resultado_correto_int)[2:]}")
                self.game_manager.add_score(-50)
                self.game_manager.mission_failed_options(self, "Chave de decodificação errada.", "Fulcrum: \"Precisão é essencial na criptografia. Um único erro e tudo está perdido.\"")
        except ValueError:
            messagebox.showerror("Entrada Inválida", "A chave final deve ser um número binário válido.")

    def retry_mission(self):
        # Avisa o GameManager para reiniciar o estado desta missão
        self.game_manager.set_game_state("START_MISSION_DC_4")