import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import tensorflow as tf

# Caminho para as imagens de paredes de escalada e os arquivos de anotações de agarras
pasta_imagens = './imgs'
arquivo_anotacoes = 'coordenadas_agarras.csv'

# Carregando as imagens e as anotações
imagens = []
anotacoes = []
with open(arquivo_anotacoes) as f:
    for linha in f:
        imagem_path, x, y, w, h = linha.strip().split(',')
        imagem = cv2.imread(os.path.join(pasta_imagens, imagem_path))
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        imagem = cv2.resize(imagem, (446, 289)) # redimensionando para 446x289
        imagens.append(imagem)
        anotacoes.append((float(x), float(y), float(w), float(h)))


# Convertendo os dados para matrizes numpy
imagens = np.array(imagens)
anotacoes = np.array(anotacoes)

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(imagens, anotacoes, test_size=0.2, random_state=42)

# Normalizando as imagens
X_train = X_train / 255.
X_test = X_test / 255.

# Convertendo as coordenadas das agarras para one-hot encoding
# Convertendo as coordenadas das agarras para one-hot encoding
y_train = tf.one_hot(np.argmax(y_train, axis=-1), depth=4)
y_test = tf.one_hot(np.argmax(y_test, axis=-1), depth=4)

X_train = np.expand_dims(X_train, axis=-1)
X_test = np.expand_dims(X_test, axis=-1)

# Definindo a arquitetura da rede neural
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(289, 446, 1))) # alterando a forma de entrada
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4, activation='sigmoid'))


# Compilando o modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print(X_train.shape)
print(X_test.shape)

# Treinando o modelo
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Avaliando o modelo no conjunto de dados de teste
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Carregando uma nova imagem
nova_imagem = cv2.imread('./img/parede.jpg')
nova_imagem = cv2.cvtColor(nova_imagem, cv2.COLOR_BGR2GRAY)
nova_imagem = cv2.resize(nova_imagem, (446, 289))

# Fazendo a previsão da localização das agarras na nova imagem
previsao = model.predict(nova_imagem.reshape(1, 289, 446, 1))

# Imprimindo as coordenadas das agarras com maior probabilidade
coordenadas = np.argmax(previsao)
print('Coordenadas da agarrar:', coordenadas)
