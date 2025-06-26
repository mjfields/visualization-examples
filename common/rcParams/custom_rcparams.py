import matplotlib.pyplot as plt

plt.style.use('default')

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'demi'

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.bf'] = 'stixgeneral:bold'
plt.rcParams['mathtext.rm'] = 'stixgeneral'
plt.rcParams['mathtext.it'] = 'stixgeneral:italic'
plt.rcParams['mathtext.bfit'] = 'stixgeneral:italic:bold'
plt.rcParams['mathtext.sf'] = 'sans' # used for stubborn symbols e.g. \star

plt.rcParams['font.cursive'] = [
    'Lucida Handwriting'
]
plt.rcParams['mathtext.cal'] = 'Lucida Handwriting'

plt.rcParams['lines.linewidth'] = 4

plt.rcParams['axes.linewidth'] = 4
plt.rcParams['axes.labelweight'] = 'demi'
plt.rcParams['axes.labelpad'] = 10.0
plt.rcParams['axes.labelsize'] = 24 
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.formatter.limits'] = [-4, 4]
plt.rcParams['axes.edgecolor'] = 'black'

plt.rcParams['hatch.linewidth'] = 3
 
plt.rcParams['xtick.labelsize'] = 22
plt.rcParams['xtick.major.size'] = 8
plt.rcParams['xtick.major.width'] = 3
plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 2

plt.rcParams['ytick.labelsize'] = 22
plt.rcParams['ytick.major.size'] = 8
plt.rcParams['ytick.major.width'] = 3
plt.rcParams['ytick.minor.size'] = 5
plt.rcParams['ytick.minor.width'] = 2

plt.rcParams['legend.fontsize'] = 22
plt.rcParams['legend.title_fontsize'] = 24
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.numpoints'] = 1
plt.rcParams['legend.framealpha'] = 0.5
plt.rcParams['legend.loc'] = 'best'

plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['figure.titleweight'] = 'demi'
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['figure.dpi'] = 300

plt.rcParams['savefig.bbox'] = 'tight'
