# AI 삼각형 검증 앱 (AI Triangle Validator)

- 하나의 아이디어, 통합 프로덕션, 크로스 플랫폼

## 개요

- **실험적 접근 :** 간단한 기하학 문제 해결을 소규모 AI 프로젝트화
- **통합 프로덕션 :** 기획-개발-디자인-테스트의 전 과정을 구현
- **크로스 플랫폼 :** 다양한 프레임워크, 배포 환경 지원

## 주요 기능

- **삼각형 성립 검증:** 입력 받은 세 변의 길이로 삼각형 형성 가능 여부 확인
- **크로스 체크:** 수학적 방법(삼각형 부등식)과 AI 모델 예측 결과 비교

## 발전

### 1단계 : 핵심 기능 구현 [v1.0.0]
- 삼각형 검증 AI 모델 개발
- PyQt,PySide 기반 UI 개발

### 2단계 : UI, 아키텍처 개선 [진행 중]
- QML 기반 선언형 UI 도입
- Figma 활용한 UI 디자인
- MVVM 기반 4계층 아키텍처 도입
- ML 모델 어댑터 패턴 적용
- 코드 모듈화 및 재구성

### 3단계 : 크로스 플랫폼 지원 [예정]

## 기술 스택

- **백엔드 :** Python, TensorFlow
- **프론트엔드 :** PyQt/PySide6 (완료), QML (진행 중)
- **아키텍처 :** 4계층 구조, 어댑터 패턴
- **배포 환경 :** Docker, PyInstaller (진행 중)
- **개발 도구 :** Git, Github

## 아키텍처 개요

4계층 아키텍처를 사용하여 UI와 ML 모델 간의 의존성을 최소화

- **View 레이어 :** QML 기반 사용자 인터페이스
- **ViewModel 레이어 :** UI와 핵심 로직 연결
- **Core 레이어 :** 핵심 비즈니스 로직
- **Model 레이어 :** ML 모델 및 어댑터

## 프로젝트 구조

triangle-validator/
├── core/ # 핵심 비즈니스 로직
│ └── triangle_validator.py
├── models/ # ML 모델 및 어댑터
│ ├── triangle_model.py
│ └── adapters/
│ └── tf_adapter.py
├── viewmodels/ # ViewModel 계층
│ └── triangle_viewmodel.py
├── views/ # View 계층 (QML UI)
│ └── triangle_view.qml
├── assets/ # 이미지 및 리소스
│ └── images/
└── docs/ # 문서


## 배포 환경

현재 네이티브 Python 환경에서 실행 가능하며, 추후 Docker, PyInstaller 패키징과 Windows/Linux 네이티브 지원을 계획 중입니다.

### 시각화

<img src="assets/images/visual5.png" width="30%" alt="예측 결과 시각화">


<details>
<summary>AI 모델 개발 과정 (Click)</summary>

### 데이터셋

*   **생성 방법 :** 세 변의 길이로 구성된 OK/NG 삼각형 데이터를 1,000,000개씩 생성
*   **데이터 형식 :** (3, 1) 형태의 NumPy 배열
*   **전처리 :** StandardScaler 사용하여 정규화

### 모델 구조

*   **종류 :** Sequential
*   **입력층 :** Flatten layer (3, 1) 배열을 1차원으로 펼침
*   **은닉층 :** Dense layer (64개 노드, ReLU 활성화 함수)
*   **출력층 :** Dense layer (1개 노드, Sigmoid 활성화 함수)

### 학습 과정

*   **손실 함수 :** Binary Cross-Entropy
*   **옵티마이저 :** Adam
*   **학습 횟수 (Epochs) :** 8

### 모델 학습 코드

```python
def gen_triangle_sides(num_samples):
    success_cases = []
    fail_cases = []
    success_cnt = 0
    fail_cnt = 0

    while True:
        # 세 변의 길이를 랜덤으로 생성
        three_sides = np.random.randint(MIN_LEN, MAX_LEN, INPUT_SHAPE)

        # 가장 긴 변 < 나머지 두 변의 합 : 성공
        if is_valid_triangle(three_sides):
            if success_cnt < num_samples:
                success_cases.append(three_sides)
                success_cnt += 1
        else:
            if fail_cnt < num_samples:
                fail_cases.append(three_sides)
                fail_cnt += 1

        if success_cnt == num_samples and fail_cnt == num_samples:
            break

    return np.array(success_cases), np.array(fail_cases)

def is_valid_triangle(three_sides):
    max_len = max(three_sides)
    others_len = sum(three_sides) - max_len
    return True if others_len > max_len else False

# 데이터 생성 및 모델 학습
num_samples = 1000000
success_cases, fail_cases = gen_triangle_sides(num_samples)

# 데이터 정규화
scaler = StandardScaler()
norm_success_cases = scaler.fit_transform(success_cases.reshape(-1, 3)).reshape(-1, 3, 1)
norm_fail_cases = scaler.fit_transform(fail_cases.reshape(-1, 3)).reshape(-1, 3, 1)

# 데이터 결합 및 레이블 생성
triangles = np.concatenate([norm_success_cases, norm_fail_cases])
labels = np.concatenate([np.ones(num_samples), np.zeros(num_samples)])

# 모델 생성 및 학습
model = models.Sequential([
    layers.Flatten(input_shape=(3, 1)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(triangles, labels, epochs=8)
```

</details>
