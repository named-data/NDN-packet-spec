.. _Interest:

Interest Packet
---------------

NDN Interest packet is TLV defined as follows:

::

    Interest ::= INTEREST-TYPE TLV-LENGTH
                   Name
                   CanBePrefix?
                   MustBeFresh?
                   ForwardingHint?
                   Nonce?
                   InterestLifetime?
                   HopLimit?
                   Parameters?

``Name`` is the only required element in an Interest packet.
``Nonce`` is required when an Interest is transmitted over the network links, i.e., a compliant forwarder must augment the Interest with the ``Nonce`` element if it is missing.
``CanBePrefix``, ``MustBeFresh``, ``InterestLifetime``, and ``ForwardingHint`` are optional elements to guide Interest matching or forwarding.
Interest can also include an optional ``Parameters`` element.

Name
~~~~

See :ref:`Name section <Name>` for details.

The ``Name`` element that can be put in the Interest is further restricted to have at least one name component.
Interests that include Name TLV that has zero name components MUST be discarded.

CanBePrefix
~~~~~~~~~~~

::

    CanBePrefix ::= CAN-BE-PREFIX-TYPE TLV-LENGTH(=0)

When present, ``Name`` element in the Interest is a prefix, exact, or full name of the requested Data packet.

When not present, the ``Name`` element is either exact or full name of the Data packet:

- if the last component of the ``Name`` has type ``ImplicitSha256DigestComponent``, Interest can be matched only to a Data packet with full name that includes the implicit digest component;

- if the last component has any other type, Interest is matched to Data if all name components in Interest's ``Name`` element equal to components in Data's ``Name`` element, without consideration of the implicit digest component.

MustBeFresh
~~~~~~~~~~~

::

   MustBeFresh ::= MUST-BE-FRESH-TYPE TLV-LENGTH(=0)

The presence or absense of the ``MustBeFresh`` element indicates whether a content store may satisfy the Interest with stale Data.
Refer for :ref:`FreshnessPeriod section <FreshnessPeriod>` for more information.

ForwardingHint
~~~~~~~~~~~~~~

::

   ForwardingHint ::= FORWARDING-HINT-TYPE TLV-LENGTH
                        Delegation+

The ForwardingHint element contains a list of name delegations, as defined in :ref:`link` section.
Each delegation implies that the requested Data packet can be retrieved by forwarding the Interest along the delegation path.
Specifics of the forwarding logic for Interests with ``ForwardingHint`` will be defined in a separated document.

.. _Nonce:

Nonce
~~~~~

Nonce defined as follows:

::

    Nonce ::= NONCE-TYPE TLV-LENGTH(=4) BYTE{4}

The Nonce carries a randomly-generated 4-octet long byte-string.
The combination of Name and Nonce should uniquely identify an Interest packet.
This is used to detect looping Interests.

InterestLifetime
~~~~~~~~~~~~~~~~

::

    InterestLifetime ::= INTEREST-LIFETIME-TYPE TLV-LENGTH nonNegativeInteger

``InterestLifetime`` indicates the (approximate) time remaining before the Interest times out.
The value is the number of milliseconds.  The timeout is relative to the arrival time of the Interest at the current node.

Nodes that forward Interests may decrease the lifetime to account for the time spent in the node before forwarding, but are not required to do so. It is recommended that these adjustments be done only for relatively large delays (measured in seconds).

It is the application that sets the value for ``InterestLifetime``.
If the ``InterestLifetime`` element is omitted, a default value of 4 seconds is used (4000).
The missing element may be added before forwarding.

HopLimit
~~~~~~~~

::

    HopLimit ::= HOP-LIMIT-TYPE TLV-LENGTH(=1) BYTE{1}

The optional ``HopLimit`` element indicates the number of hops the Interest is allowed to be forwarded.  The value is encoded as a 1-byte unsigned integer value in the range 0-255.

If element is present:

- if the ``HopLimit`` value is larger than or equal to 1, a node should accept the packet and decrease the encoded value by 1.

  If the ``HopLimit`` value becomes 0, a node can satisfy this Interest locally (cache or applications bound to local faces), but must not forward the Interests to any non-local faces.

- if ``HopLimit`` is 0, a node must drop the packet

If omitted:

- a node should accept the packet;

- when desired, a node can augment the Interest with the ``HopLimit`` element.

Parameters
~~~~~~~~~~

::

   Parameters ::= PARAMETERS-TYPE TLV-LENGTH
                    BYTE*

The ``Parameters`` element can carry any arbitrary data that parameterizes the request for Data.
The Interest's name should include a component or components to ensure uniqueness of the parametrized Interest.
For example, a SHA256 digest of the ``Parameters`` TLV can be included as one of the components of the Interest name.
