library(tidyverse)
library(here)
library(haven)
library(rdrobust)
library(readxl)


census_villages_ka <- read_csv("C:\\Users\\marti\\OneDrive\\Plocha\\research_projects\\scraping_nrega\\analysis\\census_villages_mp.csv")


audits_raw_ka <- read_csv("C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/scrapy_spiders/post_requests_test/sa_scraped_data_mp_all.csv")


audits_by_panch <- audits_raw_ka %>% 
  mutate(unmet_demand_dummy = unmet_demand %in% c('Yes, Huge Demand', 'Yes, Some Demand'),
         unmet_demand_scale = case_when(unmet_demand == 'Yes, Huge Demand' ~ 2,
                                        unmet_demand == 'Yes, Some Demand' ~ 1,
                                        unmet_demand %in% c('No', 'No, people get work when they want it') ~ 1),
         diff_in_total_exp = total_exp - total_given,
         diff_in_total_exp_pct = abs(diff_in_total_exp)/ total_given,
         diff_in_total_exp_log = log(abs(diff_in_total_exp) + 1)) %>% 
  group_by(panchayat_id) %>% 
  summarize(n_audits = n(),
            mean_unmet_demand = mean(unmet_demand_dummy, na.rm = T),
            mean_unmet_demand_scale = mean(unmet_demand_scale, na.rm = T),
            mean_issues_rep = mean(total_issues_reported, na.rm = T),
            mean_fm_amount = mean(fm_amount, na.rm = T),
            mean_fm_rep =  mean(fm_reported, na.rm = T),
            diff_in_total_exp_pct =  mean(diff_in_total_exp_pct, na.rm = T),
            diff_in_total_exp_log =  mean(diff_in_total_exp_log, na.rm = T)
            
  )


census_villages_ka <- census_villages_ka %>% 
  left_join(audits_by_panch, by = c('panchayat_code' = 'panchayat_id'))


unique_census_villages_ka <- census_villages_ka %>% 
  group_by(panchayat_code, village_census_code) %>% 
  slice(1) %>% 
  ungroup()


shrug_pc11r_key_ka <- read_dta("C:/Users/marti/OneDrive/Plocha/research_projects/hyderabad/data/shrug/shrug-v1.5.samosa-keys-dta/shrug_pc11r_key.dta") %>%
  filter(pc11_state_id == 23)

census_villages_mp_merged <- census_villages_ka %>% 
  inner_join(shrug_pc11r_key_ka, by = c('village_census_code' = 'pc11_village_id'))