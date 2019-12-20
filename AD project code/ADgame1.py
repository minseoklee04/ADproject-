from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import *
import threading
import time


class Unit:
    size = 15

    def __init__(self):
        self.rect = QRect()
        self.color = QColor(0, 0, 0)


class Myunit(Unit):
    def __init__(self):
        super().__init__()
        self.life = 3
        self.score = 0
        self.color.setRgb(255, 255, 255, 255)
        self.bullet = []
        self.itemlist = []

class SubUnit():
    def __init__(self):
        self.rect = QRect()
        self.color = QColor(0, 0, 0)
        self.color.setRgb(0, 0, 255, 255)
        self.rect.setWidth(8)
        self.rect.setHeight(8)
        self.bullet = []

class Item(Unit):
    def __init__(self):
        super().__init__()
        self.random_item = choice([(255, 0, 255), (0, 0, 255), (255, 255, 255)])
        r, g, b = self.random_item
        self.color.setRgb(r, g, b)



class Enemy(Unit):
    def __init__(self):
        super().__init__()
        self.color.setRgb(255, 0, 0)

class Boss:
    def __init__(self):
        self.rect = QRect()
        self.color = QColor(0,0,0)
        self.color.setRgb(255,255,0,255)
        self.rect.setWidth(200)
        self.rect.setHeight(100)
        self.life = 200
        self.Bossposition = False

    def __del__(self):
        pass


