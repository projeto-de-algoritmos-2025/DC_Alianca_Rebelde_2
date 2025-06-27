import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont, simpledialog
import random
import math
import re

# ==============================================================================
# FUNÇÕES AUXILIARES DO ALGORITMO 
# ==============================================================================

def dist(p1, p2):
    """Calcula a distância euclidiana entre dois pontos (naves)."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def encontrar_par_mais_proximo(pontos):
    """Função de fachada para o algoritmo. Ordena os pontos e inicia a recursão."""
    if len(pontos) < 2:
        return float('inf'), (None, None)
    
    # Pré-ordena por X e Y
    px = sorted(pontos, key=lambda p: p[0])
    py = sorted(pontos, key=lambda p: p[1])
    return _encontrar_par_recursivo(px, py)

def _encontrar_par_recursivo(px, py):
    """Função recursiva principal do algoritmo."""
    n = len(px)
    if n <= 3:
        min_dist = float('inf')
        par = (None, None)
        for i in range(n):
            for j in range(i + 1, n):
                d = dist(px[i], px[j])
                if d < min_dist:
                    min_dist = d
                    par = (px[i], px[j])
        return min_dist, par

    # Dividir
    mid = n // 2
    ponto_mediano = px[mid]
    
    # Separa os pontos em metades esquerda e direita
    px_esq = px[:mid]
    px_dir = px[mid:]
    
    py_esq = []
    py_dir = []
    # Otimização: Separa py em O(n) ao invés de reordenar
    for p in py:
        if p[0] < ponto_mediano[0] or (p[0] == ponto_mediano[0] and p in px_esq):
            py_esq.append(p)
        else:
            py_dir.append(p)

    # Conquistar recursivamente
    (dist_esq, par_esq) = _encontrar_par_recursivo(px_esq, py_esq)
    (dist_dir, par_dir) = _encontrar_par_recursivo(px_dir, py_dir)

    # Combinar (encontrar o delta inicial)
    delta = min(dist_esq, dist_dir)
    par_min = par_esq if dist_esq <= dist_dir else par_dir

    # Combinar (verificar a faixa)
    faixa_y = [p for p in py if abs(p[0] - ponto_mediano[0]) < delta]
    
    # A verificação da faixa só precisa checar os próximos 7 pontos (otimização)
    for i in range(len(faixa_y)):
        for j in range(i + 1, min(i + 8, len(faixa_y))):
            d = dist(faixa_y[i], faixa_y[j])
            if d < delta:
                delta = d
                par_min = (faixa_y[i], faixa_y[j])

    return delta, par_min

# ==============================================================================
# CLASSE DO DROIDE DE AUXÍLIO
# ==============================================================================

class HelperDroid(tk.Toplevel):
    def __init__(self, parent, game_manager):
        super().__init__(parent)
        self.overrideredirect(True) # Remove a barra de título e bordas
        self.withdraw() # Começa escondido
        self.attributes("-alpha", 0.9)
        self.attributes("-topmost", True)

        try:
            bg_color = game_manager.bg_color
            fg_color = game_manager.fg_color_light
            droid_font = game_manager.narrative_font_obj
        except AttributeError:
            bg_color = "#1c1c1c"
            fg_color = "cyan"
            droid_font = ("Consolas", 11)

        self.config(bg=bg_color, relief="solid", borderwidth=2)
        
        main_frame = tk.Frame(self, bg=bg_color, padx=15, pady=15)
        main_frame.pack()

        header_frame = tk.Frame(main_frame, bg=bg_color)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="●", font=("Arial", 14, "bold"), fg="red", bg=bg_color).pack(side=tk.LEFT)
        tk.Label(header_frame, text="PA09DC - Tactical Droid", font=("Courier", 10, "bold"), fg=fg_color, bg=bg_color).pack(side=tk.LEFT, padx=5)

        self.message_label = tk.Label(
            main_frame, text="Inicializando...", font=droid_font, 
            wraplength=380, justify=tk.LEFT, fg=fg_color, bg=bg_color
        )
        self.message_label.pack(pady=(10, 0))

    def show_message(self, message, parent_widget):
        self.message_label.config(text=message)
        self.update_idletasks()
        
        parent_x = parent_widget.winfo_rootx()
        parent_y = parent_widget.winfo_rooty()
        self.geometry(f"+{parent_x + 320}+{parent_y + 50}")
        self.deiconify()

    def hide(self):
        self.withdraw()

# ==============================================================================
# CLASSE PRINCIPAL DA MISSÃO 3
# ==============================================================================

class MissaoDC3:
    def __init__(self, root, game_manager, content_frame_para_missao):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame_para_missao

        self._carregar_estilos()
        
        # Dados e Estado da Missão
        self.nomes_naves = [f"{chr(ord('A') + i % 26)}{i // 26 if i // 26 > 0 else ''}" for i in range(52)]
        self.todas_naves = []
        self.solucao_otima_dist, self.solucao_otima_par = 0, (None, None)
        self.menor_distancia_global = float('inf')
        self.melhor_par_global = (None, None)
        
        self.nave_selecionada = None
        self.nave_medicao_1 = None
        self.nave_medicao_2 = None
        self.linhas_de_divisao = []
        self.log_acoes = []
        self.intervalo_selecionado = None
        self.quadros_de_analise = []
        self.contador_operacoes = 0
        
        self.linha_selecionada_para_combinacao = None
        self.quadros_para_combinar = None
        self.resultados_combinacao = []
        self.faixa_a_desenhar = None

        # Referências de UI
        self.canvas = None
        self.info_label = None
        self.botoes_acao_frame = None
        self.nave_selecionada_coord_label = None
        self.btn_analisar_intervalo = None
        self.btn_combinar_analises = None
        self.menor_distancia_label = None
        
        # Droide e estado do guia
        self.helper_droid = HelperDroid(self.root, self.game_manager)
        self.estado_guia = "INICIO"

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.cor_info = "#87CEFA"
            self.cor_ponto_selecionado = "red"
            self.header_font_obj = self.game_manager.header_font_obj
            self.narrative_font_obj = self.game_manager.narrative_font_obj
            self.button_font_obj = self.game_manager.button_font_obj
            self.small_bold_font_obj = self.game_manager.small_bold_font_obj
        except AttributeError:
            print("AVISO MissaoDC3: Usando fallbacks de cores/fontes.")
            self.cor_fundo = "black"; self.cor_texto = "white"; self.cor_titulo="orangered"; self.cor_info="lightblue"
            self.header_font_obj = ("Arial", 20, "bold"); self.narrative_font_obj = ("Arial", 12)

    def _limpar_frame_e_eventos(self):
        self.helper_droid.hide()
        if hasattr(self, 'canvas') and self.canvas and self.canvas.winfo_exists():
            for event in ["<Left>", "<Right>", "<Up>", "<Down>", "<Return>", "<Button-1>"]:
                self.canvas.unbind(event)
        for widget in self.base_content_frame.winfo_children(): widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame_e_eventos()
        tk.Label(self.base_content_frame, text="MISSÃO 3: Duelo no Hiperespaço", font=self.header_font_obj, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(10,15))
        imagem_missao = self.game_manager.imagens.get("Cena5.png")
        if imagem_missao:
            tk.Label(self.base_content_frame, image=imagem_missao, bg=self.cor_fundo).pack(pady=10)
        
        contexto = ("Fulcrum: \"Comandante, sua missão é analisar o mapa tático da frota e encontrar o par de naves mais próximo. Use a doutrina 'Dividir e Conquistar'. Divida recursivamente a frota, analise os casos base e combine os resultados. Cada decisão é sua.\"")
        tk.Label(self.base_content_frame, text=contexto, wraplength=700, justify=tk.LEFT, font=self.narrative_font_obj, fg=self.cor_texto, bg=self.cor_fundo).pack(pady=10, padx=20)
        ttk.Button(self.base_content_frame, text="Analisar Mapa Tático...", command=self.iniciar_fase_interativa, style="Accent.Dark.TButton").pack(pady=20)
         
    def iniciar_fase_interativa(self):
        self._limpar_frame_e_eventos()
        main_frame = tk.Frame(self.base_content_frame, bg=self.cor_fundo); main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(main_frame, bg="#0d0d2e", highlightthickness=0, takefocus=1); self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
         
        control_panel = tk.Frame(main_frame, bg=self.cor_fundo, padx=10, pady=10, width=300)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y); control_panel.pack_propagate(False)

        self.info_label = tk.Label(control_panel, text="Instruções...", font=self.narrative_font_obj, wraplength=280, justify=tk.LEFT, fg=self.cor_texto, bg=self.cor_fundo)
        self.info_label.pack(anchor="n", pady=5, fill=tk.X)
         
        nave_status_frame = tk.LabelFrame(control_panel, text="Status da Frota", font=self.small_bold_font_obj, bg=self.cor_fundo, fg=self.cor_texto, padx=10, pady=5)
        nave_status_frame.pack(pady=10, fill=tk.X, anchor="n")
        self.total_naves_label = tk.Label(nave_status_frame, text="Naves na Formação: ...", font=self.small_bold_font_obj, fg=self.cor_info, bg=self.cor_fundo, justify=tk.LEFT)
        self.total_naves_label.pack(anchor="w")
        self.nave_selecionada_coord_label = tk.Label(nave_status_frame, text="Nave Selecionada: N/A", font=self.small_bold_font_obj, fg=self.cor_info, bg=self.cor_fundo, justify=tk.LEFT)
        self.nave_selecionada_coord_label.pack(anchor="w")

        distancia_frame = tk.LabelFrame(control_panel, text="Menor Distância Analisada", font=self.small_bold_font_obj, bg=self.cor_fundo, fg=self.cor_texto, padx=10, pady=5)
        distancia_frame.pack(pady=10, fill=tk.X, anchor="n")
        self.menor_distancia_label = tk.Label(distancia_frame, text="δ Global: ∞ | Par: N/A", font=self.small_bold_font_obj, fg="#7FFF00", bg=self.cor_fundo, justify=tk.LEFT)
        self.menor_distancia_label.pack(anchor="w")

        self.botoes_acao_frame = tk.Frame(control_panel, bg=self.cor_fundo)
        self.botoes_acao_frame.pack(pady=10, fill=tk.X)
        log_frame = tk.LabelFrame(control_panel, text="Log de Operações", font=self.small_bold_font_obj, bg=self.cor_fundo, fg=self.cor_texto, padx=5, pady=5)
        log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.log_listbox = tk.Listbox(log_frame, font=("Courier", 9), bg="#1c1c1c", fg="lightgrey", borderwidth=0, highlightthickness=0)
        self.log_listbox.pack(fill=tk.BOTH, expand=True)
         
        self.root.after(100, self._setup_inicial_canvas)

    def _atualizar_guia(self, proximo_estado=None):
        if proximo_estado:
            self.estado_guia = proximo_estado

        mensagem = ""
        if self.estado_guia == "INICIO":
            mensagem = ("Olá, Comandante. Sou PA09DC. Nossa missão é achar o par de naves mais próximo usando 'Dividir e Conquistar'.\n\n"
                        "Passo 1: Divida a frota ao meio. Selecione a nave mediana (central) e pressione ENTER.")
        elif self.estado_guia == "DIVIDIR_ESQUERDA":
             mensagem = ("Ótimo. Agora, vamos resolver o subproblema da **ESQUERDA** primeiro.\n\n"
                        "Selecione um intervalo à esquerda da primeira linha e continue dividindo-o até isolar um grupo pequeno (1 a 3 naves).")
        elif self.estado_guia == "ANALISAR_BASE":
             mensagem = ("Perfeito, você isolou um grupo pequeno. Este é um 'caso base'.\n\n"
                         "Clique no botão 'Analisar Caso Base'. O algoritmo será usado para encontrar o par mais próximo neste pequeno grupo.")
        elif self.estado_guia == "PREPARAR_COMBINACAO":
             mensagem = ("Análises prontas! Agora, o passo 'Combinar'.\n\n"
                         "Clique na linha de divisão entre as duas análises que você quer combinar e depois clique em 'Combinar Análises'.")
        elif self.estado_guia == "FAIXA_DELTA":
            delta = min(self.quadros_para_combinar[0]['d_val'], self.quadros_para_combinar[1]['d_val'])
            mensagem = (f"Iniciando combinação... O menor delta (δ) entre os dois lados é {delta:.2f}.\n\n"
                        f"Agora, o passo crucial: verificamos uma 'faixa' de largura 2*δ ao redor da linha. Destaquei esta faixa em amarelo.")
        elif self.estado_guia == "CONTINUAR":
             mensagem = ("Bom trabalho. O processo se repete: Dividir, Conquistar e Combinar.\n\n"
                         "Continue até que todo o mapa tático seja coberto por uma única análise final.")
        
        if mensagem:
             self.helper_droid.show_message(mensagem, self.base_content_frame)

    def _setup_inicial_canvas(self):
        self.base_content_frame.update_idletasks()
        self._gerar_naves()
        self.solucao_otima_dist, self.solucao_otima_par = encontrar_par_mais_proximo(self.todas_naves)
        print(f"DEBUG: Solução ótima é {self.solucao_otima_par[0][2]}-{self.solucao_otima_par[1][2]} com distância {self.solucao_otima_dist:.2f}")

        px = sorted(self.todas_naves, key=lambda p: p[0])
        self.nave_selecionada = px[len(px) // 2]
         
        self._vincular_eventos()
        self.info_label.config(text="Use as setas para selecionar uma nave e ENTER para dividir, ou clique no mapa.")
        self._atualizar_display_canvas()
        self.total_naves_label.config(text=f"Naves na Formação: {len(self.todas_naves)}")
        self._atualizar_painel_info_nave()
        self._atualizar_controles()
        self._atualizar_guia("INICIO")

    def _gerar_naves(self):
        self.todas_naves = []
        num_naves = random.randint(13, 17)
        canvas_width = self.canvas.winfo_width() - 60
        canvas_height = self.canvas.winfo_height() - 60
        if canvas_width < 100 or canvas_height < 100:
            canvas_width, canvas_height = 800, 500

        DISTANCIA_MINIMA_X = 30
        pontos_gerados = []
        
        max_tentativas = num_naves * 20
        for _ in range(max_tentativas):
            if len(self.todas_naves) >= num_naves: break
            
            x = random.randint(30, canvas_width)
            
            x_valido = True
            for p in pontos_gerados:
                if abs(p[0] - x) < DISTANCIA_MINIMA_X:
                    x_valido = False
                    break
            
            if x_valido:
                y = random.randint(30, canvas_height)
                nome_nave = self.nomes_naves[len(self.todas_naves)]
                ponto_novo = (x, y, nome_nave)
                self.todas_naves.append(ponto_novo)
                pontos_gerados.append(ponto_novo)

        self.todas_naves.sort(key=lambda n: n[0])

    def _vincular_eventos(self):
        self.canvas.bind("<Left>", lambda e: self._navegar_com_seta("left"))
        self.canvas.bind("<Right>", lambda e: self._navegar_com_seta("right"))
        self.canvas.bind("<Up>", lambda e: self._navegar_com_seta("up"))
        self.canvas.bind("<Down>", lambda e: self._navegar_com_seta("down"))
        self.canvas.bind("<Return>", self.tracar_mediana)
        self.canvas.bind("<Button-1>", self._handle_clique_mouse)
        self.canvas.focus_set()

    def _atualizar_display_canvas(self):
        self.canvas.delete("all")

        if self.faixa_a_desenhar:
            x_start, x_end = self.faixa_a_desenhar
            self.canvas.create_rectangle(x_start, 0, x_end, self.canvas.winfo_height(),
                                         fill="#E8D935", stipple="gray50", outline="")

        if self.intervalo_selecionado:
            x_start, x_end = self.intervalo_selecionado
            self.canvas.create_rectangle(x_start, 0, x_end, self.canvas.winfo_height(), fill="yellow", stipple="gray25", outline="")
        
        for linha_data in self.linhas_de_divisao:
            x_val, label_num = linha_data['x'], linha_data['label']
            cor_linha = "cyan" if linha_data == self.linha_selecionada_para_combinacao else "#E0B0FF"
            largura_linha = 2 if linha_data == self.linha_selecionada_para_combinacao else 1
            self.canvas.create_line(x_val, 0, x_val, self.canvas.winfo_height(), fill=cor_linha, width=largura_linha, dash=(5,3))
            self.canvas.create_text(x_val + 5, 10, text=label_num, fill=cor_linha, font=self.small_bold_font_obj, anchor="nw")
         
        if self.nave_medicao_1 and self.nave_medicao_2:
            p1, p2 = self.nave_medicao_1, self.nave_medicao_2; 
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="magenta", width=2)
            d = dist(p1, p2)
            mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            self.canvas.create_text(mid_x, mid_y - 10, text=f"{d:.1f}", fill="magenta", font=self.small_bold_font_obj)

        for resultado in self.resultados_combinacao:
            p1, p2, dist_val = resultado['p1'], resultado['p2'], resultado['dist']
            cor_resultado = "#7FFF00"
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=cor_resultado, width=2, dash=(6, 2))
            mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            self.canvas.create_text(mid_x, mid_y + 10, text=f"δ={dist_val:.1f}", fill=cor_resultado, font=self.small_bold_font_obj)
         
        for nave in self.todas_naves:
            x, y, nome = nave
            cor_fill = self.cor_fundo; cor_outline = "white"
            if nave == self.nave_selecionada: cor_fill = cor_outline = self.cor_ponto_selecionado
            if nave == self.nave_medicao_1 or nave == self.nave_medicao_2: cor_fill = cor_outline="magenta"
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=cor_fill, outline=cor_outline, width=2)
            self.canvas.create_text(x, y - 12, text=nome, fill=cor_outline, font=self.small_bold_font_obj)
         
        for quadro in self.quadros_de_analise:
            x, y = quadro['pos']
            self.canvas.create_rectangle(x, y, x + 160, y + 65, fill="#1c1c1c", outline="cyan", width=2)
            texto_quadro = f"Análise {quadro['id']}\n{quadro['d']}\n{quadro['p']}\n{quadro['y']}"
            self.canvas.create_text(x + 5, y + 5, text=texto_quadro, anchor="nw", fill="cyan", font=("Courier", 9))

    def _atualizar_painel_info_nave(self):
        if self.nave_selecionada and self.nave_selecionada_coord_label.winfo_exists():
            x, y, nome = self.nave_selecionada
            self.nave_selecionada_coord_label.config(text=f"Nave Sel: {nome} (X:{int(x)}, Y:{int(y)})")

    def _atualizar_controles(self):
        for btn in self.botoes_acao_frame.winfo_children(): btn.destroy()
        ttk.Button(self.botoes_acao_frame, text="Traçar Mediana (Enter)", command=self.tracar_mediana, style="Dark.TButton").pack(fill=tk.X, pady=2)
         
        self.btn_analisar_intervalo = ttk.Button(self.botoes_acao_frame, text="Analisar Caso Base (Intervalo)", command=self.analisar_intervalo, style="Dark.TButton")
        self.btn_analisar_intervalo.pack(fill=tk.X, pady=2)
         
        self.btn_combinar_analises = ttk.Button(self.botoes_acao_frame, text="Combinar Análises", command=self.combinar_analises, style="Dark.TButton")
        self.btn_combinar_analises.pack(fill=tk.X, pady=2)
         
        ttk.Button(self.botoes_acao_frame, text="Reportar Vulnerabilidade Final", command=self.finalizar_missao, style="Accent.Dark.TButton").pack(fill=tk.X, pady=(10,2))
         
        self.btn_analisar_intervalo.config(state=tk.NORMAL if self.intervalo_selecionado and self._pode_analisar_intervalo() else tk.DISABLED)
        self.btn_combinar_analises.config(state=tk.NORMAL if self.linha_selecionada_para_combinacao else tk.DISABLED)

    def _navegar_com_seta(self, direcao):
        self._resetar_estados_de_selecao()
        if not (self.nave_medicao_1 and self.nave_medicao_2):
             self.nave_medicao_1 = self.nave_medicao_2 = None

        if not self.nave_selecionada: self.nave_selecionada = self.todas_naves[0] if self.todas_naves else None
        if not self.nave_selecionada: return
         
        lista_ordenada_x = sorted(self.todas_naves, key=lambda p: p[0])
        lista_ordenada_y = sorted(self.todas_naves, key=lambda p: p[1])
        try:
            if direcao in ["left", "right"]:
                idx_atual = lista_ordenada_x.index(self.nave_selecionada)
                novo_idx = (idx_atual + (-1 if direcao == "left" else 1)) % len(lista_ordenada_x)
                self.nave_selecionada = lista_ordenada_x[novo_idx]
            else:
                idx_atual = lista_ordenada_y.index(self.nave_selecionada)
                novo_idx = (idx_atual + (-1 if direcao == "up" else 1)) % len(lista_ordenada_y)
                self.nave_selecionada = lista_ordenada_y[novo_idx]
        except ValueError: self.nave_selecionada = self.todas_naves[0] if self.todas_naves else None
         
        self._atualizar_display_canvas()
        self._atualizar_painel_info_nave()
        self._atualizar_controles()
         
    def _handle_clique_mouse(self, event):
        x_clique, y_clique = event.x, event.y
        self._resetar_estados_de_selecao()
         
        # Prioridade 1: Clicou em uma nave? (Medição manual)
        nave_clicada = None
        for nave in self.todas_naves:
            if dist((x_clique, y_clique, ''), nave) < 10:
                nave_clicada = nave
                break

        if nave_clicada:
            if not self.nave_medicao_1:
                self.nave_medicao_1 = nave_clicada
                self.info_label.config(text=f"Medição manual: Nave {nave_clicada[2]} selecionada. Clique em outra para medir a distância.")
            elif nave_clicada != self.nave_medicao_1:
                self.nave_medicao_2 = nave_clicada
                d = dist(self.nave_medicao_1, self.nave_medicao_2)
                self.info_label.config(text=f"Distância manual entre {self.nave_medicao_1[2]} e {self.nave_medicao_2[2]}: {d:.2f}\nPara reportar o resultado final, use o botão.")
            self._atualizar_display_canvas()
            self.canvas.focus_set()
            return

        self.nave_medicao_1 = self.nave_medicao_2 = None

        # Prioridade 2: Clicou perto de uma linha de mediana? (Preparar para combinar)
        linha_clicada = None
        for linha in self.linhas_de_divisao:
            if abs(x_clique - linha['x']) < 5: 
                linha_clicada = linha
                break
         
        if linha_clicada:
            self._preparar_combinacao(linha_clicada)
            self._atualizar_display_canvas()
            self._atualizar_controles()
            self.canvas.focus_set()
            return
             
        # Prioridade 3: Clicou em um espaço vazio (intervalo)?
        bordas_x = sorted([0] + [l['x'] for l in self.linhas_de_divisao] + [self.canvas.winfo_width()])
        for i in range(len(bordas_x) - 1):
            if bordas_x[i] <= x_clique < bordas_x[i+1]:
                self.intervalo_selecionado = (bordas_x[i], bordas_x[i+1])
                self._verificar_estado_intervalo_selecionado()
                break
         
        self._atualizar_display_canvas()
        self._atualizar_controles()
        self.canvas.focus_set()
         
    def _resetar_estados_de_selecao(self):
        self.intervalo_selecionado = None
        self.linha_selecionada_para_combinacao = None
        self.quadros_para_combinar = None
        self.faixa_a_desenhar = None

    def _verificar_estado_intervalo_selecionado(self):
        if not self.intervalo_selecionado:
             self.info_label.config(text="Use as setas ou clique no mapa para continuar.")
             return

        naves_no_intervalo = self._naves_no_intervalo(self.intervalo_selecionado)
        nomes_naves_str = ", ".join([p[2] for p in naves_no_intervalo]) if naves_no_intervalo else "Nenhuma"
         
        if self._pode_analisar_intervalo():
            self.info_label.config(text=f"Passo 2b: Resolver Caso Base.\n\nIntervalo contém {len(naves_no_intervalo)} naves: [{nomes_naves_str}]. Clique em 'Analisar Caso Base'.")
            self._atualizar_guia("ANALISAR_BASE")
        else:
            plural = "s" if len(naves_no_intervalo) != 1 else ""
            self.info_label.config(text=f"Passo 2a: Conquistar.\n\nEste intervalo tem {len(naves_no_intervalo)} nave{plural}. Continue dividindo (ENTER) até isolar um grupo pequeno.")
            if len(self.linhas_de_divisao) > 0:
                self._atualizar_guia("DIVIDIR_ESQUERDA")
            else:
                self._atualizar_guia("CONTINUAR")
     
    def _naves_no_intervalo(self, intervalo):
        x_start, x_end = intervalo
        return [p for p in self.todas_naves if x_start <= p[0] < x_end]

    def _quadro_no_intervalo(self, intervalo):
        x_start, x_end = intervalo
        for q in self.quadros_de_analise:
            # Um quadro pertence ao intervalo se sua origem estiver nele
            if x_start <= q['origem_x'] < x_end:
                return q
        return None

    def _pode_analisar_intervalo(self):
        if not self.intervalo_selecionado: return False
        naves_no_intervalo = self._naves_no_intervalo(self.intervalo_selecionado)
        quadro_existente = self._quadro_no_intervalo(self.intervalo_selecionado)
        # O caso base é para 3 ou menos naves
        return len(naves_no_intervalo) > 0 and len(naves_no_intervalo) <= 3 and not quadro_existente

    def analisar_intervalo(self):
        if not self._pode_analisar_intervalo(): return
        
        naves_no_intervalo = self._naves_no_intervalo(self.intervalo_selecionado)
        
        # Simula a chamada recursiva para o caso base
        dist_base, par_base = _encontrar_par_recursivo(naves_no_intervalo, [])
        
        self.contador_operacoes += 1
        id_quadro = self.contador_operacoes
        
        p_str = "Ø" if not par_base[0] else f"{{{par_base[0][2]},{par_base[1][2]}}}"
        y_str = ", ".join(p[2] for p in naves_no_intervalo)
        
        # Posição do quadro de análise
        x_medio_intervalo = (self.intervalo_selecionado[0] + self.intervalo_selecionado[1]) / 2
        
        quadro_info = {
            'id': f"A{id_quadro}",
            'pos': (x_medio_intervalo - 80, 120),
            'origem_x': naves_no_intervalo[0][0], # Usa a primeira nave como referência de origem
            'd_val': dist_base,
            'd': f"d = {dist_base:.2f}" if dist_base != float('inf') else "d = ∞",
            'p_val': par_base,
            'p': f"p = {p_str}",
            'y_val': naves_no_intervalo,
            'y': f"Y = {{{y_str}}}"
        }
        
        self.quadros_de_analise.append(quadro_info)
        self._adicionar_log(f"Op {id_quadro}: Caso Base analisado. Resultado: d = {dist_base:.2f}")
        
        self._resetar_estados_de_selecao()
        self.info_label.config(text="Caso base resolvido. Continue ou clique em uma linha para combinar.")
        self._atualizar_display_canvas()
        self._atualizar_controles()
        self.canvas.focus_set()
        self._atualizar_guia("PREPARAR_COMBINACAO")

    def tracar_mediana(self, event=None):
        if not self.nave_selecionada: return
        x_selecionado = self.nave_selecionada[0]
        # Evita traçar linhas quase no mesmo lugar
        if any(abs(l['x'] - (x_selecionado + 1)) < 5 for l in self.linhas_de_divisao): return

        self.contador_operacoes += 1
        self.linhas_de_divisao.append({'x': x_selecionado + 1, 'label': str(self.contador_operacoes)})
        self._adicionar_log(f"Op {self.contador_operacoes}: Divisão em X={x_selecionado+1:.1f}")
         
        self._resetar_estados_de_selecao()
        self.info_label.config(text="Divisão criada. Clique em um dos novos intervalos para continuar.")
        self._atualizar_display_canvas()
        self._atualizar_controles()
        self.canvas.focus_set()
        if len(self.linhas_de_divisao) == 1:
            self._atualizar_guia("DIVIDIR_ESQUERDA")
        else:
            self._atualizar_guia("CONTINUAR")

    def _preparar_combinacao(self, linha):
        x_linha = linha['x']
        bordas = sorted([0] + [l['x'] for l in self.linhas_de_divisao] + [self.canvas.winfo_width()])
        try:
            idx_linha = bordas.index(x_linha)
        except ValueError:
            return # Linha não encontrada
         
        if idx_linha == 0 or idx_linha == len(bordas) - 1: return
         
        intervalo_esq = (bordas[idx_linha - 1], x_linha)
        intervalo_dir = (x_linha, bordas[idx_linha + 1])
         
        quadro_esq = self._quadro_no_intervalo(intervalo_esq)
        quadro_dir = self._quadro_no_intervalo(intervalo_dir)
         
        if quadro_esq and quadro_dir:
            self.linha_selecionada_para_combinacao = linha
            self.quadros_para_combinar = (quadro_esq, quadro_dir)
            self.info_label.config(text=f"Passo 3: Combinar.\n\nPronto para combinar as análises {quadro_esq['id']} (esquerda) e {quadro_dir['id']} (direita).")
            self._atualizar_guia("PREPARAR_COMBINACAO")
        else:
            msg = "Não é possível combinar nesta linha.\n"
            if not quadro_esq: msg += "O sub-problema à esquerda ainda não foi resolvido.\n"
            if not quadro_dir: msg += "O sub-problema à direita ainda não foi resolvido."
            self.info_label.config(text=msg)
            self.linha_selecionada_para_combinacao = None
            self.quadros_para_combinar = None

    def combinar_analises(self):
        if not self.linha_selecionada_para_combinacao or not self.quadros_para_combinar: return
         
        q_esq, q_dir = self.quadros_para_combinar
        x_linha = self.linha_selecionada_para_combinacao['x']

        d_esq, p_esq, y_esq = q_esq['d_val'], q_esq['p_val'], q_esq['y_val']
        d_dir, p_dir, y_dir = q_dir['d_val'], q_dir['p_val'], q_dir['y_val']

        delta = min(d_esq, d_dir)
        par_min = p_esq if d_esq <= d_dir else p_dir
        self._adicionar_log(f"Combinando... δ inicial = min({d_esq:.1f}, {d_dir:.1f}) = {delta:.1f}")

        self.faixa_a_desenhar = (x_linha - delta, x_linha + delta)
        self._atualizar_guia("FAIXA_DELTA")
        self._atualizar_display_canvas()
        self.root.update_idletasks()

        faixa_y = [p for p in sorted(y_esq + y_dir, key=lambda p: p[1]) if abs(p[0] - x_linha) < delta]
        self._adicionar_log(f"Verificando faixa 2*δ ({2*delta:.1f}). Naves: {[p[2] for p in faixa_y]}")
         
        for i in range(len(faixa_y)):
            for j in range(i + 1, min(i + 8, len(faixa_y))):
                p1, p2 = faixa_y[i], faixa_y[j]
                d = dist(p1, p2)
                if d < delta:
                    self._adicionar_log(f"  -> Ponto na faixa! d({p1[2]},{p2[2]})={d:.1f} < {delta:.1f}. Novo δ!")
                    delta = d
                    par_min = (p1, p2)
         
        self.contador_operacoes += 1
        id_novo_quadro = self.contador_operacoes
        p_str = "Ø" if not par_min[0] else f"{{{par_min[0][2]},{par_min[1][2]}}}"
        y_combinado = sorted(y_esq + y_dir, key=lambda p: p[1])
        y_str = ", ".join(p[2] for p in y_combinado)

        novo_quadro = {'id': f"A{id_novo_quadro}", 'pos': (x_linha - 80, 40), 'origem_x': x_linha,
                       'd_val': delta, 'd': f"d = {delta:.2f}", 'p_val': par_min, 'p': f"p = {p_str}",
                       'y_val': y_combinado, 'y': f"Y = {{{y_str[:15]}...}}"}
        self.quadros_de_analise.append(novo_quadro)
        self._adicionar_log(f"Op {id_novo_quadro}: Combinação de {q_esq['id']}+{q_dir['id']} concluída. δ final={delta:.2f}")

        if par_min[0]:
            resultado = {'p1': par_min[0], 'p2': par_min[1], 'dist': delta}
            self.resultados_combinacao.append(resultado)
            if delta < self.menor_distancia_global:
                self.menor_distancia_global = delta
                self.melhor_par_global = par_min
                self.menor_distancia_label.config(text=f"δ Global: {delta:.2f}\nPar: {par_min[0][2]}-{par_min[1][2]}")
                self._adicionar_log(f"NOVO RECORDE GLOBAL: {delta:.2f}!")

        self.info_label.config(text=f"Combinação completa! δ final = {delta:.2f}.\n\nContinue o processo.")

        self.root.after(3500, self._limpar_faixa_e_resetar)

    def _limpar_faixa_e_resetar(self):
        self._resetar_estados_de_selecao()
        self._atualizar_display_canvas()
        self._atualizar_controles()
        self.canvas.focus_set()
        self._atualizar_guia("CONTINUAR")

    def _adicionar_log(self, mensagem):
        if hasattr(self, 'log_listbox') and self.log_listbox and self.log_listbox.winfo_exists():
            self.log_acoes.insert(0, mensagem)
            self.log_listbox.delete(0, tk.END)
            for item in self.log_acoes: self.log_listbox.insert(tk.END, item)

    def finalizar_missao(self):
        self.helper_droid.hide()
        input_str = simpledialog.askstring("Reportar Vulnerabilidade", 
                                        "Digite os nomes das duas naves mais próximas, separados por vírgula (ex: G,N):",
                                        parent=self.base_content_frame)
        if not input_str:
            return

        try:
            nomes = [nome.strip().upper() for nome in input_str.split(',')]
            if len(nomes) != 2:
                raise ValueError("Forneça exatamente dois nomes de naves, separados por vírgula.")
             
            nave_map = {nave[2]: nave for nave in self.todas_naves}
            nave1_nome, nave2_nome = nomes[0], nomes[1]

            if nave1_nome not in nave_map or nave2_nome not in nave_map:
                raise ValueError(f"Nome(s) de nave inválido(s).")
             
            if nave1_nome == nave2_nome:
                raise ValueError("Os nomes das naves devem ser diferentes.")

            nave_jogador_1 = nave_map[nave1_nome]
            nave_jogador_2 = nave_map[nave2_nome]
            dist_jogador = dist(nave_jogador_1, nave_jogador_2)
            par_jogador_nomes = sorted((nave_jogador_1[2], nave_jogador_2[2]))
            par_otimo_nomes = sorted((self.solucao_otima_par[0][2], self.solucao_otima_par[1][2]))

            if abs(dist_jogador - self.solucao_otima_dist) < 0.01 and par_jogador_nomes == par_otimo_nomes:
                pontos = 500
                self.game_manager.add_score(pontos)
                messagebox.showinfo("Sucesso Tático!", f"Análise Perfeita! Vulnerabilidade encontrada entre {self.solucao_otima_par[0][2]}-{self.solucao_otima_par[1][2]} com distância {dist_jogador:.2f}.\nVocê ganhou {pontos} pontos!", parent=self.base_content_frame)
                self.game_manager.mission_completed("MissaoDC3")
            else:
                self.game_manager.add_score(-100)
                messagebox.showerror("Falha na Análise", f"O par {par_jogador_nomes[0]}-{par_jogador_nomes[1]} tem distância {dist_jogador:.2f}, mas a vulnerabilidade real era {self.solucao_otima_dist:.2f} entre {par_otimo_nomes[0]}-{par_otimo_nomes[1]}.\nPerdemos a oportunidade.", parent=self.base_content_frame)
                self.game_manager.mission_failed_options(self, "Falha na análise da frota.", "Fulcrum: \"Precisão é tudo. Tente novamente.\"")

        except ValueError as e:
            messagebox.showwarning("Entrada Inválida", str(e), parent=self.base_content_frame)
            return

    def retry_mission(self):
        print("MissaoDC3: retry_mission chamada.")
        self.game_manager.set_game_state("START_MISSION_DC_3")