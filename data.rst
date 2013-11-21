.. _data:

Data Packet
-----------

NDN Data packet is TLV defined as follows::

    Data ::= DATA-TLV TLV-LENGTH
               Name
               MetaInfo
               Content
               Signature

The Data packet represents some arbitrary binary data (held in the Content element) together with its Name, some additional bits of information (MetaInfo), and a digital Signature of the other three elements. The Name is the first element since all NDN packet processing starts with the name.  Signature is put at the end of the packet to ease the implementation because signature computation covers all the elements before Signature.

Name
~~~~

See :ref:`Name section<name>` for details.

MetaInfo
~~~~~~~~

.. [#f1] If both ``ContentType`` and ``FreshnessPeriod`` are optional, one may consider ``Metainfo`` itself should be optional. But would have all 4 parts of Data packet help simplify implementation? We leave this question to people who are more familiar with high speed implementations.

.. code-block:: none

    MetaInfo ::= META-INFO-TYPE TLV-LENGTH
                   ContentType?
                   FreshnessPeriod?

Compared with CCNx, four fields are removed: PublisherPublicKeyDigest, ExtOpt, Timestamp, and FinalBlockID for the following reasons.


- PublisherPublicKeyDigest is supposed to be used in selecting data packets signed by a particular key.
  We replace PublisherPublicKeyDigest with KeyLocator, which is part of the Signature block (see :ref:`Signature Section<signature>`), due to the following consideration.
  First, it requires data consumer to acquire a *valid* public key, as opposed to the key locator, before sending Interest out. 
  Second, if a router is to verify the content objects, it must have other means to locate the keys first.
  Further, it may require publishers to maintain their public keys and certificates by their public key digests instead of names.

- ExtOpt was intended for extending XML-based ccnb format.  Since we are now using TLV, ExtOpt is no longer needed.

- Timestamp and FinalBlockID can be useful meta information for applications, but do not need to be processed at the network layer.
  Therefore, if desired, applications should encode such meta information as part of the content.


ContentType
+++++++++++

.. code-block:: none

    ContentType ::= CONTENT-TYPE-TYPE TLV-LENGTH nonNegativeInteger

Three ContentTypes are currently defined: default (=0), LINK (=1), and KEY (=2). The **default** type of content is a BLOB (=0), which is the actual data bits identified by the data name. The \textbf{LINK} type of content is another name which identifies the actual data content. The ``KEY`` type of content is a public key.

Compared with CCNx, three types, ENCR, GONE, and NACK are removed. 
ENCR means the content is encrypted, and since the network layer should not care whether content is encrypted or not, this type is not needed.
GONE was a placeholder for implementing cache purging, however the research is yet to be carried out on how to accomplish this goal, if it is feasible to achieve, it is not included in this 0.1 version of NDN specification. 
NACK is used to signal a downstream node that the upstream node is unable to retrieve a matching data.  Since the actual NACK mechanism is still under active investigation, we do not include it in this version of specification, but may add it back in a future version. 


FreshnessPeriod
+++++++++++++++

.. code-block:: none

    FreshnessPeriod ::= FRESHNESS-PERIOD-TLV TYPE-TLV nonNegativeInteger

The optional FreshnessPeriod indicates how long a node should wait after the arrival of this data before marking it as stale.  The encoded value is number of milliseconds.  Note that the stale data is still valid data; the expiration of FreshnessPeriod only means that the producer may have produced newer data. 

Each content store associates every piece of Data with a staleness bit.
The initial setting of this bit for newly-arrived content is "not stale". If the Data carries FreshnessPeriod, then after the Data has been residing in the content store for FreshnessPeriod, it will be marked as stale. This is per object staleness and local to the NDN node. Another possible way to set the staleness bit of a local content is for a local client to send a command to the local NDN daemon. 

If an Interest contains MustBeFresh TLV, a Data that has the staleness bit set is not eligible to be sent in response to that Interest. 
The effect is the same as if that stale Data did not exist (i.e., the Interest might be matched by some other Data in the store, or, failing that, get forwarded to other nodes).
If an exact duplicate of a stale Data arrives, the effect is the same as if the stale Data had not been present. In particular, the Data in the store is no longer stale. As a practical matter, a stale Data should be ranked high on the list of things to discard from the store when a storage quota has been reached.


Content
~~~~~~~

.. code-block:: none

    Content ::= CONTENT-TYPE TLV-LENGTH BYTE*


Changes from CCNx
~~~~~~~~~~~~~~~~~

- The structure of Data packet is changed.

- SignedInfo is renamed to MetaInfo and its content is changed. 

- PublisherPublicKeyDigest and ExtOpt are removed.

- Timestamp and FinalBlockID are removed.

- KeyLocator is moved to be inside the Signature block.

- Three content types, ENCR, GONE, and NACK are removed.

- FreshnessSeconds is renamed to FreshnessPeriod and is expressed in units of milliseconds.

