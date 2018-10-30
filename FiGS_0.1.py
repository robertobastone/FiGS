################ FiGS v 0.1



#author: Roberto Bastone
#mail : robertobastone93@gmail.com

####################################PACKAGES##################################
# system
import sys
import os
import readline
# math
import numpy as np
import math 
# plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
# coordinates
import astropy
from astropy.io import fits
from astropy.wcs import WCS
# units
from astropy import units as u
# cosmology
from astropy.cosmology import Planck15 as cosmo


####################################CHECKING VERSIONS OF PACKAGE

def checkPACKAGE(package, FiGS_Version):
    if package.__version__ < FiGS_Version:
        print ">The required version for " + str(package.__name__) + " is " + str(FiGS_Version)
        print ">Yours is " + str(package.__version__) + "\n"
        sys.exit()

checkPACKAGE(np, "1.15.0")
checkPACKAGE(mpl, "2.2.3")
checkPACKAGE(astropy, "1.1.2")


#################################### OPEN FITS #############################

readline.parse_and_bind('tab: complete') 
readline.set_completer_delims(' ')

filename = raw_input(">Input your FITS file (do not forget to include the extension!) \n")
while os.path.isfile(filename) != True:	
    print ">The file does not exist."
    filename= raw_input(">Retry \n")
		
#filename = user_input #'hst_08301_41_wfpc2_f606w_wf_drz.fits'

alpha = 1e-2
beta  = 5.5e-3
gamma = 2.5e-2

z = float(raw_input(">Input the redshift of the object in the fits\n"))

################################### FUNCTIONS
# these functions convert from angular dimensions to linear dimensions given the redshift
def fromKPCtoRadius(k,redshift):
    return (k/(cosmo.kpc_proper_per_arcmin(redshift))).to(u.degree)

def fromANGtoKPC(q,redshift):
    return q*(cosmo.kpc_proper_per_arcmin(redshift))

hdu = fits.open(filename)[1]
data = hdu.data

wcs = WCS(hdu.header)


yes = {'Y','y'}
no = {'N','n'}

while True:
    choice = raw_input(">Do you want to crop the fits? [y/n]").lower()
    if choice in yes:
        print">Okay, let us crop."
        datax_min = int(raw_input(">Choose x min: "))
        datax_max = int(raw_input(">Choose x max: "))
        datay_min = int(raw_input(">Choose y min: "))
        datay_max = int(raw_input(">Choose y max: "))
        wcs = wcs[datay_min:datay_max, datax_min:datax_max]
        data = data[datay_min:datay_max, datax_min:datax_max]
        break
    elif choice in no:
        print">Okay, let us continue"
        break
    else:
        print("please select (y/n) only")
        continue

####################################PLOTTING##################################

print">Choose size of the plot (inches)."
width = int(raw_input("Width: "))
height = int(raw_input("Height: "))
fig = plt.figure( figsize=(width,height))

ax = plt.subplot(projection=wcs)

suptitle = raw_input("Choose Title: ")
plt.suptitle(suptitle, fontsize=25)

ax.imshow(data, norm=LogNorm(.01,.5), origin='lower',cmap='Blues')


colour='black'

ax.set_ylabel(r'$\delta$ (' + str(u.deg) + ')')
ax.set_xlabel(r'$\alpha$ (' + str(u.deg) + ')')

ax.grid(color=colour, ls='dashed',zorder=5)
overlay = ax.get_coords_overlay('fk5')
overlay[0].set_axislabel('Right Ascension (J2000)')
overlay[1].set_axislabel('Declination (J2000)')
plt.legend(loc='upper right')
fig.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.show()
