data <- read.csv("judgements_abstracts.csv")
data <- na.omit(data)
library(car)

#Influence of university and country on the quality ratings in general:
manova_result <- manova(cbind(Originality, Method, Credibility, Understandability,
                               Relevance, Quality.of.Citations, Linguistic.style.and.soundness.of.grammar, Overall.score) ~ 
                           country_association * university_association, data = data)

summary(manova_result)
#both independent variables are significantly influencing the quality ratings (p values of 2.2e-16 (country) and 4.51e-11 (university))
#now, we want to know which dependent variables (which quality ratings) are responsible for this significant values.
#to find out, we conduct seperate anovas for all quality dimensions

anova_result1 <- aov(Originality ~ country_association*university_association, data = data)
summary(anova_result1)
anova_result2 <- aov(Method ~ country_association*university_association, data = data)
summary(anova_result2)
anova_result3 <- aov(Credibility ~ country_association*university_association, data = data)
summary(anova_result3)
anova_result4 <- aov(Understandability ~ country_association*university_association, data = data)
summary(anova_result4)
anova_result5 <- aov(Relevance ~ country_association*university_association, data = data)
summary(anova_result5)
anova_result6 <- aov(Quality.of.Citations ~ country_association*university_association, data = data)
summary(anova_result6)
anova_result7 <- aov(Linguistic.style.and.soundness.of.grammar ~ country_association*university_association, data = data)
summary(anova_result7)
anova_result8 <- aov(Overall.score ~ country_association*university_association, data = data)
summary(anova_result8)
#chatgpt is biased towards all quality dimensions when only looking at the paper's abstract.
#bias in originality is only due to country
#bias in method is only due to country
#bias in credibility is due to country as well as university
#bias in understandability is only due to country
#bias in relevance is only due to country
#bias in quality of citations is due to both country and university
#bias in linguistic style and grammar is due to both country and university
#bias in overall score is due to both country and university

#very interesting that chatgpt is also biased in dimensions which cannot even be assessed only reading the abstract (e.g. quality of citations)


#now we want to know which pairwise comparisons are significantly differing.
#for that, we can apply a TukeyHSD function.
install.packages("multcomp")
library(multcomp)
#for originality, country is responsible for the bias, which ones?
tukey_result1 <- TukeyHSD(anova_result1)
print(tukey_result1$country_association)
#egypt - australia (-0.21 points difference)
#germany - egypt (0.20 points difference)

#for Method, country is responsible for the bias, which ones?
tukey_result2 <- TukeyHSD(anova_result2)
print(tukey_result2$country_association)
#germany - egypt (0.28 points difference)
#switzerland - egypt (0.38 points difference)
#switzerland - iran (0.35 points difference)

#for credibility, country and university are responsible for the bias, which ones?
tukey_result3 <- TukeyHSD(anova_result3)
print(tukey_result3$country_association)
print(tukey_result3$university_association)
#countries:
# Brazil-Australia         -5.066667e-01 -0.844984096 -0.16834924 8.049270e-05
# China-Australia          -4.133333e-01 -0.751650763 -0.07501590 4.108936e-03
# Egypt-Australia          -5.066667e-01 -0.844984096 -0.16834924 8.049270e-05
# India-Australia          -3.768950e-01 -0.717521768 -0.03626819 1.631942e-02
# Iran-Australia           -5.933333e-01 -0.934554829 -0.25211184 1.334851e-06
# South Africa-Australia   -3.800000e-01 -0.718317430 -0.04168257 1.349869e-02
# Germany-Brazil            3.666667e-01  0.028349237  0.70498410 2.098354e-02
# Switzerland-Brazil        6.200000e-01  0.281682570  0.95831743 2.322120e-07
# USA-Brazil                5.677551e-01  0.227715944  0.90779426 4.591025e-06
# Switzerland-China         5.266667e-01  0.188349237  0.86498410 3.113386e-05
# USA-China                 4.744218e-01  0.134382611  0.81446093 3.824119e-04
# Germany-Egypt             3.666667e-01  0.028349237  0.70498410 2.098354e-02
# Switzerland-Egypt         6.200000e-01  0.281682570  0.95831743 2.322120e-07
# USA-Egypt                 5.677551e-01  0.227715944  0.90779426 4.591025e-06
# Iran-England             -3.733333e-01 -0.714554829 -0.03211184 1.873260e-02
# Iran-Germany             -4.533333e-01 -0.794554829 -0.11211184 9.914852e-04
# Switzerland-India         4.902283e-01  0.149601520  0.83085510 1.984943e-04
# USA-India                 4.379834e-01  0.095646508  0.78032032 1.939242e-03
# Switzerland-Iran          7.066667e-01  0.365445171  1.04788816 1.857860e-09
# USA-Iran                  6.544218e-01  0.311493125  0.99735041 5.312831e-08
# Switzerland-South Africa  4.933333e-01  0.155015904  0.83165076 1.485788e-04
# USA-South Africa          4.410884e-01  0.101049277  0.78112759 1.526460e-03

