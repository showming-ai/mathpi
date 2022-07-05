arg <- commandArgs(trailingOnly = TRUE)
print(arg)
library(traj)
file_path <- paste0("C:/git-repos/mathpix_to_sympy/",arg[1],"_",arg[2],".csv")
data <- read.table(file_path, encoding="utf-8", header = TRUE, stringsAsFactors = FALSE, sep = ",")
print(data)
time_file_path <- paste0("C:/git-repos/mathpix_to_sympy/",arg[1],"_",arg[2],"_time.csv")
time <- read.table(time_file_path, encoding="utf-8", header = TRUE, stringsAsFactors = FALSE, sep = ",")
print(time)
s1 = step1measures(data, time, ID = TRUE)
s2 = step2factors(s1)
s3 = step3clusters(s2, nclusters = 3)
s3$clust.distr
x <- data
y <- s3$clusters
z <- merge(x,y,by="ID")
print(z)
#write.csv(z, row.names = FALSE, file = paste0("R_result_",arg[1],"_",arg[2],".csv"), quote = TRUE)
write.csv(z, row.names = FALSE, file = paste0("C:/git-repos/mathpix_to_sympy/",arg[1],"_",arg[2],".csv"), quote = FALSE)