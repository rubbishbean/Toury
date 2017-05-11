library(readxl)
environment <- read_excel('/Users/xpan/Downloads/Environment.xlsx')

Biodiversity <- environment[,2:3]
rownames(Biodiversity) <- environment[,1]
Biodiversity_agg <- as.matrix(apply(Biodiversity,1,mean, na.rm = TRUE) )

CO2_Emission <- environment[,5:12]
rownames(CO2_Emission) <- environment[,4]
Biodiversity_agg <- as.matrix(apply(CO2_Emission,1,mean, na.rm = TRUE) )

Energy_Related_Emissions <- environment[!is.na(environment[,13]),14:18]
rownames(Energy_Related_Emissions) <- environment[!is.na(environment[,13]),13]
Energy_Related_Emissions_agg <- as.matrix(apply(Energy_Related_Emissions,1,mean, na.rm = TRUE) )

Consumption_ODP <- environment[!is.na(environment[,19]),20:26]
rownames(Consumption_ODP) <- environment[!is.na(environment[,19]),19]
Consumption_ODP_agg <- as.matrix(apply(Consumption_ODP,1,mean, na.rm = TRUE) )

Use_of_Fertilizers <- environment[!is.na(environment[,27]),28:32]
rownames(Use_of_Fertilizers) <- environment[!is.na(environment[,27]),27]
Use_of_Fertilizers_agg <- as.matrix(apply(Use_of_Fertilizers,1,mean, na.rm = TRUE) )
x1 = merge(Biodiversity_agg,Biodiversity_agg, all =TRUE, by = 0)

x2 = merge(x1,Energy_Related_Emissions_agg, all =TRUE, by.x = "Row.names", by.y = 0) 
x3 = merge(x2,Consumption_ODP_agg, all =TRUE, by.x = "Row.names", by.y = 0) 
environment = merge(x3,Use_of_Fertilizers_agg, all =TRUE, by.x = "Row.names", by.y = 0) 

colnames(environment) = c("location","Biodiversity","CO2_Emission","Energy_Related_Emissions","Consumption_ODP","Use_of_Fertilizers")
write.csv(environment, "environment_agg.csv")
