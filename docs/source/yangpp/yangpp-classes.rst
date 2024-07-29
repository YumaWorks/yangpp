
.. include:: ../header.txt


YANG++ Classes
==================

A YANG++ class is an abstract modeling component, like the 'grouping'.
However it is much more structured and powerful than a grouping.




class-stmt
------------------

A YANG Class is a set of abstract definitions like a grouping.
The **class** statement is used like a grouping.
It must be used somewhere in the schema tree to create accessible schema nodes,
with the :ref:`uses-class-stmt`.

The :ref:`base-class-stmt` or :ref:`parent-class-stmt` must be present,
but not both.


**class-stmt Substatements**

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  deprecated
     -  :ref:`deprecated-stmt`
     -  0..1

   * -  requires
     -  :ref:`requires-stmt`
     -  0..1

   * -  presence
     -  :rfc:`7950#section-7.5.5`
     -  0..1

   * -  base-class
     -  :ref:`base-class-stmt`
     -  0..1

   * -  parent-class
     -  :ref:`parent-class-stmt`
     -  0..1

   * -  virtual
     -  :ref:`virtual-stmt`
     -  0..n

   * -  typedef
     -  :rfc:`7950#section-7.3`
     -  0..n

   * -  grouping
     -  :rfc:`7950#section-7.12`
     -  0..n

   * -  data-def-stmt
     -  Several
     -  0..n

   * -  any
     -  :ref:`any-stmt`
     -  0..n

   * -  action
     -  :rfc:`7950#section-7.15`
     -  0..n

   * -  notification
     -  :rfc:`7950#section-7.16`
     -  0..n

   * -  status
     -  :rfc:`7950#section-7.21.2`
     -  0..1

   * -  description
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  reference
     -  :rfc:`7950#section-7.21.4`
     -  0..1


The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    class-stmt = class-keyword sep identifier-arg-str optsep
                 "{" stmtsep
                     ;; these stmts can appear in any order
                     [deprecated-stmt]
                     [requires-stmt]
                     [presence-stmt]
                     [base-class-stmt / parent-class-stmt]
                     *virtual-stmt
                     *(typedef-stmt / grouping-stmt)
                     *(data-def-stmt / any-stmt)
                     *action-stmt
                     *notification-stmt
                     [status-stmt]
                     [description-stmt]
                     [reference-stmt]
                "}") stmtsep




deprecated-stmt
~~~~~~~~~~~~~~~~

This statement MUST be present if the status of the class is ``deprecated``.
It contains information to alert users to the possible removal of the class
in the future.

-  The 'description' statment SHOULD be present and contain information
   about when the class is expected to change status to 'obsolete'.


**deprecated-stmt Substatements**


.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * -  substatement
     -  section
     -  cardinality

   * -  replaced-by-stmt
     -  :ref:`replaced-by-stmt`
     -  0..n

   * -  error-message
     - :rfc:`7950#section-7.5.4.1`
     -  0..1

   * -  error-app-tag
     - :rfc:`7950#section-7.5.4.2`
     -  0..1


   * -  description-stmt
     -  :rfc:`7950#section-7.21.3`
     -  0..1

   * -  reference-stmt
     -  :rfc:`7950#section-7.21.4`
     -  0..1




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
   :emphasize-lines: 3 - 7

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
-  Multiple replaced-by statments can be listed.


The following ABNF is added to the YANG syntax:

.. code-block:: abnf

    replaced-by-stmt    = replaced-by-keyword sep replaced-by-arg-str stmtend

    replaced-by-arg-str = < a string that matches the rule >
                          < identifier-ref-arg >


Example:

.. code-block:: yang
   :emphasize-lines: 4

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





requires-stmt
~~~~~~~~~~~~~~~~~~~~~~

The 'requires' statement is used to declare external dependency information
for the class.




any-stmt
~~~~~~~~~~~~

The 'any' statement is used to provide abstract nodes with are not named.

