# Histogram výroků
#
# generováno programem gnuplot
#
set term png
set terminal png size 2000,1000
set output "histogram_vyroku.png"
set style data histograms
set style histogram rowstacked
set boxwidth 1 relative
set style fill solid 1.0 border -1
set datafile separator ","
set xtics rotate
set key outside
set yrange[0:100]
set ylabel "% výroků"
set xlabel "jména s 15 a více výroky"
set title "Rozdělení výroků podle statistik Demagog.cz (".strftime("%F", time(0)).")"
plot "stats/stats.csv" using (100.*$3/($3+$4+$5+$6)):xtic(1) linecolor rgb "#22ab55" t "pravda", \
'' using (100.*$4/($3+$4+$5+$6)):xtic(1) linecolor rgb "#ec4f2f" t "nepravda", \
'' using (100.*$5/($3+$4+$5+$6)):xtic(1) linecolor rgb "#ec912f" t "zavádějící", \
'' using (100.*$6/($3+$4+$5+$6)):xtic(1) linecolor rgb "#227594" t "neověřitelné"

