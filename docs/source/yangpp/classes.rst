
.. include:: ../header.txt


YANG++ Classes
==================

A YANG++ class is an abstract modeling component, like the YANG 'grouping'.
However it is much more structured and powerful than a grouping.




class-stmt
------------------

A YANG Class is a set of abstract definitions like a grouping.
The **class** statement is used like a grouping.
It must be used somewhere in the schema tree to create accessible schema nodes,
with the :ref:`uses-class-stmt`.


**Usage**

-  The :ref:`base-class-stmt` or :ref:`parent-class-stmt` can be present,
   but not both.

-   A :ref:`classref-stmt` must be present for each external class
    reference done within the class being defined.
-   A special path syntax identifying the reference point is used in
    these statements:

    - must-stmt
    - when-stmt
    - path-stmt


**class-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  any
     -  :ref:`any-stmt`
     -  0..n

   * -  action
     -  :rfc:`7950#section-7.15`
     -  0..n

   * -  autokey
     -  :ref:`autokey-stmt`
     -  0..1

   * -  base-class
     -  :ref:`base-class-stmt`
     -  0..1

   * -  classref
     -  :ref:`classref-stmt`
     -  0..N

   * -  data-def-stmt
     -  Several
     -  0..n

   * -  deprecated
     -  :ref:`deprecated-stmt`
     -  0..1

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  grouping
     -  :rfc:`7950#section-7.12`
     -  0..n

   * -  if-feature
     -  :rfc:`7950#section-7.20.2`
     -  0..n

   * -  key
     -  :rfc:`7950#section-7.8.2`
     -  0..1

   * -  max-elements
     -  :rfc:`7950#section-7.7.6`
     -  0..1 (if list type)

   * -  min-elements
     -  :rfc:`7950#section-7.7.5`
     -  0..1 (if list type)

   * -  must..n
     -  :rfc:`7950#section-7.5.3`
     -  0..1

   * -  notification
     -  :rfc:`7950#section-7.16`
     -  0..n

   * -  ordered-by
     -  :rfc:`7950#section-7.7.7`
     -  0..1 (if list type)

   * -  parent-class
     -  :ref:`parent-class-stmt`
     -  0..1

   * -  presence
     -  :rfc:`7950#section-7.5.5`
     -  0..1

   * -  reference
     -  :rfc:`7950#section-7.21.4`
     -  0..1

   * -  status
     -  :rfc:`7950#section-7.21.2`
     -  0..1

   * -  typedef
     -  :rfc:`7950#section-7.3`
     -  0..n

   * -  virtual
     -  :ref:`virtual-stmt`
     -  0..n

   * -  when
     -  :rfc:`7950#section-7.21.5`
     -  0..1




The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    class-stmt = class-keyword sep identifier-arg-str optsep
                 "{" stmtsep
                     ;; these stmts can appear in any order
                     [deprecated-stmt]
                     [presence-stmt / key-stmt / autokey-stmt]
                     [base-class-stmt / parent-class-stmt]
                     *virtual-stmt
                     *classref-stmt
                     *(typedef-stmt / grouping-stmt)
                     *(data-def-stmt / any-stmt)
                     *action-stmt
                     *notification-stmt
                     [max-elements-stmt]
                     [min-elements-stmt]
                     [must-stmt]
                     [when-stmt]
                     [ordered-by-stmt]
                     [status-stmt]
                     [description-stmt]
                     [reference-stmt]
                "}") stmtsep




deprecated-stmt
~~~~~~~~~~~~~~~~

This statement MUST be present if the status of the class is ``deprecated``.
It contains information to alert users to the possible removal of the class
in the future.

-  The 'description' statement SHOULD be present and contain information
   about when the class is expected to change status to 'obsolete'.


**deprecated-stmt Substatements**


.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  error-app-tag
     - :rfc:`7950#section-7.5.4.2`
     -  0..1

   * -  error-message
     - :rfc:`7950#section-7.5.4.1`
     -  0..1

   * -  reference
     -  :rfc:`7950#section-7.21.4`
     -  0..1

   * -  replaced-by
     -  :ref:`replaced-by-stmt`
     -  0..n