-  This allows templates to be constructed.
-  Does not represent a real schema node with a specific name like 'anydata'.
-  Less specific than a virtual node and can include more than data nodes.

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
                      detadef-keyword /
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
   :emphasize-lines: 4

    class config {
        base-class root;
        description
          "An instance of this class represents a conceptual datastore root.";
    }


The :ref:`uses-class-stmt` can be used anywhere a 'uses-stmt' can be used,

.. code-block:: yang
   :emphasize-lines: 3

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



message base-class
+++++++++++++++++++++++++++

This class represents a protocol message.
It it similar to the 'structure' base-class but the indended use
is for some sort of protocol message.


structure base-class
++++++++++++++++++++++++++++

This class represents an abstract data structure.
It corresponds to the 'sx:structure' schema node.
An instance of this class has the same properties as an sx:structure.







parent-class-stmt
~~~~~~~~~~~~~~~~~~~~~~~~~~

This statement is required if the class is not a base class.
It identifies the class to use and also maps any keys and
virtual objects.

-  There must be a 'map-key' substatement for each key that is inherited
   from the parent class.

-  There must be a 'map-virtual' substatement for each mandatory
   virtual object inherited from the parent class

-  There will be is a 'map-virtual' substatement for each implemented
   optional virtual object inherited from the parent class

-  The 'map-path' syntax is TBD. Probably the same as 'path-stmt'.
   It is a schema path string where the root is class root.


### Example of Name Mapping

Class Hierarchy:

.. code-block:: text

    event -> system-event -> my-system-event

    event -> system-event -> my-system-event -> my-system-event2

Object Name Derivation:

.. code-block:: text

    <event> -> <system-event> -> my-event


Example Base Class:

.. code-block:: text

    class event {
       base-class object;
       virtual mandatory {
         notification <event>;
       }
       // ...
    }



Example Parent Class:


.. code-block:: text


    class system-event {
       parent-class event {
         map-virtual event {
           map-path /system-event;
         }
       }

       // this is a replacement of the virtual 'event'
       virtual mandatory {
          notification <system-event> {
             leaf event-type { type string; }
          }
       }
    }



Example Derived Class:

.. code-block:: text

    class my-system-event {
       parent-class system-event {
         map-virtual system-event {
           map-path /my-event;
         }
       }

       // this is a replacement of the virtual 'system-event'
       notification my-event {
         // leaf event-type is inherited from system-event class
         leaf my-data { type string; }
       }
    }


To create a class instance:

.. code-block:: text

    uses-class system-event;


If there is a uses-class in the root directory
then the data nodes visible to the client if
the 'my-system-event' class is used in the server:


.. code-block:: text

    container my-system-event {
       notification my-event {
         leaf event-type { type string; }
         leaf my-data { type string; }
       }
    }



Example Extra Derived Class:

-  A new version of the event type is created that adds a leaf

.. code-block:: text

    class my-system-event2 {
       parent-class my-system-event;
       augment /my-event {
         // leaf event-type is inherited from system-event class
         leaf my-extra-data { type string; }
       }
    }



If there is a uses-class in the root directory
then the data nodes visible to the client if
the 'my-system-event2' class is used in the server:

.. code-block:: yang

    container my-system-event {
       notification my-event {
         leaf event-type { type string; }
         leaf my-data { type string; }
         leaf my-extra-data { type string; }
       }
    }






virtual-stmt
~~~~~~~~~~~~~~~~~

The virtual-stmt is used to declare virtual objects in the class.

If any virtual objects are declared then the class
cannot be instantiated.  A derived class that does not contain
and virtual objects must be used to create an instance
of the class.

The virtual-stmt is followed by the REQUIRED field.

-  Multiple virtual-stmt are allowed by no duplicate objects
   can appear in any way.

The following values are defined:

- mandatory: the virtual objects must be mapped. The datastore is
  invalid if there are any unmapped mandatory virtual objects.

