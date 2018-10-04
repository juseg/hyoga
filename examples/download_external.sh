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
