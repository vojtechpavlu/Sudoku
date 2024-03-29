# Sudoku

Projekt pro demonstraci principů symbolických metod pro řešení problémů ve 
stavovém prostoru. Tento projekt byl vyvinut jako studijní pomůcka pro výuku 
umělé inteligence při 
[Smíchovské střední průmyslové škole a gymnáziu](https://www.ssps.cz/).


**Zajímavé odkazy**

- [Sudoku na Wikipedii](https://cs.wikipedia.org/wiki/Sudoku)
- [Splňování podmínek na Wikipedii](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem)
- [Studijní materiály na Google Drive](https://tinyurl.com/ssps-umela-inteligence)


---

Samotný projekt se zaměřuje na ukázku možného řešení úlohy třídy **Constraint
Satisfaction Problem** (CSP). Problém je rámcově rozdělen do 3 bloků:

- **Definice hry**, tedy definice hrací plochy, políček a pravidel
- **Řešitelé hry**, tedy definice algoritmů, které dokáží hru samostatně řešit
- **Generátory náhodných zadání**, tedy návrh algoritmů pro generování 
  náhodných zadání, pomocí kterých je možné testovat řešitele.
  
Kód těchto bloků lze nalézt v balíčku `./src`.



## Úvod do Constraint Satisfaction Problem (CSP)

Úlohy této třídy jsou postaveny na požadavku hledání řešení, které neodporuje
omezením problému. Formálně pak lze o CSP mluvit jako o trojici množin:

- Množina proměnných
- Množina definičních oborů
- Množina omezení

### Množina proměnných

U CSP uvažujeme konečnou množinu proměnných, které se snažíme vyplnit hodnotami
z definičních oborů. Vzájemné vazby mezi proměnnými mohou býti zatíženy 
omezujícími podmínkami, stejně jako může mít každá proměnná vlastní definiční 
obor.

Formálně bychom mohli tyto proměnné popsat následovně:

$$x_{1}, x_{2}, ..., x_{n}$$

tedy že máme `n` proměnných, pro které se snažíme najít příslušné hodnoty z 
definičních oborů tak, aby nebylo porušeno žádné pravidlo.

Jsou-li vyplněny všechny proměnné, mluvíme pak o tzv. ***úplném řešení***.

### Množina definičních oborů

Jak bylo již výše naznačeno, každá proměnná může mít libovolný a vlastní 
definiční obor, jehož lze užít pro vyplnění proměnné hodnotou. Přes to,
že v našem případě budeme uvažovat striktně číselné obory, lze teoreticky
užít libovolné množiny hodnot - třeba i kategorických.

Formální zápis by mohl vypadat následovně:

$$Df_{1}, Df_{2}, ..., Df_{n}; x_{i} \in Df_{i}$$

tedy pro každou `i`-tou proměnnou můžeme použít pouze hodnoty z `i`-tého
definičního oboru.

### Množina omezení

Celé řešení musí podléhat již zmíněným omezením. Tato omezení se nemusí 
vztahovat pouze na konkrétní proměnnou, naopak může ve své působnosti omezovat
libovolné množství proměnných. Stejně tak může jedna proměnná být zatížena
vícero omezeními (vztah `M:N`).

Přípustné je pak logicky pouze takové řešení, které neodporuje žádnému z 
definovaných omezení. O takových pak mluvíme jako o tzv. ***konzistentních 
řešeních***.

Formálně bychom tuto množinu mohli popsat následovně:

$$C_{1}, C_{2}, ... , C_{m}; C_{k} \text{ souvisí s } x_{C_{j1}}, x_{C_{j2}}, ... , 
x_{C_{jk}}, $$


### Výstup úlohy

Pro nás je tedy cílem najít řešení, které má vyplněny všechny proměnné a není
porušeno jediné pravidlo, tedy kdy je stav úlohy v úplné a konzistentní 
konfiguraci.


## Definice hry

Sudoku je hra logická hra, která je postavena na problému snahy nalézt takovou
kombinaci číselných hodnot, která by neporušovala žádné pravidlo hry. Celá
hrací plocha má v původním rozložení podobu čtvercové matice o 81 políčcích,
tedy 9 řádcích, 9 sloupcích a 9 malých čtverců sdružujících 9 políček. K 
vyplnění lze užít celých čísel z intervalu `[1, 9]`.

V původním pojetí má sudoku vždy právě jedno řešení; v opačném případě o sudoku
v pravém slova smyslu nejde. Pro naše potřeby od této umělé podmínky abstrahujeme. 

### Definovaná omezení

Hra stojí na 3 základních závazných omezeních, která nesmíme v rámci zachování
konzistence hry při řešení porušit:

- *Unikátní hodnota v řádku*
- *Unikátní hodnota ve sloupečku*
- *Unikátní hodnota v malém čtverci*


### Přepis do CSP

Cílem úlohy je tedy z pohledu splňování podmínek najít takové řešení, které 
vyplní chybějící hodnoty a neporuší zároveň jediné pravidlo.

Formálněji tedy máme množinu proměnných z matice

```math
\begin{pmatrix}
    x_{1,1} & x_{1,2} & \dots & x_{1,9} \\
    x_{2,1} & x_{2,2} & \dots & x_{2,9} \\
    \vdots & \vdots & \ddots & \vdots \\
    x_{9,1} & x_{9,2} & \dots & x_{9,9} \\
\end{pmatrix}
```

přičemž platí, že definiční obor pro libovolnou proměnnou odpovídá stejnému
rozsahu, tedy:

```math
Df_{i} = \{ 1, 2, ..., 9\}
```

a již zbývají jen samotná omezení, která odpovídají výše popsaným pravidlům.



## Řešitelé hry

Jednou z metod řešení úlohy třídy CSP je pomocí prohledávání stavového 
prostoru. V nejjednodušším pojetí je k tomu využito jednoduchého algoritmu,
tzv. *Backtracking*, který je analogický k algoritmu prohledávání do hloubky 
(*Depth-First Search*, resp. *DFS*). Dobré je však poznamenat, že tento 
algoritmus patří pro potřeby tohoto použití mezi tzv. *brute-force*, tedy
výpočet hrubou silou. Jeho nevýhoda pak tkví v nutnosti slepého procházení 
všech variant, dokud není řešení nalezeno, čímž se řadí mezi méně efektivní.

Pro možnost implementace více různých algoritmů byl stanoven společný protokol
pro tato řešení pomocí abstraktní třídy `SolverAlgorithm`, kterou lze nalézt
v modulu `./src/solver.py`.

Tuto implementuje aktuálně jediná konkrétní implementace postavená právě na
backtrackingu, třída `BacktrackingSolver` nacházející se ve stejném modulu.



## Generátory náhodných zadání

K testování správnosti řešitelů je třeba jim poskytnout zadání, která mají být
vyřešena. K tomu byl navržen algoritmus, který dokáže náhodná zadání generovat.

Konkrétní implementaci lze nalézt v modulu `./src/grid_generation.py`, kde
je uvedena třída `BacktrackingGenerator` implementující svého abstraktního 
předka (třídu `GridGenerator`).

Kromě vybudování konzistentního a úplného řešení (vyřešené hry), jsou instance
této třídy také schopny náhodně některá políčka nastavit jako nevyplněná, čímž
převedou hrací plochu do stavu neúplného, aniž by tkly jejich konzistenci.