The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    deprecated-stmt = deprecated-keyword optsep
                      (";" /
                       "{" stmtsep
                           ;; these stmts can appear in any order
                           *replaced-by-stmt
                           [error-message-stmt]
                           [error-app-tag-stmt]
                           [description-stmt]
                           [reference-stmt]
                       "}") stmtsep


The following example show a class that is now deprecated.

.. code-block:: yang

    class my-message {
      base-class message;
      deprecated {
        replaced-by "newmsg:new-message";
        description
          "This message header is no longer used since version 3.1.0";
      }
      leaf id { type string; }
      status deprecated;
    }



replaced-by-stmt
++++++++++++++++++++


This statement is used to identify a replacement class for the deprecated class.
It MAY be used if a replacement class is available.

The 'replaced-by-arg-str' string identifies the module and class name
of a replacement class.

-  The replacement SHOULD have a status of 'current'.
-  Multiple replaced-by statements can be listed.


The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    replaced-by-stmt    = replaced-by-keyword sep replaced-by-arg-str stmtend

    replaced-by-arg-str = < a string that matches the rule >
                          < identifier-ref-arg >


Example:

.. code-block:: yang

    class my-message {
      base-class message;
      deprecated {
        replaced-by "newmsg:new-message";
        description
          "This message header is no longer used since version 3.1.0";
      }
      leaf id { type string; }
      status deprecated;
    }





any-stmt
~~~~~~~~~~~~

The 'any' statement is used to provide abstract nodes with are not named.

-  This allows templates to be constructed.
-  Does not represent a real schema node with a specific name like 'anydata'.
-  Less specific than a virtual node and can include more than data nodes.
-  Shares the same namespace as objects and notifications.

**Supported abstract statements**

For :ref:`object base-class` the following values of 'any-arg-str' are allowed:

-  action
-  datadef
-  notification

For all other :ref:`class types` the following values of 'any-arg-str' are allowed:

-  action
-  datadef
-  notification
-  rpc



**any-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  if-feature-stmt
     -  :rfc:`7950#section-7.20.2`
     -  0..n

   * -  mandatory-stmt
     -  :rfc:`7950#section-7.20.2`
     -  0..n

   * -  status-stmt
     -  :rfc:`7950#section-7.21.2`
     -  0..1

   * -  description-stmt
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  reference-stmt
     -  :rfc:`7950#section-7.21.4`
     -  0..1



The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    any-stmt = any-keyword sep any-type-arg-str optsep
               (";" /
                "{" stmtsep
                    ;; these stmts can appear in any order
                    *if-feature-stmt
                    [mandatory-stmt]
                    [status-stmt]
                    [description-stmt]
                    [reference-stmt]
                "}") stmtsep

   any-arg-str      = < a string that matches the rule >
                      < any-arg >

   any-arg          = action-keyword /
                      datadef-keyword /
                      notification-keyword /
                      rpc-keyword

   datadef-keyword  = %s"datadef"


**Example: Notification header**

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



**Example: Extending the Notification Header**


.. code-block:: yang

    class push-notification {
      parent-class notification;

      leaf sysName {
        type string;
        mandatory true;
        description
          "System name of the server generating the notification.";
      }

      leaf observation-time {
        type yang:date-and-time;
        mandatory true;
        description
          "Timestamp when the Push event was observed by the publisher.";
      }

      leaf collector-id {
        type uint32;
        mandatory true;
        description
          "Collector ID for this Push notification.";
      }

      leaf sequence-id {
        type string;
        mandatory true;
        description
          "Sequence ID for this Push notification";
      }
    }


autokey-stmt
~~~~~~~~~~~~~~

The 'autokey' statement is used to create a class or a list
with an automatically generated and maintained key leaf.

.. code-block:: yang

    list shopping-list {
      autokey;
      leaf item { type string; }
      leaf quantity { type uint32; }
    }

There are many use-cases where the list key does not contain any
semantics other than being a unique identifier.

-  In this mode, the designer does not want to define or implement the list key management.
-  The client does not want to provide a new unique list key by first locking the config
   and retrieving all existing entries to find an unused entry
