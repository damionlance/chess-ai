from chess_game import ChessGame
from utils.heuristics import combined
from agents.greedy_agent import GreedyAgent
from agents.random_agent import RandAgent
from agents.human_agent import HumanAgent
from agents.combined_agent_trans import CombinedAgentTrans
from agents.history_agent_trans import OrderedAgentTrans

def main():
    print("Welcome to our chess AI! Please select your difficulty:")
    print("Easy: 1")
    print("Medium: 2")
    print("Hard: 3")
    diff = input("")

    depth = 0
    if diff == "1":
        depth = 1
    elif diff == "2":
        depth = 2
    elif diff == "3":
        depth = 3

    demo_human_agent = HumanAgent(True)
    demo_opponent_agent = OrderedAgentTrans(False, combined, depth, load_hh=True)

    demo_game = ChessGame(demo_human_agent, demo_opponent_agent)
    demo_game.play_game(True)


if __name__ == "__main__":
    main()
