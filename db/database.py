

class DataBase:  
    @classmethod
    def __user_name(cls, link):
        return link.split('/')[-2]
    
    @classmethod
    def __check_value(cls, value, link=False):
        if link:
            return cls.__user_name(value)
        return value
    
    @classmethod
    def __db_cut(cls, name_file, value_cut):
        with open(f'db/{name_file}', "r+") as file:
            lines = file.readlines()

            lines_to_delete = lines[:value_cut+1]

            new_lines = [i for i in lines if i not in lines_to_delete]
            
            file.seek(0)
            file.truncate()
            
            file.writelines(new_lines)

    
    @classmethod
    def add_users(cls, name_file, value, name=True):
        """Добавляет в текстовый файл переданное значение
        Args:
            name_file (string): имя файла
            value (str/list): передаваемое значение для записи
            name (bool): True - записывается только имя, если приходит False, то 
            записывается ссылкой
        """
    
        if isinstance(value, list):
            "Если переданное значение является списком"
            for i in value:
                i = cls.__check_value(i, name)
                with open(f'db/{name_file}', 'a') as file:
                    file.write(i + '\n')
        else:
            "Переданное значение не список"
            with open(f'db/{name_file}', 'a') as file:
                value = cls.__check_value(value, name)
                file.write(value + '\n')
                
    
    @classmethod
    def get_users(cls, name_file, value=1, remove=False):
        """
        Функция принимает имя файла и количество пользователей, которое нужно вернуть, если нужно 
        вернуть больше одного пользователя, то функция возвращает список, иначе строку
        Args:
            name_file (string): имя файла
            value (int): количество пользователей, которое надо вернуть
            remove (bool): изначально False - удаление пользователей из файла не происходит, если True -
            удаляет пользователей из файла
        """
        
        with open(f'db/{name_file}') as file:
            file_users = list(map(lambda x: x[:-1], file.readlines()[:value]))
            
            if remove:
                cls.__db_cut(name_file, value)
                
            if len(file_users) == 1:
                return file_users[0]
            return file_users
        
    @classmethod
    def check_list(cls, lst1, lst2):
        lst1, lst2 = set(lst1), set(lst2)
        print(f'DELETED len(lst1 & lst2) accounts')
        return list(lst1 - (lst1 & lst2))