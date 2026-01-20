import h5py
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# -------------------------
# LOAD L1 FILE
# -------------------------
file_path = r"C:\Users\ASUS\Desktop\ISRO\NASA\oco2_L1bScGL_60284a_251031_B11213r_251112171102.h5"
file = h5py.File(file_path, 'r')

lat = file["SoundingGeometry/sounding_latitude"][:].flatten()
lon = file["SoundingGeometry/sounding_longitude"][:].flatten()
rad = file["SoundingMeasurements/radiance_strong_co2"][:]


mean_rad = rad.mean(axis=2).flatten()


file_path1 = r"C:\Users\ASUS\Desktop\ISRO\NASA\oco2_L2StdGL_60284a_251031_B11213r_251125212755.h5"
file2 = h5py.File(file_path1, 'r')

lat_l2 = file2["RetrievalGeometry/retrieval_latitude"][:]
lon_l2 = file2["RetrievalGeometry/retrieval_longitude"][:]
xco2   = file2["RetrievalResults/xco2"][:]


plt.figure(figsize=(14, 10))
ax = plt.axes(projection=ccrs.PlateCarree())


ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

ax.set_global()
ax.gridlines(draw_labels=True)


plt.scatter(lon, lat, c=mean_rad, s=5, cmap="viridis", alpha=0.5)

plt.scatter(lon_l2, lat_l2, c=xco2, s=12, cmap="jet", edgecolor="black")

plt.title("OCO-2 L1 Radiance + L2 XCO₂ Overlay")
plt.colorbar(label="Radiance / XCO₂")

plt.show()
