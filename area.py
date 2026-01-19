import h5py
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

file_path = r"C:\Users\ASUS\Desktop\ISRO\NASA\oco2_L1bScND_59408a_250901_B11213r_251008220901.h5"
file = h5py.File(file_path, 'r')

lat = file["SoundingGeometry/sounding_latitude"][:].flatten()
lon = file["SoundingGeometry/sounding_longitude"][:].flatten()
rad = file["SoundingMeasurements/radiance_strong_co2"][:]

# Mean radiance for each footprint
mean_rad = rad.mean(axis=2).flatten()

# ============================
# FIX BREAKING STRIP
# ============================
lon_unwrapped = np.unwrap(np.radians(lon))
lon_unwrapped = np.degrees(lon_unwrapped)

plt.figure(figsize=(14, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

ax.set_global()
ax.gridlines(draw_labels=True)

scatter = ax.scatter(
    lon_unwrapped,
    lat,
    c=mean_rad,
    cmap="inferno",
    s=8,
    transform=ccrs.PlateCarree()
)

cbar = plt.colorbar(scatter, ax=ax, shrink=0.5)
cbar.set_label("Mean CO₂ Radiance")

plt.title("OCO-2 CO₂ Radiance Strip (Unwrapped, No Breaks)")
plt.show()
