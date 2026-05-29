"""
Módulo Servidor MODBUS TCP.
"""
from pyModbusTCP.server import DataBank, ModbusServer

class ServidorMODBUS:
    """
    Classe Servidor Modbus encapsulada para não travar a interface gráfica (Kivy).
    """
    
    def __init__(self, host_ip: str, port: int) -> None:
        """Construtor"""
        self._db = DataBank()
        self._server = ModbusServer(
            host=host_ip, port=port, no_block=True, data_bank=self._db
        )

    def iniciar(self) -> bool:
        """
        Inicia a execução do servidor Modbus em background.
        
        Returns:
            bool: True se o servidor iniciou com sucesso, False se a porta estiver ocupada.
        """
        self._server.start()
        return self._server.is_run

    def parar(self) -> None:
        """Para a execução do servidor Modbus."""
        self._server.stop()

    def ler_holding_registers(self, addr: int, count: int = 1) -> list[int] | None:
        """Lê valores dos Holding Registers."""
        return self._db.get_holding_registers(addr, count)

    def escrever_holding_registers(self, addr: int, valores: list[int]) -> bool:
        """Escreve valores nos Holding Registers."""
        # A biblioteca retorna True ou None. O bool() converte None para False,
        # cumprindo a exigência do Type Hint de retornar estritamente um booleano.
        return bool(self._db.set_holding_registers(addr, valores))

    def ler_coils(self, addr: int, count: int = 1) -> list[bool] | None:
        """Lê o estado dos Coils."""
        return self._db.get_coils(addr, count)

    def escrever_coils(self, addr: int, valores: list[bool]) -> bool:
        """Escreve valores nos Coils."""
        # Conversão de Literal[True] | None para bool
        return bool(self._db.set_coils(addr, valores))