.. _Face Registration:

Face Management and Registration Protocol
-----------------------------------------

Face Management Protocol
^^^^^^^^^^^^^^^^^^^^^^^^

The Face Management Protocol provides a method for an entity such as ndndc to control
the faces maintained by ndnd, which are subsequently used in the Registration Protocol.

The FMP supports ``newface``, ``destroyface``, and ``queryface`` operations.

A request operation is represented as a NDN Interest with
a NDN Data in NDN-TLV encoding, while the majority of the request parameters embedded
as a component of the Interest name.
A response is represented as a Data for which the name matches the Interest,
and the content encodes any necessary response data.

For the Face Management Protocol, the content of the Data packet is FaceInstance object
as defined below.

For example, the following steps necessary to create a new face:

- Create NDN-TLV encoded FaceInstance object, containing action ``newface`` and other
  necessary fields to set up the face (e.g., ``IPProto``, ``Host``, ``Port``).

- Create NDN-TLV encoded Data packet (``<NFBLOB>``), whose content is the encoded
  FaceInstance object

- Express an Interest ``/ndnx/<NDNDID>/newface/<NFBLOB>``, where

  * ``<NDNDID>`` is the SHA256 of the public key of the forwarding daemon.

  * ``<NFBLOB>`` is encoded Data packet with encoded FaceInstance object as content.

The verb, ``newface`` occurs redundantly in both the Interest prefix and in the ``NFBLOB``.
Its presence in the prefix is for dispatching the request.
It is also in the ``NFBLOB``, so that it is signed.

The forwarding daemon creates the new face and answers with a FaceInstance containing
at least the ``FaceID``.

FaceInstance
^^^^^^^^^^^^

::

    FaceInstance ::= FACE-INSTANCE-TYPE TLV-LENGTH
                       Action?
                       FaceID?
                       IPProto?
                       Host?
                       Port?
                       MulticastInterface?
                       MulticastTTL?
                       FreshnessPeriod?

    Action             ::= ACTION-TYPE TLV-LENGTH
                            ("newface" | "destroyface" | "queryface")

    FaceID             ::= FACEID-TYPE TLV-LENGTH
                             nonNegativeInteger

    IPProto            ::= FACEID-TYPE TLV-LENGTH
                             nonNegativeInteger
                       (*IANA protocol number; 6=TCP, 17=UDP*)

    Host               ::= HOST-TYPE TLV-LENGTH
                             <textual representation of numeric IPv4 or IPv6 address>

    Port               ::= PORT-TYPE TLV-LENGTH
                             nonNegativeInteger
                       (* from the range [1..65535] *)

    MulticastInterface ::= MULTICAST-INTERFACE-TYPE TLV-LENGTH
                             <textual representation of numeric IPv4 or IPv6 address>

    MulticastTTL       ::= MULTICAST-TTL-TYPE TLV-LENGTH
                             nonNegativeInteger
                       (* from the range [1..255] *)

See :ref:`Data packet's meta info description <MetaInfo>` for definition of ``FreshnessPeriod``.

Action
++++++

When FaceInstance is used as a request, the Action must be specified.
It will not be present in a response.

+-----------------+----------------------------------------------------------------------+
| Action          | Description                                                          |
+=================+======================================================================+
| ``newface``     | If a face matching the parameters does not already exist, an attempt |
|                 | is made to create it.                                                |
|                 |                                                                      |
|                 | Then if the face exists (whether new or old) the full description is |
|                 | returned as a FaceInstance.                                          |
+-----------------+----------------------------------------------------------------------+
| ``destroyface`` | At least the FaceID must be present.                                 |
|                 | If permitted, the face is destroyed.                                 |
+-----------------+----------------------------------------------------------------------+
| ``queryface``   | TBD                                                                  |
+-----------------+----------------------------------------------------------------------+

FaceID
++++++

FaceID is not present in a `newface` request, but must be specified in
a `destroyface` or `queryface` request.
FaceID is always present in a response.

Host
++++

Identifies the IPv4 or IPv6 numeric address of the remote ndnd for this
FaceInstance.

Port
++++

Port identifies the port on the remote ndnd, or the port for the multicast group.

MulticastInterface
++++++++++++++++++

If the Host is a multicast address, and there are multiple
interfaces present, MulticastInterface will identify the unicast
numeric address of the interface to which the multicast address will be
attached.

MulticastTTL
++++++++++++

Specifies the TTL to be used for multicast operations.  The default value is 1.

FreshnessPeriod
++++++++++++++++

FreshnessPeriod is optional in a request, but is treated as a hint by the forwarding daemon.
In a response, FreshnessPeriod specifies the remaining lifetime in milliseconds of the
face.

Prefix Registration Protocol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The prefix registration protocol uses the ForwardingEntry element type
to represent both requests and responses.

::

    ForwardingEntry ::= FORWARDING-ENTRY TLV-LENGTH
                          Action?
                          Name?
                          FaceID?
                          ForwardingFlags?
                          FreshnessPeriod?

    Action          ::= ACTION-TYPE TLV-LENGTH
                          ("prefixreg" | "selfreg" | "unreg")

    FaceID          ::= FACEID-TYPE TLV-LENGTH
                          nonNegativeInteger

    ForwardingFlags ::= FORWARDING-FLAGS TLV-LENGTH
                          nonNegativeInteger

See :ref:`Name section <Name>` for definition of ``Name`` and 
:ref:`Data packet's meta info description <MetaInfo>` for definition of ``FreshnessPeriod``.


Action
++++++

When ForwardingEntry is used as a request, the Action must be specified.
It will not be present in a response.

