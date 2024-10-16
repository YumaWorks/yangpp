
.. include:: ../header.txt


YANG 1.1 Translation
================================

The intermediate or final expansion of YANG++ language constructs
can be converted to an equivalent set of YANG 1.1 modules.
Constructs that do not exist in YANG 1.1 can be omitted or
converted to YANG extensions.

Converting Base Class Types
----------------------------

Each base type can be converted to some sort of YANG 1.1 construct

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * -  class type
     -  YANG 1.1 construct

   * -  :ref:`root base-class`
     -  'anydata' or 'container' with description-stmt declaring purpose

   * -  :ref:`object base-class`
     -  'data-def' statement

   * -  :ref:`message base-class`
     -  'sx:structure' statement with description-stmt declaring purpose

   * -  :ref:`structure base-class`
     -  'sx:structure' statement


Converting Object Class Types
-----------------------------

A class root is converted to a container or list.

-  A direct conversion to a YANG 1.1 grouping is not possible.
-  A separate grouping for the class contents can be used to
   allow direct YANG 1.1 compatibility.

**Example Convert Class to a P-container:**

Example class:

.. code-block:: yang

       class address {
         presence "P-container";
         uses address-fields;
       }


Example grouping:

.. code-block:: yang

       grouping address {
         container address {
           presence "P-container";
           uses address-fields;
         }
       }


TBD: complete definitions and provide examples
