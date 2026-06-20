# EINREICHUNG FÜR DEN GIGATHON 2026 #
# AUTOR: David Höller #
# Simulation einer Kugel #

######   Initial imports   ######
import gc
import random
import tomllib, time, tkinter

######   Permanent flags and variables   ######
textOnlyMode = False
simulating = True
firstIteration = True

######   Establishing the rendering system   ######
class Renderer:
    #####  Variable setting  #####
    # ---  Initialize the renderer without invoking turtle  --- #
    def __init__(self, rows, columns):
        # ---  Set simulation size  --- #
        self.rowHeight = None
        self.columnWidth = None
        self.screenMaxY = None
        self.screenMaxX = None
        self.screenSizeY = None
        self.screenSizeX = None
        self.root = None
        self.canvas = None
        self.screen = None
        self.screensize = None
        self.rows = rows
        self.columns = columns

        # ---  Prepare for image loading and rendering  --- #
        self.images = {}
        self.imageElements = []

    # ---  Initialize the renderer invoking turtle  --- #
    def invoke_turtle(self):
        # ---  Invoke turtle  --- #
        if firstIteration:
            import turtle
            global turtle

        # ---  Set up the screen, and extract tkinter elements  --- #
        self.screen = turtle.Screen()
        self.screen.setup(width = 1.0, height = 1.0)
        self.screen.tracer(0,0)
        self.screen.bgcolor("gray")

        self.canvas = self.screen.getcanvas()

        self.root = self.canvas.winfo_toplevel()
        self.root.overrideredirect(True)

        # ---  Set scaling constants  --- #
        self.screensize = self.screen.screensize()
        self.screenSizeX = self.screensize[0] * 2
        self.screenSizeY = self.screensize[1] * 2

        # ---  Set endpoints of screen  --- #
        self.screenMaxX = self.screensize[0]
        self.screenMaxY = self.screensize[1]

        # ---  Set scale of rows and columns  --- #
        self.columnWidth = self.screenSizeX / self.columns
        self.rowHeight = self.screenSizeY / self.rows

        # ---  Hide the turtle and make it instant  --- #
        turtle.hideturtle()
        turtle.speed(0)

    #####  Close turtle  ######
    @staticmethod
    def bye():
        turtle.bye()

    #####  Calculation Functions  #####
    # ---  Calculate locations of grid boxes  --- #
    def get_grid_box_boundaries(self, x, y):
        return {"x1": -self.screenSizeX / 2 + (x * self.columnWidth), "x2": -self.screenSizeX / 2 + ((x + 1) * self.columnWidth),
                "y1": -self.screenSizeY / 2 + (y * self.rowHeight), "y2": -self.screenSizeY / 2 + ((y + 1) * self.rowHeight)}

    # ---  Get the center of a grid box  --- #
    def get_grid_box_center(self, x, y):
        boundaries = self.get_grid_box_boundaries(x, y)
        return [(boundaries["x1"] + boundaries["x2"]) / 2,
                (boundaries["y1"] + boundaries["y2"]) / 2]

    #####  Image Processing system  #####
    def create_image(self, image_name, data):
        self.images[image_name]=tkinter.PhotoImage(data=data)

    def create_sprite(self, sprite_name, data):
        self.create_image(sprite_name, data)

    #####  Rendering mechanics  #####
    # ---  Render the Grid  --- #
    def render_grid(self):
        turtle.home()
        turtle.penup()
        for i in range(self.columns + 1):
            boundaries = self.get_grid_box_boundaries(i, 0)
            turtle.goto(boundaries["x1"], -self.screenMaxY)
            turtle.pendown()
            turtle.goto(boundaries["x1"], self.screenMaxY)
            turtle.penup()
        for i in range(self.rows + 1):
            boundaries = self.get_grid_box_boundaries(0, i)
            turtle.goto(-self.screenMaxX, boundaries["y1"])
            turtle.pendown()
            turtle.goto(self.screenMaxX, boundaries["y1"])
            turtle.penup()

    # ---  Color a field  --- #
    def color_field(self, x, y, color):
        boundaries = self.get_grid_box_boundaries(x, y)
        turtle.fillcolor(color)
        turtle.penup()
        turtle.goto(boundaries["x1"], boundaries["y1"])
        turtle.pendown()
        turtle.begin_fill()
        turtle.goto(boundaries["x2"], boundaries["y1"])
        turtle.goto(boundaries["x2"], boundaries["y2"])
        turtle.goto(boundaries["x1"], boundaries["y2"])
        turtle.end_fill()
        turtle.penup()

    # ---  Render images  --- #
    def print_image(self, image_name, x, y):
        self.imageElements.append(self.canvas.create_image(x, y, image = self.images[image_name], anchor = 'center'))

    # ---  Render sprites  --- #
    def print_sprite(self, sprite_name, x, y):
        self.print_image(sprite_name, self.get_grid_box_center(x, self.rows - y - 1)[0], self.get_grid_box_center(x, self.rows - y - 1)[1])

    def kill_images(self):
        for imageElement in self.imageElements:
            self.canvas.delete(imageElement)

    # ---  Blank screen  --- #
    def blank_screen(self):
        turtle.fillcolor("white")
        turtle.penup()
        boundaries = self.get_grid_box_boundaries(0, 0)
        turtle.goto(boundaries["x1"], boundaries["y1"])
        turtle.pendown()
        turtle.begin_fill()
        boundaries = self.get_grid_box_boundaries(0, self.rows - 1)
        turtle.goto(boundaries["x1"], boundaries["y2"])
        boundaries = self.get_grid_box_boundaries(self.columns - 1, self.rows - 1)
        turtle.goto(boundaries["x2"], boundaries["y2"])
        boundaries = self.get_grid_box_boundaries(self.columns - 1, 0)
        turtle.goto(boundaries["x2"], boundaries["y1"])
        turtle.end_fill()
        turtle.penup()

    # ---  Render the path  --- #
    def render_path(self):
        turtle.width(2)
        for position in playerInstance.positions:
            turtle.setpos(position[0],position[1])
            turtle.pendown()
        center = self.get_grid_box_center(playerInstance.x, playerInstance.y)
        turtle.setpos(center[0],center[1])
        turtle.penup()
        turtle.width(1)

    # ---  Render the Progress Bar  --- #
    def render_progress_bar(self):
        turtle.color("blue")
        turtle.width(4)
        turtle.setpos(-self.screenMaxX,-self.screenMaxY-10)
        turtle.pendown()
        turtle.setpos(((2*self.screenMaxX) * (simulationInstance.currentStep / simulationInstance.steps)) - self.screenMaxX, -self.screenMaxY - 10)
        turtle.penup()
        turtle.width(1)
        turtle.color("black")

    #####  Rendering a frame  #####
    def render(self):
        turtle.clear()
        self.kill_images()
        self.blank_screen()
        self.render_path()
        self.render_grid()
        self.print_sprite("marble", playerInstance.x, playerInstance.y)
        for deflector in simulationInstance.deflectors:
            self.print_sprite("deflector", deflector[0], deflector[1])
        for randomizer in simulationInstance.randomizers:
            self.print_sprite("randomizer", randomizer[0], randomizer[1])
        for power in simulationInstance.powers:
            self.print_sprite("power", power[0], power[1])
        self.render_progress_bar()
        self.screen.update()


