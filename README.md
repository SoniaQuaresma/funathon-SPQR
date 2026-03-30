# funathon-project1
Repository of the 1st funathon project (tabular data)

# Dictionnaire des variables

1.	idlocal : identifiant cadastral unique ;
2.	ccodep : département ;
3.	ccocom : commune ;
4.	dteloc : type de logement (1 : maison,
 2 : appartement) ;
5.	anneemut : année de mutation ;
6.	datemut : date de mutation ;
7.	libnatmut : type de transaction (vente ou VEFA) ;
8.	valeurfonc : montant de la transaction ;
9.	dsupdc : surface du logement ;
10.	jannath : année d’achèvement ;
11.	nb_garages : nombre de garages ;
12.	nb_piscines
13.	nb_terrasses
14.	nb_greniers
15.	nb_caves
16.	nb_autresdep : nombre d’autres dépendances ;
17.	dnbbai : nombre de baignoires ;
18.	dnbdou : nombre de douches ;
19.	dnblav : nombre de lavabos ;
20.	dnbwc : nombre de WC ;
21.	dnbppr : nombre de pièces principales ;
22.	dnbsam : nombre de salles à manger ;
23.	dnbcha : nombre de chambres ;
24.	dnbcu8 : nombre de cuisines < 9m² ;
25.	dnbcu9 : nombre de cuisines > 9m² ;
26.	dnbsea : nombre de salles d’eau ;
27.	dnbann : nombre de pièces annexes ;
28.	dnbpdc : nombre de pièces ;
29.	x,
 y : coordonnées géo.
30. dnbniv : prend en compte le rdc
geaulc	gelelc	gesclc	ggazlc	gasclc	gchclc	gvorlc	gteglc	dniv	dcntsol	dcntagri	dcntnat   : caractéristiques des équipements (gaz,
 électricité,
 eau,
 escalier,
 ascenceur)


10/02:
quelles sont les déf de geaulc	gelelc	gesclc	ggazlc	gasclc	gchclc	gvorlc	gteglc	dniv	dcntsol	dcntagri	dcntnat  ??

Fait : 
- retrouver des transactions connues pour regarder les variables
x,
 y : coordonnées géographiques semblent ok 

Questions : 
- pourquoi deux fichiers flat et houses ?
- sélectionner un subset de variables parmi les 47 ?
- les données au moment de la transaction ? Comment sont elles mises à jour ? 
- comment détecter les ventes partielles de bien ? 
- 1 ligne par vente ? 

