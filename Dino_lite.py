import os, time, random, threading

w, h = 60, 12
dino_y = h-2
jump = 0
obstacles = []
score = 0
speed = 0.12
gap = 14
running = True
key_pressed = False

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def draw_logo():
    print("╔══════════╗")
    print("║ TASHFIQ ONBIR CYBER DINO ║")
    print("║ Score:", str(score).rjust(4), " SPEED:", f"{1/speed:.1f}x".rjust(5), "║")
    print("║ [SPACE=Jump] [Q=Quit] ║")
    print("╚══════════╝")

def draw():
    clear()
    draw_logo()
    for y in range(h):
        line = ""
        for x in range(w):
            if x == 5 and y == dino_y:
                line += "🦖"
            elif (x, y) in obstacles:
                line += "🌵"
            elif y == h-1:
                line += "═"
            elif y == h-2 and x % 4 == 0:
                line += "."
            else:
                line += " "
        print(line)

def input_thread():
    global running, key_pressed
    while running:
        try:
            key = input()
            if key == "":
                key_pressed = True
            if key == "q":
                running = False
        except:
            pass

threading.Thread(target=input_thread, daemon=True).start()

while running:
    # jump + gravity
    if jump > 0:
        dino_y -= 1
        jump -= 1
    elif dino_y < h-2:
        dino_y += 1

    # space চাপলে লাফ
    if key_pressed and dino_y == h-2:
        jump = 4
        key_pressed = False

    # obstacle move
    obstacles = [(x-1, y) for x, y in obstacles if x > 0]

    # new obstacle
    if not obstacles or obstacles[-1][0] < w - gap:
        if random.random() < 0.4:
            obstacles.append((w-1, h-2))

    # collision check
    if (5, dino_y) in obstacles:
        clear()
        print("╔══════════════╗")
        print("║ 💀 GAME OVER ║")
        print("║ Final Score:", str(score).rjust(3), "║")
        print("╚══════════════╝")
        running = False
        break

    draw()
    score += 1
    time.sleep(speed)

    # speed বাড়বে
    if score % 100 == 0:
        speed -= 0.008
        gap -= 1
        if speed < 0.04:
            speed = 0.04