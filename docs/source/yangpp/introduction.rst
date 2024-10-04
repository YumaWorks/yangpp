
.. include:: ../header.txt


YANG++ Introduction
====================

The YANG++ language adds some object-oriented design capability to
the YANG language.

However it is much more structured and powerful than a grouping.


YANG++ Terminology
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * -  term
     -  description

   * -  class
     -  a reusable set of YANG statements
   * -  base class
     -  a class that has no parent class
   * -  parent class
     -  a class that is inherited by a derived class
   * -  derived class
     -  a class that has a parent-class
   * -  specified class
     -  the class used in the data model
   * -  implemented class
     -  the class used in the implementation
   * -  class instance
     -  a data tree conforming to the conceptual schema node
        defined by the class
   * -  class root
     -  the topmost data node corresponding to the XPath
        document root for the class instance


YANG++ Design Goals
----------------------

The main goal of YANG++ is to introduce object-oriented YANG data modeling.
This can change the way YANG data models are constructed.

**Ease of Use**

YANG models are constructed from many modules, often from different sources.
Real devices have a complex collection of modules:

- standard modules from multiple SDOs
- vendor modules that augment and/or deviate standard modules
- vendor modules
- vendor product-specific deviations


It is desirable to create new functionality
from existing building blocks:

-  It is difficult and expensive to design and maintain all these YANG modules.
-  It is difficult to achieve consistent model behavior if all the
   augmentations, refinements, and deviations have to be specified
   separately for each expansion of a grouping, and not the grouping itself.
-  It is even more difficult for client applications to use the high level
   functionality from all the YANG library modules.
-  It would be simpler to use an object-oriented class hierarchy instead of
   a complex set of augments, refines, and deviations


**Reusability**

External references to objects outside the subtree being defined
should be kept as position-independent as possible.  YANG++
introduces :ref:`Position Independent YANG`,
which supports class to class external references.

The actual objects used in the external
class reference can be determined when the class is used
with the "ref'`uses-class-stmt`.
Regular schema tree external references are also supported,
but such usage is not position-independent.

**Extensibility**

Classes can be easily extended and even deviated using
a derived class.  This allows the abstract definitions
to be customized. YANG 1.1 requires every usage of a grouping
to be augmented, refined, and deviated.  YANG++ has the option
to doing this at the abstract class level.

-  YANG 1.1 requires that a designer create a new grouping
   that includes and changes the base grouping

.. code-block:: yang

    grouping std-grouping {
      // ...
    }

    grouping my-grouping {
      uses std-grouping;
      leaf my-extra-leaf {
        // ...
      }
    }

One problem is that every location the 'std-grouping' is used,
the module is changed to use 'my-grouping' instead.

.. code-block:: yang
   :emphasize-lines: 3, 8

     // OLD:
     container std-parms {
       uses std-grouping;
     }

     // NEW:
     container std-parms {
       uses my-grouping;
     }


This is often unacceptable and/or impractical.

YANG++ classes allows this sort of extensibility
without changing any of the 'uses' statements.

.. code-block:: yang
   :emphasize-lines: 13 - 16

    class std-grouping {
      // ...
    }

    class my-grouping {
      parent-class std-grouping;
      leaf my-extra-leaf {
        // ...
      }
    }

     container std-parms {
       // since match is derived-from-or-self both
       // std-grouping and my-grouping are allowed
       // YANG library indicates any class mappings
       uses-class std-grouping;
     }


**Abstract Schema Nodes: Message Templating**

YANG++ classes allow abstract placeholder nodes to be
defined with the "ref"`any-stmt`, to support structures
such as message templates.

This statement may only be applicable to the 'message'
base class.  It represents an un-named schema node
but no further schema information (i.e. derived class)
will be available, so a virtual node cannot be used.

For example, the 'notification' message header defined in
:rfc:`5277` can be defined with a simple YANG++ class:

.. code-block:: yang
   :emphasize-lines: 11

    class notification {
      base-class message;

      leaf eventTime {
        type yang:date-and-time;
        mandatory true;
        description
          "Timestamp from RFC 5277.";
      }

      any notification {
        mandatory true;
        description
          "An abstract placeholder for a representation of
           any notification-stmt.";
      }
    }


**Virtual Objects**

:ref:`Virtual objects` allow a class hierarchy to be defined with
virtual actions, notifications, and data definitions, that are expected
to be replaced and possibly "filled in" with real definitions
by a derived class.

This is sometimes similar to a YANG 1.1 empty choice, which other modules
are expected to augment with 'case' statements.

-  A derived class can add to the virtual node when a concrete node
   is defined.  This is similar to 'augments' but much simpler to use.

-  Un-named virtual nodes are supported, which allow the concrete
   node to have a different name than the virtual node.

