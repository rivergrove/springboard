import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import dataframe_image as dfi
engine = create_engine('postgresql://postgres:Virginia0@localhost:5432/anthonyolund')

def run_query(con, table_name, query):
    """ 
    Executes query on PostgreSQL database server 
    I will use this to create tables
    """
    
    try:
        # connect to the PostgreSQL server
        print(f'loading {table_name} to the PostgreSQL database...')
        con.execute(query.format(table_name, table_name))
        print(f'{table_name} loaded')

    except Exception as error:
        print(error)

def create_tables():
    
    # make table for one move checkmate games
    run_query(engine, 'one_move_cm_games',
        '''
        drop table if exists {};
        create table {} as (
        select
            distinct g.*
        from
            games g
            join moves m
                on g.game_id = m.game_id
                and m.eval in ('#1','#-1')
        )
        ''')
    
    # make table for one move checkmate game moves
    run_query(engine, 'one_move_cm_game_moves',
        '''
        drop table if exists {};
        create table {} as (
        select
            m.*
        from
            one_move_cm_games g
            join moves m
                on g.game_id = m.game_id
        )
        ''')
    
    # Percent of checkmate in 1 that are found
    run_query(engine, 'one_move_cm_moves',
        ''' 
        drop table if exists {};
        create table {} as (
        with temp as (
        select 
            *
            , lead(case when right(move,1) = '#' then 'found' else 'missed' end) over (partition by game_id order by move_number) as checkmate_in_one_found
        from 
            one_move_cm_game_moves
        )
        select 
            *
        from
            temp
        where 
            (eval = '#1' and white = 0 or eval = '#-1' and white = 1)
            and checkmate_in_one_found is not null
        )
        ''')
    
    # Games where a player missed a checkmate in 1 and lost next turn. Game with highest rated player.
    run_query(engine, 'one_move_cm_losses',
        '''
        drop table if exists one_move_cm_losses;
        create table one_move_cm_losses as (
        with temp as (
        select 
            *
            , lead(eval) over (partition by game_id order by move_number) as next_eval
        from 
            one_move_cm_game_moves
        )
        select 
            case when eval = '#1' then white_elo 
            when eval = '#-1' then black_elo
            end as losing_elo
            , t.*
        from
            temp t
            join one_move_cm_games g
                on t.game_id = g.game_id
        where 
            eval = '#1' and t.white = 0 and next_eval = '#-1' 
            or eval = '#-1' and t.white = 1 and next_eval = '#1'
        order by 1 desc
        )
        ''')
    print('all tables created')
    
def pie_games_by_termination():
    # % of games that have a checkmate in one, % of games that end in checkmate, % of games that end in time forfeit
    df = pd.read_sql(
        '''
        with end_in_checkmate as (
        select
            count(distinct g.game_id) as games
        from
            games g
            join moves m
                on g.game_id = m.game_id
                and right(m.move,1) = '#'
        )
        , temp as (
        select
            (select games from end_in_checkmate) as checkmate
            , (select count(*) from games where termination = 'Time forfeit') as time_forfeit
        )
        select 
            *
            , (select count(*) as games from games) - checkmate - time_forfeit as resignation
        from 
            temp
        ''', con=engine).T

    # create plot
    df.index.name = 'termination type'
    df.columns = ['games']
    plot = df.plot.pie(y='games',
                         labels=None, ylabel='', 
                         title="% Games by Termination Type",
                         autopct='%.1f%%'
                        )
    fig = plot.get_figure()
    file = "plots/termination_type.png"
    fig.savefig(file)
    print(f'{file} written')
    
def pie_pct_games_checkmate_in_one():
    # pct games with checkmate in 1
    df = pd.read_sql(
    '''
    select
        case when o.game_id is not null then 'True' else 'False' end as game_has_checkmate_in_one
        , count(*) as games
    from
        games g 
        left join one_move_cm_games o
            on g.game_id = o.game_id
    group by 1
    ''', con=engine)
    df.index=df['game_has_checkmate_in_one']
    plot = df.plot.pie(y='games',
                       labels=None,
                       ylabel='', 
                       title="Games has Checkmate in One",
                       autopct='%.1f%%'
                       )
    fig = plot.get_figure()
    file = "plots/pct_checkmate_in_one_games.png"
    fig.savefig(file)
    print(f'{file} written')

