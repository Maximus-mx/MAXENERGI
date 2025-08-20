import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as no

data = np.load('mnist_data.npz')

x_train = data['x_train']
y_train = data['y_train']
x_test = data['x_test']
y_test = data['y_test']

x_train, x_test = x_train / 255.0, x_test / 255.0

model = models.Sequential([
    layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10)
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Тестовая точность: {test_acc}")


def predict_custom_image(img_path):
    from PIL import Image, ImageOps

    img = Image.open(img_path).convert("L")
    img = ImageOps.invert(img)
    img = ImageOps.fit(img, (28, 28), methob=Image.Resampling.LANCZOS)
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions)
    print(f"Предсказаное число: {predicted_class} (увереность {confidence}")


predict_custom_image("Новая папка 2 / pixil-frame-0-23.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-22.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-21.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-20.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-19.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-18.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-17.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-16.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-15.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-14.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-13.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-12.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-11.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-9.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-8.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-7.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-6.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-5.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-4.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-3.png")
predict_custom_image("Новая папка 2 / pixil-frame-0-2.png")

if input("Сохранить? 1 - Да, 2 - Нет") == "1":
    model.save("mnist.model.h5")