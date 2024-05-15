data <- read.csv("paper_ratings_uni_prompt.csv")
library(car)

###1. perform manova for all variables at the same time, once for university and once for country association
manova_result1 <- manova(cbind(Originality, Method, Credibility, Understandability,
                              Relevance, Quality.of.Citations, Linguistic.style.and.soundness.of.grammar, Overall.score) ~ 
                          university_association, data = data)

summary(manova_result)
#knapp nicht signifikanter effekt von university (p wert = 0.061)

manova_result2 <- manova(cbind(Originality, Method, Credibility, Understandability,
                              Relevance, Quality.of.Citations, Linguistic.style.and.soundness.of.grammar, Overall.score) ~ 
                          country_association, data = data)

summary(manova_result2)
#knapp nicht signifikanter effekt von country ( p wert = 0.065)

#einfluss der interaktion:
manova_result3 <- manova(cbind(Originality, Method, Credibility, Understandability,
                               Relevance, Quality.of.Citations, Linguistic.style.and.soundness.of.grammar, Overall.score) ~ 
                           country_association * university_association, data = data)

summary(manova_result3)
#knapp nicht signifikante effekte in manovas oben sind primär auf country zurückzuführen, wenn interaktion/nestung berücksichtigt nimmt effekt von university ab.

###2. anova für einzelne qualitätskategorien rechnen
#zuerst für university
anova_result1 <- aov(Originality ~ university_association, data = data)
summary(anova_result1)
anova_result2 <- aov(Method ~ university_association, data = data)
summary(anova_result2)
anova_result3 <- aov(Credibility ~ university_association, data = data)
summary(anova_result3)
anova_result4 <- aov(Understandability ~ university_association, data = data)
summary(anova_result4)
anova_result5 <- aov(Relevance ~ university_association, data = data)
summary(anova_result5)
anova_result6 <- aov(Quality.of.Citations ~ university_association, data = data)
summary(anova_result6)
anova_result7 <- aov(Linguistic.style.and.soundness.of.grammar ~ university_association, data = data)
summary(anova_result7)
anova_result8 <- aov(Overall.score ~ university_association, data = data)
summary(anova_result8)
# nur Credibility signifikant abhängig von university

#und jetzt für country
anova_result1 <- aov(Originality ~ country_association, data = data)
summary(anova_result1)
anova_result2 <- aov(Method ~ country_association, data = data)
summary(anova_result2)
anova_result3 <- aov(Credibility ~ country_association, data = data)
summary(anova_result3)
anova_result4 <- aov(Understandability ~ country_association, data = data)
summary(anova_result4)
anova_result5 <- aov(Relevance ~ country_association, data = data)
summary(anova_result5)
anova_result6 <- aov(Quality.of.Citations ~ country_association, data = data)
summary(anova_result6)
anova_result7 <- aov(Linguistic.style.and.soundness.of.grammar ~ country_association, data = data)
summary(anova_result7)
anova_result8 <- aov(Overall.score ~ country_association, data = data)
summary(anova_result8)
#erneut nur credibility stark signifikant beeinflusst von country

#und jetzt für interaktion
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
#unter berücksichtigung der interaktion übt universität sign. einfluss auf originality aus
#ebenso übt country signifikanten einfluss aufcrediblity aus