class PlayGame:

    def __init__(self, parent):
        self.start_time = time.time()
        self.parent = parent
        self.myunit = Myunit()
        self.enemy = []
        self.item = []
        self.E = threading.Lock()
        self.B = threading.Lock()
        self.I = threading.Lock()
        self.bossone = 0
        self.gameover = False
        self.sub = False
        self.unit2 = False

        self.Game()

    def __del__(self):
        pass

    def Game(self):

        size = Unit.size

        self.myunit.rect.setRect(192, 600, size, size)

        t1 = threading.Thread(target=self.createEnemy)
        t2 = threading.Thread(target=self.moveEnemy)
        t3 = threading.Thread(target=self.moveBullet)
        t4 = threading.Thread(target=self.createItem)
        t5 = threading.Thread(target=self.moveItem)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

    def exitGame(self):
        self.gameover = True

    def createEnemy(self):
        while not self.gameover and self.bossone != 1:

            if time.time() - self.start_time > 180:
                self.boss = Boss()
                self.boss.rect.setRect(100, 0, 200, 100)
                self.bossone += 1

            elif randint(1, 7) == 1:
                rect = self.parent.rect()
                size = Unit.size
                enemy = Enemy()
                x = randint(0, rect.width())
                enemy.rect.setRect(x, 0, size, size)
                self.E.acquire()
                self.enemy.append(enemy)
                self.E.release()

            time.sleep(0.1)

    def moveEnemy(self):
        while not self.gameover:
            self.E.acquire()
            k = 0
            if self.bossone != 1:
                for i in self.enemy[:]:
                    if i.rect.y() > self.parent.rect().bottom():
                        del (self.enemy[k])
                    elif i.rect.intersects(self.myunit.rect):
                        del (self.enemy[k])
                        self.myunit.life -= 1
                        if self.myunit.life == 0:
                            self.gameover = True
                    else:
                        self.enemy[k].rect.adjust(0, 2, 0, 2)
                        k += 1

            else:
                self.enemy.clear()
                if self.boss.rect.intersects(self.myunit.rect):
                    self.myunit.life -= 1
                elif self.boss.Bossposition == False:
                    self.boss.rect.adjust(0, 1, 0, 1)
                if self.boss.rect.bottom() == 300:
                    self.boss.Bossposition = True

            self.E.release()

            self.parent.update()
            time.sleep(0.01)

    def moveBullet(self):

        while not self.gameover:
            k = 0
            self.B.acquire()
            for i in self.myunit.bullet[:]:
                if i.y() < self.parent.rect().y():
                    del (self.myunit.bullet[k])
                else:
                    e = 0
                    crash = False
                    self.E.acquire()
                    if self.bossone != 1:
                        for j in self.enemy[:]:
                            if j.rect.intersects(i):
                                crash = True
                                del (self.myunit.bullet[k])
                                del (self.enemy[e])
                                self.myunit.score += 1
                                break
                            else:
                                e += 1
                    else:
                        if self.boss.rect.intersects(i):
                            crash = True
                            del (self.myunit.bullet[k])
                            self.boss.life -= 1
                            if self.boss.life == 0:
                                self.myunit.score += 100
                                self.gameover = True

                    self.E.release()
                    if crash:
                        break

                    else:
                        self.myunit.bullet[k].adjust(0, -2, 0, -2)
                        k += 1


            if self.unit2 == True:
                k2 = 0

                for i in self.myunit2.bullet[:]:
                    if i.y() < self.parent.rect().y():
                        del (self.myunit2.bullet[k2])
                    else:
                        e2 = 0
                        crash2 = False
                        self.E.acquire()
                        if self.bossone != 1:
                            for j in self.enemy[:]:
                                if j.rect.intersects(i):
                                    crash2 = True
                                    del (self.myunit2.bullet[k2])
                                    del (self.enemy[e2])
                                    self.myunit.score += 1
                                    break
                                else:
                                    e2 += 1
                        else:
                            if self.boss.rect.intersects(i):
                                crash2 = True
                                del (self.myunit2.bullet[k2])
                                self.boss.life -= 1
                                if self.boss.life == 0:
                                    self.myunit.score += 100
                                    self.gameover = True
                        self.E.release()

                        if crash2:
                            break
                        else:
                            self.myunit2.bullet[k2].adjust(0, -2, 0, -2)
                            k2 += 1


            if self.sub == True:
                k3 = 0

                for i in self.l_sub.bullet[:]:
                    if i.y() < self.parent.rect().y():
                        del (self.l_sub.bullet[k3])
                    else:
                        e3 = 0
                        crash3 = False
                        self.E.acquire()
                        if self.bossone != 1:
                            for j in self.enemy[:]:
                                if j.rect.intersects(i):
                                    crash3 = True
                                    del (self.l_sub.bullet[k3])
                                    del (self.enemy[e3])
                                    self.myunit.score += 1
                                    break
                                else:
                                    e3 += 1
                        else:
                            if self.boss.rect.intersects(i):
                                crash3 = True
                                del (self.l_sub.bullet[k3])
                                self.boss.life -= 1
                                if self.boss.life == 0:
                                    self.myunit.score += 100
                                    self.gameover = True
                        self.E.release()

                        if crash3:
                            break
                        else:
                            self.l_sub.bullet[k3].adjust(0, -2, 0, -2)
                            k3 += 1
                k4 = 0

                for i in self.r_sub.bullet[:]:
                    if i.y() < self.parent.rect().y():
                        del (self.r_sub.bullet[k4])
                    else:
                        e4 = 0
                        crash4 = False
                        self.E.acquire()
                        if self.bossone != 1:
                            for j in self.enemy[:]:
                                if j.rect.intersects(i):
                                    crash4 = True
                                    del (self.r_sub.bullet[k4])
                                    del (self.enemy[e4])
                                    self.myunit.score += 1
                                    break
                                else:
                                    e4 += 1
                        else:
                            if self.boss.rect.intersects(i):
                                crash4 = True
                                del (self.r_sub.bullet[k4])
                                self.boss.life -= 1
                                if self.boss.life == 0:
                                    self.myunit.score += 100
                                    self.gameover = True
                        self.E.release()

                        if crash4:
                            break
                        else:
                            self.r_sub.bullet[k4].adjust(0, -2, 0, -2)
                            k4 += 1
            self.B.release()

            self.parent.update()
            time.sleep(0.01)

    def createItem(self):
        while not self.gameover:
            if time.time() - self.start_time > 60:
                if randint(1, 100) == 1:
                    rect = self.parent.rect()
                    size = Unit.size
                    item = Item()
                    x = randint(0, rect.width())
                    item.rect.setRect(x, 0, size, size)
                    self.I.acquire()
                    self.item.append(item)
                    self.I.release()

                time.sleep(0.1)

    def moveItem(self):
        while not self.gameover:
            self.I.acquire()
            k = 0
            for i in self.item[:]:
                if i.rect.y() > self.parent.rect().bottom():
                    del (self.item[k])
                elif i.rect.intersects(self.myunit.rect):
                    if i.random_item == (255, 0, 255):
                        self.myunit.life += 1
                    elif i.random_item not in self.myunit.itemlist:
                        self.myunit.itemlist.append(i.random_item)
                        if i.random_item == (0, 0, 255):
                            self.l_sub = SubUnit()
                            self.r_sub = SubUnit()
                            self.l_sub.rect.setRect(self.myunit.rect.left() - 10, self.myunit.rect.top() + 3,
                                                    self.l_sub.rect.height(), self.l_sub.rect.width())
                            if self.unit2 == True:
                                self.r_sub.rect.setRect(self.myunit2.rect.right() + 2, self.myunit2.rect.top() + 3,
                                                        self.r_sub.rect.height(), self.r_sub.rect.width())
                            else:
                                self.r_sub.rect.setRect(self.myunit.rect.right() + 2, self.myunit.rect.top() + 3,
                                                        self.r_sub.rect.height(), self.r_sub.rect.width())
                            self.sub = True
                        else:
                            self.myunit2 = Myunit()
                            self.myunit2.rect.setRect(self.myunit.rect.right(), self.myunit.rect.top(),
                                                      self.myunit.size, self.myunit.size)
                            self.unit2 = True
                    del (self.item[k])
                else:
                    self.item[k].rect.adjust(0, 2, 0, 2)
                    k += 1

            self.I.release()

            self.parent.update()
            time.sleep(0.01)


    def draw(self, qp):
        qp.setPen(QColor(255, 255, 255))
        qp.drawText(self.parent.rect(),
                    Qt.AlignLeft | Qt.AlignTop, 'HP:' + str(self.myunit.life))
        qp.drawText(self.parent.rect(),
                    Qt.AlignRight | Qt.AlignTop, 'Score: ' + str(self.myunit.score))

        if self.gameover == True:
            if self.myunit.life == 0:
                qp.setFont(QFont('나눔명조', 20))
                qp.drawText(self.parent.rect(),
                            Qt.AlignCenter | Qt.AlignCenter, 'Game over.\nyour score is ' + str(self.myunit.score))

            elif self.boss.life == 0:
                qp.setFont(QFont('나눔명조', 20))
                qp.drawText(self.parent.rect(),
                        Qt.AlignCenter | Qt.AlignCenter, 'Boss Clear.\nyour score is ' + str(self.myunit.score))

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(self.myunit.color)
        qp.drawRect(self.myunit.rect)

        self.E.acquire()
        for i in self.enemy:
            qp.setBrush(i.color)
            qp.drawRect(i.rect)
        self.E.release()

        self.B.acquire()
        for i in self.myunit.bullet:
            qp.setBrush(QColor(255, 255, 255))
            qp.drawEllipse(i)
        if self.unit2 == True:
            for i in self.myunit2.bullet:
                qp.setBrush(QColor(255, 255, 255))
                qp.drawEllipse(i)
        if self.sub == True:
            for i in self.r_sub.bullet:
                qp.setBrush(QColor(255, 255, 255))
                qp.drawEllipse(i)
            for i in self.l_sub.bullet:
                qp.setBrush(QColor(255, 255, 255))
                qp.drawEllipse(i)
        self.B.release()



        self.I.acquire()
        for i in self.item:
            qp.setBrush(i.color)
            qp.drawRect(i.rect)
        self.I.release()

        if self.bossone == 1:
            qp.setBrush(self.boss.color)
            qp.drawRect(self.boss.rect)

        if self.sub == True:
            qp.setBrush(self.l_sub.color)
            qp.drawRect(self.l_sub.rect)
            qp.setBrush(self.r_sub.color)
            qp.drawRect(self.r_sub.rect)

        if self.unit2 == True:
            qp.setBrush(self.myunit2.color)
            qp.drawRect(self.myunit2.rect)

    def keyDown(self, key):

        speed = 10
        if self.myunit.rect.left() > 20 and key == Qt.Key_Left:
            self.myunit.rect.adjust(-speed, 0, -speed, 0)
            if self.unit2 == True:
                self.myunit2.rect.adjust(-speed, 0, -speed, 0)
            if self.sub == True:
                self.l_sub.rect.adjust(-speed, 0, -speed, 0)
                self.r_sub.rect.adjust(-speed, 0, -speed, 0)

        elif self.myunit.rect.right() < 364 and key == Qt.Key_Right:
            self.myunit.rect.adjust(speed, 0, speed, 0)
            if self.unit2 == True:
                self.myunit2.rect.adjust(speed, 0, speed, 0)
            if self.sub == True:
                self.l_sub.rect.adjust(speed, 0, speed, 0)
                self.r_sub.rect.adjust(speed, 0, speed, 0)

        elif self.myunit.rect.top() > 200 and key == Qt.Key_Up:
            self.myunit.rect.adjust(0, -speed, 0, -speed)
            if self.unit2 == True:
                self.myunit2.rect.adjust(0, -speed, 0, -speed)
            if self.sub == True:
                self.l_sub.rect.adjust(0, -speed, 0, -speed)
                self.r_sub.rect.adjust(0, -speed, 0, -speed)

        elif self.myunit.rect.bottom() < 684 and key == Qt.Key_Down:
            self.myunit.rect.adjust(0, speed, 0, speed)
            if self.unit2 == True:
                self.myunit2.rect.adjust(0, speed, 0, speed)
            if self.sub == True:
                self.l_sub.rect.adjust(0, speed, 0, speed)
                self.r_sub.rect.adjust(0, speed, 0, speed)

        elif key == Qt.Key_Space:
            rect = QRect(self.myunit.rect)
            if self.unit2 == True:
                rect2 = QRect(self.myunit2.rect)
                self.myunit2.bullet.append(rect2)
            if self.sub == True:
                rect3 = QRect(self.l_sub.rect)
                rect4 = QRect(self.r_sub.rect)
                self.l_sub.bullet.append(rect3)
                self.r_sub.bullet.append(rect4)
            self.myunit.bullet.append(rect)

        self.parent.update()

