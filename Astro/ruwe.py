# Script created with chatGPT (https://chatgpt.com/) 
# with the following prompt (Julien Girard 2024):
"""
python code to return gaia DR3 ruwe for a star resolved by SIMBAD in a commande line script 
"""
# only one missing line:  from astropy.coordinates import SkyCoord
# Usage
# make sure you have installed: pip install astropy astroquery
"""
python gaia_ruwe.py "Sirius"
"""
# it works!

import sys
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import astropy.units as u

def get_star_coordinates(star_name):
    """
    Get the coordinates of a star from SIMBAD.

    Parameters:
    star_name : str : Name of the star

    Returns:
    tuple : Right Ascension and Declination in degrees
    """
    custom_simbad = Simbad()
    custom_simbad.TIMEOUT = 500  # Increase timeout if necessary

    # Query SIMBAD for the star
    result = custom_simbad.query_object(star_name)
    
    if result is None:
        raise ValueError(f"Star '{star_name}' not found in SIMBAD.")
    
    # Extract RA and Dec
    ra = result['RA'].data[0]
    dec = result['DEC'].data[0]
    
    return ra, dec

def get_ruwe(ra, dec):
    """
    Query Gaia DR3 for the RUWE of a star based on its coordinates.

    Parameters:
    ra : str : Right Ascension
    dec : str : Declination

    Returns:
    float : RUWE value
    """
    # Convert RA and Dec to degrees
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg), frame='icrs')
    
    # Query Gaia DR3
    query = f"""
    SELECT TOP 1 ruwe
    FROM gaiaedr3.gaia_source
    WHERE 1=CONTAINS(POINT('ICRS', {coord.ra.deg}, {coord.dec.deg}),
    CIRCLE('ICRS', gaia_source.ra, gaia_source.dec, 0.001))
    """
    
    job = Gaia.launch_job(query)
    result = job.get_results()

    if len(result) == 0:
        raise ValueError("RUWE not found for the specified coordinates.")
    
    return result['ruwe'][0]

# Main function to handle command line arguments
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gaia_ruwe.py <star_name>")
        sys.exit(1)

    star_name = sys.argv[1]

    try:
        ra, dec = get_star_coordinates(star_name)
        ruwe = get_ruwe(ra, dec)
        print(f"The RUWE for {star_name} is: {ruwe:.2f}")
    except ValueError as e:
        print(e)