-  **The current protocol operations do not fully support this feature and need improvements**
-  The key is a uint32 number from 1 .. max
-  The key is a plain leaf as required for a key leaf
-  The value 0 is reserved for indicate no key
-  TBD: Maybe not allowed for ordered-by user, or no insert operation allowed for create
-  TBD: list syntax is expected to change to support autokey, not just the class key.

.. code-block:: yang

    leaf _id_ {
      type uint32;
    }

Issues:

-  The autokey is un-named so it does not conflict with any siblings, or could
   use reserved name like "_id_".
-  The key name needs to be known by the client and be visible in retrievals

This is not the same as position-based (no key-stmt at all) because autokey does not renumber for any reason
The server assigns an unused value for the ID and the protocol operation enhancements allow this operation and convey the assigned ID to the client


base-class-stmt
~~~~~~~~~~~~~~~~~~

This statement defines the standard properties of a base class.
There is a registry of standard base classes.

The following values are supported:

-  :ref:`root base-class`
-  :ref:`object base-class`
-  :ref:`message base-class`
-  :ref:`structure base-class`




root base-class
+++++++++++++++++++

This class represents a datastore root.

.. container::

   .. note::

      -  The content is derived from the YANG library associated with the data.
      -  Content SHOULD NOT be defined for this base-class.
      -  If any content is present then its purpose is undefined by YANG++.


**Example: <config> element Class**

This simple construct represents a '<config>' parameter that
is expected to contain top-level objects as child data nodes .


The class must be declared:

.. code-block:: yang

    class config {
        base-class root;
        description
          "An instance of this class represents a conceptual datastore root.";
    }


The :ref:`uses-class-stmt` can be used anywhere a 'uses-stmt' can be used,

.. code-block:: yang

    rpc edit-data {
      input {
        uses-class config;
      }
    }




object base-class
++++++++++++++++++++

A class using this base type represents a conventional YANG object.
An instance of this class has the same properties as a container.

If the base-class statement is not present and no :ref:`parent-class-stmt`
is present, then this is the default base-class type used.

A class definition defines a node in the schema tree,
unlike a YANG 1.1 grouping.

.. code-block:: yang

    grouping data {
       leaf leaf1 { type string; }
       leaf leaf2 { type string; }
    }

    class data {
       leaf leaf1 { type string; }
       leaf leaf2 { type string; }
    }

    /* produces paths
     *    ./leaf1
     *    ./leaf2
     */
    uses data;

    /* produces paths
     *    ./data/leaf1
     *    ./data/leaf2
     */
    uses-class data;



message base-class
+++++++++++++++++++++++++++

This class represents a protocol message.
It it similar to the 'structure' base-class but the intended use
is for some sort of protocol message.

-  An instance of this class has the same properties as an sx:structure.

-  A protocol specification is expected to define any semantics
   and usage context associated with this class.


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



structure base-class
++++++++++++++++++++++++++++

This class represents an abstract data structure.
It corresponds to the 'sx:structure' schema node.

-  An instance of this class has the same properties as an sx:structure.
-  There are no semantics or usage context defined for this class


.. code-block:: yang

    class timestamp {
      base-class structure;

      leaf event-time {
        type yang:date-and-time;
      }
      leaf event-id {
        type string;
      }
    }






parent-class-stmt
~~~~~~~~~~~~~~~~~~~~~~~~~~

This statement is required if the class is not a base class.
It identifies the class to use and also maps any virtual objects.
There SHOULD be a 'map-virtual' substatement for each
virtual object inherited from the parent class

If the parent class is imported from a different module,
then the 'min-revision' statement SHOULD be used
if this class relies on definitions not present in the first
revision of the imported module.

The contents of the parent class are inherited, as if it
was a grouping.  The 'refine' statement is used to
modify any schema nodes allowed by the 'refine' statement.


**Example: Change the mandatory-stmt**

Sample parent class:

.. code-block:: yang

    class udp-client {
      uses udp-client-grouping;
    }


Sample Derived class using 'refine' to change remote-port:

.. code-block:: yang

    class udp-notif-client {
      parent-class udp-client {
        refine remote-port {
          mandatory true;
        }
      }
    }


If any inherited definitions in the class being defined
deviate from the parent class definitions then
the 'deviation' statement is used to specify the differences.
Often groupings are 'almost' reusable and the 'refine' statement
cannot make the same changes as a deviation.

