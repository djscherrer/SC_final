data <- read.csv("judgements_abstracts.csv")
data <- na.omit(data)
library(car)

#Influence of university and country on the quality ratings in general:
manova_result3 <- manova(cbind(Originality, Method, Credibility, Understandability,
                               Relevance, Quality.of.Citations, Linguistic.style.and.soundness.of.grammar, Overall.score) ~ 
                           country_association * university_association, data = data)

summary(manova_result3)
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