#universities:
tukey_df3 <- as.data.frame(tukey_result3$university_association)
significant_results3 <- subset(tukey_df3, tukey_df3[, 4] < 0.05)
print(significant_results3)
# Massachusetts Institute of Technology-China University of Mining and Technology  0.8370068  0.1422361  1.53177747 0.002265143
# University of Dundee-Massachusetts Institute of Technology                      -0.7303401 -1.4251108 -0.03556946 0.025004810
# University of Lausanne-Massachusetts Institute of Technology                    -0.8636735 -1.5584441 -0.16890280 0.001160732
# University of Potsdam-Massachusetts Institute of Technology                     -0.7103401 -1.4051108 -0.01556946 0.037186263
# Western Washington University-Massachusetts Institute of Technology             -0.8571429 -1.5554137 -0.15887206 0.001527426
# University of Lausanne-University of Cambridge                                  -0.6933333 -1.3845862 -0.00208051 0.048082994

#for understandability, country is responsible for the bias, which ones?
tukey_result4 <- TukeyHSD(anova_result4)
print(tukey_result4$country_association)
# Egypt-Brazil             -0.320000000 -0.60698089 -0.03301911 1.481250e-02
# Egypt-China              -0.386666667 -0.67364755 -0.09968578 7.616067e-04
# Germany-Egypt             0.380000000  0.09301911  0.66698089 1.054459e-03
# Switzerland-Egypt         0.453333333  0.16635245  0.74031422 2.132731e-05
# USA-Egypt                 0.326122449  0.03768109  0.61456381 1.239311e-02
# Switzerland-Iran          0.332183908  0.04273962  0.62162820 1.016264e-02
# Switzerland-South Africa  0.333333333  0.04635245  0.62031422 8.623560e-03

#for relevance, country is responsible for the bias, which ones?
tukey_result5 <- TukeyHSD(anova_result5)
print(tukey_result5$country_association)
# Egypt-Brazil             -2.533333e-01 -0.48753840 -0.01912827 0.021475341
# Iran-Brazil              -2.751724e-01 -0.51138786 -0.03895697 0.008279546

