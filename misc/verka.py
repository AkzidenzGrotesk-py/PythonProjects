#! /usr/bin/python
import cgi, os, random
args = cgi.FieldStorage()

print "Content-type: text/html\n\n"

pageContent = ""
styling = """
            @import url('https://fonts.googleapis.com/css2?family=Castoro:ital@0;1&family=Work+Sans:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&display=swap');
            
            :root {
                --yellow: #ffb300;
                --blue: #2f3e9e;
                --red: #c62828;
            }
        
            html, body {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                height: 100%;
                font-family: "Work Sans", sans-serif;
            }
"""


song_data = {
    'Albania': {'name': 'Fall From The Sky', 'artist': 'Arilena Ara',
                'youtube_link': 'vXpCWFIY6YE'},
    'Israel': {'name': 'Feker Libi (\xe1\x8d\x8d\xe1\x89\x85\xe1\x88\xad \xe1\x88\x8d\xe1\x89\xa4)',
               'artist': 'Eden Adele', 'youtube_link': 'YjzyZZ-oidc'},
    'Australia': {'name': 'Don\xe2\x80\x99t break me ',
                  'artist': 'Montaigne',
                  'youtube_link': 'gr-wWxu4974'},
    'Azerbaijan': {'name': 'Cleopatra', 'artist': 'Efendi',
                   'youtube_link': 'I0VzBCvO1Wk'},
    'Belarus': {'name': 'Da vidna (\xd0\x94\xd0\xb0 \xd0\xb2\xd1\x96\xd0\xb4\xd0\xbd\xd0\xb0)',
                'artist': 'VAL', 'youtube_link': 'F0wfxz5zq04'},
    'Belgium': {'name': 'Release Me', 'artist': 'Hooverphonic',
                'youtube_link': 'lAqjksxc4iA'},
    'Croatia': {'name': 'Divlji vjetre',
                'artist': 'Damir Ked\xc5\xbeo',
                'youtube_link': '2rOwScdxjJU'},
    'Cyprus': {'name': 'Running', 'artist': 'Sandro',
               'youtube_link': 'Jl_qEw_4OK0'},
    'Ireland': {'name': 'Story of my life', 'artist': 'Lesley Roy',
                'youtube_link': 'HLgE0Ayl5Hc'},
    'Lithuania': {'name': 'On Fire', 'artist': 'The Roop',
                  'youtube_link': '1EAUxuuu1w8'},
    'Malta': {'name': 'All of my love', 'artist': 'Destiny',
              'youtube_link': 'CFCn_8oViRw'},
    'North_Macedonia': {'name': 'You', 'artist': 'Vasil',
                        'youtube_link': 'xPZumQQExQc'},
    'Norway': {'name': 'Attention', 'artist': 'Ulrikke',
               'youtube_link': 'o9atJbnqhJU'},
    'Romania': {'name': 'Alcohol You', 'artist': 'ROXEN',
                'youtube_link': 'TmqSU3v_Mtw'},
    'Russia': {'name': 'Uno', 'artist': 'Little Big',
               'youtube_link': 'L_dWvTCdDQ4'},
    'Slovenia': {'name': 'Voda', 'artist': 'Ana Sokli\xc4\x8d',
                 'youtube_link': 'weLeotNwexg'},
    'Sweden': {'name': 'Move', 'artist': 'The Mamas',
               'youtube_link': '7EpSBDPlZn4'},
    'Ukraine': {'name': 'Solovey', 'artist': 'Go_A',
                'youtube_link': 'zNetXPSld50'},
    'United_Kingdom': {'name': 'My Last Breath',
                       'artist': 'James Newman',
                       'youtube_link': '6iS-lV909T4'},
    'France': {'name': 'Mon Alli\xc3\xa9e (The Best In Me)',
               'artist': 'Tom Leeb', 'youtube_link': 'J5SOdhXjYko'},
    'Italy': {'name': 'Fai Rumore', 'artist': 'Diodato',
              'youtube_link': 'Ogyi0GPR_Ik'},
    'The_Netherlands': {'name': 'Grow', 'artist': 'Jeangu Macrooy',
                    'youtube_link': 'Q1T96jNHjXE'},
    'Germany': {'name': 'Violent Thing', 'artist': 'Ben Dolic',
                'youtube_link': 'hAobDQ9GbT4'},
    'Spain': {'name': 'Universo', 'artist': 'Blas Cant\xc3\xb3',
              'youtube_link': 'zuDdex1st'},
    'Armenia': {'name': 'Chains on You', 'artist': 'Athena Manoukian',
                'youtube_link': 'XpQHGMM8c5U'},
    'Austria': {'name': 'Vincent Bueno', 'artist': 'Alive',
                'youtube_link': 'cOuiTJlBC50'},
    'Bulgaria': {'name': 'Tears Getting Sober', 'artist': 'Victoria',
                 'youtube_link': 'V_hgYnwZR8I'},
    'Czech_Republic': {'name': 'Kemama', 'artist': 'Benny Cristo',
                        'youtube_link': 'wROqCHLnbko'},
    'Denmark': {'name': 'Yes', 'artist': 'Ben & Tan',
                'youtube_link': 'XQ5tMhQIp1E'},
    'Estonia': {'name': 'What Love is', 'artist': 'Uku Suviste',
                'youtube_link': 'z4I3vvQzQ-E'},
    'Finland': {'name': 'Looking Back', 'artist': 'Aksel',
                'youtube_link': 'EgONBKFQpxE'},
    'Georgia': {'name': 'Take me as I am', 'artist': 'Tornike Kipiani',
                'youtube_link': 'LjNK4Xywjc4'},
    'Greece': {'name': 'Supergirl', 'artist': 'Stefania',
               'youtube_link': 'dJxCINWp_j0'},
    'Iceland': {'name': 'Think about Things',
                'artist': 'Da\xc3\xb0i og Gagnamagni\xc3\xb0',
                'youtube_link': '1HU7ocv3S2o'},
    'Latvia': {'name': 'Still Breathing',
               'artist': 'Samanta T\xc4\xabna',
               'youtube_link': '_46gTi8Ut0U'},
    'Moldova': {'name': 'Prison', 'artist': 'Natalia Gordienko',
                'youtube_link': 'RnD1ApDo5_k'},
    'Poland': {'name': 'Empires', 'artist': 'Alicja',
               'youtube_link': 's_Y7mMka4SQ'},
    'Portugal': {'name': 'Medo de Senthir', 'artist': 'Elisa',
                 'youtube_link': 'eIZ48w4epng'},
    'San_Marino': {'name': 'Freaky', 'artist': 'Senhit',
                   'youtube_link': 'c6ZNo_hVA6E'},
    'Serbia': {'name': 'Hasta la Vista', 'artist': 'Hurricane',
               'youtube_link': '8Y0cczOeznQ'},
    'Switzerland': {'name': 'R\xc3\xa9pondez-moi',
                    'artist': 'Gjon\xe2\x80\x99s Tears',
                    'youtube_link': 'O9GAfFHZE-E'},
}