######   Establishing the player system   ######
class Player:
    # ---  Initialize the Player  --- #
    def __init__(self,a,x,y,e):
        self.angle = a
        self.x = x
        self.y = y
        self.energy = e
        self.extraLog = []
        self.pastX = 0
        self.pastY = 0
        self.positions = [renderingInstance.get_grid_box_center(self.x, self.y)]

        # ---  Define direction decoding  --- #
        self.decodeDirection = {0: {"x": 0, "y": 1}, 45: {"x": 1, "y": 1}, 90: {"x": 1, "y": 0}, 135: {"x": 1, "y": -1},
                           180: {"x": 0, "y": -1}, 225: {"x": -1, "y": -1}, 270: {"x": -1, "y": 0},
                           315: {"x": -1, "y": 1}}

    # ---  Log to the command line  --- #
    def log_state(self):
        print("-" * 50)
        print("Schritt: " + str(simulationInstance.currentStep))
        print("Energie: " + str(self.energy))
        if len(self.extraLog) > 0:
            for extraLog in self.extraLog:
                print(extraLog)
        self.extraLog=[]
        if self.pastX != self.x or self.pastY != self.y:
            print("Ein Schritt wurde getätigt in die Richtung: " + str(self.angle))
            print("Dies ist der Fall, da die Energie ausreichte.")
            if simulationInstance.currentStep == 0:
                print("Vorherige Position (x,y): Keine vorherige Position, dies ist Schritt 0")
            else:
                print("Vorherige Position (x,y): (" + str(self.pastX) + "," + str(self.pastY) + ")")
            print("Neue Position (x,y): (" + str(self.x) + "," + str(self.y) + ")")
        else:
            print("Die Kugel hat keine Energie mehr, darum hat sie sich nicht bewegt.")

    # ---  Move the character with change  --- #
    def move_change(self, change_x, change_y):
        self.energy -= 1
        if self.x + change_x in range(renderingInstance.columns) and self.y + change_y in range(renderingInstance.rows):
            self.x += change_x
            self.y += change_y
        else:
            self.energy -= 10
            self.positions.append(renderingInstance.get_grid_box_center(self.x, self.y))
            angle_before_turn = self.angle
            if self.x + change_x > renderingInstance.columns-1:
                if self.angle == directions["NE"]:
                    self.angle = directions["NW"]
                if self.angle == directions["E"]:
                    self.angle=directions["W"]
                if self.angle == directions["SE"]:
                    self.angle = directions["SW"]
            if self.x + change_x < 0:
                if self.angle == directions["NW"]:
                    self.angle = directions["NE"]
                if self.angle == directions["W"]:
                    self.angle=directions["E"]
                if self.angle == directions["SW"]:
                    self.angle = directions["SE"]
            if self.y + change_y > renderingInstance.rows-1:
                if self.angle == directions["NE"]:
                    self.angle = directions["SE"]
                if self.angle == directions["N"]:
                    self.angle=directions["S"]
                if self.angle == directions["NW"]:
                    self.angle = directions["SW"]
            if self.y + change_y < 0:
                if self.angle == directions["SE"]:
                    self.angle = directions["NE"]
                if self.angle == directions["S"]:
                    self.angle=directions["N"]
                if self.angle == directions["SW"]:
                    self.angle = directions["NW"]
            self.extraLog.append("Aufgrund von einer Kollision mit einer Wand änderte sich die Richtung der Kugel von " + str(angle_before_turn) +" zu " + str(self.angle) + ". Es wurde ebenfalls Energie verloren (10).")
            self.move_step()

    # ---  Move the character base on direction  --- #
    def move_step(self):
        self.move_change(self.decodeDirection[self.angle]["x"], self.decodeDirection[self.angle]["y"])
        if [self.x, self.y] in simulationInstance.deflectors:
            angle_before_turn=self.angle
            self.energy += 20
            self.positions.append(renderingInstance.get_grid_box_center(self.x, self.y))
            simulationInstance.deflectors.pop(simulationInstance.deflectors.index([self.x, self.y]))
            if self.angle == directions["N"]:
                self.angle = directions["S"]
            elif self.angle == directions["NE"]:
                self.angle = directions["SW"]
            elif self.angle == directions["W"]:
                self.angle = directions["E"]
            elif self.angle == directions["SE"]:
                self.angle = directions["NW"]
            elif self.angle == directions["S"]:
                self.angle = directions["N"]
            elif self.angle == directions["SW"]:
                self.angle = directions["NE"]
            elif self.angle == directions["W"]:
                self.angle = directions["E"]
            elif self.angle == directions["NW"]:
                self.angle = directions["SE"]
            self.extraLog.append("Aufgrund von einer Kollision mit einem Abpraller änderte sich die Richtung der Kugel von " + str(angle_before_turn) + " zu " + str(self.angle) + ". Die Energie wurde erhöht (20).")
        if [self.x, self.y] in simulationInstance.randomizers:
            angle_before_turn=self.angle
            self.energy += 20
            self.positions.append(renderingInstance.get_grid_box_center(self.x, self.y))
            simulationInstance.randomizers.pop(simulationInstance.randomizers.index([self.x, self.y]))
            self.angle = random.choice(list(self.decodeDirection.keys()))
            self.extraLog.append("Aufgrund von einer Kollision mit einem Randomizer änderte sich die Richtung der Kugel von " + str(angle_before_turn) + " zu " + str(self.angle) + ". Die Energie wurde erhöht (20).")
        if [self.x, self.y] in simulationInstance.powers:
            self.energy += 50
            simulationInstance.powers.pop(simulationInstance.powers.index([self.x, self.y]))
            self.extraLog.append("Aufgrund von einer Kollision mit einem Power-item wurde die Energie erhöht (50).")