#for quality of citations, country and university are responsible for the bias, which ones?
tukey_result6 <- TukeyHSD(anova_result6)
print(tukey_result6$country_association)
print(tukey_result6$university_association)
#countries:
# diff          lwr          upr        p adj
# Brazil-Australia         -4.600000e-01 -0.677062191 -0.242937809 6.546289e-10
# China-Australia          -4.600000e-01 -0.677062191 -0.242937809 6.546289e-10
# Egypt-Australia          -6.733333e-01 -0.890395525 -0.456271142 0.000000e+00
# England-Australia        -2.666667e-01 -0.483728858 -0.049604475 3.768743e-03
# India-Australia          -4.351598e-01 -0.653703679 -0.216615956 9.938019e-09
# Iran-Australia           -7.149425e-01 -0.933867949 -0.496017109 0.000000e+00
# South Africa-Australia   -3.733333e-01 -0.590395525 -0.156271142 1.879979e-06
# Egypt-Brazil             -2.133333e-01 -0.430395525  0.003728858 5.901860e-02
# Germany-Brazil            2.933333e-01  0.076271142  0.510395525 7.194802e-04
# Iran-Brazil              -2.549425e-01 -0.473867949 -0.036017109 8.319675e-03
# Switzerland-Brazil        5.133333e-01  0.296271142  0.730395525 9.584555e-13
# USA-Brazil                3.960544e-01  0.177887581  0.614221262 3.222693e-07
# Germany-China             2.933333e-01  0.076271142  0.510395525 7.194802e-04
# Iran-China               -2.549425e-01 -0.473867949 -0.036017109 8.319675e-03
# Switzerland-China         5.133333e-01  0.296271142  0.730395525 9.584555e-13
# USA-China                 3.960544e-01  0.177887581  0.614221262 3.222693e-07
# England-Egypt             4.066667e-01  0.189604475  0.623728858 1.054110e-07
# Germany-Egypt             5.066667e-01  0.289604475  0.723728858 3.480327e-12
# India-Egypt               2.381735e-01  0.019629654  0.456717378 1.964096e-02
# South Africa-Egypt        3.000000e-01  0.082937809  0.517062191 4.630084e-04
# Switzerland-Egypt         7.266667e-01  0.509604475  0.943728858 0.000000e+00
# USA-Egypt                 6.093878e-01  0.391220915  0.827554596 0.000000e+00
# Iran-England             -4.482759e-01 -0.667201282 -0.229350442 3.055140e-09
# Switzerland-England       3.200000e-01  0.102937809  0.537062191 1.160129e-04
# India-Germany            -2.684932e-01 -0.487037012 -0.049949289 3.767376e-03
# Iran-Germany             -5.482759e-01 -0.767201282 -0.329350442 0.000000e+00
# Switzerland-Germany       2.200000e-01  0.002937809  0.437062191 4.374576e-02
# Iran-India               -2.797827e-01 -0.500177276 -0.059388147 2.213114e-03
# Switzerland-India         4.884932e-01  0.269949289  0.707037012 4.758616e-11
# USA-India                 3.712142e-01  0.151573180  0.590855298 3.203982e-06
# South Africa-Iran         3.416092e-01  0.122683775  0.560534616 2.931739e-05
# Switzerland-Iran          7.682759e-01  0.549350442  0.987201282 0.000000e+00
# USA-Iran                  6.509970e-01  0.430976235  0.871017666 0.000000e+00
# Switzerland-South Africa  4.266667e-01  0.209604475  0.643728858 1.677770e-08
# USA-South Africa          3.093878e-01  0.091220915  0.527554596 2.724367e-04

#universities:
tukey_df6 <- as.data.frame(tukey_result6$university_association)
significant_results6 <- subset(tukey_df6, tukey_df6[, 4] < 0.05)
print(significant_results6)
# ETH Zurich-China University of Mining and Technology                             0.4466667  0.003163497  0.890169836 0.0455600063
# Massachusetts Institute of Technology-China University of Mining and Technology  0.5068027  0.061042523  0.952562919 0.0069172086
# University of Lausanne-ETH Zurich                                               -0.4600000 -0.903503170 -0.016496830 0.0303971965
# University of Potsdam-ETH Zurich                                                -0.5000000 -0.943503170 -0.056496830 0.0080400687
# University of the Free State-ETH Zurich                                         -0.4533333 -0.896836503 -0.009830164 0.0373089835
# University of Wolverhampton-ETH Zurich                                          -0.4600000 -0.903503170 -0.016496830 0.0303971965
# Western Washington University-ETH Zurich                                        -0.4908844 -0.936644552 -0.045124156 0.0120280461
# University of Houston-Massachusetts Institute of Technology                     -0.4693878 -0.917393611 -0.021381900 0.0262550242
# University of Lausanne-Massachusetts Institute of Technology                    -0.5201361 -0.965896252 -0.074375857 0.0042707974
# University of Potsdam-Massachusetts Institute of Technology                     -0.5601361 -1.005896252 -0.114375857 0.0009123221
# University of the Free State-Massachusetts Institute of Technology              -0.5134694 -0.959229586 -0.067709190 0.0054466818
# University of Wolverhampton-Massachusetts Institute of Technology               -0.5201361 -0.965896252 -0.074375857 0.0042707974
# Western Washington University-Massachusetts Institute of Technology             -0.5510204 -0.999026264 -0.103014553 0.0014641270
# University of Potsdam-University of Cambridge                                   -0.4800000 -0.923503170 -0.036496830 0.0159638617
# Western Washington University-University of Cambridge                           -0.4708844 -0.916644552 -0.025124156 0.0232412316

