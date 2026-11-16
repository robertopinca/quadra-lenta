"""Popula o banco com o conteudo do blog e os dados pedidos na secao 4.

Uso:
    python manage.py popular_banco

Idempotente: roda quantas vezes quiser, nao duplica nada.

O minimo exigido pelo enunciado, e o que este comando cria:

    3 posts no total, 1 sem comentarios      -> 4 posts, 1 sem comentarios
    2 posts com multiplas categorias         -> 2 posts com duas categorias
    2-3 comentarios nos posts comentados     -> 3, 2 e 2
    3 categorias, cada post em ao menos uma  -> 4 categorias

CREDENCIAL DE DESENVOLVIMENTO: o super-usuario e criado como
admin / saibro1997 . Serve para abrir o /admin/ na maquina local e nada
mais. Troque antes de pos qualquer coisa no ar.
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Category, Comment, Post

User = get_user_model()

SUPERUSUARIO = {'username': 'admin', 'email': 'admin@quadralenta.test', 'senha': 'saibro1997'}

# Leitores do blog. Nunca fazem login: entram so como autor de comentario,
# criados pelo administrador a partir do super-usuario, como pede o enunciado.
LEITORES = [
    ('marcelo_tb', 'Marcelo', 'Arruda'),
    ('ana.saibro', 'Ana', 'Containi'),
    ('dudu1997', 'Eduardo', 'Prado'),
    ('vitoria_bh', 'Vitória', 'Lemes'),
    ('jorge.quadra3', 'Jorge', 'Nakamura'),
]

CATEGORIAS = [
    ('História', 'Partidas e jogadores que valem revisitar, de preferência com o vídeo aberto em outra aba.'),
    ('Grand Slam', 'Os quatro grandes, e a conversa que eles provocam.'),
    ('Análise Tática', 'Padrão de jogo, escolha de golpe, leitura de placar. A parte chata que decide partida.'),
    ('Saibro', 'A superfície que me interessa. Pó, deslize e ponto longo.'),
]


POST_GUGA = """
<p>Toda vez que alguém me pergunta por onde começar a ver tênis antigo eu
mando o mesmo jogo: a final de Roland Garros de 1997. Não porque foi bonita
&mdash; foi, mas não é o ponto. É porque dá para ver, em três sets, um jogador
resolver um problema que ninguém tinha resolvido daquele jeito.</p>

<p>O problema era o backhand. Até ali, o manual do saibro dizia que você
devolve a bola alta de revés com slice, espera, e tenta virar o ponto quando
der. Guga chegou com um backhand de uma mão que <em>atacava</em> a bola alta.
Não aparava: subia na bola e tirava ela da quadra. Contra o Bruguera, que tinha
construído uma carreira ganhando exatamente a troca que o Guga estava se
recusando a jogar.</p>

<div class="placar">
  <div class="placar-cabeca">Final &middot; Roland Garros 1997 &middot; Paris, quadra central</div>
  <table>
    <tr class="vencedor">
      <td class="jogador">Gustavo Kuerten <span class="meta">(BRA)</span></td>
      <td class="sets">6</td><td class="sets">6</td><td class="sets">6</td>
    </tr>
    <tr>
      <td class="jogador">Sergi Bruguera <span class="meta">(ESP)</span></td>
      <td class="sets">3</td><td class="sets">4</td><td class="sets">2</td>
    </tr>
  </table>
  <div class="placar-pe">
    Kuerten entrou no torneio como número 66 do mundo. Saiu campeão.
  </div>
</div>

<p>O detalhe que eu só percebi revendo: ele não ganhou por winners. Ganhou
porque empurrou o Bruguera dois metros para trás da linha de fundo e manteve
ele lá. Quando o espanhol tentou subir, o ponto já estava decidido três bolas
antes.</p>

<h3>Os três títulos em Paris</h3>

<table class="chave">
  <caption>Gustavo Kuerten em Roland Garros &mdash; finais vencidas</caption>
  <thead>
    <tr><th>Ano</th><th>Adversário na final</th><th>Observação</th></tr>
  </thead>
  <tbody>
    <tr class="campeao">
      <td class="fase">1997</td>
      <td>Sergi Bruguera (ESP)</td>
      <td>6/3 6/4 6/2 &mdash; entrou como 66º do ranking</td>
    </tr>
    <tr class="campeao">
      <td class="fase">2000</td>
      <td>Magnus Norman (SWE)</td>
      <td>Ano em que fechou como número 1 do mundo</td>
    </tr>
    <tr class="campeao">
      <td class="fase">2001</td>
      <td>Àlex Corretja (ESP)</td>
      <td>O ano do coração desenhado no saibro</td>
    </tr>
  </tbody>
