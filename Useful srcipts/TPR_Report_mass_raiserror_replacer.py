import os
import re

FILE_ENCODING = 'cp1251'
FILE_EXT = '.tpr'

def get_dirs_and_files(start_folder = None, extension = None):
    #Функция берет список всех файлов из всех указанных каталогов начиная от стартовой дериктории
    #с соответствующим расширением. Если расширение не указано то берет все файлы
    file_path_list = []
    inner_folders = {}
    if start_folder is not None:
        for root, dirs, files in os.walk(start_to_scan_folder):
            inner_folders[root] = files
    for dir_path in inner_folders.keys():
        for file_name in inner_folders[dir_path]:
            name, ext = os.path.splitext(file_name)
            if extension != None and ext == extension:
                file_path_list.append(f'{dir_path}/{file_name}') 
            elif extension == None: 
                file_path_list.append(f'{dir_path}/{file_name}') 
    return file_path_list



def take_code_and_comment(string):
    #Функция берет код ошибки и сообщение  из строки raiserror
    replace_comment_list = []
    st_ch, fin_ch = string.find("'")+1, string.rfind("'")
    code_from_comment = re.findall(r"raiserror\s\d+", string)[0]
    replace_comment_list.append((string, code_from_comment[code_from_comment.find(" ")+1:len(code_from_comment)] ,string[st_ch:fin_ch]))
    return replace_comment_list            
    


# In[46]:


start_to_scan_folder = input("Enter start directory:") 
files_and_folders_list = get_dirs_and_files(start_to_scan_folder, FILE_EXT)

    
for file_path in files_and_folders_list:
    if os.path.isfile(file_path):
        file_content = None
        replace_list = []

        #Сожрем все из файла в буфер
        with open(file_path, 'r', encoding = FILE_ENCODING) as fh:
            file_content = fh.read()
        
        #Отберем нуные нам строки из файла по регулярныму вырожению
        replace_list = re.findall(r"raiserror\s\d+\s'.+'", file_content)
        
        #Если чото нашли переименуем файл исходник
        if len(replace_list) > 0:
            print(f"{file_path} - Идет обработка...")
            os.rename(file_path,file_path + '.bak')
            
            for string in replace_list:
                ready_to_replace = take_code_and_comment(string)
                
                for current_expr, retval, comment in ready_to_replace:
                    new_expr = f"raiserror('{comment} @RetVal = %d',16,1, {retval}) with nowait;"
                    file_content = file_content.replace(current_expr, new_expr)
            #Запишем все что поменяли в новый файл со старым именем
            with open(file_path, 'w', encoding = FILE_ENCODING) as fh:
                fh.write(file_content)
            print(f"{file_path} - Обработан")
print("Работа cкрипта заверешена")
