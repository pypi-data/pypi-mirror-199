import numpy as np
from typing import Dict, List, Callable
from matplotlib import pyplot as plt
from matplotlib.pyplot import Line2D


def integrate(
        x: np.ndarray,
        y: np.ndarray,
        c: float = 0,
        expand: bool = True,
        cumul: bool = True) -> np.ndarray:

    arr = np.cumsum((x[1:]-x[:-1])*(y[1:]+y[:-1]))/2 + c
    if expand:
        arr = np.concatenate(((c,), arr))
    if not cumul:
        return arr[-1]
    return arr


def arch_shape(x: np.ndarray, L: float, H: float, k: float) -> np.ndarray:
    y = x*(k*L-x)*4/(L*(2*k*L-L))*H
    yl = y[x <= L/2]
    return np.concatenate((yl, yl[::-1]))


def arch_derivative(x: np.ndarray, L: float, H: float, k: float) -> np.ndarray:
    d = (k*L-2*x)*4/(L*(2*k*L-L))*H
    dl = d[x <= L/2]
    return np.concatenate((dl, -dl[::-1]))


class ThreeHingedArch:

    #          v +----+----+----+----+----+
    #            |    |    |    |    |    |
    #            ▼    ▼    ▼    ▼    ▼    ▼
    #                     By ▲
    #  hl                    |                        hr
    # +->               Bx <- O -> Bx                <-+
    # |                  #     |   #                  |
    # +->             #        ▼      #             <-+
    # |             #          By       #             |
    # +->          #                     #          <-+
    # |           #                       #           |
    # +->   Ax -> O                       O <- Cx   <-+
    #             ▲                       ▲
    #             |                       |
    #             Ay                      Cy

    # Effort sign convention
    #       <-
    #    +-------+
    # <- |       | ->
    #    +-------+
    #        ->
    # Positive moment: top is compressed, bottom is in traction

    def __init__(
            self,
            L: float = 2,
            H: float = 1,
            k: float = 1,
            arch_shape_func: Callable = arch_shape,
            arch_deriv_func: Callable = arch_derivative,
            num: int = 1000,
            vertical_load: Callable = lambda x: np.zeros_like(x),
            right_load: Callable = lambda y: np.zeros_like(y),
            left_load: Callable = lambda y: np.zeros_like(y),
            surface_load: Callable = lambda x: np.zeros_like(x),
            density: float = 0,  # N/m
            g: float = 9.81,
            colors: Dict = dict(
                arch='k',
                load='r',
                force='g',
                shear='m',
                moment='b'),
            alpha: float = 0.3
    ) -> None:

        # Geometry is entirely defined from these 3 parameters
        self.L = L  # Lenght
        self.H = H  # Height
        self.k0 = k  # top angle coeficient
        self.num = num

        self.colors = colors  # Diagram & plot colors
        self.alpha = alpha  # Diagram fills transparency
        self.arch_shape_func = arch_shape_func
        self.arch_deriv_func = arch_deriv_func

        self.vertical_load = vertical_load
        self.right_load = right_load
        self.left_load = left_load
        self.surface_load = surface_load
        self.density = density
        self.g = g

        self.set_shape()
        self.set_load()
        self.calculate()

    def set_shape(self):
        # numerical shape
        self.x = np.linspace(0, self.L, num=self.num)
        self.y = self.arch_shape_func(self.x, self.L, self.H, self.k0)
        self.derivative = self.arch_deriv_func(self.x, self.L, self.H, self.k0)

        # Left side
        left = self.x <= self.L/2
        self.xl = self.x[left]
        self.yl = self.y[left]

        # Rigth side
        right = self.x > self.L/2
        self.xr = self.x[right]
        self.yr = self.y[right]

        self.left, self.right = left, right

        # direction vector
        self.dv = np.array(
            (np.ones_like(self.derivative), self.derivative)
        )/np.sqrt(1+self.derivative**2)
        self.dl = np.linalg.norm((np.ones(self.num), self.derivative), axis=0)
        # normal vector
        self.nv = np.array((-self.dv[1, :], self.dv[0, :]))
        # Attaching the essentials to the object
        self.geometry = (self.x, self.y, self.L, self.H)

    def set_load(self):

        self.dead_load = self.dl*self.density*self.g

        self.sfl = self.surface_load(self.x)
        sf = self.dl*self.sfl
        sfx, sfy = sf*np.abs(self.nv) * self.dl

        self.v = self.vertical_load(self.x) + self.dead_load + sfy
        self.vl = self.v[self.left]
        self.vr = self.v[self.right]
        self.hl = self.left_load(self.yl) + sfx[self.left]
        self.hr = self.right_load(self.yr)[::-1] + sfx[self.right]

    def calculate(self):
        values, arrays = self.calc_loads()
        reactions = self.calc_reactions(values)
        return self.calc_stresses(arrays, reactions)

    def calc_loads(self):

        # Vertical left load
        Vls = integrate(self.xl, self.vl)
        # Vertical left load's moment
        Mvls = integrate(self.xl, self.vl*self.xl)
        Vl = Vls[-1]
        Mvl = Mvls[-1]

        # Horizontal left load
        Hls = integrate(self.yl, self.hl)
        # Horizontal left load's moment
        Mhls = integrate(self.yl, self.hl*self.yl)
        Hl = Hls[-1]
        Mhl = Mhls[-1]

        # Vertical right load
        Vrs = integrate(self.xr, self.vr)
        # Vertical right load's moment
        Mvrs = integrate(self.xr, self.vr*(self.xr-self.L/2))
        Vr = Vrs[-1]
        Mvr = Mvrs[-1]

        # Horizontal right load
        Hrs = -integrate(self.yr, self.hr)
        # Horizontal right load's moment
        Mhrs = -integrate(self.yr, self.hr*(self.H - self.yr))
        Hr = Hrs[-1]
        Mhr = Mhrs[-1]

        return (
            # Load sums for the reaction's calculation
            (Vr, Mvr, Vl, Mvl,
             Hr, Mhr, Hl, Mhl),
            # Load arrays for moment and normal force distribution
            (Vrs, Mvrs, Vls, Mvls,
             Hrs, Mhrs, Hls, Mhls)
        )

    def calc_reactions(self, load_values):

        if hasattr(self, "invA"):
            # In a future version, a tkinter interface will be set up
            # This function will be called repeateadly
            # Computing an inverse matrix one for all
            return self.invA@b
        else:
            (Vr, Mvr, Vl, Mvl,
             Hr, Mhr, Hl, Mhl) = load_values

            A = np.array([
                # Ax  Ay       Bx         By         Cx         Cy
                [1,    0,      -1,         0,        0,         0],
                [0,    0,       1,         0,       -1,         0],
                [0,    1,       0,         1,        0,         0],
                [0,    0,       0,        -1,        0,         1],
                [0,    0,  self.H,  self.L/2,        0,         0],
                [0,    0,       0,         0,  -self.H,  self.L/2],
            ])
            b = np.array([
                -Hl,  # Ax - Bx =-Hl
                +Hr,  # Bx - Cx = Hr
                Vl,  # Ay + By = Vl
                Vr,  # -By + Cy = Vr
                Mvl+Mhl,  # Bx*H + By*L/2 = Mvl + Mhl
                Mvr+Mhr  # -Cx*H + Cy*L/2 = Mvr + Mhr
            ])

            if np.linalg.det(A) != 0:
                self.invA = np.linalg.inv(A)
                return self.invA@b
            else:
                return np.linalg.solve(A, b)

    def calc_stresses(self, load_arrays, reactions):

        (Vrs, Mvrs, Vls, Mvls,
         Hrs, Mhrs, Hls, Mhls) = load_arrays

        Ax, Ay, Bx, By, Cx, Cy = reactions

        Ml = (
            - (Ax+Hls)*self.yl + (Ay-Vls)*self.xl
            + Mhls + Mvls
        )
        Mr = (
            + Mvrs + Mhrs
            + (Bx-Hrs)*(self.H-self.yr) - (By+Vrs)*(self.xr-self.L/2)
        )

        self.M = np.concatenate((Ml, Mr))

        Fx = np.concatenate((Ax+Hls, Bx-Hrs))
        Fy = np.concatenate((Vls-Ay, By+Vrs))
        F = np.array([Fx, Fy])
        self.N = (F*self.dv).sum(axis=0)
        self.V = (F*self.nv).sum(axis=0)

        return self.N, self.V, self.M

    def diagram(self,
                loads_scale=1.5,
                moments_scale=1.5,
                force_scale=4,
                show=True):

        # In order to scale the moment diagram to the maximum values
        moments_scale *= np.abs(self.M).max()
        force_scale *= np.abs(self.N).max()
        loads_scale *= max(
            np.abs(load).max() for load in (self.v, self.hr, self.hl)
        )

        # Check if it is null to avoid divisions by 0
        loads_scale = 1 if loads_scale == 0 else loads_scale
        moments_scale = 1 if moments_scale == 0 else moments_scale
        force_scale = 1 if force_scale == 0 else force_scale

        plt.axis('off')
        # Arch
        plt.plot(self.x, self.y, '-k', lw=3)
        # Hinges
        plt.scatter((0, self.L/2, self.L), (0, self.H, 0), s=50,
                    facecolor='w', linewidths=2, edgecolors='k', zorder=3)

        Mx, My = self.M*self.nv/moments_scale
        moment, = plt.fill(
            np.concatenate((self.x-Mx, self.x[::-1])),  # diagram on the
            np.concatenate((self.y-My, self.y[::-1])),  # tension side
            linewidth=0.0,
            color=self.colors['moment'],
            label="Moment",
            alpha=self.alpha
        )

        Nx, Ny = self.N*self.nv/force_scale
        Vx, Vy = self.V*self.nv/force_scale

        normal, = plt.fill(
            np.concatenate((self.x+Nx, self.x[::-1])),
            np.concatenate((self.y+Ny, self.y[::-1])),
            linewidth=0.0,
            color=self.colors['force'],
            label="Normal force",
            alpha=self.alpha
        )

        shear, = plt.fill(
            np.concatenate((self.x+Vx, self.x[::-1])),
            np.concatenate((self.y+Vy, self.y[::-1])),
            linewidth=0.0,
            color=self.colors['shear'],
            label="Shear force",
            alpha=self.alpha
        )

        load = None
        if not (self.v == 0).all():
            load, = plt.fill(
                np.concatenate((self.x, self.x[::-1])),
                np.concatenate((
                    1.2*self.H + self.v/loads_scale,
                    1.2*self.H + np.zeros_like(self.v)
                )),
                # linewidth=0.0,
                color=self.colors['load'],
                hatch='|',
                label="Loads",
                alpha=self.alpha
            )
        if not (self.hl == 0).all():
            load, = plt.fill(
                np.concatenate((
                    -0.1*self.L - self.hl/loads_scale,
                    -0.1*self.L + np.zeros_like(self.hl)
                )),
                np.concatenate((
                    self.yl, self.yl[::-1]
                )),
                # linewidth=0.0,
                color=self.colors['load'],
                hatch='-',
                label="Loads",
                alpha=self.alpha
            )
        if not (self.hr == 0).all():
            load, = plt.fill(
                np.concatenate((
                    1.1*self.L + self.hr[::-1]/loads_scale,
                    1.1*self.L + np.zeros_like(self.hl)
                )),
                np.concatenate((
                    self.yl, self.yl[::-1]
                )),
                # linewidth=0.0,
                color=self.colors['load'],
                hatch='-',
                label="Loads",
                alpha=self.alpha
            )

        # Grouping labels into the axis' legend
        if load is None:
            lines = (moment, normal, shear)
            print("Warning: no loads found")
        else:
            lines = (moment, normal, shear, load)
        labs = [line.get_label() for line in lines]
        plt.legend(lines, labs)

        if show:
            plt.show()

    def plot_loads(self, show=True):

        plt.plot(self.x, self.v, label='Vertical loads')
        plt.plot(self.x, np.concatenate((self.hl, self.hr)),
                 label='Horizontal loads')
        plt.plot(self.x, self.sfl, label='Surface loads')
        plt.plot(self.x, self.dead_load, label='Dead load')

        plt.title('Applied loads')
        plt.xlabel('x position')
        plt.ylabel('Load')
        plt.legend()
        plt.show()

    def plot_stresses(self, show_loads=False, show=True):

        fig, ax1 = plt.subplots(1, sharex=True, figsize=(8, 6))
        ax2 = ax1.twinx()
        if hasattr(ax1, "axline"):
            ax1.axline((0, 0), slope=0, color=self.colors['moment'],
                       linestyle='--', lw=1.5, alpha=0.5)
            ax2.axline((0, 0), slope=0, color='k',
                       linestyle='--', lw=1, alpha=0.5)

        moment, = ax1.plot(self.x, self.M, '-', label="Moment",
                           color=self.colors['moment'], lw=2)
        normal, = ax2.plot(self.x, self.N, '-.', label="Normal force",
                           color=self.colors['force'], lw=1.5)
        shear, = ax2.plot(self.x, self.V, '-.', label="Shear force",
                          color=self.colors['shear'], lw=1.5)

        if show_loads:
            lns3, = ax2.plot(self.x, self.v, '-.',
                             color=self.colors['load'],
                             label='Vertical load', lw=1)
            lns4, = ax2.plot(self.x, np.concatenate((self.hl, self.hr)), ':',
                             color=self.colors['load'],
                             label='Horizontal load', lw=1)
            lns = (moment, normal, shear, lns3, lns4)
        else:
            lns = (moment, normal, shear)

        # Merging labels into one legend
        labs = [ln.get_label() for ln in lns]
        ax2.legend(lns, labs)
        plt.title('Internal stresses')
        ax1.set_xlabel("x position")
        ax1.set_ylabel("Moment", color=self.colors["moment"])
        ax2.set_ylabel("Forces")

        # Detail colors
        ax1.tick_params(colors=self.colors["moment"], axis="y")

        if show:
            plt.show()

        return fig, ax1, ax2


if __name__ == "__main__":

    def _horizontal_load_right(y: np.ndarray):
        return np.zeros_like(y)

    def _vertical_load(x: np.ndarray):
        return (x-x.min())/(x.max()-x.min())

    def _horizontal_load_left(y: np.ndarray):
        return np.exp(_vertical_load(y))

    def _surface_load(x: np.ndarray):
        return np.ones_like(x)

    arch = ThreeHingedArch(
        L=4,  # length
        H=3,  # height
        k=1.0,
        surface_load=_surface_load,
        # vertical_load=vertical_load,
        # right_load=horizontal_load_right,
        # left_load=horizontal_load_left
    )
    plt.style.use('bmh')
    arch.plot_loads()
    plt.style.use('default')
    arch.diagram()
    plt.style.use('bmh')
    arch.plot_stresses()
