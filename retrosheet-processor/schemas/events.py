import pyarrow as pa


DEFAULT_FIELDS = [
    pa.field("game_id", pa.string()),
]


"""
Info

There are up to 34 info records, each of which contains a single
piece of information, such as the temperature, attendance,
identity of each umpire, etc. The record format is info,type,data.
    
The complete list of info record types is given at
https://www.retrosheet.org/eventfile.htm#1.

    info,attendance,32737
"""
INFO = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("type", pa.string()),
        pa.field("data", pa.string()),
    ],
    metadata={
        "type": """
        The complete list of info record types is given at
            https://www.retrosheet.org/eventfile.htm#1
        """,
        "data": "data associated with info record"
    }
)


"""
Start / Sub

There are 18 (for the NL and pre-DH AL) or 20 (for the AL with the
DH) start records, which identify the starting lineups for the game.
Each start or sub record has five fields:
    1. The first field is the Retrosheet player id, which is unique
        for each player.
    2. The second field is the player's name.
    3. The next field is either 0 (for visiting team), or 1 (for home
        team).
    4. The next field is the position in the batting order, 1 - 9.
        When a game is played using the DH rule the pitcher is given
        the batting order position 0.
    5. The last field is the fielding position. The numbers are in the
        standard notation, with designated hitters being identified as
        position 10. On sub records 11 indicates a pinch hitter and 12
        is used for a pinch runner.

The sub records are used when a player is replaced during a game. The
roster files that accompany the event files include throwing and
batting handedness information.

    start,richg001,"Gene Richards",0,1,7
"""
START_SUB = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("player_id", pa.string()),
        pa.field("player_name", pa.string()),
        pa.field("is_home_team", pa.bool_()),
        pa.field("batting_position", pa.int16()),
        pa.field("fielding_position", pa.int16()),
    ],
    metadata={
        "player_id": "Retrosheet player id",
        "player_name": "Player's name",
        "is_home_team": "either 0 (for visiting team), or 1 (for home team)",
        "batting_position": """
            position in the batting order, 1 - 9. When a game is played using
            the DH rule the pitcher is given the batting order position 0
        """,
        "fielding_position": """
            The numbers are in the standard notation, with designated hitters
            being identified as position 10. On sub records 11 indicates a
            pinch hitter and 12 is used for a pinch runner
        """,
    }
)


"""
Play

The play records contain the events of the game. Each play record has
6 fields:
    1. The first field is the inning, an integer starting at 1.
    2. The second field is either 0 (for visiting team) or 1 (for home
        team).
    3. The third field is the Retrosheet player id of the player at the
        plate.
    4. The fourth field is the count on the batter when this particular
        event (play) occurred. Most Retrosheet games do not have this
        information, and in such cases, "??" appears in this field.
    5. The fifth field is of variable length and contains all pitches to
        this batter in this plate appearance and is described below. If
        pitches are unknown, this field is left empty, nothing is between
        the commas.
    6. The sixth field describes the play or event that occurred.

        play,5,1,ramir001,00,,S8.3-H;1-2

A play record ending in a number sign, #, indicates that there is some
uncertainty in the play. Occasionally, a com record may follow providing
additional information. A play record may also contain exclamation points,
"!" indicating an exceptional play and question marks "?" indicating some
uncertainty in the play. These characters can be safely ignored.

    play,3,1,kearb001,??,,PB.2-3#
    com,"Not sure if PB, may have been balk"

The event is the most complex of all the fields and is described in detail
at https://www.retrosheet.org/eventfile.htm#5
"""
PLAY = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("inning", pa.int16()),
        pa.field("is_home_team", pa.bool_()),
        pa.field("player_id", pa.string()),
        pa.field("batting_count", pa.string()),
        pa.field("pitch_sequence", pa.string()),
        pa.field("play_desc", pa.string()),
    ],
    metadata={
        "inning": "inning, an integer starting at 1",
        "is_home_team": "either 0 (for visiting team), or 1 (for home team)",
        "player_id": "Retrosheet player id of the player at the plate",
        "batting_count": "count on the batter when the play occurred",
        "pitch_sequence": """
            variable length and contains all pitches to this batter in this
            plate appearance
        """,
        "play_desc": "describes the play or event that occurred",
    }
)


"""
Batting Adjustment

This record is used to mark a plate appearance in which the batter bats
from the side that is not expected. The syntax is:
    badj,playerid,hand

The expectation is defined by the roster file. There are two general cases
in which this is used:

    1. Many switch-hitters bat right-handed against right-handed knuckle
        ball pitchers even though the default assumption is that they would
        be batting left-handed.
            
        badj,bonib001,R indicates that switch-hitter Bobby Bonilla was
        batting right-handed against a right-handed pitcher.

    2. Occasionally a player will be listed in a roster as batting "R" or
        "L" but will bat the other way. For example, Rick Dempsey did this
        13 times in 1983. The syntax this is: badj,dempr101,L
"""
BADJ = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("player_id", pa.string()),
        pa.field("hand", pa.string()),
    ],
    metadata={
        "player_id": "Retrosheet player id of the player at the plate",
        "hand": "side when a batter bats that is not expected",
    }
)


"""
Pitching Adjustment

This record covers the very rare case in which a pitcher pitches to a
batter with the hand opposite the one listed in the roster file. To date
this has only happened once, when Greg Harris of the Expos, a right-hander,
pitched left-handed to two Cincinnati batters on 9-28-1995. The syntax is
parallel to that for the badj record: padj,harrg001,L
"""
PADJ = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("player_id", pa.string()),
        pa.field("hand", pa.string()),
    ],
    metadata={
        "player_id": "Retrosheet player id of the pitcher",
        "hand": "side when a pitcher pitches that is not expected",
    }
)


"""
Lineup Adjustment

This record is used when teams bat out of order.
"""
LADJ = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("batting_position_1", pa.int16()),
        pa.field("batting_position_2", pa.int16()),
    ],
)


"""
Runner Adjustment

This record is used in games from 2020 in which an extra inning begins with
a runner on 2nd
"""
RADJ = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("player_id", pa.string()),
        pa.field("base", pa.int16()),
    ],
    metadata={
        "player_id": "Retrosheet player id of the runner on base",
        "base": "Base the runner started on",
    }
)


"""
Data

Data records appear after all play records from the game. At present, the
only data type, field 2, that is defined specifies the number of earned runs
allowed by a pitcher. Each such record contains the pitcher's Retrosheet
player id and the number of earned runs he allowed. There is a data record
for each pitcher that appeared in the game.

    data,er,showe001,2
"""
DATA = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("data_type", pa.string()),
        pa.field("player_id", pa.string()),
        pa.field("value", pa.string()),
    ],
    metadata={
        "data_type": "Statistic that is being presented",
        "player_id": "Retrosheet player id for statistic",
        "value": "Value of statistic",
    }
)


"""
Comment

Used primarily to add explanatory information for a play. However, it may
occur anywhere in a file. The second field of the com record is quoted.

    com,"ML debut for Behenna"
"""
COMMENT = pa.schema(
    DEFAULT_FIELDS + [
        pa.field("text", pa.string()),
    ],
    metadata={
        "text": "Comment text",
    }
)