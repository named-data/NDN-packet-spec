.. _Link:

Link Object
-----------

The Link Object is a specialized form of a :ref:`Data packet <Data>`, defined as follows::

    LinkObject = DATA-TYPE TLV-LENGTH
                   Name
                   MetaInfo ; ContentType == LINK
                   LinkContent
                   Signature

    LinkContent = CONTENT-TYPE TLV-LENGTH 1*Name


Link Object is a data packet, whose content is a list of one or more names (formerly known as "delegations").
The LinkObject can be used to derive the ``ForwardingHint`` of an Interest packet.

The list of Names in ``LinkContent`` SHOULD be ordered by the producer's preference, with the most preferred by the producer listed first.

In a LinkContent, each listed Name SHOULD be distinct.