11/02 : 
stats des
| colonne           | type    |   total |   nulles |   NaN |   valides | médiane/mode       | min                 | max               |
|:------------------|:--------|--------:|---------:|------:|----------:|:-------------------|:--------------------|:------------------|
| idmutation        | String  | 4695874 |        0 |     0 |   4695874 | DVF+_9979682       | DV3F_10332875       | DVF+_9999998      |
| datemut           | Date    | 4695874 |        0 |     0 |   4695874 | 2017-12-30         | 2010-01-02          | 2024-12-31        |
| anneemut          | Int32   | 4695874 |        0 |     0 |   4695874 | 2018.0             | 2010                | 2024              |
| moismut           | Int32   | 4695874 |        0 |     0 |   4695874 | 7.0                | 1                   | 12                |
| idnatmut          | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 1                   | 1                 |
| libnatmut         | String  | 4695874 |        0 |     0 |   4695874 | Vente              | Vente               | Vente             |
| valeurfonc        | Float64 | 4695874 |        0 |     0 |   4695874 | 150000.0           | 1000.0              | 66500000.0        |
| dteloc            | String  | 4695874 |        0 |     0 |   4695874 | 2                  | 2                   | 2                 |
| jannath           | Int32   | 4695874 |      873 |     0 |   4695001 | 1974.0             | 1200                | 2024              |
| ccodep            | String  | 4695874 |        0 |     0 |   4695874 | 75                 | 01                  | 974               |
| depcom            | String  | 4695874 |        0 |     0 |   4695874 | 06088              | 01004               | 97424             |
| x                 | Float64 | 4695874 |        0 |     0 |   4695874 | 2.4807198092161706 | -63.11504016285567  | 55.72081546449435 |
| y                 | Float64 | 4695874 |        0 |     0 |   4695874 | 46.78311095709862  | -21.381146550197524 | 51.0820594859233  |
| distance_ltm      | Float64 | 4695874 |        0 |     0 |   4695874 | 10000.0            | 0.10997415915499446 | 10000.0           |
| distance_ltm_corr | Float64 | 4695874 |        0 |     0 |   4695874 | 10000.0            | 0.07971292253454423 | 10000.0           |
| dnbniv            | Int32   | 4695874 |        0 |     0 |   4695874 | 3.0                | 0                   | 99                |
| dnbbai            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 21                |
| dnbdou            | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 22                |
| dnblav            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 63                |
| dnbwc             | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 51                |
| dnbppr            | Int32   | 4695874 |        0 |     0 |   4695874 | 5.0                | 0                   | 92                |
| dnbsam            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 87                |
| dnbcha            | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 67                |
| dnbcu8            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 84                |
| dnbcu9            | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 62                |
| dnbsea            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 83                |
| dnbann            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 95                |
| dnbpdc            | Int32   | 4695874 |        0 |     0 |   4695874 | 5.0                | 1                   | 99                |
| dsupdc            | Int32   | 4695874 |        0 |     0 |   4695874 | 56.0               | 15                  | 1500              |
| geaulc            | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 2                 |
| gelelc            | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 2                 |
| gesclc            | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 2                 |
| ggazlc            | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 2                 |
| gasclc            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 2                 |
| gchclc            | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 2                 |
| gvorlc            | Int32   | 4695874 |        0 |     0 |   4695874 | 1.0                | 0                   | 2                 |
| gteglc            | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 2                 |
| dniv              | Int32   | 4695874 |        0 |     0 |   4695874 | 2.0                | 0                   | 99                |
| dcntsol           | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 69891             |
| dcntagri          | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 1114552           |
| dcntnat           | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 851235            |
| nb_garages        | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 215               |
| nb_piscines       | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 2                 |
| nb_terrasses      | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 5                 |
| nb_greniers       | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 13                |
| nb_caves          | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 22                |
| nb_autresdep      | Int32   | 4695874 |        0 |     0 |   4695874 | 0.0                | 0                   | 91                |

idnatmut = 1 tout le temps,
 pq ? 
que les vente dans le data set
répartition valeurfonc pour détecter valeurs aberrantes/ Max est à 66,
5M€. A été filtré avant ? 
distance_ltm,
 distance_ltm_corr : distance au littoral
dataset a bien été cleané avant. 99 is missing value ? 
comprend les transactions en DOM (St Martin,
 Guadeloupe,
 mais pas celles en Alsace Moselle cf. all_transactions_plot)


12/02
stat des de répartition des valeurs descriptives cf. stat_des_details_flat
Quasiment que des 0 pour les flat cf. stat_des_details_surf_flat_num et stat_des_details_surf_flat_plot
"dcntsol",

"dcntnat",

"dcntagri"
with plot of repartition for various var stat_des_details_surf_flat_num

13/02 : 
- s'inspirer des MOOC de scikit-learn qui sont top : https://inria.github.io/scikit-learn-mooc/
- have a baseline dummy model to compare to ?
- need to scale data ? 
- impact of encoder ? 
- première regression simple : 
    - filtrer sur 1 année
    - features : depcom (question encoding ?),
 dteloc (boolean apt),
 dnbppr,
 dnbcha,
 dsupdc
- do stat des with data samples to ease computation time
    - use seaborn.pairplot to plot correlation graph
    - use pandas dataframe.hist to plot histogram easily

