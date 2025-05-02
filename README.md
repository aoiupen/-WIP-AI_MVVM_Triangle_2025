# AI Triangle Validator

> A lightweight AI application that validates triangle feasibility through both mathematical rules and machine learning prediction.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

<p align="center">
  <img src="assets/images/visual5.png" width="40%" alt="Triangle Validator UI">
</p>

## 📋 Overview

This project combines geometric principles with AI to validate triangle feasibility:

- **Experimental Approach:** Transforms a simple geometric problem into a practical AI application
- **Full Development Cycle:** Covers planning, development, design, and testing
- **Cross-Platform Design:** Built for deployment across various environments

## ✨ Key Features

- **Dual Validation:** Compares mathematical calculation with AI model prediction
- **Visual Feedback:** Provides intuitive visual representation of triangle properties
- **MVVM Architecture:** Implements clean separation of concerns for maintainability

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PySide6/PyQt6
- TensorFlow 2.x

### Installation

```bash
# Clone repository
git clone https://github.com/aoiupen/triangle-validator.git
cd triangle-validator

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements-windows.txt  # Windows
# or
pip install -r requirements-linux.txt    # Linux
```

### Running the Application

```bash
python main.py
```

## 🏗️ Project Architecture

The application follows the MVVM (Model-View-ViewModel) pattern with a 4-layer architecture:

```
┌─────────┐    ┌────────────┐    ┌──────┐    ┌───────┐
│   View  │ ↔  │ ViewModel  │ ↔  │ Core │ ↔  │ Model │
└─────────┘    └────────────┘    └──────┘    └───────┘
   (QML)      (Python Bridge)    (Logic)    (AI Model)
```

- **View Layer:** QML-based user interface
- **ViewModel Layer:** Connects UI with core logic
- **Core Layer:** Contains business logic
- **Model Layer:** Handles ML model operations using adapter pattern

## 📁 Project Structure

```
triangle-validator/
├── core/              # Core business logic
├── models/            # ML models and adapters
│   └── adapters/      # Framework-specific adapters
├── viewmodels/        # ViewModel components
├── views/             # QML UI files
├── assets/            # Images and resources
└── docs/              # Documentation
```

## 📝 Development Roadmap

### Phase 1: Core Functionality ✓
- Basic triangle validation logic
- AI model development
- PyQt/PySide6 UI implementation

### Phase 2: Architecture Improvements ⚙️
- QML UI redesign
- MVVM architecture implementation
- Adapter pattern for ML frameworks
- Code refactoring and optimization

### Phase 3: Cross-Platform Support 🔮
- Multiple framework implementations
- Containerized deployment
- Native installers

## 🧠 AI Model Details

<details>
<summary>Click to expand AI model implementation details</summary>

The model validates triangle feasibility from three side lengths:

### Dataset Generation
- 1,000,000 valid and 1,000,000 invalid triangle examples
- Data normalized using StandardScaler

### Model Architecture
- Sequential model with Flatten input layer
- Hidden layer: 64 nodes with ReLU activation
- Output layer: Single node with Sigmoid activation
- Binary classification (valid/invalid triangle)

### Performance
- Binary cross-entropy loss function
- Adam optimizer
- 8 training epochs
</details>

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
