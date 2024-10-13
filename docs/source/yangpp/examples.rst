
.. include:: ../header.txt


YANG++ Examples
==================

Template Example
-----------------

In this example, a bare-bones service template is defined
that has 3 virtual members:

-  reset action
-  status action
-  config container

Example Base Class
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yang

    module base-service {
      // ..

      class base-service {
       virtual {
         // concrete class expected to map these 2 statements
         // and provide names for these actions
         action <reset>;
         action <status>;

         // concrete class expected to fill in this config container
         // as needed and use the provided name 'config'
         container config;
       }
     }

    }



Module Defining a Derived Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yang

    module my-service {
      import base-service { prefix base; }

      class mybase-service {
       parent-class base:base-service {
         map-virtual <reset> {
           map-path my-reset;
         }
         map-virtual <status> {
           map-path my-status;
         }
       }

       // local groupings work the same since the class root
       // is a real container or list node
       grouping status-parms {
          leaf status {
            type string;
          }
          leaf last-error {
            type string;
          }
       }

       // no virtual sections in this class makes it a concrete class
       // a concrete definition for each 'virtual' definition is expected.
       // if missing then a deviate (not-supported) is implied
       action my-reset {
         input {
           leaf myparm1 { type string; }
         }
       }

       action my-status {
         output {
           uses status-parms;
         }
       }

       // this is a replacement of the virtual config
       container config {
         list list1 {
           key name1;
           leaf name1 { type string; }
           leaf my-leaf2 { type string; }
         }
       }
     }


Module Using The Base Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A top-level container name ``/mybase-service`` is created.

.. code-block:: yang

       module example-services {
         // ...
         import base-mod { prefix base; }

         // top-level /mybase-service
         uses-class base:base-service {
           root-name mybase-service;
         }
       }


Objects For Derived Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, the server maps implemented class 'mybase-service' to
the specified (virtual) class 'base-service'.

Real objects created in module 'example-services':

.. code-block:: text

    module: example-services
      +--rw mybase-service
         +---x my-reset
         |  +---w input
         |     +---w myparm1?   string
         +---x my-status
         |  +--ro output
         |     +--ro status?       string
         |     +--ro last-error?   string
         +--rw config
            +--rw list1* [name1]
               +--rw name1       string
               +--rw my-leaf2?   string


Translation to YANG 1.1 Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A YANG 1.1 for the 'services' module is shown for
the mapping to the implemented class 'mybase-service'.

A generic module is not possible in this case since the
specified class is also a virtual class.


.. literalinclude:: example-services.yang
   :language: yang
