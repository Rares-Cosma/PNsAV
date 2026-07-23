<h1 style="text-align:center;">PNsAV UI/UX Brief</h1>
## 1. Project Scope
### 1.1 PNsAV

PNsAV este un program menit să preia text în limbaj natural transformându-l intern în structuri argumentative de tip ASPIC+ (vezi lucrările lui Sanjay Modgil și Henry Prakken pentru mai multe detalii), folosindu-le apoi pentru a dovedi validitatea lor, a permite vizualizarea structurată a argumentelor și de a oferi o perspectivă clară asupra analizei. Acesta folosește un complex de agenți AI (LLM-uri din API-ul OpenAI, mai specific, gpt 5.4) pentru a parsa textul în vederea construirii structurilor ASPIC+, dar și metode simbolice, manuale pentru a valida, îmbunătăți și curăța structurile. Utilizările programului sunt vaste, și evidente în logică și drept.
### 1.2 UI/UX

UI/UX (= User Interface/User Experience) reprezintă modul prin care utilizatorul interacționează cu programul. Mai specific, UI reprezintă tot ce se poate vedea, adică culori, fonturi, spațierea textului și designul butoanelor și al graficelor. Pentru proiectul nostru vei avea în vedere teme dark/light, palete de culori, design, așezare în pagină, afișarea graficelor, etc. UX pe de altă parte ține de experienta utilizatorului când folosește programul. Aici vei avea în vedere ca programul să fie intuitiv de utilizat și rapid. Numim această componentă de UI/UX a programului frontend, backendul fiind partea de procesare, care furnizează datele afișate de frontend.

## 2. Tech Stack (tehnologii folosite)

Limbajul de programare folosit o să fie Python, fiind un limbaj simplu de utilizat, perfect pentru LLM-uri și AI. Este limbajul pe care se bazează și partea de backend, asa că integrarea datelor în frontend o sa fie ușoară.

Cât despre tehnologii utilizate pentru interfață, optiunile sunt practic infinite. Ai aici o comparație între niște variante:

| Tehnologie          | Tip Aplicație    | Dificultate    | Suport Grafice & Date           | Avantaje Core                                                 | Dezavantaje                                                      |
| :------------------ | :--------------- | :------------- | :------------------------------ | :------------------------------------------------------------ | :--------------------------------------------------------------- |
| **Streamlit**       | Web App          | Ușoară         | Excelent (Nativ)                | Execuție secvențială (fără OOP), grafice instant interactive. | Design vizual rigid (greu de mutat elemente pixel cu pixel).     |
| **CustomTkinter**   | Desktop (`.exe`) | Medie          | Mediu (Cere librării extra)     | Aplicație nativă, control total pe așezarea în pagină.        | Cere înțelegerea conceptului de Layout Grid și funcții Callback. |
| **Dash (Plotly)**   | Web App          | Medie-Ridicată | Cel mai bun (Creat pentru date) | Grafice extrem de complexe și interactivitate totală.         | Cod mai abstract                                                 |
| **PyQt6 / PySide6** | Desktop          | Ridicată       | Complet dar complex             | Standardul industrial pentru aplicații desktop masive.        | Obligă folosirea Claselor și OOP rigid din primul minut.         |
Consider Streamlit ca fiind cea mai bună alegere.
## 3. De ce avem nevoie?

Pentru a face frontendul ai nevoie de definiții clare pentru datele primite. Prima pagină ar trebui să aibă posibilitatea de a introduce text, sau fișier text, sau (dacă e timp) să încarce un proiect deja existent. Pe partea de date o sa ai un graf orientat aciclic reprezentând argumentele (apasand pe noduri ar trebui sa se vada detaliile argumentului) și relațiile dintre ele, o listă de logs pentru sistem, textul initial colorat în culorile argumentelor, pentru vizualizare ușoară, și datele raw, usor de exportat. Un ecran de loading cat timp sistemul proceseaza ar fi bun.
## 4. Etape

### 4.1 Wireframe (designul paginilor, feature-uri)
### 4.2 Implementare
### 4.3 Legarea de backend

## 5. Cum arata datele?

Programul scoate aceste structuri JSON:

<p>Prompt: If a vehicle has a siren, it is an emergency vehicle. If a vehicle is an emergency vehicle, it can run red lights. Engine 42 has a siren. 
<br><br>
Atoms: {"atoms":[{"id":"a1","text":"An entity has a siren","kb_type":"premise","source_quote":"a vehicle has a siren"},{"id":"a2","text":"An entity is an emergency vehicle","kb_type":"premise","source_quote":"it is an emergency vehicle"},{"id":"a3","text":"An entity can run red lights","kb_type":"premise","source_quote":"it can run red lights"},{"id":"a4","text":"This entity is Engine 42","kb_type":"premise","source_quote":"Engine 42"},{"id":"a5","text":"This entity has a siren","kb_type":"premise","source_quote":"has a siren"}]} 
<br><br>
Rules: {"scratchpad":{"extracted_connectors":["If","If"],"disjunction_split_plan":"No OR disjunctions found; no split needed.","inversion_check":"No 'requires' inversion found."},"rules":[{"id":"r1","conclusion":"a2","premises":["a1"],"type":"defeasible"},{"id":"r2","conclusion":"a3","premises":["a2"],"type":"defeasible"},{"id":"r3","conclusion":"a1","premises":["a5"],"type":"strict"}]} 
<br><br>
Arguments: {"scratchpad":{"text_connectors_found":["If","If"],"rule_firing_verification":"P1 creates atomic arguments for all provided atoms: A1(a1), A2(a2), A3(a3), A4(a4), A5(a5). P2 fires r3 because A5 concludes a5 and matches the premise [a5], deriving A6(a1). Then r1 fires because A6 concludes a1 and matches the premise [a1], deriving A7(a2). Then r2 fires because A7 concludes a2 and matches the premise [a2], deriving A8(a3). All firings are valid and sequential. No other rules are provided."},"arguments":[{"id":"A1","conclusion":"a1","top_rule":null,"sub_arguments":[],"type":"atomic"},{"id":"A2","conclusion":"a2","top_rule":null,"sub_arguments":[],"type":"atomic"},{"id":"A3","conclusion":"a3","top_rule":null,"sub_arguments":[],"type":"atomic"},{"id":"A4","conclusion":"a4","top_rule":null,"sub_arguments":[],"type":"atomic"},{"id":"A5","conclusion":"a5","top_rule":null,"sub_arguments":[],"type":"atomic"},{"id":"A6","conclusion":"a1","top_rule":"r3","sub_arguments":["A5"],"type":"strict"},{"id":"A7","conclusion":"a2","top_rule":"r1","sub_arguments":["A6"],"type":"defeasible"},{"id":"A8","conclusion":"a3","top_rule":"r2","sub_arguments":["A7"],"type":"defeasible"}]}</p>
Logurile sunt doar o lista de text, poate tupluri, nu e o structura complexa. 