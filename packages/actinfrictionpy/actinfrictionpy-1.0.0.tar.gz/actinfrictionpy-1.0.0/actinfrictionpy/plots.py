"""Plotting classes.

Each plot type has its own class which inherits from a base class, Plot. See the
docstring of that class for more details.
"""


import matplotlib.pyplot as plt


class Plot:
    """Base class for all plot types.

    Attributes:
        f: Figure
        ax: Axis

    Methods:
        plot: Plot single timeseries
        plot_comparison: Plot multiple different timeseries
        plot_meanvar: Plot mean and variance
        setup_axis: Setup the axis, call after all plotting
        set_labels: Set labels, legend, colourbar
    """

    def __init__(self, f, ax):
        self._f = f
        self._ax = ax

    def set_labels(self):
        plt.legend()

    def plot_meanvar(self, t, mean, var, *args, **kwargs):
        self._ax.plot(t, mean, *args, **kwargs)
        self._ax.fill_between(
            t,
            mean - var**0.5,
            mean + var**0.5,
            color="0.8",
            zorder=0,
        )


class LambdaPlot(Plot):
    """Plot time series of lambda."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.lmbda, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(df_means.t, df_means.lmbda, df_vars.lmbda, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$\lambda$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class RadiusPlot(Plot):
    """Plot time series of ring radius in micro meters."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.R / 1e-6, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.R / 1e-6, df_vars.R / 1e-12, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$R / \si{\micro\meter}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class XPlot(Plot):
    """Plot time series of x position in meters."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.x, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(df_means.t, df_means.x, df_vars.x, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$x / \si{\meter}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class EquilibriumRadiusFractionPlot(Plot):
    """Plot time series of fraction of radius to equilibrium radius."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.R_eq_frac, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.R_eq_frac, df_vars.R_eq_frac, *args, **kwargs
        )

    def setup_axis(self):
        #        self._ax.set_ylabel(r"$(R_\text{max} - R) / (R_\text{max} - R_\text{eq})$")
        self._ax.set_ylabel(r"$\phi_\text{R}")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class NdtotPlot(Plot):
    """Plot time series of Ndtot."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.Ndtot, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(df_means.t, df_means.Ndtot, df_vars.Ndtot, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$N_\text{d, tot}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class NdOccupancyPlot(Plot):
    """Plot time series of Nd occupancy."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.Nd_occupancy, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.Nd_occupancy, df_vars.Nd_occupancy, *args, **kwargs
        )

    def plot_equilibrium(self, equil_occupancy, *args, **kwargs):
        self._ax.axhline(equil_occupancy, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$N_\text{d, occ}$")
        # self._ax.set_ylabel(r"$N_\text{d} / \ell_\text{tot}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class TotalForcePlot(Plot):
    """Plot time series of total force in pico Newtons."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.force_R_total / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_R_total / 1e-12,
            df_vars.force_R_total / 1e-24,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class dRdtPlot(Plot):
    """Plot time series of dR/dt in um/s."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.dR_dt / 1e-6, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.dR_dt / 1e-6, df_vars.dR_dt / 1e-12, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\dot{R} / \si{\micro\meter\per\second}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class EntropicForcePlot(Plot):
    """Plot time series of entropic force in pico Newtons."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.force_R_entropy / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_R_entropy / 1e-12,
            df_vars.force_R_entropy / 1e-24,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F_\text{ent} / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class CondensationForcePlot(Plot):
    """Plot time series of condensation force in pico Newtons."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.force_R_condensation / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_R_condensation / 1e-12,
            df_vars.force_R_condensation / 1e-24,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F_\text{cond} / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class SlidingForcePlot(Plot):
    """Plot time series of sliding force in pico Newtons."""

    def plot(self, df, ftype="cond", *args, **kwargs):
        if ftype == "cond":
            self._ax.plot(df.t, df.force_R_condensation / 1e-12, *args, **kwargs)
        elif ftype == "ent":
            self._ax.plot(df.t, df.force_R_entropy / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_R_entropy / 1e-12,
            df_vars.force_R_entropy / 1e-24,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F_\text{slide} / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class BendingForcePlot(Plot):
    """Plot time series of bending force in pico Newtons."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.force_R_bending / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_R_bending / 1e-12,
            df_vars.force_R_bending / 1e-24,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F_\text{bend} / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class ZetacXPlot(Plot):
    """Plot time series of cX friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_cX, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.zeta_cX, df_vars.zeta_cX, *args, **kwargs
        )

    def setup_axis(self):
        #        self._ax.set_ylabel(r"$\zeta_\text{cond} / \si{\second\per\kilo\gram}$")
        self._ax.set_ylabel(r"$\zeta / \si{\second\per\kilo\gram}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")
        self._ax.set_yscale("log")
        self._ax.minorticks_off()


class ZetaNdExpPlot(Plot):
    """Plot time series of double exponent friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_Nd_exp, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.zeta_Nd_exp, df_vars.zeta_Nd_exp, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta / \si{\second\per\kilo\gram}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")
        self._ax.set_yscale("log")
        self._ax.minorticks_off()


class ZetaNdExactPlot(Plot):
    """Plot time series of exact friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_Nd_exact, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.zeta_Nd_exact, df_vars.zeta_Nd_exact, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta / \si{\second\per\kilo\gram}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")
        self._ax.set_yscale("log")
        self._ax.minorticks_off()


class AllZetaPlot(Plot):
    """Plot time series of each type of friction coefficient"""

    def plot_comparison(self, dfs, colors, *args, **kwargs):
        self._ax.plot(dfs[2].t, dfs[2].zeta_Nd_exp, color=colors[2], *args, **kwargs)
        self._ax.plot(dfs[1].t, dfs[1].zeta_Nd_exp, color=colors[1], *args, **kwargs)
        self._ax.plot(dfs[0].t, dfs[0].zeta_cX, color=colors[0], *args, **kwargs)
        # super().plot_meanvar(
        #    dfs[2][0].t,
        #    dfs[2][0].zeta_Nd_exact,
        #    dfs[2][1].zeta_Nd_exact,
        #    color=colors[2],
        #    *args,
        #    **kwargs
        # )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta / \si{\second\per\kilo\gram}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")
        self._ax.set_yscale("log")
        self._ax.minorticks_off()


class BarrierNdPlot(Plot):
    """Plot the free energy barrier as a function of Nd for a set of k"""

    def __init__(self, f, ax):
        self._ax2 = ax.twiny()
        super().__init__(f, ax)

    def plot_comparison(self, df, ks, colors, markers, *args, **kwargs):
        for k, color in zip(ks, colors):
            cmap = plt.get_cmap("tab10")
            DF_exacts = df[(df.k == k) & (df.method == "exact")]
            DF_exps = df[(df.k == k) & (df.method == "exp")]
            DF_cXs = df[(df.k == k) & (df.method == "cX")]
            self._ax2.plot(
                DF_cXs.l,
                DF_cXs.DF,
                #                color=styles.TEXTBLACK,
                #                color=cmap(0),
                color=color,
                linestyle="",
                marker=markers[2],
                *args,
                **kwargs
            )
            self._ax.plot(
                DF_exps.Nd,
                DF_exps.DF,
                #                color=styles.TEXTBLACK,
                #                color=cmap(2),
                color=color,
                linestyle="",
                marker=markers[1],
                *args,
                **kwargs
            )
            self._ax.plot(
                DF_exacts.Nd,
                DF_exacts.DF,
                color=color,
                linestyle="",
                marker=markers[0],
                *args,
                **kwargs
            )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\beta \upDelta \mathcal{F}^\ddag$")
        self._ax.set_xlabel(r"$N_\text{d}$")

        self._ax.set_zorder(self._ax2.get_zorder() + 1)
        self._ax.set_frame_on(False)

        self._ax2.spines.top.set_visible(True)
        self._ax2.set_xlabel(r"$\ell$")


class Kramersr0NdPlot(Plot):
    """Plot the Kramer's r0 as a function of Nd for a set of k"""

    def plot(self, df, ks, colors, *args, **kwargs):
        for k, color in zip(ks, colors):
            r0 = df[df.k == k]
            self._ax.plot(r0.Nd, r0.r0 / 1000, color=color, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$r_0 / \qty{1000}{\per\second}$")
        self._ax.set_xlabel(r"$N_\text{d}$")
