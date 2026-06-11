# Another Eden Rope Skipping Macro (LDPlayer)

이 프로젝트는 LDPlayer 에뮬레이터에서 '어나더 에덴' 게임의 줄넘기 미니게임을 자동화하기 위한 Python 매크로 스크립트입니다. 화면 인식을 통해 줄의 움직임을 감지하고 자동으로 점프하여 줄넘기 기록을 향상시키는 데 도움을 줍니다.

두 가지 버전의 매크로가 제공됩니다:
- `Baruoki_rope.exe` (기존 `rope_macro_b.py`): "타이밍 앞당김" 버전으로, 바루오키 줄넘기 등 점프 타이밍을 약간 더 빠르게 조정하여 반응성을 높였습니다.
- `Ratle_rope.exe` (기존 `rope_macro_r.py`): "극강" 버전으로, 라틀 줄넘기 등 고난도 구간을 위해 줄 감지 로직과 타이밍을 최적화하여 안정성을 높였습니다.

## 🚀 주요 기능

- **LDPlayer 창 자동 감지**: 지정된 제목의 LDPlayer 창을 자동으로 찾아 활성화합니다.
- **실시간 화면 캡처**: `mss` 라이브러리를 사용하여 빠르고 효율적으로 화면을 캡처합니다.
- **OpenCV 기반 줄 감지**:
    - HSV 색 공간을 활용하여 빨간색 줄을 정확하게 식별합니다.
    - ROI(관심 영역) 설정을 통해 불필요한 영역을 제외하고 처리 속도를 높입니다.
    - 모폴로지 연산 및 가우시안 블러를 적용하여 노이즈를 제거하고 줄 형태를 보존합니다.
    - 줄의 Y축 위치와 강도를 분석하여 점프 타이밍을 결정합니다.
- **자동 점프**: `pyautogui`를 사용하여 감지된 줄의 위치에 맞춰 자동으로 클릭(점프)을 수행합니다.
- **동적 쿨다운**: 게임 진행 시간에 따라 점프 쿨다운을 동적으로 조절하여 고속 구간에 대응합니다.
- **핫키 제어**: `F3` 키로 매크로 시작/정지, `F4` 키로 프로그램 종료 기능을 제공합니다.

## 📋 사전 준비 사항

이 매크로를 실행하려면 다음이 필요합니다:

1.  **Python 3.x**: Python 공식 웹사이트에서 최신 버전을 다운로드하여 설치하세요. 설치 시 "Add Python to PATH" 옵션을 반드시 선택해주세요.
2.  **LDPlayer 에뮬레이터**: '어나더 에덴'이 설치된 LDPlayer가 실행 중이어야 하며, **해상도는 반드시 1920x1080 (DPI 240)**으로 설정되어 있어야 합니다.
3.  **필요한 Python 라이브러리**:
    - `opencv-python`
    - `numpy`
    - `pyautogui`
    - `mss`
    - `pywin32`
    - `tkinter` (Python 기본 내장)
    - `keyboard`

## ⚙️ 설치 방법

1.  **Python 설치**:
    Python이 설치되어 있지 않다면, 위 링크에서 Python 3.x 버전을 다운로드하여 설치합니다. 설치 마법사에서 `Add Python to PATH` 옵션을 꼭 체크하세요.

2.  **라이브러리 설치**:
    명령 프롬프트(CMD) 또는 PowerShell을 열고 다음 명령어를 실행하여 필요한 라이브러리들을 설치합니다:
    ```bash
    pip install opencv-python numpy pyautogui mss pywin32 keyboard
    ```

## 📥 다운로드 및 실행