</table>

<div class="nota">
  <strong>Nota de quem escreve:</strong> os placares set a set de 2000 e 2001 eu
  deixei de fora de propósito. Tenho eles anotados em dois lugares diferentes
  com números diferentes, e preferi não repetir informação que não consegui
  confirmar. Se alguém tiver a fonte boa, manda nos comentários.
</div>

<p>O que me irrita um pouco na conversa sobre o Guga é que ela virou
quase só sobre o coração de 2001. Beleza, foi um gesto bonito. Mas o legado
técnico está em 1997, e está no revés. Quem jogou depois dele e bate de uma mão
no saibro está, de um jeito ou de outro, respondendo àquela final.</p>
"""


POST_SLICE = """
<p>Vou bater numa tecla que me rende discussão toda vez: o slice de backhand
no saibro não é golpe defensivo. Ele é tratado como defensivo porque a maioria
usa ele quando já está em apuros, e aí a estatística confirma a crença. Causa e
efeito invertidos.</p>

<p>Passei as últimas semanas anotando à mão o que acontece depois de cada slice
de revés em jogos de saibro. Não é estudo, é caderno &mdash; vinte partidas,
anotação minha, sujeito a erro meu. Mas o padrão apareceu rápido demais para eu
ignorar.</p>

<table class="stats">
  <caption>Caderno próprio &middot; 20 partidas de saibro &middot; o que vem depois do slice de revés</caption>
  <thead>
    <tr>
      <th>Situação em que o slice foi usado</th>
      <th>Vezes</th>
      <th>Ponto ganho</th>
      <th>Bolas até fechar</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Atrás da linha, sob pressão</td>
      <td>118</td>
      <td>31%</td>
      <td>2,4</td>
    </tr>
    <tr>
      <td>Dentro da quadra, por escolha</td>
      <td>44</td>
      <td class="melhor">63%</td>
      <td class="melhor">1,8</td>
    </tr>
    <tr>
      <td>Como aproximação, subindo à rede</td>
      <td>27</td>
      <td class="melhor">59%</td>
      <td>2,1</td>
    </tr>
    <tr>
      <td>Devolução de segundo saque</td>
      <td>61</td>
      <td>44%</td>
      <td>3,6</td>
    </tr>
  </tbody>
</table>

<p>Olha a segunda linha. Quando o slice é escolha, e não socorro, ele ganha
quase dois terços dos pontos. A bola baixa e com pouco salto obriga o outro a
levantar de baixo para cima no saibro, que é a bola mais difícil de acelerar
que existe nessa superfície. Você não está sobrevivendo: está construindo.</p>

<blockquote>
  Slice bom é o que o adversário tem que levantar. Slice ruim é o que ele pode
  bater na altura do quadril.
</blockquote>

<p>O erro de execução mais comum que eu vejo em quadra de clube é mandar o
slice alto e curto, com medo da rede. Isso entrega a bola no quadril do outro,
na altura perfeita, e aí sim o golpe é defensivo &mdash; defensivo e péssimo.
A margem está em baixo e longo, não em alto e seguro.</p>

<p>Testa numa cesta de bolas antes de me responder que não funciona.</p>
"""


POST_SAIBRO_BR = """
<p>Quem viaja de Paris para uma quadra de clube em São Paulo e espera a mesma
quadra leva um susto. As duas se chamam saibro em português e as duas são
vermelhas, e param aí as semelhanças. O que muda é o que está embaixo.</p>

<p>A <em>terre battue</em> europeia é um sistema de camadas: brita grossa no
fundo, depois um colchão de calcário compactado, e no topo uma película finíssima
de pó de tijolo &mdash; coisa de dois milímetros. Você não desliza no saibro;
desliza <em>na poeira sobre</em> o calcário duro. É por isso que o pé trava no
fim do deslize.</p>

<p>O saibro brasileiro, na média dos clubes, é mais simples e mais fundo.
Camada solta mais espessa, granulometria irregular, muita variação de um clube
para o outro e até de um lado da rede para o outro depois de um jogo de
duplas.</p>

