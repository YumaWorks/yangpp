
.. include:: ../header.txt


YANG++ Introduction
====================

The YANG++ language adds some object-oriented design capability to
the YANG language.

However it is much more structured and powerful than a grouping.

YANG++ Design Goals
----------------------

The main goal of YANG++ is to introduce object-oriented YANG data modeling.

-  Improve reusability
-  Introduce :ref:`Position Independent YANG`


New YANG Statements
---------------------

There are two new statements (plus sub-statements)

-  :ref:`class-stmt`: a top-level body-stmt like 'identity-stmt'.
-  :ref:`uses-class-stmt`: a data-def-stmt like 'uses-stmt'

There is a YANG Library addition to advertise the class bindings
used (e.g. by the server) to produce the expanded schema tree.

-  classes


YANG++ Terminology
-------------------------

-  class: a reusable set of YANG statements
-  base class:  a class that has no parent class
-  parent class: a class that is inherited by a derived class
-  derived class: a class that has a parent-class
-  class instance: a data tree conforming to the conceptual schema node
   defined by the class
-  class root: the topmost data node corresponding to the XPath
   document root for the class instance



Class Types
---------------

Each class definition has a class type, which is determined
by the presence of the :ref:`base-class-stmt` or
the :ref:`parent-class-stmt`.

Each class definition within a YANG module defines a 'base class' or a 'derived class'.


.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * -  base-class present
     -  parent-class present
     -  outcome

   * -  no
     -  no
     -  Base Class with :ref:`object base-class`

   * -  yes
     -  no
     -  Base Class with specified base-class

   * -  no
     -  yes
     -  Derived Class with inherited base-class

   * -  yes
     -  yes
     -  **Error**




Class Inheritance
--------------------------

A derived class has a linear chain of ancestors, similar to
a YANG identity.  When a class is used (e.g. uses-class base1;)
the validation is the same as for an identityref leaf.

-  Instead of exact match, it is a derived-from-or-self() match

The server is allowed to apply any valid class to a particular
uses-class expansion.

-  The server is not required to use the same class in every
   expansion like a grouping.

The YANG library contains mappings between library class names
and the real classes used.

TBD: multiple inheritance (i.e. multiple parent-class-stmt)


Late Name Binding
-------------------

Whenever possible the path references within a class, either to itself
or to other classes should be relative and relocatable.
This requires some changes and improvements to the tools:

-  Algorithmic linkage between the class being defined
   and a referenced class. The :ref:`bind-class-stmt` is used
   to link a referenced class to a specific class instance.

-  Late assignment of the schema node name used for the class root.
   The :ref:`class-name-stmt` is used within the :ref:`uses-class-stmt`
   for this purpose.



Class Name Binding
---------------------------------

A server is not required to implement the exact class
that is specified in the model, called the 'specified class'.
The actual class used is called the 'implemented class'.
By default they are the same, but this is not required.
A set of class name mappings is needed to properly expand
the YANG++ schema implemented by a server in this case.

A valid class name binding has the following properties:

-  The implemented class is derived from the specified class
-  The specified class root type must match the implemented
   :ref:`class root type`

   -  For lists, the 'key' statement must be the same in both
      classes or the class does not match. If one class has
      a 'key' statement then the other must also have one that
      exactly matches.


The YANG library is used for the module information.
It needs to be extended with class name binding information.

-  The actual classes used are expected to be advertised in
   the YANG library for the server (TBD).

-  It is also possible that the class name bindings could be specified
   in a YANG Package.



.. code-block:: text

    specified class name  -> implemented class name

Example:

.. code-block:: text

    address ->  us-address


There are 2 types of class name bindings that can both be used
for the same class name. They are checked in this order:

-  **Object Level**:  The class binding is used for the
   specified object node.

   .. code-block:: yang

       object-binding /system/address {
         class-name us-address;
       }


-  **Class Level**:  The class binding is used for all
   usage of the specified class.

   .. code-block:: yang

       class-binding address {
         class-name us-address;
       }


If no class name binding is found then the specified class
name is also the implemented class name.





Virtual Objects
-----------------

A base class or parent class can define virtual objects,
which can be mandatory or optional to map. A derived class
must map these virtual objects to real objects.

A class instance cannot have any missing mandatory virtual objects.

The type and name of the object can also be virtual.

