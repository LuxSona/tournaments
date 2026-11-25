import src.backend.Tournament as Tournament
import src.frontend.UI as UI
import src.controller.loader as loader
import tkinter as tk 
from PIL import Image 

class Controller():
    def __init__(self,root : tk.Tk, tournament_name: str):
        #Load tournament
        self.loader = loader.Loader(tournament_name)

        self.competitors = self.loader.competitors
        self.image_map = self.loader.images
        #Create the tournament
        self.tournament = Tournament.SwissTournament(self.competitors)
        self.root = root
        #Implement UI
        self.current_round = 0
        self.current_matchup = 0
        #Get the first matchup
        self.ui = UI.UI(self.root, self._select_win)
        self.li = self.image_map[self.get_current_matchup().lc]
        self.ri = self.image_map[self.get_current_matchup().rc]
        self.ui.set_matchup(self.get_current_matchup(),self.li,self.ri)
    
    def get_current_matchup(self) -> Tournament.Matchup:
        return self.tournament.schedule[self.current_round][self.current_matchup]
    
    def _select_win(self, winner : int):
        """Selects who won a current matchup

        :param winner: The winner
        :type winner: int
        """
        #Increment the matchup or round. 
        self.tournament.set_winner(self.current_round, self.current_matchup, winner)
        #Get the next matchup, OR show standings
        round_length = len(self.tournament.schedule[self.current_round])
        tournament_length = len(self.tournament.schedule)
        #Now increment everything
        self.current_matchup += 1

        if self.current_matchup >= round_length:
            #Cascade down
            self.current_matchup = 0
            self.current_round += 1
        
        #Now check if the round is greater than the tournament length
        if self.current_round >= tournament_length:
            self.ui.show_standings(self.tournament.competitors)
            return 

        #Update UI
        self.li = self.image_map[self.get_current_matchup().lc]
        self.ri = self.image_map[self.get_current_matchup().rc]
        self.ui.set_matchup(self.get_current_matchup(),self.li,self.ri)