<table class="stats">
  <caption>Na prática, jogando</caption>
  <thead>
    <tr><th>&nbsp;</th><th>Terre battue europeia</th><th>Saibro de clube no Brasil</th></tr>
  </thead>
  <tbody>
    <tr><td>Camada solta</td><td>fina, ~2 mm</td><td>espessa e irregular</td></tr>
    <tr><td>Salto da bola</td><td>alto e previsível</td><td>mais baixo, morre antes</td></tr>
    <tr><td>Deslize</td><td>longo, trava no fim</td><td>curto, o pé afunda</td></tr>
    <tr><td>Depois da chuva</td><td>joga em ~1 h</td><td>depende do sol do dia</td></tr>
  </tbody>
</table>

<p>A consequência tática é grande e quase ninguém fala dela: o <em>loop</em>
alto e pesado, que é ouro em Paris, rende muito menos aqui. A bola sobe, o
salto não acompanha, e você só deu tempo para o outro se organizar. Em quadra
de clube brasileira o que paga é a bola mais plana e mais funda, e a paciência
de jogar três bolas iguais antes de abrir o ângulo.</p>

<div class="nota">
  <strong>Se você joga em clube:</strong> repare na marca do seu pé depois de um
  deslize. Se o pé afundou e deixou um buraco, a camada solta está alta demais e
  o seu jogo de base vai sofrer independente do que você treinou.
</div>

<p>Nada disso é defeito. É outra superfície, com outro jogo certo. O problema é
treinar para uma e competir na outra.</p>
"""


POST_CADERNO = """
<p>Anotação curta, mais para eu não esquecer do que para convencer ninguém.
Quando sai um resultado e todo mundo já tem opinião formada em quinze minutos,
eu olho cinco linhas da súmula antes de abrir a boca:</p>

<ol>
  <li><strong>Pontos ganhos no segundo saque.</strong> Diz mais sobre quem
  controlou o jogo do que o número de aces, que é vaidade.</li>
  <li><strong>Winners contra erros não forçados, mas separados por set.</strong>
  O total da partida esconde a virada, que é justamente o que interessa.</li>
  <li><strong>Pontos de break convertidos sobre criados.</strong> Dois de nove
  e dois de três são partidas completamente diferentes com o mesmo placar.</li>
  <li><strong>Duração média do ponto.</strong> É o jeito mais honesto de saber
  quem estava impondo o ritmo.</li>
  <li><strong>Quem sacou primeiro em cada set.</strong> Óbvio e sempre
  esquecido na hora de julgar um 7/5.</li>
</ol>

