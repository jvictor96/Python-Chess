---
marp: true
paginate: true

style: |
  section {
    background-color: #191C20;
    color: #dfedff;
  }
  section h1 {
    color: #9ECAFF;
  }
  section h3 {
    color: #9ECAFF;
    font-size: 28px;
  }
  section h5 {
    color: #dfedff;
    font-size: 25px;
  }
  section pre {
    font-size: 11px;
  }
  section p {
    font-size: 20px;
  }
  section li {
    font-size: 20px;
  }
---

# Programando o core do xadrez em 2 dias
## Usando princípios do livro Refatoração do Martin Fowler

---

### Programando o core do xadrez em 2 dias

### Primeiro dia - TDD e CI

##### Testes

No primeiro dia não consegui nenhum resultado sólido. A validação de jogadas só começou a ficar pronta no dia seguinte, mas eu estava focado em conseguir usar extreme programming e CI nesse projeto, então foquei em escrever testes. Ao fim do primeiro dia, além de 8 testes para bispo, havia 7 para cavalo, 8 para peão e 8 para torre.

Ex:

``` python
def test_valid_horizontal_rook_move():
    board = Board.move(1, "d4c4")
    assert board.legal == True
    assert isinstance(board.positions.get("c4", None), Rook)

def test_invalid_rook_move():
    board = Board.move(1, "d4c3")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)
```

---

### Programando o core do xadrez em 2 dias

### Primeiro dia - TDD e CI

##### Testes

A suíte de testes do bispo valida as regras implementadas usando um tabuleiro persistido em json em que o bispo começa na casa e4 e as outras peças nas casas normais de início.

``` python
def test_valid_forward_left_biship_move():
    board = Board.move(1, "e4d5")
    assert board.legal == True
    assert isinstance(board.positions.get("d5", None), Bishop)

def test_invalid_bishop_move():
    board = Board.move(1, "e4e5")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), Bishop)

def test_blocked_bishop_move():
    board = Board.move(1, "e4c2")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), Bishop)

def test_bishop_cant_jump_over_ally():
    board = Board.move(1, "e4h1")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), Bishop)
```


Escrever esses testes ajudou a decidir o contrato responsável por amarrar toda a lógica de validação de movimento espalhada por todas as classes. Ter um jeito tão fácil de usar o código do domínio foi excelente para o projeto, mesmo com nenhum desses testes passando no primeiro dia.

---

### Programando o core do xadrez em 2 dias

### Primeiro dia - TDD e CI

##### Contrato


``` python
def move(game_id: str, movement: str):
        board = Board.get_board(game_id)
        movement = Movement.from_string(movement, board.positions)
        board.legal = movement.is_valid()
        if board.legal:
            piece = board.positions.get(movement.start_pos)
            board.movements.append(movement)
            board.positions.pop(movement.start_pos)
            board.positions[movement.end_pos] = piece
            board.pieces = [piece for pos, piece in board.positions.items()]
        return board
```

Numa iteração posterior, o método move deixou de ser estático e carregar o tabuleiro para ser aplicado na própria instância de tabuleiro. No primeiro dia ainda não havia nenhuma dependência, injeção, ou lugar para que que isso pudesse acontecer, então a persistência estava um pouco misturada com o domínio.

---

### Programando o core do xadrez em 2 dias

### Primeiro dia - TDD e CI

##### Polimorfismo

A classe de peças no primeiro dia não servia para muito além de marcar que determinada instância era de determinada implementação de peça e que parte da validação do movimento, específica da peça deveria ficar na própria implementação, evitando condicionais longas para validar o movimento para cada tipo de peça.

``` python
class Piece(ABC):
    color: Color
    position: Position

    def __init__(self, color, position):
        self.color = color
        self.position = position

    @abstractmethod
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass
```

Aqui ocultei a implementação de cavalo, bispo rainha, rei e peão, já que todas elas são iguais.

---

### Programando o core do xadrez em 2 dias

### Primeiro dia - TDD e CI

##### Lógica de domínio

Esse é o esqueleto da validação de movimentos. Esses métodos não estavam implementados, mas eu estava tentando dar nomes bons.

``` python
    def is_valid(self):
        return all([
            self.is_the_path_clear(),
            self.is_the_destination_different_from_origin_and_in_the_board(),
            self.is_destinarion_free(),
            self.is_the_player_turn(),
            self.king_wont_be_in_check()])
```

##### Resultado dos testes do primeiro dia

36 failed, 1 passed in 0.18s
O teste verde era

``` python
def test_load():
    board = Board.get_board(0)
    assert board.positions[Position(1, 1)].__class__ != Rook.__class__
```

---

### Conclusão do primero dia

Li recentemente que o código tem dois valores, o do seu comportamento e o da sua manutenção. Como caixa preta, ele tem valor por fazer o que se propõe, nesse caso é acusar que um movimento inválido é inválido e não acusar movimentos válidos, essa é um dos lados que lhe da valor e isso eu ainda não tinha no primeiro dia. Por outro lado, **com bons nomes, fluxo simples, boa separação de responsabilidades e muitos testes bem nomeados, acredito que o código já tinha clareza, que também acrescenta valor**.

O livro Código Limpo, que estou lendo enquanto termino esse projeto, começa com citações de vários autores sobre o que é um código limpo. Alguns exemplos são:
- Um código limpo é simples e direto. Ele é tão bem legível quanto uma prosa vem escrita. 
- Além de seu criador, um desenvolvedor pode ler e melhorar um código limpo
- Expressa todas as ideias do projeto que estão no sistema

