# missoes_dc/missao_dc_3.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
import math
from algoritmos_dc.par_de_pontos_mais_proximos import encontrar_par_mais_proximo, dist

class MissaoDC3:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame
        self._carregar_estilos()

        # --- Estado da Missão ---
        self.nomes_naves = [chr(ord('A') + i) for i in range(26)] # Nomes A, B, C...
        self.todas_naves = [] # Lista de tuplas (x, y, nome)
        self.solucao_otima_dist, self.solucao_otima_par = 0, (None, None)
        
        # Para a navegação com setas
        self.nave_selecionada = None
        # Para a medição de distância com o mouse
        self.nave_medicao_1 = None
        self.nave_medicao_2 = None
        # Para o processo recursivo
        self.sub_problemas = {} # Dicionário para guardar o estado de cada sub-problema
        self.log_acoes = []

    def _carregar_estilos(self):
        # Carrega fontes e cores do GameManager
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.header_font_obj = self.game_manager.header_font_obj
            self.narrative_font_obj = self.game_manager.narrative_font_obj
            self.small_bold_font_obj = self.game_manager.small_bold_font_obj
        except AttributeError:
            self.cor_fundo, self.cor_texto, self.cor_titulo = "black", "white", "orangered"
            self.header_font_obj, self.narrative_font_obj, self.small_bold_font_obj = ("Arial",20,"bold"), ("Arial",12), ("Arial",10,"bold")

    def _limpar_frame(self):
        self.root.unbind("<Left>"); self.root.unbind("<Right>"); self.root.unbind("<Up>"); self.root.unbind("<Down>")
        if hasattr(self, 'canvas'): self.canvas.unbind("<Button-1>")
        for widget in self.base_content_frame.winfo_children(): widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame()
        # ... (código do contexto da missão, como antes) ...
        contexto = "Fulcrum: \"Comandante, sua missão é analisar o mapa tático da frota e encontrar o par de naves mais próximo. Use a doutrina 'Dividir e Conquistar' para analisar o campo de batalha. Encontre essa vulnerabilidade e nos dará a brecha de que precisamos.\""
        tk.Label(self.base_content_frame, text="MISSÃO 3: Duelo no Hiperespaço", font=self.header_font_obj, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(0,15))
        tk.Label(self.base_content_frame, text=contexto, wraplength=700, justify=tk.LEFT, font=self.narrative_font_obj, fg=self.cor_texto, bg=self.cor_fundo).pack(pady=10)
        ttk.Button(self.base_content_frame, text="Analisar Mapa Tático...", command=self.iniciar_fase_interativa, style="Accent.Dark.TButton").pack(pady=20)
        
    def iniciar_fase_interativa(self):
        self._limpar_frame()
        # Layout
        main_frame = tk.Frame(self.base_content_frame, bg=self.cor_fundo); main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(main_frame, bg="#0d0d2e", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        control_panel = tk.Frame(main_frame, bg=self.cor_fundo, padx=10, pady=10); control_panel.pack(side=tk.RIGHT, fill=tk.Y, width=300); control_panel.pack_propagate(False)

        # UI do Painel de Controle
        self.info_label = tk.Label(control_panel, text="Instruções da Missão", font=self.narrative_font_obj, wraplength=280, justify=tk.LEFT, fg=self.cor_texto, bg=self.cor_fundo)
        self.info_label.pack(anchor="n", pady=5, fill=tk.X)
        self.status_label = tk.Label(control_panel, text="", font=self.small_bold_font_obj, wraplength=280, justify=tk.LEFT, fg="#87CEFA", bg=self.cor_fundo)
        self.status_label.pack(anchor="n", pady=5, fill=tk.X)
        
        button_container = tk.Frame(control_panel, bg=self.cor_fundo); button_container.pack(pady=10, fill=tk.X)
        self.mediana_button = ttk.Button(button_container, text="Traçar Mediana Aqui", command=self.tracar_mediana, style="Dark.TButton"); self.mediana_button.pack(fill=tk.X, pady=2)
        self.finalizar_button = ttk.Button(button_container, text="Reportar Vulnerabilidade Final", command=self.finalizar_missao, style="Accent.Dark.TButton"); self.finalizar_button.pack(fill=tk.X, pady=2)
        
        log_frame = tk.LabelFrame(control_panel, text="Log de Operações", font=self.small_bold_font_obj, bg=self.cor_fundo, fg=self.cor_texto, padx=5, pady=5); log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.log_listbox = tk.Listbox(log_frame, font=("Courier", 9), bg="#1c1c1c", fg="lightgrey", borderwidth=0, highlightthickness=0); self.log_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.root.after(100, self._setup_inicial_canvas)

    def _setup_inicial_canvas(self):
        self.base_content_frame.update_idletasks()
        self._gerar_naves()
        self.solucao_otima_dist, self.solucao_otima_par = encontrar_par_mais_proximo(self.todas_naves)
        print(f"DEBUG: Solução ótima é {self.solucao_otima_par[0][2]}-{self.solucao_otima_par[1][2]} com distância {self.solucao_otima_dist:.2f}")

        self.nave_selecionada = self.todas_naves[len(self.todas_naves) // 2]
        self._vincular_eventos()
        self._atualizar_display()
        self.info_label.config(text="Mapa carregado. Use as SETAS para navegar entre as naves. Clique com o MOUSE em duas naves para medir a distância. Quando estiver pronto, selecione uma nave e clique em 'Traçar Mediana' para dividir a frota.")

    def _gerar_naves(self):
        self.todas_naves = []
        num_naves = 21 # Número ímpar para uma mediana clara
        canvas_width = self.canvas.winfo_width() - 60
        canvas_height = self.canvas.winfo_height() - 60
        pontos_gerados = set()
        while len(pontos_gerados) < num_naves:
            x = random.randint(30, canvas_width)
            if x not in [p[0] for p in pontos_gerados]:
                y = random.randint(30, canvas_height)
                pontos_gerados.add((x, y))
        self.todas_naves = sorted([(p[0], p[1], self.nomes_naves[i]) for i, p in enumerate(pontos_gerados)], key=lambda n: n[0])

    def _vincular_eventos(self):
        self.root.bind("<Left>", lambda e: self._navegar_com_seta("left"))
        self.root.bind("<Right>", lambda e: self._navegar_com_seta("right"))
        self.root.bind("<Up>", lambda e: self._navegar_com_seta("up"))
        self.root.bind("<Down>", lambda e: self._navegar_com_seta("down"))
        self.canvas.bind("<Button-1>", self._handle_clique_mouse)

    def _atualizar_display(self):
        self.canvas.delete("all")
        # Desenha linhas de divisão
        for log_item in self.log_acoes:
            if log_item.startswith("Divisão"):
                x_val = float(log_item.split("=")[1])
                self.canvas.create_line(x_val, 0, x_val, self.canvas.winfo_height(), fill="#FFFF00", width=1, dash=(5,3))
        
        # Desenha linha de medição do mouse
        if self.nave_medicao_1 and self.nave_medicao_2:
            p1, p2 = self.nave_medicao_1, self.nave_medicao_2
            distancia = dist(p1, p2)
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="magenta", width=2)
            self.status_label.config(text=f"Distância entre {p1[2]} e {p2[2]}: {distancia:.2f}")
        elif self.nave_medicao_1:
            self.status_label.config(text=f"Medindo a partir da Nave {self.nave_medicao_1[2]}. Clique em outra nave.")
        else:
            self.status_label.config(text=f"Nave selecionada para divisão: {self.nave_selecionada[2]}")

        # Desenha as naves
        for nave in self.todas_naves:
            x, y, nome = nave
            cor_fill = "cyan" if nave == self.nave_selecionada else "#1c1c1c"
            cor_outline = "cyan" if nave == self.nave_selecionada else "white"
            if nave == self.nave_medicao_1 or nave == self.nave_medicao_2: cor_fill = "magenta"; cor_outline="magenta"
            
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=cor_fill, outline=cor_outline, width=2)
            self.canvas.create_text(x, y - 12, text=nome, fill="white", font=self.small_bold_font_obj)

    def _navegar_com_seta(self, direcao):
        self.nave_medicao_1 = self.nave_medicao_2 = None # Limpa a medição
        alvo = self.nave_selecionada
        melhor_candidato = None
        menor_distancia_ponderada = float('inf')

        for candidata in self.todas_naves:
            if candidata == alvo: continue
            
            dx = candidata[0] - alvo[0]
            dy = candidata[1] - alvo[1]
            dist_real = math.hypot(dx, dy)
            
            # Pondera a distância para favorecer a direção desejada
            dist_ponderada = dist_real
            if direcao == "right" and dx > 0: dist_ponderada /= (dx / dist_real)
            elif direcao == "left" and dx < 0: dist_ponderada /= (-dx / dist_real)
            elif direcao == "down" and dy > 0: dist_ponderada /= (dy / dist_real)
            elif direcao == "up" and dy < 0: dist_ponderada /= (-dy / dist_real)
            else: continue # Ignora candidatos na direção errada

            if dist_ponderada < menor_distancia_ponderada:
                menor_distancia_ponderada = dist_ponderada
                melhor_candidato = candidata
        
        if melhor_candidato:
            self.nave_selecionada = melhor_candidato
            self._atualizar_display()

    def _handle_clique_mouse(self, event):
        nave_clicada = None
        for nave in self.todas_naves:
            if dist((event.x, event.y, ''), nave) < 10:
                nave_clicada = nave
                break
        
        if nave_clicada:
            if not self.nave_medicao_1:
                self.nave_medicao_1 = nave_clicada
                self.nave_medicao_2 = None
            elif nave_clicada != self.nave_medicao_1:
                self.nave_medicao_2 = nave_clicada
            else: # Clicou na mesma nave, limpa a medição
                self.nave_medicao_1 = self.nave_medicao_2 = None
            
            self._atualizar_display()
            
    def tracar_mediana(self):
        # A lógica recursiva aqui é simulada através do log
        x_divisao = self.nave_selecionada[0]
        self._adicionar_log(f"Divisão em X={x_divisao} (Nave {self.nave_selecionada[2]})")
        self.nave_medicao_1 = self.nave_medicao_2 = None # Limpa qualquer medição
        self._atualizar_display()
        self.info_label.config(text="Linha de divisão traçada. Continue explorando ou trace outra mediana em um sub-setor para refinar a análise.")

    def _adicionar_log(self, mensagem):
        self.log_acoes.insert(0, mensagem)
        self.log_listbox.delete(0, tk.END)
        for item in self.log_acoes: self.log_listbox.insert(tk.END, item)

    def finalizar_missao(self):
        if not self.nave_medicao_1 or not self.nave_medicao_2:
            messagebox.showwarning("Análise Incompleta", "Você precisa selecionar um par de naves clicando nelas para reportar a vulnerabilidade final.", parent=self.base_content_frame)
            return

        dist_jogador = dist(self.nave_medicao_1, self.nave_medicao_2)
        
        if abs(dist_jogador - self.solucao_otima_dist) < 0.01:
            pontos = 500
            self.game_manager.add_score(pontos)
            messagebox.showinfo("Sucesso Tático!", f"Análise Perfeita, Comandante! Você encontrou a vulnerabilidade crítica entre as naves {self.solucao_otima_par[0][2]} e {self.solucao_otima_par[1][2]} com uma distância de {dist_jogador:.2f} unidades.\n"
                                f"A frota de ataque já está a caminho!\n"
                                f"Você ganhou {pontos} pontos de influência.", parent=self.base_content_frame)
            self.game_manager.mission_completed("MissaoDC3")
        else:
            self.game_manager.add_score(-100)
            messagebox.showerror("Falha na Análise", f"Comandante, o par que você reportou tem distância {dist_jogador:.2f}, mas a vulnerabilidade real era de {self.solucao_otima_dist:.2f} entre as naves {self.solucao_otima_par[0][2]} e {self.solucao_otima_par[1][2]}.\n"
                                 "Perdemos a janela de oportunidade. A operação foi abortada. Menos 100 pontos de influência.", parent=self.base_content_frame)
            self.game_manager.mission_failed_options(self, "Falha na análise da frota.", "Fulcrum: \"A precisão é tudo nestas operações. Tente novamente.\"")

    def retry_mission(self):
        self.iniciar_fase_interativa()