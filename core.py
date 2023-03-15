import cv2
import numpy as np

# Carrega a imagem da parede de escalada
img = cv2.imread(".\img\parede.jpg")

# Converte a imagem para tons de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplica um filtro Gaussiano para suavizar a imagem
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Detecta as bordas na imagem usando o operador de Sobel
sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
edges = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)


edges = cv2.Canny(gray, 50, 200)
edges = np.uint8(edges)

lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

# Desenha as linhas detectadas na imagem original
for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Encontra os contornos dos agarras na imagem
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Desenha os contornos dos agarras na imagem original
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


# Exibe a imagem final
cv2.imshow("Resultado", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # Cria uma matriz para armazenar as posições dos agarras
# agarras = []

# # Abre o arquivo de vídeo
# cap = cv2.VideoCapture('video.mp4')

# # Loop principal do programa
# while True:
#     # Lê um frame do vídeo
#     ret, frame = cap.read()

#     # Verifica se o frame foi lido corretamente
#     if not ret:
#         break

#     # Converte o frame para tons de cinza
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Aplica um filtro Gaussiano para suavizar a imagem
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Detecta as bordas na imagem usando o operador de Sobel
#     sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
#     sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
#     edges = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)

#     # Aplica a transformada de Hough para detectar as linhas na imagem
#     lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

#     # Desenha as linhas detectadas na imagem original
#     for line in lines:
#         rho,theta = line[0]
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a*rho
#         y0 = b*rho
#         x1 = int(x0 + 1000*(-b))
#         y1 = int(y0 + 1000*(a))
#         x2 = int(x0 - 1000*(-b))
#         y2 = int(y0 - 1000*(a))
#         cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

#     # Encontra os contornos dos agarras na imagem
#     contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # Desenha os contornos dos agarras na imagem original
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         # Adiciona as posições dos agarras na matriz de agarras
#         agarras.append((x, y))

#     # Exibe o frame do vídeo com as detecções dos agarras
#     cv2.imshow('Video', frame)

#     # Verifica se a tecla 'q' foi pressionada para encerrar o programa
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Libera os recursos utilizados pelo programa
# cap.release()
# cv2.destroyAllWindows()

# # Cria uma matriz para armazenar o número de vezes que cada agarra foi tocada
# contagem_agarras = np.zeros((len(agarras),), dtype=int)

# # Define a distância máxima permitida entre o centro de massa do contorno e o centro da detecção anterior da agarra
# distancia_maxima = 50

# # Loop principal do programa
# while True:
#     # Lê um frame do vídeo
#     ret, frame = cap.read()

#     # Verifica se o frame foi lido corretamente
#     if not ret:
#         break

#     # Converte o frame para tons de cinza
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # ...

#     # Encontra os contornos dos agarras na imagem
#     contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # Verifica se há contornos para processar
#     if len(contours) > 0:
#         # Cria uma matriz para armazenar as posições dos centros de massa dos contornos
#         centros_de_massa = np.zeros((len(contours), 2), dtype=int)

#         # Calcula os centros de massa dos contornos e os armazena na matriz
#         for i, contour in enumerate(contours):
#             M = cv2.moments(contour)
#             if M['m00'] != 0:
#                 centros_de_massa[i, 0] = int(M['m10'] / M['m00'])
#                 centros_de_massa[i, 1] = int(M['m01'] / M['m00'])

#         # Percorre a matriz de agarras
#         for i, (x, y) in enumerate(agarras):
#             # Calcula a distância entre o centro de massa do contorno mais próximo e o centro da detecção anterior da agarra
#             distancias = np.sqrt(np.sum((centros_de_massa - np.array([x, y])) ** 2, axis=1))
#             distancia_minima = np.min(distancias)

#             # Se a distância mínima for menor do que a distância máxima permitida, incrementa o contador correspondente na matriz de contagem_agarras
#             if distancia_minima < distancia_maxima:
#                 contagem_agarras[i] += 1

#     # ...

# # Exibe a matriz de contagem_agarras
# print(contagem_agarras)


