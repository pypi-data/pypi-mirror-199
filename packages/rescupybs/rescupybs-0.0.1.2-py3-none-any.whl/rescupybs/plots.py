import numpy as np
import matplotlib.pyplot as plt

def Nispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) == 0:
        color = ['r']
    plt.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc=location)
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Mnispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth):
    plt.figure(figsize=figsize)
    nbands = eigenvalues.shape[-1]
    for i in range(nbands):
        if np.min(eigenvalues[0,:,i]) > -0.03:
            CBM=i
            VBM = CBM-1
            break
    fig = plt.plot(eigenvalues[0], linewidth=linewidth[0], linestyle=linestyle[0])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend([fig[VBM-5], fig[VBM-4], fig[VBM-3], fig[VBM-2], fig[VBM-1], fig[VBM], fig[CBM], fig[CBM+1], fig[CBM+2], fig[CBM+3]], [VBM-5, VBM-4, VBM-3, VBM-2, VBM-1, VBM, CBM, CBM+1, CBM+2, CBM+3], frameon=False, prop={'size':'medium'}, loc='center right')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Ispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) == 0:
        color = ['r', 'k']
    elif len(color) == 1:
        color = [color[0], 'k']

    if len(linestyle) == 1:
        linestyle = [linestyle[0], '-.']

    if len(linewidth) == 1:
        linewidth = [linewidth[0], 0.8]
    p_up = plt.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    p_do = plt.plot(eigenvalues[1], color=color[1], linewidth=linewidth[1], linestyle=linestyle[1])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Dispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) == 0:
        color = ['r', 'k']
    elif len(color) == 1:
        color = [color[0], 'k']

    if len(linestyle) == 1:
        linestyle = [linestyle[0], '-.']

    if len(linewidth) == 1:
        linewidth = [linewidth[0], 0.8]
    ax1.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    ax2.plot(eigenvalues[1], color=color[1], linewidth=linewidth[1], linestyle=linestyle[1])
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.set_yticklabels([])
    ax1.set_xlim(chpts[0],chpts[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(chpts[0],chpts[-1])
    ax2.set_ylim(vertical)
    ax1.set_ylabel('Energy (eV)')
    ax1.set_xticks(chpts,labels[:-1]+[''])
    ax2.set_xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
            ax2.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Mispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(linestyle) == 1:
        linestyle = [linestyle[0], linestyle[0]]
    if len(linewidth) == 1:
        linewidth = [linewidth[0], linewidth[0]]
    nbands = eigenvalues.shape[-1]
    for i in range(nbands):
        if np.min(eigenvalues[0,:,i]) > -0.03:
            CBM_up = i
            VBM_up = CBM_up - 1
            break
    for i in range(nbands):
        if np.min(eigenvalues[0,:,i]) > -0.03:
            CBM_do = i
            VBM_do = CBM_do - 1
            break
    p_up = ax1.plot(eigenvalues[0], linewidth=linewidth[0], linestyle=linestyle[0])
    p_do = ax2.plot(eigenvalues[1], linewidth=linewidth[1], linestyle=linestyle[1])
    ax1.legend([p_up[VBM_up-5], p_up[VBM_up-4], p_up[VBM_up-3], p_up[VBM_up-2], p_up[VBM_up-1], p_up[VBM_up], p_up[CBM_up], p_up[CBM_up+1], p_up[CBM_up+2], p_up[CBM_up+3]], [VBM_up-5, VBM_up-4, VBM_up-3, VBM_up-2, VBM_up-1, VBM_up, CBM_up, CBM_up+1, CBM_up+2, CBM_up+3], frameon=False, prop={'size':'medium'}, alignment='left', title="up", title_fontproperties={'style':'italic', 'size':'medium'}, loc='center right')
    ax2.legend([p_do[VBM_do-5], p_do[VBM_do-4], p_do[VBM_do-3], p_do[VBM_do-2], p_do[VBM_do-1], p_do[VBM_do], p_do[CBM_do], p_do[CBM_do+1], p_do[CBM_do+2], p_do[CBM_do+3]], [VBM_do-5, VBM_do-4, VBM_do-3, VBM_do-2, VBM_do-1, VBM_do, CBM_do, CBM_do+1, CBM_do+2, CBM_do+3], frameon=False, prop={'size':'medium'}, alignment='left', title="down", title_fontproperties={'style':'italic', 'size':'medium'}, loc='center right')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.set_yticklabels([])
    ax1.set_xlim(chpts[0],chpts[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(chpts[0],chpts[-1])
    ax2.set_ylim(vertical)
    ax1.set_ylabel('Energy (eV)')
    ax1.set_xticks(chpts,labels[:-1]+[''])
    ax2.set_xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
            ax2.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')
