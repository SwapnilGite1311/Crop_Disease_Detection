# Crop Disease Detection

## Run the disease detection app (Windows)

Use Python 3.10 or 3.11. From this folder, install the runtime dependencies and start the GUI:

```powershell
python -m pip install -r requirements.txt
python MAINGUI.py
```

The app needs a webcam and the trained model at `model/best.pt`. Inference is limited to 5 FPS. A class must remain above 70% confidence for 4 seconds before the app saves an image and sends one WhatsApp image/message for that detection episode. Press **q** in the camera window to stop detection. Disease descriptions are read from `Crop_file/`.

For WhatsApp sending, keep WhatsApp Web logged in on the laptop and enter a valid WhatsApp number (a 10-digit Indian number or a number with country code). On Windows, `pywin32` is required so PyWhatKit can attach the captured image from the clipboard. The WhatsApp Web tab stays open so you can see the send result. Automated spraying still requires separate hardware and is not integrated into the detection app.

The training notebook reads `ROBOFLOW_API_KEY` from the environment (or prompts for it). Hardware examples use placeholder Blynk and Wi-Fi credentials; configure them locally before use. Do not commit real credentials or captured images.

## Project notes

- `Crop_Disease_Train.ipynb` is the original Google Colab training notebook; it is not needed to run inference.
- `Plant_Detection.py` is a separate leaf identification prototype and expects files and a model that are not included in this checkout.
- `Crop_Dataset_Gen.py` is a webcam data collection utility, not the main app.
