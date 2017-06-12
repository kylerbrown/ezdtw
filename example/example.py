import resin
from scipy.io import wavfile
import ezdtw
rate1, song1 = wavfile.read('song1.wav')
rate2, song2 = wavfile.read('song2.wav')


# create spectrograms with resin

pxx1, freqs1, times1 = resin.sap_spectra(rate1).signal(song1).power()
pxx1 = resin.spectral_analysis.power_spectra_to_dB(pxx1, dB_thresh=50)
pxx2, freqs2, times2 = resin.sap_spectra(rate2).signal(song2).power()
pxx2 = resin.spectral_analysis.power_spectra_to_dB(pxx2, dB_thresh=50)

# compute warp path
x, y = ezdtw.dtw(pxx1.T, pxx2.T)
# plot results
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.title('warp path')
plt.savefig('warp_path.png')
plt.show()

# to get the actual cumulative distance matrix
from ezdtw.ezdtw import dtw_distance, cdist
distances = cdist(pxx1.T, pxx2.T)
cum_min_dist = dtw_distance(distances)

# plot everything
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(8,8))
ax1.pcolorfast(pxx1)
ax1.set_title('signal 1')
ax3.pcolorfast(pxx2)
ax3.set_title('signal 2')

ax2.pcolorfast(distances)
ax2.set_title('distances')
ax4.pcolorfast(cum_min_dist)
ax4.set_title('cumulative minimum distances')
f.savefig('example.png')