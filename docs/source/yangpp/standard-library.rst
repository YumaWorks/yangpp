
.. include:: ../header.txt


YANG++ Standard Library
========================

The YANG++ standard library is a set of conceptual APIs that can be implemented
in tools.  There are also an XPath library function defined for each API.

Compare Classes
-----------------

The 'compare' API allows two :ref:`class instances` to be compared.

-  Only the naming information is compared
-  Other child nodes of the class root are ignored for this API

**Conceptual API**

.. code-block:: yang

    rpc compare {
      input {
        leaf class1-path {
          type string;  // path to class instance
          mandatory true;
        }
        leaf class2-path {
          type string;  // path to class instance
          mandatory true;
        }
      }
      output {
        leaf result {
          type enumeration {
            enum less {
              value -1;
              description "class1 is sorted before class2.";
            }
            enum equal {
              value 0;
              description "class1 sorting is equal to class2.";
            }
            enum more {
              value 1;
              description "class1 is sorted after class2.";
            }
          }
        }
      }

**XPath API**

.. code-block:: text

    Function: number compare (node-set, node-set)

Requirements:

-   This function compares the class identifier for the first
    node-set to the second node-set.

-   Each node-set is expected to represent an instance of the same class.

-   If the class is based on a container then the value 0 is always returned.

-   If the class is based on a list with an empty key-stmt, then the value
    0 is always returned.

-   If the class is based on a user-ordered list, then the behavior is not defined

-   If the class is based on any other list then the key leafs must match

-   All classes must support canonical identifier name representations.

-   All compare operations are done on the canonical key value representations.

-   All classes should support a canonical order.

-   The actual canonical order may be implementation dependent, as allowed by YANG 1.1
    for system-ordered lists.


Return Value:

-  The value -1 is returned if the first node-set is ordered before the second node-set.

-  The value 0 is returned if the first node-set order is equal to the second node-set.

-  The value 1 is returned if the first node-set is ordered after the second node-set.
