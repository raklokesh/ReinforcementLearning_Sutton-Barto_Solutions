import numpy as np

alfa = 0.1

VA = 0
VB = 0

# TD method batch updating
converged = False
while not converged:
    Old_VA = VA
    Old_VB = VB

    # These increment updates include sum of increments from all visits to the states using TD algorithm. Worked this out by hand.
    VA = VA + alfa *(VB-VA)
    VB = VB + alfa * (6 - 8*VB)
    if abs(np.sum(VA - Old_VA + VB - Old_VB))<10**-3:
        converged = True

print('TD method state values: State A = {} State B = {}'.format(VA,VB))

VA = 0
VB = 0
# MC method batch updating
converged = False
while not converged:
    Old_VA = VA
    Old_VB = VB

    # These increment updates include sum of increments from all visits to the states using MC algorithm. Worked this out by hand.
    VA = VA + alfa *(-VA)
    VB = VB + alfa * (6 - 8*VB)
    if abs(np.sum(VA - Old_VA + VB - Old_VB))<10**-3:
        converged = True

print('MC method state values: State A = {} State B = {}'.format(VA,VB))

