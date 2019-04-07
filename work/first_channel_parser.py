def parse_duration_views(duration_str):
    """    
    Parser of a views and duration string from the First Channel video catalogue
    
    parse_duration_views(str) -> tuple(int, int, int, int)
    
    duration_str    (str)       - string to be parsed (format [d*]h:mm:ss, may contain spaces)

    Return (views, hours, minutes, seconds)
    views     - number of views of the video
    hours     - number of duration hours
    minutes   - number of duration minutes
    seconds   - number of duration seconds
    
    Dependencies: none """

    # проверка на осмысленную длину строки
    if len(duration_str) > 0:     
        cnt = 0      # счетчик разделителя времени (:)
        seconds = 0  # секунды
        minutes = 0  # минуты
        hours = 0    # часы
        views = 0    # кол-во просмотров
        
        # удаляем пробелы внутри строки
        duration_str = duration_str.replace(' ', '')
        
        # считаем кол-во разделителей времени (:)
        for i in range(len(duration_str)):
            if duration_str[i] == ':':
                cnt += 1
        # слишком много разделителей (max = 2)        
        if cnt > 2 or cnt < 1:
            raise Exception('Unknown format. String should be [d*][h:]mm:ss')
        # заданы минуты и секунды (часов нет)
        elif cnt == 1:
            if len(duration_str) < 5:
                raise Exception('Unknown format. String should be [d*][h:]mm:ss')
            else:
                try:
                    seconds = int(duration_str[-2:])
                    if seconds >= 60:
                        raise Exception('Incorrect seconds value')
                    minutes = int(duration_str[len(duration_str) - 5: len(duration_str) - 3])
                    if minutes >= 60:
                        raise Exception('Incorrect minutes value')
                    hours = 0
                    if len(duration_str) == 5:
                        views = 0
                    else:
                        views = int(duration_str[:len(duration_str) - 5])
                except ValueError:
                    raise Exception('Not decimal symbols in time representation')
        # заданы часы, минуты и секунды
        elif cnt == 2:
            if len(duration_str) < 7:
                raise Exception('Unknown format. String should be [d*][h:]mm:ss')
            else:
                try:
                    seconds = int(duration_str[-2:])
                    if seconds >= 60:
                        raise Exception('Incorrect seconds value')
                    minutes = int(duration_str[len(duration_str) - 5: len(duration_str) - 3])
                    if minutes >= 60:
                        raise Exception('Incorrect minutes value')
                    hours = int(duration_str[len(duration_str) - 7: len(duration_str) - 6])
                    if len(duration_str) == 7:
                        views = 0
                    else:
                        views = int(duration_str[:len(duration_str) - 7])
                except ValueError:
                    raise Exception('Not decimal symbols in time representation')
    else:
        raise Exception('Empty string for parsing')
    
    return views, hours, minutes, seconds

def is_duration_views_line(s):
    """    
    Check is line like duration_views pattern or is a text name of a video
    
    is_duration_views_line(str) -> bool

    s    (str)       - line for checking

    Return bool flag: 
        True - line is like duration_views pattern
        False - line is not like duratiob_views pattern
    
    Dependencies: none """
    
    result = True

    for i in range(len(s)):
        if s[i].isalpha():
            result = False

    return result

def first_channel_parse(src_path, dst_path):
    """    
    Parser of First Channel video catalogue dump.
    Reads source file and writes result in destination file.
    
    first_channel_parse(str, str) -> list(dict)

    src_path    (str)       - source file path
    dst_path    (str)       - destination file path

    Return list of dictionaries (each dictionary for every video in video data dump in source file)
    Dictionary contains of:
    views     - number of views of the video
    hours     - number of duration hours
    minutes   - number of duration minutes
    seconds   - number of duration seconds
    duration  - full duration in seconds
    
    Dependencies: none """
    result = []                         # создаем список-результат
    first_iteration = True              # флаг первой итерации (считывания первого блока данных)
    first_text = True                   # флаг первой встречи текста в блоке (а не кол-ва просмотров и длительности видео)
    src_fd = open(src_path, 'r')        # открываем файл-источник на чтение
    
    for line in src_fd:
        line = line.strip()
        if len(line) > 0:
            # проверка на начало нового блока (начинается с кол-ва просмотров и длительности ролика)
            if is_duration_views_line(line):
                if not(first_iteration):
                    result.append(d)
                first_iteration = False
                first_text = True
                d = dict()
                v, h, m, s = parse_duration_views(line)
                d['views'] = v
                d['hours'] = h
                d['minutes'] = m
                d['seconds'] = s
                d['duration'] = h * 60 * 60 + m * 60 + s
            else:
                if first_text:
                    first_text = False
                    d['name'] = line

    # добавляем последний считанный элемент
    result.append(d)
    src_fd.close()
    
    # открываем файл-результат
    dst_fd = open(dst_path, 'w')
    for e in result:
        s = e['name'] + '\t' + str(e['views']) + '\t' + str(e['duration']) + '\n'
        dst_fd.write(s)
    dst_fd.close()    

    return result