# user=USERNAME
username = args.getvalue("code")
scores_post = args.getvalue("score_data")
cards_post = args.getvalue("cards_data")

if not username:
    styling += """
            .main {
                display: grid;
                grid-template-columns: auto;
                height: 100%;
            }
            
            .container {
                display: grid;
                justify-content: center;
                align-content: center;
                text-align: center;
                height: 100%;
                background: #181A1B;
            }
            
            .container h1 {
                background: -webkit-linear-gradient(135deg, var(--blue), var(--yellow));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 64px;
                margin-bottom: 8px;
            }
            
            form input[type="text"] {
                border: none;
                background: inherit;
                padding: 8px;
                text-align: center;
                background: -webkit-linear-gradient(225deg, var(--blue), var(--yellow));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: "Castoro", serif;
                font-size: 16px;
            }
            
            form input[type="text"]:hover {
                font-style: italic;
            }
            
            form input[type="submit"] {
                border: none;
                background: -webkit-linear-gradient(225deg, var(--blue), var(--yellow));
                text-align: center;
                font-family: "Work Sans", sans-serif;
                font-size: 16px;
                padding: 8px 16px;
                margin-top: 8px;
                border-radius: 4px;
                color: #181A1B;
                font-weight: bold;
                cursor: pointer;
            }
    """
    pageContent += """
        <div class="main">
            <div class="container">
                <h1>Verka Verka</h1>
                <form action="verka.py">
                    <input type="text" id="fname" name="code" value="AdamSmith">
                    <br/>
                    <input type="submit" value="Begin Ranking!">
                </form>
            </div>
        </div>
    """
