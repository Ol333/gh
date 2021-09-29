import matplotlib.pyplot as plt
import rab_with_db as rwd

if __name__ == "__main__":
    game_for_player = []
    player_table = rwd.table_list("Player")
    for i in player_table:
        players_kifu_list = rwd.players_kifu_list(i[0],False)
        game_for_player.append(len(players_kifu_list))
        players_kifu_list = list(map(lambda x:x[1],players_kifu_list))

    print(game_for_player)

    # plt.plot().hist(game_for_player)

    