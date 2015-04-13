import time

t = time.time()
for i in range(10000000):
	pass

print time.time() - t

# En nuestra maquina del lab: 0.498979091644
# En su maquina del lab: 0.447
# En el pc de Luisma: 0.862239
# PC de Jenny: 0.581339120865
