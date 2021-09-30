# Plots interim (pre-production) simulation results
# PLOT ENERGY
set terminal png enhanced font "STIXGeneral,16" size 800,800
set format y "%.2tE%S"
set offsets graph 0.001, graph 0.001, graph 0.05, graph 0.05
set autoscale

set output "interim_md.energy.png"
set xlabel "Time (ps)"
set ylabel "Energy (kcal mol^{-1})"
plot "summary.EPTOT" w l, "summary.EKTOT" w l, "summary.ETOT" w l

# PLOT TEMPERATURE
set output "interim_md.temp.png"
set xlabel "Time (ps)"
set ylabel "Temperature (K)"
plot "summary.TEMP" w l 

# PLOT PRESSURE
set output "interim_md.pres.png"
set xlabel "Time (ps)"
set ylabel "Pressure (kcal mol^{-1} Angstrom^{-2})"
plot "summary.PRES" w l 

# PLOT VOLUME
set output "interim_md.volume.png"
set xlabel "Time (ps)"
set ylabel "Volume (Angstrom^{3})"
plot "summary.VOLUME" w l 

# PLOT DENSITY
set output "interim_md.density.png"
set xlabel "Time (ps)"
set ylabel "Density (kg m^{-3})"
plot "summary.DENSITY" w l 