else:
    vc_file = "verka/vc_" + username + ".dat"
    vp_file = "verka/vp_" + username + ".dat"
    
    CARDS = []
    BOARD = {}
    
    if not os.path.isfile(vc_file):
        with open("verka/default_vc.dat", "r") as dvcfile: 
            with open(vc_file, "w") as vcffile:
                vcffile.write(dvcfile.read())
            
        with open("verka/default_vp.dat", "r") as dvpfile: 
            with open(vp_file, "w") as vpffile:
                vpffile.write(dvpfile.read())
                
    if scores_post and cards_post:
        with open(vp_file, "w") as vpffile:
            vpffile.write(scores_post.replace("-","\n"))
    
        with open(vc_file, "w") as vcffile:
            vcffile.write(cards_post.replace("-","\n"))
            
        
    
    with open(vc_file, "r") as vcfile:
        v_cards = vcfile.read().split("\n")
        
        for i, v in enumerate(v_cards):
            v_cards[i] = v.strip()
            
        if "" in v_cards: v_cards.remove("")
        
    with open(vp_file, "r") as vpfile:
        v_points = vpfile.readlines()
    
        for i, p in enumerate(v_points):
            v_points[i] = p.strip().split(" ")
            v_points[i][1] = int(v_points[i][1])
            BOARD[v_points[i][0]] = v_points[i][1]
    
    CARDS = v_cards
        
    card1 = random.choice(CARDS)
    CARDS.remove(card1)
    card2 = random.choice(CARDS)
    CARDS.remove(card2)
        
            
    
    
    styling += """
            .main {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                height: 100%;
            }
            
            .container {
                display: grid;
                justify-content: center;
                align-content: center;
                text-align: center;
                height: 100%;
                padding: 32px;
            }
            
            .container iframe {
                border: none;
                display: block;
                
            }
            
            .container em {
                margin-top: 32px;
            }
            
            .container .ch {
                border-radius: 50%;
                width: 36px;
                height: 36px;
                padding: 8px;
            
                background: inherit;
                text-align: center;
            
                font: 32px "Work Sans", sans-serif;
                
                display: table;
                margin: 0 auto;
            }
            
            .container .chA {
                border: 2px solid #000;
                color: #000;
            }
            
            .container .chB {
                border: 2px solid #fff;
                color: #fff;
            }
            
            .choiceA {
                background: var(--yellow);
                color: #000;
            }
            
            .choiceB {
                background: var(--blue);
                color: #fff;
            }
            
            h1 {
                margin: 0;
                font-weight: 900;
                margin-bottom: 8px;
                font-size: 42px;
                font-family: Castoro, serif;
                font-style: italic;
            }
            
            h3 {
                margin: 0;
                font-weight: bold;
                margin-bottom: 32px;
            }
            
            .footer {
                width: 100%;
                text-align: center;
                padding-top: 96px;
                padding-bottom: 72px;
                background: #181A1B;
                color: #fff;
            }
            
            .footer #cards_left {
                font-weight: 900;
                font-style: italic;
            }
            
            .footer #stats {
                text-align: left;
                margin: 0 30%;
            }
            
            @media (max-width:1172px){
                .main {
                    grid-template-columns: auto;
                }
                .footer {
                    display: none;
                }
            }"""
            
    pageContent += """
        <div class="main">
            <div class="container choiceA">
                <span class="ch chA">1</span>
                <br/>
                <iframe src="https://www.youtube.com/embed/""" + song_data[card1]["youtube_link"] + """" width="520" height="415"></iframe>
                <em>press <, q or 1</em>
                <h1>""" + song_data[card1]["name"] + """</h1>
                <h3>""" + song_data[card1]["artist"] + """</h3>
            </div>
            <div class="container choiceB">
                <span class="ch chB">2</span>
                <br/>
                <iframe src="https://www.youtube.com/embed/""" + song_data[card2]["youtube_link"] + """" width="520" height="415"></iframe>
                <em>press >, w or 2</em>
                <h1>""" + song_data[card2]["name"] + """</h1>
                <h3>""" + song_data[card2]["artist"] + """</h3>
            </div>
        </div>
        
        <div class="footer">
            <div id="cards_left">... cards remaining.</div>
            
            <h1>Stats</h1>
            <div id="stats">
                ...
            </div>
        </div>
        
        <div style="text-align: center;background: #181A1B;">.</div>
        
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script type="text/javascript">
            var __d = new Date();
            var __n = __d.getTime();
            var seed =  __n;
        
            function randomDraw(choices) {
                seed += 0xe120fc15;
                let index = Math.floor(Math.random() * choices.length);
                let card = choices[index];
                choices.splice(index, 1);
                return card;
            }
            
            var song_data = """ + str(song_data) + """;
            var board = """ + str(BOARD) + """;
            var cards = """ + str(CARDS) + """;
            
            var card1 = '""" + card1 + """';
            var card2 = '""" + card2 + """';
            
            var username = '""" + username + """';
            
            function newSongs() {
                if (cards.length < 2) {
                    if (cards.length == 1) {
                        lcard = cards[0];
                        cards = Object.keys(board);
                        cards.push(lcard);
                    } else {
                        cards = Object.keys(board);
                    }
                }
            
                card1 = randomDraw(cards);
                // console.log(cards);
                card2 = randomDraw(cards);
                // console.log(cards);
                
                document.getElementsByClassName("choiceA")[0].innerHTML = '<span class="ch chA">1</span><br/><iframe src="https://www.youtube.com/embed/' + song_data[card1]["youtube_link"] + '" width="520" height="415"></iframe><em>press <, q or 1</em><h1>' + song_data[card1]["name"] + '</h1><h3>' + song_data[card1]["artist"] + '</h3>';
                
                document.getElementsByClassName("choiceB")[0].innerHTML = '<span class="ch chB">2</span><br/><iframe src="https://www.youtube.com/embed/' + song_data[card2]["youtube_link"] + '" width="520" height="415"></iframe><em>press >, w or 2</em><h1>' + song_data[card2]["name"] + '</h1><h3>' + song_data[card2]["artist"] + '</h3>';
            }
            
            function leftChosen() {
                board[card1] += 1;
                // console.log(card1);
                newSongs();
            }
            
            function rightChosen() {
                board[card2] += 1;
                // console.log(card2);
                newSongs();
            }
        
            $(document).ready(function(){
              $("body").keydown(function(event){ 
                let eW = event.which;
                /* Left side */
            	if (eW == 188 || eW == 81 || eW == 49) {
            		leftChosen();
            	}
            	/* Right side */
            	else if (eW == 190 || eW == 87 || eW == 50) {
            		rightChosen();
            	}
            	
            	/* Saving */
            	if (eW == 13) {
            	    let cards_string = "";
            	    let scores_string = "";
            	    
            	    for (let i = 0; i < cards.length; i++) {
            	        cards_string += cards[i] + "-";
            	    }
            	    cards_string += card1 + "-";
            	    cards_string += card2 + "-";
            	    
            	    for (const [key, value] of Object.entries(board)) {
            	        scores_string += key + "+" + value + "-";
                    }
                    
                    cards_string = cards_string.substring(0, cards_string.length - 1);
                    scores_string = scores_string.substring(0, scores_string.length - 1);
                    
                    
                    
                    let link = "https://kumaneko.ca/k/verka.py?code=" + username + "&score_data=" + scores_string + "&cards_data=" + cards_string;
                    
                    window.location.href = link;
            	}
            	
            	document.getElementById("cards_left").innerText = cards.length + " cards remaining."
            	
            	// Create items array
                var items = Object.keys(board).map(function(key) {
                  return [key, board[key]];
                });
                
                // Sort the array based on the second element
                items.sort(function(first, second) {
                  return second[1] - first[1];
                });
                
                let out = "";
                for (let i = 1; i < items.length+1; i++) {
                    if (cards.includes(items[i-1][0])) {
                        out += "<b>" + i + ". <em>" + items[i-1][0].replace("_", " ") + "</em></b> - " + items[i-1][1] + "<br/>";
                    }
                    else {
                        out += "[x] <b>" + i + ". " + items[i-1][0].replace("_", " ") + "</b> - " + items[i-1][1] + "<br/>";
                    }
                }
                
            	document.getElementById("stats").innerHTML = out;
              });
            });
        </script>
    """

print """
<!doctype html>
<html>
    <head>
        <title>Verka Verka</title>
        <meta charset="utf-8" />
        <style>
""" + styling + """
        </style>
    </head>
    <body>
""" + pageContent + """
    </body>
</html>

"""
