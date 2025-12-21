# 🖱️ (너대신) 클릭클릭해

화면 보호기 방지 및 반복 클릭을 위한  
**매크로 프로그램**

---

## ✨ 주요 기능

- 마우스 클릭 위치 다중 저장
- 클릭 간격 및 실행 시간 설정
- 랜덤 딜레이 (±20%)
- 마우스 이동 애니메이션
- 실행 상태 / 타이머 / 진행률 표시
- 설정 자동 저장 (JSON)
- PyInstaller 빌드 대응

---

## ⌨️ 단축키

| 키 | 기능 |
|--|--|
| F1 | 정보 표시 |
| F2 | 위치 캡처 |
| F5 | 시작 / 중지 |
| ESC | 종료 |

---

## 📁 File System

```text
app/
 ├── main.py        # 실행 진입점
 ├── app.py         # 메인 앱 클래스
 ├── ui/            # GUI 구성
 ├── core/          # 매크로 로직
 └── utils/         # 설정, 로깅, 리소스

```
### ▶ 실행 방법
pip install -r requirements.txt
python app/main.py

### 🛠️ PyInstaller 빌드
pyinstaller --onefile --noconsole app/main.py

### ⚠️ 주의사항
- 과도한 매크로 사용은 서비스 약관 위반이 될 수 있습니다.
- 개인 책임 하에 사용하세요.


### File Detail Sturcture
```
neoclick/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── app.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── styles.py
│   │   ├── layout.py
│   │   └── dialogs.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── macro.py
│   │   ├── capture.py
│   │   └── timer.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       ├── logger.py
│       └── resource.py
│
├── assets/
│   ├── mouse.ico
│   └── mouse.png
│
├── click_click_config.json
├── requirements.txt
└── README.md
```