
import os
import shutil
import json
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import psutil
import win32api

CONFIG_FILE = "config.json"
SUPPORTED_EXTENSIONS = [".mp4", ".jpg", ".jpeg", ".mov", ".wav", ".lrf"]

def find_drive_by_label(label_name):
    drives = psutil.disk_partitions()
    for drive in drives:
        try:
            vol_info = win32api.GetVolumeInformation(drive.device)
            vol_label = vol_info[0]
            if vol_label.lower() == label_name.lower():
                return drive.device
        except:
            continue
    return None

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "import_path": "D:/DJI_Imports",
        "device_label": "DJI_Action2",
        "imported_files": []
    }

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def get_all_files(root_dir):
    files = []
    for root, _, filenames in os.walk(root_dir):
        for f in filenames:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, root_dir)
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS:
                files.append((full_path, rel_path.replace("\\", "/")))
    return files

def migrate_data(old_path, new_path):
    for root, dirs, files in os.walk(old_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), old_path)
            dest_path = os.path.join(new_path, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(os.path.join(root, file), dest_path)

def import_files():
    config = load_config()
    device_path = find_drive_by_label(config["device_label"])
    if not device_path:
        messagebox.showerror("错误", "未检测到大疆相机设备！")
        return

    today = datetime.date.today().strftime("%Y-%m-%d")
    target_dir = os.path.join(config["import_path"], today)
    os.makedirs(target_dir, exist_ok=True)

    all_files = get_all_files(device_path)
    imported_files_set = set(config["imported_files"])
    new_files = [(full, rel) for full, rel in all_files if rel not in imported_files_set]

    if not new_files:
        messagebox.showinfo("提示", "没有新文件需要导入。")
        return

    copied = 0
    total_size = 0
    for src_path, rel_path in new_files:
        dst_path = os.path.join(target_dir, os.path.basename(rel_path))
        shutil.copy2(src_path, dst_path)
        total_size += os.path.getsize(dst_path)
        config["imported_files"].append(rel_path)
        copied += 1

    save_config(config)

    # 是否删除相机中的原文件
    if messagebox.askyesno("删除原文件", "导入完成，共导入 {} 个文件，是否删除相机中的这些文件？".format(copied)):
        for src_path, _ in new_files:
            try:
                os.remove(src_path)
            except:
                pass

    size_mb = total_size / 1024 / 1024
    messagebox.showinfo("导入完成", f"已导入 {copied} 个文件\n共计 {size_mb:.2f} MB")

def change_import_path():
    config = load_config()
    old_path = config["import_path"]
    new_path = filedialog.askdirectory(title="选择新的导入目录")
    if new_path:
        migrate = messagebox.askyesno("迁移数据", "是否将原有导入数据一并迁移到新目录？")
        config["import_path"] = new_path
        save_config(config)
        if migrate:
            migrate_data(old_path, new_path)
        messagebox.showinfo("完成", f"已切换至新目录：\n{new_path}")

def build_gui():
    root = tk.Tk()
    root.title("DJI Import Assistant")
    root.geometry("400x200")

    config = load_config()

    tk.Label(root, text="📷 当前设备名称: " + config["device_label"]).pack(pady=10)
    tk.Label(root, text="📂 当前导入路径:").pack()
    tk.Label(root, text=config["import_path"], fg="blue").pack()

    tk.Button(root, text="📥 导入新文件", command=import_files).pack(pady=10)
    tk.Button(root, text="🛠️ 更改导入目录", command=change_import_path).pack()
    tk.Button(root, text="❌ 退出", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
