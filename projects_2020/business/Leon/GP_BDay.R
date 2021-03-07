library(rstan)
library(tidyverse)

df <- ga.results.16.20 %>% filter(year == 2017) %>% select(t, sessions)
m.y <- mean(df$sessions)
sd.y <- sd(df$sessions)
df$sessions <- (df$sessions-m.y)/sd.y
data <- list(N = nrow(df), 
             x = df$t,
             y = df$sessions)
fit <- stan(file = "GP_BDay.stan",
            data = data,
            warmup = 500,
            chains = 1,
            iter = 1000)
params <- rstan::extract(fit)

N_obs <- 300
obs <- sort(sample(1:length(df$t), N_obs))
N_predict <- 100
x_predict <- seq(range(data$x)[1], range(data$x)[2], length.out = N_predict)
pred_data <- list(N1 = N_obs, 
                  x1 = data$x[obs],
                  y1 = data$y[obs],
                  N2 = N_predict,
                  x2 = x_predict)
pred_fit <- stan(file = "sim_GP.stan",
                 data = pred_data,
                 warmup = 1000,
                 chains = 1,
                 iter = 2000)
pred_params <- rstan::extract(pred_fit)
plot(range(pred_data$x1), range(pred_data$y1), ty="n")
for (i in 1:N_predict) {
  lines(x_predict, pred_params$f[i, (N_obs+1):(N_obs+N_predict)], col=rgb(0,0,0,0.1))
}
points(df$t, df$sessions, pch=20, col="orange", cex=0.3)
points(pred_data$x2, colMeans(pred_params$y2), pch=20, col="red", cex=0.3)
labels()
