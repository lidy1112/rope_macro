import cv2
import numpy as np
import pyautogui
import time
import mss
import win32gui
import keyboard

# ================== 설정 ==================
WINDOW_TITLE = "LDPlayer"
LOOP_DELAY = 0.008
RELATIVE_CLICK_POS = (960, 880)   

ROI_TOP = 340
ROI_BOTTOM = 850
ROI_LEFT = 380
ROI_RIGHT = 1520

# === 극강 두 번 점프 방지 ===
ROPE_Y_THRESHOLD = 750            # 감지 시작 높이를 낮춰 줄을 일찍 포착
CLICK_DELAY = 0.01                # 감지 후 클릭까지의 지연 시간 (타이밍 조절 핵심)
MIN_RED_PIXELS = 1000             # 필터 완화에 따라 최소 픽셀 수 조정
MIN_HORIZONTAL_LINE = 10000       # 줄의 가로선 강도 기준 하향
BASE_COOLDOWN = 0.50              # 초반 안정적인 박자를 위해 상향
# =========================================

running = False
last_jump_time = 0
start_time = 0
jump_count = 0

def find_ldplayer_window():
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and WINDOW_TITLE.lower() in win32gui.GetWindowText(hwnd).lower():
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
    with mss.MSS() as sct:
        screenshot = sct.grab(region)
        return np.array(screenshot)

def detect_rope_y(frame):
    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    roi = frame[ROI_TOP:ROI_BOTTOM, ROI_LEFT:ROI_RIGHT]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # HSV 필터의 채도(S)와 명도(V) 하한선을 완화하여 줄 감지력 향상
    lower1 = np.array([0, 130, 100])  # 채도와 명도 하한선 조정
    upper1 = np.array([10, 255, 255]) # Hue 범위를 좁혀 오렌지/노랑 계열 배제
    lower2 = np.array([170, 130, 100])
    upper2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    kernel = np.ones((3,7), np.uint8) # 커널 크기 줄여 줄 형태 보존
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (5, 3), 0) # 가우시안 블러 크기 줄여 줄 형태 보존
    
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
    
    detected = best_strength > MIN_HORIZONTAL_LINE and best_y > ROPE_Y_THRESHOLD
    return best_y, detected, red_count

def toggle_macro():
    global running, start_time, jump_count
    running = not running
    if running:
        start_time = time.time()
        jump_count = 0
        print(f"\n[{time.strftime('%H:%M:%S')}] 매크로 시작")
    else:
        print(f"\n[{time.strftime('%H:%M:%S')}] 정지")

def main():
    global running, last_jump_time, start_time, jump_count
    print("=== Another Eden 라틀 줄넘기 - 극강 버전 ===")
    
    rect = find_ldplayer_window()
    if not rect:
        print("LDPlayer 창을 찾지 못했습니다.")
        return
    
    region = (rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])
    print(f"창 영역: {region}")
    
    keyboard.add_hotkey('f3', toggle_macro)
    keyboard.add_hotkey('f4', lambda: keyboard.unhook_all() or exit(0))
    
    print("F3: 시작 | F4: 종료")
    
    prev_rope_y = 0  # 이전 프레임의 Y값 저장용

    try:
        while True:
            if not running:
                prev_rope_y = 0
                time.sleep(0.1)
                continue
            
            frame = capture_screen(region)
            rope_y, detected, red_count = detect_rope_y(frame)
            
            current_time = time.time()
            elapsed = current_time - start_time
            # 고속 구간 대응 하한선 유지
            dynamic_cooldown = max(0.09, BASE_COOLDOWN - (elapsed / 380))
            
            # 같은 높이에서 멈춘 경우도 포함하여 감지 누락 방지
            is_descending = (rope_y >= prev_rope_y) and rope_y > 0

            if detected and is_descending and (current_time - last_jump_time > dynamic_cooldown):
                click_x = region[0] + RELATIVE_CLICK_POS[0]
                click_y = region[1] + RELATIVE_CLICK_POS[1]
                
                time.sleep(CLICK_DELAY)  # 점프 타이밍 미세 지연
                pyautogui.click(click_x, click_y)
                jump_count += 1
                last_jump_time = current_time
                
                print(f"✅ 점프! y={rope_y} | red={red_count} | 총 {jump_count}회 | cd={dynamic_cooldown:.3f}")
            elif running and detected and rope_y > ROPE_Y_THRESHOLD:
                print(f"감지됨 y={rope_y} (red={red_count}) {'↓' if is_descending else '↑'}")
            
            prev_rope_y = rope_y  # Y값 업데이트
            time.sleep(LOOP_DELAY)
            
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()
        print(f"\n종료. 총 {jump_count}회 점프")

if __name__ == "__main__":
    main()