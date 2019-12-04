
# coding: utf-8

# ## Python wrapper library for libgeohash
# 
# https://github.com/simplegeo/libgeohash

# In[1]:


import ctypes


# In[10]:


# compile .so with: gcc -fPIC -shared -o geohash.so geohash.c

_geohash = ctypes.CDLL('./geohash_macos.so')


# In[3]:


# convenience function for wrapping c functions

def wrap_function(lib, funcname, restype, argtypes):
    """Simplify wrapping ctypes functions"""
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


# ### Define classes to represent structs used in the c api

# In[4]:


class GeoBoxDimension(ctypes.Structure):
    _fields_ = [('height', ctypes.c_double), ('width', ctypes.c_double)]

    def __repr__(self):
        return '({0}, {1})'.format(self.height, self.width)
    
    
class GeoCoord(ctypes.Structure):
    _fields_ = [('latitude', ctypes.c_double), ('longitude', ctypes.c_double), ('north', ctypes.c_double), 
                ('east', ctypes.c_double), ('south', ctypes.c_double), ('west', ctypes.c_double), 
                ('dimension', GeoBoxDimension)]

    def __repr__(self):
        return '({0}, {1})'.format(self.latitude, self.longitude)


# ### Wrap the c api in python functions

# In[5]:


geohash_encode = wrap_function(
    _geohash, 
    'geohash_encode', 
    ctypes.c_char_p, 
    (ctypes.c_double, ctypes.c_double, ctypes.c_int)
)


geohash_decode = wrap_function(
    _geohash,
    'geohash_decode',
    GeoCoord,
    [ctypes.c_char_p]
)


geohash_neighbors = wrap_function(
    _geohash,
    'geohash_neighbors',
    ctypes.POINTER(ctypes.c_char_p),
    [ctypes.c_char_p]
)


geohash_dimensions_for_precision = wrap_function(
    _geohash, 
    'geohash_dimensions_for_precision', 
    GeoBoxDimension, 
    [ctypes.c_int]
)


# ### exercise the api

# In[6]:


geohash_encode(41.41845703125, 2.17529296875, 5)


# In[7]:


geohash_decode(b'sp3e9')


# In[8]:


a = geohash_neighbors(b'sp3e9')
[a[i] for i in range(0,8)] # there are 8 neighbors


# In[9]:


geohash_dimensions_for_precision(6)