#for linguistics and grammar, country and university are responsible for the bias, which ones?
tukey_result7 <- TukeyHSD(anova_result7)
print(tukey_result7$country_association)
print(tukey_result7$university_association)
#country:
# diff         lwr          upr        p adj
# Egypt-Australia          -4.133333e-01 -0.60513638 -0.221530285 2.972169e-10
# Germany-Australia         1.800000e-01 -0.01180305  0.371803049 8.877148e-02
# Iran-Australia           -3.457471e-01 -0.53919658 -0.152297670 5.466970e-07
# Egypt-Brazil             -3.066667e-01 -0.49846972 -0.114863618 1.547558e-05
# Germany-Brazil            2.866667e-01  0.09486362  0.478469715 8.441066e-05
# Iran-Brazil              -2.390805e-01 -0.43252992 -0.045631003 3.430042e-03
# Switzerland-Brazil        2.866667e-01  0.09486362  0.478469715 8.441066e-05
# Egypt-China              -2.600000e-01 -0.45180305 -0.068196951 6.780249e-04
# England-China             2.066667e-01  0.01486362  0.398469715 2.247406e-02
# Germany-China             3.333333e-01  0.14153028  0.525136382 1.358300e-06
# Switzerland-China         3.333333e-01  0.14153028  0.525136382 1.358300e-06
# England-Egypt             4.666667e-01  0.27486362  0.658469715 0.000000e+00
# Germany-Egypt             5.933333e-01  0.40153028  0.785136382 0.000000e+00
# India-Egypt               2.756164e-01  0.08250414  0.468728738 2.377205e-04
# South Africa-Egypt        2.333333e-01  0.04153028  0.425136382 4.388626e-03
# Switzerland-Egypt         5.933333e-01  0.40153028  0.785136382 0.000000e+00
# USA-Egypt                 3.787755e-01  0.18599636  0.571554662 1.706282e-08
# Iran-England             -3.990805e-01 -0.59252992 -0.205631003 2.204985e-09
# South Africa-England     -2.333333e-01 -0.42513638 -0.041530285 4.388626e-03
# India-Germany            -3.177169e-01 -0.51082919 -0.124604595 7.021897e-06
# Iran-Germany             -5.257471e-01 -0.71919658 -0.332297670 0.000000e+00
# South Africa-Germany     -3.600000e-01 -0.55180305 -0.168196951 9.859878e-08
# USA-Germany              -2.145578e-01 -0.40733698 -0.021778671 1.516658e-02
# Iran-India               -2.080302e-01 -0.40277787 -0.013282592 2.484295e-02
# Switzerland-India         3.177169e-01  0.12460460  0.510829195 7.021897e-06
# Switzerland-Iran          5.257471e-01  0.33229767  0.719196583 0.000000e+00
# USA-Iran                  3.111893e-01  0.11677201  0.505606598 1.502353e-05
# Switzerland-South Africa  3.600000e-01  0.16819695  0.551803049 9.859878e-08
# USA-Switzerland          -2.145578e-01 -0.40733698 -0.021778671 1.516658e-02

# universities:
tukey_df7 <- as.data.frame(tukey_result7$university_association)
significant_results7 <- subset(tukey_df7, tukey_df7[, 4] < 5.0e-02)
print(significant_results7)
#no significant combinations

