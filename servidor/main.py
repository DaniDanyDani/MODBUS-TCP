from servidor_modbus import ServidorMODBUS


s = ServidorMODBUS('localhost',19888)
s.run()