1.  **실행 파일 다운로드**: 이 저장소 우측의 [Releases](https://github.com/사용자아이디/저장소이름/releases) 페이지에서 최신 버전의 `.exe` 파일을 다운로드하세요.
2.  **직접 빌드하기 (개발자용)**: 소스 코드를 직접 빌드하려면 아래 명령어를 사용하세요.
    *   **Baruoki_rope.exe**: `$cv2p = python -c "import cv2, os; print(os.path.join(os.path.dirname(cv2.__file__), 'data'))"; python -m PyInstaller --onefile --name Baruoki_rope --add-data "$($cv2p);cv2/data" rope_macro_b.py`
    *   **Ratle_rope.exe**: `$cv2p = python -c "import cv2, os; print(os.path.join(os.path.dirname(cv2.__file__), 'data'))"; python -m PyInstaller --onefile --name Ratle_rope --add-data "$($cv2p);cv2/data" rope_macro_r.py`

## ▶️ 실행 방법

1.  LDPlayer 에뮬레이터를 실행하고 '어나더 에덴' 게임을 시작합니다.
2.  줄넘기 미니게임 화면으로 이동합니다.
3.  실행 파일(`Baruoki_rope.exe` 또는 `Ratle_rope.exe`)을 관리자 권한으로 실행합니다. **매크로 실행 시 설정 UI 창이 함께 나타납니다.**
    *   또는 파이썬 스크립트로 직접 실행할 경우:
    ```bash
    python rope_macro_b.py
    # 또는
    python rope_macro_r.py
    ```
5.  콘솔 창에 시작 메시지가 나타나면, 게임 화면이 활성화된 상태에서 `F3` 키를 눌러 매크로를 시작합니다.
6.  매크로가 실행되면 자동으로 줄을 감지하고 점프를 수행합니다.
7.  매크로를 일시 정지하려면 다시 `F3` 키를 누릅니다.
8.  매크로를 완전히 종료하려면 `F4` 키를 누릅니다.

### 💡 설정 UI 사용법
매크로 실행 시 나타나는 UI 창에서 슬라이더를 움직여 `CLICK_DELAY` (라틀 버전) 또는 `BASE_COOLDOWN` (바루오키 버전)과 `ROPE_Y_THRESHOLD` 값을 실시간으로 조정할 수 있습니다. 값을 변경하면 매크로에 즉시 반영됩니다.


## ️ 설정 (고급 사용자)

스크립트 상단에 있는 `================== 설정 ==================` 섹션의 값들을 수정하여 매크로의 동작을 미세 조정할 수 있습니다.

- `WINDOW_TITLE`: LDPlayer 창의 정확한 제목 (기본값: "LDPlayer").
- `LOOP_DELAY`: 각 프레임 처리 사이의 지연 시간 (낮을수록 반응성 증가, CPU 사용량 증가).
- `RELATIVE_CLICK_POS`: LDPlayer 창 내에서 클릭할 상대적인 X, Y 좌표.
- `ROI_TOP`, `ROI_BOTTOM`, `ROI_LEFT`, `ROI_RIGHT`: 화면 캡처 및 줄 감지에 사용할 관심 영역(Region of Interest)의 좌표.
- `ROPE_Y_THRESHOLD`: 줄로 인식할 Y축 최소 높이.
- `MIN_RED_PIXELS`: 줄로 인식하기 위한 최소 빨간색 픽셀 수.
- `MIN_HORIZONTAL_LINE`: 줄의 가로선 강도 기준.
- `BASE_COOLDOWN`: 점프 후 최소 쿨다운 시간.
- `CLICK_DELAY` (`Ratle_rope.exe`에만 해당): 줄 감지 후 클릭까지의 추가 지연 시간.

이 값들은 사용자의 LDPlayer 해상도, 게임 화면 설정, 그리고 개인적인 타이밍 선호도에 따라 조정이 필요할 수 있습니다.

## ⚙️ 문제 해결 (Troubleshooting)

### 1. `.exe` 파일이 화면 인식을 못하거나 실행되지 않을 때

PyInstaller로 생성된 `.exe` 파일이 화면 인식을 못하거나 제대로 실행되지 않는 경우, 다음 단계를 시도해 보세요.

1.  **관리자 권한으로 실행 (필수)**: `.exe` 파일을 마우스 오른쪽 버튼으로 클릭하여 **"관리자 권한으로 실행"**을 선택합니다. LDPlayer가 관리자 권한으로 실행 중인 경우, 매크로도 반드시 관리자 권한이어야 클릭 명령이 전달됩니다.

2.  **Windows 디스플레이 배율 확인**: Windows 설정에서 **"텍스트, 앱 및 기타 항목의 크기 변경"이 100%**로 설정되어 있는지 확인하세요. 배율이 125%나 150%일 경우, 매크로가 엉뚱한 좌표를 캡처하게 됩니다.

3.  **OpenCV 데이터 파일 포함**: 아래 명령어로 빌드하여 OpenCV 환경 문제를 해결하세요.

    먼저, `cv2/data` 폴더의 정확한 경로를 찾아야 합니다. PowerShell 또는 CMD에서 다음 Python 명령어를 실행하여 경로를 확인하세요:
    ```powershell
    python -c "import cv2, os; print(os.path.join(os.path.dirname(cv2.__file__), 'data'))"
    ```
    예시 출력: `C:\Users\leeda\AppData\Roaming\Python\Python312\site-packages\cv2\data`

    찾은 경로를 사용하여 `.exe` 파일을 다시 빌드합니다. `YOUR_CV2_DATA_PATH` 부분을 위에서 찾은 실제 경로로 바꿔주세요.
    ```powershell
    pip install pyinstaller # 이미 설치했다면 건너뛰세요.
    python -m PyInstaller --onefile --name Baruoki_rope --add-data "YOUR_CV2_DATA_PATH;cv2/data" rope_macro_b.py
    python -m PyInstaller --onefile --name Ratle_rope --add-data "YOUR_CV2_DATA_PATH;cv2/data" rope_macro_r.py
    ```
    **예시**: `YOUR_CV2_DATA_PATH`가 `C:\Users\leeda\AppData\Roaming\Python\Python312\site-packages\cv2\data`라면:
    ```powershell
    python -m PyInstaller --onefile --name Baruoki_rope --add-data "C:\Users\leeda\AppData\Roaming\Python\Python312\site-packages\cv2\data;cv2/data" rope_macro_b.py
    ```
    생성된 `.exe` 파일은 `dist` 폴더에서 확인할 수 있습니다.

### 2. EXE 실행 시 점프 타이밍이 파이썬 실행과 다를 때

EXE 환경은 연산 속도가 빨라 점프가 일찍 발생할 가능성이 높습니다.
- **점프가 너무 빠를 때**: UI의 슬라이더를 사용하여 `CLICK_DELAY` (라틀) 또는 `BASE_COOLDOWN` (바루오키) 값을 **0.01 단위로 상향** 조정하거나, `ROPE_Y_THRESHOLD`를 더 높여보세요.
- **반응이 늦을 때**: UI의 슬라이더를 사용하여 `ROPE_Y_THRESHOLD` 값을 낮추거나 `CLICK_DELAY` (라틀) 또는 `BASE_COOLDOWN` (바루오키) 값을 줄이세요.


## ⚠️ 주의 사항

- 이 매크로는 게임의 자동 플레이를 돕기 위한 도구입니다. 게임 약관에 위배될 수 있으므로 사용에 주의하십시오.
- 이 매크로는 **1920x1080 해상도**에 최적화되어 있습니다. 다른 해상도나 DPI 설정에서는 감지 영역(ROI)이 어긋나 작동하지 않을 수 있습니다.
- 매크로 실행 중에는 마우스와 키보드 제어가 어려울 수 있으니 주의하십시오.

---

즐거운 게임 되세요!

```