def pie_pct_checkmate_in_one_found():
    df = pd.read_sql('''
    select
        checkmate_in_one_found
        , count(*) as checkmates
    from 
        one_move_cm_moves
    group by 1
    ''', con=engine)
    df.index=df['checkmate_in_one_found']
    plot = df.plot.pie(y='checkmates',
                       labels=None,
                       ylabel='', 
                       title="% Checkmate in One Found",
                       autopct='%.1f%%'
                       )
    fig = plot.get_figure()
    file = "plots/pct_checkmate_in_one_found.png"
    fig.savefig(file)
    print(f'{file} written')
    
def pie_my_pct_checkmate_in_one_found():
    # my games
    # make table for one move checkmate games
    df = pd.read_sql(
        '''
        with rivergrove_one_move_cm_games as (
        select
            distinct g.*
        from
            rivergrove_games g
            join rivergrove_moves m
                on g.game_id = m.game_id
                and m.eval in ('#1','#-1')
        )
        , rivergrove_one_move_cm_game_moves as (
        select
            m.*
        from
            rivergrove_one_move_cm_games g
            join rivergrove_moves m
                on g.game_id = m.game_id
        )
        , temp as (
        select 
            *
            , lead(case when right(move,1) = '#' then 'found' else 'missed' end) over (partition by game_id order by move_number) as checkmate_in_one_found
        from 
            rivergrove_one_move_cm_game_moves
        )
        , rivergrove_one_move_cm_moves as (
        select 
            *
        from
            temp
        where 
            (eval = '#1' and white = 0 or eval = '#-1' and white = 1)
            and checkmate_in_one_found is not null
        )
        select
            checkmate_in_one_found
            , count(*) as checkmates
        from 
            rivergrove_one_move_cm_moves
        group by 1
    ''', con=engine)
    df.index=df['checkmate_in_one_found']
    plot = df.plot.pie(y='checkmates',
                       labels=None,
                       ylabel='', 
                       title="My % Checkmate in One Found",
                       autopct='%.1f%%'
                       )
    fig = plot.get_figure()
    file = "plots/my_pct_checkmate_in_one_found.png"
    fig.savefig(file)
    print(f'{file} written')
    
def bar_pct_checkmate_in_one_found_by_game_type():
    # cut by game_type
    df = pd.read_sql('''
    select
        game_type
        , count(case when checkmate_in_one_found = 'found' then 1 end) * 100. / count(*) as checkmate_found_pct
    from 
        one_move_cm_moves m
        join one_move_cm_games g
            on m.game_id = g.game_id
    group by 1
    order by 2
    ''', con=engine)
    plot = df.plot.bar(x='game_type', 
                y='checkmate_found_pct', 
                ylabel='checkmate found %',
                title = '% 1 Move Checkmates Found by Game Type',
                legend=None
               )
    for p in plot.patches:
        plot.annotate(str(round(p.get_height(),1)), ((p.get_x()+.1) * 1.005, p.get_height() * 1.005))
    plot.yaxis.set_major_formatter(mtick.PercentFormatter())
    fig = plot.get_figure()
    file = "plots/pct_checkmate_in_one_found_pct_by_game_type.png"
    fig.savefig(file)
    print(f'{file} written')
    
def bar_pct_checkmate_in_one_found_by_elo():
    # cut by rating
    df = pd.read_sql('''
    select
        floor(case when eval = '#1' then white_elo else black_elo end / 100)::int * 100 as player_elo
        , count(case when checkmate_in_one_found = 'found' then 1 end) * 100.0 / count(*) as checkmate_found_pct
    from 
        one_move_cm_moves m
        join one_move_cm_games g
            on m.game_id = g.game_id
    group by 1
    order by 1
    ''', con=engine)
    plot = df.plot.bar(x='player_elo', 
                y='checkmate_found_pct', 
                ylabel='checkmate found %',
                title = '% 1 Move Checkmates Found by Player Elo',
                legend=None
               )
    plot.yaxis.set_major_formatter(mtick.PercentFormatter())
    fig = plot.get_figure()
    file = "plots/pct_checkmate_in_one_found_pct_by_elo.png"
    fig.savefig(file)
    print(f'{file} written')
    
