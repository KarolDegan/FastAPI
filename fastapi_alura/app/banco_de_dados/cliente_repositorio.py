from banco_de_dados.local import BancoDeDadosLocal
from modelos.cliente import Cliente, ClienteCriarAtualizar


class ClienteRepositorio:
    def __init__(self, banco_de_dados: BancoDeDadosLocal):
        self.bd = banco_de_dados

    async def listar_clientes(self) -> list[Cliente]:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            linhas = cursor.fetchall() # caso tenha id repetidos
            clientes = [
                Cliente(id_=linha[0], nome=linha[1], email=linha[2], telefone=linha[3]) # montando o objeto
                for linha in linhas
            ]
            return clientes
        
    async def obter_cliente(self, cliente_id: int) -> Cliente | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (cliente_id,)
            )
            linha = cursor.fetchone() 
            if linha:
                return Cliente(id_=linha[0], nome=linha[1], email=linha[2], telefone=linha[3])
            return None
        
    async def criar_cliente(self, cliente: ClienteCriarAtualizar) -> Cliente:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?,?,?)",
                (cliente.nome, cliente.email, cliente.telefone)
            )
            cliente_id = cursor.lastrowid # ler ultima linha criada no banco
            return Cliente(id_=cliente_id, nome=cliente.nome, email=cliente.email, telefone=cliente.telefone)
        
    async def atualizar_cliente(self, cliente_id: int, cliente: ClienteCriarAtualizar) -> Cliente | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                (cliente.nome, cliente.email, cliente.telefone, cliente_id)
            )
            if cursor.rowcount == 0:
                return None # se não encontrou o cliente para atualizar, retorna None
            return Cliente(id_=cliente_id, nome=cliente.nome, email=cliente.email, telefone=cliente.telefone)

    async def deletar_cliente(self, cliente_id: int) -> bool:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM clientes WHERE id = ?", (cliente_id,)
            )
            return cursor.rowcount > 0
