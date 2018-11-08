headers="GPS Week,GPS TOW [s],Pos Mode,Hdg Mode,SVs Tracked,SVs Used,UTC Date,UTC Time,Lat [deg],Lon [deg],Alt Ellips [m],SOG [m/s],COG [deg],Hdg [deg],Vert Vel [m/s],PDOP,HDOP,EHPE [m],EVPE [m],Baseline [m],Corr. Age [s],Delta TOW [ms],2D Delta Pos [m],3D Delta Pos [m]"
outfile='out.csv'


ref_wk_column       = 0    # REF file is created by sbp2report or nv2report
ref_tow_column      = 1
ref_fix_mode_column = 2
ref_lat_column      = 8
ref_lon_column      = 9
ref_alt_column      = 10
ref_sog_column      = 11
ref_hdg_column      = 13

# scneario time
wn = 2007
tow_start = 185000
tow_end = 186800

#Leiths house
lat = [-35, 21, 38.91844] 
lon = [149, 12, 25.74240]
alt_m = 638.728

def deg2deg(deg_list):
    out  = abs(deg_list[0]) + deg_list[1]/60.0 + deg_list[2]/3600
    if deg_list[0] < 0:
        out = -out
    return out

lat = deg2deg(lat)
lon = deg2deg(lon)


def create_row(tow, wn, position):
    row =  ['']*24
    row[ref_wk_column] = str(wn)
    row[ref_tow_column] = str(tow)
    row[ref_fix_mode_column] = str('1')
    row[ref_lat_column] = "{0:.10f}".format(position[0])
    row[ref_lon_column] = "{0:.10f}".format(position[1])
    row[ref_alt_column] = "{0:.4f}".format(position[2])
    row[ref_sog_column] = "0"
    return row

with open(outfile, 'w') as f:
    f.write(headers + "\n")
    for tow in range(tow_start*1000,tow_end*1000, 100):
        f.write(",".join(create_row(tow/1000.0, wn, [lat, lon, alt_m])))
        f.write("\n")
        print tow
    

