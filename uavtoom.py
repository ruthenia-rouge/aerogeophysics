import math as math
import PySimpleGUI as sg

sg.theme('LightBlue3')

ptt = [
    [sg.Radio('.pos в .tbl (гондола)','OPTYPE',default=False,key = 'radio1'),sg.Radio('Добавить заголовок GPS (коптер)','OPTYPE',default=False, key = 'radio2'),
    sg.Radio('Добавить заголовок RFND (коптер)','OPTYPE',default=False, key ='radio3' )],
    [sg.Text('Исходные файлы'),sg.FilesBrowse('Поиск файлов', key = 'fbpos',target='hidden'),
    sg.Text('.tbl файлы',size = (60,1),justification='r'),sg.Button('Преобразовать файлы', key = 'transform')],
    [sg.Multiline(size = (60,20), key = 'input_files'),sg.Input(key = 'hidden',visible=False, enable_events=True),
    sg.Button('Генерация имени файла', key = 'gen1'),sg.Multiline(size = (60,20), key = 'tblfile')],
]

xyz_rai = [
    [sg.Text('Исходный файл, требующий разряжения и интерполяции')],
    [sg.Input(key = 'xyzfile_input'),sg.FileBrowse('Поиск файла', key = 'fb2')],
    [sg.Text('Параметры:')],
    [sg.Text('Расстояние между точками, (м)'),sg.Text('_', key = 'dbp'),sg.Text('Число точек'),sg.Input(key = 'numpoints_xyz',size = (4,1)),sg.Button('Расчет параметров',key = 'xyz_par')],
    [sg.Text('Конечный файл')],
    [sg.Input(key = 'xyzfile_output'),sg.Button('Генерация имени файла', key = 'gen2')],
    [sg.Button('.xyz в разряж. .txt', key = 'new_ascii')]
]

layout = [[sg.TabGroup(
                    [[sg.Tab('TBL Заголовки',ptt),sg.Tab('XYZ Разряжение и интерполяция', xyz_rai)]]
                )]]
