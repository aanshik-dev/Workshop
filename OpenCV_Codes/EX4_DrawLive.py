"""
Air Drawing with Hand Gestures - OpenCV + MediaPipe
=====================================================
Gestures:
  👍 Thumb only visible   → SELECT mode   (hover thumb tip over palette swatch)
  ☝️  Index finger only   → DRAW mode     (draw with current colour)
  ✋ All 5 fingers open   → ERASE mode    (big rectangle eraser shown on screen)

Keyboard:
  C  →  clear canvas
  Q  →  quit

Requirements:
  pip install opencv-python mediapipe numpy
"""

import cv2
import mediapipe as mp
import numpy as np

# ── MediaPipe ──────────────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
)

# ── Colour palette ─────────────────────────────────────────────────────────────
PALETTE_COLORS = [
    ("Red",    (0,   0,   255)),
    ("Orange", (0,   140, 255)),
    ("Yellow", (0,   220, 220)),
    ("Green",  (0,   200,  80)),
    ("Cyan",   (200, 220,   0)),
    ("Blue",   (255,  80,   0)),
    ("Purple", (180,  0,  180)),
    ("Pink",   (147,  20, 255)),
    ("White",  (255, 255, 255)),
]

SWATCH_W    = 62
SWATCH_H    = 52
PALETTE_X   = 10
PALETTE_Y   = 10
PALETTE_GAP = 6

# ── Drawing / eraser sizes ─────────────────────────────────────────────────────
DRAW_THICKNESS  = 7
ERASER_W        = 90      # rectangle eraser half-width
ERASER_H        = 60      # rectangle eraser half-height

# ── State ──────────────────────────────────────────────────────────────────────
current_color = PALETTE_COLORS[0][1]
prev_point    = None
canvas        = None


# ══════════════════════════════════════════════════════════════════════════════
# Gesture detection
# ══════════════════════════════════════════════════════════════════════════════

def fingers_up(lm, handedness):
    """
    Returns [thumb, index, middle, ring, pinky]  ->  1 = extended, 0 = folded.
    """
    tips   = [4,  8,  12, 16, 20]
    pips   = [3,  6,  10, 14, 18]
    status = []

    # Thumb (x-axis)
    is_right = (handedness == "Right")
    if is_right:
        status.append(1 if lm[4].x < lm[3].x else 0)
    else:
        status.append(1 if lm[4].x > lm[3].x else 0)

    # Index -> Pinky (y-axis: tip above pip = extended)
    for t, p in zip(tips[1:], pips[1:]):
        status.append(1 if lm[t].y < lm[p].y else 0)

    return status


def get_gesture(lm, handedness):
    """
    'draw'   - only index finger up
    'select' - only thumb up
    'erase'  - all five fingers up
    'idle'   - anything else
    """
    f = fingers_up(lm, handedness)

    if f == [1, 1, 1, 1, 1]:
        return "erase"

    if f[0] == 0 and f[1] == 1 and f[2] == 0 and f[3] == 0 and f[4] == 0:
        return "draw"

    if f[0] == 1 and f[1] == 0 and f[2] == 0 and f[3] == 0 and f[4] == 0:
        return "select"

    return "idle"


# ══════════════════════════════════════════════════════════════════════════════
# Palette helpers
# ══════════════════════════════════════════════════════════════════════════════

def palette_rects():
    rects = []
    for i in range(len(PALETTE_COLORS)):
        x1 = PALETTE_X + i * (SWATCH_W + PALETTE_GAP)
        y1 = PALETTE_Y
        x2 = x1 + SWATCH_W
        y2 = y1 + SWATCH_H
        rects.append((x1, y1, x2, y2))
    return rects


def draw_palette(frame, active_color, gesture):
    rects = palette_rects()
    for (name, color), (x1, y1, x2, y2) in zip(PALETTE_COLORS, rects):
        ax1, ay1, ax2, ay2 = x1, y1, x2, y2
        if color == active_color:
            ax1 -= 2; ay1 -= 2; ax2 += 2; ay2 += 2

        cv2.rectangle(frame, (ax1, ay1), (ax2, ay2), color, -1)
        border_col = (0, 230, 255) if color == active_color else (255, 255, 255)
        border_w   = 4             if color == active_color else 1
        cv2.rectangle(frame, (ax1, ay1), (ax2, ay2), border_col, border_w)

    if gesture == "select":
        cv2.putText(frame, "Hover THUMB over colour",
                    (PALETTE_X, PALETTE_Y + SWATCH_H + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 230, 255), 1, cv2.LINE_AA)


def color_under_point(px, py):
    for (name, color), (x1, y1, x2, y2) in zip(PALETTE_COLORS, palette_rects()):
        if x1 <= px <= x2 and y1 <= py <= y2:
            return color
    return None


# ══════════════════════════════════════════════════════════════════════════════
# HUD
# ══════════════════════════════════════════════════════════════════════════════

