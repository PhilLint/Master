#install.packages("rjson")
library(rjson)
library(ggplot2)
library(reshape2)


full_json <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\full_experiment_results.json"
full_ <- fromJSON(paste(readLines(full_json), collapse=""))

last_json <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\last_experiment_results.json"
last_ <- fromJSON(paste(readLines(last_json), collapse=""))

sudoku_names = c(names(full_), names(last_))

random_list_file <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\experiment_results_random_list.json"
random_json <- fromJSON(paste(readLines(random_list_file), collapse=""))
names(random_json) = sudoku_names
random_df <- data.frame(matrix(unlist(random_json), nrow=length(random_json), byrow=T),stringsAsFactors=FALSE)
names(random_df) = c("conflicts", "Number_assignments", "number_removed_unit", 
                     "splits", "DPLL_calls", "runtime", "number_givens")

# 2936 sudokus with no split solved
table(random_df$splits)
random_df = random_df[random_df$splits>0,]


dlcs_list_file <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\experiment_results_dlcs_list.json"
dlcs_json <- fromJSON(paste(readLines(dlcs_list_file), collapse=""))
names(dlcs_json) = sudoku_names
dlcs_df <- data.frame(matrix(unlist(dlcs_json), nrow=length(dlcs_json), byrow=T),stringsAsFactors=FALSE)
names(dlcs_df) = c("conflicts", "Number assignments", "number_removed_unit", 
                     "splits", "DPLL calls", "runtime", "number of givens")

dlcs_df = dlcs_df[dlcs_df$splits>0,]

dlis_list_file <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\experiment_results_dlis_list.json"
dlis_json <- fromJSON(paste(readLines(dlis_list_file), collapse=""))
names(dlis_json) = sudoku_names
dlis_df <- data.frame(matrix(unlist(dlis_json), nrow=length(dlis_json), byrow=T),stringsAsFactors=FALSE)
names(dlis_df) = c("conflicts", "Number assignments", "number_removed_unit", 
                     "splits", "DPLL calls", "runtime", "number of givens")
dlis_df = dlis_df[dlis_df$splits>0,]

jw_max_list_file <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\experiment_results_jeroslow_max_list.json"
jw_max_json <- fromJSON(paste(readLines(jw_max_list_file), collapse=""))
names(jw_max_json) = sudoku_names
jw_max_df <- data.frame(matrix(unlist(jw_max_json), nrow=length(jw_max_json), byrow=T),stringsAsFactors=FALSE)
names(jw_max_df) = c("conflicts", "Number assignments", "number_removed_unit", 
                     "splits", "DPLL calls", "runtime", "number of givens")
jw_max_df = jw_max_df[jw_max_df$splits>0,]


jw_min_list_file <- "C:\\Users\\lintl\\Documents\\GitHub\\KR\\experiment_results_jeroslow_min_list.json"
jw_min_json <- fromJSON(paste(readLines(jw_min_list_file), collapse=""))
names(jw_min_json) = sudoku_names
jw_min_df <- data.frame(matrix(unlist(jw_min_json), nrow=length(jw_min_json), byrow=T),stringsAsFactors=FALSE)
names(jw_min_df) = c("conflicts", "Number assignments", "number_removed_unit", 
                     "splits", "DPLL calls", "runtime", "number of givens")
jw_min_df = jw_min_df[jw_min_df$splits>0,]

#-----
# BOXPLOTS
full_conflicts = cbind("random" = as.numeric(random_df[,1]),"dlcs" = as.numeric(dlcs_df[,1]),
                       "dlis" = as.numeric(dlis_df[,1]), "jw_max" = as.numeric(jw_max_df[,1]),
                       "jw_min" = as.numeric(jw_min_df[,1]))
rownames(full_conflicts) = rownames(random_df)

pdf("box_conflicts.pdf", width = 6, height = 4)
ggplot(melt(full_conflicts), aes(x = Var2, y = value)) +
  geom_boxplot(outlier.alpha = 0.15)+
  xlab("") + ylab("")+
  scale_y_continuous(limits = c(5, 100))+
  theme(axis.text=element_text(size=14),
          axis.title=element_text(size=12))
dev.off()

full_splits = cbind("random" = as.numeric(random_df[,4]),"dlcs" = as.numeric(dlcs_df[,4]),
                       "dlis" = as.numeric(dlis_df[,4]), "jw_max" = as.numeric(jw_max_df[,4]),
                       "jw_min" = as.numeric(jw_min_df[,4]))
rownames(full_splits) = rownames(random_df)

pdf("box_splits.pdf", width = 6, height = 4)
ggplot(melt(full_splits), aes(x = Var2, y = value)) +
  geom_boxplot(outlier.alpha = 0.15)+
  xlab("") + ylab("")+
  scale_y_continuous(limits = c(5, 200))+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=12))
dev.off()

full_unit_removed = cbind("random" = as.numeric(random_df[,3]),"dlcs" = as.numeric(dlcs_df[,3]),
                    "dlis" = as.numeric(dlis_df[,3]), "jw_max" = as.numeric(jw_max_df[,3]),
                    "jw_min" = as.numeric(jw_min_df[,3]))
