
.. include:: ../header.txt


YANG Library Additions
================================

The YANG Library (:rfc:`8525`) is augmented to provide class bindings
for the server implementation.

.. code-block:: yang

    augment /yanglib:yang-library {
      container classes {
        // contents TBD
      }
    }
