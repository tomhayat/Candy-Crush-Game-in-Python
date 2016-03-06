#!/usr/bin/python
# -*- coding: utf-8 -*-



import jeu_et_regle
import sys
from PyQt4 import QtGui, QtCore


        
class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.game = jeu_et_regle.GrilleJeu()
        self.btn = [[QtGui.QPushButton('', self)
                    for j in range(len(self.game.grille))]
                    for i in range(len(self.game.grille))]             
        self.icone_dic = {1 : 'icones/1.png',
                          2 : 'icones/2.png',
                          3 : 'icones/3.png',
                          4 : 'icones/4.png',
                          5 : 'icones/5.png',
                          6 : 'icones/6.png',
                          7 : 'icones/7.png',
                          } 
        self.initUI()
        self.click = []

                          
    def refresh_grille(self):        
        for j in range(len(self.game.grille)):
            for i in range(len(self.game.grille)):
                self.btn[i][j].setText('')
                self.set_icon(i,j)
        self.movesLabel.setText(str(self.game.moves))
        self.scoreLabel.setText(str(self.game.score))
        
    def buttonconnect(self):          
        for i in range(len(self.game.grille)):
            for j in range(len(self.game.grille)):
               self.btn[i][j].clicked.connect(self.buttonClicked) 
               self.btn[i][j].value = [i,j]

    def affiche_grille(self):  
        for i in range(len(self.game.grille)):
            for j in range(len(self.game.grille)):
                self.btn[i][j].setFixedSize(50, 50)
                self.btn[i][j].move(50*(j + 1), 50*(i + 1))
                self.set_icon(i,j)
    def set_icon(self,i,j):
        self.btn[i][j].setIcon(QtGui.QIcon(
                                    self.icone_dic[self.game.get_item(i,j)]))
    def initUI(self):
        self.buttonconnect()
        self.statusBar()
        self.affiche_grille()
        # Score
        score = QtGui.QLabel('<b>' + 'Score' + '</b>', self)
        score.move(460, 50)
        self.scoreLabel = QtGui.QLabel(str(self.game.score), self)
        self.scoreLabel.move(520, 50)
        
        # Moves 50 en y
        Moves = QtGui.QLabel('<b>' + 'Moves' + '</b>', self)
        Moves.move(460, 100)
        self.movesLabel = QtGui.QLabel(str(self.game.moves), self)
        self.movesLabel.move(520, 100)
        
        # reset button
        self.btn_reset = QtGui.QPushButton('Reset', self)
        self.btn_reset.move(450, 150)
        self.btn_reset.setFixedSize(100, 30)
        self.btn_reset.clicked.connect(self.Reset) 
        
        # Quit button
        self.btn_reset = QtGui.QPushButton('Quit', self)
        self.btn_reset.move(450, 180)
        self.btn_reset.setFixedSize(100, 30)
        self.btn_reset.clicked.connect(self.close) 
        
        # window
        self.setGeometry(220, 200, 590, 500)
        self.setWindowTitle('Match3')
        self.show()
        
    def Reset(self):
        self.game = jeu_et_regle.GrilleJeu()
        self.refresh_grille()

        
    def buttonClicked(self):
        if(self.game.moves < 20):      
            sender = self.sender()
            index = sender.value
            sender.setText('*')
            self.set_click(index)
        else:
            self.statusBar().showMessage(
            'Vous avez terminé la partie, votre score est ' + 
            str(self.game.score))
        
    def set_click(self,index):
        if( len(self.click) == 0):      
            self.click.append(index)
        elif (len(self.click) == 1):
            self.click.append(index)
            self.game.move(self.click[0][0], self.click[0][1],
                           self.click[1][0], self.click[1][1])
            self.refresh_grille()    
        else:        
            self.click =[]
            self.click.append(index)
        
            
            
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()