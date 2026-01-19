import h5py
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

file_path = r"C:\Users\ASUS\Desktop\ISRO\NASA\oco2_L1bScND_59408a_250901_B11213r_251008220901.h5"
file_path1 = r"C:\Users\ASUS\Desktop\ISRO\NASA\oco2_LtCO2_250901_B11211Ar_251028215532s.nc4"

file = h5py.File(file_path,"r")
file2 = h5py.File(file_path1,"r")

lat_l1b = file['SoundingGeometry/sounding_latitude'][:].flatten()
lon_l1b = file["SoundingGeometry/sounding_longitude"][:].flatten()

lat_l2 = file2['latitude'][:]
lon_l2 = file2['longitude'][:]
xco2   = file2['xco2'][:]



strip_xco2 = []

for la, lo in zip(lat_l1b, lon_l1b):
    dist = (la - lat_l2)**2 + (lo - lon_l2)**2
    idx = np.argmin(dist)
    strip_xco2.append(xco2[idx])

strip_xco2 = np.array(strip_xco2)



lat_min, lat_max = -70, -50       
lon_min, lon_max = -80, -60     

mask = (
    (lat_l1b >= lat_min) & (lat_l1b <= lat_max) &
    (lon_l1b >= lon_min) & (lon_l1b <= lon_max)
)

region_ppm = strip_xco2[mask]

print("Number of points in region:", region_ppm.size)
print("Mean CO₂ (ppm):", region_ppm.mean() if region_ppm.size>0 else "No data")
print("Max CO₂:", region_ppm.max() if region_ppm.size>0 else "No data")
print("Min CO₂:", region_ppm.min() if region_ppm.size>0 else "No data")



plt.figure(figsize=(14, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

ax.set_global()
ax.gridlines(draw_labels=True)

scatter = ax.scatter(
    lon_l1b,
    lat_l1b,
    c=strip_xco2,
    cmap="inferno",
    s=8,
    transform=ccrs.PlateCarree()
)

cbar = plt.colorbar(scatter, ax=ax, shrink=0.5)
cbar.set_label("CO₂ (ppm)")

plt.title("OCO-2 CO₂ PPM Strip (Matched to Radiance Footprints)")
plt.show()
