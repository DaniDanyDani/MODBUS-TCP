"""
Módulo Cliente MODBUS TCP.

Este módulo implementa a classe ClienteMODBUS para comunicação com um servidor
(CLP) utilizando o protocolo Modbus TCP através da biblioteca pymodbus.
"""

from pymodbus.client import ModbusTcpClient


class ClienteMODBUS:
    """
    Cliente MODBUS para comunicação via protocolo TCP.

    Gerencia a conexão e executa operações de leitura/escrita nas tabelas 
    de dados do dispositivo escravo (CLP).
    """

    def __init__(self, server_ip: str, porta: int, device_id: int = 1) -> None:
        """
        Inicializa o cliente Modbus TCP.

        Args:
            server_ip (str): Endereço IP do servidor MODBUS.
            porta (int): Porta de comunicação TCP do servidor.
            device_id (int, opcional): ID do dispositivo na rede Modbus. Padrão é 1.
        """
        self._cliente = ModbusTcpClient(host=server_ip, port=porta)
        self.device_id = device_id

    def conectar(self) -> bool:
        """
        Abre a conexão com o servidor MODBUS.

        Returns:
            bool: True se a conexão foi bem sucedida, False caso contrário.
        """
        return self._cliente.connect()

    def desconectar(self) -> None:
        """Fecha a conexão TCP com o servidor."""
        self._cliente.close()

    def ler_dado(self, tipo: int, addr: int):
        """
        Lê um dado da Tabela MODBUS baseado no tipo especificado.

        Tipos suportados:
            1: Holding Register (Função 03)
            2: Coil (Função 01)
            3: Input Register (Função 04)
            4: Discrete Input (Função 02)

        Args:
            tipo (int): Código numérico representando o tipo de dado.
            addr (int): Endereço de memória a ser lido.

        Returns:
            list | int | bool | None: Valor lido. Para Holding Registers, retorna
            uma lista contendo os valores convertidos em float e bits.

        Raises:
            ConnectionError: Se houver falha de comunicação com o servidor.
        """
        match tipo:
            case 1:  # Holding Register
                resp = self._cliente.read_holding_registers(
                    address=addr, count=2, device_id=self.device_id
                )
                if resp.isError():
                    raise ConnectionError(f"Falha ao ler Holding Register no endereço {addr}")

                resp_float = self._cliente.convert_from_registers(
                    resp.registers, self._cliente.DATATYPE.FLOAT32
                )
                resp_bit = self._cliente.convert_from_registers(
                    resp.registers, self._cliente.DATATYPE.BITS
                )
                return [resp_float, resp_bit]

            case 2:  # Coil
                resp = self._cliente.read_coils(
                    address=addr, count=1, device_id=self.device_id
                )
                if resp.isError():
                    raise ConnectionError(f"Falha ao ler Coil no endereço {addr}")
                return resp.bits[0]

            case 3:  # Input Register
                resp = self._cliente.read_input_registers(
                    address=addr, count=1, device_id=self.device_id
                )
                if resp.isError():
                    raise ConnectionError(f"Falha ao ler Input Register no endereço {addr}")
                return resp.registers[0]

            case 4:  # Discrete Input
                resp = self._cliente.read_discrete_inputs(
                    address=addr, count=1, device_id=self.device_id
                )
                if resp.isError():
                    raise ConnectionError(f"Falha ao ler Discrete Input no endereço {addr}")
                return resp.bits[0]

            case _:
                return None

    def escrever_dado_float(self, tipo: int, addr: int, valor: float) -> bool:
        """
        Escreve um dado do tipo Float32 na Tabela MODBUS.

        Args:
            tipo (int): Código numérico (1 para Holding Register).
            addr (int): Endereço de memória a ser escrito.
            valor (float): Valor de ponto flutuante a ser escrito.

        Returns:
            bool: True em caso de sucesso, False em caso de falha ou tipo inválido.
        """
        if tipo == 1:  # Holding Register
            registers = self._cliente.convert_to_registers(
                valor, self._cliente.DATATYPE.FLOAT32
            )
            resp = self._cliente.write_registers(
                address=addr, values=registers, device_id=self.device_id
            )
            return not resp.isError()

        return False
    
    def escrever_dado_bits(self, tipo: int, addr: int, bit_pos: int) -> bool:
        """
        Inverte o estado lógico de um bit em um Holding Register ou escreve em um Coil.

        Args:
            tipo (int): Código numérico (1 para Holding Register, 2 para Coil).
            addr (int): Endereço de memória.
            bit_pos (int): Posição do bit no Holding Register (0-15) ou o valor no Coil.

        Returns:
            bool: True em caso de sucesso, False em caso de falha ou tipo inválido.
        """
        match tipo:
            case 1:  # Holding Register
                # Lê o estado atual dos bits
                resp_leitura = self._cliente.read_holding_registers(
                    address=addr, count=2, device_id=self.device_id
                )
                if resp_leitura.isError():
                    return False
                
                bits = self._cliente.convert_from_registers(
                    resp_leitura.registers, self._cliente.DATATYPE.BITS
                )
                
                # Inversão do bit selecionado
                bits[bit_pos] = not bits[bit_pos]
                
                # Converte de volta e escreve
                registers = self._cliente.convert_to_registers(
                    bits, self._cliente.DATATYPE.BITS
                )
                resp_escrita = self._cliente.write_registers(
                    address=addr, values=registers, device_id=self.device_id
                )
                return not resp_escrita.isError()

            case 2:  # Coil
                resp = self._cliente.write_coil(
                    address=addr, value=bool(bit_pos), device_id=self.device_id
                )
                return not resp.isError()

            case _:
                return False