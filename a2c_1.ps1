python train.py `
 --algo a2c --env PortfolioAllocation-v0 `
 -tb tensorboard `
 --n-timesteps 252 `
 --optimization-log-path ac2_50_sharpe_normalized/opt_log `
 --log-folder ac2_50_sharpe_normalized/log `
 --save-freq 50 `
 --vec-env dummy `
 --n-trials 50 `
 --optimize-hyperparameters `
 --study-name ac2_50_sharpe_normalized `
 --verbose 1 `
 --env-kwargs filename:"'sp500.csv'", date_from:"'2008-01-01'", date_to:"'2017-12-31'", sample_size:500, reward_function:"'sharpe'"