def run_bar_chart_for_each_game_type():
    # cut by rating and game type
    def bar_pct_checkmate_in_one_by_elo_and_game_type(game_type):
        df = pd.read_sql('''
        select
            game_type
            , floor(case when eval = '#1' then white_elo else black_elo end / 100)::int * 100 as player_elo
            , count(case when checkmate_in_one_found = 'found' then 1 end) * 100.0 / count(*) as checkmate_found_pct
        from 
            one_move_cm_moves m
            join one_move_cm_games g
                on m.game_id = g.game_id
        where game_type = '{}'
        group by 1,2
        order by 2
        '''.format(game_type), con=engine)
        plot = df.plot.bar(x='player_elo',  
                    y='checkmate_found_pct', 
                    ylabel='checkmate found %',
                    title = '{} % 1 Move Checkmates Found by Player Elo'.format(game_type),
                    legend=None
                   )
        plot.yaxis.set_major_formatter(mtick.PercentFormatter())
        fig = plot.get_figure()
        file = "plots/pct_checkmate_in_one_found_pct_by_elo_&_game_type={}.png".format(game_type)
        fig.savefig(file)
        print(f'{file} written')
    
    game_types = pd.read_sql('''
        select distinct game_type
        from one_move_cm_games
        ''', con=engine)
    for index, row in game_types.iterrows():
        bar_pct_checkmate_in_one_by_elo_and_game_type(row['game_type'])

def pie_result_by_missed_checkmate_in_one():        
    # Result of games where player missed a checkmate in one
    df = pd.read_sql('''
    select
        case 
        when eval = '#1' and result = '1-0' or eval = '#-1' and result = '0-1' then 'win'
        when eval = '#1' and result = '0-1' or eval = '#-1' and result = '1-0' then 'loss'
        when result = '1/2-1/2' then 'draw'
        else 'error'
        end as game_result
        , count(distinct g.game_id)
    from 
        one_move_cm_moves m
        join one_move_cm_games g
            on m.game_id = g.game_id
            and checkmate_in_one_found = 'missed'
    group by 1
    ''', con=engine)
    df.index=df['game_result']
    plot = df.plot.pie(y='count',
                       labels=None,
                       ylabel='', 
                       title="Result of Games Where Player Missed a Checkmate in One",
                       autopct='%.1f%%'
                       )
    fig = plot.get_figure()
    file = "plots/result_by_checkmate_in_one_missed.png"
    fig.savefig(file)
    print(f'{file} written')
    
def reveral_of_fortune():
    # Reversal of Fortune
    # ten games with highest elo players to go from checkmate in one to losing by checkmate in one the next turn
    df = pd.read_sql('''
    select 
        *
    from 
        one_move_cm_losses
    limit 10
    ''', con=engine)
    file = "plots/highest_elo_one_move_checkmate_losses.png"
    dfi.export(df, file)
    print(f'{file} written')

def reveral_of_fortune_frequency():
    # frequency of the ultimate reversal of fortune
    df = pd.read_sql('''
    select
    '1 in ' || 
    ((select count(*) from games) / (select count(*) from one_move_cm_losses))::varchar || 
    ' games go from checkmate in one to losing by checkmate in one the next turn' as col
    ''', con=engine)
    print(df.iloc[0]['col'])
    
def players_with_most_games_and_perfect_checkmate_in_one_pct():
    # Players with the most games and a perfect checkmate in 1 pct
    df = pd.read_sql('''
    select
        case when m.white = 0 and eval = '#1' then g.white
        when m.white = 1 and eval = '#-1' then g.black
        end as player_name
        , max(case when m.white = 0 and eval = '#1' then white_elo
        when m.white = 1 and eval = '#-1' then black_elo
        end) as max_player_elo
        , count(*) checkmate_in_one_games
        , count(case when checkmate_in_one_found = 'found' then 1 end) * 100 / 
        count(*) as pct_checkmate_in_one_found
    from 
        one_move_cm_moves m
        join one_move_cm_games g
            on m.game_id = g.game_id
            and (m.white = 0 and eval = '#1' or m.white = 1 and eval = '#-1')
    group by 1
    having 
        count(case when checkmate_in_one_found = 'found' then 1 end) * 1.0 / count(*) = 1
    order by 3 desc, 2 desc
    limit 10
    ''', con=engine)
    file = "plots/players_with_most_games_&_perfect_checkmate_in_one_pct.png"
    dfi.export(df,file)
    print(f'{file} written')
    
def run_visualizations():
    create_tables()
    pie_games_by_termination()
    pie_pct_games_checkmate_in_one()
    pie_pct_checkmate_in_one_found()
    pie_my_pct_checkmate_in_one_found()
    bar_pct_checkmate_in_one_found_by_game_type()
    bar_pct_checkmate_in_one_found_by_elo()
    run_bar_chart_for_each_game_type()
    pie_result_by_missed_checkmate_in_one()
    reveral_of_fortune()
    reveral_of_fortune_frequency()
    players_with_most_games_and_perfect_checkmate_in_one_pct()