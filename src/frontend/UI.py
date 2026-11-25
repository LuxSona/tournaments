import tkinter as tk 
from collections.abc import Callable
from src.backend.Tournament import SwissTournament, Matchup

class UI:
    def __init__(self, root : tk.Tk, select_win : Callable[[int], None]):
        #Self variables
        self.root = root 
        self.select_win = select_win

        #The main competition panel, which will have a left competitor, a right competitor, and a DRAW button. 
        self.root.title("Tournament")
        root.geometry("600x600")
        # Create top frame for competitors (side by side)
        self.competition_frame = tk.Frame(root)

        # Left and right competitor panels
        self.left_competitor_panel = tk.Frame(self.competition_frame)
        self.right_competitor_panel = tk.Frame(self.competition_frame)

        #Set their size to be equal and bordered
        # Labels for both competitors
        self.left_competitor_name = tk.Label(self.left_competitor_panel)
        self.right_competitor_name = tk.Label(self.right_competitor_panel)

        # Pack the labels so they're visible
        self.left_competitor_name.pack(fill=tk.BOTH, expand=True)
        self.right_competitor_name.pack(fill=tk.BOTH, expand=True)

        # Competitor frames (for displaying images or other content)
        self.left_competitor = tk.Frame(self.left_competitor_panel)
        self.right_competitor = tk.Frame(self.right_competitor_panel)
        self.left_competitor.config(width=300, height=600, borderwidth=2, relief="solid")
        self.right_competitor.config(width=300, height=600, borderwidth=2, relief="solid")
        # Pack competitor frames (empty initially)
        self.left_competitor.pack(fill=tk.BOTH, expand=True)
        self.right_competitor.pack(fill=tk.BOTH, expand=True)

        # Initialize matchup to None
        self.current_matchup = None

        # We want there to be a left panel, and a right panel, and centered underneath them is the draw button.
        # Create bottom frame for draw button
        self.draw_frame = tk.Frame(root)

        self.draw = tk.Button(self.draw_frame, text="DRAW", width=10)
        self.initialize_bindings()
        self.draw.pack()
        self.draw_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.left_competitor_panel.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.right_competitor_panel.pack(side=tk.RIGHT, fill = tk.BOTH, expand = True)
        self.competition_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_standings(self, competitors : list):
        """Takes a list of competitors and shows their standings

        :param competitors: A list of competitor objects
        :type competitors: list[]
        """        
        #Show a column list of all competitors and their updated elo ratings
        standings_panel = tk.Frame(self.root)
        for competitor in competitors:
            #Get the name
            name = competitor.name
            rating = competitor.getRating()
            #Write the name and rating to a line
            line = tk.Label(standings_panel, text=f"{name}: {rating}")
            #Pack the line
            line.pack()
        #Clear everything and display the standings to the user
        self.competition_frame.pack_forget()
        self.draw_frame.pack_forget()
        standings_panel.pack(fill=tk.BOTH, expand=True)

        
    def initialize_bindings(self):
        #The panels should effectively call 'set_winner' on the controller's tournament, where the left panel calls select_win with 1, the right panel calls -1, and DRAW calls it with 0.
        self.left_competitor.bind("<Button-1>", lambda event: self.select_win(1))
        self.right_competitor.bind("<Button-1>", lambda event: self.select_win(-1))
    
        # Handle draw button
        self.draw.bind("<Button-1>", lambda event: self.select_win(0))

    def set_matchup(self, matchup: Matchup):
        self.current_matchup = matchup
        #Set the text of the left and right competitors.
        self.left_competitor_name.config(text=matchup.lc.name)
        self.right_competitor_name.config(text=matchup.rc.name)



