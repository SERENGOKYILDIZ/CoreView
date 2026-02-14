import subprocess
import os
import shutil
import sys
import time
from config import APP_NAME, VERSION

def build():
    print(f"[{APP_NAME}] v{VERSION} Derleme işlemi başlıyor...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, "assets", "logo.ico")
    
    # the folder of Release : releases/v1.0.0
    release_folder = os.path.join(current_dir, "releases", f"{APP_NAME}-v{VERSION}")
    # PyInstaller'ın oluşturacağı klasör adı:
    final_name = f"{APP_NAME}-v{VERSION}"
    
    if not os.path.exists(icon_path):
        print(f"❌ HATA: İkon bulunamadı: {icon_path}")
        return

    # 1. Eski Süreçleri Kapat
    print("⏳ Çalışan eski uygulamalar kapatılıyor...")
    subprocess.run(["taskkill", "/F", "/IM", f"{final_name}.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    # 2. PyInstaller Komutu (--onedir en sağlıklısıdır)
    command = [
        'pyinstaller',
        '--noconsole',
        '--onedir', 
        '--clean',
        f'--name={final_name}',
        f'--icon={icon_path}',
        '--add-data', f'assets{os.pathsep}assets',
        '--hidden-import', 'PyQt6.QtWebEngineWidgets',
        'main.py'
    ]

    try:
        # 3. Temizlik
        for folder in ["dist", "build"]:
            if os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=True)

        if os.path.exists(release_folder):
            shutil.rmtree(release_folder, ignore_errors=True)

        # 4. Derleme
        subprocess.run(command, check=True)

        # 5. Taşıma İşlemi (Klasörü komple taşıyoruz)
        generated_folder = os.path.join(current_dir, "dist", final_name)
        
        if os.path.exists(generated_folder):
            print(f"📦 Klasör taşınıyor: {release_folder}")
            shutil.move(generated_folder, release_folder)
            print(f"\n✅ BAŞARILI: Tüm uygulama dosyaları şurada:")
            print(f"👉 {release_folder}")
        else:
            print("❌ HATA: PyInstaller çıktı klasörü bulunamadı!")

        # Temizlik
        if os.path.exists("dist"): shutil.rmtree("dist")
        if os.path.exists("build"): shutil.rmtree("build")
        spec_file = f"{final_name}.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"🗑️ Geçici dosya silindi: {spec_file}")
        
    except subprocess.CalledProcessError:
        print("\n❌ DERLEME HATASI: PyInstaller çalışırken bir hata oluştu.")
    except Exception as e:
        print(f"\n❌ BEKLENMEYEN HATA: {e}")

if __name__ == "__main__":
    build()