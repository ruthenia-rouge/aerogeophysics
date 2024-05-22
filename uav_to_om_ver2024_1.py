import math as math
import PySimpleGUI as sg
from geopy import distance
import time

sg.theme('LightBlue2')

ptt = [
    [sg.Radio('.pos в .tbl (гондола)','OPTYPE',default=False,key = 'radio1'),sg.Radio('Добавить заголовок GPS (коптер)','OPTYPE',default=False, key = 'radio2'),
    sg.Radio('Добавить заголовок RFND (коптер)','OPTYPE',default=False, key ='radio3' )],
    [sg.Text('Исходные файлы'),sg.FilesBrowse('Поиск файлов', key = 'fbpos',target='hidden'),
    sg.Text('.tbl файлы',size = (60,1),justification='r'),sg.Button('Преобразовать файлы', key = 'transform')],
    [sg.Multiline(size = (60,10), key = 'input_files'),sg.Input(key = 'hidden',visible=False, enable_events=True),
    sg.Button('Генерация имени файла', key = 'gen1'),sg.Multiline(size = (60,10), key = 'tblfile')],
]

xyz_rai = [
    [sg.Radio('Для файлов OM - прямоуг. коорд.','OPTYPE2',default = True, key = 'radom'),sg.Radio('Для файлов MisPlan','OPTYPE2',default = False, key = 'radmp')],
    [sg.Text('Исходный файл, требующий разряжения и интерполяции')],
    [sg.Input(key = 'xyzfile_input',size = (100,1)),sg.FileBrowse('Поиск файла', key = 'fb2')],
    [sg.Text('Параметры:')],
    [sg.Text('Расстояние между точками, (м)'),sg.Text('_', key = 'dbp'),sg.Text('Число точек'),sg.Input(key = 'numpoints_xyz',size = (4,1)),sg.Button('Расчет параметров',key = 'xyz_par')],
    [sg.Text('Конечный файл')],
    [sg.Input(key = 'xyzfile_output',size = (100,1)),sg.Button('Генерация имени файла', key = 'gen2')],
    [sg.Button('Создать разряженный .txt', key = 'new_ascii')]
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
        listfiles_ = ''
        for i in range(lnght):
            listfiles_ += listfiles[i]
            listfiles_ += '\n'
        window['input_files'].update(listfiles_)

    if event == 'gen1':
        new_onefile =  listfiles[0].rsplit('/',1)[0] +'/' + str(time.gmtime()[2])+'_'+str(time.gmtime()[1])
        new_listfiles = []
        if values['radio1'] == True:
            listfiles_ = listfiles_.replace('.pos','.tbl')
            new_onefile = new_onefile +'_sensor.tbl'
        elif values['radio2'] == True:
            listfiles_ = listfiles_.replace('.tbl','_gps.tbl')
            new_onefile = new_onefile +'_gps.tbl'
        elif values['radio3']== True:
            listfiles_ = listfiles_.replace('.tbl','_rfnd.tbl')
            new_onefile = new_onefile +'_rfnd.tbl'
        else:
            name_file2 = 'Нет новых файлов'
            sg.popup_error('Ошибка: Выберите тип преобразования')            
        window['tblfile'].update(new_onefile)


    if event == 'transform':
        new_onefile  = values['tblfile']
        if values['radio1'] == True:
            for i in range (lnght):
                name_file1 = listfiles[i]
                name_file2 = new_onefile 
                file1 = open(name_file1,'r')
                if i == 0:
                    file2 = open(name_file2,'w')
                else:
                    file2 = open(name_file2,'a')
                j = 0
                while j < 24 :
                    j += 1
                    line = file1.readline()
                if i == 0:
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
            sg.popup_ok('Новый файл успешно сформированн')
        elif values['radio3'] == True:
            for i in range (lnght):
                name_file1 = listfiles[i]
                name_file2 = new_onefile 
                file1 = open(name_file1,'r')
                if i == 0:
                    file2 = open(name_file2,'w')
                else:
                    file2 = open(name_file2,'a')
                if i== 0:    
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
            sg.popup_ok('Новый файл успешно сформированн')
        elif values['radio2'] == True:
            for i in range (lnght):
                name_file1 = listfiles[i]
                name_file2 = new_onefile 
                file1 = open(name_file1,'r')
                if i == 0:
                    file2 = open(name_file2,'w')
                else:
                    file2 = open(name_file2,'a')
                if i== 0:   
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
            sg.popup_ok('Новый файл успешно сформированн')
        else: 
            sg.popup_error('Ошибка: Выберите тип преобразования')   
        
    
    if (event == 'gen2' and values['radmp'] == True):
        fb2 = str(values['fb2'])
        fb2 = fb2.replace('.waypoints','.txt')
        fb2 = fb2.replace('.txt','_new.txt')        
        window['xyzfile_output'].update(fb2)
    elif(event == 'gen2' and values['radmp'] == False):
        fb2 = str(values['fb2'])
        fb2 = fb2.replace('.XYZ','.txt')
        window['xyzfile_output'].update(fb2)

    
    if event == 'xyz_par':
        name_file3 = values['xyzfile_input']
        num_lines = sum(1 for line in open(name_file3, 'r'))
        sum_dif_dist = 0
        sum_disp_dif_dist = 0
        rare_origin = open(name_file3)
        r = rare_origin.readlines()
        steps = int(values['numpoints_xyz'])
        if (values['radmp'] == False):
            for i in range (num_lines-1):
                el1 = r[i]
                el2 = r[i+1]
                x1 = float(el1.split()[0])
                y1 = float(el1.split()[1])
                x2= float(el2.split()[0])
                y2 = float(el2.split()[1])
                dif_x = abs(x2-x1)
                dif_y = abs(y2-y1)
                dif_dist = round(math.sqrt(dif_x*dif_x+dif_y*dif_y),6)
                if values['radom'] == True:
                    disp_dif_dist = round(math.sqrt(dif_x*dif_x+dif_y*dif_y),6)
                sum_dif_dist += dif_dist
                sum_disp_dif_dist  += disp_dif_dist
            step_dist = sum_dif_dist/steps
            displ_step_dist = sum_disp_dif_dist/steps
            window['dbp'].update(displ_step_dist)
        else:
            for i in range (2, num_lines-1):
                el1 = r[i]
                el2 = r[i+1]
                x1 = float(el1.split()[8])
                y1 = float(el1.split()[9])
                x2= float(el2.split()[8])
                y2 = float(el2.split()[9])
                dif_x = abs(x2-x1)
                dif_y = abs(y2-y1)
                dif_dist = round(math.sqrt(dif_x*dif_x+dif_y*dif_y),12)
                latlon1 = (x1,y1)
                latlon2 = (x2,y2)
                disp_dif_dist = distance.distance(latlon1, latlon2).meters
                sum_dif_dist += dif_dist
                sum_disp_dif_dist  += disp_dif_dist
            step_dist = sum_dif_dist/steps
            displ_step_dist = sum_disp_dif_dist/steps
            window['dbp'].update(displ_step_dist)                

    if event == 'new_ascii':
        name_file3 = values['xyzfile_input']
        rare_origin = open(name_file3)
        r = rare_origin.readlines()
        name_file4 = values['xyzfile_output']
        num_lines = sum(1 for line in open(name_file3, 'r'))
        file_rarz_ex = open(name_file4,'w')
        if (values['radmp'] == False):
            file_rarz_ex.write('X Y N \n')   
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
                dif_dist = math.sqrt(dif_x*dif_x+dif_y*dif_y)
                steps_per_point = steps*(dif_dist/sum_dif_dist)
                x_step = dif_x/steps_per_point
                y_step = dif_y/steps_per_point
                print (steps_per_point)
                for j in range(int(steps_per_point)):
                    x3 = x1+(j+1)*x_step
                    y3 = y1+(j+1)*y_step
                    file_rarz_ex.write(str(x3));file_rarz_ex.write(' ');file_rarz_ex.write(str(y3));file_rarz_ex.write('\n')
                file_rarz_ex.write(str(x2));file_rarz_ex.write(' ');file_rarz_ex.write(str(y2));file_rarz_ex.write('\n') 
        else:
            file_rarz_ex.write('Lat Lon N \n')                        
            temp_string = str(r[2].split()[8]) + ' ' + str(r[2].split()[9]) + ' 1\n'
            file_rarz_ex.write(temp_string)
            k = 1
            sum_disp_dif_dist = 0
            for i in range (1, num_lines-1):
                el1 = r[i]
                el2 = r[i+1]
                x1 = float(el1.split()[8])
                y1 = float(el1.split()[9])
                x2= float(el2.split()[8])
                y2 = float(el2.split()[9])
                dif_x = (x2-x1)
                dif_y = (y2-y1)
                latlon1 = (x1,y1)
                latlon2 = (x2,y2)
                disp_dif_dist = distance.distance(latlon1, latlon2).meters
                sum_disp_dif_dist  += disp_dif_dist
            for i in range (1,num_lines-1):
                el1 = r[i]
                el2 = r[i+1]
                x1 = float(el1.split()[8])
                y1 = float(el1.split()[9])
                x2= float(el2.split()[8])
                y2 = float(el2.split()[9])
                latlon1 = (x1,y1)
                latlon2 = (x2,y2)
                disp_dif_dist = distance.distance(latlon1, latlon2).meters
                percent = disp_dif_dist/sum_disp_dif_dist
                num_steps=percent*steps
                print(percent)
                step_x = (x2-x1)/num_steps
                step_y = (y2-y1)/num_steps
                for j in range (1,int(num_steps)+1):
                    x3 = x1+j*step_x
                    y3 = y1+j*step_y
                    k+=1
                    file_rarz_ex.write(str(x3));file_rarz_ex.write(' ');file_rarz_ex.write(str(y3));file_rarz_ex.write(' ');file_rarz_ex.write(str(k));file_rarz_ex.write('\n')
                k+=1
                file_rarz_ex.write(str(x2));file_rarz_ex.write(' ');file_rarz_ex.write(str(y2));file_rarz_ex.write(' ');file_rarz_ex.write(str(k));file_rarz_ex.write('\n')        
        file_rarz_ex.close()
        sg.popup_ok('Новый файл успешно разряжен')


window.close()


