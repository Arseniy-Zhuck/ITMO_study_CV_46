from typing import Optional, Dict

import cv2
import numpy as np
import timm
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from ultralytics import YOLO


class BalkaClassifier:
    def __init__(
        self,
        detector_path: str = "models/kleimo_detector.pt",
        classifier_path: str = "models/effb0_classifier.pt",
        device: Optional[str] = None,
        det_conf: float = 0.55,
        img_size: int = 224,
        tta: int = 1,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.det_conf = det_conf
        self.img_size = img_size
        self.detector = YOLO(detector_path)
        self.clf_type = self._detect_classifier_type(classifier_path)
        if self.clf_type == "timm":
            ckpt = torch.load(classifier_path, map_location=self.device)
            self.classes = ckpt["classes"]
            arch = ckpt["args"]["model"]
            self.classifier = timm.create_model(arch, pretrained=False, num_classes=len(self.classes))
            self.classifier.load_state_dict(ckpt["model"])
            self.classifier.to(self.device).eval()
            self.views = self._build_views(img_size, tta)
        else:
            self.classifier = YOLO(classifier_path)
            names = self.classifier.names
            self.classes = [names[i] for i in range(len(names))]

    @staticmethod
    def _detect_classifier_type(path: str) -> str:
        try:
            ckpt = torch.load(path, map_location="cpu")
            if isinstance(ckpt, dict) and "classes" in ckpt and "args" in ckpt:
                return "timm"
        except Exception:
            pass
        return "yolo"

    @staticmethod
    def _build_views(img_size: int, n_tta: int):
        tail = [A.CLAHE(clip_limit=2.0, p=1.0), A.Normalize(), ToTensorV2()]
        s, b, c = img_size, int(img_size * 1.15), int(img_size * 1.30)
        specs = [
            [A.Resize(s, s)],
            [A.Resize(b, b), A.CenterCrop(s, s)],
            [A.Resize(c, c), A.CenterCrop(s, s)],
        ][:max(1, n_tta)]
        return [A.Compose(sp + tail) for sp in specs]

    def _classify_crop(self, crop_bgr: np.ndarray) -> np.ndarray:
        if self.clf_type == "timm":
            rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
            acc = np.zeros(len(self.classes), dtype=np.float64)
            with torch.no_grad():
                for tf in self.views:
                    x = tf(image=rgb)["image"].unsqueeze(0).to(self.device)
                    acc += self.classifier(x).softmax(1)[0].cpu().numpy()
            return acc / len(self.views)
        else:  # yolo-cls
            r = self.classifier.predict(crop_bgr, imgsz=self.img_size, verbose=False)[0]
            return r.probs.data.cpu().numpy().astype(np.float64)

    def balka_classify(self, frame: np.ndarray) -> Optional[Dict]:
        if frame is None or frame.size == 0:
            return None

        det = self.detector.predict(frame, conf=self.det_conf, verbose=False)[0]
        boxes = det.boxes.xyxy.cpu().numpy().astype(int) if det.boxes is not None else []

        if len(boxes) == 0:
            return None

        total_prob = np.zeros(len(self.classes), dtype=np.float64)
        n_used = 0
        h, w = frame.shape[:2]
        for x1, y1, x2, y2 in boxes:
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            if x2 <= x1 or y2 <= y1:
                continue
            crop = frame[y1:y2, x1:x2]
            total_prob += self._classify_crop(crop)
            n_used += 1

        if n_used == 0:
            return None

        avg_prob = total_prob / n_used
        idx = int(avg_prob.argmax())
        return {
            "factory": self.classes[idx],
            "confidence": round(float(avg_prob[idx]), 4),
            "n_stamps": n_used,
        }


if __name__ == "__main__":
    import sys
    clf = BalkaClassifier()
    img = cv2.imread(sys.argv[1])
    print(clf.balka_classify(img))