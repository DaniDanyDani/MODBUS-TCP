import sys
import time
from pathlib import Path

# Ajusta o path para encontrar as pastas 'servidor' e 'cliente' na raiz do projeto
sys.path.append(str(Path(__file__).resolve().parent.parent))

from servidor.servidor_modbus import ServidorMODBUS
from cliente.cliente_modbus import ClienteMODBUS

# Importando os módulos de teste criados
import teste_hr_float
import teste_hr_bits
import teste_coil
import teste_somente_leitura

def main():
    print("=== INICIANDO SUÍTE DE TESTES MODBUS ===")
    
    # 1. Inicia o Servidor (localhost para compatibilidade com WSL)
    s = ServidorMODBUS('localhost', 19888)
    if not s.iniciar():
        print("[ERRO CRÍTICO] Falha ao iniciar o servidor. A porta pode estar ocupada.")
        return
    print("[OK] Servidor iniciado.")

    # Pausa para garantir a abertura do socket
    time.sleep(0.5)

    # 2. Inicia o Cliente (localhost para forçar IPv4 local)
    c = ClienteMODBUS('localhost', 19888)
    if not c.conectar():
        print("[ERRO CRÍTICO] Cliente não conseguiu conectar ao servidor.")
        s.parar()
        return
    print("[OK] Cliente conectado com sucesso.\n")

    # 3. Execução dos Módulos
    try:
        teste_hr_float.executar(c)
        teste_hr_bits.executar(c)
        teste_coil.executar(c)
        teste_somente_leitura.executar(c)
        
        print("=== TODOS OS TESTES PASSARAM COM SUCESSO ===")

    except Exception as e:
        print(f"\n[FALHA] Ocorreu uma exceção durante os testes: {e}")
        
    finally:
        print("\n--- Encerrando Infraestrutura ---")
        c.desconectar()
        print("[OK] Cliente desconectado.")
        s.parar()
        print("[OK] Servidor desligado.")

if __name__ == '__main__':
    main()