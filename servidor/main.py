import sys
import time
import random
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from servidor_modbus import ServidorMODBUS

# =================================================
# Inicialização do servidor para simulação no terminal
# =================================================
s = ServidorMODBUS('localhost', 19888)
if s.iniciar():    
    try:
        while True:
            # Simula a variação do processo
            novo_valor = random.randrange(int(0.95 * 400), int(1.05 * 400))
            s.escrever_holding_registers(1000, [novo_valor])
            
            print('======================')
            print("Tabela MODBUS")
            print(f"Holding Register \r\n R1000: {s.ler_holding_registers(1000)} \r\n R2000: {s.ler_holding_registers(2000)}")
            print(f"Coil \r\n R1000: {s.ler_coils(1000)}")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nEncerrando o servidor (Ctrl+C)...")
        s.parar()
else:
    print("Falha ao iniciar o servidor. A porta 19888 pode estar ocupada.")