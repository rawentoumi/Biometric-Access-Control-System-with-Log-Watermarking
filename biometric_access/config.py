import os

# ─── Paths ─────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(BASE_DIR, "biometric.db")
LOGS_DIR   = os.path.join(BASE_DIR, "logs")
FACES_DIR  = os.path.join(BASE_DIR, "faces_db")

os.makedirs(LOGS_DIR,  exist_ok=True)
os.makedirs(FACES_DIR, exist_ok=True)

# ─── Facial recognition ───────────────────────────────────────────────────
FACE_TOLERANCE       = 0.50   # maximal distance for face recognition (lower = stricter)
RECOGNITION_MODEL    = "hog"  # "hog" (CPU, rapide) ou "cnn" (GPU, precise)
FRAME_SKIP           = 3      # Traiter 1 frame sur N (optimisation temps réel)

# ─── Watermarking ─────────────────────────────────────────────────────────────
WATERMARK_METHOD     = "LSB"  # "LSB" or "DCT"

# ─── Email notifications ──────────────────────────────────────────────────────
SMTP_SERVER          = "smtp.gmail.com"
SMTP_PORT            = 587
EMAIL_SENDER         = "votre_email@gmail.com"      # ← to modify
EMAIL_PASSWORD       = "votre_mot_de_passe_app"     # ← email app password recommended 
EMAIL_RECIPIENT      = "admin@exemple.com"           # ← to modify
EMAIL_ENABLED        = False   # Set to True to enable email notifications (requires valid credentials)

# ─── Interface ────────────────────────────────────────────────────────────────
WEBCAM_INDEX         = 0
WINDOW_TITLE         = "Biometric Access Control"
FRAME_WIDTH          = 640
FRAME_HEIGHT         = 480

# ─── Interface colors (BGR for OpenCV, hex for Tkinter) ───────────────────
COLOR_GRANTED  = {"tk": "#27ae60", "cv": (39, 174, 96)}
COLOR_DENIED   = {"tk": "#e67e22", "cv": (39, 126, 230)}
COLOR_INTRUDER = {"tk": "#e74c3c", "cv": (60, 76, 231)}
COLOR_NEUTRAL  = {"tk": "#2c3e50", "cv": (80, 62, 44)}