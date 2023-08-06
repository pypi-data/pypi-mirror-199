import rich
import numpy as np
import pandas as pd
import plotext as plt
import scipy.sparse as sp
import plotly.express as px
# Long only portfolio optimization.
import cvxpy as cp

from .progression import Pbar, console

__all__ = ["init_portfolios", "compute_tradeoff_curve", "experiment"]

np.random.seed(1)


def init_portfolios(num_assets: int = 10):
    mu = np.abs(np.random.randn(num_assets, 1))
    Sigma = np.random.randn(num_assets, num_assets)
    Sigma = Sigma.T.dot(Sigma)

    w = cp.Variable(num_assets)
    gamma = cp.Parameter(nonneg=True)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma)
    prob = cp.Problem(cp.Maximize(ret - gamma * risk), [cp.sum(w) == 1, w >= 0])

    return mu, Sigma, w, gamma, ret, risk, prob

def compute_tradeoff_curve(
    mu, Sigma, w,
    gamma, ret, risk,
    prob,
    gamma_lower: float = -4,
    gamma_upper: float = 4,
    gamma_samples: int = 100,
    ):
    # Compute trade-off curve.
    risk_data = np.zeros(gamma_samples)
    ret_data = np.zeros(gamma_samples)
    gamma_vals = np.logspace(gamma_lower, gamma_upper, num=gamma_samples)

    results = []
    with Pbar as progress:
        task = progress.add_task("Computing trade-off curve...", total=gamma_samples)
        for i in range(gamma_samples):
            progress.update(task, description=f"Computing trade-off curve for ɣ = {gamma_vals[i]}")
            gamma.value = gamma_vals[i]
            prob.solve()
            risk_data[i] = cp.sqrt(risk).value
            ret_data[i] = ret.value
            results += [{
                'gamma': gamma_vals[i],
                'risk': risk_data[i],
                'return': ret_data[i],
                **{f'w{i}': w.value[i] for i in range(len(w.value))}
            }]
            progress.update(task, advance=1)

    console.print("✅ Done! (in [bold green]{task.completed} seconds)[/bold green]")
    
    console.print("📊 Plotting trade-off curve (quickly in terminal, for better graphs call the `plot` function)...")
    
    plt.plot(risk_data, ret_data)
    plt.xlabel("Standard deviation")
    plt.ylabel("Return")
    plt.show()


    df = pd.DataFrame(results)
    
    console.print("📅 Results:")
    console.print(df)
    
    return {
        "mu": mu,
        "Sigma": Sigma,
        "results": df,
    }


def plot_tradeoff_curve(risk_data, ret_data, gamma_vals):
    markers_pos = (29, 40)
    

    # markers_on = [29, 40]
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # plt.plot(risk_data, ret_data, "g-")
    # for marker in markers_on:
    #     plt.plot(risk_data[marker], ret_data[marker], "bs")
    #     ax.annotate(
    #         r"$\gamma = %.2f$" % gamma_vals[marker],
    #         xy=(risk_data[marker] + 0.08, ret_data[marker] - 0.03),
    #     )
    # for i in range(n):
    #     plt.plot(cp.sqrt(Sigma[i, i]).value, mu[i], "ro")
    # plt.xlabel("Standard deviation")
    # plt.ylabel("Return")
    # plt.show()
    
def experiment(gamma_lower: float = -4, gamma_upper: float = 4, gamma_samples: int = 100):
    mu, Sigma, w, gamma, ret, risk, prob = init_portfolios(
        num_assets=gamma_samples
    )
    return compute_tradeoff_curve(mu, Sigma, w, gamma, ret, risk, prob)
    
    
if __name__ == '__main__':
    experiment()