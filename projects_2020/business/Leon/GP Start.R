library(rstan)
N <- 100
data <- list(N = N, 
             x = seq(-10, 10, length.out = N),
             alpha = 1,
             rho = 1)
ndraws <- 50
fit <- stan(file = "GP_start.stan",
            data = data,
            algorithm = "Fixed_param",
            warmup = 0,
            chains = 1,
            iter = ndraws)
params <- extract(fit)
plot(c(-10,10), c(-5,5), ty="n")
for (i in 1:ndraws) {
  lines(data$x, params$f[i,], pch = 20, col = rgb(0, 0.55, 0.5, 0.2), cex = 0.5)
}
#points(data$x, params$f[ndraws-1, ], pch = 20, col = "black", cex = 0.5)
lines(data$x, colMeans(params$f), lwd = 3)
