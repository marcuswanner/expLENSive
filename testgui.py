import burngui as g
import time
g.Initialize(4, 2)
g.SendArray([[0, 0], [0, 0], [-1, -1], [0, 0]])
time.sleep(1)
g.SendArray([[0, 0], [0, 0], [0, -1], [0, 0]])
time.sleep(1)
g.Finished()
time.sleep(1)
