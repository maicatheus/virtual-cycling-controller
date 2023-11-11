# Controlador de Ciclismo Virtual

![Giff pedalando](https://i.ibb.co/VtVKYsc/Whats-App-Video-2023-11-11-at-16-48-24-1.gif)

Este é um programa em Python que utiliza visão computacional e entrada de gamepad virtual para criar um controlador de ciclismo virtual. Ele permite que você controle um jogo (GTA V, no meu caso.. Mas se aplica a outros games) pedalando e virando na frente de uma câmera. O programa utiliza as seguintes tecnologias:

- OpenCV para capturar frames da câmera e processamento de imagem.
- Mediapipe para estimativa de pose, o que ajuda a detectar os pontos de referência do corpo do usuário.
- vgamepad para simular uma entrada de gamepad virtual.
- Cálculos matemáticos para determinar a velocidade de pedalada, o ângulo de direção e muito mais.

## Como Funciona

O programa funciona da seguinte forma:

1. Ele captura frames da câmera padrão (geralmente a webcam).
2. Utiliza o Mediapipe para estimar a pose do corpo do usuário, incluindo pontos de referência-chave, como mãos, ombros e articulações do corpo.
3. Calcula a distância entre pontos de referência específicos do corpo (por exemplo, pés e quadril) para determinar quando uma pedalada foi efetuada e calcular as rotações por minuto (RPM).
4. Calcula o ângulo entre a cabeça do usuário e o centro da cintura para controlar a direção.
5. Com base no RPM calculado e no ângulo de direção, ele simula a entrada do gamepad para controlar um jogo de ciclismo virtual.

## Dependências

Antes de executar o código, você precisará instalar as seguintes bibliotecas Python:

- OpenCV (`cv2`)
- Mediapipe (`mediapipe`)
- vgamepad (`vgamepad`)

Você pode instalar essas dependências usando o `pip`:

```bash
pip install opencv-python mediapipe vgamepad
