import cv2
import numpy as np
import pyautogui
import time
import mss
import win32gui
import keyboard

# ================== 설정 ==================
WINDOW_TITLE = "LDPlayer"
LOOP_DELAY = 0.010
RELATIVE_CLICK_POS = (960, 880)   

# ROI
ROI_TOP = 350
ROI_BOTTOM = 820
ROI_LEFT = 450
ROI_RIGHT = 1450

# === 타이밍 앞당김 ===
ROPE_Y_THRESHOLD = 530            # ← 낮춰서 점프를 더 빨리 (이전 620 → 560)
MIN_RED_PIXELS = 2200
MIN_HORIZONTAL_LINE = 1800        # 강한 줄 유지
BASE_COOLDOWN = 0.105
# =========================================

running = False
last_jump_time = 0
start_time = 0
jump_count = 0

def find_ldplayer_window():
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            if WINDOW_TITLE.lower() in win32gui.GetWindowText(hwnd).lower():
                hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        hwnd = hwnds[0]
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    return None

def capture_screen(region):
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        return np.array(screenshot)

def detect_rope_y(frame):
    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    roi = frame[ROI_TOP:ROI_BOTTOM, ROI_LEFT:ROI_RIGHT]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    lower1 = np.array([0, 95, 95])
    upper1 = np.array([12, 255, 255])
    lower2 = np.array([168, 95, 95])
    upper2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    kernel = np.ones((4,8), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (5,3), 0)
    
    red_count = cv2.countNonZero(mask)
    if red_count < MIN_RED_PIXELS:
        return 0, False, red_count
    
    y_proj = np.sum(mask, axis=1)
    best_y = 0
    best_strength = 0
    for y in range(len(y_proj)-1, 30, -1):
        if y_proj[y] > best_strength:
            best_strength = y_proj[y]
            best_y = y + ROI_TOP
    
    detected = (best_strength > MIN_HORIZONTAL_LINE and best_y > ROPE_Y_THRESHOLD)
    return best_y, detected, red_count

def toggle_macro():
    global running, start_time, jump_count
    running = not running
    if running:
        start_time = time.time()
        jump_count = 0
        print(f"\n[{time.strftime('%H:%M:%S')}] 매크로 시작 - 타이밍 앞당김")
    else:
        print(f"\n[{time.strftime('%H:%M:%S')}] 매크로 정지")

def main():
    global running, last_jump_time, start_time, jump_count
    print("=== Another Eden 줄넘기 - 점프 빨라짐 버전 ===")
    
    rect = find_ldplayer_window()
    if not rect:
        print("LDPlayer 창을 찾지 못했습니다.")
        return
    
    region = (rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])
    print(f"창 영역: {region}")
    
    keyboard.add_hotkey('f3', toggle_macro)
    keyboard.add_hotkey('f4', lambda: keyboard.unhook_all() or exit(0))
    
    print("F3 눌러 시작")
    
    try:
        while True:
            if not running:
                time.sleep(0.1)
                continue
            
            frame = capture_screen(region)
            rope_y, detected, red_count = detect_rope_y(frame)
            
            elapsed = time.time() - start_time
            dynamic_cooldown = max(0.065, BASE_COOLDOWN - (elapsed / 220))
            
            current_time = time.time()
            if detected and (current_time - last_jump_time > dynamic_cooldown):
                click_x = region[0] + RELATIVE_CLICK_POS[0]
                click_y = region[1] + RELATIVE_CLICK_POS[1]
                
                pyautogui.click(click_x, click_y)
                jump_count += 1
                last_jump_time = current_time
                
                print(f"✅ 점프! y={rope_y} | red={red_count} | 총 {jump_count}회 | cd={dynamic_cooldown:.3f}")
            elif running and 380 < rope_y < 800 and red_count > 5000:
                print(f"감지됨 y={rope_y} (red={red_count})")
            
            time.sleep(LOOP_DELAY)
            
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()
        print(f"\n종료. 총 {jump_count}회 점프")

if __name__ == "__main__":
    main()