<div class="container">
<script>setTimeout(function(){window.location.reload(1); }, 4000);</script>
<h1>Ceci est la page qui affiche le résultat de la dernière partie</h1>

  % include('head.html')
<div class="border shadow p-3 mb-5 bg-white rounded text-center">
<p> Nom machine : {{last_game.machine.nom}}</p>
<p> Jeu installe : {{last_game.machine.jeu_installe}} </p>
<p> Durée de la derniere partie {{last_game.duree_jeu}}s </p>
<p> Jouruer Gagnant : {{last_game.gagnant}}</p>
</div>
% include('footer.html')

   <br>
   </div>

