
.. include:: ../header.txt


YANG 1.1 Translation
================================

It should be possible to use modules that contain YANG++ statements
with tools that only understand YANG 1.1 modules, by converting
the module to YANG 1.1 first.

The intermediate or final expansion of YANG++ language constructs
can be converted to an equivalent set of YANG 1.1 modules.
Constructs that do not exist in YANG 1.1 can be omitted or
converted to YANG extensions.


**Direct Translation Approach**

The direct translation focuses entirely on the final schema tree.

-  Each :ref:`uses-class-stmt` must be replaced with the
   equivalent YANG 1.1 statements

   -  statements not supported by YANG 1.1 must be omitted or
      converted to extensions somehow


-  All :ref:`class-stmt` definitions can be removed from the
   translation.

**Grouping Translation Approach**

For the 'object' base class, a class can be easily converted
to a grouping, and a 'uses-class' statement can be converted
to a 'uses' statement.


-  Each :ref:`class-stmt` definition is converted to a grouping

-  Each :ref:`uses-class-stmt` is replaced with a 'uses' statement
   for the grouping that was converted from a class.

-  It may not be possible to converted derived classes into
   a hierarchy of groupings.  Instead, all inherited concrete
   statements are also included in the grouping.

**XPath Conversion**

Proper XPath conversion from Class Path strings to plain XPath
may only be possible using the direct translation approach.
The complete XPath cannot be constructed until the final 'uses'
expansion point is known.


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
Unlike a grouping, a class has a root node that becomes a
real schema node, exactly as done for YANG Schema Mount :rfc:`8528`.

**Example: Convert Class to a P-container:**

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


**Example: Convert Class to a List:**

Example class:

.. code-block:: yang

       class address {
         key "last-name first-name";
         uses address-fields;
       }


Example grouping:

.. code-block:: yang

       grouping address {
         list address {
           key "last-name first-name";
           uses address-fields;
         }
       }


**Example: Convert a Derived Class to a Grouping:**

Example class:

.. code-block:: yang

    class std-parms {
      leaf std-leaf ( type string; }
    }

    class my-parms {
      parent-class std-parms;
      leaf my-extra-leaf { type string; }
    }


Example grouping:

.. code-block:: yang

       grouping my-parms {
         container my-parms {
           leaf std-leaf ( type string; }
           leaf my-extra-leaf { type string; }
         }
       }




TBD: complete definitions and more examples