######   Configuring simulation information   ######
class Simulation:
    def __init__(self, name_simulation, maximum_steps, deflector_count, randomizer_count, power_count, delay=0.1):
        self.currentStep = 0
        self.name = name_simulation
        self.steps = maximum_steps
        self.delay = delay
        self.deflectors = []
        self.randomizers = []
        self.powers = []
        self.storms = 0
        self.winds = 0
        self.success = False

        # ---  Create deflectors  --- #
        # --- Make possibles --- #
        for i in range(renderingInstance.columns):
            for j in range (renderingInstance.rows):
                self.deflectors.append([i,j])

        # --- Select locations --- #
        random.shuffle(self.deflectors)
        while len(self.deflectors) > deflector_count:
            self.deflectors.pop()


        # ---  Create randomizers  --- #
        # --- Make possibles --- #
        for i in range(renderingInstance.columns):
            for j in range (renderingInstance.rows):
                self.randomizers.append([i,j])

        # --- Prevent overlap --- #
        for deflector in self.deflectors:
            if deflector in self.randomizers:
                self.randomizers.pop(self.randomizers.index(deflector))

        # --- Select locations --- #
        random.shuffle(self.randomizers)
        while len(self.randomizers) > randomizer_count:
            self.randomizers.pop()


        # ---  Create powers  --- #
        # --- Make possibles --- #
        for i in range(renderingInstance.columns):
            for j in range (renderingInstance.rows):
                self.powers.append([i,j])

        # --- Prevent overlap --- #
        for deflector in self.deflectors:
            if deflector in self.powers:
                self.powers.pop(self.powers.index(deflector))

        for randomizer in self.randomizers:
            if randomizer in self.powers:
                self.powers.pop(self.powers.index(randomizer))

        # --- Select locations --- #
        random.shuffle(self.powers)
        while len(self.powers) > power_count:
            self.powers.pop()

    #####  Make a step in a simulation  #####
    def step(self):
        time.sleep(self.delay)
        playerInstance.pastX = playerInstance.x
        playerInstance.pastY = playerInstance.y

        # ---  Run Wirbelsturm  --- #
        if random.randint(1,50) == 1:
            self.storms += 1
            initial_direction = playerInstance.angle
            playerInstance.angle = random.choice(list(playerInstance.decodeDirection.keys()))
            playerInstance.positions.append(renderingInstance.get_grid_box_center(playerInstance.x, playerInstance.y))
            playerInstance.extraLog.append("Das Zufallsevent Wirbelsturm ist eingetreten, und die Richtung der Kugel wurde zufällig geändert von Richtung " + str(initial_direction) + " auf Richtung " + str(playerInstance.angle))

        # ---  Run Gegenwind  --- #
        if random.randint(1,50) == 1:
            self.winds += 1
            playerInstance.energy -= 10
            playerInstance.extraLog.append("Das Zufallsevent Gegenwind ist eingetreten, und die Kugel verlor 10 Energie")

        # ---  Conduct movement  --- #
        if playerInstance.energy > 0:
            playerInstance.move_step()
        if not textOnlyMode:
            renderingInstance.render()
        gc.collect()
        if playerInstance.energy < 0:
            playerInstance.energy = 0
        playerInstance.log_state()

    #####  Run the simulation, and record the outcome  #####
    def simulate(self):
        playerInstance.log_state()
        for i in range(steps):
            self.currentStep = i+1
            self.step()
            if playerInstance.energy <= 0:
                self.step()
                print("-"*50)
                print("Die Simulation wurde Angehalten, da die Energie der Kugel aufgebraucht wurde.")
                simulationInstance.success = False
                break
        if playerInstance.energy > 0:
            print("-" * 50)
            print("Die Simulation wurde Angehalten, da die maximale Schrittzahl erreicht wurde.")
            simulationInstance.success = True
        else:
            print("-" * 50)
            print("Die Simulation wurde Angehalten, da die Energie der Kugel aufgebraucht wurde.")
            simulationInstance.success = False


