import cv2
import easyocr
import re
import os
from collections import defaultdict

# Initialize OCR once
reader = easyocr.Reader(['en'], gpu=False)

# Indian number plate regex
INDIAN_PLATE_REGEX = re.compile(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$')

# Common OCR mistakes
CHAR_MAP = {
    'O': '0', 'Q': '0', 'D': '0',
    'I': '1', 'L': '1',
    'S': '5', 'B': '8', 'Z': '2'
}

# Valid Indian state codes
VALID_STATES = [
    "MH","DL","UP","KA","TN","GJ","RJ","MP","PB","HR","BR",
    "WB","OD","AP","TS","KL","CG","JH","UK","HP","JK","AS"
]

# =========================
# Correction helpers
# =========================

def smart_correct(text):
    return "".join(CHAR_MAP.get(c, c) for c in text)


def fix_state_code(text):
    if len(text) < 2:
        return text

    first2 = text[:2]

    for state in VALID_STATES:
        diff = sum(a != b for a, b in zip(first2, state))
        if diff <= 1:
            return state + text[2:]

    return text


def clean_double_letters(text):
    if len(text) >= 3 and text[0] == text[1]:
        return text[1:]
    return text

# =========================
# Preprocessing
# =========================

def preprocess_variants(img):

    variants = []

    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(2.0, (8, 8))
    variants.append(clahe.apply(gray))

    blur = cv2.bilateralFilter(gray, 11, 17, 17)

    th = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15, 4
    )

    variants.append(th)
    variants.append(cv2.bitwise_not(th))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    variants.append(cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel))

    return variants

# =========================
# OCR MAIN FUNCTION
# =========================

def extract_number(plate_path, debug=False):

    if not os.path.exists(plate_path):
        return None

    img = cv2.imread(plate_path)
    if img is None:
        return None

    variants = preprocess_variants(img)

    plate_scores = defaultdict(list)

    for i, var in enumerate(variants):

        try:
            results = reader.readtext(var)
        except Exception:
            continue

        for (_, text, conf) in results:

            raw = re.sub(r'[^A-Z0-9]', '', text.upper())

            raw = smart_correct(raw)
            raw = fix_state_code(raw)
            raw = clean_double_letters(raw)

            if debug:
                print(f"Variant {i} → {raw} | Conf: {conf}")

            if len(raw) < 8 or len(raw) > 11:
                continue

            m = re.search(r'([A-Z]{2})(\d{2})([A-Z]{1,2})(\d{4})', raw)
            if not m:
                continue

            plate = "".join(m.groups())

            if INDIAN_PLATE_REGEX.match(plate):
                plate_scores[plate].append(conf)

    # ======================
    # Majority voting
    # ======================

    best_plate = None
    best_votes = 0
    best_avg_conf = 0

    for plate, confs in plate_scores.items():

        votes = len(confs)
        avg_conf = sum(confs) / votes

        if (
            votes > best_votes or
            (votes == best_votes and avg_conf > best_avg_conf)
        ):
            best_votes = votes
            best_avg_conf = avg_conf
            best_plate = plate

    return best_plate
    