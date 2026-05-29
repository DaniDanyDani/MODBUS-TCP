def executar(cliente):
    print("--- Testando Escrita e Leitura FLOAT (Holding Register) ---")
    valor_float_teste = 256.75
    addr_hr = 1500
    
    sucesso = cliente.escrever_dado_float(1, addr_hr, valor_float_teste)
    if not sucesso:
        raise RuntimeError(f"Falha ao escrever float {valor_float_teste} no endereço {addr_hr}")
        
    res_hr = cliente.ler_dado(1, addr_hr)
    print(f"Esperado: {valor_float_teste} | Lido: {res_hr[0]}")
    print(f"Memória RAW (Bits): {res_hr[1]}\n")