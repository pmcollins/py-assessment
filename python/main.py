from __future__ import print_function

import mysql.connector
import csv

from inserter import Inserter
from dbutil import DbUtil
from transformation import PointsAccumulator


########################################
USER = 'pcollins'
PASSWORD = 'poiupoiu'
HOST = '192.168.209.129'
DATABASE = 'rh'
########################################


class HockeyStatsLoader:

    def __init__(self, _connection):
        self._db = DbUtil(_connection)

    def load_csv_into_db(self):
        self._drop_tables()
        self._create_tables()
        self._load_master()
        self._load_coaches()
        self._load_awards_players()
        points_accumulator = self._transform_and_load_scores()
        self._write_points_summary(points_accumulator)
        self._db.commit()
        print()

    def _drop_tables(self):
        """Drops all required tables. Useful for multiple runs."""
        for table_name in ('awards_players', 'coaches', 'master', 'points_summary', 'player_teams'):
            sql = 'DROP TABLE IF EXISTS ' + table_name
            self._db.execute_sql(sql)

    def _create_tables(self):
        """Executes all of the table creation sql files."""
        self._db.execute_sql_files((
            'create-awards-players', 'create-coaches', 'create-master', 'create-player-teams', 'create-points-summary'
        ))

    def _load_master(self):
        """Loads the Master dataset into the db."""
        self._load_csv('master', (
            'playerID', 'coachID', 'hofID', 'firstName', 'lastName', 'nameNote', 'nameGiven', 'nameNick',
            'height', 'weight', 'shootCatch', 'legendsID', 'ihdbID', 'hrefID',
            'firstNHL', 'lastNHL', 'firstWHA', 'lastWHA', 'pos',
            'birthYear', 'birthMon', 'birthDay', 'birthCountry', 'birthState', 'birthCity',
            'deathYear', 'deathMon', 'deathDay', 'deathCountry', 'deathState', 'deathCity'
        ))

    def _load_coaches(self):
        """Loads the Coaches dataset into the db."""
        self._load_csv('coaches', (
            'coachID', 'year', 'tmID', 'lgID', 'stint', 'notes', 'g', 'w', 'l', 't', 'postg', 'postw', 'postl', 'postt'
        ))

    def _load_awards_players(self):
        """Loads the AwardsPlayers dataset into the db."""
        self._load_csv('awards_players', (
            'playerID', 'award', 'year', 'lgID', 'note', 'pos'
        ), file_name='AwardsPlayers')

    def _transform_and_load_scores(self):
        """This method does two things on the Scoring data set: it performs the custom transformation requested by the
        assessment, summarizing player points into the 'points_summary' table, and it populates the 'player_teams'
        table.

        The 'player_teams' table just maps players to the team they were on for the indicated year. This is used by
        the final query.

        The 'points_summary' table has the result of the transformation, which is just all of a player's points over
        the years, summarized into a single row per player containing the min, max, and average yearly points.
        """
        points_accumulator = PointsAccumulator()
        player_teams_inserter = Inserter('player_teams', ('playerId', 'teamId', 'year'))
        with open(self._get_csv_fname('Scoring'), 'r') as csv_file:
            # since we're not using all of the columns, we use DictReader to index into the csv row by column name
            rows = csv.DictReader(csv_file)
            cursor = self._db.cursor()
            for row in rows:
                player_id = row['playerID']
                player_teams_inserter.insert(cursor, [player_id, row['tmID'], row['year']])
                points_accumulator.add(player_id, int(row['Pts'] or 0))
            cursor.close()
        return points_accumulator

    def _write_points_summary(self, points_accumulator):
        """Given a points_accumulator, inserts points summary rows into the 'points_summary' table."""
        points_summary = points_accumulator.summarize()
        points_summary_inserter = Inserter('points_summary', ('playerId', 'min_pts', 'max_pts', 'avg_pts', 'seasons'))
        cursor = self._db.cursor()
        for key, value in points_summary.iteritems():
            row = [key]
            row.extend(value)
            points_summary_inserter.insert(cursor, row)
        cursor.close()

    def _load_csv(self, table_name, cols, file_name=None):
        """Reads a csv file and writes the contents to a table.

        The csv file and table should have the same column names.
        If the csv file name isn't just the table name in title case, pass in an explicit 'file_name' argument.

        :param table_name: name of the table
        :param cols: a tuple of the columns, in order, in the csv file and table
        :param file_name: (optional) the explicit file name
        :return: None
        """
        file_name = file_name or table_name.title()
        inserter = Inserter(table_name.lower(), cols)
        with open(self._get_csv_fname(file_name), 'r') as csv_file:
            rows = csv.reader(csv_file)
            next(rows)  # skip the header
            cursor = self._db.cursor()
            # for every row in the csv file, insert a row into the corresponding table
            for row in rows:
                inserter.insert(cursor, row)
            cursor.close()

    @staticmethod
    def _get_csv_fname(file_name):
        print('Loading csv: ' + file_name)
        return '../csv/' + file_name + '.csv'


class HockeyStatsReader:

    def __init__(self, _connection):
        self._db = DbUtil(_connection)

    def run_all_queries(self):
        """Runs the queries required by the assessment."""
        self._print_query('coach-ranking', 'Ranking of coaches for each year by number of wins')
        self._print_player_rankings()
        self._print_top_coach_players()

    def _print_player_rankings(self):
        """Using a stored procedure, prints the players by number of awards each year."""
        print('Ranking of players by number of awards each year')
        self._drop_proc('player_rankings_by_awards')
        self._db.execute_sql_files(('create-proc-player-rankings',))
        rows = self._db.get_proc_results('player_rankings_by_awards')
        self._format(rows)
        print()

    def _print_top_coach_players(self):
        """Gets the details of the players who won the maximum number of awards for a year during which the coach for
        that team also had the maximum wins.

        The full query can be found in 'top-coach-players-inline.sql', but the full query has also been factored into
        views, which are defined below and then used in the final query.
        """
        self._define_views()
        self._print_query('top-coach-players', 'Top coach players')

    def _drop_proc(self, name):
        self._db.execute_sql('DROP PROCEDURE IF EXISTS ' + name)

    def _print_query(self, fname, title):
        """Runs the sql query contained in the given file and prints the results."""
        print(title)
        self._format(self._db.fetchall(fname))
        print()

    def _define_views(self):
        """Defines all of the views used by the top-coach-players query."""
        self._db.execute_sql_files((
            'create-view-top-coach-wins',
            'create-view-top-coaches',
            'create-view-yearly-player-award-count',
            'create-view-top-yearly-award-counts',
            'create-view-top-award-players'
        ))

    @staticmethod
    def _format(rows):
        """Prints the given rows in a simple format."""
        for row in rows:
            for col in row:
                print('[' + str(col) + ']', end='')
            print()


if __name__ == '__main__':
    connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)

    loader = HockeyStatsLoader(connection)
    loader.load_csv_into_db()

    reader = HockeyStatsReader(connection)
    reader.run_all_queries()

    connection.close()
