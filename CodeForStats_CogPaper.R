library(tidyverse)
library(afex)
library(lme4)
library(lmerTest)
library(conflicted)
library(dplyr)
library(emmeans)
library(readxl)
library(dplyr)
library(ggplot2)
library(rstatix)


# Stats Fig 1 E - First 6 days only @ 2 months

df <- readxl::read_xlsx("C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")

# Filter Histology

df <- df %>%
  dplyr::filter(
    (Time == "3weeks" & !Mouse...1 %in% c(
         'AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8',
         'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0',
         'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52')) |
      (Time == "2months" &!Mouse...1 %in% c(
           "J1", "K1", "V1", "W2", "X4", "AY31",
           "AZ4", "AZ6", "AZ7", "AX3", "AQ52")))

df$R_Nb_omissions[df$R_Nb_omissions == 'NA'] <- NA
df$Nb_side_omissions = as.numeric(df$L_Nb_omissions) + as.numeric(df$R_Nb_omissions)

df$L_TOT_trial[df$L_TOT_trial == 'NA'] <- NA
df$R_TOT_trial[df$R_TOT_trial == 'NA'] <- NA
df$TOT_trial = as.numeric(df$L_TOT_trial) + as.numeric(df$R_TOT_trial)


df$Pct_side_omission = df$Nb_side_omissions / df$TOT_trial * 100

df6d_8w <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  dplyr::filter(!Mouse...1 %in% c("J1", "K1", "V1", "W2", "X4", "AY31","AZ4", "AZ6", "AZ7", "AX3", "AQ52")) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_success_both_sides = as.numeric(Avg_success_both_sides)
  )