- `prefixreg` - Register (or re-register) the prefix on the specified face.
- `selfreg` - Register (or re-register) the prefix on the current face; the
  FaceID need not be present in the request, but if present it must match
  the current face.
- `unreg` - Remove the prefix registration for the specified face.

FaceID
++++++

FaceID is required in `prefixreg` and `unreg` requests.
FaceID is always present in a response.

Name
++++

This is the name prefix to be acted on.

ForwardingFlags
+++++++++++++++

This integer holds the inclusive OR of the following bit fields:

+----------------------------+---------------+-----------------------------------------------------------------------------+
| Flag mnemonic              | Bit (decimal) | Description                                                                 |
+============================+===============+=============================================================================+
| ``NDN_FORW_ACTIVE``        | 1             | Indicates that the entry is active;                                         |
|                            |               | interests will not be sent for inactive entries (but see note below).       |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_CHILD_INHERIT`` | 2             | Denotes that this entry may be used even if there is a longer match         |
|                            |               | available.  In the absence of this bit, the presence of a longer matching   |
|                            |               | prefix that has an active entry will prevent this entry from being used.    |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_ADVERTISE``     | 4             | Indicates that the prefix may be advertised to other nodes.                 |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_LAST``          | 8             | Indicates that this entry should be used last, if nothing else worked.      |
|                            |               | This is intended to be used by ndndc and similar programs to monitor        |
|                            |               | unanswered interests.                                                       |
|                            |               |                                                                             |
|                            |               | The presence of this flag on any entry causes the associated face to be     |
|                            |               | considered non-local, as far as interest forwarding is concerned.           |
|                            |               | Thus it will not receive interests with Scope=1, nor will it receive        |
|                            |               | interests in namespaces that are marked local.  However, the ability of     |
|                            |               | the face to change prefix registrations is not affected.                    |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_CAPTURE``       | 16            | Says that no shorter prefix may be used, overriding child-inherit bits that |
|                            |               | would otherwise make the shorter entries usable.                            |
|                            |               |                                                                             |
|                            |               | For a child-inherit bit to be overridden, the ``NDN_FORW_CAPTURE_OK`` must  |
|                            |               | be set in the same forwarding entry that has ``NDN_FORW_CHILD_INHERIT``     |
|                            |               | set.  Note that this means that using ``NDN_FORW_CAPTURE`` will have no     |
|                            |               | effect if the ``NDN_FORW_CAPTURE_OK`` flag is not used.                     |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_LOCAL``         | 32            | Restricts the namespace to use by applications on the local machine.        |
|                            |               |                                                                             |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_TAP``           | 64            | Causes the entry to be used right away.  This is intended for debugging     |
|                            |               | and monitoring purposes.  It is likely that there will be no response as    |
|                            |               | a result, so no intentional delay is added before any further forwarding    |
|                            |               | of this interest.                                                           |
+----------------------------+---------------+-----------------------------------------------------------------------------+
| ``NDN_FORW_CAPTURE_OK``    | 128           | used in conjunction with ``NDN_FORW_CHILD_INHERIT`` allows a                |
|                            |               | ``NDN_FORW_CAPTURE`` flag on a longer prefix to override the effect of      |
|                            |               | the child-inherit bit.                                                      |
+----------------------------+---------------+-----------------------------------------------------------------------------+

The flags ``NDN_FORW_ADVERTISE``, ``NDN_FORW_CAPTURE`` and ``NDN_FORW_LOCAL`` affect
the prefix as a whole, rather than the individual registrations.
Their effects take place whether or not the ``NDN_FORW_ACTIVE`` bit is set.

FreshnessPeriod
+++++++++++++++

FreshnessPeriod is optional in a request, but is treated as a hint by the forwarding daemon.
In a response, FreshnessPeriod specifies the remaining lifetime in milliseconds of the registration.


Type code assignment
^^^^^^^^^^^^^^^^^^^^

Face management and registration protocol uses the following type codes, which are assigned
from the :ref:`application range (128-252) <type reservations>`.

Some codes (e.g., `Name`, `FreshnessPeriod`), re-use code assignment from the NDN-TLV specification.

+---------------------------------------------+-------------------+----------------+
| Type                                        | Assigned value    | Assigned value |
|                                             | (decimal)         | (hexadecimal)  |
+=============================================+===================+================+
| **Application-specific definitions**                                             |
+---------------------------------------------+-------------------+----------------+
| FaceInstance                                | 128               | 0x80           |
+---------------------------------------------+-------------------+----------------+
| ForwardingEntry                             | 129               | 0x81           |
+---------------------------------------------+-------------------+----------------+
| Action                                      | 130               | 0x82           |
+---------------------------------------------+-------------------+----------------+
| FaceID                                      | 131               | 0x83           |
+---------------------------------------------+-------------------+----------------+
| IPProto                                     | 132               | 0x84           |
+---------------------------------------------+-------------------+----------------+
| Host                                        | 133               | 0x85           |
+---------------------------------------------+-------------------+----------------+
| Port                                        | 134               | 0x86           |
+---------------------------------------------+-------------------+----------------+
| MulticastInterface                          | 135               | 0x87           |
+---------------------------------------------+-------------------+----------------+
| MulticastTTL                                | 136               | 0x88           |
+---------------------------------------------+-------------------+----------------+
| ForwardingFlags                             | 137               | 0x89           |
+---------------------------------------------+-------------------+----------------+
| **Re-used definitions**                                                          |
+---------------------------------------------+-------------------+----------------+
| FreshnessPeriod                             | 20                | 0x14           |
+---------------------------------------------+-------------------+----------------+
| Name                                        | 2                 | 0x02           |
+---------------------------------------------+-------------------+----------------+