---

# Segundo dia

## Criando mais testes e fazendo-os ficarem verdes

---

### Segundo dia

### Criando mais testes e fazendo-os ficarem verdes

##### Testes

Nos primeiros 2 commits do dia implementei mais 22 testes.

No quinto commit do dia fui de 38 testes falhando e 21 passando para 18 testes falhando e 41 passando, com a implementação do método is_movement_valid do bispo, torre, cavalo e peão, que não chegavam a validar se havia peças no caminho.

A maior parte do que fiz foi trabalhar nisso até que eu tivesse 56 verdes e 7 vermelhos. Eu sabia que se eu tivesse um código capaz de rodar um método comprovadamente consistente de move, dado um tabuleiro de xadrez e um movimento, eu teria o que eu estava buscando.

---

### Segundo dia

### Criando mais testes e fazendo-os ficarem verdes

##### Testes

Nesse dia coloquei fixtures nos meus testes

```python
@pytest.fixture
def board():
        board = BoardIO.get_board(0)
        board = board.bypass_validation_move("h1d4")  
        board = board.bypass_validation_move("c1e4")  
        return board
```

O tabuleiro 0 é o tabuleiro antes de xadrez arrumado, gravado em como json em um arquivo. Hoje o construtor de Board cria o tabuleiro novo caso não seja passado nenhuma peça no construtor, o tabuleiro arrumado está codificado em python no construtor, já que é uma regra de negócio e não tem relação com a persistência.

O método bypass_validation_move foi criado só para ser usado nos testes. Escrever código útil para ajudar em testes foi algo que me ajudou muito durante o projeto.

As minhas leituras recentes sobre XP, CI e Agile me convenceram que essa é uma boa bússola e que é possível tornar o código cada vez mais limpo com pequenas modificações em direção a limpeza se houverem testes que sempre comprovem o funcionamento do programa.

---

### Segundo dia

### Criando mais testes e fazendo-os ficarem verdes

##### Código

Adicionei o método get_middle_places na abstração das peças para poder validar o caminho que estavam fazendo.

``` python
class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        verifications = [
            destination[0].x == self.position.x,
            destination[0].y == self.position.y,
        ]
        return any(verifications)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        min_x = min(destination[0].x, self.position.x)
        max_x = max(destination[0].x, self.position.x)
        min_y = min(destination[0].y, self.position.y)
        max_y = max(destination[0].y, self.position.y)
        possibilities = {
            destination[0].x == self.position.x: lambda: [Position(self.position.x, i) for i in range(min_y + 1, max_y)],
            destination[0].y == self.position.y: lambda: [Position(i, self.position.y) for i in range(min_x + 1, max_x)]
        }
        return possibilities[True]()
```

Gosto de programar declarativamente. Possibilities é um dicionário com apenas uma chave true que diz se o movimento foi horizontal ou vertical, cujo valor retorna as casas viajadas.

---

### Segundo dia

### Criando mais testes e fazendo-os ficarem verdes

##### Código

Na camada superior eu tinha.

``` python
    def is_valid(self):
        if self.get_piece_in_the_origin() is None:
            return False
        return all([
            self.is_the_path_clear(),
            self.is_the_destination_different_from_origin_and_in_the_board(),
            self.is_destinarion_free(),
            self.is_the_player_turn(),
            self.king_wont_be_in_check()])

    def get_piece_in_the_origin(self):
        return self.positions.get(self.start_pos, None)

    def is_the_path_clear(self):
        piece = self.get_piece_in_the_origin()
        if piece is None:
            return False
        if piece.is_movement_valid((self.end_pos, self.positions.get(self.end_pos))) is False:
            return False
        if any([place in self.positions.keys() for place in piece.get_middle_places((self.end_pos, self.positions.get(self.end_pos)))]):
            return False
        return True

    def is_the_destination_different_from_origin_and_in_the_board(self):
        return self.start_pos != self.end_pos

    def is_destinarion_free(self):
        return self.positions.get(self.end_pos, None) is None or self.positions.get(self.end_pos, None).color != self.get_piece_in_the_origin().color
```

---

# Segundo dia

## Organização

---

### Segundo dia

### Organização

##### Composition root

No segundo dia criei um composition root. 

```python
from daemon import ChessDaemon

ChessDaemon().main_loop()
```

O fluxo de ChessDaemon estava baseado em ler um arquivo com o input do comando e printar o tabuleiro em outro arquivo. O programa já funcionava e testei esse fluxo na prática. Nesse dia consegui escrever essa classe Daemon, responsável por controlar o fluxo dentro do loop, assim ficou mais evidente quando a persistência deveria ser usada e a parte da persistência nasceu como componente isolado do domínio. Porém eu ainda não estava usando ports, adapters e injeção. Escrever tudo isso em dois dias já havia me dado muito trabalho.

---

### Segundo dia

### Organização

##### Conclusão do segundo dia

A ideia que eu tinha era integrar vários módulos que rodassem de forma independente e manipulassem os arquivos de input e output. No terceiro dia escrevi um shell simples para manipular o arquivo de input e um script para capturar o output. O sistema acabou evoluindo para o DealerDaemon se tornar um máquina de estados rodando em uma máquina de estados em uma thread separa, o que é um destino um pouco óbvio olhando agora, e no lugar de executar vários códigos em threads separadas usando sessões de bash diferentes, que era o que eu imaginava para desacoplamento, foi melhor rodar várias threads no mesmo processo e ter um composition root rico para orquestrar tudo isso.