In YANG++ deviations are allowed inline in the class definition
and not always considered as defects or lack of conformance. They are
used to adapt the parent class for new requirements.

**Example: Remove unused leafs from the parent class**

Sample Derived class using 'deviation' to remove
the 'local-address' and 'local-port' leafs:

.. code-block:: yang

    class example-client {
      parent-class udp-client {
        deviation local-address {
          deviate not-supported;
        }
        deviation local-port {
          deviate not-supported;
        }
      }
    }


**parent-class-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  deviation
     -  :rfc:`7950#section-7.20.3`
     -  0..n

   * -  map-virtual
     -  :ref:`map-virtual-stmt`
     -  0..n

   * -  min-revision
     -  TBD
     -  0..1


   * -  reference-stmt
     -  :rfc:`7950#section-7.21.4`
     -  0..1

   * -  refine
     -  :rfc:`7950#section-7.13.2`
     -  0..n


The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    parent-class-stmt   = parent-class-keyword sep identifier-arg-str optsep
                         (";" /
                          "{" stmtsep
                              ;; these stmts can appear in any order
                              *map-virtual-stmt
                              [min-revision-stmt]
                              [description-stmt]
                              [reference-stmt]
                              *deviation-stmt
                              *refine-stmt
                          "}") stmtsep



**Example: Adding leafs with a derived class**

The 'address' class represents one generic address:

.. code-block:: yang

    class address {
      leaf last-name {
        type string;
        description
          "Last name of the person who is associated with this address";
      }
      leaf first-name {
        type string;
        description
          "First name of the person who is associated with this address";
      }
      leaf street {
        type string;
        description "street address";
      }
      leaf city {
        type string;
        description "City address";
      }
    }


The 'us-address' class has all the leafs as the parent class
plus a zipcode, ordered after the last parent child node.

.. code-block:: yang

    class us-address {
      parent-class address;

      leaf zipcode {
        type string { length "5 | 10"; }
        description "zipcode";
      }
    }


When the 'address' class is used with a :ref:`uses-class-stmt` statement
the server MAY implement the 'address' class or any class that is derived
from this class.

**Example: Make an address list class**

The 'us-address-list' class is a list using the existing leafs in
the 'us-address' class

-  This class cannot be used with a :ref:`uses-class-stmt` unless the specified
   class has a 'key' statement that matches the implemented class.

.. code-block:: yang

    class us-address-list {
      parent-class us-address;
      key "last-name first-name";
    }



map-virtual-stmt
+++++++++++++++++

The 'map-virtual' statement is used to bind a virtual definition
from the parent class to a concrete or virtual definition in the
class being defined.

-  The 'map-virtual' identifier-arg-str value from the parent class
   is mapped to the identifier in the class being defined.

-  If a virtual identifier from the parent class is not mapped, then it is not
   removed from the class being defined.  Another derived class could
   support the virtual node.

**Example: Map Virtual Actions to New Virtual Actions**

A virtual node must be mapped to a concrete node to be usable
in the schema tree. However, a derived class is also allowed
to modify virtual nodes from the parent class to create new
virtual nodes.


.. code-block:: yang

    class base-test {
      virtual {
        action <un-named-test>;
        action named-test;
      }
    }

    class test1-template {
      parent-class base-test {
        map-virtual un-named-test {
          map-path my-base-test;
       }
      }

      virtual {
        // un-named-test modified and still un-named
        action <my-base-test> {
          input {
            leaf id { type uint16; }
          }
        }

        // named-test is still virtual
        action named-test {
          input {
            leaf id { type uint16; }
          }
        }
      }
    }



**map-virtual-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  map-path
     -  :ref:`map-path-stmt`
     -  1


The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    map-virtual-stmt   = map-virtual-keyword sep identifier-arg-str optsep
                         "{" stmtsep
                             map-path-stmt
                         "}" stmtsep


map-path-stmt
%%%%%%%%%%%%%%%%%%%%


The 'map-path' statement is used to bind a virtual definition
from the parent class to a concrete or virtual definition in the
class being defined.


