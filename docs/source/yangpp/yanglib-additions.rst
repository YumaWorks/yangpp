
.. include:: ../header.txt


YANG Library Additions
================================

The YANG Library (:rfc:`8525`) is augmented to provide class bindings
for the server implementation.


.. code-block:: text

    module: yangpp-classmap

      augment /yanglib:yang-library:
        +--ro yangpp
           +--ro classmap* [specified-module specified-class]
              +--ro specified-module      yang:yang-identifier
              +--ro specified-class       yang:yang-identifier
              +--ro implemented-module    yang:yang-identifier
              +--ro implemented-class     yang:yang-identifier


The module 'yangpp-classmap' defines a data structure
to identify a mapping beterrn a specified class ID and
an implemented class ID.


.. literalinclude:: ../../../modules/yangpp-classmap.yang
    :language: yang
