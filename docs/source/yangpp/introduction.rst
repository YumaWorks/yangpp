
.. include:: ../header.txt


YANG++ Introduction
====================

The YANG++ language adds some object-oriented design capability to
the YANG language. A simple conceptual class hierarchy is defined,
based on four basic :ref:`class types`.


YANG++ Terminology
-------------------------

-  **class**: a reusable set of YANG statements

-  **class ID**: the module name and class identifier value for a class

-  **base class**: a built-in base type, not defined with a class definition

-  **class instance**: a data tree conforming to the conceptual schema node
   defined by the class

-  **class root**: the topmost data node and XPath document root for the
   class instance

-  **concrete class**: a class that does not contain any virtual objects.

-  **concrete object**: an object that is not defined within
   a :ref:`virtual-stmt`

-  **derived class**: a class that has a parent-class

-  **implemented class**: the concrete class used in the implementation

-  **parent class**: the class that is inherited by a derived class

-  **root class**: a class that has a base class and no parent class

-  **specified class**: the class used in the YANG data model

-  **virtual class**: a class that contains any :ref:`virtual objects`

-  **virtual object**: a named object that is defined within a
   :ref:`virtual-stmt`

-  **virtual object template**: an un-named object that is defined within
   a :ref:`virtual-stmt`


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

YANG++ classes allows this sort of extensibility
without changing any of the 'uses' statements or requiring augment
and deviation statements for every 'uses' statement.


