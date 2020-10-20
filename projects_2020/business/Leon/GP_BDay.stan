data {
  int<lower=1> N; // number of data points
  real x[N]; // data
  vector[N] y;
}

transformed data {
  vector[N] mu = rep_vector(0, N); // mean
}

parameters {
  real<lower=0> l; // time scale parameter
  real<lower=0> logsigma; // log-uniform prior for sigma
  real<lower=0> sigma1;
  real<lower=0> epsilon;
}

model {
  matrix[N,N] K = cov_exp_quad(x, sigma1, l) + diag_matrix(rep_vector(square(epsilon), N)); // Covariance function
  matrix[N,N] L_K = cholesky_decompose(K); // Faster for large datasets
  
  l ~ normal(0, 3);
  sigma1 ~ normal(0, 1);
  epsilon ~ normal(0, exp(logsigma));
  
  y ~ multi_normal_cholesky(mu, L_K);
}

//generated quantities {
//  vector[N] f = multi_normal_rng(mu, K);
//}