rownames(full_unit_removed) = rownames(random_df)

pdf("box_units.pdf", width = 6, height = 4)
ggplot(melt(full_unit_removed), aes(x = Var2, y = value)) +
  geom_boxplot(outlier.alpha = 0.05)+
  xlab("") + ylab("")+
  scale_y_continuous(limits = c(200, 8000))+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=12))
dev.off()


full_runtime = cbind("random" = as.numeric(random_df[,6]),"dlcs" = as.numeric(dlcs_df[,6]),
                          "dlis" = as.numeric(dlis_df[,6]), "jw_max" = as.numeric(jw_max_df[,6]),
                          "jw_min" = as.numeric(jw_min_df[,6]))
rownames(full_runtime) =  rownames(random_df)

pdf("box_runtime.pdf", width = 6, height = 4)
ggplot(melt(full_runtime), aes(x = Var2, y = value)) +
  geom_boxplot(outlier.alpha = 0.05)+
  xlab("") + ylab("")+
  scale_y_continuous(limits = c(0, 20))+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=12))
dev.off()

#-----
# scatterplot given literals against conflicts and stuff 
# Loess method
random_df$conflicts = as.numeric(random_df$conflicts) 
random_df$number_givens = as.numeric(random_df$number_givens) 

full_scatter = as.data.frame(cbind("random" = random_df$conflicts, 
                     "dlcs" = dlcs_df$conflicts, 
                     "dlis" = dlis_df$conflicts, 
                     "jw_min" = jw_min_df$conflicts, 
                     "jw_max" = jw_max_df$conflicts, 
                     "givens" = random_df$number_givens,
                     "id" = rownames(random_df)))

full_scatter_melt = melt(full_scatter, id.vars = c("id", "givens"))

full_scatter_melt$value = as.numeric(full_scatter_melt$value)
full_scatter_melt$givens = as.numeric(levels(full_scatter_melt$givens))[full_scatter_melt$givens]

pdf("scatter_conflicts.pdf", width = 6, height = 4)
ggplot(full_scatter_melt, aes(x=givens, y=value)) + geom_point(alpha = 0.05, size = 2)+
  scale_y_continuous(limits = c(0, 10000))+
  scale_x_continuous(limits = c(17, 40))+
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=12))+
  ylab("confilcts")
dev.off()


full_scatter_splits = as.data.frame(cbind("random" = random_df$splits, 
                                   "dlcs" = dlcs_df$splits, 
                                   "dlis" = dlis_df$splits, 
                                   "jw_min" = jw_min_df$splits, 
                                   "jw_max" = jw_max_df$splits, 
                                   "givens" = random_df$number_givens,
                                   "id" = rownames(random_df)))

full_scatter_splits_melt = melt(full_scatter_splits, id.vars = c("id", "givens"))

full_scatter_splits_melt$value = as.numeric(full_scatter_melt$value)
full_scatter_splits_melt$givens = as.numeric(levels(full_scatter_splits_melt$givens))[full_scatter_splits_melt$givens]

pdf("scatter_splits.pdf", width = 6, height = 4)
ggplot(full_scatter_splits_melt, aes(x=givens, y=value)) + geom_point(alpha = 0.05, size = 2)+
  scale_y_continuous(limits = c(0, 10000))+
  scale_x_continuous(limits = c(17, 40))+
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=12))+
  ylab("splits")
dev.off()


full_scatter_unit = as.data.frame(cbind("random" = random_df$number_removed_unit, 
                                          "dlcs" = dlcs_df$number_removed_unit, 
                                          "dlis" = dlis_df$number_removed_unit, 
                                          "jw_min" = jw_min_df$number_removed_unit, 
                                          "jw_max" = jw_max_df$number_removed_unit, 
                                          "givens" = random_df$number_givens,
                                          "id" = rownames(random_df)))

full_scatter_unit_melt = melt(full_scatter_unit, id.vars = c("id", "givens"))

full_scatter_unit_melt$value = as.numeric(full_scatter_unit_melt$value)
full_scatter_unit_melt$givens = as.numeric(levels(full_scatter_unit_melt$givens))[full_scatter_unit_melt$givens]

pdf("scatter_units.pdf", width = 6, height = 4)
ggplot(full_scatter_unit_melt, aes(x=givens, y=value)) + geom_point(alpha = 0.05, size = 2)+
  scale_y_continuous(limits = c(0, 100000))+
  scale_x_continuous(limits = c(17, 40))+
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=12))+
  ylab("units removed")
dev.off()


#-----
# DUE TO A LOSS OF CODE AT THE LAST MINUTE ARE A FEW LINES GONE
# statistical tests

# are data normally distributed? -> histogram

random_df$conflicts
ggplot(data=random_df, aes(random_df$conflicts)) + geom_histogram(bins = 50)
  
# that was the wilcox test
wilcox.test()

# that was the correlation test 
cor.test()
  
  