window = sg.Window('UAVtoOM',layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'hidden':
        window.Element('input_files').update(values['hidden'])
        listfiles = values['hidden'].split(';')
        lnght = len(listfiles)
        window['input_files'].update(listfiles)

    if event == 'gen1':
        new_listfiles = []
        for i in range (lnght):
            name_file1 = listfiles[i]
            if values['radio1'] == True:
                name_file2 = listfiles[i].replace('.pos','.tbl')
                new_listfiles.append(name_file2)
            elif values['radio2'] == True:
                name_file2 = listfiles[i].replace('.tbl','')
                name_file2 = name_file2 + '_gps.tbl'
                new_listfiles.append(name_file2)
            elif values['radio3']== True:
                name_file2 = listfiles[i].replace('.tbl','')
                name_file2 = name_file2 + '_rfnd.tbl'
                new_listfiles.append(name_file2)
            else:
                name_file2 = 'Нет новых файлов'
                new_listfiles.append(name_file2)
                sg.popup_error('Ошибка: Выберите тип преобразования')            
        window['tblfile'].update(new_listfiles)


    if event == 'transform':
        if values['radio1'] == True:
            new_listfiles = values['tblfile'].split(',')
            for i in range (lnght):
                name_file1 = listfiles[i]
                name_file2 = new_listfiles[i]
                name_file2 = name_file2.replace("[","")
                name_file2 = name_file2.replace("]","")
                name_file2 = name_file2.replace("'","")
                name_file2 = name_file2.replace(" ","")
                print(name_file2)
                file1 = open(name_file1,'r')
                file2 = open(name_file2,'w')
                i = 0
                while i < 24 :
                    i += 1
                    line = file1.readline()
                file2.write("/= QQ :real \n/= GPST :real \n/= latitude :real")
                file2.write("\n/= longitude :real \n/= height :real \n/= Q :real \n/= ns :real \n/= sdn(m) :real" )
                file2.write(" \n/= sde(m) :real \n/= sdu(m) :real \n/= sdne(m) :real \n/= sdeu(m) :real \n/= sdun(m) :real \n" )
                file2.write("/= age(s) :real \n/= ratio :real\n")
                while True:
                    line = file1.readline()
                    file2.write(line)
                    if not line:
                        break
                file1.close()
                file2.close()
            sg.popup_ok('Новые файлы успешно сформированны')
        elif values['radio3'] == True:
            new_listfiles = values['tblfile'].split(',')
            for i in range (lnght):
                name_file1 = listfiles[i]
                name_file2 = new_listfiles[i]
                name_file2 = name_file2.replace("[","")
                name_file2 = name_file2.replace("]","")
                name_file2 = name_file2.replace("'","")
                name_file2 = name_file2.replace(" ","")
                print(name_file2)
                file1 = open(name_file1,'r')
                file2 = open(name_file2,'w')
                file2.write("/= Q :real\n/= Date :real\n/= GMS :real\n/= QQ :real\n/= TimeUS :real\n/= QQQ :real\n")
                file2.write("/= RFND :real\n/= QQQQQ :real\n/= QQQQQQ :real\n")
                while True:
                    line = file1.readline()
                    line = line.replace(","," ")
                    file2.write(line)
                    if not line:
                        break
                file1.close()
                file2.close()
            sg.popup_ok('Новые файлы успешно сформированны')
        elif values['radio2'] == True:
            new_listfiles = values['tblfile'].split(',')
            for i in range (lnght):
                name_file1 = listfiles[i]
                name_file2 = new_listfiles[i]
                name_file2 = name_file2.replace("[","")
                name_file2 = name_file2.replace("]","")
                name_file2 = name_file2.replace("'","")
                name_file2 = name_file2.replace(" ","")
                print(name_file2)
                file1 = open(name_file1,'r')
                file2 = open(name_file2,'w')
                file2.write("/= Q :real\n/= Date :real\n/= GMS :real\n/= QQ :real\n/= TimeUS :real\n/= QQQ :real\n")
                file2.write("/= GMS_sec :real\n/= GMS_week :real\n/= QQQQ :real\n/= QQQQQ :real\n/= lat :real\n")
                file2.write("/= lon :real\n/= H :real\n/= QQQQQQ :real\n/= QQQQQQQ :real\n/= QQQQQQQQ :real\n")
                file2.write("/= QQQQQQQQQ :real\n/= QQQQQQQQQQ :real\n/= QQQQQQQQQQQ :real\n")
                while True:
                    line = file1.readline()
                    line = line.replace(","," ")
                    file2.write(line)
                    if not line:
                        break
                file1.close()
                file2.close()
            sg.popup_ok('Новые файлы успешно сформированны')
        else: 
            sg.popup_error('Ошибка: Выберите тип преобразования')   
        


    
    if event == 'gen2':
        fb2 = str(values['fb2'])
        fb2 = fb2.replace('.XYZ','.txt')
        window['xyzfile_output'].update(fb2)

    if event == 'xyz_par':
        name_file3 = values['xyzfile_input']
        num_lines = sum(1 for line in open(name_file3, 'r'))
        sum_dif_dist = 0
        rare_origin = open(name_file3)
        r = rare_origin.readlines()
        steps = int(values['numpoints_xyz'])
        for i in range (num_lines-1):
            el1 = r[i]
            el2 = r[i+1]
            x1 = float(el1.split()[0])
            y1 = float(el1.split()[1])
            x2= float(el2.split()[0])
            y2 = float(el2.split()[1])
            dif_x = abs(x2-x1)
            dif_y = abs(y2-y1)
            dif_dist = round(math.sqrt(dif_x*dif_x+dif_y*dif_y),2)
            sum_dif_dist += dif_dist
        step_dist = sum_dif_dist/steps
        window['dbp'].update(step_dist)

    if event == 'new_ascii':
        name_file3 = values['xyzfile_input']
        rare_origin = open(name_file3)
        r = rare_origin.readlines()
        name_file4 = values['xyzfile_output']
        num_lines = sum(1 for line in open(name_file3, 'r'))
        file_rarz_ex = open(name_file4,'w')
        file_rarz_ex.write(r[0])
        for i in range(num_lines-1):
            el1 = r[i]
            el2 = r[i+1]
            x1 = float(el1.split()[0])
            y1 = float(el1.split()[1])
            x2= float(el2.split()[0])
            y2 = float(el2.split()[1])
            dif_x = (x2-x1)
            dif_y = (y2-y1)
            dif_dist = round(math.sqrt(dif_x*dif_x+dif_y*dif_y),2)
            steps_per_point = int(steps*(dif_dist/sum_dif_dist))
            x_step = dif_x/steps_per_point
            y_step = dif_y/steps_per_point
            print (steps_per_point)
            for j in range(steps_per_point-1):
                x3 = round(x1+(j+1)*x_step,6)
                y3 = round(y1+(j+1)*y_step,6)
                file_rarz_ex.write(str(x3));file_rarz_ex.write(' ');file_rarz_ex.write(str(y3));file_rarz_ex.write('\n')
            file_rarz_ex.write(str(x2));file_rarz_ex.write(' ');file_rarz_ex.write(str(y2));file_rarz_ex.write('\n') 
        file_rarz_ex.close()

window.close()


