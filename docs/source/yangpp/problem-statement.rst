
.. include:: ../header.txt

YANG++ Problem Statement
==============================

**The YANG reuse mechanisms need improvement.**

Modern software is object-oriented with a layered abstraction model.
This provides a more structured and reusable design, that can be
easily adapted for new uses.

If YANG was more object-oriented it would be easier to build
and maintain reusable software that used the data models derived
from the YANG modules.

There are several limitations of YANG 1.1 addressed in YANG++.


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
