from random import randint,random
import copy


class PokerGameVars():
    GamePhase = 'Waiting start'
    EntranceFee = 10
    BettPrice = 0

class Card:
    def __init__(self):
        self.rank = ''
        self.suit = ''

    def PrintCard(self):
        print('|',self.rank,self.suit,'|')

class PackCards(object):
    def __init__(self):
        Ranks = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
        Suit1 = [''] * 13
        Suit2 = [''] * 13
        Suit3 = [''] * 13
        Suit4 = [''] * 13

        for i in range(len(Suit1)):
            Suit1[i] = Card()
            Suit1[i].rank = Ranks[i]
            Suit1[i].suit = 'C'

        for i in range(len(Suit2)):
            Suit2[i] = Card()
            Suit2[i].rank = Ranks[i]
            Suit2[i].suit = 'D'

        for i in range(len(Suit3)):
            Suit3[i] = Card()
            Suit3[i].suit = 'H'
            Suit3[i].rank = Ranks[i]

        for i in range(len(Suit4)):
            Suit4[i] = Card()
            Suit4[i].rank = Ranks[i]
            Suit4[i].suit = 'S'

        self.PackOrdered = Suit1 + Suit2 + Suit3 + Suit4
        self.PackShuffle = copy.copy(self.PackOrdered)



    def Shuffle(self):
        Inter = self.PackOrdered
        self.PackShuffle = []

        while len(Inter) > 0:
            RandNumb = randint(0,len(Inter)-1)
            self.PackShuffle.append(Inter[RandNumb])
            del Inter[RandNumb]

    def PrintPack(self):
        for i in self.PackShuffle:
            i.PrintCard()
    def AcceptCard(self,Card):
        self.PackShuffle.append(Card)

class GroupCards(PackCards):
    def __init__(self,SetOfCards):
        super().__init__()
        self.PackShuffle = copy.copy(SetOfCards)

    def DealCard(self):
        try:
            card = self.PackShuffle[0]
            del self.PackShuffle[0]
            return card
        except:
            print("Oops!")

class Player(PokerGameVars):
    def __init__(self) -> None:
        self.CardInHand = GroupCards([])
        self.PlayerNum = 0
        self.Capital = 1000
        self.Intent = 'playing'
        self.CurrentBettingPrice = 0

    def AcceptCard(self,Card):
        self.CardInHand.PackShuffle.append(Card)

class AIPlayer(Player,PokerGameVars):
    def __init__(self) -> None:
        super().__init__()


    def PlaceEntranceFee(self):
        self.Capital = self.Capital - super().EntranceFee


    def PlaceBett(self):
        num = random()   
        if num < 0.1:
            self.Intent = 'Fold'
            self.CurrentBettingPrice = 0
        else:
            self.Intent = 'Call'
            self.CurrentBettingPrice = int(random()*self.Capital)
            self.Capital = self.Capital - self.CurrentBettingPrice

    def PlaceBett2(self):
        num = random()
        if num < 0.1:
            self.Intent = 'Raise'
            self.CurrentBettingPrice = self.Capital
            self.Capital = 0
            
        elif num > 0.7:
            self.Intent = 'Fold'
            self.CurrentBettingPrice = 0
        else:
            self.Intent = 'Call'
            if PokerGameVars.BettPrice > self.Capital:
                self.CurrentBettingPrice = self.Capital
            else:
                self.CurrentBettingPrice = int(random()*self.Capital)
            self.Capital = self.Capital - self.CurrentBettingPrice
            
class UserPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

class Dealer:
    def __init__(self,Pack):
        self.RespondibleForPack = Pack
        self.Deck = GroupCards(self.RespondibleForPack.PackShuffle)
        
    def Shuffle(self):
        self.Deck.Shuffle()
    def DealToObject(self,ObjectName):
        ObjectName.AcceptCard(self.Deck.DealCard())

class Table():
    def __init__(self) -> None:
        self.CardInHand = GroupCards([])
        self.Pot = 0

class PokerGameLoop(PokerGameVars):
    def __init__(self, PackCardsObject, ListOfPlayers):
        self.Dealer = Dealer(PackCardsObject)
        self.PlayersList = ListOfPlayers
        self.RoundCompleted = 0
        self.PlayersActiveInRound = []
        self.Stake = 0
        self.Table = Table()



        for i in range(len(self.PlayersList)):
            self.PlayersList[i].PlayerNum = i+1
            self.PlayersActiveInRound.append('Active')
        

    def StartGame(self):
        self.GameOn = True
        self.Dealer.Shuffle()
        GameSteps = ['EntranceFee','PreFlop','PreFlopBetting','Flop','FlopBetting','Turn','TurnBetting','River','RiverBetting']
 
        CountRounds = 0
        while CountRounds < 1:
            self.blind = self.PlayersList[self.RoundCompleted % len(self.PlayersList)]
            for i in GameSteps:
                PokerGameVars.GamePhase = i
                if i == 'EntranceFee':
                    self.GetEntranceFee()
                if i == 'PreFlop':
                    self.DealPreFlop()
                if i == 'PreFlopBetting':
                    self.GetPreFlopBets()
                if i == 'Flop':
                    self.DealFlop()
                    self.DisplayTable()


            CountRounds =+ 1
    
    
    def GetEntranceFee(self):
        for i in self.PlayersList:
            i.PlaceEntranceFee()


    def DealPreFlop(self):
        for i in self.PlayersList:
            self.Dealer.DealToObject(i)
            self.Dealer.DealToObject(i)

    def GetPreFlopBets(self):
        CheckingBlind = True
        Counter = 0
        while CheckingBlind:
            self.blind.PlaceBett()
            blindid = (self.RoundCompleted+Counter) % len(self.PlayersList)
            if self.blind.Intent == 'Fold':
                
                self.blind = self.PlayersList[blindid]
            else:
                self.Stake = self.blind.CurrentBettingPrice
                PokerGameVars.BettPrice = self.blind.CurrentBettingPrice
                self.PlayersActiveInRound[blindid] = self.blind.Intent
                CheckingBlind = False
        
                
        for i in range(len(self.PlayersList)):
            if (self.PlayersActiveInRound[i] != 'Fold') and (self.PlayersList[i] != self.blind):
                print('found blind',self.PlayersList[i] == self.blind)
                self.PlayersList[i].PlaceBett2()
                if self.PlayersList[i].Intent == 'Fold':
                    self.PlayersActiveInRound[i] = 'Fold'
                if self.PlayersList[i].Intent == 'Call':

                    self.PlayersActiveInRound[i] = 'Call'
                    self.Stake = self.Stake + self.PlayersList[i].CurrentBettingPrice
                if self.PlayersList[i].Intent == 'Raise':

                    self.PlayersActiveInRound[i] = 'Raise'
                    self.Stake = self.Stake + self.PlayersList[i].CurrentBettingPrice
            print(self.PlayersActiveInRound)
            print(self.Stake)
                    #self.GetPreFlopBets()

    def DealFlop(self):
        self.Dealer.DealToObject(self.Table.CardInHand)
        self.Dealer.DealToObject(self.Table.CardInHand)
        self.Dealer.DealToObject(self.Table.CardInHand)
    
    def DisplayTable(self):
        print('########################################')
        self.Table.CardInHand.PrintPack()

            




