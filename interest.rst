.. _Interest:

Interest Packet
---------------

NDN Interest packet is TLV defined as follows:

::

    Interest ::= INTEREST-TYPE TLV-LENGTH 
                   Name
                   Selectors?
                   Nonce
                   Scope?
                   InterestLifetime?

``Name`` and ``Nonce`` are the only two two required elements in an Interest packet.
Selectors are optional elements that further qualify Data that may match the Interest.
They are used for discovering and selecting the Data that matches best to what the application wants. Selectors are placed right after the Name to facilitate implementations that may use continuous memory block of Name and Selectors TLVs together as the index for PIT lookup. By using a TLV to group all the Selectors, an implementation can easily skip them to find Nonce, which is used together with Name to identify looping Interests. 
If Selectors TLV is present in the Interest, it MUST contain at least one selector.

The two other optional elements, Scope and InterestLifetime, are referred to as *Guiders*.
They affect Interest forwarding behavior, e.g., how far the Interest may be forwarded, and how long an Interest may be kept in the PIT. They are not grouped.


Name
~~~~

The Name element in an Interest is synonymous with the term *prefix*.
See :ref:`Name section <Name>` for details.

.. _Selectors:

Selectors
~~~~~~~~~

::

    Selectors ::= SELECTORS-TYPE TLV-LENGTH 
                    MinSuffixComponents?
                    MaxSuffixComponents?
                    PublisherPublicKeyLocator?
                    Exclude?
                    ChildSelector?
                    MustBeFresh?

MinSuffixComponents, MaxSuffixComponents
++++++++++++++++++++++++++++++++++++++++

::

    MinSuffixComponents ::= MIN-SUFFIX-COMPONENTS-TYPE TLV-LENGTH
                              nonNegativeInteger

    MaxSuffixComponents ::= MAX-SUFFIX-COMPONENTS-TYPE TLV-LENGTH
                              nonNegativeInteger

When needed, ``MinSuffixComponents`` and ``MaxSuffixComponents`` allow a data consumer to indicate whether the Name in the Interest is the full name including the digest, or the full name except for the digest, or the content it is seeking has a known range of legitimate component counts. 
These two parameters refer to the number of name components beyond those in the prefix, and counting the implicit digest, that may occur in the matching Data. 
The default for ``MinSuffixComponents`` is 0 and for ``MaxSuffixComponents`` is effectively infinite, meaning that any Data whose name starts with the prefix is a match.  Often only one of these will be needed to get the desired effect.

 
PublisherPublicKeyLocator
+++++++++++++++++++++++++

::

    PublisherPublicKeyLocator ::= KeyLocator

This element specifies the name of the key which is used to sign the Data packet that the consumer is requesting.
This is a way for the Interest to select answers from a particular publisher.

See :ref:`KeyLocator` section for more detail.

Exclude
+++++++

::

    Exclude ::= EXCLUDE-TYPE TLV-LENGTH Any? (NameComponent (Any)?)+
    Any ::= ANY-TYPE TLV-LENGTH(=0)

The ``Exclude`` selectors allows requester to specify list and/or ranges of names components that MUST NOT appear as a continuation of the Name prefix in the responding Data packet to the Interest.
For example, if Interest is expressed for ``/ndn/edu`` and Exclude specifies one name component ``ucla``, then nor data producer nor conforming NDN routers are allowed to return any Data packet that has prefix ``/ndn/edu/ucla``.

Exclude filter applies only to a name component of the Data packet name that is located at a position that numerically equals to the number of name components in the Interest packet, assuming 0 is the first name component.

The Components in the exclusion list MUST occur in strictly increasing order according to the canonical NDN name component ordering (:ref:`Name Section<name>`), with optional leading, trailing, and interleaved ``Any`` components. The following defines processing of ``Any`` components:

- If none of the ``Any`` components are specified, the filter excludes only to the names specified in the Exclude list.

- If a leading ``Any`` component is specified, then the filter excludes all names that are smaller or equal (in NDN name component canonical ordering) to the first NameComponent in the Exclude list.

- If a trailing ``Any`` component is specified, then the filter excludes all names that are larger or equal (in NDN name component canonical ordering) to the last NameComponent in the Exclude list.