#for overall score, country and university are responsible for the bias, which ones?
tukey_result8 <- TukeyHSD(anova_result8)
print(tukey_result8$country_association)
print(tukey_result8$university_association)
#country:
# diff          lwr         upr        p adj
# China-Australia          -0.130800000 -0.249761449 -0.01183855 1.764072e-02
# Egypt-Australia          -0.310313333 -0.429274782 -0.19135188 0.000000e+00
# India-Australia          -0.159249772 -0.279023254 -0.03947629 9.773480e-04
# Iran-Australia           -0.312409195 -0.432391791 -0.19242660 0.000000e+00
# South Africa-Australia   -0.174133333 -0.293094782 -0.05517188 1.363581e-04
# Egypt-Brazil             -0.203633333 -0.322594782 -0.08467188 2.177634e-06
# Iran-Brazil              -0.205729195 -0.325711791 -0.08574660 2.067215e-06
# Switzerland-Brazil        0.199913333  0.080951884  0.31887478 3.796732e-06
# Egypt-China              -0.179513333 -0.298474782 -0.06055188 6.721306e-05
# Iran-China               -0.181609195 -0.301591791 -0.06162660 6.244647e-05
# Switzerland-China         0.224033333  0.105071884  0.34299478 8.713265e-08
# England-Egypt             0.222613333  0.103651884  0.34157478 1.100226e-07
# Germany-Egypt             0.291780000  0.172818551  0.41074145 0.000000e+00
# India-Egypt               0.151063562  0.031290080  0.27083704 2.466671e-03
# South Africa-Egypt        0.136180000  0.017218551  0.25514145 1.051728e-02
# Switzerland-Egypt         0.403546667  0.284585218  0.52250812 0.000000e+00
# USA-Egypt                 0.264452109  0.144885254  0.38401896 8.222278e-11
# Iran-England             -0.224709195 -0.344691791 -0.10472660 1.067656e-07
# Switzerland-England       0.180933333  0.061971884  0.29989478 5.556633e-05
# India-Germany            -0.140716438 -0.260489920 -0.02094296 7.345998e-03
# Iran-Germany             -0.293875862 -0.413858458 -0.17389327 0.000000e+00
# South Africa-Germany     -0.155600000 -0.274561449 -0.03663855 1.317223e-03
# Iran-India               -0.153159424 -0.273947188 -0.03237166 2.256252e-03
# Switzerland-India         0.252483105  0.132709623  0.37225659 8.359060e-10
# South Africa-Iran         0.138275862  0.018293266  0.25825846 9.602721e-03
# Switzerland-Iran          0.405642529  0.285659933  0.52562512 0.000000e+00
# USA-Iran                  0.266547971  0.145965096  0.38713085 8.463663e-11
# Switzerland-South Africa  0.267366667  0.148405218  0.38632812 3.554868e-11
# USA-South Africa          0.128272109  0.008705254  0.24783896 2.364312e-02
# USA-Switzerland          -0.139094558 -0.258661412 -0.01952770 8.439761e-03

#universities:
tukey_df8 <- as.data.frame(tukey_result8$university_association)
significant_results8 <- subset(tukey_df8, tukey_df8[, 4] < 5.0e-02)
print(significant_results8)
# Massachusetts Institute of Technology-Alexandria University                      0.2621981  0.01789816  0.506498030 1.822352e-02
# Massachusetts Institute of Technology-China University of Mining and Technology  0.3161714  0.07187149  0.560471363 4.585859e-04
# University of Potsdam-ETH Zurich                                                -0.2472333 -0.49029630 -0.004170369 3.989932e-02
# Western Washington University-ETH Zurich                                        -0.2483748 -0.49267476 -0.004074896 4.015444e-02
# Shiraz University-Massachusetts Institute of Technology                         -0.2555247 -0.50233090 -0.008718568 3.119090e-02
# The University of Adelaide-Massachusetts Institute of Technology                -0.2514714 -0.49577136 -0.007171494 3.384717e-02
# Universidade de Brasília-Massachusetts Institute of Technology                  -0.2871914 -0.53149136 -0.042891494 3.699266e-03
# University of Delhi-Massachusetts Institute of Technology                       -0.2587883 -0.50559449 -0.011982159 2.595385e-02
# University of Dundee-Massachusetts Institute of Technology                      -0.3086714 -0.55297136 -0.064371494 8.054565e-04
# University of Houston-Massachusetts Institute of Technology                     -0.3167347 -0.56226537 -0.071204022 4.957107e-04
# University of Lausanne-Massachusetts Institute of Technology                    -0.3435048 -0.58780470 -0.099204828 5.185482e-05
# University of Potsdam-Massachusetts Institute of Technology                     -0.3578381 -0.60213803 -0.113538161 1.532559e-05
# University of the Free State-Massachusetts Institute of Technology              -0.2655381 -0.50983803 -0.021238161 1.490360e-02
# University of Wolverhampton-Massachusetts Institute of Technology               -0.2883714 -0.53267136 -0.044071494 3.414164e-03
# Western Washington University-Massachusetts Institute of Technology             -0.3589796 -0.60451026 -0.113448920 1.622540e-05
# University of Lausanne-University of Cambridge                                  -0.2648333 -0.50789630 -0.021770369 1.433129e-02
# University of Potsdam-University of Cambridge                                   -0.2791667 -0.52222963 -0.036103702 5.749220e-03
# Western Washington University-University of Cambridge                           -0.2803082 -0.52460810 -0.036008229 5.855641e-03