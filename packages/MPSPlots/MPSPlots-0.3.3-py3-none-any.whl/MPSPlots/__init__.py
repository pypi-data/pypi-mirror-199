from MPSPlots.tools.directories import style_directory
import matplotlib.pyplot as plt


def use_new_age_style():
    plt.style.use(style_directory.joinpath('new_age.mplstyle'))


def use_ggplot_style():
    plt.style.use('ggplot')


def use_default_style():
    plt.style.use('default')

# -