-  If a :ref:`uses-class-stmt` specifies a class with any virtual
   objects in it, then a :ref:`class name binding` for a concrete
   class MUST exist in the YANG library configuration.

-  A concrete object cannot be changed to a virtual object in a derived class.

-  A virtual object cannot be mapped to another virtual object.

-  If any virtual objects are not defined in the derived class
   then the derived class is also a virtual class.  The virtual
   nodes are passed through to the next derived class.

-  Properties can be added by a derived concrete object.

-  Any changes to the inherited virtual or concrete objects
   need to be allowed with 'refine' and/or 'deviation' statements
   within the :ref:`parent-class-stmt`.

-  Variations from the inherited virtual object without any
   such statements are treated as errors.

-  TBD: Use warnings instead of strict rules for NBC changes

-  TBD: complex nested templates with deep virtual objects

Example: Abstract class represents a Contact entry in a phone book.

.. code-block:: yang

   class ContactTemplate {
     virtual {
       container <identity> {
         description
           "Container with the fields representing the
            identity of the contact. The container can have
            any name valid for the context, that does not conflict
            with any sibling node names.";
       }
       container contact-info {
         description
           "Container with the fields representing the
            contact information for the person with
            the associated <identity> information.
            The container must be named 'contact-info'.";
       }
     }
   }


A derived class is needed which resolves the virtual objects.

-  A :ref:`map-virtual-stmt` is needed for the ``<identity>``
   mapping to a concrete object name.

-  This mapping is not needed for the ``contact-info`` container
   since a name change is not allowed.


