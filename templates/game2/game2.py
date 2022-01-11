import shelve
game2 =  shelve.open("game2")
game2['outcome'] = "Victory"
game2['vouchers'] = 0
game2.close()
