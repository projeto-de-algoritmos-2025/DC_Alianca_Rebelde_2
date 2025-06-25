# algoritmos_dc/closest_pair.py
import math

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_pair_otimo(pontos):
    """Função de referência que calcula a solução ótima para comparação."""
    px = sorted(pontos, key=lambda p: p[0])
    py = sorted(pontos, key=lambda p: p[1])
    return _closest_pair_recursivo(px, py)

def _closest_pair_recursivo(px, py):
    n = len(px)
    if n <= 3:
        # Caso base: força bruta
        min_dist = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                d = dist(px[i], px[j])
                if d < min_dist:
                    min_dist = d
        return min_dist

    # Divisão
    meio = n // 2
    ponto_mediano = px[meio]
    
    px_esq = px[:meio]
    px_dir = px[meio:]
    
    py_esq, py_dir = [], []
    for p in py:
        if p[0] <= ponto_mediano[0]:
            py_esq.append(p)
        else:
            py_dir.append(p)

    # Conquista
    dist_esq = _closest_pair_recursivo(px_esq, py_esq)
    dist_dir = _closest_pair_recursivo(px_dir, py_dir)
    delta = min(dist_esq, dist_dir)

    # Combinação
    faixa = [p for p in py if abs(p[0] - ponto_mediano[0]) < delta]
    
    for i in range(len(faixa)):
        for j in range(i + 1, min(i + 8, len(faixa))):
            d = dist(faixa[i], faixa[j])
            if d < delta:
                delta = d
    
    return delta