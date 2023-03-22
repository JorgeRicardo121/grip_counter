import cv2
import pandas as pd

# Carrega a imagem da parede de escalada
img = cv2.imread('./img/parede.jpg')

# Converte a imagem para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplica uma limiarização na imagem para obter a máscara das agarras
_, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Encontra os contornos na imagem
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define o número de agarras que você deseja selecionar
num_agarras = 2

# Define uma lista para armazenar as coordenadas das agarras selecionadas
coords = []

# Define a variável para armazenar as coordenadas do ponto inicial do retângulo
rect_start = None

# Define a função de callback do mouse para capturar cliques na imagem
def mouse_callback(event, x, y, flags, param):
    # Usa a variável global rect_start para armazenar as coordenadas do ponto inicial do retângulo
    global rect_start
    # Se o botão esquerdo do mouse for pressionado, armazena as coordenadas do ponto inicial do retângulo
    if event == cv2.EVENT_LBUTTONDOWN:
        rect_start = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if rect_start is not None:
            # Desenha um retângulo em tempo real com o mouse enquanto o usuário está selecionando a agarra
            img_copy = img.copy()
            cv2.rectangle(img_copy, rect_start, (x, y), (0, 0, 255), 2)
            cv2.imshow('Selecione as agarras', img_copy)


    # Se o botão esquerdo do mouse for solto, calcula as coordenadas do retângulo e adiciona à lista de agarras
    elif event == cv2.EVENT_LBUTTONUP:
        rect_end = (x, y)
        # Calcula as coordenadas do retângulo a partir dos pontos inicial e final selecionados pelo usuário
        x1, y1 = min(rect_start[0], rect_end[0]), min(rect_start[1], rect_end[1])
        x2, y2 = max(rect_start[0], rect_end[0]), max(rect_start[1], rect_end[1])
        coords.append((x1, y1, x2, y2))
        # Desenha um retângulo em volta da última agarra selecionada
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # Atualiza a janela de exibição da imagem
        cv2.imshow('Selecione as agarras', img)

# Cria a janela de exibição da imagem e define a função de callback do mouse
cv2.namedWindow('Selecione as agarras')
cv2.setMouseCallback('Selecione as agarras', mouse_callback)



# Loop principal para selecionar as agarras
while len(coords) < num_agarras:
    cv2.imshow('Selecione as agarras', img)
    cv2.waitKey(1)
    
for i, contour in enumerate(contours):
    # Extrai a região correspondente ao contorno atual
    x, y, w, h = cv2.boundingRect(contour)
    roi = img[y:y+h, x:x+w]
    
    # Salva a região como um novo arquivo PNG
    cv2.imwrite(f"agarras/agarra_{i}.png", roi)

# Exibe a imagem com os retângulos em volta das agarras selecionadas
for i, (x1, y1, x2, y2) in enumerate(coords):
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.putText(img, f'Agarra {i+1}', (x2+10, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

cv2.imshow('Agarras selecionadas', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # Cria um DataFrame com as coordenadas das agarras
df = pd.DataFrame(coords, columns=['x', 'y', 'w', 'h'])

# # Salva o DataFrame em um arquivo CSV
df.to_csv('coordenadas_agarras.csv', index=False)

# Salva a imagem com as agarras contornadas em um arquivo PNG
cv2.imwrite('agarras_contornadas.png', img)