.. code-block:: abnf

    map-path-stmt    = map-path-keyword sep map-path-arg-str stmtend

    map-path-arg-str = < a string that matches the rule >
                        < identifier-ref-arg / "<" identifier-arg-str ">" >



virtual-stmt
~~~~~~~~~~~~~~~~~

The virtual-stmt is used to declare virtual objects in the class.

If any virtual objects are declared then the class
cannot be instantiated.  A derived class that does not contain
and virtual objects must be used to create an instance
of the class.

The virtual-stmt is not followed by any keyword.

-  Multiple virtual-stmt are allowed but no duplicate objects
   can appear in any way.


.. code-block:: yang

       virtual {
         // concrete class expected to map these statements
         action <reset> {
           description
             "Some sort of reset action is expected";
         }

         list list1 {
           key name1;
           leaf name1 { type string; }
         }
       }



**Virtual Node Name Placeholders**


If the identifier value for the sub-statement is wrapped,
then it is a name placeholder and a derived class that
creates a concrete version must provide a :ref:`map-virtual-stmt`
to assign a real name.


.. code-block:: text

    '<' identifier '>'

Example:

.. code-block:: yang

     virtual {
        action <reset>;
     }


**virtual-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  action
     -  :rfc:`7950#section-7.15`
     -  0..n

   * -  container
     -  :rfc:`7950#section-7.5`
     -  0..n

   * -  choice
     -  :rfc:`7950#section-7.9`
     -  0..n

   * -  leaf
     -  :rfc:`7950#section-7.6`
     -  0..n

   * -  leaf-list
     -  :rfc:`7950#section-7.7`
     -  0..n

   * -  list
     -  :rfc:`7950#section-7.8`
     -  0..n

   * -  notification
     -  :rfc:`7950#section-7.16`
     -  0..n



.. code-block:: abnf

    virtual-stmt = virtual-keyword optsep
                     "{" stmtsep
                         ;; these stmts can appear in any order
                         1*(container-stmt /
                            leaf-stmt /
                            leaf-list-stmt /
                            list-stmt /
                            choice-stmt /
                            action-stmt /
                            notification-stmt)
                     "}" stmtsep








classref-stmt
~~~~~~~~~~~~~~~~~~~~~~~~~~

This statement is required if the class references any other classes.
Referencing a class does not alter the schema tree like using a class
with :ref:`uses-class-stmt`.

Class references can be used instead of absolute or relative schema tree
references:

- path-stmt
- when-stmt
- must-stmt

Since a class can be used in multiple objects, a reference point
is needed to identify each usage within the class being defined.
Each 'classref' statement defines a reference point.
The :ref:`class path string` is used to declare a reference point.



**classref-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  if-feature-stmt
     -  :rfc:`7950#section-7.20.2`
     -  0..n

   * -  reference-stmt
     -  :rfc:`7950#section-7.21.4`
     -  0..1



The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    classref-stmt   = classref-keyword sep identifier-arg-str optsep
                      (";" /
                       "{" stmtsep
                            ;; these stmts can appear in any order
                            *if-feature-stmt
                            [description-stmt]
                            [reference-stmt]
                        "}" ) stmtsep







uses-class-stmt
---------------------

This statement is similar to the YANG 'uses' statement, which conceptually
expands a grouping in place of the 'uses' node in the schema tree.
A class is conceptually expanded in the schema tree instead of a grouping.

.. code-block:: yang

    container system {
      uses-class address;
    }

The following schema nodes are created by the uses-class statement.

.. code-block:: text

    +--rw system
       +--rw address
          +--rw last-name     string
          +--rw first-name    string
          +--rw street?       string
          +--rw city?         string
          +--rw zipcode?      string




**Nested use-class**

If this statement appears within a class definition, then it
is a 'nested use-class' and the class binding information
is not required.

**Final use-class**

If this statement appears as a plain 'data-def-stmt'
then it is a 'final use-class' and the class binding information
is required.

A :ref:`bind-classref-stmt` is needed for all classes
referenced in the class being used in
:ref:`Class Path String` sub-statements
within the class.


**uses-class-stmt Substatements**


