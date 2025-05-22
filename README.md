# PongBall

Jogo clássico Pong em Python usando Pygame, OpenCV e NumPy.

## Funcionalidades

- Bola com detecção de contorno (Canny) via OpenCV.
- Efeito de “glow” por alguns frames ao rebater.
- Sons: batida na raquete, ponto marcado e vitória.
- Tela inicial, pausa (tecla P) e placar até 10 pontos.
- Animações de fade-in/fade-out.

## Requisitos

- Python 3.8+
- Pygame (~=2.6.1)
- OpenCV (`opencv-python`)
- NumPy

## Instalação

1. Clone este repositório  
   ```bash
   git clone https://github.com/admjorgeluiz/PongBall.git
   cd PongBall
   ```
2. Crie um virtualenv e ative-o (opcional)  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac  
   venv\Scripts\activate     # Windows
   ```
3. Instale dependências  
   ```bash
   pip install -r requirements.txt
   ```

## Como Jogar

Execute o jogo:
```bash
python main.py
```

- **Iniciar**: Pressione **ESPAÇO** na tela inicial.  
- **Movimentar**:  
  - Jogador A: **W** (subir) / **S** (descer)  
  - Jogador B: **↑** (subir) / **↓** (descer)  
- **Pausa**: Tecla **P**  
- **Vencer**: Primeiro a 10 pontos.  

## Estrutura de Arquivos

- `main.py` – fluxo principal, tratamento de eventos, placar e telas.  
- `ball.py` – classe Ball: movimento, contorno OpenCV, brilho e colisões.  
- `paddle.py` – classe Paddle: desenho e movimento das raquetes.  
- `requirements.txt` – dependências do projeto.  
- Arquivos de som (`.mp3`) na raiz.

## Contribuição

1. Faça um fork.  
2. Crie uma branch (`git checkout -b feature/minha-feature`).  
3. Commit suas mudanças (`git commit -m 'Minha feature'`).  
4. Push para sua branch (`git push origin feature/minha-feature`).  
5. Abra um Pull Request.

## Licença

Projeto aberto sob licença MIT. Veja o arquivo `LICENSE` para detalhes.
