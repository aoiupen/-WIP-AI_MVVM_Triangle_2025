# AI 삼각형 검증 앱 (AI Triangle Validator)

> 수학적 규칙과 머신러닝 예측을 통해 삼각형의 성립 가능성을 검증하는 경량 AI 애플리케이션

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

<p align="center">
  <img src="assets/images/visual5.png" width="40%" alt="삼각형 검증 UI">
</p>

## 📋 개요

이 프로젝트는 기하학적 원리와 AI를 결합하여 삼각형 성립 가능성을 검증합니다:

- **실험적 접근:** 간단한 기하학 문제를 실용적인 AI 애플리케이션으로 변환
- **전체 개발 주기:** 기획부터 개발, 디자인, 테스트까지 전 과정 포함
- **크로스 플랫폼 설계:** 다양한 환경에서의 배포를 위한 구조

## ✨ 주요 기능

- **이중 검증:** 수학적 계산과 AI 모델 예측 결과 비교
- **시각적 피드백:** 삼각형 속성의 직관적인 시각화 제공
- **MVVM 아키텍처:** 유지보수성을 위한 관심사 명확한 분리

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.8+
- PySide6/PyQt6
- TensorFlow 2.x

### 설치 방법

```bash
# 저장소 복제
git clone https://github.com/aoiupen/triangle-validator.git
cd triangle-validator

# 가상 환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 또는
.venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements-windows.txt  # Windows
# 또는
pip install -r requirements-linux.txt    # Linux
```

### 애플리케이션 실행

```bash
python main.py
```

## 🏗️ 프로젝트 아키텍처

이 애플리케이션은 4계층 아키텍처와 함께 MVVM(Model-View-ViewModel) 패턴을 따릅니다:

```
┌─────────┐    ┌────────────┐    ┌──────┐    ┌───────┐
│   View  │ ↔  │ ViewModel  │ ↔  │ Core │ ↔  │ Model │
└─────────┘    └────────────┘    └──────┘    └───────┘
   (QML)      (Python Bridge)    (Logic)     (AI Model)
```

- **View 계층:** QML 기반 사용자 인터페이스
- **ViewModel 계층:** UI와 핵심 로직 연결
- **Core 계층:** 비즈니스 로직 포함
- **Model 계층:** 어댑터 패턴을 사용한 ML 모델 작업 처리

## 📁 프로젝트 구조

```
triangle-validator/
├── core/              # 핵심 비즈니스 로직
├── models/            # ML 모델 및 어댑터
│   └── adapters/      # 프레임워크별 어댑터
├── viewmodels/        # ViewModel 컴포넌트
├── views/             # QML UI 파일
├── assets/            # 이미지 및 리소스
└── docs/              # 문서
```

## 📝 개발 로드맵

### 1단계: 핵심 기능 구현 ✓
- 기본 삼각형 검증 로직
- AI 모델 개발
- PyQt/PySide6 UI 구현

### 2단계: 아키텍처 개선 ⚙️
- QML UI 재설계
- MVVM 아키텍처 구현
- ML 프레임워크용 어댑터 패턴
- 코드 리팩토링 및 최적화

### 3단계: 크로스 플랫폼 지원 🔮
- 다중 프레임워크 구현
- 컨테이너화된 배포
- 네이티브 인스톨러

## 🧠 AI 모델 세부 정보

<details>
<summary>AI 모델 구현 세부 정보 보기</summary>

이 모델은 세 변의 길이로부터 삼각형 성립 가능성을 검증합니다:

### 데이터셋 생성
- 100만 개의 유효한 삼각형과 100만 개의 유효하지 않은 삼각형 예제
- StandardScaler를 사용한 데이터 정규화

### 모델 아키텍처
- Flatten 입력 레이어가 있는 Sequential 모델
- 은닉층: ReLU 활성화 함수가 있는 64개 노드
- 출력층: Sigmoid 활성화 함수가 있는 단일 노드
- 이진 분류(유효/유효하지 않은 삼각형)

### 성능
- 이진 크로스 엔트로피 손실 함수
- Adam 옵티마이저
- 8회 학습 에폭
</details>

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🤝 기여하기

기여는 언제나 환영합니다! 이슈나 풀 리퀘스트를 자유롭게 제출해주세요. 