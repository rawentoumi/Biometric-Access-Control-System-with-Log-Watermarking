import os

# ─── Paths ─────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(BASE_DIR, "biometric.db")
LOGS_DIR   = os.path.join(BASE_DIR, "logs")
FACES_DIR  = os.path.join(BASE_DIR, "faces_db")

os.makedirs(LOGS_DIR,  exist_ok=True)
os.makedirs(FACES_DIR, exist_ok=True)

# ─── Facial recognition ───────────────────────────────────────────────────
FACE_TOLERANCE       = 0.50   # Distance maximale pour considérer une correspondance
RECOGNITION_MODEL    = "hog"  # "hog" (CPU, rapide) ou "cnn" (GPU, précis)
FRAME_SKIP           = 3      # Traiter 1 frame sur N (optimisation temps réel)

# ─── Watermarking ─────────────────────────────────────────────────────────────
WATERMARK_METHOD     = "LSB"  # "LSB" ou "DCT"

# ─── Email notifications ──────────────────────────────────────────────────────
SMTP_SERVER          = "smtp.gmail.com"
SMTP_PORT            = 587
EMAIL_SENDER         = "votre_email@gmail.com"      # ← à modifier
EMAIL_PASSWORD       = "votre_mot_de_passe_app"     # ← mot de passe d'application Gmail
EMAIL_RECIPIENT      = "admin@exemple.com"           # ← à modifier
EMAIL_ENABLED        = False   # Mettre True pour activer les envois

# ─── Interface ────────────────────────────────────────────────────────────────
WEBCAM_INDEX         = 0
WINDOW_TITLE         = "Système de Contrôle d'Accès Biométrique"
FRAME_WIDTH          = 640
FRAME_HEIGHT         = 480

# ─── Interface colors (BGR for OpenCV, hex for Tkinter) ───────────────────
COLOR_GRANTED  = {"tk": "#27ae60", "cv": (39, 174, 96)}
COLOR_DENIED   = {"tk": "#e67e22", "cv": (39, 126, 230)}
COLOR_INTRUDER = {"tk": "#e74c3c", "cv": (60, 76, 231)}
COLOR_NEUTRAL  = {"tk": "#2c3e50", "cv": (80, 62, 44)}