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

# Organizando o meu código com SOLID em duas semanas
## Usando princípios do livro Arquitetura Limpa do Uncle Bob

---

### Organizando o meu código com SOLID em duas semanas

### Primeira semana

##### Teclado, UI e persistência

No início identifiquei apenas os códigos de entrada e saída mais convencionais e removi o uso dos seus construtores de dentro do fluxo principal para usá-los apenas na classe main do projeto. Como eu tinha um worker (chamado de daemon na época), que era iniciado separadamente, eu tinha duas mains.

```python
DaemonController(PhysicalKeyboard(), FileGamePersistenceAdapter()).read_action()
```
```python
ChessDaemon(FileGamePersistenceAdapter(), TextViewerAdapter()).main_loop()
```

Nessa versão eu já tinha uma segunda implementação de Keyboard chama inMemoryKeyboard que eu usava para testes.

---

### Organizando o meu código com SOLID em duas semanas

### Primeira semana

##### Todas as classes

No segundo dia eu decidi tirar não só os construtores IO do código como todos os construtores, tudo deveria esta na main. Além disso decidi juntar o código da criação do worker com o código da UI no mesmo arquivo, para executar um arquivo só e ter apenas um lugar de injeção.

```python
movement_machine = MovementStateMachine() 
dealer_machine = DealerStateMachine()

file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapater = TextViewerAdapter()

opponent_listener = OpponentListener(
    movement_machine=movement_machine
)

moderator = Moderator(
    game_persistence_adapter=file_persistence
)
dealer = Dealer(
    game_persistence_adapter=file_persistence
)

...

```

As duas classes de machine implementavam register e main_loop, que eu usava para injetar as classes de comportamento, que eram handlers, para os estados das máquinas. Então Moderator e Dealer que vemos no código anterior implementavam a interface Handler que eu havia criado.

---

### Organizando o meu código com SOLID em duas semanas

### Primeira semana

##### Simplificando a main

O código evoluiu e ficou mais limpo na main. Eu levei o código de criação do worker para dentro de DealerDispatcher e o worker se tornou algo que era reiniciado toda vez que um jogo diferente era aberto pela UI. Também retirei o método register para que o mapa de handlers e estados fosse montado na main e usado no construtor da máquina.

```python
file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapter = TextViewerAdapter(
    persistence=file_persistence,
    user=user
)
message_crossing_factory = FileMessageCrossingFactory()
movements = queue.Queue()
                   
dealer_machine = DealerStateMachine({
    DealerState.READING: CommandReader(keyboard=physical_keyboard),
    DealerState.FILTERING: CommandRouter(movements=movements, user=user, game_viewer=viewer_adapter, persistence=file_persistence),
    DealerState.EXECUTING: DealerDispatcher(message_crossing_factory=message_crossing_factory, game_viewer=viewer_adapter, keyboard=physical_keyboard)
})

dealer_machine.main_loop()
```
---

# Segunda semana
## Fechando o projeto com TDD

---

### Segunda semana

### Fechando o projeto com TDD

##### Escrevendo testes com DI

``` python
@pytest.fixture
def dealer_machine():
    user="jose"
    memory_persistence = MemoryGamePersistenceAdapter()
    memory_keyboard = InMemoryKeyboard()
    viewer_adapter = NoViewerAdapter()
    message_crossing_factory = FileMessageCrossingFactory(user)
    movements = queue.Queue()
                    
    return DealerStateMachine({
        DealerState.READING: CommandReader(keyboard=memory_keyboard),
        DealerState.FILTERING: CommandRouter(movements=movements, user=user, game_viewer=viewer_adapter, persistence=memory_persistence),
        DealerState.EXECUTING: DealerDispatcher(
          movements=movements, 
          user=user, 
          message_crossing_factory=message_crossing_factory, 
          game_viewer=viewer_adapter, 
          keyboard=memory_keyboard, 
          persistence=memory_persistence)
    }, mode=DealerMachineMode.WHILE_THERE_ARE_MESSAGES_ON_KEYBOARD)
```

Com esse setup escrevi testes muito completos que me permitiram encontrar bugs que não teria tido paciência e método para procurar manualmente. Os dias seguintes foram intensos de conserto de bugs.

---

### Segunda semana

### Fechando o projeto com TDD

##### Testando grande cenários

```python
def test_pastor_check(dealer_machine):
    dispatcher : DealerDispatcher = dealer_machine.handler_map[DealerState.EXECUTING]
    dispatcher.register_opponent_moves(["a7a6", "a6a5", "h7h6", "a8a7"]) # This will actually user the file message crossing under the hood
    keyboard: InMemoryKeyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    keyboard.append_output("sg")
    keyboard.append_output("gisele")
    keyboard.append_output("cg")
    keyboard.append_output("1")
    keyboard.append_output("play move e2e4")
    keyboard.append_output("play move f1c4")
    keyboard.append_output("play move d1f3")
    keyboard.append_output("play move f3f7")
    dealer_machine.main_loop()
    dealer_machine.wait_test_game_end()
    persistence : MemoryGamePersistenceAdapter = dealer_machine.handler_map[DealerState.EXECUTING].persistence
    game = persistence.get_board(1)
    assert game != None
    assert game.winner == "jose"
```

Teste que cria jogo e faz o cheque mate do pastor.

---

### Segunda semana

### Fechando o projeto com TDD

##### Fechando o projeto

Os últimos testes, de roque e promoção de peão foram esverdeados e um último teste de sistema automatizado implementado, o de uma partida longa e histórica do Norway Chess 2025 com mais de 120 movimentos.

Uma ultima suíte de testes unitários também foi implementada.

```python
def test_minor_roque(board: Board):
    board.move("e1g1")
    assert board.legal

def test_major_roque(board: Board):
    board.move("e1c1")
    assert board.legal

def test_blocked_by_knight_major_roque(blocked_by_kngiht: Board):
    blocked_by_kngiht.move("e1c1")
    assert not blocked_by_kngiht.legal

def test_blocked_by_bishop_minor_roque(blocked_by_bishop: Board):
    blocked_by_bishop.move("e1g1")
    assert not blocked_by_bishop.legal

def test_blocked_by_queen_major_roque(blocked_by_queen: Board):
    blocked_by_queen.move("e1c1")
    assert not blocked_by_queen.legal

def test_absent_rook_roque(absent_rook: Board):
    absent_rook.move("e1c1")
    assert not absent_rook.legal
```