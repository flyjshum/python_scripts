# coding=utf-8
# python 2.7
# требуется установка через pip fdb и PyMySQL
import fdb
import pymysql

filepath1 = 'firstNameFile.txt'
filepath2 = 'secondNameFile.txt'

try:
    con = fdb.connect(host='localhost', database='test.fdb', user='sysdba', password='masterkey',
                      port=3050)
    cur = con.cursor()
    cur.execute("select * from firstname")
    result = cur.fetchall()
    try:
        f1 = open(filepath1, 'wx')
        fileSize1 = len(result)
        for id, name in result:
            f1.writelines(str(id) + ';' + name + '\n')
        print "Write " + str(fileSize1) + " lines in file " + filepath1

        cur.execute("select * from secondname")
        result = cur.fetchall()
        f2 = open(filepath2, 'wx')
        fileSize2 = len(result)
        for id, name in result:
            f2.writelines(str(id) + ';' + name + '\n')
        print "Write " + str(fileSize2) + " lines in file " + filepath2
        f1.close()
        f2.close()

        # нет внешнего ключа, связь между таблицами отсутствует, заполняем попарно
        # в результирующей таблице будет количество строк = макс в одном из файле
        f1 = open(filepath1, 'r')
        f2 = open(filepath2, 'r')
        fNames = f1.readlines()
        sNames = f2.readlines()
        con = pymysql.connect(host='localhost', user='root', password='_Linux87_1', db='test')
        cur = con.cursor()
        i = 0
        while i < max(fileSize1, fileSize2):
            if i < fileSize1:
                fName = fNames[i].split(";")[1][:-1]
            else:
                fName = ''
            if i < fileSize2:
                sName = sNames[i].split(";")[1][:-1]
            else:
                sName = ''
            query = 'insert into persons (id, firstname, secondname) values (' + str(
                i + 1) + ',"' + fName + '","' + sName + '")'
            cur.execute(query)
            con.commit()
            i += 1

    except Exception as e:
        print "Error: "+str(e)
        f1.close()
        f2.close()
    con.close()
except Exception as e:
    print "Error: "+str(e)