df_stat = subset(df6d_8w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_success_both_sides'))

# Nb of mice

table(unique(df_stat[, c("Mouse...1", "Condition")])$Condition)

# RM-ANOVA
a1 <- aov_car(Avg_success_both_sides ~ Condition * Day + Error(Mouse...1/Day), data = df_stat)
summary(a1)

# Mixed model
m1 <- lmerTest::lmer(Avg_success_both_sides ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

# Post hoc: compare groups within each day
emm <- emmeans(m1, ~ Condition | Day)
emmeans(m1, ~ Condition | Day) |> pairs(adjust = "holm")

# Pairwise comparisons between conditions at each day
ph <- contrast(emm, method = "pairwise", adjust = "holm")
summary(ph)

df_stat %>%
  dplyr::group_by(Day, Condition) %>%
  dplyr::summarise(n_animals = dplyr::n_distinct(Mouse...1),
                   .groups = "drop") %>%
  dplyr::arrange(Day, Condition)

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
  dplyr::filter(!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52')) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_success_both_sides = as.numeric(Avg_success_both_sides)
  )

df_stat = subset(df6d_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_success_both_sides'))

df_3w <- df %>%
  dplyr::filter(Time == "3weeks",!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52'))

table(unique(df_3w[, c("Mouse...1", "Condition")])$Condition)


# Mixed model - preferred 
m1 <- lmerTest::lmer(Avg_success_both_sides ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

library(emmeans)

emm <- emmeans(m1, ~ Condition | Day)
pairs(emm, adjust = "holm")

df_stat %>%
  dplyr::group_by(Day, Condition) %>%
  dplyr::summarise(n_animals = dplyr::n_distinct(Mouse...1),
                   .groups = "drop") %>%
  dplyr::arrange(Day, Condition)

#####
##### Figure 2
#####

# Stats Fig 2A, left panel - First 6 days only @ 3 weeks

dfRT_3w = df 
dfRT_3w$Avg_RT[dfRT_3w$Avg_RT == "NA"] <- NA
dfRT_3w$Avg_RT <- as.numeric(dfRT_3w$Avg_RT)

dfRT_3w <- dfRT_3w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  dplyr::filter(!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52')) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_RT = as.numeric(Avg_RT)
  )

table(unique(dfRT_3w[, c("Mouse...1", "Condition")])$Condition)

df_stat = subset(dfRT_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Avg_RT'))

df_3w <- df %>%
  dplyr::filter(Time == "3weeks",!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52'))

table(unique(df_3w[, c("Mouse...1", "Condition")])$Condition)

# Mixed model - preferred 
m1 <- lmerTest::lmer(Avg_RT ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2A, right panel - First 6 days only @ 8 weeks

dfRT_8w = df 
dfRT_8w$Avg_RT[dfRT_8w$Avg_RT == "NA"] <- NA
dfRT_8w$Avg_RT <- as.numeric(dfRT_8w$Avg_RT)

dfRT_8w <- dfRT_8w %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  dplyr::filter(!Mouse...1 %in% c("J1", "K1", "V1", "W2", "X4", "AY31","AZ4", "AZ6", "AZ7", "AX3", "AQ52")) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Avg_RT = as.numeric(Avg_RT)
  )

table(unique(dfRT_8w[, c("Mouse...1", "Condition")])$Condition)

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
  dplyr::filter(!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52')) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    TOT_CNP = as.numeric(TOT_CNP)
  )

table(unique(dfCNP_3w[, c("Mouse...1", "Condition")])$Condition)

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
  dplyr::filter(!Mouse...1 %in% c("J1", "K1", "V1", "W2", "X4", "AY31","AZ4", "AZ6", "AZ7", "AX3", "AQ52")) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    TOT_CNP = as.numeric(TOT_CNP)
  )

table(unique(dfCNP_8w[, c("Mouse...1", "Condition")])$Condition)

df_stat = subset(dfCNP_8w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'TOT_CNP'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(TOT_CNP ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)


# Stats Fig 2C, left panel - First 6 days only @ 3 weeks

dfSO_3w <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  dplyr::filter(!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52')) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Pct_side_omission  = as.numeric(Pct_side_omission )
  )

table(unique(dfSO_3w[, c("Mouse...1", "Condition")])$Condition)

df_stat = subset(dfSO_3w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Pct_side_omission'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Pct_side_omission ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

# Post hoc: compare groups within each day
emm <- emmeans(m1, ~ Condition | Day)
emmeans(m1, ~ Condition | Day) |> pairs(adjust = "holm")

df_stat %>%
  dplyr::group_by(Day, Condition) %>%
  dplyr::summarise(n_animals = dplyr::n_distinct(Mouse...1),
                   .groups = "drop") %>%
  dplyr::arrange(Day, Condition)

# Stats Fig 2C, right panel - First 6 days only @ 8 weeks

dfSO_8w <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '2months') %>%
  dplyr::filter(!Mouse...1 %in% c("J1", "K1", "V1", "W2", "X4", "AY31","AZ4", "AZ6", "AZ7", "AX3", "AQ52")) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Pct_side_omission = as.numeric(Pct_side_omission)
  )

table(unique(dfSO_8w[, c("Mouse...1", "Condition")])$Condition)

df_stat = subset(dfSO_8w, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Pct_side_omission'))

# Mixed model - preferred 
m1 <- lmerTest::lmer(Pct_side_omission ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

# Post hoc: compare groups within each day
emm <- emmeans(m1, ~ Condition | Day)
emmeans(m1, ~ Condition | Day) |> pairs(adjust = "holm")

df_stat %>%
  dplyr::group_by(Day, Condition) %>%
  dplyr::summarise(n_animals = dplyr::n_distinct(Mouse...1),
                   .groups = "drop") %>%
  dplyr::arrange(Day, Condition)


# Stats Panel D 

library(readr)
library(dplyr)
library(purrr)

# ------------------------------------------------------------
# Function equivalent to calculate_average_latency()
# ------------------------------------------------------------

calculate_average_latency <- function(path) {
  
  # Get all CSV files in the folder
  files <- list.files(
    path = path,
    pattern = "\\.csv$",
    full.names = TRUE
  )
  
  # Process each CSV
  results_df_phase1 <- map_dfr(files, function(file_path) {
    
    # Get filename only
    filename <- basename(file_path)
    
    # Extract mouse, date and phase from filename
    # Equivalent to:
    # ele_filename = filename.split('_')
    # mouse = ele_filename[0]
    # date = ele_filename[1]
    # phase = ele_filename[2]
    
    ele_filename <- strsplit(filename, "_")[[1]]
    
    mouse <- ele_filename[1]
    date  <- ele_filename[2]
    phase <- ele_filename[3]
    
    # Read CSV without header
    df <- read.csv(
      file_path,
      header = FALSE,
      stringsAsFactors = FALSE
    )
    
    # Check that there are at least 2 columns
    if (ncol(df) < 2) {
      message(
        paste(
          "File", filename,
          "does not have at least two columns. Skipping."
        )
      )
      return(NULL)
    }
    
    # Second column = latency
    latencies <- as.numeric(df[[2]])
    
    # Convert milliseconds to seconds
    latencies_sec <- latencies / 1000
    
    # Calculate average latency
    average_latency <- mean(
      latencies_sec,
      na.rm = TRUE
    )
    
    # Return one row for this mouse/file
    data.frame(
      Mouse = mouse,
      Date = date,
      AvgLatency = average_latency,
      Phase = phase,
      stringsAsFactors = FALSE
    )
  })
  
  print(results_df_phase1)
  
  return(results_df_phase1)
}

path_3weeks <- "C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/Phase1_Files/Analysis_Files"

results_3weeks <- calculate_average_latency(path_3weeks)

path_8weeks <-"C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/Phase1_Files/Analysis_Files/2months/Berenice"

results_8weeks <- calculate_average_latency(path_8weeks)


results_3weeks <- results_3weeks %>%
  mutate(Time = "3weeks")

results_8weeks <- results_8weeks %>%
  mutate(Time = "8weeks")

results_df_phase1 <- bind_rows(
  results_3weeks,
  results_8weeks
)

# Save readable Excel-compatible file
write.csv(results_df_phase1, "results_df_phase1.csv", row.names = FALSE)

metadata <- read_excel("C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")

metadata_unique <- metadata %>%
  select(Mouse...1, Condition) %>%
  distinct()
metadata_unique <- metadata_unique %>%
  rename(Mouse = `Mouse...1`)

results_df_phase1 <- results_df_phase1 %>%
  left_join(
    metadata_unique,
    by = "Mouse"
  )

# 3 weeks
t.test(
  AvgLatency ~ Condition,
  data = subset(results_df_phase1, Time == "3weeks"),
  var.equal = FALSE
)

# 8 weeks
t.test(
  AvgLatency ~ Condition,
  data = subset(results_df_phase1, Time == "8weeks"),
  var.equal = FALSE
)


# Nb of mice 

n_animals <- results_df_phase1 %>%
  group_by(Time, Condition) %>%
  summarise(
    n = n_distinct(Mouse),
    .groups = "drop"
  )

n_animals

# Stats Panel E

df_motiv <- read_excel("C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/MotivationTest_AdlibitumFood.xlsx")

# Apply the same exclusions as in the plotting code (based on histo exclusion)
df_motiv <- df_motiv[!(df_motiv$Mouse %in% c("Nb0", "Nb1", "Nb2", "Nb3", "AY31")), ]

sub <- df_motiv[, c("Condition", "Food_consumed_Hourly")]
sub <- na.omit(sub)
sub <- sub[sub$Condition %in% c("CTL", "asyn"), ]

# Make sure Condition is a factor
sub$Condition <- factor(sub$Condition,
                        levels = c("CTL", "asyn"))

# Student's t-test

t_test <- t.test(
  Food_consumed_Hourly ~ Condition,
  data = sub,
  var.equal = TRUE,       # Student's t-test
  alternative = "two.sided"
)

t_test

# Animals' number 

df_motiv %>%
  group_by(Condition) %>%
  summarise(N = n_distinct(Mouse))



#####
##### Stats Figure 3
#####

df_phase2 <- readxl::read_xlsx("C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")

# Filter Histology

dfs_p2 <- df_phase2 %>%
  dplyr::filter(Time == "3weeks",!Mouse...1 %in% c('AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6', 'AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52')) %>%
  dplyr::filter(Time == "2months",!Mouse...1 %in% c("J1", "K1", "V1", "W2", "X4", "AY31","AZ4", "AZ6", "AZ7", "AX3", "AQ52"))

df <- readxl::read_xlsx("C:/Users/u0185834/OneDrive - KU Leuven/CognitivePaper/Data/Sorted_ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")

df_phase3 <- df %>%
  dplyr::filter(Day %in% 1:6) %>%
  dplyr::filter(Time == '3weeks') %>%
  dplyr::filter(Time == "3weeks",!Mouse...1 %in% c('AK4', 'AM22', 'AP0', 'AQ6')) %>%
  mutate(
    Mouse = factor('Mouse...1'),
    Condition = factor(Condition),
    Day = factor(Day),
    Time = factor(Time),
    Successful_trials = as.numeric(Successful_trials)
  )

df_stat = subset(df_phase3, select = c('Mouse...1', 'Condition', 'Day', 'Time', 'Successful_trials'))

# Nb of mice

table(unique(df_stat[, c("Mouse...1", "Condition")])$Condition)

# RM-ANOVA
a1 <- aov_car(Successful_trials ~ Condition * Day + Error(Mouse...1/Day), data = df_stat)
summary(a1)

# Mixed model
m1 <- lmerTest::lmer(Successful_trials ~ Condition * Day + (1 | Mouse...1), data = df_stat)
anova(m1)

# 