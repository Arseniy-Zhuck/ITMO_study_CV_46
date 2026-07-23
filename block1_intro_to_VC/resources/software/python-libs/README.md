# Python-библиотеки и программные средства

# Список используемого программного обеспечения (Python-библиотеки)

По результатам анализа следующих заданий:
- Домашнее задание №1 (работа с изображениями, цветовые пространства, фильтрация, морфология, частотная фильтрация)
- Домашнее задание №2 (аффинные и перспективные преобразования)
- Домашнее задание №3 (поиск и анализ контуров, детектирование прямых)
- Лабораторная работа №1 (6 вариантов: выравнивание документа, штрих-код, дорожные знаки, монеты, перспектива, стрелочный прибор, USB-штекер)
- Задачи на классификацию и детекцию с аугментацией (Tomato Leaf Disease, WeedCrop)
- Задача оценки устойчивости модели к искажениям (надрессорная балка)

---

## Таблица библиотек

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|---|---|---|---|---|---|
| **OpenCV** (`opencv-python`) | Загрузка, обработка, фильтрация, геометрические преобразования, детекция контуров, работа с видео и камерой. | HW1 (все), HW2 (все), HW3 (все), LR1 (все варианты) | [PyPI](https://pypi.org/project/opencv-python/) | Apache 2.0 | 2026-07-23 |
| **NumPy** (`numpy`) | Многомерные массивы, линейная алгебра, БПФ, генерация случайных чисел, основы научных вычислений. | HW1 (задания 8–22), HW2 (задания 4–9), HW3 (задания 2–7), LR1 | [PyPI](https://pypi.org/project/numpy/) | BSD-3-Clause | 2026-07-23 |
| **PyTorch** (`torch`) | Фреймворк глубокого обучения: тензоры, автоматическое дифференцирование, GPU-ускорение, построение нейросетей. | tasks.md (аугментация, классификация, детекция), augmentation_task.md (устойчивость) | [PyPI](https://pypi.org/project/torch/) | BSD-3-Clause | 2026-07-23 |
| **TorchVision** (`torchvision`) | Предобученные модели (MobileNetV2, DenseNet121, ResNet-50, ConvNeXt-Tiny, EfficientNet-B0), датасеты, трансформации. | tasks.md (задание 1), augmentation_task.md | [PyPI](https://pypi.org/project/torchvision/) | BSD-3-Clause | 2026-07-23 |
| **Ultralytics** (`ultralytics`) | Обучение и инференс моделей YOLO (YOLOv8n и др.) для детекции, сегментации, классификации. | tasks.md (задание 3 – сравнение YOLOv8 с EfficientDet) | [PyPI](https://pypi.org/project/ultralytics/) | AGPL-3.0 | 2026-07-23 |
| **EfficientDet** (`effdet`) | PyTorch-реализация EfficientDet (EfficientDet-D0) для детекции объектов. | tasks.md (задания 2–3) | [PyPI](https://pypi.org/project/effdet/) | Apache 2.0 | 2026-07-23 |
| **Albumentations** (`albumentations`) | Высокопроизводительная библиотека для аугментации изображений: геометрические, цветовые, шумовые искажения. | tasks.md (задания 1–3) | [PyPI](https://pypi.org/project/albumentations/) | **Dual-licensed** (AGPL-3.0 / Commercial); версия ≤ 2.0.8 — MIT | 2026-07-23 |
| **Matplotlib** (`matplotlib`) | Построение графиков, визуализация изображений, отображение кривых обучения, матриц ошибок, гистограмм. | tasks.md (задания 1–3), HW1 (гистограммы) | [PyPI](https://pypi.org/project/matplotlib/) | BSD-совместимая (основана на PSF) | 2026-07-23 |
| **Pandas** (`pandas`) | Обработка табличных данных, логирование и анализ результатов экспериментов (CSV, Excel). | tasks.md | [PyPI](https://pypi.org/project/pandas/) | BSD | 2026-07-23 |
| **Scikit-learn** (`scikit-learn`) | Метрики качества (mAP, Precision, Recall, F1, accuracy), матрица ошибок, базовые алгоритмы ML. | tasks.md (задания 1–3) | [PyPI](https://pypi.org/project/scikit-learn/) | BSD-3-Clause | 2026-07-23 |

---

## Команды установки (все зависимости)

```bash
# Базовые библиотеки
pip install opencv-python numpy matplotlib pandas scikit-learn

# Глубокое обучение
pip install torch torchvision

# Детекция и сегментация
pip install ultralytics effdet

# Аугментация
pip install albumentations

```

## Совместимость и требования

- **Python:** версия **3.10** или выше (рекомендовано для всех перечисленных библиотек; проверено на 3.10–3.12).
- **PyTorch:** требует CUDA 11.8+ для GPU-ускорения (опционально, работает и на CPU). Устанавливается командой `pip install torch torchvision` – автоматически подбирается подходящая сборка.
- **OpenCV:** предварительно собранные «колёса» для CPU (опция `opencv-python`). Для использования CUDA-модулей (например, `cv2.cuda`) требуется самостоятельная сборка из исходников.
- **Ultralytics:** поддерживает Python ≥ 3.8; требует PyTorch ≥ 1.8. Устанавливается как `pip install ultralytics`.
- **EfficientDet (`effdet`):** требует PyTorch ≥ 1.9; работает с Python 3.10+.
- **Albumentations:** до версии 2.0.8 работает на любой версии Python 3.8+; версии 2.0.9+ могут иметь дополнительные зависимости (например, `opencv-python-headless`). Рекомендуется фиксировать версию: `pip install albumentations==2.0.8` для совместимости.
- **Matplotlib, Pandas, Scikit-learn:** стабильно работают с Python ≥ 3.8; обновления не вносят критических изменений.

### Рекомендуемые команды установки для разных платформ

```bash
# Минимальный набор для всех заданий (без глубокого обучения)
pip install opencv-python numpy matplotlib pandas scikit-learn

# Для заданий с нейросетями
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118   # CUDA 11.8
# или для CPU:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Для детекции
pip install ultralytics effdet

# Для аугментации (фиксированная версия 2.0.8)
pip install albumentations==2.0.8
```
```python
import cv2, numpy, torch, torchvision, albumentations, ultralytics, effdet, matplotlib, pandas, sklearn
print("Все библиотеки импортированы успешно!")
```

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision
from ultralytics import YOLO
import albumentations as A
import pandas as pd
from sklearn.metrics import accuracy_score

# 1. Чтение изображения
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Частотная фильтрация (NumPy + OpenCV)
spectrum = np.fft.fft2(gray)
spectrum_shift = np.fft.fftshift(spectrum)

# 3. Аугментация (Albumentations)
aug = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=15),
    A.ColorJitter(brightness=0.2, contrast=0.2)
])
augmented = aug(image=img)['image']

# 4. Предобученная модель (TorchVision)
model = torchvision.models.mobilenet_v2(pretrained=True)
model.eval()
tensor = torch.from_numpy(gray).unsqueeze(0).unsqueeze(0).float()  # пример

# 5. YOLO для детекции
model_yolo = YOLO('yolov8n.pt')
results = model_yolo(img)
results.show()

# 6. Построение графика (Matplotlib)
plt.plot([1,2,3], [0.5, 0.7, 0.9])
plt.title('Accuracy over epochs')
plt.show()
```