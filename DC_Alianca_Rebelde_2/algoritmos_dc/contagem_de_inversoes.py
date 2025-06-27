def contar_inversoes(arr):
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        meio = len(arr) // 2
        esquerda, inv_esq = merge_sort(arr[:meio])
        direita, inv_dir = merge_sort(arr[meio:])
        intercalado, inv_merge = merge(esquerda, direita)
        return intercalado, inv_esq + inv_dir + inv_merge

    def merge(esq, dir):
        resultado = []
        i = j = inv = 0
        while i < len(esq) and j < len(dir):
            if esq[i] <= dir[j]:
                resultado.append(esq[i])
                i += 1
            else:
                resultado.append(dir[j])
                inv += len(esq) - i  # Todas as restantes da esquerda causam inversão
                j += 1
        resultado.extend(esq[i:])
        resultado.extend(dir[j:])
        return resultado, inv

    _, total = merge_sort(arr)
    return total
