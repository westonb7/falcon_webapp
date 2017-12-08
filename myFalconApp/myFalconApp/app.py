import falcon

## Carts aren't necessary for the functionality of this app,
##  I used them while testing things in the Falcon tutorial.

from .weights import Resource
## from .carts import Resource_c 

api = application = falcon.API()

weights = Resource()
## carts = Resource_c()
api.add_route('/weights', weights)
## api.add_route('/carts', carts)
