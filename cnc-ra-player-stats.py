import requests
import argparse
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument('player1_id', type=int)
parser.add_argument('player2_id', type=int)
parser.add_argument('--player1_filename_prefix', type=str)
parser.add_argument('--player2_filename_prefix', type=str)
parser.add_argument('--season', type=int, default=11)
args = parser.parse_args()
PLAYER1_ID = args.player1_id
PLAYER2_ID = args.player2_id
SEASON_NUMBER = args.season

if args.player1_filename_prefix:
    PLAYER1_FILENAME_PREFIX = args.player1_filename_prefix
else:
    PLAYER1_FILENAME_PREFIX = "player1"
if args.player2_filename_prefix:
    PLAYER2_FILENAME_PREFIX = args.player2_filename_prefix
else:
    PLAYER2_FILENAME_PREFIX = "player2"

BASE_URL = "https://cnc-stats-api.azurewebsites.net"

def get_player_stats(player_id):
    logging.info(f"Getting player stats for: {player_id}")
    url = f"{BASE_URL}/api/Player/{player_id}?season={SEASON_NUMBER}"
    logging.debug(url)
    response = requests.get(url).json()
    player_wins = int(response['position']['wins'])
    player_losses = int(response['position']['losses'])
    games_played = int(response['position']['gamesPlayed'])
    player_details = {
        'id': player_id,
        'name': response['position']['name'],
        'points': int(response['position']['points']),
        'wins': player_wins,
        'losses': player_losses,
        'wl_ratio': int((player_wins / games_played)*100)
    }
    return player_details

def write_player_stats_to_files(filename_prefix, player_stats):
    logging.info(f"Writing {player_stats} to {filename_prefix}*.txt")
    for stat in player_stats:
        write_stat_to_file(filename_prefix, stat, player_stats[stat])

def write_stat_to_file(filename_prefix, filename_stat, stat):
    filename = f"{filename_prefix}_{filename_stat}.txt"
    logging.info(f"Writing {filename}: '{stat}'")
    f = open(filename, "w+")
    f.write(f"{stat}")
    f.close()

def main():
    logging.debug(f"Base URL: {BASE_URL}")
    logging.info(f"Player 1 ID: {PLAYER1_ID}")
    logging.info(f"Player 2 ID: {PLAYER2_ID}")
    logging.info(f"Player 1 filename prefix: {PLAYER1_FILENAME_PREFIX}")
    logging.info(f"Player 2 filename prefix: {PLAYER2_FILENAME_PREFIX}")
    logging.info(f"Ladder season: {SEASON_NUMBER}")
    player_1_stats = get_player_stats(PLAYER1_ID)
    player_2_stats = get_player_stats(PLAYER2_ID)
    write_player_stats_to_files(PLAYER1_FILENAME_PREFIX, player_1_stats)
    write_player_stats_to_files(PLAYER2_FILENAME_PREFIX, player_2_stats)

if __name__ == "__main__":
    main()