.. code-block:: yang

    class Contact {
      parent-class ContactTemplate {
        map-virtual <identity> {
          map-path name;
        }
      }

      container name {
        leaf first-name { type string;
        leaf last-name { type string; }
      }

      container contact-info {
        leaf email-address {
          type string;
        }
      }
    }

In this example, a :ref:`class name binding` must be
configured to map the 'Contact' class to the 'ContactTemplate' class.

.. code-block:: yang

    container sysadmin-contact {
      uses-class ContactTemplate;
    }



A new abstract class can be created which uses this class:

.. code-block:: yang

    class ContactList {
      list contacts {
        autokey;
        uses-class ContactTemplate;
      }
    }



**Containment and Model Structure**

YANG 1.1 allows every type of statement to appear in any module.
There are no rules or even guidelines for the organization
of modules that augment and deviate a base model.

It is often difficult to tell where all the data definitions
for the expanded schema tree are located.  They are scattered
across any number of modules.  The YANG++ class hierarchy
allows these definitions to be defined in one place.


**Standard API Library**

The :ref:`YANG++ Standard Library` contains conceptual API
definitions that allow basic operations on classes.

There is one API defined at this time to :ref:`compare classes`.

New YANG Statements
---------------------

There are two new statements (plus sub-statements)

-  :ref:`class-stmt`: a top-level body-stmt like 'identity-stmt'.
-  :ref:`uses-class-stmt`: a data-def-stmt like 'uses-stmt'

There is a YANG Library addition to advertise the class bindings
used (e.g. by the server) to produce the expanded schema tree.

YANG Library Extensions
---------------------------

The :ref:`class name binding` information for a server
needs to be defined that specifies the implemented classes
on the server. This YANG module is TBD.

.. code-block:: yang

    augment /yanglib:yang-library {
      container classes {
        // contents TBD
      }
    }



Class Types
---------------

There are 4 types of classes defined:

-  **root** : configuration root with top-level YANG data schema nodes
   as child nodes

   -  :ref:`root base-class`

-  **object** : YANG data-def-stmt node

   -  :ref:`object base-class` (default)

-  **message**: Abstract structure representing a protocol message

   -  :ref:`message base-class`


-  **structure**: Abstract structure representing an 'sx:structure'

   -  :ref:`structure base-class`

Each class definition has a class type, which is determined
by the presence of the :ref:`base-class-stmt` or
the :ref:`parent-class-stmt`.
Each class definition within a YANG module defines a 'base class'
or a 'derived class'.

-  If a :ref:`base-class-stmt` is present then the class being defined
   is a base class with the specified class type.

-  If a :ref:`parent-class-stmt` is present then the class being defined
   is a derived class with the specified parent class.

-  If neither statement is present then the class being defined
   is a base class with the :ref:`object base-class`.




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



Late Name Binding
-------------------

Whenever possible the path references within a class, either to itself
or to other classes should be relative and relocatable.
This requires some changes and improvements to the tools:

-  Algorithmic linkage between the class being defined
   and a referenced class. The :ref:`bind-classref-stmt` is used
   to link a referenced class to a specific class instance.

-  Late assignment of the schema node name used for the class root.
   The :ref:`root-name-stmt` is used within the :ref:`uses-class-stmt`
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

    specified class name  ->  implemented class name

Example:

.. code-block:: text

    address  ->  us-address


There are 2 types of class name bindings that can both be used
for the same class name. They are checked in this order:

-  **Object Level**:  The class binding is used for the
   specified object node.

   .. code-block:: yang

       object-binding /system/address {
         root-name us-address;
       }


-  **Class Level**:  The class binding is used for all
   usage of the specified class.

   .. code-block:: yang

       class-binding address {
         root-name us-address;
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
It has a combination of properties from existing YANG constructs.
A class is like a 'grouping' since it is abstract and requires
a corresponding 'uses' type of statement to create real schema nodes.
A class is also like a schema mount point because it can be used
in a position independent way without rewriting XPath and path statements.
The class root is a real schema node just like a schema mount point.

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

For every usage of a class, the specified class and the
implemented class MUST have a matching root type.
For list types, the keys MUST also match.


Class Instances
-----------------------

An instance of a class is not the same as the expansion
of a grouping.

There is a data node created with the name corresponding to
the class named in the 'uses-class-stmt'.

Example: The same 'address-fields' leafs from a grouping are
used to create different types of class instances.

-  If a non-empty 'key' statement is present in the class then the class root
   is a list with one or more key leafs.

   .. code-block:: yang

       class address {
         key "last-name first-name";
         uses address-fields;
       }

-  If an empty 'key' statement is present in the class then the class root
   is a list with the integer index as the key.

   .. code-block:: yang

       class address {
         key "";
         uses address-fields;
       }

-  If a 'presence' statement is present in the class then the class
   root is a presence container.


   .. code-block:: yang

       class address {
         presence "P-container";
         uses address-fields;
       }

-  If neither of the 'presence' or 'key' statements is present then
   the class root is a non-presence container.

   .. code-block:: yang

       class address {
         uses address-fields;
       }


Class Lifecycle
--------------------


The 'status' property (:rfc:`7950#section-7.21.2`) is used in YANG++,
but there are changes and additions.

The enumerations have the following meaning in YANG++:

-  **current**: class definition is current and MUST be implemented
   if supported
-  **deprecated**: class definition is deprecated and MUST be
   implemented if supported.

   -  This class SHOULD be changed to 'obsolete'
      status in the future.

   - A :ref:`deprecated-stmt` is expected to be present for this class

-  **obsolete**: class definition is obsolete and SHOULD NOT be implemented





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

Example:

Class Path String
~~~~~~~~~~~~~~~~~~~


A plain 'path', 'must' or 'when' expression is always
relative to the 'root' node.  Class path strings are
not relative to the document root. Instead they are
relative to the specified class reference point.

-  Use the :ref:`classref-stmt` in the :ref:`class-stmt`
   to declare the reference point.
-  Use the :ref:`bind-classref-stmt` in the :ref:`uses-class-stmt`
   to bind the reference point to the schema tree.

Since a class root is a real data node the 'uses-class'
statement can be placed anywhere with consistent predictable
results, unlike the parent of a 'uses' statement.
The parent of any statements in the class is the class root.

**Only the first path segment is changed.**
In each XPath 'expr', if this segment identifies a class reference point,
then the 'path' string that follows is relative to that class root.
The actual schema tree
root is determined when the class is used.

A class-relative expression begins with a special string containing
the class name and the reference point name:

.. code-block:: text

     [ prefix ':' ] class-name '::'  classref '/' path

.. container::

   .. note::

      -  The 'path' does not include the class root name.
         Instead the reference point name is used.
      -  The 'path' is a relative-path not absolute-path


Examples:

.. code-block:: text

     addr:address::user-address/last-name

     us-address::mgmt-addr/zipcode


A Class Path string is position-independent.
The actual schema nodes used for the validation
are determined by the :ref:`uses-class-stmt` details.
The actual paths are adjusted, based on the schema tree
location of the 'uses-class' statement.


**Example: when-stmt linkage**

The class 'class-B' from 'mod2' could contain a conditional leaf that depends
on the value of another leaf in 'class-A' from 'mod1'.


.. code-block:: yang

    class class-A {
      container top {
        leaf A {
          type int32;
        }
      }
    }


    class class-B {
      classref "mod1:class-A::test" {
        description "An example test reference point";
      }
      container top2 {
        leaf B {
          when "/mod1:class-A::test/top/A > 10";
          type int32;
        }
      }
    }


**Example: leafref linkage**

The class 'person-name' could contain a leafref that depends
on the value of the 'last-name' leaf in an address class,
defined in the 'addr' module.



.. code-block:: yang

    class person-name {
      classref "addr:address:addr";
      leaf last {
        type leafref {
          path "addr:address::addr/last-name";
        }
      }
      leaf first {
        type leafref {
          path "addr:address::addr/first-name";
        }
      }
    }