- If ``Any`` component is specified between two NameComponents in the list, then the filter excludes all names from the range from the right NameComponent to the left NameComponent, including both ends.


Exclude filter MUST not consist of a single ``Any`` component or one NameComponent with leading and trailing ``Any`` components.


ChildSelector
+++++++++++++

::

    ChildSelector ::= CHILD-SELECTOR-TYPE TLV-LENGTH 
                        nonNegativeInteger

Often a given Interest can match more than one Data within a given content store.
The ``ChildSelector`` provides a way of expressing a preference for which of these should be returned.
If the value is 0, the leftmost child is preferred.
If 1, the rightmost child is preferred.
Here leftmost and rightmost refer to the least and greatest components according to the canonical NDN name component ordering (:ref:`Name Section<name>`).
This ordering is only done at the level of the name hierarchy one past the name prefix.

For example, assuming in the name hierarchy the component immediately after the name prefix  is the version number, whose next level is the segment number, then setting ChildSelector to be 1 will retrieve the rightmost version number (i.e., the latest version) and the leftmost segment number (i.e., the first segment). However, this selection is only done with respect to a single content store, not globally. Additional rounds that exclude the earlier versions may be used to explore other content stores for newer versions. 
In this case, the use of ChildSelector does not change the multi-round outcome, but it decreases the number of rounds needed to converge to an answer.
 
MustBeFresh
+++++++++++

::

   MustBeFresh ::= MUST-BE-FRESH-TYPE TLV-LENGTH(=0)

This selector is encoded with Type and Length but no Value part.
When it is absent from an Interest packet, the router can respond with a Data packet from its content store whose FreshnessPeriod is either still valid or expired. 
When it is present in an Interest packet, the router should not return Data packet from its content store whose FreshnessPeriod has expired.

The FreshnessPeriod carried in each Data packet (:ref:`Data Section<data>`) is set by the original producer.  It starts counting down when the Data packet arrives at a node. Consequently if a node is N hops away from the original producer, it may not consider the Data stale until N *X* FreshnessPeriod after the Data is produced.

.. _Nonce:

Nonce
~~~~~

Nonce defined as follows:

::

    Nonce ::= NONCE-TYPE TLV-LENGTH(=4) BYTE{4}

The Nonce carries a randomly-genenerated 4-octet long byte-string.
The combination of Name and Nonce should uniquely identify an Interest packet.
This is used to detect looping Interests.

.. _Guiders:

Guiders
~~~~~~~

Scope
+++++

::

    Scope ::= SCOPE-TYPE TLV-LENGTH nonNegativeInteger

This value limits how far the Interest may propagate.
Scope 0 prevents propagation beyond the local NDN daemon (even to other applications on the same host). Scope 1 limits propagation to the applications on the originating host.
Scope 2 limits propagation to no further than the next node. 
Other values are not defined at this time, and will cause the Interest packet to be dropped.

Note that Scope is not a hop count---the value is not decremented as the Interest is forwarded.
 
InterestLifetime
++++++++++++++++

::

    InterestLifetime ::= INTEREST-LIFETIME-TYPE TLV-LENGTH nonNegativeInteger

``InterestLifetime`` indicates the (approximate) time remaining before the Interest times out. 
The value is the number of milliseconds.  The timeout is relative to the arrival time of the Interest at the current node.

Nodes that forward Interests may decrease the lifetime to account for the time spent in the node before forwarding, but are not required to do so. It is recommended that these adjustments be done only for relatively large delays (measured in seconds).

It is the application that sets the value for ``InterestLifetime``.
If the ``InterestLifetime`` element is omitted, a default value of 4 seconds is used (4000).
The missing element may be added before forwarding.

Changes from CCNx
~~~~~~~~~~~~~~~~~

- ``Nonce`` is changed from optional to required.

- ``PublisherPublicKeyDigest`` is replaced by ``PublisherPublicKeyLocator``.

- ``AnswerOriginKind`` is simplified from 4bits to a 1-bit ``MustBeFresh``.

- ``FaceID`` has been removed.

- ``InterestLifetime`` changes the unit to the number of milliseconds.

- Removed Bloom Filter from Exclude.
