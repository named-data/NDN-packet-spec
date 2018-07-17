.. _data:

Data Packet
-----------

NDN Data packet is TLV defined as follows::

    Data ::= DATA-TLV TLV-LENGTH
               Name
               MetaInfo?
               Content?
               Signature

The Data packet represents some arbitrary binary data (held in the optional ``Content`` element) together with its ``Name``, some additional bits of optional information (``MetaInfo``), and a digital ``Signature`` of the other element(s). The Name is the first element since all NDN packet processing starts with the name.  Signature is put at the end of the packet to ease the implementation because signature computation covers all the elements before Signature.

As recommended by :ref:`TLV evolvability guidelines <evolvability>`, unrecognized non-critical TLV elements may appear in the Data packet.
However, they must not appear before the ``Name`` element.

Name
~~~~

See :ref:`Name section <Name>` for details.

.. _MetaInfo:

MetaInfo
~~~~~~~~

::

    MetaInfo ::= META-INFO-TYPE TLV-LENGTH
                   ContentType?
                   FreshnessPeriod?
                   FinalBlockId?

ContentType
+++++++++++

::

    ContentType ::= CONTENT-TYPE-TYPE TLV-LENGTH
                      nonNegativeInteger

The following ContentTypes are currently defined:

+-----------------+-----------------+--------------------------------------------------------------+
| ContentType     | Assigned number | Description of the content                                   |
+=================+=================+==============================================================+
| BLOB            | 0               | payload identified by the data name; this is the default     |
|                 |                 | ContentType                                                  |
+-----------------+-----------------+--------------------------------------------------------------+
| LINK            | 1               | a list of delegations (see :ref:`link`)                      |
+-----------------+-----------------+--------------------------------------------------------------+
| KEY             | 2               | public key                                                   |
+-----------------+-----------------+--------------------------------------------------------------+
| NACK            | 3               | application-level NACK                                       |
+-----------------+-----------------+--------------------------------------------------------------+

Other ContentType numbers are assigned and maintained in `NDN Packet Specification Wiki <https://redmine.named-data.net/projects/ndn-tlv/wiki/ContentType>`__.

.. _FreshnessPeriod:

FreshnessPeriod
+++++++++++++++

::

    FreshnessPeriod ::= FRESHNESS-PERIOD-TLV TLV-LENGTH
                          nonNegativeInteger

The optional ``FreshnessPeriod`` indicates how long a node should wait after the arrival of this data before marking it "non-fresh".
The encoded value is number of milliseconds.
Note that the "non-fresh" data is still valid data; the expiration of ``FreshnessPeriod`` only means that the producer may have produced newer data.

If the Data packet carries a ``FreshnessPeriod`` greater than zero, a node should initially consider it "fresh".  After the Data has resided in the node for ``FreshnessPeriod`` milliseconds, it will be marked as "non-fresh".
If the Data does not have a ``FreshnessPeriod`` or if it has a ``FreshnessPeriod`` equal to zero, it MUST be immediately marked "non-fresh".

If an Interest contains ``MustBeFresh`` element, a node MUST NOT return "non-fresh" Data in response to this Interest.
The effect is the same as if that "non-fresh" Data did not exist (i.e., the Interest might be matched by some other Data in the store, or, failing that, get forwarded to other nodes).
When an exact duplicate of the "non-fresh" Data packet with a positive ``FreshnessPeriod`` value arrives at the node, the node SHOULD re-mark it as "fresh" for the specified duration.

FinalBlockId
++++++++++++

::

    FinalBlockId ::= FINAL-BLOCK-ID-TYPE TLV-LENGTH
                       NameComponent

The optional FinalBlockId identifies the final block in a sequence of fragments.
It should be present in the final block itself, and may also be present in other fragments to provide advanced warning of the end to consumers.
The value here should be equal to the last explicit name component of the final block.


.. _Content:

Content
~~~~~~~

::

    Content ::= CONTENT-TYPE TLV-LENGTH BYTE*

The ``Content`` element can carry any arbitrary sequence of bytes.
