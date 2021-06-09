import os
import filecmp
import glob
import json
import sys

target = ''

def progress_download(block_count, block_size, total_size):
    percentage = 100.0 * block_count * block_size / total_size
    if percentage > 100:
    	percentage = 100
    sys.stdout.write(f'\rダウンロードしています... {percentage:.0f}% ')

def data_download(path):
    import urllib.request
    import zipfile
    os.makedirs(path,exist_ok=True)
    try:
        urllib.request.urlretrieve("https://meedownloads.blob.core.windows.net/add-ons/Vanilla_Resource_Pack_1.17.0.zip", f'{path}/temp.zip',progress_download)
    except:
        error('データをダウンロード中にエラーが発生しました')
    with zipfile.ZipFile(f'{path}/temp.zip') as zf:
        zf.extractall(path)
    os.remove(f'{path}/temp.zip')

def cls():
    os.system('cls')

def error(text):
    print(f'エラー: {text}')
    input('エンターを押してプログラムを終了...')
    sys.exit()

def is_dir(target):
    if os.path.exists(target):
        if os.path.isdir(target):
            return True
        else:return False
    else:return False

def process_files(target):
    removed_size = 0
    removed_file = 0
    removed_folder = 0
    files = glob.glob(target+'/**/*.*',recursive=True)
    for i in files:
        if os.path.exists(i):
            path = './Resource'+i.replace(target,'')
            if not os.path.exists(path):
                removed_size += os.path.getsize(i)
                removed_file += 1
                os.remove(i)
                continue
            if filecmp.cmp(i,path):
                removed_size += os.path.getsize(i)
                removed_file += 1
                os.remove(i)
    
    folders = glob.glob(target+'./**',recursive=True)
    for i in folders:
        if os.path.isdir(i):
            if [f for f in os.listdir(i) if not f.startswith('.')] == []:
                removed_folder += 1
                try:
                    os.rmdir(i)
                except:pass
    return removed_file,removed_folder,removed_size

# Main
if __name__ == '__main__':
    if not os.path.exists('./Resource/'):
        print('お待ちください...')
        print('データをダウンロードしています...')
        data_download('./Resource')
        cls()

    loop = True
    while loop: # User Input
        cls()
        loop = False
        print('CheckResource - v1.0')
        print('Created by SkyLake')
        print('-------------------------------------')
        print('リソースパックの無駄なファイルを検出して削除します\nチェックするリソースパックのフォルダーをここにドラッグアンドドロップしてエンターを押してください')
        target = input('')
        target = target.replace('"','')
        cls()
        if target == 'u': # Option "u"
            import shutil
            shutil.rmtree('./Resource')
            print('データをアップデートしています.....')
            data_download('./Resource')
            loop = True
        elif target == 'e': # Option "e"
            sys.exit()

    # Main Process
    print('準備中です...')
    if is_dir(target): # True/False
        print('準備が完了しました。')
        print('処理を開始します。よろしいですか？(Enter)')
        input()
        print('処理中です...')
        removed_file,removed_folder,removed_size = process_files(target) # Process Files
        cls()
        # Result
        print('処理が完了しました。')
        print(f'削除したファイル: {removed_file}\n削除したフォルダー: {removed_folder}\n削除した容量: {removed_size/1000/1000:.2f}MB')
        input('エンターを押してプログラムを終了.....')
    else:error('指定されたパスは正しくありません')