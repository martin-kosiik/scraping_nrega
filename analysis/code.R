library(tidyverse)
library(here)
library(haven)

library(readxl)
census_codes_ka <- read_excel("C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/census_codes_ka.xls", 
                              skip = 1)

names(census_codes_ka) <- c('state_2001', 'district_2001', 'subdistrict_2001', 'village_2001', 'name_2001',
                            'state_2011', 'district_2011', 'subdistrict_2011', 'village_2011', 'name_2011')

census_codes_ka %>% 
  count(village_2011, sort = T) %>% View()


census_codes_ka %>% 
  add_count(village_2011) %>% 
  filter(village_2011 != '000000') %>% 
  filter(n > 1) %>% 
  View()

census_villages_ka <- read_csv("census_villages_ka.csv")


audits_raw_ka <- read_csv("C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/scrapy_spiders/post_requests_test/sa_scraped_data_ka_all.csv")


audits_by_panch <- audits_raw_ka %>% 
  mutate(unmet_demand_dummy = unmet_demand %in% c('Yes, Huge Demand', 'Yes, Some Demand')) %>% 
  group_by(panchayat_id) %>% 
  summarize(n_audits = n(),
            mean_unmet_demand = mean(unmet_demand_dummy, na.rm = T),
            mean_issues_rep = mean(total_issues_reported, na.rm = T),
            mean_fm_amount = mean(fm_amount, na.rm = T),
            mean_fm_rep =  mean(fm_reported, na.rm = T)
  )
  

census_villages_ka <- census_villages_ka %>% 
  left_join(audits_by_panch, by = c('panchayat_code' = 'panchayat_id'))


census_villages_ka %>% 
  mutate(comb = str_c(village_name,village_census_code )) %>% 
  count(village_census_code, sort = T)

census_villages_ka %>% 
  filter(village_census_code != 'missing') %>% 
  mutate(comb = str_c(village_name,village_census_code )) %>% 
  count(village_census_code, district_census_code, sort = T)


census_villages_ka %>% 
  filter(village_census_code != 'missing') %>% 
  mutate(comb = str_c(village_name,village_census_code )) %>% 
  count(village_census_code, district_census_code, block_census_code, sort = T)

census_villages_ka %>% 
  filter(village_census_code == "602023") %>% 
  View()

census_villages_ka %>% 
  mutate(comb = str_c(village_name,village_census_code )) %>% 
  count(comb, sort = T)


census_villages_ka %>% 
  filter(village_name == 'AKKURU')




unique_census_villages_ka <- census_villages_ka %>% 
  group_by(panchayat_code, village_census_code) %>% 
  slice(1) %>% 
  ungroup()


unique_census_villages_ka %>% 
  count(village_census_code, sort = T)
  

unique_census_villages_ka %>% 
  filter(village_census_code == '602023') %>% 
  View()


unique_census_villages_ka %>% 
  filter(village_census_code != 'missing') %>% 
  mutate(comb = str_c(village_name,village_census_code )) %>% 
  count(village_census_code, district_census_code, sort = T) %>% View()


unique_census_villages_ka %>% 
  filter(village_census_code != 'missing') %>% 
  mutate(comb = str_c(village_name,village_census_code )) %>% 
  count(village_census_code, block_census_code, district_census_code, sort = T) %>% View()





census_villages_ka %>% 
  summarise(n_missing = sum(is.na(n_audits)))

shrug_pc01 <- read_dta("C:/Users/marti/OneDrive/Plocha/research_projects/hyderabad/data/shrug/shrug-v1.5.samosa-pop-econ-census-dta/shrug_pc01.dta")
shrug_pc11 <- read_dta("C:/Users/marti/OneDrive/Plocha/research_projects/hyderabad/data/shrug/shrug-v1.5.samosa-pop-econ-census-dta/shrug_pc11.dta")


shrug_pc01r_key <- read_dta("C:/Users/marti/OneDrive/Plocha/research_projects/hyderabad/data/shrug/shrug-v1.5.samosa-keys-dta/shrug_pc01r_key.dta")

