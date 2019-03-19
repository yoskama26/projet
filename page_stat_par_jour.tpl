<div class="container">
<script>setTimeout(function(){window.location.reload(1); }, 4000);</script>
% include('head.html')
<h1>Ceci est la page des statistiques par jour qui reçoit en parametre la machine {{nom}}</h1>
<div class="border shadow p-3 mb-5 bg-white rounded text-center">
% for item in stats:
   <p> Terminal N° : {{item.machine}}</p>
   <p> Nombres de partie aujord'hui : {{item.nb_partie_jour}}</p>
   <p> Durée moyenne d'une partie : {{item.duree_moy_partie_jour}}</p>
   <p> Nombres de fois que le Joueur 1 a gagné : {{item.nb_fois_gagnant1}} </p>
   <p> Nombres de fois que le Joueur 2 a gagné : {{item.nb_fois_gagnant2}} </p>
   <p> Nombres de fois qu'il y a eu Egalité : {{item.nb_fois_egalite}} </p>
   <br>
% end
</div>
% include('footer.html')
</div>