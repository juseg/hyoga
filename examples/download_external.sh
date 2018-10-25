# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

# Retrieve external data
# ----------------------

# create and move to data directory
mkdir -p external
cd external

# download CleanTOPO (full version) worldwide elevation data
wget -nc http://naciscdn.org/data/cleantopo/Full.zip
unzip -jn Full.zip Full/CleanTOPO2.{tif,tfw}

# download Hokkaido SRTM land topographic data
if [ ! -f srtm_hokkaido.tif ]
then

    # download SRTM data
    serv="http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff"
    for tile in srtm_{64_04,65_03,65_04,66_04}
    do
        wget -nc $serv/$tile.zip
        unzip -n $tile.zip $tile.{hdr,tfw,tif}
    done

    # build virtual patch
    gdalbuildvrt srtm.vrt srtm_??_??.tif

fi