.. code-block:: yang

    class std-parms {
      leaf std-leaf ( type string; }
    }

    class my-parms {
      parent-class std-parms;
      leaf my-extra-leaf { type string; }
    }

    // since match is derived-from-or-self both
    // std-grouping and my-grouping are allowed
    // YANG library indicates any class mappings
    uses-class std-parms {
      root-name top;
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
:rfc:`5277` can be defined with a simple YANG++ message base class
containing an 'any notification' statement.

.. code-block:: yang

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

**Virtual Object Templates**

:ref:`Virtual objects` can be un-named, allowing the concrete object definition
to pick the name of the object.


**Containment and Model Structure**

YANG 1.1 allows every type of statement to appear in any module.
There are no rules or even guidelines for the organization
of modules that augment and deviate a base model.

It is often difficult to tell where all the data definitions
for the expanded schema tree are located.  They are scattered
across any number of modules.  The YANG++ class hierarchy
allows these definitions to be defined in one place.

Inline deviations are allowed in YANG++, for use-cases where
an existing class definition is almost suitable for a new application,
but needs deviations (e.g., remove an irrelevant leaf).


**Standard Library**

The :ref:`YANG++ Standard Library` contains conceptual API
definitions that allow basic operations on classes.
There is one API defined at this time to :ref:`compare classes`.

**Seamless Integration With YANG 1.1**

Every statement in YANG 1.1 is supported in YANG++.
YANG++ is designed to use YANG 1.1 directly, so it is easy
to reuse existing YANG 1.1 modules.
The XPath syntax is extended to support :ref:`class path string`
syntax, but all existing XPath syntax is still valid.


**Automatic Translation to YANG 1.1**

It should be possible to define a standard :ref:`YANG 1.1 Translation`
if all virtual objects are resolved and known to the compiler.
Translation allows existing tools to be used with new YANG++ models.

The :ref:`any-stmt` cannot be supported in YANG 1.1 since
all YANG 1.1 nodes are named, and this statement is a placeholder template
without an assigned name.

**Relationship to YANG Language Abstractions**

There is existing work in this area in :rfc:`6095`.
It contains a specification for a layered abstraction model,
and a detailed example for chassis components.
The YANG++ builds on this effort and addresses the
reusability and integration aspects of YANG.

The previous work was more focused on providing XML
Schema Document (XSD) functionality by introducing complex types.
YANG++ attempts to provide the layered abstraction capabilities
with derived classes. :ref:`Virtual objects` are supported
with more control over the model behavior.

YANG++ does not provide any recursion features like :rfc:`6095`.
This is very complex to implement and it cannot be supported in
YANG. A final schema tree cannot be generated if a class or
grouping uses itself, because this causes infinite depth.


New YANG Statements
---------------------

There are two new statements (plus sub-statements)

-  :ref:`class-stmt`: a top-level body-stmt like 'identity-stmt'.
-  :ref:`uses-class-stmt`: a data-def-stmt like 'uses-stmt'

There is a YANG Library addition to advertise the class bindings
used (e.g. by the server) to produce the expanded schema tree.

New YANG Library Objects
---------------------------

The :ref:`class name binding` information for a server
needs to be defined that specifies the implemented classes
on the server. This YANG module is defined
in the :ref:`YANG Library Additions` section.


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

-  Instead of augmenting and deviating objects for every 'uses'
   of a grouping, the :ref:`parent-class-stmt` is used to
   conceptually and automatically extend the grouping.

The server is allowed to apply any valid class to a particular
uses-class expansion.

-  The server is not required to use the same class in every
   expansion like a grouping.

The :ref:`YANG library additions` define mappings between the specified class names
and the implemented classes used.



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
   for this purpose.  The root-name is needed to use the same class
   more than once as sibling nodes.

   .. code-block:: yang

        class envelope {
          uses-class address {
            root-name from-address;
          }
          uses-class address {
            root-name to-address;
        }
      }


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


Class References
---------------------------------

A class reference is defined with the :ref:`class path string`
and exported from the class with a :ref:`classref-stmt`.

TBD: decide if classref-stmt needed or rely on compilers
to find all the class path strings.  It may be useful for documentation
and instructions to YANG modelers needing to write the
:ref:`uses-class-stmt` for the class with external references.

There are two types of class references defined:

-  **external class reference**: path string document root and context node
   is the class root of the external class

-  **current class reference**: path string document root and context node
   is the class root of the current class


An external class reference allows objects in other classes
to be used in YANG validation statements (must, when, path)
without knowing the final schema tree
locations of the objects.

References to objects in other classes should be done if possible
to make the class as relocatable as possible.  However,
traditional paths referencing the final schema tree are supported.

A class is expected to "export" its class references using
the :ref:`classref-stmt`. A separate statement is needed
for each class instance used in a conceptual reference.

Example:

.. code-block:: yang


    class caps {
      leaf max-widgets {
        type uint32;
        default 42;
      }
    }

    // mod1 defines the system capabilities class
    class system-caps {
      parent-class caps;
      // add more system caps
    }

    // mod2 defines the system config class
    class system-config {
      classref "mod1:system-caps::syscaps" {
        description "Need to reference the system capabilities";
      }

      container mycaps {
        leaf max-widgets {
          must ". <= /mod1:system-caps::syscaps/max-widgets";
          type uint32;
        }
      }
    }




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

-  A virtual object can be mapped to a new virtual object.

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


**Example: Abstract class represents a contact entry in a phone book.**

.. code-block:: yang

   class contact-template {
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

    class contact {
      parent-class contact-template {
        map-virtual identity {
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
configured to map the 'Contact' class to the 'contact-template' class.

.. code-block:: yang

    container sysadmin-contact {
      uses-class contact-template;
    }



A new abstract class can be created which uses this class:

.. code-block:: yang

    class contacts {
      autokey;
      uses-class contact-template {
        root-name contact;
      }
    }


**Example: A virtual case within a concrete choice**

.. code-block:: yang

    class options {
      virtual {
        augment "config/mand-choice" {
          case <mand-case>;
        }
      }

      container config {
        choice mand-choice {
          mandatory true;
        }
      }
    }

In this example it is clear to developers and compilers
that the model requires at least one case to be usable.


.. code-block:: yang

    class my-options {
      parent-class options {
        map-virtual mand-case {
          map-path "config/mand-choice/my-case";
        }
      }

      augment "config/mand-choice" {
        case my-case {
          leaf my-leaf { type string; }
        }
      }

    }




Class Root
-------------

A YANG++ class is more structured than a grouping.
It has a combination of properties from existing YANG constructs.

-  A class is like a 'grouping' since it is abstract and requires
   a corresponding 'uses' type of statement to create real schema nodes.
-  A class is also like a schema mount point because it can be used
   in a position independent way without rewriting XPath and path statements.

The class root is a real schema node just like a schema mount point.
The schema node type (container or list) depends on the class root type.
The class root is also the document root for any :ref:`class path string`
referencing the class.


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
   is a list with the integer 'position' index as the key.

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


Path For Current Class
~~~~~~~~~~~~~~~~~~~~~~~~~

A special shorthand string is available, similar to the 'this'
pointer in C++.  This allows the class root to be easily
referenced from anywhere within the class, so paths are
simpler to use without mistakes.


.. code-block:: text

         '::/' [ path ]




Examples:

.. code-block:: text

     ::/

     ::/last-name

     ::/top2/B
