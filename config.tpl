
<div class="container">
% include('head.html')
    <h1>CONFIGURATION</h1>
<div class="border shadow p-3 mb-5 bg-white rounded">
            <form action="/config" method="post">
                <p>
                    adresse_ip : <input type="text"  name='adresse_ip' value = "0.0.0.0" placeholder="xxx.xxx.xxx.xxx" />
                </p>
                <p>
                    name_server : <input type="text" name='name_server' value = "0" placeholder=""/>
                </p>
                <p>
                    game  : <input type="text" name='game' value = "0" placeholder=""/>
                </p>
                <p>
                    Max player delay : <input type="number" name='Max player delay' step="10" value="0" min="0" max="100"/>
                </p>
                <p>
                    Max coin blink delay: <input type="number" name='Max coin blink delay' step="10" value="0" min="0" max="100" />
                </p>
                <p>
                    Victory blink delay : <input type="number" name='Victory blink delay' step="10" value="0" min="0" max="100" />
                </p>
                <p>
                    level : <input type="number" step="1" name='level' value="0" min="0" max="10" />
                </p>
                 player 1 :
                <select name="nom" size="1">
                <option>rouge
                <option>vert
                <option>bleu
                </select>



                 player 2 :
                <select name="nom" size="1">
                <option>rouge
                <option>vert
                <option>bleu
                </select>


             <div class="text-center">
        <button>Envoyer les modif</button>
            </div>
            </div>
            </form>
           % include('footer.html')
</div>