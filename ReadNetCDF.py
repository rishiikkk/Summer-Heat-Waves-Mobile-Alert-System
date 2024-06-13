# Dump stats of a netcdf file
from netCDF4 import Dataset
import sys
import numpy as np


def ncdump(nc_fid, verb=True):
    def print_ncattr(key):
        try:
            print ('\t\ttype:', repr(nc_fid.variables[key].dtype))
            for ncattr in nc_fid.variables[key].ncattrs():
                print ('\t\t%s:' % ncattr,\
                  repr(nc_fid.variables[key].getncattr(ncattr)))
        except KeyError:
            print ('\t\tWARNING: %s does not contain variable attributes' % key)

# NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print ('NetCDF Global Attributes:')
        for nc_attr in nc_attrs:
            print ('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
# Dimension shape information.
    if verb:
        print ('NetCDF dimension information:')
        for dim in nc_dims:
            print ('\tName:', dim)
            print ('\t\tsize:', len(nc_fid.dimensions[dim]))
            print_ncattr(dim)
# Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print ('NetCDF variable information:')
        for var in nc_vars:
            if var not in nc_dims:
                print ('\tName:', var)
                print ('\t\tdimensions:', nc_fid.variables[var].dimensions)
                print ('\t\tsize:', nc_fid.variables[var].size)
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

print ("The file has the name %s" % (sys.argv[1]))

#nc_f = 'NEW_FRANCE_MEAN_ANOMALY_ts.06-07-08.nc'  # Your filename
nc_f = sys.argv[1]
nc_fid = Dataset(nc_f, 'r')  # Dataset is the class behavior to open the file
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

field = nc_fid.variables[sys.argv[2]][:]
print(field)
print(field.shape)
print(np.mean(field))
print(np.std(field))
