Observation framework
=====================

Owlready2 provides an observation framework in the owlready2.observe module. It allows adding listeners to any entity
of an ontology, in order to be notified when the entity is modified.


Adding and removing listeners
-----------------------------

Let us create a (very) small ontology:

::
   
   >>> onto = get_ontology("http://test.org/test.owl")
   >>> with onto:
   ...   class Pizza(Thing): pass
   ...   class price(Thing >> float): pass
   ...   pizza = Pizza()

And then import the observe module and add a listener to pizza:

::

   >>> from owlready2.observe import *
   >>> def listener(entity, props):
   ...     print("Listener:", entity, props)
   >>> observe(pizza, listener)

The observe() function is used to add a listener to an entity.
   
Whenever relation are added or removed to the entity, listener is called:

::

   >>> pizza.price = [11.0]
   Listener: 305 [304]

The listener receives two arguments: the entity and a list of properties (NB unless you coalesce event as explained below,
the list includes a single value). For performance purpose, Observe uses "store-IDs" as argument for the entity
and the properties, and not Python objects (hence you see integer values above). Here, 305 is the "store-ID" of the pizza
entity and 304 the "store-ID" of the price property (NB the number may differ).

You may convert store-IDs to Python objects with World._get_by_storid(storid).
Here is a modified listener that shows entity and property objects instead of store-IDs:

::

   >>> def listener(entity, props):
   ...     entity =   default_world._get_by_storid(entity)
   ...     props  = [ default_world._get_by_storid(prop) for prop in props ]
   ...     print("Listener:", entity, props)
   
   >>> unobserve(pizza) # Remove previous listener
   >>> observe(pizza, listener)
   
   >>> pizza.price = [11.0]
   Listener: onto.pizza [onto.price]

The unobserve() function is used to remove a listener from an entity (if no listener is given, all listeners are removed).



Coalescing events
-----------------

The coalesced_observations environment can be used to coalesce events and listener calls.

For instance, the following code generates 3 calls to the listener:

::

   >>> pizza.price.append(12.0)
   Listener: onto.pizza [onto.price]
   >>> pizza.label = ["Pizz", "Test pizza"]
   Listener: onto.pizza [rdf-schema.label]
   Listener: onto.pizza [rdf-schema.label]

Since two labels are added, there are 2 calls for the set label operation.
These multiple calls can be problematic if the listener has a performance cost (e.g. updating the user interface).

Multiple calls can be coalesced and merged using the coalesced_observations environment, as follows:

::

   >>> with coalesced_observations:
   ...     pizza.price.append(13.0)
   ...     pizza.label = ["Pizz2", "Test pizza2"]
   Listener: onto.pizza [onto.price, rdf-schema.label]

No call to listeners are emitted inside the "with coalesced_observations" block, and a single call is emitted at the end,
possibly with more than one property.

In addition, you can add/remove general listener to coalesced_observations, with the add_listener() and remove_listener()
methods. The general listener is called without argument, whenever a change is done in the quadstore.


Stopping observation
--------------------

Using the observation framework may have a performance cost. After using it, if you no longer need it,
you should stop it by calling stop_observing(), as follows:

::
   
   >>> stop_observing(default_world)

