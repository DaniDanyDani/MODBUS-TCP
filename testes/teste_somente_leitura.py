def executar(cliente):
    print("--- Testando Funções de Somente Leitura ---")
    
    res_ir = cliente.ler_dado(3, 3000)
    if res_ir is None:
         raise RuntimeError("Falha ao ler Input Register.")
         
    res_di = cliente.ler_dado(4, 4000)
    if res_di is None:
         raise RuntimeError("Falha ao ler Discrete Input.")
         
    print(f"Input Register (Addr 3000): {res_ir} (Padrão de fábrica é 0)")
    print(f"Discrete Input (Addr 4000): {res_di} (Padrão de fábrica é False)\n")