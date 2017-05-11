library(readxl)
total <- read_excel("~/Downloads/total.xlsx")
total = total[!is.na(total$location),]
data_agg <- aggregate(total,by = list(total$location),FUN = mean, na.rm=F)[,-2]
colnames(data_agg)[1] <- c('location')
p = dim(data_agg)[2]

#replace NA as median and replace 0 as median

for ( i in 2:p){
  data_agg[is.na(data_agg[,i]),i] <- median(data_agg[,i], na.rm = TRUE)
  data_agg[data_agg[,i] == 0, i]<- median(data_agg[,i], na.rm = TRUE)
}

data_agg_1 = data_agg[sapply(data_agg,is.numeric)]

################HeatMap###############################################
cormat <- round(cor(data_agg_1),2)
head(cormat)
library(reshape2)
melted_cormat <- melt(cormat)
head(melted_cormat)
library(ggplot2)
ggplot(data = melted_cormat, aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()

get_lower_tri<-function(cormat){
  cormat[upper.tri(cormat)] <- NA
  return(cormat)
}
# Get upper triangle of the correlation matrix
get_upper_tri <- function(cormat){
  cormat[lower.tri(cormat)]<- NA
  return(cormat)
}
upper_tri <- get_upper_tri(cormat)
upper_tri

library(reshape2)
melted_cormat <- melt(upper_tri, na.rm = TRUE)
# Heatmap
library(ggplot2)
ggplot(data = melted_cormat, aes(Var2, Var1, fill = value))+
  geom_tile(color = "white")+
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), space = "Lab", 
                       name="Pearson\nCorrelation") +
  theme_minimal()+ 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()

reorder_cormat <- function(cormat){
  # Use correlation between variables as distance
  dd <- as.dist((1-cormat)/2)
  hc <- hclust(dd)
  cormat <-cormat[hc$order, hc$order]
}

# Reorder the correlation matrix
cormat <- reorder_cormat(cormat)
upper_tri <- get_upper_tri(cormat)
# Melt the correlation matrix
melted_cormat <- melt(upper_tri, na.rm = TRUE)
# Create a ggheatmap
ggheatmap <- ggplot(melted_cormat, aes(Var2, Var1, fill = value))+
  geom_tile(color = "white")+
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), space = "Lab", 
                       name="Pearson\nCorrelation") +
  theme_minimal()+ # minimal theme
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()
# Print the heatmap
print(ggheatmap)
##################################################################################

pairs(data_agg_1)
data_agg_log = log(data_agg_1)
data_agg.pca <- prcomp(data_agg_log)
summary(data_agg.pca) #The cumulative Proportion for PC6 = 0.86838
#Choose n.pca = 6
round(data_agg.pca$sdev,2)

plot(data_agg.pca$sdev,type="l", ylab="SD of PC", xlab="PC number")


names(data_agg.pca)
sort(abs(data_agg.pca$rotation[,1:6]))
plot(data_agg.pca)
biplot(data_agg.pca, scale = 0)

library(devtools)
install_github("vqv/ggbiplot")
library(ggbiplot)
data_agg.pca <- prcomp(data_agg_log)
ggbiplot(data_agg.pca, obs.scale = 1, var.scale = 1,
         groups = data_agg_log.class, ellipse = TRUE, circle = TRUE) +
  scale_color_discrete(name = '') +
  theme(legend.direction = 'horizontal', legend.position = 'top')


bcR.nmds <- metaMDS(data_agg_log,plot=TRUE)
ordiplot(bcR.nmds,type="points")
orditorp(bcR.nmds,display="sites",cex=.5,air=0.001)
#Minimum sums of squared distances (S^2) for a given dimension k (aka, Stress)
stressplot(bcR.nmds,main="Stress Plot for Bray-Curtis row-wise") #amazing
plot(bcR.nmds, type="t",main="NMDS Plot") ## 4 groups

library(cluster) 
fit <- kmeans(data_agg_log, 4)
data_agg_log <- as.matrix(data_agg_log)
clusplot(data_agg_log, fit$cluster, color=TRUE, shade=TRUE, 
          lines=0,main = "K-MEANS")

data_agg_log.class = as.factor(fit$cluster)



pairs(data_agg_1)
data_agg_log = log(data_agg_1)
data_agg.pca <- prcomp(data_agg_log)
summary(data_agg.pca) #The cumulative Proportion for PC6 = 0.86838
#Choose n.pca = 6
round(data_agg.pca$sdev,2)

plot(data_agg.pca$sdev,type="l", ylab="SD of PC", xlab="PC number")


names(data_agg.pca)
sort(abs(data_agg.pca$rotation[,1:6]))
plot(data_agg.pca)
biplot(data_agg.pca, scale = 0)

mu = colMeans(data_agg_log)

nComp = 6
Xhat = data_agg.pca$x[,1:nComp] %*% t(data_agg.pca$rotation[,1:nComp])
Xhat = scale(Xhat, center = -mu, scale = FALSE)

names(Xhat[1,])

require(caret)
trans = preProcess(data_agg_1, 
                   method=c("BoxCox", "center", 
                            "scale", "pca"))
PC = predict(trans, data_agg_1)

rate = c(3, 7, 9, 5, 4, 8, 6, 1, 2)


scale = data.frame(Xhat[1,]*rate)

write.csv(scale,'scale.csv')




