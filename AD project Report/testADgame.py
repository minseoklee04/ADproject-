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