.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  augment
     -  :rfc:`7950#section-7.17`
     -  0..n

   * -  bind-classref
     -  :ref:`bind-classref-stmt`
     -  0..n

   * -  root-name
     -  :ref:`root-name-stmt`
     -  0..1

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  deviation
     -  :rfc:`7950#section-7.20.3`
     -  0..n

   * -  if-feature
     -  :rfc:`7950#section-7.20.2d`
     -  0..n

   * -  reference
     -  :rfc:`7950#section-7.21.4`
     -  0..1

   * -  refine
     -  :rfc:`7950#section-7.13.2`
     -  0..n

   * -  status-stmt
     -  :rfc:`7950#section-7.21.2`
     -  0..1

   * -  when-stmt
     -  :rfc:`7950#section-7.21.5`
     -  0..1


.. code-block:: abnf


        uses-class-stmt = uses-class-keyword sep identifier-ref-arg-str optsep
               (";" /
                "{" stmtsep
                    ;; these stmts can appear in any order
                    [root-name-stmt]
                    *bind-classref-stmt
                    [when-stmt]
                    *if-feature-stmt
                    [status-stmt]
                    [description-stmt]
                    [reference-stmt]
                    *refine-stmt
                    *deviation-stmt
                    *uses-augment-stmt
                 "}") stmtsep


root-name-stmt
~~~~~~~~~~~~~~~~~~~

This statement is used to change the schema node name of the class root.
Normally this is the same as the name of the specified class.
A name can be specified instead, which allows customization and
the ability to use the same class more than once as sibling nodes.

**Example: Envelope with from-address and to-address sub-trees.**

.. code-block:: yang

    class envelope {
      uses-class address {
        root-name from-address;
      }
      uses-class address {
        root-name to-address;
      }
    }


bind-classref-stmt
~~~~~~~~~~~~~~~~~~~~~

This statement is used to bind a relative schema node reference
in a :ref:`class path string`.  A 'final use-class' must provide
this information so all path referenced can be resolved within
the real schema tree.

-  A corresponding :ref:`classref-stmt` must be found in the
   class being used, or the binding cannot be completed.


.. container::

   .. note::

      -  The :ref:`uses-class-stmt` can only safely provide refpoint
         bindings for the specified class, not the implemented class
      -  TBD: Additional or changed 'bind-classref' definitions
         in a different implemented class need to be handled somehow.
      -  TBD: Need to automatically-as-possible handle bindings
         for nested classref


**bind-classref-stmt Substatements**


.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  path
     -  :rfc:`7950#section-9.9.2`
     -  1

   * -  reference
     -  :rfc:`7950#section-7.21.4`
     -  0..1



.. code-block:: abnf

    bind-classref-stmt   = bind-classref-keyword sep identifier-arg-str optsep
                        "{" stmtsep
                            ;; these stmts can appear in any order
                            path-stmt
                            [description-stmt]
                            [reference-stmt]
                        "}" stmtsep



**Example: Leafref to capabilities needs to be resolved**

The 'push-caps' class is setup by the system:

.. code-block:: yang

    class push-caps {
      leaf min-interval {
        type uint32;
        units centiseconds;
      }
      leaf max-segment-size {
        type uint32;
        units bytes;
      }
    }

The class is used within a container named 'system'.
The class root name is 'push-capabilities'.

.. code-block:: yang

    container system {
      uses-class push-caps {
        root-name "push-capabilities";
      }
    }

Assume another class called 'push-settings' is defined
that validates fields against the push capabilities.


.. code-block:: yang

    class push-settings {
      classref "sys:push-caps::syscaps" {
        description "System capabilities to use";
      }

      leaf min-interval {
        type uint32;
        units centiseconds;
        must ". >= /sys:push-caps::syscaps/min-interval";
      }
      leaf max-segment-size {
        type uint32;
        units bytes;
        must ". <= /sys:push-caps::syscaps/max-segment-size";
      }
    }

In order to use the 'push-settings' class in a final uses-class,
a 'bind-class' statement must be provided:

-  The 'path' is a plain schema-path string and identifies schema nodes.
   The schema node name is 'push-capabilities' in this case.

.. code-block:: yang

    container settings {
      uses-class push-settings {
        bind-classref sys:push-caps::syscaps {
          path "/sys:system/sys:push-capabilities";
        }
      }
    }
