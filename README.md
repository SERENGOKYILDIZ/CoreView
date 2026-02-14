# CoreView
*(formerly Markdown-Viewer)*

**CoreView** is a high-performance Markdown viewer built for speed and seamless integration with Windows. Utilizing **Python 3** and **PyQt6 (QWebEngine/Chromium)**, it delivers a modern, GitHub-style rendering experience with automatic dark/light mode adaptability.

Designed for professionals, CoreView launches instantly in a maximized window, providing an immersive and distraction-free environment for reading and reviewing Markdown documentation.

## Downloads

[![Download CoreView](https://img.shields.io/badge/Download-CoreView_v1.0.0-blue?style=for-the-badge&logo=windows)](https://github.com/SERENGOKYILDIZ/CoreView/releases/download/v1.0.0/CoreView-v1.0_Setup.exe)

## Features

*   **High-Performance Rendering**: Powered by Chromium (via QWebEngine) for fast and accurate Markdown display.
*   **GitHub-Style UI**: Familiar and clean interface that mirrors GitHub's rendering standards.
*   **Dynamic Theme Support**: Automatically adapts to your system's Dark or Light mode preference.
*   **Professional UX**: Auto-starts in "Maximized" mode for immediate productivity.
*   **Windows Integration**:
    *   Full context menu integration.
    *   Optional `.md` file association to make CoreView your default viewer.
    *   Custom Uninstall Display Icon in the Windows Control Panel.
*   **Multi-language Installer**: Professional installation wizard with support for **English** and **Turkish**.

## Developer Setup

### Prerequisites
*   Python 3.x
*   pip

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/SERENGOKYILDIZ/CoreView.git
    cd CoreView
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python main.py
    ```

## Build Process

CoreView includes a sophisticated build system to streamline development and distribution.

### 1. Create Standalone Executable
The `build.py` script uses **PyInstaller** to compile the application into a standalone directory. It handles all cleanup automatically.

```bash
python build.py
```
*   *Output*: Creates a standalone build in the `dist` directory.
*   *Cleanup*: Automatically removes `.spec` files and temporary build artifacts.

### 2. Generate Windows Installer
The `make_setup.py` script integrates with **Inno Setup** to create a professional Windows installer.

```bash
python make_setup.py
```
*   **Interactive**: Prompts you to select a version from the `/releases` folder.
*   **Registry Integration**: Configures file associations and uninstall options.
*   **Localization**: Generates an installer supporting both English and Turkish.

## 👨‍💻 Author

**Semi Eren Gökyıldız**
- Email: [gokyildizsemieren@gmail.com](mailto:gokyildizsemieren@gmail.com)
- Website: [https://semierengokyildiz.vercel.app/](https://semierengokyildiz.vercel.app/)
- GitHub: [SERENGOKYILDIZ](https://github.com/SERENGOKYILDIZ)
- LinkedIn: [semi-eren-gokyildiz](https://www.linkedin.com/in/semi-eren-gokyildiz/)