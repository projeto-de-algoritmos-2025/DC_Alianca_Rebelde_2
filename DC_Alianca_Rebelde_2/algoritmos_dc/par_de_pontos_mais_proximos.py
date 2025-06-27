# algoritmos_dc/par_de_pontos_mais_proximos.py
import math

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def encontrar_par_mais_proximo(pontos):
    if len(pontos) < 2: return float('inf'), (None, None)
    px = sorted(pontos, key=lambda p: p[0])
    py = sorted(pontos, key=lambda p: p[1])
    return _encontrar_par_recursivo(px, py)

def _encontrar_par_recursivo(px, py):
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

    mid = n // 2
    ponto_mediano = px[mid]
    
    px_esq = px[:mid]; px_dir = px[mid:]
    py_esq, py_dir = [], []
    for p in py:
        if p[0] < ponto_mediano[0] or (p[0] == ponto_mediano[0] and p in px_esq): py_esq.append(p)
        else: py_dir.append(p)

    (dist_esq, par_esq) = _encontrar_par_recursivo(px_esq, py_esq)
    (dist_dir, par_dir) = _encontrar_par_recursivo(px_dir, py_dir)
    delta, par_min = (dist_esq, par_esq) if dist_esq <= dist_dir else (dist_dir, par_dir)

    faixa_y = [p for p in py if abs(p[0] - ponto_mediano[0]) < delta]
    for i in range(len(faixa_y)):
        for j in range(i + 1, min(i + 8, len(faixa_y))):
            d = dist(faixa_y[i], faixa_y[j])
            if d < delta:
                delta = d; par_min = (faixa_y[i], faixa_y[j])
    return delta, par_min