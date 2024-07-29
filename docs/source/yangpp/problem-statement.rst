
.. include:: ../header.txt

YANG++ Problem Statement
==============================

**The YANG reuse mechanisms need improvement.**

Modern software is object-oriented with a layered abstraction model.
This provides a more structured and reusable design, that can be
easily adapted for new uses.

If YANG was more object-oriented it would be easier to build
and maintain reusable software that used the data models.

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

-  Groupings cannot be augmented

   -  A new grouping can be created with a new name
      but all the related 'uses' statements would need to be
      changed to specify the new grouping name.
   -  Each location where a 'uses' statement expands the grouping
      can have 'augment' statements added to it.

-  Groupings are invariable and apply the same everywhere they are used

   -  There is no way to upgrade or refine a grouping.  Each
      expanded 'uses' statement must be augmented or refined.

-  Groupings cannot reference other groupings other than expanding
   them inline with a 'uses' statement.



YANG is Not Relocatable
-------------------------

YANG is not relocatable.
The path strings for schema nodes or data nodes must be specified from root,
or be relative to the context node determined by various complex rules.
It is not possible to



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


Backward Compatibility Problems
------------------------------------

It is not possible to discover the minimum required revision at a granularity
that is meaningful. A module-level indication is not sufficient and new
mechanisms are needed to help mitigate the problems causes by
non-backward-compatible changes to YANG modules.
