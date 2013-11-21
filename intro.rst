Introduction
------------

This version 0.1 specification aims to describe the NDN packet format only, a much narrower scope than a full NDN protocol specification. Our plan is to circulate and finalize the packet format first, then write down the full protocol specification. 

In addition to this protocol specification draft, we are also in the process of putting out a set of technical memos that document our reasoning behind the design choices of important issues.  The first few to come out will address the following issues:

- Packet fragmentation: end-to-end versus hop-by-hop;

- Understanding the tradeoffs of (not) handling Interest selectors;

- NDN Name discovery: why do we need it?

- NDN naming convention; and

- Scaling NDN routing.

In the rest of the document, we assume readers are familiar with how NDN/CCN works in general. For a description of the current CCNx protocol definition, please refer to `<http://www.ccnx.org/releases/latest/doc/technical/CCNxProtocol.html>`_.
