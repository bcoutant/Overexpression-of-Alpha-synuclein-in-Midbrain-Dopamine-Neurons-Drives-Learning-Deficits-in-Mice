library(tidyverse)
library(afex)
library(lme4)
library(lmerTest)
library(conflicted)
library(dplyr)
library(emmeans)

# Stats Fig 1 E - First 6 days only @ 2 months

df <- readxl::read_xlsx("C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")

df$R_Nb_omissions[df$R_Nb_omissions == 'NA'] <- NA
df$Nb_side_omissions = as.numeric(df$L_Nb_omissions) + as.numeric(df$R_Nb_omissions)

df$L_TOT_trial[df$L_TOT_trial == 'NA'] <- NA
df$R_TOT_trial[df$R_TOT_trial == 'NA'] <- NA
df$TOT_trial = as.numeric(df$L_TOT_trial) + as.numeric(df$R_TOT_trial)


df$Pct_side_omission = df$Nb_side_omissions / df$TOT_trial * 100

df6d_8w <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_success_both_sides = as.numeric(Avg_success_both_sides)
  )
  
df_stat = subset(df6, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_success_both_sides'))

# RM-ANOVA
a1 <- aov_car(Avg_success_both_sides ~ Condition * Day + Error(Mouse...1/Day), data = df_stat)
summary(a1)

# Mixed model
m1 <- lmerTest::lmer(Avg_success_both_sides ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

# 

library(emmeans)

# Post hoc: compare groups within each day
emm <- emmeans(m1, ~ Condition | Day)
emmeans(m1, ~ Condition | Day) |> pairs(adjust = "holm")

#emmeans(m1, ~ Condition | Day) |> pairs(adjust = "benforroni")

# Pairwise comparisons between conditions at each day
ph <- contrast(emm, method = "pairwise", adjust = "holm")
summary(ph)


# Check the residuals of the model 
res <- residuals(m1)
shapiro.test(res)
qqnorm(res)
qqline(res)
hist(res)



# Stats Fig 1 F - First 6 days only @ 3 weeks

# There are Na and character 'NA' in df$Ag_success_both_sides - let's remove them 

df6d_3w = df 
df6d_3w$Avg_success_both_sides[df6d_3w$Avg_success_both_sides == "NA"] <- NA
df6d_3w$Avg_success_both_sides <- as.numeric(df6d_3w$Avg_success_both_sides)

df6d_3w <- df6d_3w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_success_both_sides = as.numeric(Avg_success_both_sides)
  )

df_stat = subset(df6d_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_success_both_sides'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Avg_success_both_sides ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2A, left panel - First 6 days only @ 3 weeks

dfRT_3w = df 
dfRT_3w$Avg_RT[dfRT_3w$Avg_RT == "NA"] <- NA
dfRT_3w$Avg_RT <- as.numeric(dfRT_3w$Avg_RT)

dfRT_3w <- dfRT_3w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_RT = as.numeric(Avg_RT)
  )

df_stat = subset(dfRT_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_RT'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Avg_RT ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2A, right panel - First 6 days only @ 8 weeks

dfRT_8w = df 
dfRT_8w$NAvg_RT[dfRT_8w$Avg_RT == "NA"] <- NA
dfRT_8w$Avg_RT <- as.numeric(dfRT_8w$Avg_RT)

dfRT_8w <- dfRT_8w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_RT = as.numeric(Avg_RT)
  )

df_stat = subset(dfRT_8w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_RT'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Avg_RT ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2B, left panel - First 6 days only @ 3 weeks

dfCNP_3w = df 
dfCNP_3w$TOT_CNP[dfCNP_3w$TOT_CNP == "NA"] <- NA
dfCNP_3w$TOT_CNP <- as.numeric(dfCNP_3w$TOT_CNP)

dfCNP_3w <- dfCNP_3w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    TOT_CNP = as.numeric(TOT_CNP)
  )

df_stat = subset(dfCNP_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'TOT_CNP'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(TOT_CNP ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2B, right panel - First 6 days only @ 8 weeks

dfCNP_8w = df 
dfCNP_8w$TOT_CNP[dfCNP_8w$TOT_CNP == "NA"] <- NA
dfCNP_8w$TOT_CNP <- as.numeric(dfCNP_8w$TOT_CNP)

dfCNP_8w <- dfCNP_8w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    TOT_CNP = as.numeric(TOT_CNP)
  )

df_stat = subset(dfCNP_8w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'TOT_CNP'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(TOT_CNP ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2C, left panel - First 6 days only @ 3 weeks

dfSO_3w <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Pct_side_omission  = as.numeric(Pct_side_omission )
  )

df_stat = subset(dfSO_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Pct_side_omission'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Pct_side_omission ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2C, right panel - First 6 days only @ 8 weeks

dfSO_8w <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Pct_side_omission = as.numeric(Pct_side_omission)
  )

df_stat = subset(dfSO_8w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Pct_side_omission'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Pct_side_omission ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

