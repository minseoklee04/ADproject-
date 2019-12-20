import unittest

from game.ADgame import *

class TestADgame(unittest.TestCase):

    def setUp(self):
        self.myunit = Myunit()
        self.subunit = SubUnit()
        self.enemy = Enemy()
        self.item = Item()
        self.boss = Boss()


    def tearDown(self):
        pass

    def testMyunitInitialvalue(self):
        self.assertEqual(self.myunit.size, 15)
        self.assertEqual(self.myunit.life, 3)
        self.assertEqual(self.myunit.score, 0)
        self.assertEqual(self.myunit.color, QColor(255,255,255,255))
        self.assertEqual(self.myunit.bullet, [])
        self.assertEqual(self.myunit.itemlist, [])

    def testSubunitInitialvalue(self):
        self.assertEqual(self.subunit.bullet, [])
        self.assertEqual(self.subunit.color, QColor(0,0,255,255))
        self.assertEqual(self.subunit.rect.width(), 8)
        self.assertEqual(self.subunit.rect.height(), 8)

    def testEnemyInitialvalue(self):
        self.assertEqual(self.enemy.color, QColor(255,0,0,255))
        self.assertEqual(self.enemy.size, 15)

    def testItemInitialvalue(self):
        self.assertEqual(self.item.size, 15)
        self.assertIn(self.item.random_item, [(255, 0, 255), (0, 0, 255), (255, 255, 255)])
        r, g, b = self.item.random_item
        self.assertEqual(self.item.color, QColor(r,g,b))

    def testBossInitialvalue(self):
        self.assertEqual(self.boss.color, QColor(255,255,0,255))
        self.assertEqual(self.boss.rect.width(), 200)
        self.assertEqual(self.boss.rect.height(), 100)
        self.assertEqual(self.boss.life, 200)
        self.assertFalse(self.boss.Bossposition)
        
 ## 저희는 대부분의 코드 구현을 PlayGame 클래스 에서 구현을 해서 PlayGame 객체를 만들어야 하는데 객체를 만드는 부분에
## thread 함수를 실행시키는 부분이 들어가 있어서 객체생성이 실행되면 thread가 같이 돌아가서 단위테스트 진행이 되지 않습니다...
## 죄송합니다.
