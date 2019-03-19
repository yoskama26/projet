<form action='' method='post'>
    adresse_ip :
    <input type="text" name="adresse_ip" value="{{ config.adresse_ip }}"> <br>

    name_server :
    <input type="text" name="name_server" value="{{ config.name_server }}"> <br>

    game :
    <select name="game">
       <option {{ "selected" if config.game == "morpion" else "" }} value="morpion">Morpion</option>
       <option {{ "selected" if config.game == "puissance 4" else "" }} value="puissance 4">Puissance 4</option>
    </select> <br>

    max player delay :
    <input type="number" name="max_player_delay" value="{{ config.max_player_delay }}"> <br>

    max coin blink delay :
    <input type="number" name="max_coin_blink_delay" value="{{ config.max_coin_blink_delay }}"> <br>

    Victory Blink delay :
    <input type="number" name="victory_blink_delay" value="{{ config.victory_blink_delay }}"> <br>

    Level :
    <input type="number" name="level" value="1" max="5" value="{{ config.level }}"> <br>

    Player 1 color :
    <select name="player1_color">
       <option {{ "selected" if config.player1_color == "bleu" else "" }} value="bleu">Bleu</option>
       <option {{ "selected" if config.player1_color == "vert" else "" }} value="vert">Vert</option>
       <option {{ "selected" if config.player1_color == "rouge" else "" }} value="rouge">Rouge</option>
    </select>
    <br>

    Player 2 color :
    <select name="player2_color">
       <option {{ "selected" if config.player2_color == "bleu" else "" }} value="bleu">Bleu</option>
       <option {{ "selected" if config.player2_color == "vert" else "" }} value="vert">Vert</option>
       <option {{ "selected" if config.player2_color == "rouge" else "" }} value="rouge">Rouge</option>
    </select>
    <br> <br>

   <input type="reset">
   <input type="submit">
</form>