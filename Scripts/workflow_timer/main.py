import time, os
from pynput import keyboard
from worktimer import WorkTimer

t = WorkTimer("Testimer")

def main():
	global t
	t.start()
	lis = keyboard.Listener(on_press=on_press)
	lis.start()
	run()

def on_press(key):
	global t
	if key.name == "space":
		t.pause()
	if key.name == "enter":
		t.stop()

def run():
	global t
	while True:
		os.system("clear")
		t.run()
		print(t)
		time.sleep(1)

if __name__ == "__main__":
	main()