
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import z2pack

# Creating the System. Note that the SCF charge file does not need to be
# copied, but instead can be referenced in the .files file.
# The k-points input is appended to the .in file
# The command (mpirun ...) will have to be replaced to match your system.
system = z2pack.fp.System(
    input_files=[
        "scf_vasp/CHGCAR",
        "input/INCAR",
        "input/POSCAR",
        "input/POTCAR",
        "input/wannier90.win"
    ],                              # Step 1
    kpt_fct=z2pack.fp.kpoint.vasp,  # Step 2
    kpt_path="KPOINTS",             # Step 2
    command="mpirun /public/software/apps/vasp/vasp.6.4.1-wannier/bin/vasp_ncl >& log",  # Step 3
    mmn_path='wannier90.mmn'        # Step 4 (this is the default setting)
)

if not os.path.exists('./results'):
    os.mkdir('./results')
if not os.path.exists('./plots'):
    os.mkdir('./plots')

# Running the WCC calculation - standard settings
result_0 = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [s, t, 0],
    save_file='./results/res_0.p',
    load=True
)
result_1 = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [s, t, 0.5],
    save_file='./results/res_1.p',
    load=True
)

# Plotting WCC evolution
#fig, ax = plt.subplots(1, 1, sharey=True, figsize=(9, 5))
fig, ax = plt.subplots(figsize=(5.0,4.5))
z2pack.plot.chern(result_0, axis=ax)
#z2pack.plot.chern(result_1, axis=ax[1])

ax.set_xticks([0, 0.5, 1])
ax.set_yticks([0, 0.5, 1])
ax.set_xticklabels(["0","$\pi$", "2$\pi$"], size=16)
ax.set_yticklabels(["0", "0.5", "1.0"], size=16)
ax.set_xlabel('ky', fontsize=18)
ax.set_ylabel('Sum of WCC', fontsize=18)
plt.savefig('plots/chern1.pdf', bbox_inches='tight')

print(
    'Chern topological invariant at kz = 0: {0}'.format(
        z2pack.invariant.chern(result_0)
    )
)
#print(
#    'Chern topological invariant at kz = 0.5: {0}'.format(
#        z2pack.invariant.chern(result_1)
#    )
#)
