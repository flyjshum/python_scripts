# coding=utf-8
# python 2.7
import os
import time
import zipfile

timeout = 5000
val1 = './val1'
val2 = './val2'

#Функция проверяет сколько времени назад модифицирован файл
#Параметр file - имя проверяемого файла
def checkModifyFile(file):
    a = os.path.getmtime(file)
    b = time.time()
    return int(((b - a) / 60))


# Данной функции передаем лог для проверки (текстовый или архив)
# И ссылку на открытый файл конфигурации
# Функции составляет список списков сигнатур для проверки
# И ищет в переданном файле сигнатуру
def checkFileSignature(checkedLogFile, f):
    listAllSignature = []
    listSignature = [False, False]
    while True:
        line = f.readline()
        if line[-1:] == '\n':
            line = line[:-1]
        if len(line) == 0:
            break
        else:
            if str(line).isdigit():
                if int(line) == 0:
                    listSignature[0] = str(timeout)
                else:
                    listSignature[0] = line
            else:
                listSignature[1] = str(line)
        if not False in listSignature:
            listAllSignature.append(listSignature)
            listSignature = [False, False]

    timeFileModify = checkModifyFile(checkedLogFile)
    isFind = False
    isTime = False
    #Разный способ загрузки файла в память, в зависимости от переданного типа
    if os.path.splitext(checkedLogFile)[1]=='.txt':
        f = open(checkedLogFile, 'r')
    else:
        archive = zipfile.ZipFile(checkedLogFile, 'r')
        f = archive.open(archive.namelist()[0])
#Убираем символы новой строки
    for line in f.readlines():
        if line[-1:] == '\n':
            line = line[:-1]

        for listSignature in listAllSignature:
            if (listSignature[1] == line):
                msg = "Signature '" + listSignature[1] + "' found in file " + checkedLogFile
                isFind = True
                if timeFileModify <= int(listSignature[0]):
                    msg += " at last " + listSignature[0] + " minutes"
                    isTime = True
    f.close()
    if isFind == False and isTime == False:
        print "Not found signature"
    else:
        print msg


def scanTxtFile(file):
    isFound = False
    msg = "Not found in cfg"
    #Прогоняем загруженный файл по каждой конфигурации, ищем в каком конфиге он есть
    #Если находим, то дальнейшие конфиги не смотрим
    for curCfgDir, cfgDirs, cfgFiles in os.walk(val2):
        for cfgFile in cfgFiles:
            if os.path.splitext(cfgFile)[1] == '.cfg':
                f = open(os.path.join(curCfgDir, cfgFile), 'r')
                if cfgFile == 'default.cfg':
                    for line in f.readlines():
                        index = file.rfind('/')
                        nameFile = file[index + 1:]
                        if nameFile == line[:-1] or nameFile == line:
                            msg = file + " was found in " + cfgFile
                            isFound = True
                            if checkModifyFile(file) <= timeout:
                                msg += " and was update: " + str(checkModifyFile(file)) + \
                                       " minutes ago (timeout=" + str(timeout) + ")"
                            print msg
                            break
                else:
                    index = file.rfind('/')
                    nameFile = file[index + 1:]
                    if nameFile == f.readline()[5:-1]:
                        msg = file + " was found in " + cfgFile
                        isFound = True
                        print msg
                        checkFileSignature(file, f)
                        break
                f.close()
    if isFound == False:
        print msg
    print "--------"


for curdir, dirs, files in os.walk(val1):
    print "Search in directory " + curdir + "\n"
    for file in files:
        if os.path.splitext(file)[1] in ['.txt','.zip']:
            print "Search " + file
            scanTxtFile(os.path.join(val1, file))