If the class identifier is wrapped in angle brackets then the
name is a virtual name that is expected to be replaced
in a derived class.  The first class that binds a real name
to the object becomes the name of the object in the class API.


Class Root
-------------

A YANG++ class is more structured than a grouping.
It has a combination of properties from existing YANG constructs

-  **grouping**:  a class is abstract like a grouping and requires
   a corresponding 'uses' type of statement to create real schema nodes

-  **mount point**:  a class root can be used in a position independent way
   without rewriting XPath and path statements.  The class root is a real
   schema node just like a mount point.

The class root is an actual schema node in the object tree.
The schema node type depends on the class root type.


Class Root Type
~~~~~~~~~~~~~~~~~~

A class root can be one of 3 types of YANG schema nodes:

-  presence container
-  non-presence container
-  list

The :ref:`uses-class-stmt` is used to bind classes to actual schema tree nodes.
The class root is the top-level schema node which conceptually replaces the
'uses-class' statement.



Class Instances
-----------------------

An instance of a class is not the same as the expansion
of a grouping.

There is a data node created with the name corresponding to
the class named in the 'uses-class-stmt'.

-  If a non-empty 'key' statement is present in the class then the class root
   is a list with one or more key leafs.

   .. code-block:: yang

       class address {
         key "last-name first-name";
         uses address;
       }

-  If an empty 'key' statement is present in the class then the class root
   is a list with the integer index as the key.

   .. code-block:: yang

       class address {
         key "";
         uses address;
       }

-  If a 'presence' statement is present in the class then the class
   root is a presence container.


   .. code-block:: yang

       class address {
         presence "P-container";
         uses address;
       }

-  If neither of the 'presence' or 'key' statements is present then
   the class root is a non-presence container.

   .. code-block:: yang

       class address {
         uses address;
       }


Class Lifecycle
--------------------


The 'status' property (:rfc:`7950#section-7.21.2`) is used in YANG++,
but there are changes and additions.

The enumerations have the folowing meaning in YANG++:

-  **current**: class definition is current and MUST be implemented
   if supported
-  **deprecated**: class definition is deprecated and MUST be
   implemented if supported.

   -  This class SHOULD be changed to 'obsolete'
      status in the future.

   - A :ref:`deprecated-stmt` is expected to be present for this class

-  **obsolete**: class definition is obsolete and MUST NOT be implemented







Position Independent YANG
------------------------------

It is possible in YANG++ to specify 3 different types of path strings

-  Schema Node Path:

   -  Traditional schema tree path that is used
      in the 'augment' and 'deviation' statements.
   -  The root node is the root of a datastore or a mount point
      within a datastore.

-  Data Node Path:

   -  Traditional data tree path that is used
      in the 'path' statement.
   -  The root node is the root of a datastore or a mount point
      within a datastore.

-  Class Path:

   -  New data tree path that is used
      in any statement referencing a data node.
   -  The root node is the class root.
   -  The class root serves as the 'docroot' for the XPath context
      for the class.


YANG++ classes can always reference nodes in their own class
(same as a grouping). However, it can also reference nodes in
other classes using a 'class path'.

The actual data node bindings are done with the :ref:`uses-class-stmt`.


Class Path Syntax
~~~~~~~~~~~~~~~~~~~


A plain 'path', 'must' or 'when' expression is always
relative to the 'root' node.  These path strings are
not relative to the class root.

Since a class root is a real data node the 'uses-class'
statement can be placed anywhere with consistent predictable
results, unlike the parent of a 'uses' statement.
The parent of any statements in the class is the class root.

A class-relative expression begins with a special string containing
the class name:

.. code-block:: text

     [ prefix ':' ] class-name '::' path


Example:


.. code-block:: text

     mod1:class-A::top/A


A Class Path string is position-independent.
The actual data nodes used for the validation
are determined at run-time.
The actual paths are adjusted, based on the 'uses-class' statement.


-  TBD: Details of design-time, build-time, and run-time binding control



Example: 'class-B' from 'mod2' could contain a conditional leaf that depends
on the value of another leaf in 'class-A' from 'mod1'.


.. code-block:: yang

    class class-A {
      base-class object;

      container top {
        leaf A {
          type int32;
        }
      }
    }


    class class-B {
      base-class object;
      container top2 {
        leaf B {
          when "/mod1:class-A::top/A > 10";
          type int32;
        }
      }
    }