def draw_hud(frame, gesture, color):
    label_map = {
        "select": "THUMB ONLY  |  SELECT COLOUR",
        "draw":   "INDEX ONLY  |  DRAWING",
        "erase":  "ALL FINGERS  |  ERASING",
        "idle":   "...",
    }
    label = label_map.get(gesture, "")
    h, w  = frame.shape[:2]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - 52), (w, h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    cv2.putText(frame, label, (14, h - 16),
                cv2.FONT_HERSHEY_SIMPLEX, 0.72, (230, 230, 230), 2, cv2.LINE_AA)

    # Active colour dot
    cx, cy = w - 42, h - 26
    cv2.circle(frame, (cx, cy), 18, color, -1)
    cv2.circle(frame, (cx, cy), 18, (255, 255, 255), 2)

    cv2.putText(frame, "Q: quit  |  C: clear", (w - 234, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 200, 200), 1, cv2.LINE_AA)


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    global canvas, current_color, prev_point

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("Air Drawing started.  Q = quit   C = clear canvas")
    print("Gestures:")
    print("  Thumb only       -> SELECT colour from palette")
    print("  Index only       -> DRAW")
    print("  All 5 fingers    -> ERASE (rectangle)")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        h, w  = frame.shape[:2]

        if canvas is None:
            canvas = np.zeros((h, w, 3), dtype=np.uint8)

        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gesture   = "idle"
        index_tip = None
        thumb_tip = None
        palm_pt   = None

        if results.multi_hand_landmarks:
            for hl, hc in zip(results.multi_hand_landmarks,
                              results.multi_handedness):
                handedness = hc.classification[0].label
                lm         = hl.landmark

                mp_draw.draw_landmarks(
                    frame, hl, mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(60, 180, 60),  thickness=1, circle_radius=2),
                    mp_draw.DrawingSpec(color=(60, 60, 180),  thickness=1),
                )

                gesture = get_gesture(lm, handedness)

                ix = int(lm[8].x * w);  iy = int(lm[8].y * h)   # index tip
                tx = int(lm[4].x * w);  ty = int(lm[4].y * h)   # thumb tip
                wx = int(lm[0].x * w);  wy = int(lm[0].y * h)   # wrist / palm

                index_tip = (ix, iy)
                thumb_tip = (tx, ty)
                palm_pt   = (wx, wy)

                # ── SELECT ──────────────────────────────────────────────────
                if gesture == "select":
                    picked = color_under_point(tx, ty)
                    if picked:
                        current_color = picked
                    prev_point = None

                # ── DRAW ────────────────────────────────────────────────────
                elif gesture == "draw":
                    if prev_point is not None:
                        cv2.line(canvas, prev_point, (ix, iy),
                                current_color, DRAW_THICKNESS)
                    prev_point = (ix, iy)

                # ── ERASE ───────────────────────────────────────────────────
                elif gesture == "erase":
                    ex1 = max(0,     wx - ERASER_W)
                    ey1 = max(0,     wy - ERASER_H)
                    ex2 = min(w - 1, wx + ERASER_W)
                    ey2 = min(h - 1, wy + ERASER_H)
                    cv2.rectangle(canvas, (ex1, ey1), (ex2, ey2), (0, 0, 0), -1)
                    prev_point = None

                else:
                    prev_point = None

        else:
            prev_point = None
            gesture    = "idle"

        # ── Compose ─────────────────────────────────────────────────────────
        canvas_mask = canvas.astype(bool)
        display     = frame.copy()
        display[canvas_mask] = canvas[canvas_mask]

        # ── Palette ─────────────────────────────────────────────────────────
        draw_palette(display, current_color, gesture)

        # ── Cursors / overlays ───────────────────────────────────────────────
        if gesture == "erase" and palm_pt:
            wx, wy = palm_pt
            ex1 = max(0,     wx - ERASER_W)
            ey1 = max(0,     wy - ERASER_H)
            ex2 = min(w - 1, wx + ERASER_W)
            ey2 = min(h - 1, wy + ERASER_H)
            # Filled black rectangle
            cv2.rectangle(display, (ex1, ey1), (ex2, ey2), (0, 0, 0), -1)
            # Bright cyan outline so it's visible against both light & dark strokes
            cv2.rectangle(display, (ex1, ey1), (ex2, ey2), (0, 220, 255), 3)
            # Label
            cv2.putText(display, "ERASER", (ex1 + 6, ey1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 255), 2, cv2.LINE_AA)

        elif gesture == "draw" and index_tip:
            cv2.circle(display, index_tip, DRAW_THICKNESS // 2 + 2,
                      current_color, -1)
            cv2.circle(display, index_tip, DRAW_THICKNESS // 2 + 2,
                      (255, 255, 255), 1)

        elif gesture == "select" and thumb_tip:
            cv2.drawMarker(display, thumb_tip, (0, 230, 255),
                          cv2.MARKER_CROSS, 28, 2, cv2.LINE_AA)

        # ── HUD ─────────────────────────────────────────────────────────────
        draw_hud(display, gesture, current_color)

        cv2.imshow("Air Drawing  |  Q=quit  C=clear", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas[:] = 0

    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    main()