while simulating:
    ######   Initialization of the program   ######
    # ---  Set up components  --- #
    renderingInstance = Renderer(25, 35)

    ######   Automatic Explanation   #####
    input("Dieses Programm ist eine Simulation einer Kugel die anhand von eingegebenen Parametern automatisch ausgeführt wird. Sie ist erfolgreich, wenn die Energie ausreicht. [Enter] zum fortfahren...")
    input("Diese Simulation enthält drei Elemente mit denen eine Kugel kollidieren kann, wonach sie sich selbst zerstören: Abpraller, Randomizer, und Power-items. [Enter] zum fortfahren...")
    input("Abpraller prallen die Kugel in die entgegengesetzte Richtung von der sie kam ab. [Enter] zum fortfahren...")
    input("Randomizer schickt die Kugel in eine Zufällige richtung. [Enter] zum fortfahren...")
    input("Power-items erhöhen die Energie der Kugel um 50. [Enter] zum fortfahren...")
    input("Die Kugel besitzt Energie. Sie verliert diese bei einer Kollision mit einer Wand (wobei sie von der Wand abprallt), sowie konstant bei jeder Bewegung aufgrund von Reibung. [Enter] zum fortfahren...")
    input("Die Kugel gewinnt Energie wenn sie mit einem Element interagiert. [Enter] zum fortfahren...")
    input("Zusätzlich gibt es zwei Zufallsevents, die bei jedem Schritt eine chance aufzutreten besitzen. [Enter] zum fortfahren...")
    input("Das Erste ist Wirbelsturm. Dies setzt die Richtung der Kugel auf eine Zufällige Richtung. [Enter] zum fortfahren...")
    input("Das Zweite ist Gegenwind. Dies nimmt der Kugel 10 Energie. [Enter] zum fortfahren...")
    input("Die simulation wird bei einem vollständigen Verlust der Energie, oder bei überschreitung der maximalen Simulationsschritten abgebrochen. [Enter] zum fortfahren...")
    input("Die gesamte simulation wird im Terminal protokolliert. [Enter] zum fortfahren...")
    input("Sie werden nun dazu aufgefordert, die Startparameter einzugeben. [Enter] zum fortfahren...")
    print("\n"*50)

    ######   Gathering parameters   ######
    name = input("Name der Simulation: ")

    # ---  Get and validate initial direction  --- #
    directions = {"N":0, "NE":45, "E":90, "SE":135, "S":180, "SW":225, "W":270, "NW":315}
    valid = False

    while not valid:
        try:
            initialA = directions[input("Geben sie die Startrichtung als Himmelsrichtung an, gewählt von N, NE, E, SE, S, SW, W, NW: ")]
            valid = True
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

    # ---  Get and validate initial x  --- #
    valid = False

    while not valid:
        try:
            initialX = int(input("Geben sie die Startposition x an, als ganze Zahl von 0 bis " + str(renderingInstance.columns - 1) + ": "))
            if initialX in range(renderingInstance.columns):
                valid = True
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

    # ---  Get and validate initial y  --- #
    valid = False

    while not valid:
        try:
            initialY = int(input("Geben sie die Startposition y an, als ganze Zahl von 0 bis " + str(renderingInstance.rows - 1) + ": "))
            if initialY in range(renderingInstance.rows):
                valid = True
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

    # ---  Get how many frames to run  --- #
    valid = False

    while not valid:
        try:
            steps = int(input("Geben sie ein wie viele Schritte simuliert werden sollen (Zwischen 1000 und 2000 sind empfohlen, gemessen auf einem M1 macbook): "))
            if steps > 0:
                valid = True
            else:
                print("Ungültige Eingabe, bitte versuchen Sie es erneut")
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

    # ---  Get initial energy  --- #
    valid = False

    while not valid:
        try:
            initialE = int(input("Geben sie die Startenergie an, als ganze Zahl. Empfohlen wird "+str(int(round(steps+(steps/3))))+": "))
            if initialE >= 0:
                valid = True
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

    # ---  Get how many deflectors to create  --- #
    valid = False

    while not valid:
        try:
            deflectors = int(input("Geben sie die Zahl der Abpraller an (Empfohlen wird 15): "))
            if deflectors > -1:
                valid = True
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

    # ---  Get how many randomizers to create  --- #
    valid = False

    while not valid:
        try:
            randomizers = int(input("Geben sie die Zahl der Randomizer an (Empfohlen wird 15): "))
            if randomizers > -1:
                valid = True
        except:
            print("Ungültige Eingabe, bitte versuchen Sie es erneut")
            pass

        # ---  Get how many powers to create  --- #
        valid = False

        while not valid:
            try:
                powers = int(input("Geben sie die Zahl der Power-items an (Empfohlen wird 15): "))
                if powers > -1:
                    valid = True
            except:
                print("Ungültige Eingabe, bitte versuchen Sie es erneut")
                pass


    ######   Initialization of the program   ######
    # ---  Set up components  --- #
    simulationInstance = Simulation(name, steps, deflectors, randomizers, powers, delay = 0)
    renderingInstance.invoke_turtle()
    playerInstance = Player(initialA, initialX, initialY, initialE)

    # ---  Get image data  --- #
    with open("pyproject.toml", "rb") as f:
        imageData = tomllib.load(f)

    # ---  Create the images  --- #
    for name in imageData.keys():
        renderingInstance.create_sprite(name, imageData[name])

    ######   Initial log   ######
    print("\n"*50)
    renderingInstance.render()
    print("Die Simulation " + simulationInstance.name + " beginnt in 5 Sekunden. Bitte halten sie das Turtle Fenster bereit.")
    print("Unter der Simulation wird eine Fortschrittsleiste angezeigt, die visualisiert, wie viele Schritte der Maximalschritte erreicht sind. Sollte die Simulation sich nicht mehr bewegen, schauen sie ins Terminal um zu überprüfen ob die Simulation beendet ist.")
    print("Die Parameter die eingegeben wurden lauten:")
    print("Startrichtung: "+str(initialA))
    print("Startkoordinate: ("+str(initialX)+", "+str(initialY)+")")
    print("Maximalschritte: "+str(steps))
    print("Startenergie: "+str(initialE))
    print("Abpraller: "+str(deflectors))
    print("Randomizer: "+str(randomizers))
    print("Power-items: " + str(powers))
    print("Ausgeführte Schritte: " + str(simulationInstance.currentStep))
    print("Überbleibende Energie: " + str(playerInstance.energy))
    print("Genutzte Abpraller: " + str(deflectors - len(simulationInstance.deflectors)))
    print("Genutzte Randomizer: " + str(randomizers - len(simulationInstance.randomizers)))
    print("Genutzte Power-items: " + str(powers - len(simulationInstance.powers)))

    time.sleep(5)

    ######   Establishing the simulation procedure   ######
    startingTime = time.time()
    simulationInstance.simulate()

    ######   Output result   ######
    renderingInstance.render()
    print("Die Simulation " + simulationInstance.name + " erfolgte in in " + str(round(time.time() - startingTime)) + " Sekunden")
    print("Die Parameter die eingegeben wurden lauten:")
    print("Startrichtung: " + str(initialA))
    print("Startkoordinate: (" + str(initialX) + ", " + str(initialY) + ")")
    print("Maximalschritte: " + str(steps))
    print("Startenergie: " + str(initialE))
    print("Endkoordinate: (" + str(playerInstance.x) + ", " + str(playerInstance.y) + ")")
    print("Genutzte Abpraller: " + str(deflectors))
    print("Genutzte Randomizer: " + str(randomizers))
    print("Genutzte Power-items: " + str(powers))
    print("Anzahl von Wirbelstürmen: " + str(simulationInstance.storms))
    print("Anzahl von Gegenwinden: " + str(simulationInstance.winds))
    if simulationInstance.success:
        print("Hat die Energie der Kugel ausgereicht: Ja")
    else:
        print("Hat die Energie der Kugel ausgereicht: Nein")

    firstIteration = False
    print("-"*50)
    simulating = input("Erneut Durchführen? J für Ja, N für Nein: ").lower() == "j"

######   Exit program cleanly   ######
renderingInstance.bye()