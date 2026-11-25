from src.controller.controller import Controller
from tkinter import Tk 



def main():
    root = Tk()
    controller = Controller(root, "templates/tournaments/tournament_template.json")
    root.mainloop()

if __name__ == "__main__":
    main()