- optional:the virtual objects are not present if not mapped.
  This is similar to a false 'when-stmt' that removes a node
  from the schema tree.

Example:

.. code-block:: text

    virtual mandatory {
      // derived class must map these statements
      rpc reset;

      list list1 {
        key name1;
        leaf name1 { type string; }
        // ...
      }
    }

    virtual optional {
      // derived class may map these statements
      rpc restart;
    }







uses-class-stmt
---------------------




YANG++ Class Examples
-----------------------

.. code-block:: text

      class NAME {

        // standard fields: status, description, reference
        // standard fields: if-feature, when-stmt, must-stmt

        parent-class NAME {
          map-virtual NAME {
            // must be a top-level action, notification, or object
            // that matches the virtual with the same name in
            // the parent class
            map-path PATH;
          }

        }

        // if virtual objects in this class then must have
        // a derived class to use an instance of the class
        // REQUIRED = mandatory or optional
        virtual REQUIRED {
           action-stmt | notification-stmt | data-def-stmt
        }

        // action-stmt | notification-stmt | data-def-stmt

        uses-class NAME {
           // works like a regular uses-stmt
           // TBD: refine-class-stmt
        }

      }



**Example Base Class:**

.. code-block:: text

    module base-mod {
      // ..

      class base1 {
       requires {
          require-module foo-base {
            min-revision 2020-01-01;
          }
       }

       virtual mandatory {
         // derived class must map these statements
         rpc reset;

         list list1 {
           key name1;
           leaf name1 { type string; }
           // ...
         }
       }

       virtual optional {
         // derived class may map these statements
         rpc restart;
       }

       // this is a concrete list part of the base class
       // and not replaced because it is not virtual
       list list2 {
         key name2;
         leaf name2 { type string; }
         // ...
       }
     }

    }



**Example Derived Class:**

.. code-block:: text

    module mybase-mod {
      import base-mod { prefix base; }

      // a class
      class mybase1 {
       parent-class base:base1 {
         map-key name {
           map-path /my-list/my-name;
         }
         map-virtual reset1 {
           map-path /my-reset;
         }
         map-virtual restart {
           map-path /my-restart;
         }
         map-virtual list1 {
           map-path /my-list1;
         }
       }

       // no instance or empty instance-stmt in a derived class
       // means no added keys to the parent class
       instance;

       // no virtual sections in this class makes it a concrete class


       // this is a replacement of the virtual rpc reset
       rpc my-reset {
       }

       // this is a replacement of the virtual rpc reset
       rpc my-restart {
         input {
           leaf test-mode {
             type boolean;
             default false;
           }
         }
       }

       // this is a replacement of the virtual list list1
       list my-list1 {
         key my-name;
         leaf my-name { type string; }
         // ...
       }

        // list list2 is also present in an instance of this class
        augment "/list2" {
          leaf myleaf { type int8; }
        }
     }


**Example Concrete Module:**

.. code-block:: text

       module base1-real {
         // ...
         import base-mod { prefix myb; }

         // top-level /base1
         uses-class myb:base1;
       }

Server YANG Library Mapping

-  For each module that contains implemented classes,
   a class entry is required in the yang-library update

-  Maps real-class to lib-class

.. code-block:: text

      classes {
        class [lib-class] {
          lib-class /base-mod:base1
          real-class /mybase-mod:mybase1
        }
      }
      modules {
       module base1-real;
     }
     imported-modules {
       module base-mod;
       module mybase-mod;
     }



Virtual objects created:

- action /base1[name]/reset       mapped to mybase1::my-reset
- action /base1[name]/restart     mapped to mybase1::my-restart
- list   /base1[name]/list1       mapped to mybase1::my-list1
- list   /base1[name]/list2       mapped to base1::list2

Real objects created:

- action /base1[name]/my-reset
- action /base1[name]/my-restart
- list   /base1[name]/my-list1
- list   /base1[name]/list2