shrug_pc11r_key <- read_dta("C:/Users/marti/OneDrive/Plocha/research_projects/hyderabad/data/shrug/shrug-v1.5.samosa-keys-dta/shrug_pc11r_key.dta")


#shrug_pc01r_key <- shrug_pc01r_key %>% 
#  left_join(shrug_pc01, by = 'shrid')

# Karnataka - 2011 cennsus code is 29


shrug_pc11r_key <- shrug_pc11r_key %>% 
  left_join(shrug_pc01, by = 'shrid')

shrug_pc11r_key_ka <- shrug_pc11r_key %>% 
  filter(pc11_state_id == 29)

shrug_pc11r_key_ka %>% 
  count(pc11_village_id, sort = T)



shrug_pc11r_key %>% 
  filter(pc11_state_id == 29, pc11_district_id == 584, pc11_subdistrict_id == 29001) 
# 29001

shrug_pc11r_key %>% 
  filter(pc11_state_id == 29, pc11_district_id == 584) %>% 
  View()

shrug_pc11r_key %>% 
  filter(pc11_state_id == 29, pc11_district_id == 584) %>% 
  count(pc11_subdistrict_id)

census_villages_ka %>% 
  filter(district_census_code == 584) %>% 
  count(block_code)



census_villages_ka %>% 
  inner_join(shrug_pc11r_key, by = c('village_census_code' = 'pc11_village_id'))



census_villages_ka_merged <- census_villages_ka %>% 
  inner_join(shrug_pc11r_key_ka, by = c('village_census_code' = 'pc11_village_id')) %>% 
  #left_join(shrug_pc01r_key %>% filter(pc01_state_id == 29), by = 'shrid')
  left_join(shrug_pc01, by = 'shrid')
  
  
census_villages_ka_merged %>% 
  filter(!is.na(pc01_pca_tot_p))







##################################
# Mp

census_villages_mp <- read_csv("census_villages_mp.csv")


audits_raw_mp <- read_csv("C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/scrapy_spiders/post_requests_test/sa_scraped_data_mp_all.csv")

audits_raw_mp %>% 
  count(unmet_demand)



audits_by_panch <- audits_raw_mp %>% 
  mutate(unmet_demand_dummy = unmet_demand %in% c('Yes, Huge Demand', 'Yes, Some Demand'),
         unmet_demand_scale = case_when(unmet_demand == 'Yes, Huge Demand' ~ 2,
                                        unmet_demand == 'Yes, Some Demand' ~ 1,
                                        unmet_demand %in% c('No', 'No, people get work when they want it') ~ 1)) %>% 
  group_by(panchayat_id) %>% 
  summarize(n_audits = n(),
            mean_unmet_demand = mean(unmet_demand_dummy, na.rm = T),
            mean_unmet_demand_scale = mean(unmet_demand_scale, na.rm = T),
            mean_issues_rep = mean(total_issues_reported, na.rm = T),
            mean_fm_amount = mean(fm_amount, na.rm = T),
            mean_fm_rep =  mean(fm_reported, na.rm = T)
  )


census_villages_mp <- census_villages_mp %>% 
  left_join(audits_by_panch, by = c('panchayat_code' = 'panchayat_id'))


shrug_pc11r_key_mp <- shrug_pc11r_key %>% 
  filter(pc11_state_id == 23)

shrug_pc11r_key_mp %>% 
  count(pc11_village_id, sort = T)


census_villages_mp_merged <- census_villages_mp %>% 
  inner_join(shrug_pc11r_key_mp, by = c('village_census_code' = 'pc11_village_id')) %>% 
  #left_join(shrug_pc01r_key %>% filter(pc01_state_id == 29), by = 'shrid')
  left_join(shrug_pc11, by = 'shrid')

panchayats_mp <- census_villages_mp_merged %>% 
  group_by(village_census_code) %>% 
  slice(1) %>% 
  ungroup() %>% 
  group_by(panchayat_code) %>% 
  summarize(total_pop_2011 = sum(pc11_pca_tot_p, na.rm = T),
            mean_unmet_demand_scale = mean(mean_unmet_demand_scale, na.rm = T))
  #mutate()
  