pairplot with log_price : cf. stat_des_some_vars_pairplot

16/02
- stat des on depcom (question encoding ?),
 dteloc (boolean apt),
 dnbppr,
 dnbcha,
 dsupdc
- calculating price_sqm
- fitter a first RFregressor on 100 000 and 150 000 obs with depcom (question encoding ?),
 dteloc (boolean apt),
 dnbppr,
 dnbcha,
 dsupdc

|N_obs | price | price per sqm |
| -- | --- | --- |
|100 000|  5 CV ; <br> - Mean cross validation accuracy is : 0.551 +- 0.011 with an elapsed time of 129.945s <br> - Mean cross validation accuracy is : 0.495 +- 0.046 with an elapsed time of 184.692s | |

- Stay on a region and do not filter on years. Have price per sqm and not price. 

19/02 : 
- feature selection : cf. nb_features_accuracy
    keep all paris (75) transactions. 
    Add ccordinates (x,
 y)
    Target = price per sqm
    2 sets of feature : 
        - a minimal : CV score = 9%  
        - all features : CV score = 22%
    Impact of outlier ? 
    Removes all prices_sqm below quantile 0.9 and above quantile 0.1. Impact : 
        - a minimal : CV score = 13% +-3%  
        - all features : CV score = 38% +-2%
    Removes all prices_sqm below quantile 0.8 and above quantile 0.2. Impact : 
        - a minimal : CV score = 6% +-1%  
        - all features : CV score = 25% +-2%

Cf features_plus_model_selection
Data set : 
   - 7 col (['depcom',
 'x',
 'y',
 'dteloc',
 'dnbppr',
 'dnbcha',
 'dsupdc'])
   - n_ops : 322805 

= Model is : GradientBoostingRegressor 
  Metrics are : 
   - MAPE : 0.151 
   - R2 : 0.172 
  with an elapsed time of 28.503s
= Model is : HistGradientBoostingRegressor 
  Metrics are : 
   - MAPE : 0.149 
   - R2 : 0.189 
  with an elapsed time of 1.353s
= Model is : RandomForestRegressor 
  Metrics are : 
   - MAPE : 0.161 
   - R2 : 0.027 
  with an elapsed time of 108.227s
Data set : 
   - 27 col (['anneemut',
 'dteloc',
 'jannath',
 'ccodep',
 'depcom',
 'x',
 'y',
 'distance_ltm',
 'dnbniv',
 'dnbbai',
 'dnbdou',
 'dnblav',
 'dnbwc',
 'dnbppr',
 'dnbsam',
 'dnbcha',
 'dnbcu8',
 'dnbcu9',
 'dnbsea',
 'dnbann',
 'dnbpdc',
 'dsupdc',
 'dniv',
 'nb_terrasses',
 'nb_greniers',
 'nb_caves',
 'nb_autresdep'])
   - n_ops : 322805 

= Model is : GradientBoostingRegressor 
  Metrics are : 
   - MAPE : 0.119 
   - R2 : 0.427 
  with an elapsed time of 63.356s
= Model is : HistGradientBoostingRegressor 
  Metrics are : 
   - MAPE : 0.113 
   - R2 : 0.469 
  with an elapsed time of 2.295s
= Model is : RandomForestRegressor 
  Metrics are : 
   - MAPE : 0.113 
   - R2 : 0.463 
  with an elapsed time of 242.980s

HistGradientBoostingRegressor => far better model

dummyregressor :
- score is 0 so model performs much better

Hyperparameter tuning
 => impact of hyperparams on MAPE is residual. cf. hyperparams_tuning and cf. hyperparams_plot

add dniv / dnbniv as dnivrel : no impact,
 cf nb_features_accuracy. 

Add distance to Seine ? 

Plot the results ? 

stat des with pandas to select variables : cf. stat_des75_pandas



 - que veulent dire   'gchclc',  'gvorlc',  'gteglc'
 - codification des variables : maximisées ? 

