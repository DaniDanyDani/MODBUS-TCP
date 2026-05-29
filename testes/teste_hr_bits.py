def executar(cliente):
    print("--- Testando Manipulação de BITS (Holding Register) ---")
    addr_hr = 1500
    bit_alvo = 5
    
    # Lê o estado atual
    res_hr_antes = cliente.ler_dado(1, addr_hr)
    estado_antes = res_hr_antes[1][bit_alvo]
    print(f"Estado do bit {bit_alvo} antes: {estado_antes}")
    
    # Inverte o bit
    sucesso = cliente.escrever_dado_bits(1, addr_hr, bit_alvo)
    if not sucesso:
        raise RuntimeError(f"Falha ao inverter bit {bit_alvo} no endereço {addr_hr}")
        
    # Lê novamente para confirmar
    res_hr_depois = cliente.ler_dado(1, addr_hr)
    estado_depois = res_hr_depois[1][bit_alvo]
    print(f"Estado do bit {bit_alvo} depois: {estado_depois}\n")