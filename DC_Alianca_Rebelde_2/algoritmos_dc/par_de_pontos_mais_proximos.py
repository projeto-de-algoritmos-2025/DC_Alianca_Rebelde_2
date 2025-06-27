# algoritmos_dc/par_de_pontos_mais_proximos.py
import math

def dist(p1, p2):
    """Calcula a distância euclidiana entre dois pontos (ignora o nome)."""
    # p1 e p2 são tuplas como (x, y, nome)
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Deixaremos a função de solução ótima aqui para quando precisarmos dela
def encontrar_par_mais_proximo(pontos):
    if len(pontos) < 2: return float('inf'), (None, None)
    dist_min = float('inf')
    par = (None, None)
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            d = dist(pontos[i], pontos[j])
            if d < dist_min:
                dist_min = d; par = (pontos[i], pontos[j])
    return dist_min, par