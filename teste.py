import cv2
import numpy as np

img = cv2.imread(".\img\parede_marcada.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplica um filtro Gaussiano para suavizar a imagem
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Detecta as bordas na imagem usando o operador de Sobel
sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
edges = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
edges = cv2.Canny(gray, 50, 200)
# Aplica a transformada de Hough para detectar as linhas na imagem
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

# Exibe a imagem final
cv2.imshow("Resultado", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
