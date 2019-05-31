Type-Length-Value (TLV) Encoding
--------------------------------

Each NDN packet is encoded in a Type-Length-Value (TLV) format.  NDN Interest and Data packets are distinguished by the type number in the first and outmost TLV\ :sub:`0`\ .

An NDN packet is mainly a collection of TLVs inside TLV\ :sub:`0`\ .  Some TLVs may contain sub-TLVs, and each sub-TLV may also be further nested.  A guiding design principle is to keep the order of TLV\ :sub:`i`\ s deterministic, and keep the level of nesting as small as possible to minimize both processing overhead and chances for errors.

Note that NDN packet format does not have a fixed packet header nor does it encode a protocol version number. Instead the design uses the TLV format to provide the flexibility of adding new types and phasing out old types as the protocol evolves over time.  The absence of a fixed header makes it possible to support packets of very small sizes efficiently, without the header overhead.
There is also no packet fragmentation support at network level.
Whenever needed, NDN packets may be fragmented and reassembled hop-by-hop. [#f1]_

.. [#f1] `"Packet Fragmentation in NDN: Why NDN Uses Hop-By-Hop Fragmentation (NDN Memo)" by A. Afanasyev, J. Shi, L. Wang, B. Zhang, and L. Zhang., NDN Memo, Technical Report NDN-0032 <http://named-data.net/publications/techreports/ndn-0032-1-ndn-memo-fragmentation/>`__

Variable Size Encoding for type (T) and length (L)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Both the text below and that in :ref:`TLV encoding section <TLV>` are adopted from an earlier packet specification draft by Mark Stapp)

To minimize the overhead during early deployment and to allow flexibility of future protocol extensions to meet unforeseeable needs, both type (T) and length (L) take a variable size format.
For implementation simplicity, both type and length take the same encoding format.

We define a variable-length encoding for numbers in NDN as follows::

     VAR-NUMBER-1 = %x00-FC
     VAR-NUMBER-3 = %xFD 2OCTET
     VAR-NUMBER-5 = %xFE 4OCTET
     VAR-NUMBER-9 = %xFF 8OCTET

The first octet of the number either carries the actual number, or signals that a multi-octet encoding is present, as defined below:

- If the first octet is less than or equal to 252 (0xFC), the number is encoded in that octet.

- If the first octet is 253 (0xFD), the number is encoded in the following 2 octets, in network byte-order.
  This number must be greater than 252 (0xFC).

- If the first octet is 254 (0xFE), the number is encoded in the following 4 octets, in network byte-order.
  This number must be greater than 65535 (0xFFFF).

- If the first octet is 255 (0xFF), the number is encoded in the following 8 octets, in network byte-order.
  This number must be greater than 4294967295 (0xFFFFFFFF).

A number MUST be encoded in the shortest format.
For example, the number 1024 is encoded as %xFD0400 in VAR-NUMBER-3 format, not %xFE00000400 in VAR-NUMBER-5 format.

.. note::
   The formal grammar of NDN packet format in this specification is given using `Augmented BNF for Syntax Specifications <https://tools.ietf.org/html/rfc5234>`__

.. _TLV:

TLV Encoding
~~~~~~~~~~~~

TLV encoding for NDN packets is defined as follows::

    NDN-TLV = TLV-TYPE TLV-LENGTH TLV-VALUE
    TLV-TYPE = VAR-NUMBER-1 / VAR-NUMBER-3 / VAR-NUMBER-5
    TLV-LENGTH = VAR-NUMBER-1 / VAR-NUMBER-3 / VAR-NUMBER-5 / VAR-NUMBER-9
    TLV-VALUE = *OCTET

TLV-TYPE MUST be in the range ``1-4294967295`` (inclusive).
Zero is reserved to indicate an invalid TLV element and MUST NOT appear on the wire.
TLV-TYPE SHOULD be unique at all nested levels.
Section :ref:`types` of this document lists initial TLV-TYPE assignments.

The ``TLV-LENGTH`` field indicates number of bytes that ``TLV-VALUE`` uses.
It **does not** include number of bytes that ``TLV-TYPE`` and ``TLV-LENGTH`` fields themselves occupy.
In particular, empty payload TLV will carry ``TLV-LENGTH`` equal to 0.

This encoding offers a reasonable balance between compactness and flexibility.
Most common, standardized TLV-TYPE numbers will be allocated from a small-integer number-space, and these common types will be able to use the compact, single-byte encoding.

Non Negative Integer Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A number of TLV elements in NDN packet format take a non-negative integer as their TLV-VALUE, with the following definition::

    nonNegativeInteger = 1OCTET / 2OCTET / 4OCTET / 8OCTET

TLV-LENGTH of the TLV element MUST be either 1, 2, 4, or 8.
Depending on TLV-LENGTH, a nonNegativeInteger is encoded as follows:

- if the length is 1, the nonNegativeInteger is encoded in one octet;

- if the length is 2, the nonNegativeInteger is encoded in 2 octets, in network byte-order;

- if the length is 4, the nonNegativeInteger is encoded in 4 octets, in network byte-order;

- if the length is 8, the nonNegativeInteger is encoded in 8 octets, in network byte-order.

The following shows a few examples of TLVs that have nonNegativeInteger as their value component in hexadecimal format (where ``TT`` represents ``TLV-TYPE``, followed by the ``TLV-LENGTH``, then ``TLV-VALUE``)::

    0     => TT0100
    1     => TT0101
    255   => TT01FF
    256   => TT020100
    65535 => TT02FFFF
    65536 => TT0400010000

.. _evolvability:

Considerations for Evolvability of TLV-Based Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ensure that the TLV-based protocol can evolve over time without requiring flag days, the least significant bit of TLV-TYPE number (unless overriden by the specification of a particular network/library/application TLV element) is reserved to indicate whether that TLV element is "critical" or "non-critical".
A compliant TLV format decoder should follow the order, quantity, and presence requirements of the recognized elements defined in the corresponding specification.
At the same time, if decoder encounters an unrecognized or out-of-order element, the behavior should be as follows:

- if the least significant bit of element's TLV-TYPE number is ``1``, abort decoding and report an error;
- if the least significant bit of element's TLV-TYPE number is ``0``, ignore the element and continue decoding.

.. note::
    A recognized element is considered out-of-order if it appears in the element order that violates a specification.  For example,
    - when a specification defines a sequence {``F1`` ``F2`` ``F3``}, an element ``F3`` would be out-of-order in the sequence {``F1`` ``F3`` ``F2``};
    - for {``F1`` ``F2?`` ``F3``} specification (i.e., when ``F2`` is optional, ``F2`` would be out-of-order in the same sequence {``F1`` ``F3`` ``F2``}.

.. note::
   TLV-TYPE numbers 0-31 (inclusive) are "grandfathered" and all designated as "critical" for the purpose of packet processing.
