Установка:
pip install -r requirements.txt

________________________________________


Параметры конструктора:

detector_path (по умолчанию models/kleimo_detector.pt) - веса YOLO детектора

classifier_path (по умолчанию models/effb0_classifier.pt) - веса классификатора (тип определится автоматически. Это пришлось сделать, так как yolo классифаер загружается иначе чем timm)

device (по усолчанию авто) - устройство вычислений

det_conf (по усолчанию 0.55) - порог уверенности при детекции клейма

img_size (по умолчанию 224) - размер входа классификатора 

tta (по умолчанию 1) - число видов при классификации

_________________________

Использование:

```python
from balka_classifier import BalkaClassifier
import cv2
 
clf = BalkaClassifier(
    detector_path="models/kleimo_detector.pt",
    classifier_path="models/effb0_classifier.pt",
)
 
frame = cv2.imread("balka.jpg")
result = clf.balka_classify(frame)
 
print(result)
# {"factory": "altai", "confidence": 0.98, "n_stamps": 2}
# либо None, если клейма на кадре не найдены
```


## Сводная таблица

| Модель | Датасет | Формат | Предобработка | Балок | Accuracy | Macro-F1 |
| --- | --- | --- | --- | --- | --- | --- |
| tf_efficientnet_b0 | clean_crops_clean | beam_vote | кроп детектор + чистка + CLAHE | 296 | 0.9865 | 0.9847 |
| yolo11s-cls.pt | data_crops_clean | beam_vote | кроп детектор + чистка | 296 | 0.9865 | 0.9837 |
| resnet50 | clean_crops_clean | beam_vote | кроп детектор + чистка + CLAHE + 2ух фазное обучение | 296 | 0.9764 | 0.9724 |
| convnext_tiny | clean_crops_clean | beam_vote | кроп детектор + чистка + CLAHE + пониженный lr | 296 | 0.9696 | 0.9675 |


## Подробности по прогонам

### tf_efficientnet_b0 @ 224px (ckpt: best_effb0_crops.pt) — clean_crops_clean

- **Формат:** beam_vote
- **Предобработка:** кроп детектор + чистка + CLAHE
- **Размер входа:** 224px | **TTA:** 1 | **Балок:** 296 | **Кропов:** 503
- **Accuracy:** 0.9865 | **Macro-F1:** 0.9847

**Метрики по заводам:**

| Завод | Precision | Recall | F1 | Балок |
| --- | --- | --- | --- | --- |
| altai | 0.980 | 1.000 | 0.990 | 49 |
| begickaya | 0.990 | 1.000 | 0.995 | 100 |
| promlit | 1.000 | 0.940 | 0.969 | 50 |
| ruzhimmash | 0.980 | 0.980 | 0.980 | 50 |
| tihvin | 0.979 | 1.000 | 0.990 | 47 |

**Матрица ошибок** (строки — истина, столбцы — предсказание):

|  | altai | begickaya | promlit | ruzhimmash | tihvin |
| --- | --- | --- | --- | --- | --- |
| altai | 49 | 0 | 0 | 0 | 0 |
| begickaya | 0 | 100 | 0 | 0 | 0 |
| promlit | 1 | 1 | 47 | 1 | 0 |
| ruzhimmash | 0 | 0 | 0 | 49 | 1 |
| tihvin | 0 | 0 | 0 | 0 | 47 |

### YOLO-cls (yolo11s-cls.pt) @ 224px — data_crops_clean

- **Формат:** beam_vote
- **Предобработка:** кроп детектор + чистка
- **Размер входа:** 224px | **TTA:** 1 | **Балок:** 296 | **Кропов:** 503
- **Accuracy:** 0.9865 | **Macro-F1:** 0.9837

**Метрики по заводам:**

| Завод | Precision | Recall | F1 | Балок |
| --- | --- | --- | --- | --- |
| altai | 0.961 | 1.000 | 0.980 | 49 |
| begickaya | 1.000 | 1.000 | 1.000 | 100 |
| promlit | 1.000 | 0.920 | 0.958 | 50 |
| ruzhimmash | 0.962 | 1.000 | 0.980 | 50 |
| tihvin | 1.000 | 1.000 | 1.000 | 47 |

**Матрица ошибок** (строки — истина, столбцы — предсказание):

|  | altai | begickaya | promlit | ruzhimmash | tihvin |
| --- | --- | --- | --- | --- | --- |
| altai | 49 | 0 | 0 | 0 | 0 |
| begickaya | 0 | 100 | 0 | 0 | 0 |
| promlit | 2 | 0 | 46 | 2 | 0 |
| ruzhimmash | 0 | 0 | 0 | 50 | 0 |
| tihvin | 0 | 0 | 0 | 0 | 47 |

### resnet50 @ 224px (ckpt: best_ft_r50.pt) — clean_crops_clean

- **Формат:** beam_vote
- **Предобработка:** кроп детектор + чистка + CLAHE + 2ух фазное обучение
- **Размер входа:** 224px | **TTA:** 1 | **Балок:** 296 | **Кропов:** 503
- **Accuracy:** 0.9764 | **Macro-F1:** 0.9724

**Метрики по заводам:**

| Завод | Precision | Recall | F1 | Балок |
| --- | --- | --- | --- | --- |
| altai | 0.980 | 1.000 | 0.990 | 49 |
| begickaya | 0.990 | 1.000 | 0.995 | 100 |
| promlit | 1.000 | 0.860 | 0.925 | 50 |
| ruzhimmash | 0.909 | 1.000 | 0.952 | 50 |
| tihvin | 1.000 | 1.000 | 1.000 | 47 |

**Матрица ошибок** (строки — истина, столбцы — предсказание):

|  | altai | begickaya | promlit | ruzhimmash | tihvin |
| --- | --- | --- | --- | --- | --- |
| altai | 49 | 0 | 0 | 0 | 0 |
| begickaya | 0 | 100 | 0 | 0 | 0 |
| promlit | 1 | 1 | 43 | 5 | 0 |
| ruzhimmash | 0 | 0 | 0 | 50 | 0 |
| tihvin | 0 | 0 | 0 | 0 | 47 |

### convnext_tiny @ 224px (ckpt: best_cnx_warm.pt) — clean_crops_clean

- **Формат:** beam_vote
- **Предобработка:** кроп детектор + чистка + CLAHE + пониженный lr
- **Размер входа:** 224px | **TTA:** 1 | **Балок:** 296 | **Кропов:** 503
- **Accuracy:** 0.9696 | **Macro-F1:** 0.9675

**Метрики по заводам:**

| Завод | Precision | Recall | F1 | Балок |
| --- | --- | --- | --- | --- |
| altai | 0.907 | 1.000 | 0.952 | 49 |
| begickaya | 0.971 | 0.990 | 0.980 | 100 |
| promlit | 1.000 | 0.900 | 0.947 | 50 |
| ruzhimmash | 1.000 | 0.940 | 0.969 | 50 |
| tihvin | 0.979 | 1.000 | 0.990 | 47 |

**Матрица ошибок** (строки — истина, столбцы — предсказание):

|  | altai | begickaya | promlit | ruzhimmash | tihvin |
| --- | --- | --- | --- | --- | --- |
| altai | 49 | 0 | 0 | 0 | 0 |
| begickaya | 0 | 99 | 0 | 0 | 1 |
| promlit | 3 | 2 | 45 | 0 | 0 |
| ruzhimmash | 2 | 1 | 0 | 47 | 0 |
| tihvin | 0 | 0 | 0 | 0 | 47 |
