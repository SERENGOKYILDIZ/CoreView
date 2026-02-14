import subprocess
import os
import sys
from config import APP_NAME, VERSION

def select_release():
    releases_path = os.path.join(os.getcwd(), "releases")
    if not os.path.exists(releases_path):
        print("❌ HATA: 'releases' klasörü bulunamadı!")
        return None

    folders = [f for f in os.listdir(releases_path) if os.path.isdir(os.path.join(releases_path, f))]
    if not folders:
        print("❌ HATA: 'releases' içinde klasör bulunamadı!")
        return None

    print(f"\n--- {APP_NAME} Release Seçimi ---")
    for i, folder in enumerate(folders, 1):
        print(f"[{i}] {folder}")
    
    try:
        choice = int(input(f"\nHangi sürümü paketlemek istersiniz? (1-{len(folders)}): "))
        if 1 <= choice <= len(folders):
            return folders[choice - 1]
    except ValueError:
        pass
    print("❌ Geçersiz seçim!")
    return None

def generate_iss_file(selected_folder):
    current_dir = os.getcwd()
    release_path = os.path.join(current_dir, "releases", selected_folder)
    app_filename = selected_folder
    setup_output_name = f"{selected_folder.replace(' ', '_')}_Setup"

    iss = "; " + APP_NAME + " Kurulum Betiği\n"
    iss += '#define MyAppName "' + APP_NAME + '"\n'
    iss += '#define MyAppVersion "' + VERSION + '"\n'
    iss += '#define MyAppPublisher "Semi Eren Gökyıldız"\n'
    iss += '#define MyAppExeName "' + app_filename + '.exe"\n'
    iss += '#define MyReleasePath "' + release_path + '"\n'

    iss += "\n[Setup]\n"
    iss += "AppId={{D3B5A5C1-E8A4-4A6B-9F1D-8F2B3C4D5E6F}\n"
    iss += "AppName={#MyAppName}\n"
    iss += "AppVersion={#MyAppVersion}\n"
    
    # --- İSİM DÜZELTME (Denetim Masası için) ---
    # Bu satır Denetim Masasında "#" veya "version" ibaresini kaldırıp sadece adı yazar.
    iss += "AppVerName={#MyAppName}\n"
    
    iss += "AppPublisher={#MyAppPublisher}\n"
    iss += "DefaultDirName={autopf}\\{#MyAppName}\n"
    iss += "DefaultGroupName={#MyAppName}\n"
    iss += "AllowNoIcons=yes\n"
    iss += "OutputDir=setup_output\n"
    iss += "OutputBaseFilename=" + setup_output_name + "\n"
    iss += "SetupIconFile=assets\\logo.ico\n"
    iss += "UninstallDisplayIcon={app}\\{#MyAppExeName}\n"
    iss += "Compression=lzma\n"
    iss += "SolidCompression=yes\n"
    iss += "WizardStyle=modern\n"

    iss += "\n[Languages]\n"
    iss += 'Name: "turkish"; MessagesFile: "compiler:Languages\\Turkish.isl"\n'
    iss += 'Name: "english"; MessagesFile: "compiler:Default.isl"\n'

    iss += "\n[CustomMessages]\n"
    iss += 'turkish.AssocDescription=' + APP_NAME + ' uygulamasını .md dosyaları için varsayılan yap\n'
    iss += 'english.AssocDescription=Make ' + APP_NAME + ' the default application for .md files\n'
    iss += 'turkish.MdDocName=Markdown Dosyası\n'
    iss += 'english.MdDocName=Markdown Document\n'

    iss += "\n[Tasks]\n"
    iss += 'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked\n'
    iss += 'Name: "associate"; Description: "{cm:AssocDescription}"; GroupDescription: "File Association:"; Flags: checkedonce\n'

    iss += "\n[Files]\n"
    iss += 'Source: "{#MyReleasePath}\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs\n'

    iss += "\n[Icons]\n"
    iss += 'Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"\n'
    iss += 'Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon\n'

    iss += "\n[Registry]\n"
    # --- REGISTRY FİX ---
    # .md anahtarının varsayılan değerini (Default) değiştiriyoruz.
    iss += 'Root: HKCR; Subkey: ".md"; ValueType: string; ValueName: ""; ValueData: "{#MyAppName}.Doc"; Flags: uninsdeletevalue; Tasks: associate\n'
    
    # Uygulama detaylarını tanımlıyoruz
    iss += 'Root: HKCR; Subkey: "{#MyAppName}.Doc"; ValueType: string; ValueName: ""; ValueData: "{cm:MdDocName}"; Flags: uninsdeletekey; Tasks: associate\n'
    iss += 'Root: HKCR; Subkey: "{#MyAppName}.Doc\\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\\{#MyAppExeName},0"; Tasks: associate\n'
    iss += 'Root: HKCR; Subkey: "{#MyAppName}.Doc\\shell\\open\\command"; ValueType: string; ValueName: ""; ValueData: """{app}\\{#MyAppExeName}"" ""%1"""; Tasks: associate\n'

    with open("temp_installer.iss", "w", encoding="utf-8-sig") as f:
        f.write(iss)
    return "temp_installer.iss"

def build_setup():
    iscc_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if not os.path.exists(iscc_path):
        print(f"❌ HATA: ISCC.exe bulunamadı.")
        return

    selected = select_release()
    if not selected: return

    iss_file = generate_iss_file(selected)
    print(f"📦 {selected} için Setup derleniyor...")
    
    try:
        subprocess.run([iscc_path, iss_file], check=True)
        print(f"\n✅ BAŞARILI: Denetim Masası ikonu ve dil destekleri eklendi.")
    except Exception as e:
        print(f"❌ HATA: {e}")
    finally:
        if os.path.exists(iss_file):
            os.remove(iss_file)

if __name__ == "__main__":
    build_setup()