def executar(cliente):
    print("--- Testando Escrita e Leitura COIL ---")
    addr_coil = 2000
    
    # 1 representa True/High em sistemas Modbus
    sucesso = cliente.escrever_dado_bits(2, addr_coil, 1) 
    if not sucesso:
        raise RuntimeError(f"Falha ao escrever no Coil {addr_coil}")
        
    res_coil = cliente.ler_dado(2, addr_coil)
    print(f"Esperado: True | Lido: {res_coil}\n")