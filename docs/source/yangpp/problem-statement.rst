
.. include:: ../header.txt

YANG++ Problem Statement
==============================

The YANG reuse mechanisms need improvement.

Modern software is object-oriented with a layered abstraction model.
This provides a more structured and reusable design, that can be
easily adapted for new uses.

YANG data models are difficult to use because
the components of a composite conceptual model are spread
over many modules.  There can be many standard modules,
vendor models, and vendor deviations, all required to
understand the intended data model.

The YANG reuse mechanisms do not provide any real abstraction layer.
A grouping is just a syntactic mechanism to cut-and-paste
data node definitions.  All path references (must, when, leafref)
must specify the final schema tree.  It is not easy to construct
path expressions that are position-independent.

If YANG was more object-oriented it would be easier to build
and maintain reusable software that used the data models derived
from the YANG modules.



Problems With Groupings
--------------------------

YANG 1.1 (:rfc:`7950`) has 'grouping-stmt' to define reusable components.
This supports abstraction of schema nodes that are
expanded with the 'uses-stmt'.

A YANG 'grouping' statement is like a C typedef for a struct.
This is just an abstraction that does not cause any real schema
nodes to be created

A YANG 'uses' statement is a like a C variable using the struct typedef
The expansion of the grouping creates real schema nodes that
can be accessed with NETCONF or RESTCONF.

Groupings and the uses expansion mechanisms have several limitations:

-  **Groupings cannot be augmented**

   -  A new grouping can be created with a new name
      but all the related 'uses' statements would need to be
      changed to specify the new grouping name.

   -  Each location where a 'uses' statement expands the grouping
      can have 'augment' statements added to it.

   -  Development of standard groupings takes a long time
      in an attempt to provide a complete and 'perfect' grouping
      in the first release.

-  **Groupings are invariable and apply the same everywhere they are used**

   -  There is no way to upgrade or refine a grouping.  Each
      expanded 'uses' statement must be augmented or refined.

   -  It can be much simpler to modify the grouping instead
      of modifying the expansion in each 'uses' statement.

   -  It should be possible to provide updates, upgrades,
      vendor enhancements and deviations in 'replacement'
      groupings that are expanded instead of the specified grouping.

   -  It can be complex and error-prone to find and update
      every expansion of a grouping.  This is tedious work
      and can result in large YANG files if a grouping is
      used frequently.


-  **Groupings cannot reference other groupings**

   -  Groupings can use other groupings but they can also reference
      data nodes in the schema tree. The 'must', 'when', and 'path'
      statements apply to the schema tree, after all 'uses'
      statements have been expanded.

   -  The external references assume a certain structure
      which limits the contexts and schema tree locations
      that a grouping can be used.

   -  It is desirable to reference nodes in other groupings,
      so the references are completely relocatable, as much
      as possible.  The actual schema tree nodes should not need to
      be specified.  It should be possible to defer this step
      until the 'uses' statement is expanded.

-  **Groupings cannot be deviated**

   -  Groupings are not always completely reusable as defined.
      It is desirable to apply deviations to a grouping,
      instead of needing to apply the deviations every place
      the grouping is expanded with the 'uses' statement.


Problems Building Data Models
------------------------------

Although the term 'data model' is not precise, it generally refers
to the conceptual schema tree derived from the final expansion
of the objects, according to the associated YANG library.

It is desirable to extend and alter any grouping without
needing to monitor every usage of that grouping.

YANG 1.1 has 2 ways to extend and change data models.
In both cases the designer must be aware of every
usage of the grouping in order to extend or change it.

The first is to create a new grouping that uses the old grouping
and replace the 'uses' statement everywhere the new grouping is needed.
It is often unacceptable because the source module cannot be changed,
especially for standard modules.


.. code-block:: yang

    // module std
    grouping std-parms {
      leaf std-leaf ( type string; }
    }

    // module example-parms
    grouping my-parms {
      uses std:std-parms;
      leaf my-extra-leaf { type string; }
    }

    // OLD module top-parms
    container top {
      uses std:std-parms;
    }

    // NEW module top-parms
    container top {
      uses ex:my-parms;
    }


The only approach that is widely used is to  augment and deviate each
expanded data node everywhere the 'uses' statement for
the grouping appears. This "after expansion" approach is difficult
to maintain to achieve consistent and current YANG module additions.
It may be possible if there are only one or two uses of the grouping,
and the designers are aware of every usage of the grouping.


.. code-block:: yang

    // module std
    grouping std-parms {
      leaf std-leaf ( type string; }
    }

    // module top-parms
    container top {
      uses std-parms;
    }

    // module example-parms
    augment /top {
      leaf my-extra-leaf { type string; }
    }




YANG is Not Relocatable
-------------------------

YANG is not relocatable.
The path strings for schema nodes or data nodes must be specified from root,
or be relative to the context node determined by various complex rules.

It is not possible to use path locations that are relative to
an abstract definition (e.g., grouping) instead of referencing
only the data tree.



Magic Root Problems
------------------------

YANG lacks a standard way to identify a "root" node.
This is a container or list node that have conceptual child
nodes.  The set of child nodes is derived from the
top-level datastore objects in the modules from some module-set.


Anydata Parameter Problems
----------------------------------

The 'anydata' (or 'anyxml') node types are misused.

- They are used as roots, which is inappropriate because
  these are terminal nodes in the schema.

- Even when used correctly to represent some actual YANG subtrees,
  there is no standard way to identify which subtrees are encoded as
  child nodes of the 'anydata'.

-  There is no way to properly validate child nodes of 'anydata'.


Message Validation Problems
-------------------------------

The 'sx:structure' extension from :rfc:`8791` is often used to model
message definitions so YANG automation tools can be used.
However many protocol messages are too complex for YANG, because an
abstract **unnamed** node is present in the message pattern.
The 'notification' message from :rfc:`5277` is an example of this
type of message.
