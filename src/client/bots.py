from comms.comms import Protocol, Parse
from comms.comms import INCOME, FOREIGN_AID, COUP, TAX, ASSASSINATE, STEAL, EXCHANGE, ACTIONS, TARGET_ACTIONS  # Actions
from comms.comms import ASSASSIN, AMBASSADOR, CAPTAIN, DUKE, CONTESSA, CHARACTERS  # Characters
from .player import Player


class CoupBot(Player):
    """
    CoopBot player class.
    """

    def __init__(self):
        super().__init__()
        self.verbose = True  # Error messages and connection status
        self.ui = False  # User interface like input prompts

    def receive(self, message: str):
        # TODO
        # Implement your bot here

        # Use Parse to help reading messages. Example:

        # m = Parse(message)
        # command = m.command
        # source = m.sourceID
        # card1 = m.card1
        # card2 = m.card2
        # action = m.action
        # target = m.targetID
        # coins = m.coins

        # Use Protocol to create messages. Example:

        # p = Protocol()
        # m = p.ACT("1", COUP, "2")
        
        # Put the reply onto the checkout queue. Example:
        # self.checkout.put(m)
        
        raise NotImplementedError
