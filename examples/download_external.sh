# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

# Retrieve external data
# ----------------------

# create and move to data directory
mkdir -p external
cd external

# prepare CleanTOPO2 (full version) worldwide elevation data
if [ ! -f cleantopo2.tif ]
then

    # download CleanTOPO2 data
    wget -nc http://naciscdn.org/data/cleantopo/Full.zip
    unzip -jn Full.zip Full/CleanTOPO2.{tif,tfw}

    # reproject for Hokkaido
    gdalwarp -r cubic -s_srs "+proj=longlat" -t_srs "+proj=utm +zone=54" \
         -te 250000 4500000 1050000 5100000 -tr 5000 5000 \
         CleanTOPO2.tif cleantopo2.tif

fi

# prepare SRTM land topographic data
if [ ! -f srtm.tif ]
then

    # download SRTM data
    serv="http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff"
    for tile in srtm_{64_04,65_03,65_04,66_04}
    do
        wget -nc $serv/$tile.zip
        unzip -n $tile.zip $tile.{hdr,tfw,tif}
    done

    ## fix offset in cleantopo2
    #gdal_translate -a_offset "-10701" -ot Int16 cleantopo2{,.tmp1}.tif
    #gdal_translate -unscale cleantopo2{.tmp1,.tmp2}.tif
    #rm cleantopo2{.tmp1,.tmp2}.tif

    # patch and reproject for Hokkaido
    gdalwarp -r cubic -s_srs "+proj=longlat" -t_srs "+proj=utm +zone=54" \
             -te 250000 4500000 1050000 5100000 -tr 500 500 \
             srtm_??_??.tif srtm.tif

fi
