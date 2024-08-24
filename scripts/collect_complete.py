from tqdm import tqdm
import numpy as np
import shutil
import os
import re

DATA_DIR = ''
datasets_prefix = {'MD40/bowl': 'MD', 'native':'NA', 'scanned':'SC', 'SN_bowl': 'SN'}
ignored = []
test_only_datasets = ['scanned']

def delete(path):
    if os.path.exists(path):
        os.remove(path)

def process_dir(directory, dataset, restart=False):
    real_dir = os.path.realpath(directory)
    dataset_dir = os.path.join(real_dir, dataset)
    collection_dir = os.path.join(real_dir, 'collection')
    dataset_name = real_dir.split('/')[-1]
    dataset_statement = f'{os.path.join(real_dir, f"__collection_{dataset_name}")}.csv'
    dataset_train = f'{os.path.join(real_dir, "__collection_train")}.csv'
    dataset_test = f'{os.path.join(real_dir, "__collection_test")}.csv'
    obj_list, train_list, test_list = [], [], []

    os.makedirs(collection_dir, exist_ok=True)
    if restart:
        delete(dataset_statement)
        delete(dataset_train)
        delete(dataset_test)
 
    for root, dirs, files in os.walk(dataset_dir):
        prefix = datasets_prefix[dataset]
        files = [file for file in files if file.endswith('.npy') ]
        if not files:
            continue
        if prefix == 'NA':
            shape = root.split('/')[-1].split(' ')[-1].lower()
            prefix = f'{datasets_prefix[dataset]}-{shape}' 
        is_test = ('/test' in root)
        for file in tqdm(files, desc=f'Copying files {dataset}', total=len(files)): 
            number = ''.join(re.findall(r'\d+', file))
            new_name = f"{collection_dir[1:]}/{prefix}_{number}.npy"
            
            for ext in ['.obj', '.off']:
                mesh_file = file.replace('.npy', ext)
                mesh_path = os.path.join(root, mesh_file)
                if os.path.exists(mesh_path):
                    shutil.copy(mesh_path, f'/{new_name.replace(".npy", ext)}')

            shutil.copy(os.path.join(root, file), f'/{new_name}')

            relative_name = os.path.join(directory, 'collection', f"{prefix}_{number}.npy")
            obj_list.append(relative_name)
            if is_test:
                test_list.append(relative_name)
            else:
                train_list.append(relative_name)
                
    if test_list == [] and (not dataset in test_only_datasets):
        donations = np.random.choice(
            range(0, len(train_list)), 
            size= int(len(train_list)*.7), 
            replace=False)
        donations[::-1].sort() # reverse
        for idx in donations:
            test_list.append(train_list.pop(idx))
    
    if dataset in test_only_datasets:
        test_list = [] + train_list
        train_list = []

    with open(dataset_statement, 'a') as f:
        for file in obj_list:
            f.write(f'{file}\n')
    with open(dataset_train, 'a') as f:
        for file in train_list:
            f.write(f'{file}\n')
    with open(dataset_test, 'a') as f:
        for file in test_list:
            f.write(f'{file}\n')


if __name__ == '__main__':
    restart = True
    for directory in datasets_prefix:
        process_dir(DATA_DIR, directory, restart=restart)
        restart = False