# Applications

> ⚠️ **These applications are research and demonstration artifacts, not clinically validated
> devices.** The external validation reported in the accompanying article shows the model does
> **not** transfer to independent clinical images and systematically **under-grades** burn
> severity — the dangerous direction. Do not use any of this software to make care decisions.

Three clients were built around the same two-stage model. Only **source** is committed here;
build artifacts, dependency caches, and model weights are deliberately excluded (see
[`.gitignore`](../.gitignore)). Model weights are hosted on Kaggle and archived on Zenodo at
publication.

---

## Architecture

```
┌──────────────┐   image    ┌────────────────────────────────────────────┐
│  Flutter app │ ─────────► │            Flask inference server          │
│  (burn_ai2)  │            │                                            │
│              │            │  YOLOv8x-seg  →  binary mask × image        │
│              │ ◄───────── │      ↓                                     │
└──────────────┘  grade +   │  resize / crop / normalise                 │
                  masked    │      ↓                                     │
                  image     │  Swin classifier → 1st / 2nd / 3rd degree  │
                            │                                            │
                            │  if no burn region is found,               │
                            │  the full frame is classified (fallback)   │
                            └────────────────────────────────────────────┘

┌────────────────────┐
│  iOS native app    │  same two-stage design, run on-device via LibTorch
│  (BurnDetectAI)    │  instead of calling the server
└────────────────────┘
```

The **no-detection fallback** is important: rather than failing when the localiser returns no
region, the server classifies the full frame. This is the "robust pipeline" evaluated in the
paper, and it is why the reported pipeline never has an auto-fail denominator.

---

## `flask-server/` — inference API

Single endpoint service that runs both stages.

| | |
|---|---|
| Endpoint | `POST /analyze` (multipart image upload) |
| Returns | predicted degree, confidence, and a URL to the masked image |
| Max upload | 16 MB |
| Stack | Flask + Ultralytics YOLO + `timm` Swin, served with gunicorn |
| Deployment | Hugging Face Spaces (HTTPS on 443) |

```bash
cd apps/flask-server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# place the two checkpoints in ./models/ (see docs/MODEL_CARD.md for sources)
python app.py            # dev
# gunicorn app:app       # production
```

**Note on pinned versions.** `requirements.txt` pins `torch==2.5.1` / `torchvision==0.20.1`.
This is deliberate: newer torch builds dropped the `sm_60` kernels needed by the NVIDIA P100
used for part of the benchmark. See the compute note in the root [`README`](../README.md).

## `flutter-app/` — cross-platform mobile client

Dart source only (`lib/`, `pubspec.yaml`, `test/`).

```
lib/
├── main.dart
├── config/
│   ├── app_config.dart          # API base URL (build-time, see below)
│   └── theme.dart
├── screens/
│   ├── splash_screen.dart
│   ├── home/home_screen.dart
│   └── processing/{image_processing_screen,result_screen}.dart
└── services/
    ├── burn_analyzer_service.dart   # POSTs to {base}/analyze
    └── burn_result.dart
```

The server URL is **not hardcoded** — it is injected at build time, so no endpoint or
credential is committed:

```bash
flutter pub get
flutter run --dart-define=BURN_API_BASE_URL=https://<your-space>.hf.space
```

## `ios-native/` — SwiftUI client

A separate native implementation that runs the models **on-device** (LibTorch) rather than
calling the server. Swift source only; the Xcode project, Pods, and bundled `.pt`/`.mlmodel`
weights are excluded.

```
BurnDetectAI/
├── BurnDetectAIApp.swift
├── Models/{BurnModels,ModelManager}.swift    # on-device inference
├── ViewModels/{AuthViewModel,BurnDetectionViewModel}.swift
├── Views/                                    # Camera, Home, Processing, Result, History, …
└── Helpers/Theme.swift
```

---

## Which model does each client run?

The deployed clients ship a **Swin-Small** classifier, whereas every pipeline number reported
in the paper uses the benchmarked **Swin-Tiny** weights. This discrepancy is stated explicitly
in the article (§3.3) and is the reason the app is described as a demonstration artifact rather
than the evaluated system.
