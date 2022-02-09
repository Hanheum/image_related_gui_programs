import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from threading import Thread
from time import sleep

image_dir = ''
image_list = []
#image_count = 0
locations = []
savecount = 0
flag = 0
save_dir = ''
click_count = 0
start_point = 0
mode = 0

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global UI_set, locations
        UI_set = QtUiTools.QUiLoader().load(resource_path("image_cutter.ui"))
        UI_set.quit_log.setText('PLEASE PRESS QUIT BUTTON FIRST')
        self.click_log_manager()

        UI_set.OK.clicked.connect(self.read_dir_list)
        UI_set.quiter.clicked.connect(self.ender)
        UI_set.save_OK.clicked.connect(self.read_save_dir)
        UI_set.start_point_ok.clicked.connect(self.set_start_point)
        UI_set.image_count_OK.clicked.connect(self.set_image_count)

        self.setWindowIcon(QtGui.QPixmap(resource_path("./logo.png")))
        self.setCentralWidget(UI_set)
        self.setWindowTitle("IMAGE CUTTER")
        self.resize(1700, 1010)
        self.show()

    def set_image_count(self):
        global image_count
        image_count = int(UI_set.image_count.toPlainText())-1

    def set_start_point(self):
        global start_point
        start_point = int(UI_set.start_point.toPlainText())

    def ender(self):
        global flag
        flag = 1
        UI_set.quit_log.setText('NOW YOU CAN PRESS X')

    def read_save_dir(self):
        global save_dir
        txt = UI_set.save_dir_select.toPlainText()
        save_dir = txt
        UI_set.save_log.setText('SAVE DIRECTORY SELECTED')

    def change_button_status(self):
        global button_status
        button_status = 1

    def read_dir_list(self):
        global image_dir
        UI_set.log.setText('IMAGE DIRECTORY SELECTED')
        txt = UI_set.dir_select.toPlainText()
        image_dir = txt
        self.image_list_generator(image_list, image_dir)

    def pop_up_images(self):
        UI_set.image_log.setText('')
        global image_count, image_dir, image_list
        try:
            pixmap = QtGui.QPixmap(image_dir + '/' + image_list[image_count])
            UI_set.image_blank.setPixmap(pixmap)
            UI_set.image_blank.setScaledContents(True)

            image_count += 1

            UI_set.COUNT.setText('{}/{}'.format(image_count, len(image_list)))
        except:
            if image_count >= len(image_list):
                UI_set.image_log.setText('NO MORE IMAGES')
            else:
                UI_set.image_log.setText('ERROR')



    def image_list_generator(self, save, dir):
        try:
            the_list = os.listdir(dir)
            for i in range(len(the_list)):
                save.append(the_list[i])

            UI_set.next_button.clicked.connect(self.pop_up_images)

        except:
            UI_set.log.setText('ERROR')

    def mousePressEvent(self, event):
        global click_count, mode
        '''p = event.pos()  # relative to widget
        gp = self.mapToGlobal(p)  # relative to screen
        rw = self.window().mapFromGlobal(gp)  # relative to window
        rw = str(rw)
        strings1 = rw.split('(')
        rw = strings1[1]
        strings2 = rw.split(')')
        rw = strings2[0]
        strings3 = rw.split(', ')
        x, y = int(strings3[0]), int(strings3[1])
        if x>=310 and x<=1010 and y>=30 and y<=730:
            coordinates = [x-310, y-30]
            locations.append(coordinates)
            if click_count==2:
                click_count = 0
                #self.click_log_manager_0()
            click_count += 1
            self.click_log_manager()'''
        if mode == 0:
            mode = 1
            UI_set.mode.setText('drawing')
        elif mode == 1:
            mode = 2
            UI_set.mode.setText('not drawing')


    def save_flag_manager(self):
        UI_set.image_log.setText('SAVED')
        sleep(0.3)
        UI_set.image_log.setText('')

    def click_log_manager(self):
        global click_count
        UI_set.how_many_click.setText('CLICK COUNT:{}'.format(click_count))

    '''def click_log_manager_0(self):
        UI_set.how_many_click.setText('CLICK COUNT:{}'.format(0))'''


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

def drag_a_line():
    global locations, mode
    loc = QtGui.QCursor().pos()
    loc = main.window().mapFromGlobal(loc)
    x = loc.x()
    y = loc.y()
    if x >= 310 and x <= 1010 and y >= 30 and y <= 730 :
        if mode == 1:
            coordinates = [x - 310, y - 30]
            print(coordinates)
            try:
                locations.index(coordinates)
            except:
                locations.append(coordinates)
        elif mode == 2:
            location_text = str(locations)
            file = open(save_dir, 'a')
            file.write(image_dir+'\\'+image_list[image_count-1]+'\n')
            file.write(location_text+'\n')
            locations = []
            mode = 0

def main_thing():
    global flag, main
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        main = MainView()

        # main.show()
        sys.exit(app.exec_())



def sub_thing():
    global locations, image_dir, image_list, image_count, savecount, flag, saving_flag, main, click_count
    while True:
        drag_a_line()
        '''if len(locations) == 2:
            image = Image.open(image_dir + '/' + image_list[image_count-1]).convert('RGB')
            image = image.resize((700, 700))
            x1, y1 = locations[0][0], locations[0][1]
            x2, y2 = locations[1][0], locations[1][1]
            if x1 < x2:
                xbegin = x1
                xend = x2
            else:
                xbegin = x2
                xend = x1

            if y1 < y2:
                ybegin = y1
                yend = y2
            else:
                ybegin = y2
                yend = y1

            image = image.crop((xbegin, ybegin, xend, yend))
            image.save(save_dir+'\\{}.jpg'.format(savecount + 1 + start_point))
            main.save_flag_manager()
            savecount += 1

            #main.click_log_manager_0()

            locations = []'''

        if not flag==0:
            break

main_thread = Thread(target=main_thing)
sub_thread = Thread(target=sub_thing)
main_thread.start()
sleep(1)
sub_thread.start()

