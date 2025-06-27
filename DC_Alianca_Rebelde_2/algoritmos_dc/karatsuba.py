# algoritmos_dc/karatsuba.py

def karatsuba(x_str, y_str):
    # Converte para string para garantir o tipo e poder dividir
    x_str, y_str = str(x_str), str(y_str)
    
    # Caso base da recursão
    if len(x_str) == 1 or len(y_str) == 1:
        # Converte para int na base correta (2 para binário, 10 para decimal)
        base = 2 if all(c in '01' for c in x_str+y_str) else 10
        return int(x_str, base) * int(y_str, base)

    # Garante que os números tenham o mesmo comprimento par
    n = max(len(x_str), len(y_str))
    if n % 2 != 0:
        n += 1
    
    n2 = n // 2
    
    x_str = x_str.zfill(n)
    y_str = y_str.zfill(n)

    # Divide as strings
    a_str = x_str[:-n2]
    b_str = x_str[-n2:]
    c_str = y_str[:-n2]
    d_str = y_str[-n2:]
    
    # 3 chamadas recursivas, passando as strings
    ac = karatsuba(a_str, c_str)
    bd = karatsuba(b_str, d_str)
    
    # Para o passo do meio, precisamos somar os números, não concatenar as strings
    base = 2 if all(c in '01' for c in x_str+y_str) else 10
    a, b = int(a_str, base), int(b_str, base)
    c, d = int(c_str, base), int(d_str, base)
    soma_prod = karatsuba(str(a + b), str(c + d))

    ad_plus_bc = soma_prod - ac - bd
    
    # Combina os resultados usando deslocamento de bits (shifting), que é o equivalente binário de multiplicar por potências de 10
    resultado_final = (ac << (2 * n2)) + (ad_plus_bc << n2) + bd
    
    return resultado_final