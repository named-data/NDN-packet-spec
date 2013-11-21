Type-Length-Value (TLV) Encoding
--------------------------------

Each NDN packet is encoded in a Type-Length-Value (TLV) format.  NDN Interest and Data packets are distinguished by the type value in the first and outmost TLV\ :sub:`0`\ .

An NDN packet is mainly a collection of TLVs inside TLV\ :sub:`0`\ .  Some TLVs may contain sub-TLVs, and each sub-TLV may also be further nested.  A guiding design principle is to keep the order of TLV\ :sub:`i`\ s deterministic, and keep the level of nesting as small as possible to minimize both processing overhead and chances for errors.

Note that NDN packet format does not have a fixed packet header nor does it encode a protocol version number. Instead the design uses the TLV format to provide the flexibility of adding new types and phasing out old types as the protocol evolves over time.  The absence of a fixed header makes it possible to support packets of very small sizes efficiently, without the header overhead.
There is also no packet fragmentation support at network level.
Whenever needed, NDN packets may be fragmented and reassembled hop-by-hop. [#f1]_

.. [#f1] Today's IP networks provide point-to-point packet delivery and perform end-to-end fragmentation. An NDN network, on the other hand, may fetch requested data from any in-network storage, thus the notion of data flowing along an end-to-end path does not apply.

Variable Size Encoding for type (T) and length (L)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Both the text below and that in :ref:`TLV encoding section <TLV>` are adopted from an earlier packet specification draft by Mark Stapp)

To minimize the overhead during early deployment and to allow flexibility of future protocol extensions to meet unforeseeable needs, both type (T) and length (L) take a variable size format.
For implementation simplicity, both type and length take the same encoding format.

We define a variable-length encoding for numbers in NDN as follows::

     VAR-NUMBER := BYTE+

The first octet of the number either carries the actual numeric value, or signals that a multi-octet encoding is present, as defined below:

- if the first octet is < 253, the number is encoded in that octet;

- if the first octet == 253, the number is encoded in the
  following 2 octets, in net byte-order;

- if the first octet == 254, the number is encoded in the
  following 4 octets, in net byte-order;

- if the first octet == 255, the number is encoded in the
  following 8 octets, in net byte-order.


One-octet value::

     0 1 2 3 4 5 6 7 
    +---------------+
    | < 253 = VALUE |
    +---------------+


Two-octet value::

                         1                   2
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 
    +---------------+---------------+---------------+
    |      253      |  VALUE (MSB)     VALUE (LSB)  |   
    +---------------+---------------+---------------+

Four-octet value::

                         1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------+---------------+----------------+--------------+
    |      254      |  VALUE (MSB)                                  /
    +---------------+---------------+----------------+--------------+
    |  VALUE (LSB)  |
    +---------------+

Eight-octet value::

                         1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------+---------------+----------------+--------------+
    |      255      |  VALUE (MSB)                                  /
    +---------------+                                               +
    |                                                               /
    +               +---------------+----------------+--------------+
    |  VALUE (LSB)  |
    +---------------+


.. _TLV:

TLV Encoding
~~~~~~~~~~~~

TLV encoding for NDN pakcets is defined as follows::

     NDN-TLV := TLV-TYPE TLV-LENGTH TLV-VALUE?
     TLV-TYPE := VAR-NUMBER
     TLV-LENGTH := VAR-NUMBER
     TLV-VALUE := BYTE+


TLV-TYPE SHOULD be unique at all nested levels.
The TLV Type number space and initial assignments will be specified in the later revision of the current document.
NDN packet design will try best to keep the length of T staying with a single byte.

The ``TLV-LENGTH`` value represents number of bytes that ``TLV-VALUE`` uses.
It **does not** include number of bytes that ``TLV-TYPE`` and ``TLV-LENGTH`` fields themselves occupy.
In particular, empty payload TLV will carry ``TLV-LENGTH`` equal to 0.


This encoding offers a reasonable balance between compactness and flexibility.
Most common, standardized Type codes will be allocated from a small-integer number-space, and these common Types will be able to use the compact, single-byte encoding. 

Non Negative Integer Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A number of TLV elements in NDN packet format take a non-negative integer as their value, with the following definition::

    nonNegativeInteger ::= BYTE+

Length value of the TLV element MUST be either 1, 2, 4, or 8.
Depending on the length value, a nonNegativeInteger is encoded as follows:

- if the length is 1 (i.e. the value length is 1 octet), the nonNegativeInteger is encoded in one octet;

- if the length is 2 (= value length is 2 octets), the nonNegativeInteger is encoded in 2 octets, in net byte-order; 

- if the length is 4 (= value length is 4 octets), the nonNegativeInteger is encoded in 4 octets, in net byte-order; 

- if the length is 8 (= value length is 8 octets), the nonNegativeInteger is encoded in 8 octets, in net byte-order. 

The following shows a few examples of TLVs that has nonNegativeInteger as their value component in hexadecimal format (where ``TT`` represents ``TLV-TYPE``, followed by the ``TLV-LENGTH``, then ``TLV-VALUE``)::

    0     => TT0100
    1     => TT0101
    255   => TT01FF
    256   => TT020100
    65535 => TT02FFFF
    65536 => TT0400010000


Changes from CCNx
~~~~~~~~~~~~~~~~~

- XML-based ccnb packet encoding is replaced by TLV encoding.
