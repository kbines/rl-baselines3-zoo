from typing import Any, Dict

import numpy as np
import optuna
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
from torch import nn as nn

from utils import linear_schedule

def sample_a2c_params(trial: optuna.Trial) -> Dict[str, Any]:
    """
    Sampler for A2C hyperparams.

    :param trial:
    :return:
    """
    gamma = trial.suggest_categorical("gamma", [0.9, 0.95, 0.98, 0.99, 0.995, 0.999, 0.9999])
    normalize_advantage = trial.suggest_categorical("normalize_advantage", [False, True])
    max_grad_norm = trial.suggest_categorical("max_grad_norm", [0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 5])
    # Toggle PyTorch RMS Prop (different from TF one, cf doc)
    use_rms_prop = trial.suggest_categorical("use_rms_prop", [False, True])
    gae_lambda = trial.suggest_categorical("gae_lambda", [0.8, 0.9, 0.92, 0.95, 0.98, 0.99, 1.0])
    #n_steps = trial.suggest_categorical("n_steps", [8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    n_steps = trial.suggest_categorical("n_steps", [1,5,10,20])
    lr_schedule = trial.suggest_categorical("lr_schedule", ["linear", "constant"])
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1)
    ent_coef = trial.suggest_loguniform("ent_coef", 0.00000001, 0.1)
    vf_coef = trial.suggest_uniform("vf_coef", 0, 1)
    # Uncomment for gSDE (continuous actions)
    log_std_init = trial.suggest_uniform("log_std_init", -4, 1)
    ortho_init = trial.suggest_categorical("ortho_init", [False, True])
    net_arch = trial.suggest_categorical("net_arch", ["small", "medium","3small","3medium"])
    sde_net_arch = trial.suggest_categorical("sde_net_arch", [None, "tiny", "small"])
    # full_std = trial.suggest_categorical("full_std", [False, True])
    activation_fn = trial.suggest_categorical('activation_fn', ['tanh', 'relu', 'elu', 'leaky_relu'])
    # activation_fn = trial.suggest_categorical("activation_fn", ["tanh", "relu"])

    if lr_schedule == "linear":
        learning_rate = linear_schedule(learning_rate)

    net_arch = {
        "tiny": [dict(pi=[32, 32], vf=[32, 32])],
        "small": [dict(pi=[64, 64], vf=[64, 64])],
        "medium": [dict(pi=[256, 256], vf=[256, 256])],
        "3small": [dict(pi=[64, 64, 64], vf=[64, 64, 64])],
        "3medium": [dict(pi=[256, 256, 256], vf=[256, 256, 256])],
    }[net_arch]

    sde_net_arch = {
         None: None,
         "tiny": [64],
         "small": [64, 64],
     }[sde_net_arch]

    activation_fn = {"tanh": nn.Tanh, "relu": nn.ReLU, "elu": nn.ELU, "leaky_relu": nn.LeakyReLU}[activation_fn]

    return {
        "gamma": gamma,
        "normalize_advantage": normalize_advantage,
        "max_grad_norm": max_grad_norm,
        "use_rms_prop": use_rms_prop,
        "gae_lambda": gae_lambda,
        "n_steps": n_steps,
        "learning_rate": learning_rate,
        "ent_coef": ent_coef,
        "vf_coef": vf_coef,
        "policy_kwargs": dict(
            log_std_init=log_std_init,
            ortho_init=ortho_init,
            net_arch=net_arch,
            sde_net_arch=sde_net_arch,
            activation_fn=activation_fn
        ),
    }


HYPERPARAMS_SAMPLER = {
    "a2c": sample_a2c_params
}
