from bottle import route, run, template, post, request, redirect
from models import GameServerConfig
from models import StatsPerDay
from models import StatsPerMatch
from models import ReceivedMessage


@route('/config/<nom_machine>')
def config_machine(nom_machine):
    obj = GameServerConfig.get(GameServerConfig.name_server == nom_machine)
    return template('config2.tpl', config=obj)

@post('/config/<nom_machine>')
def config_machine(nom_machine):
    print(dict(request.forms))
    obj = GameServerConfig.update(**request.forms).where(GameServerConfig.name_server == nom_machine)
    obj.execute()
    redirect('/config/'+nom_machine)


@route('/gameservers')
def gameservers():
    return template('page_game_servers.html', Serveurs_info=GameServerConfig.select())


@route('/config')
def config():
    return template('config.tpl')


@route('/page_stats_day/<nom_machine>')
def page_stats_day(nom_machine):
    return template('page_stat_par_jour.tpl', nom=nom_machine, stats=StatsPerDay.select())


@route('/spm')
def index_robin():
    return template('index_robin.html', name='Robin', Stats_list=StatsPerMatch.select())


@route('/page_last_game')
def page_last_game():
    try:
        last_result = StatsPerMatch.select().order_by(StatsPerMatch.date_debut.desc())[0]

    except IndexError:
        last_result = None
    return template('page_last_game.html', last_game=last_result)


@route('/page_message_received')
def message_received():
    return template('page_message_received.html', message_recu=ReceivedMessage.select())


if __name__=='__main__':
    run(debug=True, reloader=True)
