# Script created with chatGPT (https://chatgpt.com/) 
# with the following prompt (Julien Girard 2024):
"""
python code using astropy coordinates.SkyCoord to return the separation between two stars whose name is resolved by simbad. 
Please return the separation in degrees, arcminutes, minutes arcseconds. 
Please make a command line script "python separation_simbad.py star1 star2" 
"""
# Usage
# make sure you have installed: pip install astropy astroquery
"""
python separation_simbad.py "Sirius" "Betelgeuse"
"""
# it works!

import sys
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
import astropy.units as u

def get_star_coordinates(star_name):
    """
    Get the coordinates of a star from SIMBAD.

    Parameters:
    star_name : str : Name of the star

    Returns:
    SkyCoord : Coordinates of the star
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
    
    # Create a SkyCoord object
    return SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg), frame='icrs')

def calculate_separation(star1_name, star2_name):
    """
    Calculate the angular separation between two stars given their names.

    Parameters:
    star1_name : str : Name of the first star
    star2_name : str : Name of the second star

    Returns:
    tuple : Angular separation in degrees, arcminutes, arcseconds
    """
    # Get coordinates of both stars
    star1 = get_star_coordinates(star1_name)
    star2 = get_star_coordinates(star2_name)

    # Calculate the separation in degrees
    separation = star1.separation(star2).degree

    # Convert to degrees, arcminutes, and arcseconds
    degrees = int(separation)
    arcminutes = int((separation - degrees) * 60)
    arcseconds = (separation - degrees - arcminutes / 60) * 3600

    return degrees, arcminutes, arcseconds

# Main function to handle command line arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python separation_simbad.py <star1> <star2>")
        sys.exit(1)

    star1_name = sys.argv[1]
    star2_name = sys.argv[2]

    try:
        degrees, arcminutes, arcseconds = calculate_separation(star1_name, star2_name)
        print(f"The angular separation between {star1_name} and {star2_name} is:")
        print(f"{degrees}° {arcminutes}' {arcseconds:.2f}''")
    except ValueError as e:
        print(e)
