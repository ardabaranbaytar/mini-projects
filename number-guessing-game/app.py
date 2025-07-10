from flask import Flask, session, render_template_string, request
import random

app = Flask(__name__)
app.secret_key = 'benimGizliAnahtarim2025'

HTML = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sayı Tahmin Oyunu + Adam Asmaca</title>
    <style>
        :root {
            --bg-gradient-start: #f4f5fa;
            --bg-gradient-end: #d1dae9;
            --container-bg: #ffffff;
            --primary-color: #6366f1;
            --primary-color-dark: #3730a3;
            --secondary-color: #fbbf24;
            --secondary-color-dark: #fde68a;
            --text-dark: #312e81;
            --text-light: #475569;
            --text-on-primary: #ffffff;
            --text-on-secondary: #78350f;
            --border-color: #818cf8;
            --svg-stroke-color: #475569;
            --svg-platform-color: #cbd5e1;
            --success-bg: #bbf7d0;
            --success-text: #166534;
            --fail-bg: #fee2e2;
            --fail-text: #991b1b;
            --hint-bg: #dbeafe;
            --hint-text: #1e293b;
            --shadow-color: rgba(44, 62, 80, 0.1);
            --font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            --border-radius: 12px;
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background: linear-gradient(135deg, #f4f5fa 0%, #d1dae9 100%);
            min-height: 100vh;
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;

            /* Ekle: Ortalamak için */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

    
        .container {
            display: flex; /* İçeriklerin yan yana gelmesi için */
            align-items: flex-start; /* İçerikleri üste hizalar */
            gap: 2rem; /* .game-content ve .hangman-box arasına boşluk */
            width: 100%;
            max-width: 950px;
            background: var(--container-bg);
            padding: 2.5rem;
            border-radius: var(--border-radius);
            box-shadow: 0 10px 25px -5px var(--shadow-color);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .game-content {
            flex: 2; /* Oyun içeriğinin daha fazla yer kaplamasını sağlar */
        }

        .hangman-box {
            flex: 1; /* Adam asmaca kutusunun daha az yer kaplamasını sağlar */
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 1rem;
            min-width: 180px;
        }

        
        h2 {
            text-align: center;
            font-size: 2em;
            margin-top: 0;
            margin-bottom: 30px;
            color: var(--text-dark);
            font-weight: 600;
            line-height: 1.3;
        }

        form {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }

        input[type="number"] {
            width: 90px;
            padding: 10px 15px;
            font-size: 1.1em;
            border: 2px solid var(--border-color);
            border-radius: var(--border-radius) 0 0 var(--border-radius);
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="number"]:focus {
            border-color: var(--primary-color);
        }

        .btn {
            padding: 10px 22px;
            font-size: 1.1em;
            border: none;
            cursor: pointer;
            transition: background-color 0.2s ease, transform 0.1s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
        }

        .btn-primary {
            background: var(--primary-color);
            color: var(--text-on-primary);
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
        }
        .btn-primary:hover {
            background: var(--primary-color-dark);
        }

        .btn-restart {
            background: var(--secondary-color);
            color: var(--text-on-secondary);
            border-radius: var(--border-radius);
            padding: 12px 26px;
            font-size: 1.07em;
            margin-top: 18px;
            font-weight: 500;
        }
        .btn-restart:hover {
            background: var(--secondary-color-dark);
        }
        
        .restart-btn-wrapper {
             display: flex;
             justify-content: center;
        }

        .feedback {
            margin: 15px 0;
            padding: 15px 10px;
            border-radius: var(--border-radius);
            font-size: 1.08em;
            font-weight: 500;
            text-align: center;
        }
        .success { background: var(--success-bg); color: var(--success-text); }
        .fail    { background: var(--fail-bg); color: var(--fail-text); }
        .hint    { background: var(--hint-bg); color: var(--hint-text); }

        .remaining-guesses, .wrong-guesses-count {
            text-align: center;
            font-size: 1.05em;
            font-weight: 500;
        }
        .remaining-guesses { color: var(--primary-color-dark); margin-top: 8px; }
        .wrong-guesses-count { color: var(--text-light); margin-top: 0.5rem; }
        
        .hangman-svg {
            width: 140px;
            height: 210px;
            margin-bottom: 7px;
        }
        .hangman-label {
            font-size: 1.2em;
            color: var(--text-light);
            margin-bottom: 6px;
            font-weight: 500;
        }
        .hangman-part {
            stroke-linecap: round;
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }
        @keyframes fadeIn {
            to { opacity: 1; }
        }

        .platform-part {
            stroke-linecap: round;
        }

        @media (max-width: 768px) {
            body { padding: 1rem; }
            .container {
                flex-direction: column; /* Küçük ekranlarda alt alta diz */
                align-items: center;
                gap: 2.5rem;
                padding: 2rem 1.5rem;
            }
            .game-content {
                width: 100%;
            }
            h2 {
                font-size: 1.5em; /* Mobil için başlığı küçült */
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="game-content">
            <h2>1-100 arasında bir sayı tuttum. 5 tahminde bulabilir misin?</h2>
            
            {% if not bitti %}
            <form method="post">
                <input type="number" name="tahmin" min="1" max="100" required placeholder="Tahminin">
                <button type="submit" class="btn btn-primary">Tahmin Et</button>
            </form>
            {% endif %}
            
            {% if mesaj %}
            <div class="feedback {{ mesaj_turu }}">{{ mesaj }}</div>
            {% endif %}
            
            <div class="remaining-guesses">Kalan hakkın: {{ kalan_hak }}</div>
            
            {% if bitti %}
            <div class="restart-btn-wrapper">
                <form method="get">
                    <button type="submit" class="btn btn-restart">Yeniden Başla</button>
                </form>
            </div>
            {% endif %}
        </div>
        
        <div class="hangman-box">
            <div class="hangman-label">Adam Asmaca</div>
            <svg class="hangman-svg" viewBox="0 0 140 210">
                <line class="platform-part" x1="20" y1="200" x2="120" y2="200" stroke="var(--svg-platform-color)" stroke-width="8"/>
                <line class="platform-part" x1="40" y1="200" x2="40" y2="10" stroke="var(--svg-platform-color)" stroke-width="8"/>
                <line class="platform-part" x1="36" y1="10" x2="70" y2="10" stroke="var(--svg-platform-color)" stroke-width="8"/>
                
                {% if yanlis_sayi > 0 %}
                <line class="hangman-part" x1="70" y1="10" x2="70" y2="40" stroke="var(--svg-stroke-color)" stroke-width="4"/> {% endif %}
                {% if yanlis_sayi > 1 %}
                <circle class="hangman-part" cx="70" cy="60" r="20" fill="none" stroke="var(--svg-stroke-color)" stroke-width="4"/> {% endif %}
                {% if yanlis_sayi > 2 %}
                <line class="hangman-part" x1="70" y1="80" x2="70" y2="135" stroke="var(--svg-stroke-color)" stroke-width="4"/> {% endif %}
                {% if yanlis_sayi > 3 %}
                <line class="hangman-part" x1="70" y1="95" x2="50" y2="120" stroke="var(--svg-stroke-color)" stroke-width="4"/> <line class="hangman-part" x1="70" y1="95" x2="90" y2="120" stroke="var(--svg-stroke-color)" stroke-width="4"/> {% endif %}
                {% if yanlis_sayi > 4 %}
                <line class="hangman-part" x1="70" y1="135" x2="55" y2="170" stroke="var(--svg-stroke-color)" stroke-width="4"/> <line class="hangman-part" x1="70" y1="135" x2="85" y2="170" stroke="var(--svg-stroke-color)" stroke-width="4"/> {% endif %}
            </svg>
            <div class="wrong-guesses-count">Yanlış sayısı: {{ yanlis_sayi }}</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def sayi_tahmin():
    mesaj = ""
    mesaj_turu = "hint"
    if 'sayi' not in session or request.method == 'GET':
        session['sayi'] = random.randint(1, 100)
        session['hak'] = 5
        session['onceki_fark'] = None
        session['yanlis_sayi'] = 0
        mesaj = "Başladık! Tahminini gir."
        mesaj_turu = "hint"
        bitti = False
    else:
        sayi = session['sayi']
        hak = session['hak']
        onceki_fark = session['onceki_fark']
        yanlis_sayi = session['yanlis_sayi']

        tahmin = int(request.form['tahmin'])
        hak -= 1
        fark = abs(sayi - tahmin)

        if tahmin == sayi:
            mesaj = f"🎉 Tebrikler! Doğru bildin. Sayı: {sayi}"
            mesaj_turu = "success"
            bitti = True
            session.clear()
            kalan_hak = hak
            return render_template_string(
                HTML, mesaj=mesaj, kalan_hak=kalan_hak, bitti=bitti, mesaj_turu=mesaj_turu, yanlis_sayi=yanlis_sayi)
        elif tahmin > sayi:
            mesaj = "Daha düşük bir sayı dene."
            mesaj_turu = "hint"
        else:
            mesaj = "Daha yüksek bir sayı dene."
            mesaj_turu = "hint"

        if onceki_fark is not None:
            if fark < onceki_fark:
                mesaj += " 🔥 Daha sıcak! (yaklaştın)"
            elif fark > onceki_fark:
                mesaj += " ❄️ Daha soğuk! (uzaklaştın)"
            else:
                mesaj += " 😐 Aynı uzaklıktasın."
        session['onceki_fark'] = fark

        yanlis_sayi += 1  # Her yanlışta artır
        session['yanlis_sayi'] = yanlis_sayi

        if hak == 0:
            mesaj = f"Üzgünüm, hakkın bitti! Adam asıldı. Doğru sayı: {sayi}"
            mesaj_turu = "fail"
            bitti = True
            session.clear()
            kalan_hak = 0
            return render_template_string(
                HTML, mesaj=mesaj, kalan_hak=kalan_hak, bitti=bitti, mesaj_turu=mesaj_turu, yanlis_sayi=yanlis_sayi)
        else:
            session['hak'] = hak
            kalan_hak = hak
            bitti = False

    kalan_hak = session.get('hak', 5)
    bitti = kalan_hak == 0
    mesaj = locals().get('mesaj', "Tahminini gir.")
    mesaj_turu = locals().get('mesaj_turu', "hint")
    yanlis_sayi = session.get('yanlis_sayi', 0)
    return render_template_string(
        HTML, mesaj=mesaj, kalan_hak=kalan_hak, bitti=bitti, mesaj_turu=mesaj_turu, yanlis_sayi=yanlis_sayi
    )

if __name__ == '__main__':
    app.run(debug=True)
