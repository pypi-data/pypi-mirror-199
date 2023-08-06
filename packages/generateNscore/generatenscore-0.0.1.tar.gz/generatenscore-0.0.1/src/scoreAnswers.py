import generateNscore as GnS

a=GnS.scoreAnswerFiles('K0322c/K0322cWork.pickle', 'K0322c/K0322c_txt')
a.scoreThem()
a.saveResults()