<p>Nenhuma dessas aparece na manchete. Todas as cinco aparecem na súmula
oficial, de graça, no mesmo site onde a pessoa leu o placar.</p>
"""


COMENTARIOS = {
    'guga': [
        ('dudu1997',
         'cara eu tinha 11 anos e vi essa final na casa da minha avó, '
         'lembro do meu tio falando "esse menino não ganha do Bruguera nunca". '
         'ganhou em 3 sets. nunca mais ouvi ele falar de tênis'),
        ('ana.saibro',
         'Discordo da parte do legado. O backhand dele era genial mas era '
         'irreproduzível, dependia de um timing que quase ninguém tem. O que '
         'mudou o saibro de verdade foi a mudança nas cordas, não o Guga.'),
        ('marcelo_tb',
         'os placares de 2000 e 2001 estão no site da ITF, dá pra conferir lá. '
         'boa por não ter chutado'),
    ],
    'slice': [
        ('jorge.quadra3',
         'Testei na cesta hoje. Baixo e fundo é MUITO mais difícil de executar '
         'do que você faz parecer, errei umas 15 na rede antes de pegar. mas '
         'quando entra o cara realmente tem que levantar de baixo. convencido'),
        ('ana.saibro',
         'A tabela é interessante mas 44 repetições na linha que você usa pra '
         'provar o argumento é pouca coisa. Com amostra desse tamanho eu não '
         'escreveria "63%" com duas casas de confiança.'),
    ],
    'saibro': [
        ('vitoria_bh',
         'finalmente alguém falando disso. jogo em clube em bh e sempre achei '
         'que meu topspin era ruim, passei anos achando isso. é que a quadra '
         'come a bola mesmo'),
        ('marcelo_tb',
         'detalhe: varia muito com o clube também. tem quadra aqui que depois '
         'de molhar fica mais rápida que piso duro, e no dia seguinte tá '
         'funda de novo. zero previsibilidade'),
    ],
}


class Command(BaseCommand):
    help = 'Popula o blog com posts, categorias, usuarios e comentarios.'

    def handle(self, *args, **options):
        self.stdout.write('Populando o banco...')

        admin = self._criar_superusuario()
        leitores = self._criar_leitores()
        categorias = self._criar_categorias()
        posts = self._criar_posts(categorias)
        self._criar_comentarios(posts, leitores)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Pronto. Resumo do banco:'))
        self.stdout.write(f'  categorias ..... {Category.objects.count()}')
        self.stdout.write(f'  posts .......... {Post.objects.count()}')
        self.stdout.write(f'  comentarios .... {Comment.objects.count()}')
        self.stdout.write(f'  usuarios ....... {User.objects.count()}')
        self.stdout.write('')
        sem = Post.objects.filter(comentarios__isnull=True).count()
        multi = sum(1 for p in Post.objects.all() if p.categorias.count() > 1)
        self.stdout.write(f'  posts sem comentarios .............. {sem}')
        self.stdout.write(f'  posts em mais de uma categoria ..... {multi}')
        self.stdout.write('')
        self.stdout.write(f'  admin em /admin/ ... {admin.username}')

    # ------------------------------------------------------------------ #

    def _criar_superusuario(self):
        admin, criado = User.objects.get_or_create(
            username=SUPERUSUARIO['username'],
            defaults={
                'email': SUPERUSUARIO['email'],
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if criado:
            admin.set_password(SUPERUSUARIO['senha'])
            admin.save()
            self.stdout.write(f'  + super-usuario {admin.username}')
        return admin

    def _criar_leitores(self):
        leitores = {}
        for username, nome, sobrenome in LEITORES:
            usuario, criado = User.objects.get_or_create(
                username=username,
                defaults={'first_name': nome, 'last_name': sobrenome},
            )
            if criado:
                # Nao logam: so assinam comentario.
                usuario.set_unusable_password()
                usuario.save()
                self.stdout.write(f'  + leitor {username}')
            leitores[username] = usuario
        return leitores

    def _criar_categorias(self):
        categorias = {}
        for nome, descricao in CATEGORIAS:
            categoria, criada = Category.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao},
            )
            if criada:
                self.stdout.write(f'  + categoria {nome}')
            categorias[nome] = categoria
        return categorias

    def _criar_posts(self, categorias):
        definicoes = [
            (
                'guga',
                'Guga em 1997: o backhand que ninguém tinha visto',
                POST_GUGA,
                datetime(2026, 9, 14, 21, 40),
                ['História', 'Grand Slam'],
            ),
            (
                'slice',
                'O slice de backhand no saibro não é golpe defensivo',
                POST_SLICE,
                datetime(2026, 10, 7, 8, 15),
                ['Análise Tática', 'Saibro'],
            ),
            (
                'saibro',
                'Por que o saibro brasileiro bate diferente do de Paris',
                POST_SAIBRO_BR,
                datetime(2026, 10, 29, 19, 5),
                ['Saibro'],
            ),
            (
                'caderno',
                'Caderno: as cinco linhas que eu olho num placar',
                POST_CADERNO,
                datetime(2026, 11, 11, 7, 30),
                ['Análise Tática'],
            ),
        ]

        posts = {}
        for chave, titulo, conteudo, quando, nomes_categorias in definicoes:
            post, criado = Post.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'conteudo': conteudo.strip(),
                    'data_postagem': timezone.make_aware(quando),
                },
            )
            if criado:
                post.categorias.set(categorias[n] for n in nomes_categorias)
                self.stdout.write(f'  + post {titulo[:44]}...')
            posts[chave] = post
        return posts

    def _criar_comentarios(self, posts, leitores):
        # Horas escolhidas a dedo para a ordenacao por data ficar visivel na
        # pagina do post: o mais recente aparece primeiro.
        horarios = {
            'guga': [
                datetime(2026, 9, 14, 23, 12),
                datetime(2026, 9, 15, 9, 48),
                datetime(2026, 9, 17, 14, 2),
            ],
            'slice': [
                datetime(2026, 10, 7, 20, 31),
                datetime(2026, 10, 9, 11, 17),
            ],
            'saibro': [
                datetime(2026, 10, 30, 7, 55),
                datetime(2026, 11, 2, 16, 40),
            ],
        }

        for chave, comentarios in COMENTARIOS.items():
            post = posts[chave]
            for (username, texto), quando in zip(comentarios, horarios[chave]):
                _, criado = Comment.objects.get_or_create(
                    post=post,
                    autor=leitores[username],
                    defaults={
                        'texto': texto,
                        'data_postagem': timezone.make_aware(quando),
                    },
                )
                if criado:
                    self.stdout.write(f'  + comentario de {username}')
