# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 21:38:31 2018

@author: Peter
"""

from PIL import Image; import numpy as np

chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

SC=.5
GCF=1
WCF =2
url = 'http://pbs.twimg.com/profile_images/1014154533939875840/I8tOiJCX_normal.jpg'
url = 'http://pbs.twimg.com/profile_images/705853280560226304/_GhZ8LRg_normal.jpg'
url = 'http://pbs.twimg.com/profile_images/585444733603962881/pria5Eg0_normal.jpg'

import requests
from io import BytesIO

response = requests.get(url)
img = Image.open(BytesIO(response.content))
S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
img = np.sum( np.asarray( img.resize(S) ), axis=2)
img -= img.min()
img = (1.0 - img/img.max())**GCF*(chars.size-1)

print( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )