.. vim: set textwidth=79

*****************
Synapse Changelog
*****************

v2.109.0 - 2022-09-27
=====================

Features and Enhancements
-------------------------
- Add a ``format()`` API to ``str`` variables in Storm.
  (`#2849 <https://github.com/vertexproject/synapse/pull/2849>`_)
- Update the Telepath user resolution for TLS links to prefer resolving users
  by the Cell ``aha:network`` over the certificate common name.
  (`#2850 <https://github.com/vertexproject/synapse/pull/2850>`_)
- Update all Synapse tools which make telepath connections to use the
  ``withTeleEnv()`` helper.
  (`#2844 <https://github.com/vertexproject/synapse/pull/2844>`_)
- Update the Telepath and HTTPs TLS listeners to drop RSA based key exchanges
  and disable client initiated renegotiation.
  (`#2845 <https://github.com/vertexproject/synapse/pull/2845>`_)
- Update the minimum allowed versions of the ``aioimaplib`` and ``oauthlib``
  libraries.
  (`#2847 <https://github.com/vertexproject/synapse/pull/2847>`_)
  (`#2854 <https://github.com/vertexproject/synapse/pull/2854>`_)

Bugfixes
--------
- Correct default Telepath ``cell://`` paths in Synapse tools.
  (`#2853 <https://github.com/vertexproject/synapse/pull/2853>`_)
- Fix typos in the inline documentation for several model elements.
  (`#2852 <https://github.com/vertexproject/synapse/pull/2852>`_)
- Adjust expression syntax rules in Storm grammar to remove incorrect
  whitespace sensitivity in certain expression operators.
  (`#2846 <https://github.com/vertexproject/synapse/pull/2846>`_)

Improved Documentation
----------------------
- Update Storm and Storm HTTP API documentation to show the set of ``opts``
  and different types of message that may be streamed by from Storm APIs.
  Add example HTTP API client code to the Synapse repository.
  (`#2834 <https://github.com/vertexproject/synapse/pull/2834>`_)
- Update the Data Model and Analytical model background documentation.
  Expand on the discussion of light edges use. Expand discussion of tags
  versus forms, linking the two via ``:tag`` props.
  (`#2848 <https://github.com/vertexproject/synapse/pull/2848>`_)


v2.108.0 - 2022-09-12
=====================

Features and Enhancements
-------------------------
- Update the Telepath TLS connections to require a minimum TLS version of 1.2.
  (`#2833 <https://github.com/vertexproject/synapse/pull/2833>`_)
- Update the Axon implementation to use the ``initServiceStorage()`` and
  ``initServiceRuntime()`` methods, instead of overriding ``__anit__``.
  (`#2837 <https://github.com/vertexproject/synapse/pull/2837>`_)
- Update the minimum allowed versions of the ``aiosmtplib`` and ``regex``
  libraries.
  (`#2832 <https://github.com/vertexproject/synapse/pull/2832>`_)
  (`#2841 <https://github.com/vertexproject/synapse/pull/2841>`_)

Bugfixes
--------
- Catch ``LarkError`` exceptions in all Storm query parsing modes.
  (`#2840 <https://github.com/vertexproject/synapse/pull/2840>`_)
- Catch ``FileNotFound`` errors in ``synapse.tools.healthcheck``. This could
  be caused by the tool running during container startup, and prior to a
  service making its Unix listening socket available.
  (`#2836 <https://github.com/vertexproject/synapse/pull/2836>`_)
- Fix an issue in ``Axon.csvrows()`` where invalid data would cause
  processing of a file to stop.
  (`#2835 <https://github.com/vertexproject/synapse/pull/2835>`_)
- Address a deprecation warning in the Synapse codebase.
  (`#2842 <https://github.com/vertexproject/synapse/pull/2842>`_)
- Correct the type of ``syn:splice:splice`` to be ``data``. Previously it
  was ``str``.
  (`#2839 <https://github.com/vertexproject/synapse/pull/2839>`_)

Improved Documentation
----------------------
- Replace ``livenessProbe`` references with ``readinessProbe`` in the
  Kubernetes documentation and examples. The ``startupProbe.failureThreshold``
  value was increased to its maximum value.
  (`#2838 <https://github.com/vertexproject/synapse/pull/2838>`_)
- Fix a typo in the Rapid Power-Up documentation.
  (`#2831 <https://github.com/vertexproject/synapse/pull/2831>`_)

v2.107.0 - 2022-09-01
=====================

Automatic Migrations
--------------------
- Migrate the ``risk:alert:type`` property to a ``taxonomy`` type
  and create new nodes as needed.
  (`#2828 <https://github.com/vertexproject/synapse/pull/2828>`_)
- Migrate the ``pol:country:name`` property to a ``geo:name`` type
  and create new nodes as needed.
  (`#2828 <https://github.com/vertexproject/synapse/pull/2828>`_)
- See :ref:`datamigration` for more information about automatic migrations.

Features and Enhancements
-------------------------
- Updates to the ``geo``, ``inet``, ``media``, ``pol``, ``proj``, and
  ``risk`` models.
  (`#2828 <https://github.com/vertexproject/synapse/pull/2828>`_)
  (`#2829 <https://github.com/vertexproject/synapse/pull/2829>`_)

  ``geo:area``
    Add a new type to record the size of a geographic area.

  ``geo:place:taxonomy``
    Add a form to record an analyst defined taxonomy of different places.

  ``geo:place``
    Add a ``type`` property to record the taxonomy of a place.

  ``inet:web:memb``
    This form has been deprecated.

  ``inet:web:member``
    Add a guid form that represents a web account's membership in a channel or group.

  ``media:news:taxonomy``
    Add a form to record an analyst defined taxonomy of different types or sources of news.

  ``media:news``
    Add a ``type`` property to record the taxonomy of the news.
    Add an ``ext:id`` property to record an external identifier provided by a publisher.

  ``pol:vitals``
    Add a guid form to record the vitals for a country.

  ``pol:country``
    Add ``names``, ``place``, ``dissolved`` and ``vitals`` secondary properties.
    The ``name`` is changed from a ``str`` to a ``geo:name`` type.
    Deprecate the ``pop`` secondary property.

  ``pol:candidate``
    Add an ``incumbent`` property to note if the candidate was an incumbent
    in a race.

  ``proj``
    Add missing docstrings to the ``proj`` model forms.

  ``risk:alert:taxonomy``
    Add a form to record an analyst defined taxonomy of alert types.

  ``risk:alert``
    The ``type`` property is changed from a ``str`` to the
    ``risk:alert:taxonomy`` type.

- Add ``**`` as a power operator for Storm expression syntax.
  (`#2827 <https://github.com/vertexproject/synapse/pull/2827>`_)
- Add a new test helper, ``synapse.test.utils.StormPkgTest`` to assist with
  testing Rapid Power-Ups.
  (`#2819 <https://github.com/vertexproject/synapse/pull/2819>`_)
- Add ``$lib.axon.metrics()`` to get the metrics from the Axon that the
  Cortex is connected to.
  (`#2818 <https://github.com/vertexproject/synapse/pull/2818>`_)
- Add ``pack()`` methods to the ``storm:auth:user`` and ``storm:auth:role``
  objects. This API returns the definitions of the User and Role objects.
  (`#2823 <https://github.com/vertexproject/synapse/pull/2823>`_)
- Change the Storm Package ``require`` values to log debug messages instead
  of raising exceptions if the requirements are not met. Add a
  ``$lib.pkg.deps()`` API that allows inspecting if a package has its
  dependencies met or has conflicts.
  (`#2820 <https://github.com/vertexproject/synapse/pull/2820>`_)

Bugfixes
--------
- Prevent ``None`` objects from being normalized as tag parts from variables
  in Storm.
  (`#2822 <https://github.com/vertexproject/synapse/pull/2822>`_)
- Avoid intermediate conversion to floats during storage operations related to
  Synapse Number objects in Storm.
  (`#2825 <https://github.com/vertexproject/synapse/pull/2825>`_)

Improved Documentation
----------------------
- Add Developer documentation for writing Rapid Power-Ups.
  (`#2803 <https://github.com/vertexproject/synapse/pull/2803>`_)
- Add the ``synapse.tests.utils`` package to the Synapse API autodocs.
  (`#2819 <https://github.com/vertexproject/synapse/pull/2819>`_)
- Update Devops documentation to note the storage requirements for taking
  backups of Synapse services.
  (`#2824 <https://github.com/vertexproject/synapse/pull/2824>`_)
- Update the Storm ``min`` and ``max`` command help to clarify their usage.
  (`#2826 <https://github.com/vertexproject/synapse/pull/2826>`_)

v2.106.0 - 2022-08-23
=====================

Features and Enhancements
-------------------------
- Add a new tool, ``synapse.tools.axon2axon``, for copying the data from one
  Axon to another Axon.
  (`#2813 <https://github.com/vertexproject/synapse/pull/2813>`_)
  (`#2816 <https://github.com/vertexproject/synapse/pull/2816>`_)

Bugfixes
--------
- Subquery filters did not update runtime variables in the outer scope. This
  behavior has been updated to make subquery filter behavior consistent with
  regular subqueries.
  (`#2815 <https://github.com/vertexproject/synapse/pull/2815>`_)
- Fix an issue with converting the Number Storm primitive into its Python
  primitive.
  (`#2811 <https://github.com/vertexproject/synapse/pull/2811>`_)

v2.105.0 - 2022-08-19
=====================

Features and Enhancements
-------------------------
- Add a Number primitive to Storm to facilitate fixed point math
  operations. Values in expressions which are parsed as floating
  point values will now be Numbers by default. Values can also
  be cast to Numbers with ``$lib.math.number()``.
  (`#2762 <https://github.com/vertexproject/synapse/pull/2762>`_)
- Add ``$lib.basex.encode()`` and ``$lib.basex.decode()`` for
  encoding and decoding strings using arbitrary charsets.
  (`#2807 <https://github.com/vertexproject/synapse/pull/2807>`_)
- The tag removal operator (``-#``) now accepts lists of tags
  to remove.
  (`#2808 <https://github.com/vertexproject/synapse/pull/2808>`_)
- Add a ``$node.difftags()`` API to calculate and optionally apply
  the difference between a list of tags and those present on a node.
  (`#2808 <https://github.com/vertexproject/synapse/pull/2808>`_)
- Scraped Ethereum addresses are now returned in their EIP55
  checksummed form. This change also applies to lookup mode.
  (`#2809 <https://github.com/vertexproject/synapse/pull/2809>`_)
- Updates to the ``mat``, ``ps``, and ``risk`` models.
  (`#2804 <https://github.com/vertexproject/synapse/pull/2804>`_)

  ``mass``
    Add a type for storing mass with grams as a base unit.

  ``ps:vitals``
    Add a form to record statistics and demographic data about a person
    or contact.

  ``ps:person``
    Add a ``vitals`` secondary property to record the most recent known
    vitals for the person.

  ``ps:contact``
    Add a ``vitals`` secondary property to record the most recent known
    vitals for the contact.

  ``risk:tool:taxonomy``
    Add a form to record an analyst defined taxonomy of different tools.

  ``risk:tool:software``
    Add a form to record software tools used in threat activity.

  ``risk:threat``
    Add ``reporter``, ``reporter:name``, ``org:loc``, ``org:names``,
    and ``goals`` secondary properties.

- Annotate the following light edges.
  (`#2804 <https://github.com/vertexproject/synapse/pull/2804>`_)

  ``uses``
    When used with ``risk:threat`` nodes, the edge indicates the target
    node is used by the source node.

Bugfixes
--------
- Fix language used in the ``model.deprecated.check`` command.
  (`#2806 <https://github.com/vertexproject/synapse/pull/2806>`_)
- Remove the ``-y`` switch in the ``count`` command.
  (`#2806 <https://github.com/vertexproject/synapse/pull/2806>`_)

v2.104.0 - 2022-08-09
=====================

Automatic Migrations
--------------------
- Migrate `crypto:x509:cert:serial` from `str` to `hex` type. Existing values
  which cannot be converted as integers or hex values will be moved into
  nodedata under the key ``migration:0_2_10`` as ``{'serial': value}``
  (`#2789 <https://github.com/vertexproject/synapse/pull/2789>`_)
- Migrate ``ps:contact:title`` to the ``ou:jobtitle`` type and create
  ``ou:jobtitle`` nodes.
  (`#2789 <https://github.com/vertexproject/synapse/pull/2789>`_)
- Correct hugenum property index values for values with more than
  28 digits of precision.
  (`#2766 <https://github.com/vertexproject/synapse/pull/2766>`_)
- See :ref:`datamigration` for more information about automatic migrations.

Features and Enhancements
-------------------------
- Updates to the ``crypto`` and ``ps`` models.
  (`#2789 <https://github.com/vertexproject/synapse/pull/2789>`_)

  ``crypto:x509:cert``
    The ``serial`` secondary property has been changed from a ``str`` to a
    ``hex`` type.

  ``ps:contact``
    The type of the ``title`` secondary property has been changed from a
    ``str`` to an ``ou:jobtitle``.

- Add ``$lib.hex.toint()``, ``$lib.hex.fromint()``, ``$lib.hex.trimext()``
  and ``$lib.hex.signext()`` Storm APIs for handling hex encoded integers.
  (`#2789 <https://github.com/vertexproject/synapse/pull/2789>`_)
- Add ``set()`` and ``setdefault()`` APIs on the SynErr exception class.
  Improve support for unpickling SynErr exceptions.
  (`#2797 <https://github.com/vertexproject/synapse/pull/2797>`_)
- Add logging configuration to methods which are called in spawned processes,
  and log exceptions occurring in the processes before tearing them down.
  (`#2795 <https://github.com/vertexproject/synapse/pull/2795>`_)

Bugfixes
--------
- BadTypeValu errors raised when normalizing a tag timestamp now include
  the name of the tag being set.
  (`#2797 <https://github.com/vertexproject/synapse/pull/2797>`_)
- Correct a CI issue that prevented the v2.103.0 Docker images from
  being published.
  (`#2798 <https://github.com/vertexproject/synapse/pull/2798>`_)

Improved Documentation
----------------------
- Update data model documentation.
  (`#2796 <https://github.com/vertexproject/synapse/pull/2796>`_)

v2.103.0 - 2022-08-05
=====================

Features and Enhancements
-------------------------
- Updates to the ``it``, ``ou``, and ``risk`` models.
  (`#2778 <https://github.com/vertexproject/synapse/pull/2778>`_)

  ``it:prod:soft``
    Add a ``techniques`` secondary property to record techniques employed by
    the author of the software.

  ``ou:campaign``
    Add a ``techniques`` secondary property to record techniques employed by
    the campaign.

  ``ou:org``
    Add a ``techniques`` secondary property to record techniques employed by
    the org.

  ``ou:technique``
    Add a form to record specific techniques used to achieve a goal.

  ``ou:technique:taxonomy``
    Add a form to record an analyst defined taxonomy of different techniques.

  ``risk:attack``
    Add a ``techniques`` secondary property to record techniques employed
    during the attack.
    Deprecate the following secondary properties, in favor of using light
    edges.

      - ``target``
      - ``target:host``
      - ``target:org``
      - ``target:person``
      - ``target:place``
      - ``used:email``
      - ``used:file``
      - ``used:host``
      - ``used:server``
      - ``used:software``
      - ``used:url``
      - ``used:vuln``
      - ``via:email``
      - ``via:ipv4``
      - ``via:ipv6``
      - ``via:phone``

  ``risk:compromise``
    Add a ``techniques`` secondary property to record techniques employed
    during the compromise.

  ``risk:threat``
    Add a form to record a threat cluster or subgraph of threat activity
    attributable to one group.

- Annotate the following light edges.
  (`#2778 <https://github.com/vertexproject/synapse/pull/2778>`_)

  ``targets``
    When used with ``ou:org``, ``ou:campaign``, ``risk:threat``, or
    ``risk:attack`` nodes, the edge indicates the target node was targeted
    by the source node.

  ``uses``
    When used with an ``ou:campaign`` or ``risk:attack`` node, the edge
    indicates the target node is used by the source node.

- Change the behavior of the Storm ``count`` command to consume nodes.
  If the previous behavior is desired, use the ``--yield`` option when
  invoking the ``count`` command.
  (`#2779 <https://github.com/vertexproject/synapse/pull/2779>`_)
- Add ``$lib.random.int()`` API to Storm for generating random integers.
  (`#2783 <https://github.com/vertexproject/synapse/pull/2783>`_)
- Add a new tool, ``synapse.tools.livebackup`` for taking a live backup of
  a service.
  (`#2788 <https://github.com/vertexproject/synapse/pull/2788>`_)
- The Storm ``$lib.jsonstor.cacheset()`` API now returns a dict containing the
  path and time. The ``$lib.jsonstor.cacheget()`` API now has an argument to
  retrieve the entire set of enveloped data.
  (`#2790 <https://github.com/vertexproject/synapse/pull/2790>`_)
- Add a HTTP 404 handler for the Axon ``v1/by/sha256/<sha256>`` endpoint which
  catches invalid ``<sha256>`` values.
  (`#2780 <https://github.com/vertexproject/synapse/pull/2780>`_)
- Add helper scripts for doing bulk Synapse Docker image builds and testing.
  (`#2716 <https://github.com/vertexproject/synapse/pull/2716>`_)
- Add ``aha:\\`` support to ``synapse.tools.csvtool``.
  (`#2791 <https://github.com/vertexproject/synapse/pull/2791>`_)

Bugfixes
--------
- Ensure that errors that occur when backing up a service are logged prior
  to tearing down the subprocess performing the backup.
  (`#2781 <https://github.com/vertexproject/synapse/pull/2781>`_)
- Add missing docstring for ``$lib.stix.import``.
  (`#2786 <https://github.com/vertexproject/synapse/pull/2786>`_)
- Allow setting tags on a Node from a Storm ``List`` object.
  (`#2782 <https://github.com/vertexproject/synapse/pull/2782>`_)

Improved Documentation
----------------------
- Remove ``synapse-google-ct`` from the list of Rapid Power-Ups.
  (`#2779 <https://github.com/vertexproject/synapse/pull/2779>`_)
- Add developer documentation for building Synapse Docker containers.
  (`#2716 <https://github.com/vertexproject/synapse/pull/2716>`_)
- Fix spelling errors in model documentation.
  (`#2782 <https://github.com/vertexproject/synapse/pull/2782>`_)

Deprecations
------------
- The ``vertexproject/synapse:master-py37`` and
  ``vertexproject/synapse:v2.x.x-py37`` Docker containers are no longer being
  built.
  (`#2716 <https://github.com/vertexproject/synapse/pull/2716>`_)

v2.102.0 - 2022-07-25
=====================

Features and Enhancements
-------------------------
- Updates to the ``crypto``, ``geo``, ``inet``, ``mat``, ``media``, ``ou``,
  ``pol``, and ``proj`` models.
  (`#2757 <https://github.com/vertexproject/synapse/pull/2757>`_)
  (`#2771 <https://github.com/vertexproject/synapse/pull/2771>`_)

  ``crypto:key``
    Add ``public:md5``, ``public:sha1``, and ``public:sha256`` secondary
    properties to record those hashes for the public key.
    Add ``private:md5``, ``private:sha1``, and ``private:sha256`` secondary
    properties to record those hashes for the public key.

  ``geo:nloc``
    The ``geo:nloc`` form has been deprecated.

  ``geo:telem``
    Add a new form to record a the location of a given node at a given time.
    This replaces the use of ``geo:nloc``.

  ``it:sec:c2:config``
    Add a ``proxies`` secondary property to record proxy URLS used to
    communicate to a C2 server.
    Add a ``listens`` secondary property to record urls the software should
    bind.
    Add a ``dns:resolvers`` secondary property to record DNS servers the
    software should use.
    Add a ``http:headers`` secondary property to record HTTP headers the
    software should use.

  ``it:exec:query``
    Add a new form to record an instance of a query executed on a host.

  ``it:query``
    Add a new form to record query strings.

  ``mat:type``
    Add a taxonomy type to record taxonomies of material specifications or
    items.

  ``mat:item``
    Add a ``type`` secondary property to record the item type.

  ``mat:spec``
    Add a ``type`` secondary property to record the item type.

  ``media:news``
    Add a ``publisher`` secondary property to record the org that published
    the news.
    Add a ``publisher:name`` secondary property to record the name of the org.
    Deprecate the ``org`` secondary property.

  ``ou:campaign``
    Add a ``conflict`` secondary property to record the primary conflict
    associated the campaign.

  ``ou:conflict``
    Add a new form to record a conflict between two or more campaigns which
    have mutually exclusive goals.

  ``ou:contribution``
    Add a new form to represent contributing material support to a campaign.

  ``pol:election``
    Add a new form to record an election.

  ``pol:race``
    Add a new form to record indivdual races in an election.

  ``pol:office``
    Add a new form to record an appointed or elected office.

  ``pol:term``
    Add a new form to record the term in office for an individual.

  ``pol:candidate``
    Add a form to record a candidate for a given race.

  ``pol:pollingplace``
    Add a form to record the polling locations for a given election.

  ``proj:ticket``
    Add a ``ext:creator`` secondary form to record contact information from
    and external system.

- Annotate the following light edges.
  (`#2757 <https://github.com/vertexproject/synapse/pull/2757>`_)

  ``about``
    A light edge created by the Storm ``note.add`` command, which records
    the relationship between a ``meta:note`` node and the target node.

  ``includes``
    When used with a ``ou:contribution`` node, the edge indicates the target
    node was the contribution made.

  ``has``
    When used with a ``meta:ruleset`` and ``meta:rule`` node, indicates
    the ruleset contains the rule.

  ``matches``
    When used with a ``meta:rule`` node, the edge indicates the target
    node matches the rule.

  ``refs``
    A light edge where the source node refers to the target node.

  ``seenat``
    When used with a ``geo:telem`` target node, the edge indicates the source
    node was seen a given location.

  ``uses``
    When used with a ``ou:org`` node, the edge indicates the target node
    is used by the organization.

- Commonly used light edges are now being annotated in the model, and are
  available through Cortex APIs which expose the data model.
  (`#2757 <https://github.com/vertexproject/synapse/pull/2757>`_)
- Make Storm command argument parsing errors into exceptions. Previously the
  argument parsing would cause the Storm runtime to be torn down with
  ``print`` messages, which could be missed. This now means that automations
  which have a invalid Storm command invocation will fail loudly.
  (`#2769 <https://github.com/vertexproject/synapse/pull/2769>`_)
- Allow a Storm API caller to set the task identifier by setting the ``task``
  value in the Storm ``opts`` dictionary.
  (`#2768 <https://github.com/vertexproject/synapse/pull/2768>`_)
  (`#2774 <https://github.com/vertexproject/synapse/pull/2774>`_)
- Add support for registering and exporting custom STIX objects with the
  ``$lib.stix`` Storm APIS.
  (`#2773 <https://github.com/vertexproject/synapse/pull/2773>`_)
- Add APIS and Storm APIs for enumerating mirrors that have been registered
  with AHA.
  (`#2760 <https://github.com/vertexproject/synapse/pull/2760>`_)

Bugfixes
--------
- Ensure that auto-adds are created when merging part of a View when using
  the Storm ``merge --apply`` command.
  (`#2770 <https://github.com/vertexproject/synapse/pull/2770>`_)
- Add missing support for handling timezone offsets without colon separators
  when normalizing ``time`` values. ``time`` values which contain timezone
  offsets and not enough data to resolve minute level resolution will now fail
  to parse.
  (`#2772 <https://github.com/vertexproject/synapse/pull/2772>`_)
- Fix an issue when normalizing ``inet:url`` values when the host value was
  the IPv4 address ``0.0.0.0``.
  (`#2771 <https://github.com/vertexproject/synapse/pull/2771>`_)
- Fix an issue with the Storm ``cron.list`` command, where the command failed
  to run when a user had been deleted.
  (`#2776 <https://github.com/vertexproject/synapse/pull/2776>`_)

Improved Documentation
----------------------
- Update the Storm user documentation to include the Embedded Property syntax,
  which is a shorthand (``::``) that can be used to reference properties on
  adjacent nodes.
  (`#2767 <https://github.com/vertexproject/synapse/pull/2767>`_)
- Update the Synapse Glossary.
  (`#2767 <https://github.com/vertexproject/synapse/pull/2767>`_)
- Update Devops documentation to clarify the Aha URLs which end with``...``
  are intentional.
  (`#2775 <https://github.com/vertexproject/synapse/pull/2775>`_)

v2.101.1 - 2022-07-14
=====================

Bugfixes
--------
- Fix an issue where the Storm ``scrape`` command could fail to run with
  inbound nodes.
  (`#2761 <https://github.com/vertexproject/synapse/pull/2761>`_)
- Fix broken links in documentation.
  (`#2763 <https://github.com/vertexproject/synapse/pull/2763>`_)
- Fix an issue with the Axon ``AxonHttpBySha256V1`` API handler related to
  detecting ``Range`` support in the Axon.
  (`#2764 <https://github.com/vertexproject/synapse/pull/2764>`_)


v2.101.0 - 2022-07-12
=====================

Automatic Migrations
--------------------
- Create nodes in the Cortex for the updated properties noted in the data
  model updates listed below.
- Axon indices are migrated to account for storing offset information to
  support the new offset and size API options.
- See :ref:`datamigration` for more information about automatic migrations.

Features and Enhancements
-------------------------
- Updates to the ``crypto``, ``infotech``, ``ps``, and ``transport`` models.
  (`#2720 <https://github.com/vertexproject/synapse/pull/2720>`_)
  (`#2738 <https://github.com/vertexproject/synapse/pull/2738>`_)
  (`#2739 <https://github.com/vertexproject/synapse/pull/2739>`_)
  (`#2747 <https://github.com/vertexproject/synapse/pull/2747>`_)

  ``crypto:smart:effect:minttoken``
    Add a new form to model smart contract effects which create
    non-fungible tokens.

  ``crypto:smart:effect:burntoken```
    Add a new form to model smart contract effects which destroy
    non-fungible tokens.

  ``crypto:smart:effect:proxytoken``
    Add a new form that tracks grants for a non-owner address the ability to
    manipulate a specific non-fungible token.

  ``crypto:smart:effect:proxytokenall``
    Add a new form that tracks grants for a non-owner address the ability to
    manipulate all of the non-fungible tokens.

  ``crypto:smart:effect:proxytokens``
    Add a new form that tracks grants for a non-owner address to manipulate
    fungible tokens.

  ``it:av:signame``
    Add a new form to track AV signature names. Migrate
    ``it:av:filehit:sig:name`` and ``it:av:sig:name`` to use the new form.

  ``it:exec:proc``
    Add a ``name`` secondary property to track the display name of a process.
    Add a ``path:base`` secondary property to track the basename of the
    executable for the process.

  ``ps:contact``
    Add an ``orgnames`` secondary property to track an array of orgnames
    associated with a contact.

  ``transport:sea:vessel``
    Add ``make`` and ``model`` secondary properties to track information
    about the vessel.

- Add a new Storm command, ``movenodes``, that can be used to move a node
  entirely from one layer to another.
  (`#2714 <https://github.com/vertexproject/synapse/pull/2714>`_)
- Add a new Storm library, ``$lib.gen``, to assist with creating nodes based
  on secondary property based deconfliction.
  (`#2754 <https://github.com/vertexproject/synapse/pull/2754>`_)
- Add a ``sorted()`` method to the ``storm:stat:tally`` object, to simplify
  handling of tallied data.
  (`#2748 <https://github.com/vertexproject/synapse/pull/2748>`_)
- Add a new Storm function, ``$lib.mime.html.totext()``, to extract inner tag
  text from HTML strings.
  (`#2744 <https://github.com/vertexproject/synapse/pull/2744>`_)
- Add Storm functions ``$lib.crypto.hashes.md5()``,
  ``$lib.crypto.hashes.sha1()``, ``$lib.crypto.hashes.sha256()`` and
  ``$lib.crypto.hashes.sha512()`` to allow hashing bytes directly in Storm.
  (`#2743 <https://github.com/vertexproject/synapse/pull/2743>`_)
- Add an ``Axon.csvrows()`` API for streaming CSV rows from an Axon, and a
  corresponding ``$lib.axon.csvrows()`` Storm API.
  (`#2719 <https://github.com/vertexproject/synapse/pull/2719>`_)
- Expand Synapse requirements to include updated versions of the
  ``pycryptome``, ``pygments``, and ``scalecodec`` modules.
  (`#2752 <https://github.com/vertexproject/synapse/pull/2752>`_)
- Add range support to ``Axon.get()`` to read bytes from a given offset and
  size. The ``/api/v1/axon/files/by/sha256/<SHA-256>`` HTTP API has been
  updated to support a ``Range`` header that accepts a ``bytes`` value to read
  a subset of bytes that way as well.
  (`#2731 <https://github.com/vertexproject/synapse/pull/2731>`_)
  (`#2755 <https://github.com/vertexproject/synapse/pull/2755>`_)
  (`#2758 <https://github.com/vertexproject/synapse/pull/2758>`_)

Bugfixes
--------
- Fix ``$lib.time.parse()`` when ``%z`` is used in the format specifier.
  (`#2749 <https://github.com/vertexproject/synapse/pull/2749>`_)
- Non-string form-data fields are now serialized as JSON when using the
  ``Axon.postfiles()`` API.
  (`#2751 <https://github.com/vertexproject/synapse/pull/2751>`_)
  (`#2759 <https://github.com/vertexproject/synapse/pull/2759>`_)
- Fix a byte-alignment issue in the ``Axon.readlines()`` API.
  (`#2719 <https://github.com/vertexproject/synapse/pull/2719>`_)


v2.100.0 - 2022-06-30
=====================

Features and Enhancements
-------------------------
- Support parsing CVSS version 3.1 prefix values.
  (`#2732 <https://github.com/vertexproject/synapse/pull/2732>`_)

Bugfixes
--------
- Normalize tag value lists in ``snap.addTag()`` to properly handle JSON
  inputs from HTTP APIs.
  (`#2734 <https://github.com/vertexproject/synapse/pull/2734>`_)
- Fix an issue that allowed multiple concurrent streaming backups to occur.
  (`#2725 <https://github.com/vertexproject/synapse/pull/2725>`_)

Improved Documentation
----------------------
- Add an entry to the devops task documentation for trimming Nexus logs.
  (`#2730 <https://github.com/vertexproject/synapse/pull/2730>`_)
- Update the list of available Rapid Power-Ups.
  (`#2735 <https://github.com/vertexproject/synapse/pull/2735>`_)


v2.99.0 - 2022-06-23
====================

Features and Enhancements
-------------------------
- Add an extensible STIX 2.1 import library, ``$lib.stix.import``. The
  function ``$lib.stix.import.ingest()`` can be used to STIX bundles into a
  Cortex via Storm.
  (`#2727 <https://github.com/vertexproject/synapse/pull/2727>`_)
- Add a Storm ``uptime`` command to display the uptime of a Cortex or a Storm
  Service configured on the Cortex.
  (`#2728 <https://github.com/vertexproject/synapse/pull/2728>`_)
- Add ``--view`` and ``--optsfile`` arguments to ``synapse.tools.csvtool``.
  (`#2726 <https://github.com/vertexproject/synapse/pull/2726>`_)

Bugfixes
--------
- Fix an issue getting the maximum available memory for a host running with
  Linux cgroupsv2 apis.
  (`#2728 <https://github.com/vertexproject/synapse/pull/2728>`_)

v2.98.0 - 2022-06-17
====================

Features and Enhancements
-------------------------
- Updates to the ``econ`` model.
  (`#2717 <https://github.com/vertexproject/synapse/pull/2717>`_)

  ``econ:acct:balance``
    Add ``total:received`` and ``total:sent`` properties to record total
    currency sent and received by the account.

- Add additional debug logging for Aha provisioning.
  (`#2722 <https://github.com/vertexproject/synapse/pull/2722>`_)
- Adjust whitespace requirements on Storm grammar related to tags.
  (`#2721 <https://github.com/vertexproject/synapse/pull/2721>`_)
- Always run the function provided to the Storm ``divert`` command per node.
  (`#2718 <https://github.com/vertexproject/synapse/pull/2718>`_)

Bugfixes
--------
- Fix an issue that prevented function arguments named ``func`` in Storm
  function calls.
  (`#2715 <https://github.com/vertexproject/synapse/pull/2715>`_)
- Ensure that active coroutines have been cancelled when changing a Cell from
  active to passive status; before starting any passive coroutines.
  (`#2713 <https://github.com/vertexproject/synapse/pull/2713>`_)
- Fix an issue where ``Nexus._tellAhaReady`` was registering with the Aha
  service when the Cell did not have a proper Aha service name set.
  (`#2723 <https://github.com/vertexproject/synapse/pull/2723>`_)


v2.97.0 - 2022-06-06
====================

Features and Enhancements
-------------------------
- Add an ``/api/v1/aha/provision/service`` HTTP API to the Aha service. This
  can be used to generate ``aha:provision`` URLs.
  (`#2707 <https://github.com/vertexproject/synapse/pull/2707>`_)
- Add ``proxy`` options to ``$lib.inet.http`` Storm APIs, to allow an admin
  user to specify an alternative (or to disable) proxy setting.
  (`#2706 <https://github.com/vertexproject/synapse/pull/2706>`_)
- Add a ``--tag`` and ``--prop`` option to the Storm ``diff`` command. Update
  the Storm ``merge`` command examples to show more real-world use cases.
  (`#2710 <https://github.com/vertexproject/synapse/pull/2710>`_)
- Add the ability to set the layers in a non-forked view with the
  ``$view.set(layers, $iden)`` API on the Storm view object.
  (`#2711 <https://github.com/vertexproject/synapse/pull/2711>`_)
- Improve Storm parser logic for handling list and expression syntax.
  (`#2698 <https://github.com/vertexproject/synapse/pull/2698>`_)
  (`#2708 <https://github.com/vertexproject/synapse/pull/2708>`_)

Bugfixes
--------
- Improve error handling of double quoted strings in Storm when null
  characters are present in the raw query string. This situation now raises a
  BadSyntax error instead of an opaque Python ValueError.
  (`#2709 <https://github.com/vertexproject/synapse/pull/2709>`_)
- Fix unquoted JSON keys which were incorrectly allowed in Storm JSON style
  expression syntax.
  (`#2698 <https://github.com/vertexproject/synapse/pull/2698>`_)
- When merging layer data, add missing permission checks for light edge and
  node data changes.
  (`#2671 <https://github.com/vertexproject/synapse/pull/2671>`_)


v2.96.0 - 2022-05-31
====================

Features and Enhancements
-------------------------
- Updates to the ``transport`` model.
  (`#2697 <https://github.com/vertexproject/synapse/pull/2697>`_)

  ``velocity``
    Add a new base type to record velocities in millimeters/second.

  ``transport:direction``
    Add a new type to indicate a direction of movement with respect to true
    North.

  ``transport:air:telem``
    Add ``:course`` and ``:heading`` properties to record the direction of travel.
    Add ``:speed``, ``:airspeed`` and ``:verticalspeed`` properties to record
    the speed of travel.

  ``transport:sea:telem``
    Add ``:course`` and ``:heading`` properties to record the direction of travel.
    Add a ``:speed`` property to record the speed of travel.
    Add ``:destination``, ``:destination:name`` and ``:destination:eta`` to record
    information about the destination.

- Restore the precedence of environment variables over ``cell.yaml`` options
  during Cell startup. API driven overrides are now stored in the
  ``cell.mods.yaml`` file.
  (`#2699 <https://github.com/vertexproject/synapse/pull/2699>`_)
- Add ``--dmon-port`` and ``--https-port`` options to the
  ``synapse.tools.aha.provision.service`` tool in order to specify fixed
  listening ports during provisioning.
  (`#2703 <https://github.com/vertexproject/synapse/pull/2703>`_)
- Add the ability of ``synapse.tools.moduser`` to set user passwords.
  (`#2695 <https://github.com/vertexproject/synapse/pull/2695>`_)
- Restore the call to the ``recover()`` method on the Nexus during Cell
  startup.
  (`#2701 <https://github.com/vertexproject/synapse/pull/2701>`_)
- Add ``mesg`` arguments to ``NoSuchLayer`` exceptions.
  (`#2696 <https://github.com/vertexproject/synapse/pull/2696>`_)
- Make the LMDB slab startup more resilient to a corrupted ``cell.opts.yaml``
  file.
  (`#2694 <https://github.com/vertexproject/synapse/pull/2694>`_)

Bugfixes
--------
- Fix missing variable checks in Storm.
  (`#2702 <https://github.com/vertexproject/synapse/pull/2702>`_)

Improved Documentation
----------------------
- Add a warning to the deployment guide about using Docker on Mac OS.
  (`#2700 <https://github.com/vertexproject/synapse/pull/2700>`_)

v2.95.1 - 2022-05-24
====================

Bugfixes
--------
- Fix a regression in the Telepath ``aha://`` update from ``v2.95.0``.
  (`#2693 <https://github.com/vertexproject/synapse/pull/2693>`_)


v2.95.0 - 2022-05-24
====================

Features and Enhancements
-------------------------
- Add a ``search`` mode to Storm. The ``search`` mode utilizes the Storm
  search interface to lift nodes. The ``lookup`` mode no longer uses the
  search interface.
  (`#2689 <https://github.com/vertexproject/synapse/pull/2689>`_)
- Add a ``?mirror=true`` flag to ``aha://`` Telepath URLs which will cause
  the Aha service lookups to prefer using a mirror of the service rather than
  the leader.
  (`#2681 <https://github.com/vertexproject/synapse/pull/2681>`_)
- Add ``$lib.inet.http.urlencode()`` and ``$lib.inet.http.urldecode()`` Storm
  APIs for handling URL encoding.
  (`#2688 <https://github.com/vertexproject/synapse/pull/2688>`_)
- Add type validation for all Cell configuration options throughout the
  lifetime of the Cell and all operations which modify its configuration
  values. This prevents invalid values from being persisted on disk.
  (`#2687 <https://github.com/vertexproject/synapse/pull/2687>`_)
  (`#2691 <https://github.com/vertexproject/synapse/pull/2691>`_)

Bugfixes
--------
- Fix an issue where the ``=`` sign in the Storm grammar was assigned an
  anonymous terminal name by the grammar parser. This caused an issue with
  interpreting various syntax errors.
  (`#2690 <https://github.com/vertexproject/synapse/pull/2690>`_)


v2.94.0 - 2022-05-18
====================

Automatic Migrations
--------------------
- Re-normalize the migrated properties noted in the data model updates listed
  below. See :ref:`datamigration` for more information about automatic
  migrations.

Features and Enhancements
-------------------------
- Updates to the ``crypto``, ``infotech``, ``org``, and ``person`` models.
  (`#2620 <https://github.com/vertexproject/synapse/pull/2620>`_)
  (`#2684 <https://github.com/vertexproject/synapse/pull/2684>`_)

  ``crypto:algorithm``
    Add a form to represent a named cryptography algorithm.

  ``crypto:key``
    Add a form to represent a cryptographic key and algorithm.

  ``crypto:smart:effect:transfertoken``
    Add a form to represent the effect of transferring ownership of a
    non-fungible token.

  ``crypto:smart:effect:transfertokens``
    Add a form to represent the effect of transferring multiple fungible
    tokens.

  ``crypto:smart:effect:edittokensupply``
    Add a form to represent the increase or decrease in the supply of
    fungible tokens.

  ``it:prod:softname``
    Add a form to represent a software name.

  ``it:host``
    Add a ``:os:name`` secondary property.

  ``it:mitre:attack:software``
    Migrate the ``:name`` and ``:names`` properties to ``it:prod:softname``
    type.

  ``it:prod:soft``
    Migrate the ``:name`` and ``:names`` properties to ``it:prod:softname``
    type.

  ``it:prod:softver``
    Deprecate the ``:software:name`` property.
    Migrate the ``:name`` and ``:names`` properties to ``it:prod:softname``
    type.

  ``it:app:yara:rule``
    Add a ``:family`` property to represent the software family the rule is
    designed to detect.

  ``it:sec:c2:config``
    Add a form to represent C2 configuration data.

  ``ou:campaign``
    Add a ``:org:name`` property to represent the name of the organization
    responsible the campaign.
    Add a ``:org:fqdn`` property to represent the fqdn of the organization
    responsible the campaign.
    Add a ``:team`` property to represent the team responsible for the
    campaign.

  ``ou:team``
    Add a form to represent a team within an organization.

  ``ou:industry``
    Migrate the ``:name`` property to ``ou:industryname`` type.
    Add a ``:names`` property for alternative names.

  ``ou:industryname``
    Add a form to represent the name of an industry.

  ``ou:position``
    Add a ``:team`` property to represent the team associated with a given
    position.

  ``ps:contact``
    Add a ``:crypto:address`` property to represent the crypto currency
    address associated with the contact.

- Add ``$lib.copy()`` to Storm. This allows making copies of objects which
  are compatible with being serialized with msgpack.
  (`#2678 <https://github.com/vertexproject/synapse/pull/2678>`_)
- Remove `print` events from the Storm `limit` command.
  (`#2674 <https://github.com/vertexproject/synapse/pull/2674>`_)

Bugfixes
--------
- Fix an issue where client certificates presented in Telepath ``ssl``
  connections could fallback to resolving users by a prefix. This was not
  intended to be allowed when client certificates are used with Telepath.
  (`#2675 <https://github.com/vertexproject/synapse/pull/2675>`_)
- Fix an issue where ``node:del`` triggers could fail to fire when adding
  nodeedits directly to a view or snap.
  (`#2654 <https://github.com/vertexproject/synapse/pull/2654>`_)
- Fix header escaping when generating autodoc content for Synapse Cells.
  (`#2677 <https://github.com/vertexproject/synapse/pull/2677>`_)
- Assorted unit tests fixes to make tests more stable.
  (`#2680 <https://github.com/vertexproject/synapse/pull/2680>`_)
- Fix an issue with Storm function argument parsing.
  (`#2685 <https://github.com/vertexproject/synapse/pull/2685>`_)

Improved Documentation
----------------------
- Add an introduction to Storm libraries and types.
  (`#2670 <https://github.com/vertexproject/synapse/pull/2670>`_)
  (`#2683 <https://github.com/vertexproject/synapse/pull/2683>`_)
- Fix small typos and corrections in the devops documentation.
  (`#2673 <https://github.com/vertexproject/synapse/pull/2673>`_)


v2.93.0 - 2022-05-04
====================

Features and Enhancements
-------------------------
- Updates to the ``inet`` and ``infotech`` models.
  (`#2666 <https://github.com/vertexproject/synapse/pull/2666>`_)

  ``:sandbox:file``
      Add a ``sandbox:file`` property to record an initial sample from a
      sandbox environment to the following forms:

        ``it:exec:proc``
        ``it:exec:thread``
        ``it:exec:loadlib``
        ``it:exec:mmap``
        ``it:exec:mutex``
        ``it:exec:pipe``
        ``it:exec:url``
        ``it:exec:bind``
        ``it:exec:file:add``
        ``it:exec:file:del``
        ``it:exec:file:read``
        ``it:exec:file:write``
        ``it:exec:reg:del``
        ``it:exec:reg:get``
        ``it:exec:reg:set``


  ``it:host:activity``
    Update the interface to add a ``sandbox:file`` property to record an
    initial sample from a sandbox environment.

- Changed primary Storm parser to a LALR compatible syntax to gain 80x speed
  up in parsing Storm queries
  (`#2649 <https://github.com/vertexproject/synapse/pull/2649>`_)
- Added service provisioning API to AHA service and associated tool
  ``synapse.tools.aha.provision.service`` and documentation to make
  it easy to bootstrap Synapse services using service discovery and
  SSL client-side certificates to identify service accounts.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added user provisioning API to AHA service and associated tools
  ``synapse.tools.aha.provision.user`` and ``synapse.tools.aha.enroll``
  to make it easy to bootstrap new users with SSL client-side certificates
  and AHA service discovery configuration.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added automatic mirror initialization logic to Synapse services to
  enable new mirrors to be initilized dynamically via AHA provisioning
  rather than from a pre-existing backup.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added ``handoff()`` API to Synapse services to allow mirrors to be
  gracefully promoted to leader.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added ``synapse.tools.promote`` to allow easy promotion of mirror to
  leader using the new ``handoff()`` API.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added ``aha:provision`` configuration to Synapse services to allow
  them to automatically provision and self-configure using AHA.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Adjusted Synapse service configuration preference to allow runtime settings
  to be stored in ``cell.yaml``.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added optional ``certhash`` parameter to telepath ``ssl://`` URLs to
  allow cert-pinning behavior and automatic trust of provisioning URLs.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added ``synapse.tools.moduser`` and ``synapse.tools.modrole`` commands
  to modernize and ease user/role management from within Synapse service
  docker containers.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Add ``$lib.jsonstor.cacheget()`` and ``lib.jsonstor.cacheset()`` functions
  in Storm to easily implement data caching in the JSONStor.
  (`#2662 <https://github.com/vertexproject/synapse/pull/2662>`_)
- Add a ``params`` option to ``$lib.inet.http.connect()`` to pass parameters
  when creating Websocket connections in Storm.
  (`#2664 <https://github.com/vertexproject/synapse/pull/2664>`_)

Bugfixes
--------
- Added ``getCellRunId()`` API to Synapse services to allow them to detect
  incorrect mirror configurations where they refer to themselves.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Ensure that CLI history files can be read and written upon
  starting interactive CLI tools.
  (`#2660 <https://github.com/vertexproject/synapse/pull/2660>`_)
- Assorted unit tests fixes to make tests more stable.
  (`#2656 <https://github.com/vertexproject/synapse/pull/2656>`_)
  (`#2665 <https://github.com/vertexproject/synapse/pull/2665>`_)
- Fix several uses of Python features which are formally deprecated
  and may be removed in future Python versions.
  (`#2668 <https://github.com/vertexproject/synapse/pull/2668>`_)

Improved Documentation
----------------------
- Added new Deployment Guide with step-by-step production ready deployment
  instructions
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Refactored Devops Guide to give task-oriented instructions on performing
  common devops tasks.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added new minimal Admin Guide as a place for documenting Cortex admin tasks.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Updated Getting Started to direct users to synapse-quickstart instructions.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Added ``easycert`` tool documentation.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Removed ``cmdr`` tool documentation to emphasize newer tools such as
  ``storm``.
  (`#2641 <https://github.com/vertexproject/synapse/pull/2641>`_)
- Update the list of available Advanced and Rapid Power-Ups.
  (`#2667 <https://github.com/vertexproject/synapse/pull/2667>`_)


v2.92.0 - 2022-04-28
====================

Features and Enhancements
-------------------------
- Update the allowed versions of the ``pyopenssl`` and ``pytz`` libraries.
  (`#2657 <https://github.com/vertexproject/synapse/pull/2657>`_)
  (`#2658 <https://github.com/vertexproject/synapse/pull/2658>`_)

Bugfixes
--------
- When setting ival properties, they are now properly merged with existing
  values. This only affected multi-layer views.
  (`#2655 <https://github.com/vertexproject/synapse/pull/2655>`_)


v2.91.1 - 2022-04-24
====================

Bugfixes
--------
- Fix a parsing regression in inet:url nodes related to unencoded "@" symbols
  in URLs.
  (`#2653 <https://github.com/vertexproject/synapse/pull/2653>`_)


v2.91.0 - 2022-04-21
====================

Features and Enhancements
-------------------------
- Updates to the ``inet`` and ``infotech`` models.
  (`#2634 <https://github.com/vertexproject/synapse/pull/2634>`_)
  (`#2644 <https://github.com/vertexproject/synapse/pull/2644>`_)
  (`#2652 <https://github.com/vertexproject/synapse/pull/2652>`_)

  ``inet:url``
    The ``inet:url`` type now recognizes various ``file:///`` values from
    RFC 8089.

  ``it:sec:cve``
    The ``it:sec:cve`` type now replaces various Unicode dashes with hyphen
    characters when norming. This allows a wider range of inputs to be
    accepted for the type. Scrape related APIs have also been updated to
    match on this wider range of inputs.

- The Cell now uses ``./backup`` as a default path for storing backups in, if
  the ``backup:dir`` path is not set.
  (`#2648 <https://github.com/vertexproject/synapse/pull/2648>`_)
- Add POSIX advisory locking around the Cell ``cell.guid`` file, to prevent
  multiple processes from attempting to start a Cell from the same directory.
  (`#2642 <https://github.com/vertexproject/synapse/pull/2642>`_)
- Change the default ``SLAB_COMMIT_WARN`` time from 5 seconds to 1 second, in
  order to quickly identify slow storage performance.
  (`#2630 <https://github.com/vertexproject/synapse/pull/2630>`_)
- Change the Cell ``iterBackupArchive`` and ``iterNewBackupArchive`` routines
  to always log exceptions they encounter, and report the final log message
  at the appropriate log level for success and failure.
  (`#2629 <https://github.com/vertexproject/synapse/pull/2629>`_)
- When normalizing the ``str`` types, when ``onespace`` is specified, we skip
  the ``strip`` behavior since it is redundant.
  (`#2635 <https://github.com/vertexproject/synapse/pull/2635>`_)
- Log exceptions raised by Cell creation in ``initFromArgv``. Catch
  ``lmdb.LockError`` when opening a LMDB database and re-raise an exception
  with a clear error message.
  (`#2638 <https://github.com/vertexproject/synapse/pull/2638>`_)
- Update schema validation for Storm packages to ensure that cmd arguments do
  not have excess fields in them.
  (`#2650 <https://github.com/vertexproject/synapse/pull/2650>`_)

Bugfixes
--------
- Adjust comma requirements for the JSON style list and dictionary expressions
  in Storm.
  (`#2636 <https://github.com/vertexproject/synapse/pull/2636>`_)
- Add Storm query logging in a code execution path where it was missing.
  (`#2647 <https://github.com/vertexproject/synapse/pull/2647>`_)
- Tuplify the output of ``synapse.tools.genpkg.loadPkgProto`` to ensure that
  Python list constructs ``[...]`` do not make it into Power-Up documentation.
  (`#2646 <https://github.com/vertexproject/synapse/pull/2646>`_)
- Fix an issue with heavy Stormtypes objects where caching was preventing
  some objects from behaving in a dynamic fashion as they were intended to.
  (`#2640 <https://github.com/vertexproject/synapse/pull/2640>`_)
- In norming ``int`` values, when something is outside of the minimum or
  maximum size of the type, we now include the string representation of the
  valu instead of the raw value.
  (`#2643 <https://github.com/vertexproject/synapse/pull/2643>`_)
- Raise a ``NotReady`` exception when a client attempts to resolve an
  ``aha://`` URL and there have not been any ``aha`` servers registered.
  (`#2645 <https://github.com/vertexproject/synapse/pull/2645>`_)

Improved Documentation
----------------------
- Update Storm command reference to add additional commands.
  (`#2633 <https://github.com/vertexproject/synapse/pull/2633>`_)
- Expand Stormtypes API documentation.
  (`#2637 <https://github.com/vertexproject/synapse/pull/2637>`_)
  (`#2639 <https://github.com/vertexproject/synapse/pull/2639>`_)


v2.90.0 - 2022-04-04
====================

Features and Enhancements
-------------------------
- Updates to the ``meta`` and ``infotech`` models.
  (`#2624 <https://github.com/vertexproject/synapse/pull/2624>`_)

  ``meta:rule``
    Add a new form for generic rules, which should be linked to
    the nodes they match with a ``matches`` light edge.

  ``meta:ruleset``
    Add ``:author``, ``:created``, and ``:updated`` secondary properties.

  ``it:app:yara:rule``
    Add ``:created`` and ``:updated`` secondary properties.

- Add a new Docker image ``vertexproject/synapse-jsonstor``.
  (`#2627 <https://github.com/vertexproject/synapse/pull/2627>`_)

- Allow passing a version requirement string to ``$lib.import()``.
  (`#2626 <https://github.com/vertexproject/synapse/pull/2626>`_)

Bugfixes
--------
- Fix an issue where using a regex lift on an array property could
  incorrectly yield the same node multiple times.
  (`#2625 <https://github.com/vertexproject/synapse/pull/2625>`_)

Improved Documentation
----------------------
- Update documentation regarding mirroring to be clearer about
  whether a given cell supports it.
  (`#2619 <https://github.com/vertexproject/synapse/pull/2619>`_)


v2.89.0 - 2022-03-31
====================

Features and Enhancements
-------------------------
- Update the ``meta`` model.
  (`#2621 <https://github.com/vertexproject/synapse/pull/2621>`_)

  ``meta:ruleset``
    Add a new form to denote the collection of a set of nodes representing
    rules, which should be linked together with a ``has`` light edge.

- Add additional filter options for the Storm ``merge`` command.
  (`#2615 <https://github.com/vertexproject/synapse/pull/2615>`_)
- Update the ``BadSyntaxError`` exception thrown when parsing Storm queries to
  additionally include line and column when available. Fix an issue
  where a ``!`` character being present in the exception text could truncate
  the output.
  (`#2618 <https://github.com/vertexproject/synapse/pull/2618>`_)


v2.88.0 - 2022-03-23
====================

Automatic Migrations
--------------------
- Re-normalize the ``geo:place:name``, ``crypto:currency:block:hash``, and
  ``crypto:currency:transaction:hash`` values to account for their modeling
  changes. Migrate ``crypto:currency:transaction:input`` and
  ``crypto:currency:transaction:output`` values to the secondary properties
  on the respective ``crypto:payment:input`` and ``crypto:payment:output``
  nodes to account for the modeling changes. Make ``geo:name`` nodes for
  ``geo:place:name`` secondary properties to account for the modeling changes.
  See :ref:`datamigration` for more information about automatic
  migrations.

Features and Enhancements
-------------------------
- Several updates for the ``crypto``, ``geospace``, ``inet``, and ``meta``
  models.
  (`#2594 <https://github.com/vertexproject/synapse/pull/2594>`_)
  (`#2608 <https://github.com/vertexproject/synapse/pull/2608>`_)
  (`#2611 <https://github.com/vertexproject/synapse/pull/2611>`_)
  (`#2616 <https://github.com/vertexproject/synapse/pull/2616>`_)

  ``crypto:payment:input``
    Add a secondary property ``:transaction`` to denote the transaction
    for the payment.

  ``crypto:payment:output``
    Add a secondary property ``:transaction`` to denote the transaction
    for the payment.

  ``crypto:currency:block``
    Change the type of the ``:hash`` property from a ``0x`` prefixed ``str``
    to a ``hex`` type.

  ``crypto:currency:transaction``
    Change the type of the ``:hash`` property from a ``0x`` prefixed ``str``
    to a ``hex`` type.
    Deprecate the ``:inputs`` and ``:outputs`` secondary properties.

  ``geo:place``
    Change the type of the ``:name`` secondary property to ``geo:name``.

  ``inet:web:channel``
    Add a new form to denote a channel within a web service or instance.

  ``inet:web:instance``
    Add a new form to track an instance of a web service, such as a channel
    based messaging platform.

  ``inet:web:mesg``
    Add ``:channel``, ``:place``, and ``:place:name`` secondary properties.

  ``inet:web:post``
    Add ``:channel`` and ``:place:name`` secondary properties.

  ``meta:event``
    Add a new form to denote an analytically relevant event in a curated
    timeline.

  ``meta:event:taxonomy``
    Add a new form to represent a taxonomy of ``meta:event:type`` values.

  ``meta:timeline``
    Add a new form to denote a curated timeline of analytically relevant
    events.

  ``meta:timeline:taxonomy``
    Add a new form to represent a taxonomy of ``meta:timeline:type`` values.

- Add support for ``$lib.len()`` to count the length of emitter or generator
  functions.
  (`#2603 <https://github.com/vertexproject/synapse/pull/2603>`_)
- Add support for scrape APIs to handle text that has been defanged with
  ``\\.`` characters.
  (`#2605 <https://github.com/vertexproject/synapse/pull/2605>`_)
- Add a ``nomerge`` option to View objects that can be set to prevent merging
  a long lived fork.
  (`#2614 <https://github.com/vertexproject/synapse/pull/2614>`_)
- Add ``liftByProp()`` and ``liftByTag()`` methods to the Stormtypes
  ``storm:layer`` objects. These allow lifting of nodes based on data stored
  in a specific layer.
  (`#2613 <https://github.com/vertexproject/synapse/pull/2613>`_)
- Expand Synapse requirements to include updated versions of the ``pygments``
  library.
  (`#2602 <https://github.com/vertexproject/synapse/pull/2602>`_)

Improved Documentation
----------------------
- Fix the example regular expressions used in the ``$lib.scrape.genMatches()``
  Storm library API examples.
  (`#2606 <https://github.com/vertexproject/synapse/pull/2606>`_)


v2.87.0 - 2022-03-18
====================

Features and Enhancements
-------------------------
- Several updates for the ``inet`` and ``meta`` models.
  (`#2589 <https://github.com/vertexproject/synapse/pull/2589>`_)
  (`#2592 <https://github.com/vertexproject/synapse/pull/2592>`_)

  ``inet:ssl:jarmhash``
    Add a form to record JARM hashes.

  ``inet:ssl:jarmsample``
    Add a form to record JARM hashes being present on a server.

  ``meta:note``
    Add a form for recording free text notes.

- Update the Synapse docker containers to be built from a Ubuntu based image,
  instead of a Debian based image.
  (`#2596 <https://github.com/vertexproject/synapse/pull/2596>`_)
- Add a Storm ``note.add`` command that creates a ``meta:note`` node to record
  freeform text, and links that node to the input nodes using a ``about`` light
  edge.
  (`#2592 <https://github.com/vertexproject/synapse/pull/2592>`_)
- Support non-writeable or non-existing directories within Synapse ``certdir``
  directories.
  (`#2590 <https://github.com/vertexproject/synapse/pull/2590>`_)
- Add an optional ``tick`` argument to the
  ``synapse.lib.lmdbslab.Hist.add()`` function. This is exposed internally
  for Axon implementations to use.
  (`#2593 <https://github.com/vertexproject/synapse/pull/2593>`_)
- Expand Synapse requirements to include updated versions of the
  ``pycryptome``, ``pygments``, ``scalecodec`` and ``xxhash`` modules.
  (`#2598 <https://github.com/vertexproject/synapse/pull/2598>`_)

Bugfixes
--------
- Fix an issue where the StormDmon stop/start status was not properly being
  updated in the runtime object, despite being properly updated in the Hive.
  (`#2598 <https://github.com/vertexproject/synapse/pull/2598>`_)
- Calls to ``addUnivProp()`` APIs when the universal property name already
  exists now raise a ``DupPropName`` exception.
  (`#2601 <https://github.com/vertexproject/synapse/pull/2601>`_)


v2.86.0 - 2022-03-09
====================

Automatic Migrations
--------------------
- Migrate secondary properties in Cortex nodes which use ``hugenum`` type to
  account for updated ranges. See :ref:`datamigration` for more
  information about automatic migrations.

Features and Enhancements
-------------------------
- Extend the number of decimal places the ``hugenum`` type can store to 24
  places, with a new maximum value of 730750818665451459101842.
  (`#2584 <https://github.com/vertexproject/synapse/pull/2584>`_)
  (`#2586 <https://github.com/vertexproject/synapse/pull/2586>`_)
- Update ``fastjsonschema`` to version ``2.15.3``.
  (`#2581 <https://github.com/vertexproject/synapse/pull/2581>`_)

Bugfixes
--------
- Add missing read-only flags to secondary properties of Comp type forms which
  were computed from the primary property of the node. This includes the
  following:
  (`#2587 <https://github.com/vertexproject/synapse/pull/2587>`_)

    - ``crypto:currency:address:coin``
    - ``crypto:currency:address:iden``
    - ``crypto:currency:block:coin``
    - ``crypto:currency:block:offset``
    - ``crypto:currency:client:coinaddr``
    - ``crypto:currency:client:inetaddr``
    - ``crypto:currency:smart:token:contract``
    - ``crypto:currency:smart:token:tokenid``
    - ``crypto:x509:revoked:crl``
    - ``crypto:x509:revoked:cert``
    - ``crypto:x509:signedfile:cert``
    - ``crypto:x509:signedfile:file``
    - ``econ:acquired:item``
    - ``econ:acquired:purchase``
    - ``inet:dns:query:client``
    - ``inet:dns:query:name``
    - ``inet:dns:query:type``
    - ``inet:whois:contact:type``
    - ``inet:wifi:ap:bssid``
    - ``inet:wifi:ap:ssid``
    - ``mat:itemimage:file``
    - ``mat:itemimage:item``
    - ``mat:specimage:file``
    - ``mat:specimage:spec``
    - ``ou:id:number:type``
    - ``ou:id:number:value``
    - ``ou:hasgoal:goal``
    - ``ou:hasgoal:org``
    - ``tel:mob:cell:carrier``
    - ``tel:mob:cell:carrier:mcc``
    - ``tel:mob:cell:carrier:mnc``
    - ``tel:mob:cell:cid``
    - ``tel:mob:cell:lac``

- Fix an issue where Layers configured with writeback mirrors did not properly
  handle results which did not have any changes.
  (`#2583 <https://github.com/vertexproject/synapse/pull/2583>`_)

Improved Documentation
----------------------
- Fix spelling issues in documentation and API docstrings.
  (`#2582 <https://github.com/vertexproject/synapse/pull/2582>`_)
  (`#2585 <https://github.com/vertexproject/synapse/pull/2585>`_)


v2.85.1 - 2022-03-03
====================

Bugfixes
--------
- Fix a permission enforcement issue in autoadd mode that allowed
  users with view read permissions to add automatically detected and
  validated nodes but make no further edits.
  (`#2579 <https://github.com/vertexproject/synapse/pull/2579>`_)
- Log errors encountered in the Layer mirror loop which don't have a
  local caller waiting on the change.
  (`#2580 <https://github.com/vertexproject/synapse/pull/2580>`_)


v2.85.0 - 2022-03-03
====================

Features and Enhancements
-------------------------

- Several updates for the ``crypto``, ``geo``, ``inet``, ``it``, ``ps`` and
  ``risk`` models.
  (`#2570 <https://github.com/vertexproject/synapse/pull/2570>`_)
  (`#2573 <https://github.com/vertexproject/synapse/pull/2573>`_)
  (`#2574 <https://github.com/vertexproject/synapse/pull/2574>`_)

  ``crypto:payment:input``
    Add a new form to record payments made into a transaction.

  ``crypto:payment:output``
    Add a new form to record payments receieved from a transaction.

  ``crypto:currency:transaction``
    Add ``inputs`` and ``outputs`` array secondary properties to record inputs
    and outputs for a given transaction.

  ``geo:name``
    Add a new form representing an unstructured place name or address.

  ``geo:place``
    Add a ``names`` secondary property which is an array of ``geo:name``
    values.

  ``inet:flow``
    Add ``dst:txcount``, ``src:txcount``, ``tot:txcount`` and ``tot:txbytes``
    secondary properties.

  ``it:exec:proc``
    Add an ``account`` secondary property as a ``it:account`` type. Mark the
    ``user`` secondary property as deprecated.

  ``ps:contact``
    Add ``birth:place``, ``birth:place:loc``, ``birth:place:name``,
    ``death:place``, ``death:place:loc`` and ``death:place:name`` secondary
    properties.

  ``risk:compromise``
    Add a ``theft:price`` secondary property to represent value of stolen
    assets.

- Embed Cron, StormDmon, and Trigger iden values and automation types into
  the Storm runtime when those automations are run. This information is
  populated in a dictionary variable named ``$auto``.
  (`#2565 <https://github.com/vertexproject/synapse/pull/2565>`_)
- Add ``$lib.crypto.coin.ethereum.eip55()`` to convert an Ethereum address to a
  checksummed address.
  (`#2577 <https://github.com/vertexproject/synapse/pull/2577>`_)
- Add a ``default`` argument to the  ``$lib.user.allowed()`` and ``allowed()``
  method on ``storm:user`` StormType.
  (`#2570 <https://github.com/vertexproject/synapse/pull/2570>`_)
- Add a ``inaugural`` configuration key to the base ``Cell`` class. This can
  currently be used to bootstrap roles, permissions, and users in a Cell upon
  the first time it is started.
  (`#2570 <https://github.com/vertexproject/synapse/pull/2570>`_)
- De-duplicate nodes when running the Storm ``lookup`` mode to lift nodes.
  (`#2567 <https://github.com/vertexproject/synapse/pull/2567>`_)
- Add a test helper that can be used to isolate the
  ``synapse.lib.certdir.certdir`` singleton behavior via context manager.
  (`#2564 <https://github.com/vertexproject/synapse/pull/2564>`_)

Bugfixes
--------
- Calls to ``addFormProp()`` APIs when the property name already exists now
  raise a ``DupPropName`` exception.
  (`#2566 <https://github.com/vertexproject/synapse/pull/2566>`_)
- Do not allow Storm ``macro``'s to be created that have names greater than
  492 characters in length.
  (`#2569 <https://github.com/vertexproject/synapse/pull/2569>`_)
- Fix a bug in the scrape logic for Ethereum where the regular expression
  matched on ``0X`` prefixed strings but the validation logic did not account
  for that uppercase character.
  (`#2575 <https://github.com/vertexproject/synapse/pull/2575>`_)

Improved Documentation
----------------------
- Add documentation for the ``$auto`` variable embedded into the Cron,
  StormDmon, and Trigger automations. Add documentation for variables
  representing the form, node value, properties and tags which are responsible
  for Triggers running.
  (`#2565 <https://github.com/vertexproject/synapse/pull/2565>`_)


v2.84.0 - 2022-02-22
====================

Features and Enhancements
-------------------------
- Add ``$lib.time.toUTC()`` to adjust a local epoch milliseconds time to
  UTC.
  (`#2550 <https://github.com/vertexproject/synapse/pull/2550>`_)
- Add a optional ``timeout`` argument to ``$lib.service.wait()``. The function
  now returns ``$lib.true`` if the service is available, or ``$lib.false`` if
  the service does not become available during the timeout window.
  (`#2561 <https://github.com/vertexproject/synapse/pull/2561>`_)
- Update the ``Layer.verify()`` routines to add verification of tagprop and
  array indexes in layers.  These routines are in a beta status and are
  subject to change.
  (`#2560 <https://github.com/vertexproject/synapse/pull/2560>`_)
- Update the Cortex's connection to a remote Axon to use a Telepath Client.
  (`#2559 <https://github.com/vertexproject/synapse/pull/2559>`_)


v2.83.0 - 2022-02-17
====================

Features and Enhancements
-------------------------
- Add ``:ip:proto`` and ``:ip:tcp:flags`` properties to the ``inet:flow``
  form.
  (`#2554 <https://github.com/vertexproject/synapse/pull/2554>`_)
- Add ``$lib.log.debug()``, ``$lib.log.info()``, ``$lib.log.warning()``, and
  ``$lib.log.error()`` Stormtypes APIs. These allow a user to send log
  messages to the Cortex logging output directly.
- Update the ``synapse.tools.genpkg`` tool to support using files with the
  ``.storm`` extension. This is enabled by adding the following option to a
  Storm package definition.
  (`#2555 <https://github.com/vertexproject/synapse/pull/2555>`_)

  ::

    genopts:
      dotstorm: true


- Add form and prop values to ``BadTypeValu`` exceptions when raised during
  node edit generation.
  (`#2552 <https://github.com/vertexproject/synapse/pull/2552>`_)

Bugfixes
--------
- Correct a race condition in the ``CoreApi.syncLayersEvents`` and
  ``CoreApi.syncIndexEvents`` APIs.
  (`#2553 <https://github.com/vertexproject/synapse/pull/2553>`_)

Improved Documentation
----------------------
- Remove outdated documentation related to making ``CoreModule`` classes.
  (`#2556 <https://github.com/vertexproject/synapse/pull/2556>`_)


v2.82.1 - 2022-02-11
====================

Bugfixes
--------
- Re-order node edit validation to only check read-only status of properties
  if the value would change.
  (`#2547 <https://github.com/vertexproject/synapse/pull/2547>`_)
- Raise the correct exception when parsing invalid time values, like
  ``0000-00-00``.
  (`#2548 <https://github.com/vertexproject/synapse/pull/2548>`_)
- Disable node caching for ``StormDmon`` runtimes to avoid potential
  cache coherency issues.
  (`#2549 <https://github.com/vertexproject/synapse/pull/2549>`_)


v2.82.0 - 2022-02-10
====================

Features and Enhancements
-------------------------
- Add an ``addNode()`` API to the Stormtypes ``storm:view`` object. This
  allows the programmatic creation of a node with properties being set in
  a transactional fashion.
  (`#2540 <https://github.com/vertexproject/synapse/pull/2540>`_)
- Add support to Storm for creating JSON style list and dictionary objects.
  (`#2544 <https://github.com/vertexproject/synapse/pull/2544>`_)
- The ``AhaCell`` now bootstraps TLS CA certificates for the configured
  ``aha:network`` value, a host certificate for the ``aha:name`` value,
  and a user certificate for the ``aha:admin`` value.
  (`#2542 <https://github.com/vertexproject/synapse/pull/2542>`_)
- Add ``mesg`` arguments to all exceptions raised in ``synapse.lib.certdir``.
  (`#2546 <https://github.com/vertexproject/synapse/pull/2546>`_)

Improved Documentation
----------------------
- Fix some missing and incorrect docstrings for Stormtypes.
  (`#2545 <https://github.com/vertexproject/synapse/pull/2545>`_)

Deprecations
------------
- Telepath APIs and Storm commands related to ``splices`` have been marked as
  deprecated.
  (`#2541 <https://github.com/vertexproject/synapse/pull/2541>`_)


v2.81.0 - 2022-01-31
====================

Features and Enhancements
-------------------------
- The ``it:sec:cpe`` now recognizes CPE 2.2 strings during type normalization.
  CPE 2.2 strings will be upcast to CPE 2.3 and the 2.2 string will be added
  to the ``:v2_2`` secondary property of ``it:sec:cpe``. The Storm hotfix
  ``$lib.cell.hotFixesApply()`` can be used to populate the ``:v2_2``
  property on existing ``it:sec:cpe`` nodes where it is not set.
  (`#2537 <https://github.com/vertexproject/synapse/pull/2537>`_)
  (`#2538 <https://github.com/vertexproject/synapse/pull/2538>`_)
  (`#2539 <https://github.com/vertexproject/synapse/pull/2539>`_)
- Setting properties on nodes may now take a fast path if the normed property
  has no subs, no autoadds and is not a locked property.
  (`#2539 <https://github.com/vertexproject/synapse/pull/2539>`_)

Bugfixes
--------
- Fix an issue with ``Ival`` ``norm()`` routines when norming a tuple or list
  of values. The max value returned previously could have exceeded the value
  of the future marker ``?``, which would have been then caused an a
  ``BadTypeValu`` exception during node edit construction. This is  is now
  caught during the initial ``norm()`` call.
  (`#2539 <https://github.com/vertexproject/synapse/pull/2539>`_)


v2.80.1 - 2022-01-26
====================

Bugfixes
--------
- The embedded JsonStor added to the Cortex in ``v2.80.0`` needed to have a
  stable iden for the Cell and and auth subsystem. This has been added.
  (`#2536 <https://github.com/vertexproject/synapse/pull/2536>`_)


v2.80.0 - 2022-01-25
====================

Features and Enhancements
-------------------------
- Add a triple quoted string ``'''`` syntax to Storm for defining multiline
  strings.
  (`#2530 <https://github.com/vertexproject/synapse/pull/2530>`_)
- Add a JSONStor to the Cortex, and expose that in Storm for storing user
  related content.
  (`#2530 <https://github.com/vertexproject/synapse/pull/2530>`_)
  (`#2513 <https://github.com/vertexproject/synapse/pull/2513>`_)
- Add durable user notifications to Storm that can be used to send and receive
  messages between users.
  (`#2513 <https://github.com/vertexproject/synapse/pull/2513>`_)
- Add a ``leaf`` argument to ``$node.tags()`` that causes the function to only
  return the leaf tags.
  (`#2535 <https://github.com/vertexproject/synapse/pull/2535>`_)
- Add an error message in the default help text in pure Storm commands when a
  user provides additional arguments or switches, in addition to the
  ``--help`` switch.
  (`#2533 <https://github.com/vertexproject/synapse/pull/2533>`_)
- Update ``synapse.tools.genpkg`` to automatically bundle Optic workflows from
  files on disk.
  (`#2531 <https://github.com/vertexproject/synapse/pull/2531>`_)
- Expand Synapse requirements to include updated versions of the
  ``packaging``, ``pycryptome`` and ``scalecodec`` modules.
  (`#2534 <https://github.com/vertexproject/synapse/pull/2534>`_)

Bugfixes
--------
- Add a missing ``tostr()`` call to the Storm ``background`` query argument.
  (`#2532 <https://github.com/vertexproject/synapse/pull/2532>`_)


v2.79.0 - 2022-01-18
====================

Features and Enhancements
-------------------------
- Add ``$lib.scrape.ndefs()`` and ``$lib.scrape.context()`` to scrape text.
  The ``ndefs()`` API yields a unique set of node form and value pairs,
  while the ``context()`` API yields node form, value, and context information
  for all matches in the text.
  (`#2508 <https://github.com/vertexproject/synapse/pull/2508>`_)
- Add ``:name`` and ``:desc`` properties to the ``it:prod:softver`` form.
  (`#2528 <https://github.com/vertexproject/synapse/pull/2528>`_)
- Update the ``Layer.verify()`` routines to reduce false errors related to
  array types. The method now takes a dictionary of configuration options.
  These routines are in a beta status and are subject to change.
  (`#2527 <https://github.com/vertexproject/synapse/pull/2527>`_)
- Allow setting a View's parent if does not have an existing parent View
  and only has a single layer.
  (`#2515 <https://github.com/vertexproject/synapse/pull/2515>`_)
- Add ``hxxp[:\\]`` and ``hxxps[:\\]`` to the list of known defanging
  strategies which are identified and replaced during text scraping.
  (`#2526 <https://github.com/vertexproject/synapse/pull/2526>`_)
- Expand Synapse requirements to include updated versions of the
  ``typing-extensions`` module.
  (`#2525 <https://github.com/vertexproject/synapse/pull/2525>`_)

Bugfixes
--------
- Storm module interfaces now populate ``modconf`` data when loaded.
  (`#2508 <https://github.com/vertexproject/synapse/pull/2508>`_)
- Fix a missing keyword argument from the ``AxonApi.wput()`` method.
  (`#2527 <https://github.com/vertexproject/synapse/pull/2527>`_)

Deprecations
------------
- The ``$lib.scrape()`` function has been deprecated in favor the new
  ``$lib.scrape`` library functions.
  (`#2508 <https://github.com/vertexproject/synapse/pull/2508>`_)


v2.78.0 - 2022-01-14
====================

Automatic Migrations
--------------------
- Migrate Cortex nodes which may have been skipped in an earlier migration due
  to missing tagprop indexes. See :ref:`datamigration` for more
  information about automatic migrations.

Features and Enhancements
-------------------------
- Expand Synapse requirements to include updated versions of the ``base58``,
  ``cbor2``, ``lmdb``, ``pycryptodome``, ``PyYAML``, ``xxhash``.
  (`#2520 <https://github.com/vertexproject/synapse/pull/2520>`_)

Bugfixes
--------
- Fix an issue with the Tagprop migration from ``v2.42.0`` where a missing
  index could have resulted in Layer storage nodes not being updated.
  (`#2522 <https://github.com/vertexproject/synapse/pull/2522>`_)
  (`#2523 <https://github.com/vertexproject/synapse/pull/2523>`_)
- Fix an issue with ``synapse.lib.platforms.linux.getTotalMemory()`` when
  using a process segregated with the Linux cgroups2 API.
  (`#2517 <https://github.com/vertexproject/synapse/pull/2517>`_)

Improved Documentation
----------------------
- Add devops instructions related to automatic data migrations for Synapse
  components.
  (`#2523 <https://github.com/vertexproject/synapse/pull/2523>`_)
- Update the model deprecation documentation for the ``it:host:model`` and
  ``it:host:make`` properties.
  (`#2521 <https://github.com/vertexproject/synapse/pull/2521>`_)


v2.77.0 - 2022-01-07
====================

Features and Enhancements
-------------------------
- Add Mach-O metadata support the file model. This includes the following
  new forms: ``file:mime:macho:loadcmd``, ``file:mime:macho:version``,
  ``file:mime:macho:uuid``, ``file:mime:macho:segment``, and
  ``file:mime:macho:section``.
  (`#2503 <https://github.com/vertexproject/synapse/pull/2503>`_)
- Add ``it:screenshot``, ``it:prod:hardware``, ``it:prod:component``,
  ``it:prod:hardwaretype``, and ``risk:mitigation`` forms to the model. Add
  ``:hardware`` property to ``risk:hasvuln`` form. Add ``:hardware`` property
  to ``it:host`` form. The ``:manu`` and ``:model`` secondary properties on
  ``it:host`` have been deprecated.
  (`#2514 <https://github.com/vertexproject/synapse/pull/2514>`_)
- The ``guid`` type now strips hyphen (``-``) characters when doing norm. This
  allows users to provide external UUID / GUID strings for use.
  (`#2514 <https://github.com/vertexproject/synapse/pull/2514>`_)
- Add a ``Axon.postfiles()`` to allow POSTing files as multi-part form encoded
  files over HTTP. This is also exposed through the ``fields`` argument on the
  Storm ``$lib.inet.http.post()`` and ``$lib.inet:http:request`` APIs.
  (`#2516 <https://github.com/vertexproject/synapse/pull/2516>`_)
- Add ``.yu`` ccTLD to the list of TLDs identified by the Synapse scrape
  functionality.
  (`#2518 <https://github.com/vertexproject/synapse/pull/2518>`_)
- Add ``mesg`` arguments to all instances of ``NoSuchProp`` exceptions.
  (`#2519 <https://github.com/vertexproject/synapse/pull/2519>`_)


v2.76.0 - 2022-01-04
====================

Features and Enhancements
-------------------------
- Add ``emit`` and ``stop`` keywords to Storm. The ``emit`` keyword is used
  in functions to make them behave as generators, which can yield arbitrary
  values. The ``stop`` keyword can be used to prematurely end a function which
  is ``emit``'ing values.
  (`#2475 <https://github.com/vertexproject/synapse/pull/2475>`_)
- Add Storm Module Interfaces. This allows Storm Package authors to define
  common module interfaces, so that multiple modules can implement the API
  convention to provide a consistent set of data across multiple Storm
  modules. A ``search`` convention is added to the Cortex, which will be used
  in ``lookup`` mode when the ``storm:interface:search`` configuration option
  is set.
  (`#2475 <https://github.com/vertexproject/synapse/pull/2475>`_)
- Storm queries in ``lookup`` mode now fire ``look:miss`` events into the
  Storm message stream when the lookup value contains a valid node value,
  but the node is not present in the current View.
  (`#2475 <https://github.com/vertexproject/synapse/pull/2475>`_)
- Add a ``:host`` secondary property to ``risk:hasvuln`` form to record
  ``it:host`` instances which have a vulnerability.
  (`#2512 <https://github.com/vertexproject/synapse/pull/2512>`_)
- Add ``synapse.lib.scrape`` support for identifying ``it:sec:cve`` values.
  (`#2509 <https://github.com/vertexproject/synapse/pull/2509>`_)

Bugfixes
--------
- Fix an ``IndexError`` that can occur during ``Layer.verify()`` routines.
  These routines are in a beta status and are subject to change.
  (`#2507 <https://github.com/vertexproject/synapse/pull/2507>`_)
- Ensure that parameter and header arguments passed to Storm
  ``$lib.inet.http`` functions are cast into strings values.
  (`#2510 <https://github.com/vertexproject/synapse/pull/2510>`_)


v2.75.0 - 2021-12-16
====================

This release contains an automatic data migration that may cause additional
startup time on the first boot. This is done to unique array properties which
previously were not uniqued. Deployments with startup or liveliness probes
should have those disabled while this upgrade is performed to prevent
accidental termination of the Cortex process. Please ensure you have a tested
backup available before applying this update.

Features and Enhancements
-------------------------

- Update the following array properties to be unique sets, and add a data
  model migration to update the data at rest:
  (`#2469 <https://github.com/vertexproject/synapse/pull/2469>`_)

    - ``biz:rfp:requirements``
    - ``crypto:x509:cert:ext:sans``
    - ``crypto:x509:cert:ext:crls``
    - ``crypto:x509:cert:identities:fqdns``
    - ``crypto:x509:cert:identities:emails``
    - ``crypto:x509:cert:identities:ipv4s``
    - ``crypto:x509:cert:identities:ipv6s``
    - ``crypto:x509:cert:identities:urls``
    - ``crypto:x509:cert:crl:urls``
    - ``inet:whois:iprec:contacts``
    - ``inet:whois:iprec:links``
    - ``inet:whois:ipcontact:roles``
    - ``inet:whois:ipcontact:links``
    - ``inet:whois:ipcontact:contacts``
    - ``it:account:groups``
    - ``it:group:groups``
    - ``it:reveng:function:impcalls``
    - ``it:reveng:filefunc:funccalls``
    - ``it:sec:cve:references``
    - ``risk:vuln:cwes``
    - ``tel:txtmesg:recipients``

- Add Layer index verification routines, to compare the Layer indices against
  the stored data for Nodes. This is exposed via the ``.verify()`` API on the
  Stormtypes ``storm:layer`` object.
  These routines are in a beta status and are subject to change.
  (`#2488 <https://github.com/vertexproject/synapse/pull/2488>`_)
- The ``.json()`` API on ``storm:http:resp`` now raises a
  ``s_exc.BadJsonText`` exception, which can be caught with the Storm
  ``try ... catch`` syntax.
  (`#2500 <https://github.com/vertexproject/synapse/pull/2500>`_)
- Add ``$lib.inet.ipv6.expand()`` to expand an IPv6 address to its long form.
  (`#2502 <https://github.com/vertexproject/synapse/pull/2502>`_)
- Add ``hasPathObj()``, ``copyPathObj()`` and ``copyPathObjs()`` APIs to the
  ``JsonStor``.
  (`#2438 <https://github.com/vertexproject/synapse/pull/2438>`_)
- Allow setting a custom title when making documentation for Cell
  ``confdefs`` with the ``synapse.tools.autodoc`` tool.
  (`#2504 <https://github.com/vertexproject/synapse/pull/2504>`_)
- Update the minimum version of the ``aiohttp`` library to ``v3.8.1``.
  (`#2495 <https://github.com/vertexproject/synapse/pull/2495>`_)

Improved Documentation
----------------------
- Add content previously hosted at ``commercial.docs.vertex.link`` to the
  mainline Synapse documentation. This includes some devops information
  related to orchestration, information about Advanced and Rapid Power-Ups,
  information about the Synapse User Interface, as well as some support
  information.
  (`#2498 <https://github.com/vertexproject/synapse/pull/2498>`_)
  (`#2499 <https://github.com/vertexproject/synapse/pull/2499>`_)
  (`#2501 <https://github.com/vertexproject/synapse/pull/2501>`_)
- Add ``Synapse-Malshare`` and ``Synapse-TeamCymru`` Rapid Power-Ups to the
  list of available Rapid Power-Ups.
  (`#2506 <https://github.com/vertexproject/synapse/pull/2506>`_)
- Document the ``jsonlines`` option for the ``api/v1/storm`` and
  ``api/v1/storm/nodes`` HTTP APIs.
  (`#2505 <https://github.com/vertexproject/synapse/pull/2505>`_)


v2.74.0 - 2021-12-08
====================

Features and Enhancements
-------------------------
- Add ``.onion`` and ``.bit`` to the TLD list used for scraping text. Update
  the TLD list from the latest IANA TLD list.
  (`#2483 <https://github.com/vertexproject/synapse/pull/2483>`_)
  (`#2497 <https://github.com/vertexproject/synapse/pull/2497>`_)
- Add support for writeback mirroring of layers.
  (`#2463 <https://github.com/vertexproject/synapse/pull/2463>`_)
  (`#2489 <https://github.com/vertexproject/synapse/pull/2489>`_)
- Add ``$lib.scrape()`` Stormtypes API. This can be used to do programmatic
  scraping of text using the same regular expressions used by the Storm
  ``scrape`` command and the ``synapse.lib.scrape`` APIs.
  (`#2486 <https://github.com/vertexproject/synapse/pull/2486>`_)
- Add a ``jsonlines`` output mode to Cortex streaming HTTP endpoints.
  (`#2493 <https://github.com/vertexproject/synapse/pull/2493>`_)
- Add a ``--raw`` argument to the Storm ``pkg.load`` command. This loads the
  raw JSON response as a Storm package.
  (`#2491 <https://github.com/vertexproject/synapse/pull/2491>`_)
- Add a ``blocked`` enum to the ``proj:ticket:status`` property to represent a
  blocked ticket.
  (`#2490 <https://github.com/vertexproject/synapse/pull/2490>`_)

Bugfixes
--------
- Fix a behavior with ``$path`` losing variables in pure Storm command
  execution.
  (`#2492 <https://github.com/vertexproject/synapse/pull/2492>`_)

Improved Documentation
----------------------
- Update the description of the Storm ``scrape`` command.
  (`#2494 <https://github.com/vertexproject/synapse/pull/2494>`_)


v2.73.0 - 2021-12-02
====================

Features and Enhancements
-------------------------
- Add a Storm ``runas`` command. This allows admin users to execute Storm
  commands as other users.
  (`#2473 <https://github.com/vertexproject/synapse/pull/2473>`_)
- Add a Storm ``intersect`` command. This command produces the intersection
  of nodes emitted by running a Storm query over all inbound nodes to the
  ``intersect`` command.
  (`#2480 <https://github.com/vertexproject/synapse/pull/2480>`_)
- Add ``wait`` and ``timeout`` parameters to the ``Axon.hashes()`` and
  ``$lib.axon.list()`` APIs.
  (`#2481 <https://github.com/vertexproject/synapse/pull/2481>`_)
- Add a ``readonly`` flag to ``synapse.tools.genpkg.loadPkgProto()`` and
  ``synapse.tools.genpkg.tryLoadPkgProto()`` APIs. If set to ``True`` this
  will open files in read only mode.
  (`#2485 <https://github.com/vertexproject/synapse/pull/2485>`_)
- Allow Storm Prim objects to be capable of directly yielding nodes when used
  in ``yield`` statements.
  (`#2479 <https://github.com/vertexproject/synapse/pull/2479>`_)
- Update the StormDmon subsystem to add debug log information about state
  changes, as well as additional data for structured logging output.
  (`#2455 <https://github.com/vertexproject/synapse/pull/2455>`_)

Bugfixes
--------
- Catch a fatal application error that can occur in the Cortex if the forked
  process pool becomes unusable. Previously this would cause the Cortex to
  appear unresponsive for executing Storm queries; now this causes the Cortex
  to shut down gracefully.
  (`#2472 <https://github.com/vertexproject/synapse/pull/2472>`_)
- Fix a Storm path variable scoping issue where variables were improperly
  scoped when nodes were passed into pure Storm commands.
  (`#2459 <https://github.com/vertexproject/synapse/pull/2459>`_)


v2.72.0 - 2021-11-23
====================

Features and Enhancements
-------------------------
- Update the cron subsystem logs to include the cron name, as well as adding
  additional data for structured logging output.
  (`#2477 <https://github.com/vertexproject/synapse/pull/2477>`_)
- Add a ``sort_keys`` argument to the ``$lib.yaml.save()`` Stormtype API.
  (`#2474 <https://github.com/vertexproject/synapse/pull/2474>`_)

Bugfixes
--------
- Update the ``asyncio-socks`` version to a version which has a pinned version
  range for the ``python-socks`` dependency.
  (`#2478 <https://github.com/vertexproject/synapse/pull/2478>`_)


v2.71.1 - 2021-11-22
====================

Bugfixes
--------
- Update the ``PyOpenSSL`` version to ``21.0.0`` and pin a range of modern
  versions of the ``cryptography`` which have stronger API compatibility.
  This resolves an API compatibility issue with the two libraries which
  affected SSL certificate generation.
  (`#2476 <https://github.com/vertexproject/synapse/pull/2476>`_)


v2.71.0 - 2021-11-19
====================

Features and Enhancements
-------------------------
- Add support for asynchronous triggers. This mode of trigger operation queues
  up the trigger event in the View for eventual processing.
  (`#2464 <https://github.com/vertexproject/synapse/pull/2464>`_)
- Update the crypto model to add a ``crypto:smart:token`` form to represent a
  token managed by a smart contract.
  (`#2462 <https://github.com/vertexproject/synapse/pull/2462>`_)
- Add ``$lib.axon.readlines()`` and ``$lib.axon.jsonlines()`` to Stormtypes.
  (`#2468 <https://github.com/vertexproject/synapse/pull/2468>`_)
- Add the Storm ``mode`` to the structured log output of a Cortex executing a
  Storm query.
  (`#2466 <https://github.com/vertexproject/synapse/pull/2466>`_)

Bugfixes
--------
- Fix an error when converting Lark exceptions to Synapse ``BadSyntaxError``.
  (`#2471 <https://github.com/vertexproject/synapse/pull/2471>`_)

Improved Documentation
----------------------
- Revise the Synapse documentation layout.
  (`#2460 <https://github.com/vertexproject/synapse/pull/2460>`_)
- Update type specific behavior documentation for ``time`` types, including
  the recently added wildcard time syntax.
  (`#2467 <https://github.com/vertexproject/synapse/pull/2467>`_)
- Sort the Storm Type documentation by name.
  (`#2465 <https://github.com/vertexproject/synapse/pull/2465>`_)
- Add 404 handler pages to our documentation.
  (`#2461 <https://github.com/vertexproject/synapse/pull/2461>`_)
  (`#2470 <https://github.com/vertexproject/synapse/pull/2470>`_)

Deprecations
------------
- Remove ``$path.trace()`` objects.
  (`#2445 <https://github.com/vertexproject/synapse/pull/2445>`_)


v2.70.1 - 2021-11-08
====================

Bugfixes
--------
- Fix an issue where ``$path.meta`` data was not being properly serialized
  when heavy Stormtype objects were set on the ``$path.meta`` dictionary.
  (`#2456 <https://github.com/vertexproject/synapse/pull/2456>`_)
- Fix an issue with Stormtypes ``Str.encode()`` and ``Bytes.decode()`` methods
  when handling potentially malformed Unicode string data.
  (`#2457 <https://github.com/vertexproject/synapse/pull/2457>`_)

Improved Documentation
----------------------
- Update the Storm Control Flow documentation with additional examples.
  (`#2443 <https://github.com/vertexproject/synapse/pull/2443>`_)


v2.70.0 - 2021-11-03
====================

Features and Enhancements
-------------------------
- Add ``:dst:handshake`` and ``src:handshake`` properties to ``inet:flow`` to
  record text representations of the handshake strings of a given connection.
  (`#2451 <https://github.com/vertexproject/synapse/pull/2451>`_)
- Add a ``proj:attachment`` form to the ``project`` model to represent
  attachments to a given ``proj:ticket``.
  (`#2451 <https://github.com/vertexproject/synapse/pull/2451>`_)
- Add a implicit wildcard behavior to the ``time`` type when lifting or
  filtering nodes. Dates ending in a ``*`` are converted into ranges covering
  all possible times in them. For example, ``.created=202101*`` would lift all
  nodes created on the first month of 2021.
  (`#2446 <https://github.com/vertexproject/synapse/pull/2446>`_)
- Add the following ``$lib.time`` functions to chop information from a time
  value.
  (`#2446 <https://github.com/vertexproject/synapse/pull/2446>`_)

    - ``$lib.time.year()``
    - ``$lib.time.month()``
    - ``$lib.time.day()``
    - ``$lib.time.hour()``
    - ``$lib.time.minute()``
    - ``$lib.time.second()``
    - ``$lib.time.dayofweek()``
    - ``$lib.time.dayofmonth()``
    - ``$lib.time.monthofyear()``

- Add ``List.extend()``, ``List.slice()``, ``Str.find()``, and ``Str.size()``
  functions to Stormtypes.
  (`#2450 <https://github.com/vertexproject/synapse/pull/2450>`_)
  (`#2451 <https://github.com/vertexproject/synapse/pull/2451>`_)
- Add ``$lib.json.schema()`` and a ``storm:json:schema`` object to Stormtypes.
  These can be used to validate arbitrary data JSON structures in Storm using
  JSON Schema.
  (`#2448 <https://github.com/vertexproject/synapse/pull/2448>`_)
- Update syntax checking rules and address deprecation warnings for strings
  in the Synapse codebase.
  (`#2426 <https://github.com/vertexproject/synapse/pull/2426>`_)


v2.69.0 - 2021-11-02
====================

Features and Enhancements
-------------------------
- Add support for building Optic Workflows for Storm Packages in the
  ``synapse.tools.genpkg`` tool.
  (`#2444 <https://github.com/vertexproject/synapse/pull/2444>`_)
- The ``synapse.tools.storm`` CLI tool now prints out node properties in
  precedence order.
  (`#2449 <https://github.com/vertexproject/synapse/pull/2449>`_)
- Update the global Stormtypes registry to better track types when they are
  added or removed.
  (`#2447 <https://github.com/vertexproject/synapse/pull/2447>`_)


v2.68.0 - 2021-10-29
====================

Features and Enhancements
-------------------------
- Add ``crypto:currency:transaction``, ``crypto:currency:block``,
  ``crypto:smart:contract`` and ``econ:acct:balanc`` forms.
  (`#2423 <https://github.com/vertexproject/synapse/pull/2423>`_)
- Add ``$lib.hex.decode()`` and ``$lib.hex.encode()`` Stormtypes functions to
  encode and decode hexidecimal data as bytes. Add ``slice()`` and
  ``unpack()`` methods to the Storm Bytes object.
  (`#2441 <https://github.com/vertexproject/synapse/pull/2441>`_)
- Add ``$lib.yaml`` and ``$lib.xml`` Stormtypes libraries for interacting with
  YAML and XML text, respectively.
  (`#2434 <https://github.com/vertexproject/synapse/pull/2434>`_)
- Add a Storm ``version`` command to show the user the current version of
  Synapse the Cortex is using.
  (`#2440 <https://github.com/vertexproject/synapse/pull/2440>`_)

Bugfixes
--------
- Fix overzealous ``if`` statement caching in Storm.
  (`#2442 <https://github.com/vertexproject/synapse/pull/2442>`_)


v2.67.0 - 2021-10-27
====================

Features and Enhancements
-------------------------
- Add ``$node.addEdge()`` and ``$node.delEdge()`` APIs in Storm to allow for
  programatically setting edges. Add a ``reverse`` argument to
  ``$node.edges()`` that allows traversing edges in reverse.
  (`#2351 <https://github.com/vertexproject/synapse/pull/2351>`_)

Bugfixes
--------
- Fix a pair of regressions related to unicode/IDNA support for scraping and
  normalizing FQDNs.
  (`#2436 <https://github.com/vertexproject/synapse/pull/2436>`_)

Improved Documentation
----------------------
- Add documentation for the Cortex ``api/v1/storm/call`` HTTP API endpoint.
  (`#2435 <https://github.com/vertexproject/synapse/pull/2435>`_)


v2.66.0 - 2021-10-26
====================

Features and Enhancements
-------------------------
- Improve unicode/IDNA support for scraping and normalizing FQDNs.
  (`#2408 <https://github.com/vertexproject/synapse/pull/2408>`_)
- Add ``$lib.inet.http.ouath`` to support OAuth based workflows in Storm,
  starting with OAuth v1.0 support.
  (`#2413 <https://github.com/vertexproject/synapse/pull/2413>`_)
- Replace ``pysha3`` requirement with ``pycryptodome``.
  (`#2422 <https://github.com/vertexproject/synapse/pull/2422>`_)
- Add a ``tls:ca:dir`` configuration option to the Cortex and Axon. This can
  be used to provide a directory of CA certificate files which are used in
  Storm HTTP API and Axon wget/wput APIs.
  (`#2429 <https://github.com/vertexproject/synapse/pull/2429>`_)

Bugfixes
--------
- Catch and raise bad ctors given in RStorm ``storm-cortex`` directives.
  (`#2424 <https://github.com/vertexproject/synapse/pull/2424>`_)
- Fix an issue with the ``cron.at`` command not properly capturing the current
  view when making the Cron job.
  (`#2425 <https://github.com/vertexproject/synapse/pull/2425>`_)
- Disallow the creation of extended properties, universal properties, and tag
  properties which are not valid properties in the Storm grammar.
  (`#2428 <https://github.com/vertexproject/synapse/pull/2428>`_)
- Fix an issue with ``$lib.guid()`` missing a ``toprim()`` call on its input.
  (`#2421 <https://github.com/vertexproject/synapse/pull/2421>`_)

Improved Documentation
----------------------
- Update our Cell devops documentation to note how to replace the TLS keypair
  used by the built in webserver with third party certificates.
  (`#2432 <https://github.com/vertexproject/synapse/pull/2432>`_)


v2.65.0 - 2021-10-16
====================

Features and Enhancements
-------------------------
- Add support for interacting with IMAP email servers though Storm, using the
  ``$lib.inet.imap.connect()`` function. This returns a object that can be
  used to delete, read, and search emails in a given IMAP mailbox.
  (`#2399 <https://github.com/vertexproject/synapse/pull/2399>`_)
- Add a new Storm command, ``once``. This command can be used to 'gate' a node
  in a Storm pipeline such that the node only passes through the command
  exactly one time for a given named 'gate'. The gate information is stored in
  nodedata, so it is inspectable and subject to all other features that
  apply to nodedata.
  (`#2404 <https://github.com/vertexproject/synapse/pull/2404>`_)
- Add a ``:released`` property to ``it:prod:softver`` to record when a
  software version was released.
  (`#2419 <https://github.com/vertexproject/synapse/pull/2419>`_)
- Add a ``tryLoadPkgProto`` convenience function to the
  ``synapse.tools.genpkg`` for Storm service package generation with inline
  documentation.
  (`#2414 <https://github.com/vertexproject/synapse/pull/2414>`_)

Bugfixes
--------
- Add ``asyncio.sleep(0)`` calls in the ``movetag`` implementation to address
  some possible hot-loops.
  (`#2411 <https://github.com/vertexproject/synapse/pull/2411>`_)
- Clarify and sanitize URLS in a Aha related log message i
  ``synapse.telepath``.
  (`#2415 <https://github.com/vertexproject/synapse/pull/2415>`_)

Improved Documentation
----------------------
- Update our ``fork`` definition documentation.
  (`#2409 <https://github.com/vertexproject/synapse/pull/2409>`_)
- Add documentation for using client-side TLS certificates in Telepath.
  (`#2412 <https://github.com/vertexproject/synapse/pull/2412>`_)
- Update the Storm CLI tool documentation.
  (`#2406 <https://github.com/vertexproject/synapse/pull/2406>`_)
- The Storm types and Storm library documentation now automatically links
  from return values to return types.
  (`#2410 <https://github.com/vertexproject/synapse/pull/2410>`_)

v2.64.1 - 2021-10-08
====================

Bugfixes
--------
- Add a retry loop in the base ``Cell`` class when attempting to register with
  an ``Aha`` server.
  (`#2405 <https://github.com/vertexproject/synapse/pull/2405>`_)
- Change the behavior of ``synapse.common.yamlload()`` to not create files
  when the expected file is not present on disk, and open existing files in
  read-only mode.
  (`#2396 <https://github.com/vertexproject/synapse/pull/2396>`_)


v2.64.0 - 2021-10-06
====================

Features and Enhancements
-------------------------
- Add support for scraping the following cryptocurrency addresses to the
  ``synapse.lib.scrape`` APIs and Storm ``scrape`` command.
  (`#2387 <https://github.com/vertexproject/synapse/pull/2387>`_)
  (`#2401 <https://github.com/vertexproject/synapse/pull/2401>`_)

    - Bitcoin
    - Bitcoin Cash
    - Ethereum
    - Ripple
    - Cardano
    - Polkadot

  The internal cache of regular expressions in the ``synapse.lib.scrape``
  library is also now a private member; API users should use the
  ``synapse.lib.scrape.scrape()`` function moving forward.

- Add ``:names`` property to the ``it:mitre:attack:software`` form.
  (`#2397 <https://github.com/vertexproject/synapse/pull/2397>`_)
- Add a ``:desc`` property to the ``inet:whois:iprec`` form.
  (`#2392 <https://github.com/vertexproject/synapse/pull/2392>`_)
- Added several new Rstorm directives.
  (`#2359 <https://github.com/vertexproject/synapse/pull/2359>`_)
  (`#2400 <https://github.com/vertexproject/synapse/pull/2400>`_)

  - ``storm-cli`` - Runs a Storm query with the Storm CLI tool
  - ``storm-fail`` - Toggles whether or not the following Storm command
    should fail or not.
  - ``storm-multiline`` - Allows embedding a multiline Storm query as a JSON
    encoded string for future execution.
  - ``storm-vcr-callback`` - Allows specifying a custom callback which a VCR
    object is sent too.

Bugfixes
--------
- Fix a missing ``toprim()`` call when loading a Storm package directly with
  Storm.
  (`#2359 <https://github.com/vertexproject/synapse/pull/2359>`_)
- Fix a caching issue where tagprops were not always being populated in a
  ``Node`` tagprop dictionary.
  (`#2396 <https://github.com/vertexproject/synapse/pull/2396>`_)
- Add a ``mesg`` argument to a few ``NoSuchVar`` and ``BadTypeValu``
  exceptions.
  (`#2403 <https://github.com/vertexproject/synapse/pull/2403>`_)

Improved Documentation
----------------------
- Storm reference docs have been converted from Jupyter notebook format to
  Synapse ``.rstorm`` format, and now display examples using the Storm CLI
  tool, instead of the Cmdr CLI tool.
  (`#2359 <https://github.com/vertexproject/synapse/pull/2359>`_)


v2.63.0 - 2021-09-29
====================

Features and Enhancements
-------------------------
- Add a ``risk:attacktype`` taxonomy to the risk model. Add ``:desc`` and
  ``:type`` properties to the ``risk:attack`` form.
  (`#2386 <https://github.com/vertexproject/synapse/pull/2386>`_)
- Add ``:path`` property to the ``it:prod:softfile`` form.
  (`#2388 <https://github.com/vertexproject/synapse/pull/2388>`_)

Bugfixes
--------
- Fix the repr for the``storm:auth:user``  Stormtype when printing a user
  object in Storm.
  (`#2383 <https://github.com/vertexproject/synapse/pull/2383>`_)


v2.62.1 - 2021-09-22
====================

Bugfixes
--------
- Fix an issue in the Nexus log V1 to V2 migration code which resulted in
  LMDB file copies being made instead of having directories renamed. This can
  result in a sparse file copy of the Nexus log, resulting in a condition
  where the volume containing the Cell directory may run out of space.
  (`#2374 <https://github.com/vertexproject/synapse/pull/2374>`_)


v2.62.0 - 2021-09-21
====================

Features and Enhancements
-------------------------
- Add APIs to support trimming, rotating and culling Nexus logs from Cells
  with Nexus logging enabled. These operations are distributed to downstream
  consumers, of the Nexus log (e.g. mirrors). For the Cortex, this can be
  invoked in Storm with the ``$lib.cell.trimNexsLog()`` Stormtypes API. The
  Cortex devops documentation contains more information about Nexus log
  rotation.
  (`#2339 <https://github.com/vertexproject/synapse/pull/2339>`_)
  (`#2371 <https://github.com/vertexproject/synapse/pull/2371>`_)
- Add ``.size()`` API to the Stormtypes ``storm:query`` object. This will run
  the query and return the number of nodes it would have yielded.
  (`#2363 <https://github.com/vertexproject/synapse/pull/2363>`_)

Improved Documentation
----------------------
- Document the tag glob meanings on the Stormtypes ``$node.tags()`` API.
  (`#2368 <https://github.com/vertexproject/synapse/pull/2368>`_)


v2.61.0 - 2021-09-17
====================

Features and Enhancements
-------------------------
- Add a ``!export`` command to the Storm CLI to save query results to a
  ``.nodes`` file.
  (`#2356 <https://github.com/vertexproject/synapse/pull/2356>`_)
- Add ``$lib.cell.hotFixesCheck()`` and ``$lib.cell.hotFixesApply()``
  Stormtypes functions. These can be used to apply optional hotfixes to a
  Cortex on demand by an admin.
  (`#2348 <https://github.com/vertexproject/synapse/pull/2348>`_)
- Add ``$lib.infosec.cvss.calculateFromProps()`` to allow calculating a CVSS
  score from a dictionary of CVSS properties.
  (`#2353 <https://github.com/vertexproject/synapse/pull/2353>`_)
- Add ``$node.data.has()`` API to Stormtypes to allow easy checking if a node
  has nodedata for a given name.
  (`#2350 <https://github.com/vertexproject/synapse/pull/2350>`_)

Bugfixes
--------
- Fix for large return values with ``synapse.lib.coro.spawn()``.
  (`#2355 <https://github.com/vertexproject/synapse/pull/2355>`_)
- Fix ``synapse.lib.scrape.scrape()`` capturing various common characters used
  to enclose URLs.
  (`#2352 <https://github.com/vertexproject/synapse/pull/2352>`_)
- Ensure that generators being yielded from are always being closed.
  (`#2358 <https://github.com/vertexproject/synapse/pull/2358>`_)
- Fix docstring for ``str.upper()`` in Stormtypes.
  (`#2354 <https://github.com/vertexproject/synapse/pull/2354>`_)

Improved Documentation
----------------------
- Add link to the Power-Ups blog post from the Cortex dev-ops documentation.
  (`#2357 <https://github.com/vertexproject/synapse/pull/2357>`_)


v2.60.0 - 2021-09-07
====================

Features and Enhancements
-------------------------
- Add new ``risk:compromise`` and ``risk:compromisetype`` forms. Add
  ``attacker``, ``compromise``, and ``target`` secondary properties to the
  ``risk:attack`` form.
  (`#2348 <https://github.com/vertexproject/synapse/pull/2348>`_)

Bugfixes
--------
- Add a missing ``wait()`` call when calling the ``CoreApi.getAxonUpload()``
  and ``CoreApi.getAxonBytes()`` Telepath APIs.
  (`#2349 <https://github.com/vertexproject/synapse/pull/2349>`_)

Deprecations
------------
- Deprecate the ``actor:org``, ``actor:person``, ``target:org`` and
  ``target:person`` properties on ``risk:attack`` in favor of new ``attacker``
  and ``target`` secondary properties. Deprecate the ``type`` property on
  ``ou:campaign`` in favor of the ``camptype`` property.
  (`#2348 <https://github.com/vertexproject/synapse/pull/2348>`_)


v2.59.0 - 2021-09-02
====================

Features and Enhancements
-------------------------
- Add a new Storm command, ``pkg.docs``, to enumerate any documentation that
  has been bundled with a Storm package.
  (`#2341 <https://github.com/vertexproject/synapse/pull/2341>`_)
- Add support for manipulating ``'proj:comment`` nodes via Stormtypes.
  (`#2345 <https://github.com/vertexproject/synapse/pull/2345>`_)
- Add ``Axon.wput()`` and ``$lib.axon.wput()`` to allow POSTing a file from
  an Axon to a given URL.
  (`#2347 <https://github.com/vertexproject/synapse/pull/2347>`_)
- Add ``$lib.export.toaxon()`` to allow exporting a ``.nodes`` file directly
  to an Axon based on a given storm query and opts.
  (`#2347 <https://github.com/vertexproject/synapse/pull/2347>`_)
- The ``synapse.tools.feed`` tool now accepts a ``--view`` argument to feed
  data to a specific View.
  (`#2342 <https://github.com/vertexproject/synapse/pull/2342>`_)
- The ``synapse.tools.feed`` tool now treats ``.nodes`` files as msgpack files
  for feeding data to a Cortex.
  (`#2343 <https://github.com/vertexproject/synapse/pull/2343>`_)
- When the Storm ``help`` command has an argument without any matching
  commands, it now prints a helpful message.
  (`#2338 <https://github.com/vertexproject/synapse/pull/2338>`_)

Bugfixes
--------
- Fix a caching issue between ``$lib.lift.byNodeData()`` and altering the
  existing node data on a given node.
  (`#2344 <https://github.com/vertexproject/synapse/pull/2344>`_)
- Fix an issue with backups were known lmdbslabs could be omitted from being
  treated as lmdb databases, resulting in inefficient file copies being made.
  (`#2346 <https://github.com/vertexproject/synapse/pull/2346>`_)


v2.58.0 - 2021-08-26
====================

Features and Enhancements
-------------------------
- Add ``!pushfile``, ``!pullfile``, and ``!runfile`` commands to the
  ``synapse.tools.storm`` tool.
  (`#2334 <https://github.com/vertexproject/synapse/pull/2334>`_)
- Add multiname SNI support to ``ssl://`` listening configurations for
  the Daemon.
  (`#2336 <https://github.com/vertexproject/synapse/pull/2336>`_)
- Add a new Cortex HTTP API Endpoint, ``/api/v1/feed``. This can be used to
  add nodes to the Cortex in bulk.
  (`#2337 <https://github.com/vertexproject/synapse/pull/2337>`_)
- Refactor the ``syn.nodes`` feed API implementation to smooth out the ingest
  rate.
  (`#2337 <https://github.com/vertexproject/synapse/pull/2337>`_)
- Sort the Storm Package commands in documentation created by
  ``synpse.tools.autodoc`` alphabetically.
  (`#2335 <https://github.com/vertexproject/synapse/pull/2335>`_)

Deprecations
------------
- Deprecate the ``syn.splices`` and ``syn.nodedata`` feed API formats.
  (`#2337 <https://github.com/vertexproject/synapse/pull/2337>`_)


v2.57.0 - 2021-08-24
====================

Features and Enhancements
-------------------------
- Add a basic ``synapse.tools.storm`` CLI tool. This can be used to connect
  to a Cortex via Telepath and directly execute Storm commands.
  (`#2332 <https://github.com/vertexproject/synapse/pull/2332>`_)
- Add an ``inet:http:session`` form to track the concept of a prolonged
  session a user may have with a webserver across multiple HTTP requests.
  Add an ``:success` property to the ``ou:campaign`` form to track if a
  campaign was sucessful or not. Add an ``:goal`` property to the
  ``risk:attack`` form to track the specific goal of the attack. Add an
  ``:desc`` property to the ``proj:project`` form to capture a description of
  the project.
  (`#2333 <https://github.com/vertexproject/synapse/pull/2333>`_)

Bugfixes
--------
- Fix an issue with ``synapse.lib.rstorm`` where multiline node properties
  could produce RST which did not render properly.
  (`#2331 <https://github.com/vertexproject/synapse/pull/2331>`_)

Improved Documentation
----------------------
- Clean up the documentation for the Storm ``wget`` command.
  (`#2325 <https://github.com/vertexproject/synapse/pull/2325>`_)


v2.56.0 - 2021-08-19
====================

Features and Enhancements
-------------------------
- Refactor some internal Axon APIs for downstream use.
  (`#2330 <https://github.com/vertexproject/synapse/pull/2330>`_)

Bugfixes
--------
- Resolve an ambiguity in the Storm grammar with yield statement and dollar
  expressions inside filter expression. There is a slight backwards
  incompatibility with this change, as dollar expressions insider of filter
  expressions now require a ``$`` prepended where before it was optional.
  (`#2322 <https://github.com/vertexproject/synapse/pull/2322>`_)


v2.55.0 - 2021-08-18
====================

Features and Enhancements
-------------------------

- Add ``$node.props.set()`` Stormtypes API to allow programmatically setting
  node properties.
  (`#2324 <https://github.com/vertexproject/synapse/pull/2324>`_)
- Deny non-runtsafe invocations of the following Storm commands:
  (`#2326 <https://github.com/vertexproject/synapse/pull/2326>`_)

    - ``graph``
    - ``iden``
    - ``movetag``
    - ``parallel``
    - ``tee``
    - ``tree``

- Add a ``Axon.hashset()`` API to get the md5, sha1, sha256 and sha512 hashes
  of file in the Axon. This is exposed in Stormtypes via the
  ``$lib.bytes.hashset()`` API.
  (`#2327 <https://github.com/vertexproject/synapse/pull/2327>`_)
- Add the ``synapse.servers.stemcell`` server and a new Docker image,
  ``vertexproject/synaspe-stemcell``. The Stemcell server is similar to the
  ``synapse.servers.cell`` server, except it resolves the Cell ctor from the
  ``cell:ctor`` key from the ``cell.yaml`` file, or from the
  ``SYN_STEM_CELL_CTOR`` environment variable.
  (`#2328 <https://github.com/vertexproject/synapse/pull/2328>`_)


v2.54.0 - 2021-08-05
====================

Features and Enhancements
-------------------------

- Add ``storm-envvar`` directive to RST preprocessor to include environment
  variables in ``storm-pre`` directive execution context.
  (`#2321 <https://github.com/vertexproject/synapse/pull/2321>`_)
- Add new ``diff`` storm command to allow users to easily lift the set of nodes
  with changes in the top layer of a forked view.  Also adds the ``--no-tags``
  option to the ``merge`` command to allow users to omit ``tag:add`` node edits
  and newly constructed ``syn:tag`` nodes when merging selected nodes.
  (`#2320 <https://github.com/vertexproject/synapse/pull/2320>`_)
- Adds the following properties to the data model:
  (`#2319 <https://github.com/vertexproject/synapse/pull/2319>`_)

    - ``biz:deal:buyer:org``
    - ``biz:deal:buyer:orgname``
    - ``biz:deal:buyer:orgfqdn``
    - ``biz:deal:seller:org``
    - ``biz:deal:seller:orgname``
    - ``biz:deal:seller:orgfqdn``
    - ``biz:prod:madeby:org``
    - ``biz:prod:madeby:orgname``
    - ``biz:prod:madeby:orgfqdn``
    - ``ou:opening:posted``
    - ``ou:opening:removed``
    - ``ou:org:vitals``

- Updates ``storm-mock-http`` to support multiple HTTP requests/responses
  in RST preprocessor.
  (`#2317 <https://github.com/vertexproject/synapse/pull/2317>`_)

v2.53.0 - 2021-08-05
====================

This release contains an automatic data migration that may cause additional
startup time on the first boot. This is done to unique array properties which
previously were not uniqued. Deployments with startup or liveliness probes
should have those disabled while this upgrade is performed to prevent
accidental termination of the Cortex process. Please ensure you have a tested
backup available before applying this update.

Features and Enhancements
-------------------------
- Add an ``embeds`` option to Storm to allow extracting additional data
  when performing queries.
  (`#2314 <https://github.com/vertexproject/synapse/pull/2314>`_)
- Enforce node data permissions at the Layer boundary. Remove the
  ``node.data.get`` and ``node.data.list`` permissions.
  (`#2311 <https://github.com/vertexproject/synapse/pull/2311>`_)
- Add ``auth.self.set.email``, ``auth.self.set.name``,
  ``auth.self.set.passwd`` permissions on users when changing those values.
  These permissions default to being allowed, allowing a rule to be created
  that can deny users from changing these values.
  (`#2311 <https://github.com/vertexproject/synapse/pull/2311>`_)
- Add ``$lib.inet.smtp`` to allow sending email messages from Storm.
  (`#2315 <https://github.com/vertexproject/synapse/pull/2315>`_)
- Warn if a LMDB commit operation takes too long.
  (`#2316 <https://github.com/vertexproject/synapse/pull/2316>`_)
- Add new data types, ``taxon`` and ``taxonomy``, to describe hierarchical
  taxonomies.
  (`#2312 <https://github.com/vertexproject/synapse/pull/2312>`_)
- Add a new Business Development model. This allows tracking items related to
  contract, sales, and purchasing lifecycles. This adds the following new forms
  to the data model: ``biz:dealtype``, ``biz:prodtype``, ``biz:dealstatus``,
  ``biz:rfp``, ``biz:deal``, ``biz:bundle``, ``biz:product``, and
  ``biz:stake``. The Org model is also updated to add new forms for supporting
  parts of the business lifecycle, adding ``ou:jobtype``,
  ``ou:jobtitle``, ``ou:employment``, ``ou:opening``, ``ou:vitals``,
  ``ou:camptype``, and ``ou:orgtype``, ``ou:conttype`` forms. The Person model
  got a new form, ``ps:workhist``.
  (`#2312 <https://github.com/vertexproject/synapse/pull/2312>`_)
- Add a ``:deleted`` property to ``inet:web:post``.
  (`#2312 <https://github.com/vertexproject/synapse/pull/2312>`_)
- Update the following array properties to be unique sets, and add a data
  model migration to update the data at rest:
  (`#2312 <https://github.com/vertexproject/synapse/pull/2312>`_)

    - ``edu:course:prereqs``
    - ``edu:class:assistants``
    - ``ou:org:subs``
    - ``ou:org:names``
    - ``ou:org:dns:mx``
    - ``ou:org:locations``
    - ``ou:org:industries``
    - ``ou:industry:sic``
    - ``ou:industry:subs``
    - ``ou:industry:isic``
    - ``ou:industry:naics``
    - ``ou:preso:sponsors``
    - ``ou:preso:presenters``
    - ``ou:conference:sponsors``
    - ``ou:conference:event:sponsors``
    - ``ou:conference:attendee:roles``
    - ``ou:conference:event:attendee:roles``
    - ``ou:contract:types``
    - ``ou:contract:parties``
    - ``ou:contract:requirements``
    - ``ou:position:reports``
    - ``ps:person:names``
    - ``ps:person:nicks``
    - ``ps:persona:names``
    - ``ps:persona:nicks``
    - ``ps:education:classes``
    - ``ps:contactlist:contacts``

Bugfixes
--------
- Prevent renaming the ``all`` role.
  (`#2313 <https://github.com/vertexproject/synapse/pull/2313>`_)

Improved Documentation
----------------------
- Add documentation about Linux kernel parameteres which can be tuned to
  affect Cortex performance.
  (`#2316 <https://github.com/vertexproject/synapse/pull/2316>`_)


v2.52.1 - 2021-07-30
====================

Bugfixes
--------
- Fix a display regression when enumerating Cron jobs with the Storm
  ``cron.list`` command.
  (`#2309 <https://github.com/vertexproject/synapse/pull/2309>`_)


v2.52.0 - 2021-07-29
====================

Features and Enhancements
-------------------------
- Add a new specification for defining input forms that a pure Storm command
  knows how to natively handle.
  (`#2301 <https://github.com/vertexproject/synapse/pull/2301>`_)
- Add ``Lib.reverse()`` and ``Lib.sort()`` methods to Stormtypes API.
  (`#2306 <https://github.com/vertexproject/synapse/pull/2306>`_)
- Add ``View.parent`` property in Stormtypes API.
  (`#2306 <https://github.com/vertexproject/synapse/pull/2306>`_)
- Support Telepath Share objects in Storm.
  (`#2293 <https://github.com/vertexproject/synapse/pull/2293>`_)
- Allow users to specify a view to run a cron job against, move a cron job to
  a new view, and update permission check for adding/moving cron jobs to views.
  (`#2292 <https://github.com/vertexproject/synapse/pull/2292>`_)
- Add CPE and software name infomation to the ``inet:flow`` form. Add
  ``it:av:prochit``, ``it:exec:thread``, ``it:exec:loadlib``,
  ``it:exec:mmap``, ``it:app:yara:procmatch`` forms to the infotech model.
  Add ``:names`` arrays to ``it:prod:soft`` and ``it:prod:softver`` forms
  to assist in entity resolution of software. Add a ``risk:alert`` form to
  the risk model to allow for capturing arbitrary alerts.
  (`#2304 <https://github.com/vertexproject/synapse/pull/2304>`_)
- Allow Storm packages to specify other packages they require and possible
  conflicts would prevent them from being installed in a Cortex.
  (`#2307 <https://github.com/vertexproject/synapse/pull/2307>`_)

Bugfixes
--------
- Specify the View when lifting ``syn:trigger`` runt nodes.
  (`#2300 <https://github.com/vertexproject/synapse/pull/2300>`_)
- Update the scrape URL regular expression to ignore trailing periods and
  commas.
  (`#2302 <https://github.com/vertexproject/synapse/pull/2302>`_)
- Fix a bug in Path scope for nodes yielding by pure Storm commands.
  (`#2305 <https://github.com/vertexproject/synapse/pull/2305>`_)


v2.51.0 - 2021-07-26
====================

Features and Enhancements
-------------------------
- Add a ``--size`` option to the Storm ``divert`` command to limit the number
  of times the generator is iterated.
  (`#2297 <https://github.com/vertexproject/synapse/pull/2297>`_)
- Add a ``perms`` key to the pure Storm command definition. This allows for
  adding intuitive permission boundaries for pure Storm commands which are
  checked prior to command execution.
  (`#2297 <https://github.com/vertexproject/synapse/pull/2297>`_)
- Allow full properties with comparators when specifying the destination
  or source when walking light edges.
  (`#2298 <https://github.com/vertexproject/synapse/pull/2298>`_)

Bugfixes
--------
- Fix an issue with LMDB slabs not being backed up if their directories did
  not end in ``.lmdb``.
  (`#2296 <https://github.com/vertexproject/synapse/pull/2296>`_)


v2.50.0 - 2021-07-22
====================

Features and Enhancements
-------------------------
- Add ``.cacheget()`` and ``cacheset()`` APIs to the Storm ``storm:node:data``
  object for easy caching of structured data on nodes based on time.
  (`#2290 <https://github.com/vertexproject/synapse/pull/2290>`_)
- Make the Stormtypes unique properly with a Set type. This does disallow the
  use of mutable types such as dictionaries inside of a Set.
  (`#2225 <https://github.com/vertexproject/synapse/pull/2225>`_)
- Skip executing non-runtsafe commands when there are no inbound nodes.
  (`#2291 <https://github.com/vertexproject/synapse/pull/2291>`_)
- Add ``asroot:perms`` key to Storm Package modules. This allows package
  authors to easily declare permissions their packages. Add Storm commands
  ``auth.user.add``, ``auth.role.add``, ``auth.user.addrule``,
  ``auth.role.addrule``, and ``pkg.perms.list`` to help with some of the
  permission management.
  (`#2294 <https://github.com/vertexproject/synapse/pull/2294>`_)


v2.49.0 - 2021-07-19
====================

Features and Enhancements
-------------------------
- Add a ``iden`` parameter when creating Cron jobs to allow the creation of
  jobs with stable identifiers.
  (`#2264 <https://github.com/vertexproject/synapse/pull/2264>`_)
- Add ``$lib.cell`` Stormtypes library to allow for introspection of the
  Cortex from Storm for Admin users.
  (`#2285 <https://github.com/vertexproject/synapse/pull/2285>`_)
- Change the Telepath Client connection loop error logging to log at the
  Error level instead of the Info level.
  (`#2283 <https://github.com/vertexproject/synapse/pull/2283>`_)
- Make the tag part normalization more resilient to data containing non-word
  characters.
  (`#2289 <https://github.com/vertexproject/synapse/pull/2289>`_)
- Add ``$lib.tags.prefix()`` Stormtypes to assist with normalizing a list of
  tags with a common prefix.
  (`#2289 <https://github.com/vertexproject/synapse/pull/2289>`_)
- Do not allow the Storm ``divert`` command to work with non-generator
  functions.
  (`#2282 <https://github.com/vertexproject/synapse/pull/2282>`_)

Bugfixes
--------
- Fix an issue with Storm command execution with non-runtsafe options.
  (`#2284 <https://github.com/vertexproject/synapse/pull/2284>`_)
- Log when the process pool fails to initialize. This may occur in certain
  where CPython multiprocessing primitives are not completely supported.
  (`#2288 <https://github.com/vertexproject/synapse/pull/2288>`_)
- In the Telepath Client, fix a race condition which could have raised an
  AttributeError in Aha resolutions.
  (`#2286 <https://github.com/vertexproject/synapse/pull/2286>`_)
- Prevent the reuse of a Telepath Client object when it has been fini'd.
  (`#2286 <https://github.com/vertexproject/synapse/pull/2286>`_)
- Fix a race condition in the Aha server when handling distributed changes
  which could have left the service in a desynchronized state.
  (`#2287 <https://github.com/vertexproject/synapse/pull/2287>`_)

Improved Documentation
----------------------
- Update the documentation for the ``synapse.tools.feed`` tool.
  (`#2279 <https://github.com/vertexproject/synapse/pull/2279>`_)


v2.48.0 - 2021-07-13
====================

Features and Enhancements
-------------------------
- Add a Storm ``divert`` command to ease the implementation of ``--yield``
  constructs in Storm commands. This optionally yields nodes from a generator,
  or yields inbound nodes, while still ensuring the generator is conusmed.
  (`#2277 <https://github.com/vertexproject/synapse/pull/2277>`_)
- Add Storm runtime debug tracking. This is a boolean flag that can be set or
  unset via ``$lib.debug``. It can be used by Storm packages to determine if
  they should take extra actions, such as additional print statements, without
  needing to track additional function arguments in their implementations.
  (`#2278 <https://github.com/vertexproject/synapse/pull/2278>`_)

Bugfixes
--------
- Fix an ambiguity in the Storm grammar.
  (`#2280 <https://github.com/vertexproject/synapse/pull/2280>`_)
- Fix an issue where form autoadds could fail to be created in specific cases of
  the model.
  (`#2273 <https://github.com/vertexproject/synapse/pull/2273>`_)


v2.47.0 - 2021-07-07
====================

Features and Enhancements
-------------------------
- Add ``$lib.regex.replace()`` Stormtypes API to perform regex based
  replacement of string parts.
  (`#2274 <https://github.com/vertexproject/synapse/pull/2274>`_)
- Add universal properties to the dictionary returned by
  ``Cortex.getModelDict()`` as a ``univs`` key.
  (`#2276 <https://github.com/vertexproject/synapse/pull/2276>`_)
- Add additional ``asyncio.sleep(0)`` statements to ``Layer._storNodeEdits``
  to improve Cortex responsiveness when storing large numbers of edits at
  once.
  (`#2275 <https://github.com/vertexproject/synapse/pull/2275>`_)


v2.46.0 - 2021-07-02
====================

Features and Enhancements
-------------------------
- Update the Cortex ``storm:log:level`` configuration value to accept string
  values such as ``DEBUG``, ``INFO``, etc. The default log level for Storm
  query logs is now ``INFO`` level.
  (`#2262 <https://github.com/vertexproject/synapse/pull/2262>`_)
- Add ``$lib.regex.findall()`` Stormtypes API to find all matching parts of a
  regular expression in a given string.
  (`#2265 <https://github.com/vertexproject/synapse/pull/2265>`_)
- Add ``$lib.inet.http.head()`` Stormtypes API to perform easy HEAD requests,
  and ``allow_redirects`` arguments to existing ``lib.inet.http`` APIs to
  allow controlling the redirect behavior.
  (`#2268 <https://github.com/vertexproject/synapse/pull/2268>`_)
- Add ``$lib.storm.eval()`` API to evaluate Storm values from strings.
  (`#2269 <https://github.com/vertexproject/synapse/pull/2269>`_)
- Add ``getSystemInfo()`` and ``getBackupInfo()`` APIS to the Cell for getting
  useful system information.
  (`#2267 <https://github.com/vertexproject/synapse/pull/2267>`_)
- Allow lists in rstorm bodies.
  (`#2261 <https://github.com/vertexproject/synapse/pull/2261>`_)
- Add a ``:desc`` secondary property to the ``proj:sprint`` form.
  (`#2261 <https://github.com/vertexproject/synapse/pull/2261>`_)
- Call _normStormPkg in all loadStormPkg paths, move validation to post
  normalization and remove mutation in validator
  (`#2260 <https://github.com/vertexproject/synapse/pull/2260>`_)
- Add ``SYN_SLAB_COMMIT_PERIOD`` environment variable to control the Synapse
  slab commit period. Add ``layer:lmdb:max_replay_log`` Cortex option to
  control the slab replay log size.
  (`#2266 <https://github.com/vertexproject/synapse/pull/2266>`_)
- Update Ahacell log messages.
  (`#2270 <https://github.com/vertexproject/synapse/pull/2270>`_)

Bugfixes
--------
- Fix an issue where the ``Trigger.pack()`` method failed when the user that
  created the trigger had been deleted.
  (`#2263 <https://github.com/vertexproject/synapse/pull/2263>`_)

Improved Documentation
----------------------
- Update the Cortex devops documentation for the Cortex to document the Storm
  query logging. Update the Cell devops documentation to explain the Cell
  logging and how to enable structured (JSON) logging output.
  (`#2262 <https://github.com/vertexproject/synapse/pull/2262>`_)
- Update Stormtypes API documentation for ``bool``, ``storm:project:epic``,
  ``storm:project:epics``, ``storm:project:ticket``,
  ``storm:project:tickets``, ``storm:project:sprint``,
  ``storm:project:sprints``, ``storm:project``, ``storm:stix:bundle`` types.
  (`#2261 <https://github.com/vertexproject/synapse/pull/2261>`_)


v2.45.0 - 2021-06-25
====================

Features and Enhancements
-------------------------
- Add a application level process pool the base Cell implemenation. Move the
  processing of Storm query text into the process pool.
  (`#2250 <https://github.com/vertexproject/synapse/pull/2250>`_)
  (`#2259 <https://github.com/vertexproject/synapse/pull/2259>`_)
- Minimize the re-validation of Storm code on Cortex boot.
  (`#2257 <https://github.com/vertexproject/synapse/pull/2257>`_)
- Add the ``ou:preso`` form to record conferences and presentations. Add a
  ``status`` secondary property to the ``it:mitre:attack:technique`` form to
  track if techniques are current, deprecated or withdrawn.
  (`#2254 <https://github.com/vertexproject/synapse/pull/2254>`_)

Bugfixes
--------
- Remove incorrect use of ``cmdopts`` in Storm command definitions unit tests.
  (`#2258 <https://github.com/vertexproject/synapse/pull/2258>`_


v2.44.0 - 2021-06-23
====================

This release contains an automatic data migration that may cause additional
startup time on the first boot. This only applies to a Cortex that is using
user defined tag properties or using ``ps:person:name`` properties.
Deployments with startup or liveliness probes should have those disabled while
this upgrade is performed to prevent accidental termination of the Cortex
process. Please ensure you have a tested backup available before applying this
update.

Features and Enhancements
-------------------------
- Add a ``.move()`` method on Stormtypes ``storm:trigger`` objects to allow
  moving a Trigger from one View to another View.
  (`#2252 <https://github.com/vertexproject/synapse/pull/2252>`_)
- When the Aha service marks a service as down, log why that service is being
  marked as such.
  (`#2255 <https://github.com/vertexproject/synapse/pull/2255>`_)
- Add ``:budget:price`` property to the ``ou:contract`` form. Add ``:settled``
  property to the ``econ:purchase`` form.
  (`#2253 <https://github.com/vertexproject/synapse/pull/2253>`_

Bugfixes
--------
- Make the array property ``ps:person:names`` a unique array property.
  (`#2253 <https://github.com/vertexproject/synapse/pull/2253>`_
- Add missing tagprop key migration for the bybuidv3 index.
  (`#2256 <https://github.com/vertexproject/synapse/pull/2256>`_)


v2.43.0 - 2021-06-21
====================

Features and Enhancements
-------------------------
- Add a ``.type`` string to the Stormtypes ``storm:auth:gate`` object to
  allow a user to identify the type of auth gate it is.
  (`#2238 <https://github.com/vertexproject/synapse/pull/2238>`_)
- Add ``$lib.user.iden`` reference to the Stormtype ``$lib.user`` to get the
  iden of the current user executing Storm code.
  (`#2236 <https://github.com/vertexproject/synapse/pull/2236>`_)
- Add a ``--no-build`` option to ``synapse.tools.genpkg`` to allow pushing an
  a complete Storm Package file.
  (`#2231 <https://github.com/vertexproject/synapse/pull/2231>`_)
  (`#2232 <https://github.com/vertexproject/synapse/pull/2232>`_)
  (`#2233 <https://github.com/vertexproject/synapse/pull/2233>`_)
- The Storm ``movetag`` command now checks for cycles when setting the
  ``syn:tag:isnow`` property.
  (`#2229 <https://github.com/vertexproject/synapse/pull/2229>`_)
- Deprecate the ``ou:org:has`` form, in favor of using light edges for
  storing those relationships.
  (`#2234 <https://github.com/vertexproject/synapse/pull/2234>`_)
- Add a ``description`` property to the ``ou:industry`` form.
  (`#2239 <https://github.com/vertexproject/synapse/pull/2239>`_)
- Add a ``--name`` parameter to the Storm ``trigger.add`` command to name
  triggers upon creation.
  (`#2237 <https://github.com/vertexproject/synapse/pull/2237>`_)
- Add ``regx`` to the ``BadTypeValu`` exception of the ``str`` type when
  a regular expression fails to match.
  (`#2240 <https://github.com/vertexproject/synapse/pull/2240>`_)
- Consolidate Storm parsers to a single Parser object to improve startup time.
  (`#2247 <https://github.com/vertexproject/synapse/pull/2247>`_)
- Improve error logging in the Cortex ``callStorm()`` and ``storm()`` APIs.
  (`#2243 <https://github.com/vertexproject/synapse/pull/2243>`_)
- Add ``from:contract``, ``to:contract``, and ``memo`` properties to the
  ``econ:acct:payment`` form.
  (`#2248 <https://github.com/vertexproject/synapse/pull/2248>`_)
- Improve the Cell backup streaming APIs link cleanup.
  (`#2249 <https://github.com/vertexproject/synapse/pull/2249>`_)

Bugfixes
--------
- Fix issue with grabbing the incorrect Telepath link when performing a Cell
  backup.
  (`#2246 <https://github.com/vertexproject/synapse/pull/2246>`_)
- Fix missing ``toprim`` calls in ``$lib.inet.http.connect()``.
  (`#2235 <https://github.com/vertexproject/synapse/pull/2235>`_)
- Fix missing Storm command form hint schema from the Storm Package schema.
  (`#2242 <https://github.com/vertexproject/synapse/pull/2242>`_)

Improved Documentation
----------------------
- Add documentation for deprecated model forms and properties, along with
  modeling alternatives.
  (`#2234 <https://github.com/vertexproject/synapse/pull/2234>`_)
- Update documentation for the Storm ``help`` command to add examples of
  command substring matching.
  (`#2241 <https://github.com/vertexproject/synapse/pull/2241>`_)

v2.42.2 - 2021-06-11
====================

Bugfixes
--------
- Protect against a few possible RuntimeErrors due to dictionary sizes
  changing during iteration.
  (`#2227 <https://github.com/vertexproject/synapse/pull/2227>`_)
- Fix StormType ``Lib`` lookups with imported modules which were raising
  a ``TypeError`` instead of a ``NoSuchName`` error.
  (`#2228 <https://github.com/vertexproject/synapse/pull/2228>`_)
- Drop old Storm Packages if they are present when re-adding them. This fixes
  an issue with runtime updates leaving old commands in the Cortex.
  (`#2230 <https://github.com/vertexproject/synapse/pull/2230>`_)


v2.42.1 - 2021-06-09
====================

Features and Enhancements
-------------------------
- Add a ``--no-docs`` option to the  ``synapse.tools.genpkg`` tool. When used,
  this not embed inline documentation into the generated Storm packages.
  (`#2226 <https://github.com/vertexproject/synapse/pull/2226>`_)


v2.42.0 - 2021-06-03
====================

Features and Enhancements
-------------------------
- Add a ``--headers`` and ``--parameters`` arguments to the Storm ``wget``
  command. The default headers now includes a browser like UA string.
  (`#2208 <https://github.com/vertexproject/synapse/pull/2208>`_)
- Add the ability to modify the name of a role via Storm.
  (`#2222 <https://github.com/vertexproject/synapse/pull/2222>`_)

Bugfixes
--------
- Fix an issue in the JsonStor cell where there were missing fini calls.
  (`#2223 <https://github.com/vertexproject/synapse/pull/2223>`_)
- Add a missing timeout to an ``getAhaSvc()`` call.
  (`#2224 <https://github.com/vertexproject/synapse/pull/2224>`_)
- Change how tagprops are serialized to avoid a issue with sending packed
  nodes over HTTP APIs. This changes the packed node structure of tagprops
  from a dictionary keyed with ``(tagname, propertyname)`` to a dictionary
  keyed off of the ``tagname``, which now points to a dictionary containing
  the ``propertyname`` which represents the value of the tagprop.
  (`#2221` <https://github.com/vertexproject/synapse/pull/2221>`_)


v2.41.1 - 2021-05-27
====================

Bugfixes
--------
- Add PR ``#2117`` to bugfix list in CHANGLOG.rst for v2.41.0 :D

v2.41.0 - 2021-05-27
====================

Features and Enhancements
-------------------------
- Add an ``it:cmd`` form and update the ``it:exec:proc:cmd`` property to
  use it. This release includes an automatic data migration on startup to
  update the ``it:exec:proc:cmd`` on any existing ``it:exec:proc`` nodes.
  (`#2219 <https://github.com/vertexproject/synapse/pull/2219>`_)

Bugfixes
--------
- Fix an issue where passing a Base object to a sub-runtime in Storm
  did not correctly increase the reference count.
  (`#2216 <https://github.com/vertexproject/synapse/pull/2216>`_)
- Fix an issue where the ``tee`` command could potentially run the
  specified queries twice.
  (`#2218 <https://github.com/vertexproject/synapse/pull/2218>`_)
- Fix for rstorm using mock when the HTTP body is bytes.
  (`#2217 <https://github.com/vertexproject/synapse/pull/2217>`_)

v2.40.0 - 2021-05-26
====================

Features and Enhancements
-------------------------
- Add a ``--parallel`` switch to the ``tee`` Storm command. This allows for
  all of the Storm queries provided to the ``tee`` command to execute in
  parallel, potentially producing a mixed output stream of nodes.
  (`#2209 <https://github.com/vertexproject/synapse/pull/2209>`_)
- Convert the Storm Runtime object in a Base object, allowing for reference
  counted Storm variables which are made from Base objects and are properly
  torn down.
  (`#2203 <https://github.com/vertexproject/synapse/pull/2203>`_)
- Add ``$lib.inet.http.connect()`` method which creates a Websocket object
  inside of Storm, allowing a user to send and receive messages over a
  websocket.
  (`#2203 <https://github.com/vertexproject/synapse/pull/2203>`_)
- Support pivot join operations on tags.
  (`#2213 <https://github.com/vertexproject/synapse/pull/2213>`_)
- Add ``stormrepr()`` implementation for ``synapse.lib.stormtypes.Lib``, which
  allows for ``$lib.print()`` to display useful strings for Storm Libraries
  and imported modules.
  (`#2212 <https://github.com/vertexproject/synapse/pull/2212>`_)
- Add a storm API top updated a user name.
  (`#2214 <https://github.com/vertexproject/synapse/pull/2214>`_)

Bugfixes
--------
- Fix the logger name for ``synapse.lib.aha``.
  (`#2210 <https://github.com/vertexproject/synapse/pull/2210>`_)
- Log ``ImportError`` exceptions in ``synapse.lib.dyndeps.getDynMod``. This
  allows easier debugging when using the ``synapse.servers.cell`` server when
  running custom Cell implementations.
  (`#2211 <https://github.com/vertexproject/synapse/pull/2211>`_)
- Fix an issue where a Storm command which failed to set command arguments
  successfully would not teardown the Storm runtime.
  (`#2212 <https://github.com/vertexproject/synapse/pull/2212>`_)

v2.39.1 - 2021-05-21
====================

Bugfixes
--------
- Fix an issue with referencing the Telepath user session object prior to a
  valid user being set.
  (`#2207 <https://github.com/vertexproject/synapse/pull/2207>`_)


v2.39.0 - 2021-05-20
====================

Features and Enhancements
-------------------------

- Add more useful output to Storm when printing heavy objects with
  ``$lib.print()``.
  (`#2185 <https://github.com/vertexproject/synapse/pull/2185>`_)
- Check rule edits for roles against provided authgates in Storm.
  (`#2199 <https://github.com/vertexproject/synapse/pull/2199>`_)
- Add ``Str.rsplit()`` and maxsplit arguments to ``split()/rsplit()`` APIs
  in Storm.
  (`#2200 <https://github.com/vertexproject/synapse/pull/2200>`_)
- Add default argument values to the output of Storm command help output.
  (`#2198 <https://github.com/vertexproject/synapse/pull/2198>`_)
- Add a ``syn:tag:part`` Type and allow the ``syn:tag`` type to normalize a
  list of tag parts to create a tag string. This is intended to be used with
  the ``$lib.cast()`` function in Storm.
  (`#2192 <https://github.com/vertexproject/synapse/pull/2192>`_)
- Add debug logging to the Axon for reading, writing, or deleting of blobs.
  (`#2202 <https://github.com/vertexproject/synapse/pull/2202>`_)
- Add a timeout argument to the ``$lib.inet.http`` functions. The functions
  will all now always return a ``storm:http:resp`` object; if the ``.code``
  is -1, an unrecoverable exception occurred while making the request.
  (`#2205 <https://github.com/vertexproject/synapse/pull/2205>`_)
- Add support for embedding a logo and documentation into a Storm Package.
  (`#2204 <https://github.com/vertexproject/synapse/pull/2204>`_)

Bugfixes
--------
- Fix export filters to correctly filter tagprops.
  (`#2196 <https://github.com/vertexproject/synapse/pull/2196>`_)
- Fix an issue with Hotcount which prevented it from storing negative values.
  (`#2197 <https://github.com/vertexproject/synapse/pull/2197>`_)
- Fix an issue where ``hideconf`` configuration values were being included
  in autodoc output.
  (`#2199 <https://github.com/vertexproject/synapse/pull/2199>`_)


v2.38.0 - 2021-05-14
====================

Features and Enhancements
-------------------------
- Remove trigger inheritance from Views. Views will now only execute triggers
  which are created inside of them.
  (`#2189 <https://github.com/vertexproject/synapse/pull/2189>`_)
- Remove read-only property flags from secondary properties on ``file:bytes``
  nodes.
  (`#2191 <https://github.com/vertexproject/synapse/pull/2191>`_)
- Add a simple ``it:log:event`` form to capture log events.
  (`#2195 <https://github.com/vertexproject/synapse/pull/2195>`_)
- Add structured logging as an option for Synapse Cells. When enabled, this
  produces logs as JSONL sent to stderr. This can be set via the
  ``SYN_LOG_STRUCT`` environment variable, or adding the
  ``--structured-logging`` command line switch.
  (`#2179 <https://github.com/vertexproject/synapse/pull/2179>`_)
- Add a ``nodes.import`` command to import a ``.nodes`` file from a URL.
  (`#2186 <https://github.com/vertexproject/synapse/pull/2186>`_)
- Allow the ``desc`` key to View and Layer objects in Storm. This can be used
  to set descriptions for these objects.
  (`#2190 <https://github.com/vertexproject/synapse/pull/2190>`_)
- Use the gateiden in Storm auth when modifying rules; allowing users to share
  Views and Layers with other users.
  (`#2194 <https://github.com/vertexproject/synapse/pull/2194>`_)

Bugfixes
--------
- Fix an issue with Storm Dmon deletion not behaving properly in mirror
  configurations.
  (`#2188 <https://github.com/vertexproject/synapse/pull/2188>`_)
- Explicitly close generators in Telepath where an exception has caused the
  generator to exit early.
  (`#2183 <https://github.com/vertexproject/synapse/pull/2183>`_)
- Fix an issue where a trigger owner not having access to a view would
  cause the Storm pipeline to stop.
  (`#2189 <https://github.com/vertexproject/synapse/pull/2189>`_)


v2.37.0 - 2021-05-12
====================

Features and Enhancements
-------------------------
- Add a ``file:mime:image`` interface to the Synapse model for recording MIME
  specific metadata from image files.
  (`#2187 <https://github.com/vertexproject/synapse/pull/2187>`_)
- Add ``file:mime:jpg``, ``file:mime:tiff``, ``file:mime:gif`` and
  ``file:mime:png`` specific forms for recording metadata of those file types.
  (`#2187 <https://github.com/vertexproject/synapse/pull/2187>`_)
- Add ``$lib.pkg.has()`` Stormtype API to check for for the existence of a
  given Storm package by name.
  (`#2182 <https://github.com/vertexproject/synapse/pull/2182>`_)
- All ``None / $lib.null`` as input to setting a user password. This clears
  the password and prevents a user from being able to login.
  (`#2181 <https://github.com/vertexproject/synapse/pull/2181>`_)
- Grab any Layer push/pull offset values when calling ``Layer.pack()``.
  (`#2184 <https://github.com/vertexproject/synapse/pull/2184>`_)
- Move the retrieval of ``https:headers`` from HTTPAPI handlers into a
  function so that downstream implementers can redirect where the extra
  values are retrieved from.
  (`#2187 <https://github.com/vertexproject/synapse/pull/2187>`_)

Bugfixes
--------
- Fix an issue which allowed for deleted Storm Packages to be retrieved from
  memory.
  (`#2182 <https://github.com/vertexproject/synapse/pull/2182>`_)


v2.36.0 - 2021-05-06
====================

Features and Enhancements
-------------------------
- Add ``risk:vuln`` support to the default Stix 2.1 export, and capture
  vulnerability information used by threat actors and in campaigns. Add the
  ability to validate Stix 2.1 bundles to ensure that they are Stix 2.1 CS02
  compliant. Add the ability to lift Synapse nodes based on bundles which were
  previously exported from Synapse. The lift feature only works with bundles
  created with Synapse v2.36.0 or greater.
  (`#2174 <https://github.com/vertexproject/synapse/pull/2174>`_)
- Add a ``Str.upper()`` function for uppercasing strings in Storm.
  (`#2174 <https://github.com/vertexproject/synapse/pull/2174>`_)
- Automatically bump a user's StormDmon's when they are locked or unlocked.
  (`#2177 <https://github.com/vertexproject/synapse/pull/2177>`_)
- Add Storm Package support to ``synapse.tools.autodocs`` and update the
  rstorm implementation to capture additional directives.
  (`#2172 <https://github.com/vertexproject/synapse/pull/2172>`_)
- Tighten lark-parser version requirements.
  (`#2175 <https://github.com/vertexproject/synapse/pull/2175>`_)

Bugfixes
--------
- Fix reported layer size to represent actual disk usage.
  (`#2173 <https://github.com/vertexproject/synapse/pull/2173>`_)


v2.35.0 - 2021-04-27
====================

Features and Enhancements
-------------------------
- Add ``:issuer:cert`` and ``:selfsigned`` properties to the
  ``crypto:x509:cert`` form to enable modeling X509 certificate chains.
  (`#2163 <https://github.com/vertexproject/synapse/pull/2163>`_)
- Add a ``https:headers`` configuration option to the Cell to allow setting
  arbitrary HTTP headers for the Cell HTTPAPI server.
  (`#2164 <https://github.com/vertexproject/synapse/pull/2164>`_)
- Update the Cell HTTPAPI server to have a minimum TLS version of v1.2. Add a
  default ``/robots.txt`` route. Add ``X-XSS=Protection`` and
  ``X-Content-Type-Options`` headers to the default HTTPAPI responses.
  (`#2164 <https://github.com/vertexproject/synapse/pull/2164>`_)
- Update the minimum version of LMDB to ``1.2.1``.
  (`#2169 <https://github.com/vertexproject/synapse/pull/2169>`_)

Bugfixes
--------
- Improve the error message for Storm syntax error handling.
  (`#2162 <https://github.com/vertexproject/synapse/pull/2162>`_)
- Update the layer byarray index migration to account for arrays of
  ``inet:fqdn`` values.
  (`#2165 <https://github.com/vertexproject/synapse/pull/2165>`_)
  (`#2166 <https://github.com/vertexproject/synapse/pull/2166>`_)
- Update the ``vertexproject/synapse-aha``, ``vertexproject/synapse-axon``,
  ``vertexproject/synapse-cortex``, and ``vertexproject/synapse-cryotank``
  Docker images to use ``tini`` as a default entrypoint. This fixes an issue
  where signals were not properly being propagated to the Cells.
  (`#2168 <https://github.com/vertexproject/synapse/pull/2168>`_)
- Fix an issue with enfanged indicators which were not properly being lifted
  by Storm when operating in ``lookup`` mode.
  (`#2170 <https://github.com/vertexproject/synapse/pull/2170>`_)


v2.34.0 - 2021-04-20
====================

Features and Enhancements
-------------------------
- Storm function definitions now allow keyword arguments which may have
  default values. These must be read-only values.
  (`#2155 <https://github.com/vertexproject/synapse/pull/2155>`_)
  (`#2157 <https://github.com/vertexproject/synapse/pull/2157>`_)
- Add a ``getCellInfo()`` API to the ``Cell`` and ``CellAPI`` classes. This
  returns metadata about the cell, its version, and the currently installed
  Synapse version. Cell implementers who wish to expose Cell specific version
  information must adhere to conventiosn documented in the API docstrings of
  the function.
  (`#2151 <https://github.com/vertexproject/synapse/pull/2151>`_)
- Allow external Storm modules to be added in genpkg definitions.
  (`#2159 <https://github.com/vertexproject/synapse/pull/2159>`_)

Bugfixes
--------
- The ``$lib.layer.get()`` Stormtypes returned the top layer of the default
  view in the Cortex when called with no arguments, instead of the top layer
  of the current view. This now returns the top layer of the current view.
  (`#2156 <https://github.com/vertexproject/synapse/pull/2156>`_)
- Avoid calling ``applyNodeEdit`` when editing a tag on a Node and there are
  no edits to make.
  (`#2161 <https://github.com/vertexproject/synapse/pull/2161>`_)

Improved Documentation
----------------------
- Fix typo in docstrings from ``$lib.model.tags`` Stormtypes.
  (`#2160 <https://github.com/vertexproject/synapse/pull/2160>`_)


v2.33.1 - 2021-04-13
====================

Bugfixes
--------

- Fix a regression when expanding list objects in Storm.
  (`#2154 <https://github.com/vertexproject/synapse/pull/2154>`_)


v2.33.0 - 2021-04-12
====================

Features and Enhancements
-------------------------
- Add CWE and CVSS support to the ``risk:vuln`` form.
  (`#2143 <https://github.com/vertexproject/synapse/pull/2143>`_)
- Add a new Stormtypes library, ``$lib.infosec.cvss``, to assist with
  parsing CVSS data, computing scores, and updating ``risk:vuln`` nodes.
  (`#2143 <https://github.com/vertexproject/synapse/pull/2143>`_)
- Add ATT&CK, CWD, and CPE support to the IT model.
  (`#2143 <https://github.com/vertexproject/synapse/pull/2143>`_)
- Add ``it:network``, ``it:domain``, ``it:account``, ``it:group`` and
  ``it:login`` guid forms to model common IT concepts.
  (`#2096 <https://github.com/vertexproject/synapse/pull/2096>`_)
- Add a new model, ``project``, to model projects, tickets, sprints and epics.
  The preliminary forms for this model include ``proj:project``,
  ``proj:sprint``, ``proj:ticket``, ``proj:comment``, and ``projec:project``.
  (`#2096 <https://github.com/vertexproject/synapse/pull/2096>`_)
- Add a new Stormtypes library, ``$lib.project``, to assist with using the
  project model. The API is provisional.
  (`#2096 <https://github.com/vertexproject/synapse/pull/2096>`_)
- Allow lifting ``guid`` types with the prefix (``^=``) operator.
  (`#2096 <https://github.com/vertexproject/synapse/pull/2096>`_)
- Add ``ou:contest:result:url`` to record where to find contest results.
  (`#2144 <https://github.com/vertexproject/synapse/pull/2144>`_)
- Allow subquery as a value in additional places in Storm. This use must yield
  exactly one node. Secondary property assignments to array types may yield
  multiple nodes.
  (`#2137 <https://github.com/vertexproject/synapse/pull/2137>`_)
- Tighten up Storm iterator behavior on the backend. This should not have have
  user-facing changes in Storm behavior.
  (`#2148 <https://github.com/vertexproject/synapse/pull/2148>`_)
  (`#2096 <https://github.com/vertexproject/synapse/pull/2096>`_)
- Update the Cell backup routine so that it blocks the ioloop less.
  (`#2145 <https://github.com/vertexproject/synapse/pull/2145>`_)
- Expose the remote name and version of Storm Services in the ``service.list``
  command.
  (`#2149 <https://github.com/vertexproject/synapse/pull/2149>`_)
- Move test deprecated model elements into their own Coremodule.
  (`#2150 <https://github.com/vertexproject/synapse/pull/2150>`_)
- Update ``lark`` dependency.
  (`#2146 <https://github.com/vertexproject/synapse/pull/2146>`_)

Bugfixes
--------
- Fix incorrect grammer in model.edge commands.
  (`#2147 <https://github.com/vertexproject/synapse/pull/2147>`_)
- Reduce unit test memory usage.
  (`#2152 <https://github.com/vertexproject/synapse/pull/2152>`_)
- Pin ``jupyter-client`` library.
  (`#2153 <https://github.com/vertexproject/synapse/pull/2153>`_)


v2.32.1 - 2021-04-01
====================

Features and Enhancements
-------------------------
- The Storm ``$lib.exit()`` function now takes message arguments similar to
  ``$lib.warn()`` and fires that message into the run time as a ``warn`` prior
  to stopping the runtime.
  (`#2138 <https://github.com/vertexproject/synapse/pull/2138>`_)
- Update ``pygments`` minimum version to ``v2.7.4``.
  (`#2139 <https://github.com/vertexproject/synapse/pull/2139>`_)

Bugfixes
--------
- Do not allow light edge creation on runt nodes.
  (`#2136 <https://github.com/vertexproject/synapse/pull/2136>`_)
- Fix backup test timeout issues.
  (`#2141 <https://github.com/vertexproject/synapse/pull/2141>`_)
- Fix the ``synapse.lib.msgpack.en()`` function so that now raises the correct
  exceptions when operating in fallback mode.
  (`#2140 <https://github.com/vertexproject/synapse/pull/2140>`_)
- Fix the ``Snap.addNodes()`` API handling of deprecated model elements when
  doing bulk data ingest.
  (`#2142 <https://github.com/vertexproject/synapse/pull/2142>`_)


v2.32.0 - 2021-03-30
====================

Features and Enhancements
-------------------------
- Increase the verbosity of logging statements related to Cell backup
  operations. This allows for better visibility into what is happening
  while a backup is occurring.
  (`#2124 <https://github.com/vertexproject/synapse/pull/2124>`_)
- Add Telepath and Storm APIs for setting all the roles of a User at once.
  (`#2127 <https://github.com/vertexproject/synapse/pull/2127>`_)
- Expose the Synapse package commit hash over Telepath and Stormtypes.
  (`#2133 <https://github.com/vertexproject/synapse/pull/2133>`_)

Bugfixes
--------
- Increase the process spawn timeout for Cell backup operations. Prevent the
  Cell backup from grabbing lmdb transactions for slabs in the cell local tmp
  directory.
  (`#2124 <https://github.com/vertexproject/synapse/pull/2124>`_)


v2.31.1 - 2021-03-25
====================

Bugfixes
--------
- Fix a formatting issue preventing Python packages from being uploaded to
  PyPI.
  (`#2131 <https://github.com/vertexproject/synapse/pull/2131>`_)


v2.31.0 - 2021-03-24
====================

Features and Enhancements
-------------------------
- Add initial capability for exporting STIX 2.1 from the Cortex.
  (`#2120 <https://github.com/vertexproject/synapse/pull/2120>`_)
- Refactor how lift APIs are implemented, moving them up to the Cortex itself.
  This results in multi-layer lifts now yielding nodes in a sorted order.
  (`#2093 <https://github.com/vertexproject/synapse/pull/2093>`_)
  (`#2128 <https://github.com/vertexproject/synapse/pull/2128>`_)
- Add ``$lib.range()`` Storm function to generate ranges of integers.
  (`#2122 <https://github.com/vertexproject/synapse/pull/2122>`_)
- Add an ``errok`` option to the ``$lib.time.parse()`` Storm function to
  allow the function to return ``$lib.null`` if the time string fails to
  parse.
  (`#2126 <https://github.com/vertexproject/synapse/pull/2126>`_)
- Don't execute Cron jobs, Triggers, or StormDmons for locked users.
  (`#2123 <https://github.com/vertexproject/synapse/pull/2123>`_)
  (`#2129 <https://github.com/vertexproject/synapse/pull/2129>`_)
- The ``git`` commit hash is now embedded into the ``synapse.lib.version``
  module when building PyPi packages and Docker images.
  (`#2119 <https://github.com/vertexproject/synapse/pull/2119>`_)

Improved Documentation
----------------------
- Update Axon wget API documentation to note that we always store the body of
  the HTTP response, regardless of status code.
  (`#2125 <https://github.com/vertexproject/synapse/pull/2125>`_)


v2.30.0 - 2021-03-17
====================

Features and Enhancements
-------------------------
- Add ``$lib.trycast()`` to allow for Storm control flow based on type
  normalization.
  (`#2113 <https://github.com/vertexproject/synapse/pull/2113>`_)

Bugfixes
--------
- Resolve a bug related to pivoting to a secondary property that is an
  array value.
  (`#2111 <https://github.com/vertexproject/synapse/pull/2111>`_)
- Fix an issue with Aha and persisting the online state of services upon
  startup.
  (`#2103 <https://github.com/vertexproject/synapse/pull/2103>`_)
- Convert the type of ``inet:web:acct:singup:client:ipv6`` from a
  ``inet:ipv4`` to an ``inet:ipv6``.
  (`#2114 <https://github.com/vertexproject/synapse/pull/2114>`_)
- Fix an idempotency issue when deleting a custom form.
  (`#2112 <https://github.com/vertexproject/synapse/pull/2112>`_)

Improved Documentation
----------------------
- Update README.rst.
  (`#2115 <https://github.com/vertexproject/synapse/pull/2115>`_)
  (`#2117 <https://github.com/vertexproject/synapse/pull/2117>`_)
  (`#2116 <https://github.com/vertexproject/synapse/pull/2116>`_)


v2.29.0 - 2021-03-11
====================

This release includes a Cortex storage Layer bugfix. It does an automatic
upgrade upon startup to identify and correct invalid array index values.
Depending on time needed to perform this automatic upgrade, the Cortex may
appear unresponsive. Deployments with startup or liveliness probes should
have those disabled while this upgrade is performed to prevent accidental
termination of the Cortex process.

Features and Enhancements
-------------------------
- Add a ``reverse`` argument to ``$lib.sorted()`` to allow a Storm user
  to easily reverse an iterable item.
  (`#2109 <https://github.com/vertexproject/synapse/pull/2109>`_)
- Update minimum required versions of Tornado and PyYAML.
  (`#2108 <https://github.com/vertexproject/synapse/pull/2108>`_)

Bugfixes
--------
- Fix an issue with Array property type deletion not properly deleting values
  in the ``byarray`` index. This requires an automatic data migration done at
  Cortex startup to remove extra index values which may be present in the
  index.
  (`#2104 <https://github.com/vertexproject/synapse/pull/2104>`_)
  (`#2106 <https://github.com/vertexproject/synapse/pull/2106>`_)
- Fix issues with using the Storm ``?=`` operator with types which can
  generate multiple values from a given input string when making nodes.
  (`#2105 <https://github.com/vertexproject/synapse/pull/2105>`_)
  (`#2107 <https://github.com/vertexproject/synapse/pull/2107>`_)

Improved Documentation
----------------------
- Add Devops documentation explaining our Docker container offerings.
  (`#2104 <https://github.com/vertexproject/synapse/pull/2104>`_)
  (`#2110 <https://github.com/vertexproject/synapse/pull/2110>`_)


v2.28.1 - 2021-03-08
====================

Bugfixes
--------
- Fix ``$lib.model.prop()`` API when called with a universal property.
  It now returns ``$lib.null`` instead of raising an exception.
  (`#2100 <https://github.com/vertexproject/synapse/pull/2100>`_)
- Fix the streaming backup API when used with Telepath and SSL.
  (`#2101 <https://github.com/vertexproject/synapse/pull/2101>`_)

Improved Documentation
----------------------
- Add API documentation for the Axon.
  (`#2098 <https://github.com/vertexproject/synapse/pull/2098>`_)
- Update the Storm pivot reference documentation.
  (`#2101 <https://github.com/vertexproject/synapse/pull/2101>`_)


v2.28.0 - 2021-02-26
====================

Features and Enhancements
-------------------------
- Add ``String.reverse()`` Stormtypes API to reverse a string.
  (`#2086 <https://github.com/vertexproject/synapse/pull/2086>`_)
- Add Cell APIs for streaming compressed backups.
  (`#2084 <https://github.com/vertexproject/synapse/pull/2084>`_)
  (`#2091 <https://github.com/vertexproject/synapse/pull/2091>`_)
- Refactor ``snap.addNodes()`` to reduce the transaction count.
  (`#2087 <https://github.com/vertexproject/synapse/pull/2087>`_)
  (`#2090 <https://github.com/vertexproject/synapse/pull/2090>`_)
- Add ``$lib.axon.list()`` Stormtypes API to list hashes in an Axon.
  (`#2088 <https://github.com/vertexproject/synapse/pull/2088>`_)
- Add user permissions requirements for Aha CSR signing.
  (`#2089 <https://github.com/vertexproject/synapse/pull/2089>`_)
- Add ``aha:svcinfo`` configuration option for the base Cell.
  (`#2089 <https://github.com/vertexproject/synapse/pull/2089>`_)
- Add interfaces to the output of ``model.getModelDefs()`` and the
  ``getModelDict()`` APIs.
  (`#2092 <https://github.com/vertexproject/synapse/pull/2092>`_)
- Update pylmdb to ``v1.1.1``.
  (`#2076 <https://github.com/vertexproject/synapse/pull/2076>`_)

Bugfixes
--------
- Fix incorrect permissions check in the ``merge --diff`` Storm command.
  (`#2085 <https://github.com/vertexproject/synapse/pull/2085>`_)
- Fix service teardown issue in Aha service on fini.
  (`#2089 <https://github.com/vertexproject/synapse/pull/2089>`_)
- Fix possible ``synapse.tools.cmdr`` teardown issue when using Aha.
  (`#2089 <https://github.com/vertexproject/synapse/pull/2089>`_)
- Cast ``synapse_minversion`` from Storm Packages into a tuple to avoid
  packages added with HTTP endpoints from failing to validate.
  (`#2095 <https://github.com/vertexproject/synapse/pull/2095>`_)

Improved Documentation
----------------------
- Add documentation for the Aha discovery service.
  (`#2089 <https://github.com/vertexproject/synapse/pull/2089>`_)
- Add documentation for assigning secondary properties via subquery syntax.
  (`#2097 <https://github.com/vertexproject/synapse/pull/2097>`_)

v2.27.0 - 2021-02-16
====================

Features and Enhancements
-------------------------
- Allow property assignment and array operations from subqueries.
  (`#2072 <https://github.com/vertexproject/synapse/pull/2072>`_)
- Add APIs to the Axon to allow the deletion of blobs via Telepath and HTTP
  APIs.
  (`#2080 <https://github.com/vertexproject/synapse/pull/2080>`_)
- Add a ``str.slice()`` stormtypes method to allow easy string slicing.
  (`#2083 <https://github.com/vertexproject/synapse/pull/2083>`_)
- Modularize the Storm HTTP API handlers.
  (`#2082 <https://github.com/vertexproject/synapse/pull/2082>`_)

Bugfixes
--------
- Fix Agenda events which were not being properly tracked via the Nexus.
  (`#2078 <https://github.com/vertexproject/synapse/pull/2078>`_)

Improved Documentation
----------------------
- Add documentation for the Cortex ``/api/v1/storm/export`` HTTP endpoint.
  This also included documentation for the scrub option in Storm.
  (`#2079 <https://github.com/vertexproject/synapse/pull/2079>`_)
- Add a Code of Conduct for Synapse.
  (`#2081 <https://github.com/vertexproject/synapse/pull/2081>`_)


v2.26.0 - 2021-02-05
====================

Features and Enhancements
-------------------------
- Add Storm commands for easily adding, deleting, and listing layer push
  and pull configurations.
  (`#2071 <https://github.com/vertexproject/synapse/pull/2071>`_)

Bugfixes
--------
- Fix ``layer.getPropCount()`` API for universal properties.
  (`#2073 <https://github.com/vertexproject/synapse/pull/2073>`_)
- Add a missing async yield in ``Snap.addNodes()``.
  (`#2074 <https://github.com/vertexproject/synapse/pull/2074>`_)
- Constrain lmdb version due to unexpected behavior in ``v1.1.0``.
  (`#2075 <https://github.com/vertexproject/synapse/pull/2075>`_)

Improved Documentation
----------------------
- Update user docs for Storm flow control and data model references.
  (`#2066 <https://github.com/vertexproject/synapse/pull/2066>`_)


v2.25.0 - 2021-02-01
====================

Features and Enhancements
-------------------------
- Implement tag model based pruning behavior for controlling how individual
  tag trees are deleted from nodes.
  (`#2067 <https://github.com/vertexproject/synapse/pull/2067>`_)
- Add model interfaces for defining common sets of properties for forms,
  starting with some file mime metadata.
  (`#2040 <https://github.com/vertexproject/synapse/pull/2040>`_)
- Add ``file:mime:msdoc``, ``file:mime:msxls``, ``file:mime:msppt``, and
  ``file:mime:rtf`` forms.
  (`#2040 <https://github.com/vertexproject/synapse/pull/2040>`_)
- Tweak the ival normalizer to auto-expand intervals with a single element.
  (`#2070 <https://github.com/vertexproject/synapse/pull/2070>`_)
- Removed the experimental ``spawn`` feature of the Storm runtime.
  (`#2068 <https://github.com/vertexproject/synapse/pull/2068>`_)

Bugfixes
--------
- Add a missing async yield statement in ``View.getEdgeVerbs()``.
  (`#2069 <https://github.com/vertexproject/synapse/pull/2069>`_)

Improved Documentation
----------------------
- Correct incorrect references to the ``synapse.tools.easycert``
  documentation.
  (`#2065 <https://github.com/vertexproject/synapse/pull/2065>`_)


v2.24.0 - 2021-01-29
====================

Features and Enhancements
-------------------------
- Add support for storing model metadata for tags and support for enforcing
  tag trees using regular expressions.
  (`#2056 <https://github.com/vertexproject/synapse/pull/2056>`_)
- Add ``ou:contest:url`` secondary property.
  (`#2059 <https://github.com/vertexproject/synapse/pull/2059>`_)
- Add ``synapse.lib.autodoc`` to collect some Storm documentation helpers
  into a single library.
  (`#2034 <https://github.com/vertexproject/synapse/pull/2034>`_)
- Add ``tag.prune`` Storm command to remove parent tags when removing a
  leaf tag from a node.
  (`#2062 <https://github.com/vertexproject/synapse/pull/2062>`_)
- Update the ``msgpack`` Python dependency to version ``v1.0.2``.
  (`#1735 <https://github.com/vertexproject/synapse/pull/1735>`_)
- Add logs to Cell backup routines.
  (`#2060 <https://github.com/vertexproject/synapse/pull/2060>`_)
- Export the Layer iterrows APIs to the CoreApi.
  (`#2061 <https://github.com/vertexproject/synapse/pull/2061>`_)

Bugfixes
--------
- Do not connect to Aha servers when they are not needed.
  (`#2058 <https://github.com/vertexproject/synapse/pull/2058>`_)
- Make the array property ``ou:org:industries`` a unique array property.
  (`#2059 <https://github.com/vertexproject/synapse/pull/2059>`_)
- Add permission checks to the Storm ``movetag`` command.
  (`#2063 <https://github.com/vertexproject/synapse/pull/2063>`_)
- Add permissions checks to the Storm ``edges.del`` command.
  (`#2064 <https://github.com/vertexproject/synapse/pull/2064>`_)

Improved Documentation
----------------------
- Add documentation for the ``synapse.tools.genpkg`` utility, for loading
  Storm packages into a Cortex.
  (`#2057 <https://github.com/vertexproject/synapse/pull/2057>`_)
- Refactor the Stormtypes documentation generation to make it data driven.
  (`#2034 <https://github.com/vertexproject/synapse/pull/2034>`_)


v2.23.0 - 2021-01-21
====================

Features and Enhancements
-------------------------
- Add support for ndef based light edge definitions in the ``syn.nodes``
  feed API.
  (`#2051 <https://github.com/vertexproject/synapse/pull/2051>`_)
  (`#2053 <https://github.com/vertexproject/synapse/pull/2053>`_)
- Add ISIC codes to the ``ou:industry`` form.
  (`#2054 <https://github.com/vertexproject/synapse/pull/2054>`_)
  (`#2055 <https://github.com/vertexproject/synapse/pull/2055>`_)
- Add secondary properties ``:loc``, ``:latlong``, and ``:place`` to the
  ``inet:web:action`` and ``inet:web:logon`` forms.
  (`#2052 <https://github.com/vertexproject/synapse/pull/2052>`_)
- Add secondary property ``:enabled`` to the form ``it:app:yara:rule``.
  (`#2052 <https://github.com/vertexproject/synapse/pull/2052>`_)
- Deprecate the ``file:string`` and ``ou:member`` forms, in favor of
  using light edges for storing those relationships.
  (`#2052 <https://github.com/vertexproject/synapse/pull/2052>`_)


v2.22.0 - 2021-01-19
====================

Features and Enhancements
-------------------------
- Allow expression statements to be used in Storm filters.
  (`#2041 <https://github.com/vertexproject/synapse/pull/2041>`_)
- Add ``file:subfile:path`` secondary property to record the path a file was
  stored in a parent file. The corresponding ``file:subfile:name`` property is
  marked as deprecated.
  (`#2043 <https://github.com/vertexproject/synapse/pull/2043>`_)
- Make the Axon ``wget()`` timeout a configurable parameter.
  (`#2047 <https://github.com/vertexproject/synapse/pull/2047>`_)
- Add a ``Cortex.exportStorm()`` on the Cortex which allows for exporting
  nodes from a Storm query which can be directly ingested with the
  ``syn.nodes`` feed function. If the data is serialized using msgpack and
  stored in a Axon, it can be added to a Cortex with the new
  ``Cortex.feedFromAxon()`` API. A new HTTP API, ``/api/v1/storm/export``,
  can be used to get a msgpacked file using this export interface.
  (`#2045 <https://github.com/vertexproject/synapse/pull/2045>`_)

Bugfixes
--------
- Fix issues in the Layer push and pull loop code.
  (`#2044 <https://github.com/vertexproject/synapse/pull/2044>`_)
  (`#2048 <https://github.com/vertexproject/synapse/pull/2048>`_)
- Add missing ``toprim()`` and ``tostr()`` calls for the Stormtypes Whois
  guid generation helpers.
  (`#2046 <https://github.com/vertexproject/synapse/pull/2046>`_)
- Fix behavior in the Storm lookup mode which failed to lookup some expected
  results.
  (`#2049 <https://github.com/vertexproject/synapse/pull/2049>`_)
- Fix ``$lib.pkg.get()`` return value when the package is not present.
  (`#2050 <https://github.com/vertexproject/synapse/pull/2050>`_)


v2.21.1 - 2021-01-04
====================

Bugfixes
--------
- Fix a variable scoping issue causing a race condition.
  (`#2042 <https://github.com/vertexproject/synapse/pull/2042>`_)


v2.21.0 - 2020-12-31
====================

Features and Enhancements
-------------------------
- Add a Storm ``wget`` command which will download a file from a URL using
  the Cortex Axon and yield ``inet:urlfile`` nodes.
  (`#2035 <https://github.com/vertexproject/synapse/pull/2035>`_)
- Add a ``--diff`` option to the ``merge`` command to enumerate changes.
  (`#2037 <https://github.com/vertexproject/synapse/pull/2037>`_)
- Allow StormLib Layer API to dynamically update a Layer's logedits setting.
  (`#2038 <https://github.com/vertexproject/synapse/pull/2038>`_)
- Add StormLib APIs for adding and deleting extended model properties, forms
  and tag properties.
  (`#2039 <https://github.com/vertexproject/synapse/pull/2039>`_)

Bugfixes
--------
- Fix an issue with the JsonStor not created nested entries properly.
  (`#2036 <https://github.com/vertexproject/synapse/pull/2036>`_)


v2.20.0 - 2020-12-29
====================

Features and Enhancements
-------------------------
- Correct the StormType ``Queue.pop()`` API to properly pop and return
  only the item at the specified index or the next entry in the Queue.
  This simplifies the intent behind the ``.pop()`` operation; and removes
  the ``cull`` and ``wait`` parameters which were previously on the method.
  (`#2032 <https://github.com/vertexproject/synapse/pull/2032>`_)

Bugfixes
--------
- Use ``resp.iter_chunked`` in the Axon ``.wget()`` API to improve
  compatibility with some third party libraries.
  (`#2030 <https://github.com/vertexproject/synapse/pull/2030>`_)
- Require the use of a msgpack based deepcopy operation in handling
  storage nodes.
  (`#2031 <https://github.com/vertexproject/synapse/pull/2031>`_)
- Fix for ambiguous whitespace in Storm command argument parsing.
  (`#2033 <https://github.com/vertexproject/synapse/pull/2033>`_)


v2.19.0 - 2020-12-27
====================

Features and Enhancements
-------------------------

- Add APIs to remove decommissioned services from AHA servers.
- Add (optional) explicit network parameters to AHA APIs.
  (`#2029 <https://github.com/vertexproject/synapse/pull/2029>`_)

- Add cell.isCellActive() API to differentiate leaders/mirrors.
  (`#2028 <https://github.com/vertexproject/synapse/pull/2028>`_)

- Add pop() method to Storm list objects.
  (`#2027 <https://github.com/vertexproject/synapse/pull/2027>`_)

Bugfixes
--------

- Fix bug in dry-run output of new merge command.
  (`#2026 <https://github.com/vertexproject/synapse/pull/2026>`_)

v2.18.1 - 2020-12-24
====================

Bugfixes
--------

- Make syncIndexEvents testing more resiliant
- Make syncIndexEvents yield more often when filtering results
  (`#2025 <https://github.com/vertexproject/synapse/pull/2025>`_)

- Update push/pull tests to use new waittask() API
- Raise clear errors in ambiguous use of node.tagglobs() API
- Update model docs and examples for geo:latitude and geo:longitude
- Support deref form names in storm node add expressions
  (`#2024 <https://github.com/vertexproject/synapse/pull/2024>`_)

- Update tests to normalize equality comparison values
  (`#2023 <https://github.com/vertexproject/synapse/pull/2023>`_)

v2.18.0 - 2020-12-23
====================

Features and Enhancements
-------------------------

- Added axon.size() API and storm plumbing
  (`#2020 <https://github.com/vertexproject/synapse/pull/2020>`_)

Bugfixes
--------

- Fix active coro issue uncovered with cluster testing
  (`#2021 <https://github.com/vertexproject/synapse/pull/2021>`_)

v2.17.1 - 2020-12-22
====================

Features and Enhancements
-------------------------

- Added (BETA) RST pre-processor to embed Storm output into RST docs.
  (`#1988 <https://github.com/vertexproject/synapse/pull/1988>`_)

- Added a ``merge`` command to allow per-node Layer merge operations to
  be done.
  (`#2009 <https://github.com/vertexproject/synapse/pull/2009>`_)

- Updated storm package format to include a semver version string.
  (`#2016 <https://github.com/vertexproject/synapse/pull/2016>`_)

- Added telepath proxy getPipeline API to minimize round-trip delay.
  (`#1615 <https://github.com/vertexproject/synapse/pull/1615>`_)

- Added Node properties iteration and setitem APIs to storm.
  (`#2011 <https://github.com/vertexproject/synapse/pull/2011>`_)


Bugfixes
--------

- Fixes for active coro API and internal layer API name fixes.
  (`#2018 <https://github.com/vertexproject/synapse/pull/2018>`_)

- Allow :prop -+> * join syntax.
  (`#2015 <https://github.com/vertexproject/synapse/pull/2015>`_)

- Make getFormCount() API return a primitive dictionary.
  (`#2014 <https://github.com/vertexproject/synapse/pull/2014>`_)

- Make StormVarListError messages more user friendly.
  (`#2013 <https://github.com/vertexproject/synapse/pull/2013>`_)

v2.17.0 - 2020-12-22
====================

``2.17.0`` was not published due to CI issues.


v2.16.1 - 2020-12-17
====================

Features and Enhancements
-------------------------
- Allow the ``matchdef`` used in the ``Layer.syncIndexEvents()`` API
  to match on tagprop data.
  (`#2010 <https://github.com/vertexproject/synapse/pull/2010>`_)

Bugfixes
--------
- Properly detect and raise a client side exception in Telepath generators
  when the underlying Link has been closed.
  (`#2008 <https://github.com/vertexproject/synapse/pull/2008>`_)
- Refactor the Layer push/push test to not reach through the Layer API
  boundary.
  (`#2012 <https://github.com/vertexproject/synapse/pull/2012>`_)

Improved Documentation
----------------------
- Add documentation for Storm raw pivot syntax.
  (`#2007 <https://github.com/vertexproject/synapse/pull/2007>`_)
- Add documentation for recently added Storm commands.
  (`#2007 <https://github.com/vertexproject/synapse/pull/2007>`_)
- General cleanup and clarifications.
  (`#2007 <https://github.com/vertexproject/synapse/pull/2007>`_)


v2.16.0 - 2020-12-15
====================

Features and Enhancements
-------------------------
- Replaced the View sync APIs introduced in ``v2.14.0`` with Layer specific
  sync APIs.
  (`#2003 <https://github.com/vertexproject/synapse/pull/2003>`_)
- Add ``$lib.regex.matches()`` and ``$lib.regex.search()`` Stormtypes APIs for
  performing regular expression operations against text in Storm.
  (`#1999 <https://github.com/vertexproject/synapse/pull/1999>`_)
  (`#2005 <https://github.com/vertexproject/synapse/pull/2005>`_)
- Add ``synapse.tools.genpkg`` for generating Storm packages and loading them
  into a Cortex.
  (`#2004 <https://github.com/vertexproject/synapse/pull/2004>`_)
- Refactored the StormDmon implementation to use a single async task and allow
  the Dmons to be restarted via ``$lib.dmon.bump(iden)``. This replaces the
  outer task / inner task paradigm that was previously present. Also add the
  ability to persistently disable and enable a StomDmon.
  (`#1998 <https://github.com/vertexproject/synapse/pull/1998>`_)
- Added ``aha://`` support to the ``synapse.tools.pushfile`` and
  ``synapse.tools.pullfile`` tools.
  (`#2006 <https://github.com/vertexproject/synapse/pull/2006>`_)

Bugfixes
--------
- Properly handle whitespace in keyword arguments when calling functions in
  Storm.
  (`#1997 <https://github.com/vertexproject/synapse/pull/1997>`_)
- Fix some garbage collection issues causing periodic pauses in a Cortex due
  to failing to close some generators used in the Storm Command AST node.
  (`#2001 <https://github.com/vertexproject/synapse/pull/2001>`_)
  (`#2002 <https://github.com/vertexproject/synapse/pull/2002>`_)
- Fix scope based permission checks in Storm.
  (`#2000 <https://github.com/vertexproject/synapse/pull/2000>`_)


v2.15.0 - 2020-12-11
====================

Features and Enhancements
-------------------------
- Add two new Cortex APIs: ``syncIndexEvents`` and ``syncLayerEvents`` useful
  for external indexing.
  (`#1948 <https://github.com/vertexproject/synapse/pull/1948>`_)
  (`#1996 <https://github.com/vertexproject/synapse/pull/1996>`_)
- LMDB Slab improvements: Allow dupfixed dbs, add ``firstkey`` method, inline
  ``_ispo2``, add HotCount deletion.
  (`#1948 <https://github.com/vertexproject/synapse/pull/1948>`_)
- Add method to merge sort sorted async generators.
  (`#1948 <https://github.com/vertexproject/synapse/pull/1948>`_)

Bugfixes
--------
- Ensure parent FQDN exists even in out-of-order node edit playback.
  (`#1995 <https://github.com/vertexproject/synapse/pull/1995>`_)


v2.14.2 - 2020-12-10
====================

Bugfixes
--------
- Fix an issue with the new layer push / pull code.
  (`#1994 <https://github.com/vertexproject/synapse/pull/1994>`_)
- Fix an issue with the url sanitization function when the path contains
  an ``@`` character.
  (`#1993 <https://github.com/vertexproject/synapse/pull/1993>`_)


v2.14.1 - 2020-12-09
====================

Features and Enhancements
-------------------------
- Add a ``/api/v1/active`` HTTPAPI to the Cell that can be used as an
  unauthenticated liveliness check.
  (`#1987 <https://github.com/vertexproject/synapse/pull/1987>`_)
- Add ``$lib.pip.gen()`` Stormtypes API for ephemeral queues and bulk data
  access in Storm.
  (`#1986 <https://github.com/vertexproject/synapse/pull/1986>`_)
- Add a ``$lib.model.tagprop()`` Stormtypes API for retrieving Tagprop
  definitions.
  (`#1990 <https://github.com/vertexproject/synapse/pull/1990>`_)
- Add efficient View and Layer push/pull configurations.
  (`#1991 <https://github.com/vertexproject/synapse/pull/1991>`_)
  (`#1992 <https://github.com/vertexproject/synapse/pull/1992>`_)
- Add ``getAhaUrls()`` to the Aha service to prepare for additional
  service discovery.
  (`#1989 <https://github.com/vertexproject/synapse/pull/1989>`_)
- Add a ``/api/v1/auth/onepass/issue`` HTTPAPI for an admin to mint a
  one-time password for a Cell user.
  (`#1982 <https://github.com/vertexproject/synapse/pull/1982>`_)

Bugfixes
--------
- Make ``aha://`` urls honor local paths.
  (`#1985 <https://github.com/vertexproject/synapse/pull/1985>`_)


v2.14.0 - 2020-12-09
====================

``2.14.0`` was not published due to CI issues.


v2.13.0 - 2020-12-04
====================

Features and Enhancements
-------------------------
- Add ``$lib.pkg.get()`` StormTypes function to get the Storm Package
  definition for a given package by name.
  (`#1983 <https://github.com/vertexproject/synapse/pull/1983>`_)

Bugfixes
--------
- The user account provisioned by the ``aha:admin`` could be locked out.
  Now, upon startup, if they have been locked out or had their admin status
  removed, they are unlocked and admin is reset.
  (`#1984 <https://github.com/vertexproject/synapse/pull/1984>`_)


v2.12.3 - 2020-12-03
====================

Bugfixes
--------
- Prevent OverflowError exceptions which could have resulted from lift
  operations with integer storage types.
  (`#1980 <https://github.com/vertexproject/synapse/pull/1980>`_)
- Remove ``inet:ipv4`` norm routine wrap-around behavior for integers which
  are outside the normal bounds of IPv4 addresses.
  (`#1979 <https://github.com/vertexproject/synapse/pull/1979>`_)
- Fix ``view.add`` and fork related permissions.
  (`#1981 <https://github.com/vertexproject/synapse/pull/1981>`_)
- Read ``telepath.yaml`` when using the ``synapse.tools.cellauth`` tool.
  (`#1981 <https://github.com/vertexproject/synapse/pull/1981>`_)


v2.12.2 - 2020-12-01
====================

This release also includes the changes from v2.12.1, which was not released
due to an issue with CI pipelines.

Bugfixes
--------
- Add the missing API ``getPathObjs`` on the JsonStorCell.
  (`#1976 <https://github.com/vertexproject/synapse/pull/1976>`_)
- Fix the HasRelPropCond AST node support for Storm pivprop operations.
  (`#1972 <https://github.com/vertexproject/synapse/pull/1972>`_)
- Fix support for the ``aha:registry`` config parameter in a Cell to support
  an array of strings.
  (`#1975 <https://github.com/vertexproject/synapse/pull/1975>`_)
- Split the ``Cortex.addForm()`` Nexus handler into two parts to allow for
  safe event replay.
  (`#1978 <https://github.com/vertexproject/synapse/pull/1978>`_)
- Stop forking a large number of child layers in a View persistence test.
  (`#1977 <https://github.com/vertexproject/synapse/pull/1977>`_)


v2.12.1 - 2020-12-01
====================

Bugfixes
--------
- Add the missing API ``getPathObjs`` on the JsonStorCell.
  (`#1976 <https://github.com/vertexproject/synapse/pull/1976>`_)
- Fix the HasRelPropCond AST node support for Storm pivprop operations.
  (`#1972 <https://github.com/vertexproject/synapse/pull/1972>`_)
- Fix support for the ``aha:registry`` config parameter in a Cell to support
  an array of strings.
  (`#1975 <https://github.com/vertexproject/synapse/pull/1975>`_)


v2.12.0 - 2020-11-30
====================

Features and Enhancements
-------------------------
- Add a ``onload`` paramter to the ``stormpkg`` definition. This represents
  a Storm query which is executed every time the ``stormpkg`` is loaded in
  a Cortex.
  (`#1971 <https://github.com/vertexproject/synapse/pull/1971>`_)
  (`#1974 <https://github.com/vertexproject/synapse/pull/1974>`_)
- Add the ability, in Storm, to unset variables, remove items from
  dictionaries, and remove items from lists. This is done via assigning
  ``$lib.undef`` to the value to be removed.
  (`#1970 <https://github.com/vertexproject/synapse/pull/1970>`_)
- Add support for SOCKS proxy support for outgoing connections from an Axon
  and Cortex, using the ``'http:proxy`` configuration option. This
  configuration value must be a valid string for the
  ``aiohttp_socks.ProxyConnector.from_url()`` API. The SOCKS proxy is used by
  the Axon when downloading files; and by the Cortex when making HTTP
  connections inside of Storm.
  (`#1968 <https://github.com/vertexproject/synapse/pull/1968>`_)
- Add ``aha:admin`` to the Cell configuration to provide a common name that
  is used to create an admin user for remote access to the Cell via the
  Aha service.
  (`#1969 <https://github.com/vertexproject/synapse/pull/1969>`_)
- Add ``auth:ctor`` and ``auth:conf`` config to the Cell in order to allow
  hooking the construction of the ``HiveAuth`` object.
  (`#1969 <https://github.com/vertexproject/synapse/pull/1969>`_)


v2.11.0 - 2020-11-25
====================

Features and Enhancements
-------------------------
- Optimize Storm lift and filter queries, so that more efficient lift
  operations may be performed in some cases.
  (`#1966 <https://github.com/vertexproject/synapse/pull/1966>`_)
- Add a ``Axon.wget()`` API to allow the Axon to retrieve files directly
  from a URL.
  (`#1965 <https://github.com/vertexproject/synapse/pull/1965>`_)
- Add a JsonStor Cell, which allows for hierarchical storage and retrieval
  of JSON documents.
  (`#1954 <https://github.com/vertexproject/synapse/pull/1954>`_)
- Add a Cortex HTTP API, ``/api/v1/storm/call``. This behaves like the
  ``CoreApi.callStorm()`` API.
  (`#1967 <https://github.com/vertexproject/synapse/pull/1967>`_)
- Add ``:client:host`` and ``:server:host`` secondary properties to the
  ``inet:http:request`` form.
  (`#1955 <https://github.com/vertexproject/synapse/pull/1955>`_)
- Add ``:host`` and ``:acct`` secondary properties to the
  ``inet:search:query`` form.
  (`#1955 <https://github.com/vertexproject/synapse/pull/1955>`_)
- Add a Telepath service discovery implementation, the Aha cell. The Aha
  APIs are currently provisional and subject to change.
  (`#1954 <https://github.com/vertexproject/synapse/pull/1954>`_)


v2.10.2 - 2020-11-20
====================

Features and Enhancements
-------------------------
- The Storm ``cron.at`` command now supports a ``--now`` flag to create a
  cron job which immediately executes.
  (`#1963 <https://github.com/vertexproject/synapse/pull/1963>`_)

Bugfixes
--------
- Fix a cleanup race that caused occasional ``test_lmdbslab_base`` failures.
  (`#1962 <https://github.com/vertexproject/synapse/pull/1962>`_)
- Fix an issue with ``EDIT_NODEDATA_SET`` nodeedits missing the ``oldv``
  value.
  (`#1961 <https://github.com/vertexproject/synapse/pull/1961>`_)
- Fix an issue where ``cron.cleanup`` could have prematurely deleted some cron
  jobs.
  (`#1963 <https://github.com/vertexproject/synapse/pull/1963>`_)


v2.10.1 - 2020-11-17
====================

Bugfixes
--------
- Fix a CI issue which prevented the Python ``sdist`` package from being
  uploaded to PyPi.
  (`#1960 <https://github.com/vertexproject/synapse/pull/1960>`_)


v2.10.0 - 2020-11-17
====================

Announcements
-------------

The ``v2.10.0`` Synapse release contains support for Python 3.8. Docker images
are now built using a Python 3.8 image by default. There are also Python 3.7
images available as ``vertexproject/synapse:master-py37`` and
``vertexproject/synapse:v2.x.x-py37``.


Features and Enhancements
-------------------------
- Python 3.8 release support for Docker and PyPi.
  (`#1921 <https://github.com/vertexproject/synapse/pull/1921>`_)
  (`#1956 <https://github.com/vertexproject/synapse/pull/1956>`_)
- Add support for adding extended forms to the Cortex. This allows users to
  define their own forms using the existing types which are available in the
  Synapse data model.
  (`#1944 <https://github.com/vertexproject/synapse/pull/1944>`_)
- The Storm ``and`` and ``or`` statements now short-circuit and will return
  when their logical condition is first met. This means that subsequent
  clauses in those statements may not be executed.
  (`#1952 <https://github.com/vertexproject/synapse/pull/1952>`_)
- Add a mechanism for Storm Services to specify commands which may require
  privilege elevation to execute. An example of this may be to allow a command
  to create nodes; without managning individual permissions on what nodes a
  user may normally be allowed to create. Services using this mechanism wiill
  use the ``storm.asroot.cmd.<<cmd name>>`` hierarchy to grant this permission.
  (`#1953 <https://github.com/vertexproject/synapse/pull/1953>`_)
  (`#1958 <https://github.com/vertexproject/synapse/pull/1958>`_)
- Add ``$lib.json`` Stormtypes Library to convert between string data and
  primitives.
  (`#1949 <https://github.com/vertexproject/synapse/pull/1949>`_)
- Add a ``parallel`` command to allow for executing a portion of a Storm
  query in parallel. Add a ``background`` command to execute a Storm query
  as a detached task from the current query, capturing variables in the
  process.
  (`#1931 <https://github.com/vertexproject/synapse/pull/1931>`_)
  (`#1957 <https://github.com/vertexproject/synapse/pull/1957>`_)
- Add a ``$lib.exit()`` function to StormTypes to allow for quickly
  exiting a Storm query.
  (`#1931 <https://github.com/vertexproject/synapse/pull/1931>`_)
- Add ``$lib.bytes.upload()`` to Stormtypes for streaming bytes into the
  Axon that the Cortex is configured with.
  (`#1945 <https://github.com/vertexproject/synapse/pull/1945>`_)
- Add Storm commands to manage locking and unlocking deprecated model
  properties.
  (`#1909 <https://github.com/vertexproject/synapse/pull/1909>`_)
- Add ``cron.cleanup`` command to make it easy to clean up completed cron
  jobs.
  (`#1942 <https://github.com/vertexproject/synapse/pull/1942>`_)
- Add date of death properties and consistently named photo secondary
  properties.
  (`#1929 <https://github.com/vertexproject/synapse/pull/1929>`_)
- Add model additions for representing education and awards.
  (`#1930 <https://github.com/vertexproject/synapse/pull/1930>`_)
- Add additional account linkages to the ``inet`` model for users and groups.
  (`#1946 <https://github.com/vertexproject/synapse/pull/1946>`_)
- Add ``inet:web:hashtag`` as its own form, and add ``:hashtags`` to
  ``inet:web:post``.
  (`#1946 <https://github.com/vertexproject/synapse/pull/1946>`_)
- Add ``lang:translation`` to capture language translations of texts in a more
  comprehensive way than older ``lang`` model forms did. The ``lang:idiom``
  and ``lang:trans`` forms have been marked as deprecated.
  (`#1946 <https://github.com/vertexproject/synapse/pull/1946>`_)
- Update the ``ou`` model to add ``ou:attendee`` and ``ou:contest`` and
  ``ou:contest:result`` forms. Several secondary properties related to
  conference attendance have been marked deprecated.
  (`#1946 <https://github.com/vertexproject/synapse/pull/1946>`_)
- The ``ps:persona`` and ``ps:persona:has`` forms have been marked as
  deprecated.
  (`#1946 <https://github.com/vertexproject/synapse/pull/1946>`_)
- Add ``ps:contactlist`` to allow collecting multiple ``ps:contact`` nodes
  together.
  (`#1935 <https://github.com/vertexproject/synapse/pull/1935>`_)
- Allow the Storm Service cmdargs to accept any valid model type in the
  ``type`` value.
  (`#1923 <https://github.com/vertexproject/synapse/pull/1923>`_)
  (`#1936 <https://github.com/vertexproject/synapse/pull/1936>`_)
- Add ``>``, ``<``, ``>=`` and ``<=`` comparators for ``inet:ipv4`` type.
  (`#1938 <https://github.com/vertexproject/synapse/pull/1938>`_)
- Add configuration options to the Axon to limit the amount of data which
  can be stored in it. Add a configuration option the Cortex to limit
  the number of nodes which may be stored in a given Cortex.
  (`#1950 <https://github.com/vertexproject/synapse/pull/1950>`_)

Bugfixes
--------
- Fix a potential incorrect length for Spooled sets during fallback.
  (`#1937 <https://github.com/vertexproject/synapse/pull/1937>`_)
- Fix an issue with the Telepath ``Client`` object caching their ``Method``
  and ``GenrMethod`` attributes across re-connections of the underlying
  ``Proxy`` objects.
  (`#1939 <https://github.com/vertexproject/synapse/pull/1939>`_)
  (`#1941 <https://github.com/vertexproject/synapse/pull/1941>`_)
- Fix a bug where a temporary spool slab cleanup failed to remove all
  files from the filesystem that were created when the slab was made.
  (`#1940 <https://github.com/vertexproject/synapse/pull/1940>`_)
- Move exceptions which do not subclass ``SynErr`` out of ``synapse/exc.py``.
  (`#1947 <https://github.com/vertexproject/synapse/pull/1947>`_)
  (`#1951 <https://github.com/vertexproject/synapse/pull/1951>`_)


v2.9.2 - 2020-10-27
===================

Bugfixes
--------
- Fix an issue where a Cortex migrated from a `01x` release could
  overwrite entries in a Layer's historical nodeedit log.
  (`#1934 <https://github.com/vertexproject/synapse/pull/1934>`_)
- Fix an issue with the layer definition schema.
  (`#1927 <https://github.com/vertexproject/synapse/pull/1927>`_)


v2.9.1 - 2020-10-22
===================

Features and Enhancements
-------------------------
- Reuse existing an existing ``DateTime`` object when making time strings.
  This gives a slight performance boost for the ``synapse.lib.time.repr()``
  function.
  (`#1919 <https://github.com/vertexproject/synapse/pull/1919>`_)
- Remove deprecated use of ``loop`` arguments when calling ``asyncio``
  primitives.
  (`#1920 <https://github.com/vertexproject/synapse/pull/1920>`_)
- Allow Storm Services to define a minimum required Synapse version by the
  Cortex. If the Cortex is not running the minimum version, the Cortex will
  not load
  (`#1900 <https://github.com/vertexproject/synapse/pull/1900>`_)
- Only get the nxsindx in the ``Layer.storeNodeEdits()`` function if logging
  edits.
  (`#1926 <https://github.com/vertexproject/synapse/pull/1926>`_)
- Include the Node iden value in the ``CantDelNode`` exception when
  attempting to delete a Node failes due to existing references to the node.
  (`#1926 <https://github.com/vertexproject/synapse/pull/1926>`_)
- Take advantage of the LMDB append operation when possible.
  (`#1912 <https://github.com/vertexproject/synapse/pull/1912>`_)

Bugfixes
--------
- Fix an issues in the Telepath Client where an exception thrown by a onlink
  function could cause additional linkloop tasks to be spawned.
  (`#1924 <https://github.com/vertexproject/synapse/pull/1924>`_)


v2.9.0 - 2020-10-19
===================

Announcements
-------------

The ``v2.9.0`` Synapse release contains an automatic Cortex Layer data
migration. The updated layer storage format reduces disk and memory
requirements for a layer. It is recommended to test this process with a
backup of a Cortex before updating a production Cortex.

In order to maximize the space savings from the new layer storage format,
after the Cortex has been migrated to ``v2.9.0``, one can take a cold
backup of the Cortex and restore the Cortex from that backup. This
compacts the LMDB databases which back the Layers and reclaims disk space
as a result. This is an optional step; as LMDB will eventually re-use the
existing space on disk.

If there are any questions about this, please reach out in the Synapse Slack
channel so we can assist with any data migration questions.

Features and Enhancements
-------------------------
- Optimize the layer storage format for memory size and performance.
  (`#1877 <https://github.com/vertexproject/synapse/pull/1877>`_)
  (`#1885 <https://github.com/vertexproject/synapse/pull/1885>`_)
  (`#1899 <https://github.com/vertexproject/synapse/pull/1899>`_)
  (`#1917 <https://github.com/vertexproject/synapse/pull/1917>`_)
- Initial support Python 3.8 compatibility for the core Synapse library.
  Additional 3.8 support (such as wheels and Docker images) will be available
  in future releases.
  (`#1907 <https://github.com/vertexproject/synapse/pull/1907>`_)
- Add a read only Storm option to the Storm runtime. This option prevents
  executing commands or Stormtypes functions which may modify data in the
  Cortex.
  (`#1869 <https://github.com/vertexproject/synapse/pull/1869>`_)
  (`#1916 <https://github.com/vertexproject/synapse/pull/1916>`_)
- Allow the Telepath Dmon to disconnect clients using a ready status.
  (`#1881 <https://github.com/vertexproject/synapse/pull/1881>`_)
- Ensure that there is only one online backup of a Cell occurring at a time.
  (`#1883 <https://github.com/vertexproject/synapse/pull/1883>`_)
- Added ``.lower()``, ``.strip()``, ``.lstrip()`` and ``.rstrip()`` methods
  to the Stormtypes Str object. These behave like the Python ``str`` methods.
  (`#1886 <https://github.com/vertexproject/synapse/pull/1886>`_)
  (`#1906 <https://github.com/vertexproject/synapse/pull/1906>`_)
- When scraping text, defanged indicators are now refanged by default.
  (`#1888 <https://github.com/vertexproject/synapse/pull/1888>`_)
- Normalize read-only property declarations to use booleans in the data model.
  (`#1887 <https://github.com/vertexproject/synapse/pull/1887>`_)
- Add ``lift.byverb`` command to allow lifting nodes using a light edge verb.
  (`#1890 <https://github.com/vertexproject/synapse/pull/1890>`_)
- Add netblock and range lift helpers for ``inet:ipv6`` type, similar to the
  helpers for ``inet:ipv4``.
  (`#1869 <https://github.com/vertexproject/synapse/pull/1869>`_)
- Add a ``edges.del`` command to bulk remove light weight edges from nodes.
  (`#1893 <https://github.com/vertexproject/synapse/pull/1893>`_)
- The ``yield`` keyword in Storm now supports iterating over Stormtypes List
  and Set objects.
  (`#1898 <https://github.com/vertexproject/synapse/pull/1898>`_)
- Add ``ou:contract``, ``ou:industry`` and ``it:reveng:function:strings``
  forms to the data model.
  (`#1894 <https://github.com/vertexproject/synapse/pull/1894>`_)
- Add some display type-hinting to the data model for some string fields which
  may be multi-line fields.
  (`#1892 <https://github.com/vertexproject/synapse/pull/1892>`_)
- Add ``getFormCounts()`` API to the Stormtypes View and Layer objects.
  (`#1903 <https://github.com/vertexproject/synapse/pull/1903>`_)
- Allow Cortex layers to report their total size on disk. This is exposed in
  the Stormtypes ``Layer.pack()`` method for a layer.
  (`#1910 <https://github.com/vertexproject/synapse/pull/1910>`_)
- Expose the remote Storm Service name in the ``$lib.service.get()``
  Stormtypes API. This allows getting a service object without knowing
  the name of the service as it was locally added to a Cortex. Also add
  a ``$lib.service.has()`` API which allows checking to see if a service
  is available on a Cortex.
  (`#1908 <https://github.com/vertexproject/synapse/pull/1908>`_)
  (`#1915 <https://github.com/vertexproject/synapse/pull/1915>`_)
- Add regular expression (``~=``) and prefix matching (``^=``) expression
  comparators that can be used with logical expressions inside of Storm.
  (`#1906 <https://github.com/vertexproject/synapse/pull/1906>`_)
- Promote ``CoreApi.addFeedData()`` calls to tracked tasks which can be
  viewed and terminated.
  (`#1918 <https://github.com/vertexproject/synapse/pull/1918>`_)

Bugfixes
--------
- Fixed a Storm bug where attempting to access an undeclared variable
  silently fails. This will now raise a ``NoSuchVar`` exception. This
  is verified at runtime, not at syntax evaluation.
  (`#1916 <https://github.com/vertexproject/synapse/pull/1916>`_)
- Ensure that Storm HTTP APIs tear down the runtime task if the remote
  disconnects before consuming all of the messages.
  (`#1889 <https://github.com/vertexproject/synapse/pull/1889>`_)
- Fix an issue where the ``model.edge.list`` command could block the ioloop
  for large Cortex.
  (`#1890 <https://github.com/vertexproject/synapse/pull/1890>`_)
- Fix a regex based lifting bug.
  (`#1899 <https://github.com/vertexproject/synapse/pull/1899>`_)
- Fix a few possibly greedy points in the AST code which could have resulted
  in greedy CPU use.
  (`#1902 <https://github.com/vertexproject/synapse/pull/1902>`_)
- When pivoting across light edges, if the destination form was not a valid
  form, nothing happened. Now a StormRuntimeError is raised if the
  destination form is not valid.
  (`#1905 <https://github.com/vertexproject/synapse/pull/1905>`_)
- Fix an issue with spawn processes accessing lmdb databases after a slab
  resize event has occurred by the main process.
  (`#1914 <https://github.com/vertexproject/synapse/pull/1914>`_)
- Fix a slab teardown race seen in testing Python 3.8 on MacOS.
  (`#1914 <https://github.com/vertexproject/synapse/pull/1914>`_)

Deprecations
------------
- The ``0.1.x`` to ``2.x.x`` Migration tool and associated Cortex sync
  service has been removed from Synapse in the ``2.9.0`` release.

Improved Documentation
----------------------
- Clarify user documentation for pivot out and pivot in operations.
  (`#1891 <https://github.com/vertexproject/synapse/pull/1891>`_)
- Add a deprecation policy for Synapse Data model elements.
  (`#1895 <https://github.com/vertexproject/synapse/pull/1895>`_)
- Pretty print large data structures that may occur in the data model
  documentation.
  (`#1897 <https://github.com/vertexproject/synapse/pull/1897>`_)
- Update Storm Lift documentation to add the ``?=`` operator.
  (`#1904 <https://github.com/vertexproject/synapse/pull/1904>`_)


v2.8.0 - 2020-09-22
===================

Features and Enhancements
-------------------------
- Module updates to support generic organization identifiers, generic
  advertising identifiers, asnet6 and a few other secondary property additions.
  (`#1879 <https://github.com/vertexproject/synapse/pull/1879>`_)
- Update the Cell backup APIs to perform a consistent backup across all slabs
  for a Cell.
  (`#1873 <https://github.com/vertexproject/synapse/pull/1873>`_)
- Add support for a environment variable, ``SYN_LOCKMEM_DISABLE`` which will
  disable any memory locking of LMDB slabs.
  (`#1882 <https://github.com/vertexproject/synapse/pull/1882>`_)

Deprecations
------------

- The ``0.1.x`` to ``2.x.x`` Migration tool and and associated Cortex sync
  service will be removed from Synapse in the ``2.9.0`` release. In order to
  move forward to ``2.9.0``, please make sure that any Cortexes which still
  need to be migrated will first be migrated to ``2.8.x`` prior to attempting
  to use ``2.9.x``.

Improved Documentation
----------------------
- Add Synapse README content to the Pypi page. This was a community
  contribution from https://github.com/wesinator.  (`#1872
  <https://github.com/vertexproject/synapse/pull/1872>`_)


v2.7.3 - 2020-09-16
===================

Deprecations
------------
- The ``0.1.x`` to ``2.x.x`` Migration tool and and associated Cortex sync service will be removed from Synapse in
  the ``2.9.0`` release. In order to move forward to ``2.9.0``, please make sure that any Cortexes which still need to
  be migrated will first be migrated to ``2.8.x`` prior to attempting to use ``2.9.x``.
  (`#1880 <https://github.com/vertexproject/synapse/pull/1880>`_)

Bugfixes
--------
- Remove duplicate words in a comment. This was a community contribution from enadjoe.
  (`#1874 <https://github.com/vertexproject/synapse/pull/1874>`_)
- Fix a nested Nexus log event in Storm Service deletion. The ``del`` event causing Storm code execution could lead to
  nested Nexus events, which is incongruent with how Nexus change handlers work. This now spins off the Storm code in
  a free-running coroutine. This does change the service ``del`` semantics since any support Storm packages a service
  had may be removed by the time the handler executes.
  (`#1876 <https://github.com/vertexproject/synapse/pull/1876>`_)
- Fix an issue where the ``cull`` parameter was not being passed to the multiqueue properly when calling ``.gets()``
  on a Storm Types Queue object.
  (`#1876 <https://github.com/vertexproject/synapse/pull/1876>`_)
- Pin the ``nbconvert`` package to a known working version, as ``v6.0.0`` of that package broke the Synapse document
  generation by changing how templates work.
  (`#1876 <https://github.com/vertexproject/synapse/pull/1876>`_)
- Correct ``min`` and ``max`` integer examples in tagprop documentation and tests.
  (`#1878 <https://github.com/vertexproject/synapse/pull/1878>`_)


v2.7.2 - 2020-09-04
===================

Features and Enhancements
-------------------------
- Update tests for additional test code coverage. This was a community contribution from blackout.
  (`#1867 <https://github.com/vertexproject/synapse/pull/1867>`_)
- Add implicit links to documentation generated for Storm services, to allow for direct linking inside of documentation
  to specific Storm commands.
  (`#1866 <https://github.com/vertexproject/synapse/pull/1866>`_)
- Add future support for deprecating model elements in the Synapse data model. This support will produce client and
  server side warnings when deprecated model elements are used or loaded by custom model extensions or CoreModules.
  (`#1863 <https://github.com/vertexproject/synapse/pull/1863>`_)

Bugfixes
--------
- Update ``FixedCache.put()`` to avoid a cache miss. This was a community contribution from blackout.
  (`#1868 <https://github.com/vertexproject/synapse/pull/1868>`_)
- Fix the ioloop construction to be aware of ``SYN_GREEDY_CORO`` environment variable to put the ioloop into debug mode
  and log long-running coroutines.
  (`#1870 <https://github.com/vertexproject/synapse/pull/1870>`_)
- Fix how service permissions are checked in ``$lib.service.get()`` and ``$lib.service.wait()`` Storm library calls.
  These APIs now first check ``service.get.<service iden>`` before checking ``service.get.<service name>`` permissions.
  A successful ``service.get.<service name>`` check will result in a warning to the client and the server.
  (`#1871 <https://github.com/vertexproject/synapse/pull/1871>`_)


v2.7.1 - 2020-08-26
===================

Features and Enhancements
-------------------------
- Refactor an Axon unit test to make it easier to test alternative Axon implementations.
  (`#1862 <https://github.com/vertexproject/synapse/pull/1862>`_)

Bugfixes
--------
- Fix an issue in ``synapse.tools.cmdr`` where it did not ensure that the users Synapse directory was created before
  trying to open files in the directory.
  (`#1860 <https://github.com/vertexproject/synapse/issues/1860>`_)
  (`#1861 <https://github.com/vertexproject/synapse/pull/1861>`_)

Improved Documentation
----------------------
- Fix an incorrect statement in our documentation about the intrinsic Axon that a Cortex creates being remotely
  accessible.
  (`#1862 <https://github.com/vertexproject/synapse/pull/1862>`_)


v2.7.0 - 2020-08-21
===================

Features and Enhancements
-------------------------
- Add Telepath and HTTP API support to set and remove global Storm variables.
  (`#1846 <https://github.com/vertexproject/synapse/pull/1846>`_)
- Add Cell level APIs for performing the backup of a Cell. These APIs are exposed inside of a Cortex via a Storm Library.
  (`#1844 <https://github.com/vertexproject/synapse/pull/1844>`_)
- Add support for Cron name and doc fields to be editable.
  (`#1848 <https://github.com/vertexproject/synapse/pull/1848>`_)
- Add support for Runtime-only (``runt``) nodes in the PivotOut operation (``-> *``).
  (`#1851 <https://github.com/vertexproject/synapse/pull/1851>`_)
- Add ``:nicks`` and ``:names`` secondary properties to ``ps:person`` and ``ps:persona`` types.
  (`#1852 <https://github.com/vertexproject/synapse/pull/1852>`_)
- Add a new ``ou:position`` form and a few associated secondary properties.
  (`#1849 <https://github.com/vertexproject/synapse/pull/1849>`_)
- Add a step to the CI build process to smoke test the sdist and wheel packages before publishing them to PyPI.
  (`#1853 <https://github.com/vertexproject/synapse/pull/1853>`_)
- Add support for representing ``nodedata`` in the command hinting for Storm command implementations and expose it on
  the ``syn:cmd`` runt nodes.
  (`#1850 <https://github.com/vertexproject/synapse/pull/1850>`_)
- Add package level configuration data to Storm Packages in the ``modconf`` value of a package definition. This is added
  to the runtime variables when a Storm package is imported, and includes the ``svciden`` for packages which come from
  Storm Services.
  (`#1855 <https://github.com/vertexproject/synapse/pull/1855>`_)
- Add support for passing HTTP params when using ``$lib.inet.http.*`` functions to make HTTP calls in Storm.
  (`#1856 <https://github.com/vertexproject/synapse/pull/1856>`_)
- Log Storm queries made via the ``callStorm()`` and ``count()`` APIs.
  (`#1857 <https://github.com/vertexproject/synapse/pull/1857>`_)

Bugfixes
--------
- Fix an issue were some Storm filter operations were not yielding CPU time appropriately.
  (`#1845 <https://github.com/vertexproject/synapse/pull/1845>`_)

Improved Documentation
----------------------
- Remove a reference to deprecated ``eval()`` API from quickstart documentation.
  (`#1858 <https://github.com/vertexproject/synapse/pull/1858>`_)


v2.6.0 - 2020-08-13
===================

Features and Enhancements
-------------------------

- Support ``+hh:mm`` and ``+hh:mm`` timezone offset parsing when normalizing ``time`` values.
  (`#1833 <https://github.com/vertexproject/synapse/pull/1833>`_)
- Enable making mirrors of Cortex mirrors work.
  (`#1836 <https://github.com/vertexproject/synapse/pull/1836>`_)
- Remove read-only properties from ``inet:flow`` and ``inet:http:request`` forms.
  (`#1840 <https://github.com/vertexproject/synapse/pull/1840>`_)
- Add support for setting nodedata and light edges in the ``syn.nodes`` ingest format.
  (`#1839 <https://github.com/vertexproject/synapse/pull/1839>`_)
- Sync the LMDB Slab replay log if it gets too large instead of waiting for a force commit operation.
  (`#1838 <https://github.com/vertexproject/synapse/pull/1838>`_)
- Make the Agenda unit tests an actual component test to reduce test complexity.
  (`#1837 <https://github.com/vertexproject/synapse/pull/1837>`_)
- Support glob patterns when specifying files to upload to an Axon with ``synapse.tools.pushfile``.
  (`#1837 <https://github.com/vertexproject/synapse/pull/1837>`_)
- Use the node edit metadata to store and set the ``.created`` property on nodes, so that mirrors of Cortexes have
  consistent ``.created`` timestamps.
  (`#1765 <https://github.com/vertexproject/synapse/pull/1765>`_)
- Support parent runtime variables being accessed during the execution of a ``macro.exec`` command.
  (`#1841 <https://github.com/vertexproject/synapse/pull/1841>`_)
- Setting tags from variable values in Storm now calls ``s_stormtypes.tostr()`` on the variable value.
  (`#1843 <https://github.com/vertexproject/synapse/pull/1843>`_)

Bugfixes
--------
- The Storm ``tree`` command now catches the Synapse ``RecursionLimitHit`` error and raises a ``StormRuntimeError``
  instead. The ``RecursionLimitHit`` being raised by that command was, in practice, confusing.
  (`#1832 <https://github.com/vertexproject/synapse/pull/1832>`_)
- Resolve memory leak issues related to callStorm and Base object teardowns with exceptions.
  (`#1842 <https://github.com/vertexproject/synapse/pull/1842>`_)


v2.5.1 - 2020-08-05
===================

Features and Enhancements
-------------------------

- Add performance oriented counting APIs per layer, and expose them via Stormtypes.
  (`#1813 <https://github.com/vertexproject/synapse/pull/1813>`_)
- Add the ability to clone a layer, primarily for benchmarking and testing purposes.
  (`#1819 <https://github.com/vertexproject/synapse/pull/1819>`_)
- Update the benchmark script to run on remote Cortexes.
  (`#1829 <https://github.com/vertexproject/synapse/pull/1829>`_)

Bugfixes
--------
- Sanitize passwords from Telepath URLs during specific cases where the URL may be logged.
  (`#1830 <https://github.com/vertexproject/synapse/pull/1830>`_)

Improved Documentation
----------------------

- Fix a few typos in docstrings.
  (`#1831 <https://github.com/vertexproject/synapse/pull/1831>`_)


v2.5.0 - 2020-07-30
===================

Features and Enhancements
-------------------------

- Refactor the Nexus to remove leadership awareness.
  (`#1785 <https://github.com/vertexproject/synapse/pull/1785>`_)
- Add support for client-side certificates in Telepath for SSL connections.
  (`#1785 <https://github.com/vertexproject/synapse/pull/1785>`_)
- Add multi-dir support for CertDir.
  (`#1785 <https://github.com/vertexproject/synapse/pull/1785>`_)
- Add a ``--no-edges`` option to the Storm ``graph`` command.
  (`#1805 <https://github.com/vertexproject/synapse/pull/1805>`_)
- Add ``:doc:url`` to the ``syn:tag`` form to allow recording a URL which may document a tag.
  (`#1805 <https://github.com/vertexproject/synapse/pull/1805>`_)
- Add ``CoreApi.reqValidStorm()`` and a ``/api/v1/reqvalidstorm`` Cortex HTTPAPI endpoint to validate that a given
  Storm query is valid Storm syntax.
  (`#1806 <https://github.com/vertexproject/synapse/pull/1806>`_)
- Support Unicode white space in Storm. All Python `\s` (Unicode white space + ASCII separators) is now treated as
  white space in Storm.
  (`#1812 <https://github.com/vertexproject/synapse/pull/1812>`_)
- Refactor how StormLib and StormPrim objects access their object locals, and add them to a global registry to support
  runtime introspection of those classes.
  (`#1804 <https://github.com/vertexproject/synapse/pull/1804>`_)
- Add smoke tests for the Docker containers built in CircleCI, as well as adding Docker healthchecks to the Cortex,
  Axon and Cryotank images.
  (`#1815 <https://github.com/vertexproject/synapse/pull/1815>`_)
- Initialize the names of the default view and layer in a fresh Cortex to ``default``.
  (`#1814 <https://github.com/vertexproject/synapse/pull/1814>`_)
- Add HTTPAPI endpoints for the Axon to upload, download and check for the existend of files.
  (`#1817 <https://github.com/vertexproject/synapse/pull/1817>`_)
  (`#1822 <https://github.com/vertexproject/synapse/pull/1822>`_)
  (`#1824 <https://github.com/vertexproject/synapse/pull/1824>`_)
  (`#1825 <https://github.com/vertexproject/synapse/pull/1825>`_)
- Add a ``$lib.bytes.has()`` API to check if the Axon a Cortex is configured with knows about a given sha256 value.
  (`#1822 <https://github.com/vertexproject/synapse/pull/1822>`_)
- Add initial model for prices, currences, securities and exchanges.
  (`#1820 <https://github.com/vertexproject/synapse/pull/1820>`_)
- Add a ``:author`` field to the ``it:app:yara:rule`` form.
  (`#1821 <https://github.com/vertexproject/synapse/pull/1821>`_)
- Add an experimental option to set the NexusLog as a ``map_async`` slab.
  (`#1826 <https://github.com/vertexproject/synapse/pull/1826>`_)
- Add an initial transportation model.
  (`#1816 <https://github.com/vertexproject/synapse/pull/1816>`_)
- Add the ability to dereference an item, from a list of items, in Storm via index.
  (`#1827 <https://github.com/vertexproject/synapse/pull/1827>`_)
- Add a generic ``$lib.inet.http.request()`` Stormlib function make HTTP requests with arbitrary verbs.
  (`#1828 <https://github.com/vertexproject/synapse/pull/1828>`_)

Bugfixes
--------
- Fix an issue with the Docker builds for Synapse where the package was not being installed properly.
  (`#1815 <https://github.com/vertexproject/synapse/pull/1815>`_)

Improved Documentation
----------------------

- Update documentation for deploying Cortex mirrors.
  (`#1811 <https://github.com/vertexproject/synapse/pull/1811>`_)
- Add automatically generated documentation for all the Storm ``$lib...`` functions and Storm Primitive types.
  (`#1804 <https://github.com/vertexproject/synapse/pull/1804>`_)
- Add examples of creating a given Form to the automatically generated documentation for the automatically generated
  datamodel documentation.
  (`#1818 <https://github.com/vertexproject/synapse/pull/1818>`_)
- Add additional documentation for Cortex automation.
  (`#1797 <https://github.com/vertexproject/synapse/pull/1797>`_)
- Add Devops documentation for the list of user permissions relevant to a Cell, Cortex and Axon.
  (`#1823 <https://github.com/vertexproject/synapse/pull/1823>`_)


v2.4.0 - 2020-07-15
===================

Features and Enhancements
-------------------------

- Update the Storm ``scrape`` command to make ``refs`` light edges, instead of ``edge:refs`` nodes.
  (`#1801 <https://github.com/vertexproject/synapse/pull/1801>`_)
  (`#1803 <https://github.com/vertexproject/synapse/pull/1803>`_)
- Add ``:headers`` and ``:response:headers`` secondary properties to the ``inet:http:request`` form as Array types, so
  that requests can be directly linked to headers.
  (`#1800 <https://github.com/vertexproject/synapse/pull/1800>`_)
- Add ``:headers`` secondary property to the ``inet:email:messaage`` form as Array types, so that messages can be
  directly linked to headers.
  (`#1800 <https://github.com/vertexproject/synapse/pull/1800>`_)
- Add additional model elements to support recording additional data for binary reverse engineering.
  (`#1802 <https://github.com/vertexproject/synapse/pull/1802>`_)


v2.3.1 - 2020-07-13
===================

Bugfixes
--------
- Prohibit invalid rules from being set on a User or Role object.
  (`#1798 <https://github.com/vertexproject/synapse/pull/1798>`_)


v2.3.0 - 2020-07-09
===================

Features and Enhancements
-------------------------

- Add ``ps.list`` and ``ps.kill`` commands to Storm, to allow introspecting the runtime tasks during
  (`#1782 <https://github.com/vertexproject/synapse/pull/1782>`_)
- Add an ``autoadd`` mode to Storm, which will extract basic indicators and make nodes from them when executed. This is
  a superset of the behavior in the ``lookup`` mode.
  (`#1795 <https://github.com/vertexproject/synapse/pull/1795>`_)
- Support skipping directories in the ``synapse.tools.backup`` tool.
  (`#1792 <https://github.com/vertexproject/synapse/pull/1792>`_)
- Add prefix based lifting to the Hex type.
  (`#1796 <https://github.com/vertexproject/synapse/pull/1796>`_)

Bugfixes
--------
- Fix an issue for prop pivot out syntax where the source data is an array type.
  (`#1794 <https://github.com/vertexproject/synapse/pull/1794>`_)

Improved Documentation
----------------------

- Add Synapse data model background on light edges and update the Storm data modification and pivot references for light
  edges.
  (`#1784 <https://github.com/vertexproject/synapse/pull/1784>`_)
- Add additional terms to the Synapse glossary.
  (`#1784 <https://github.com/vertexproject/synapse/pull/1784>`_)
- Add documentation for additional Storm commands.
  (`#1784 <https://github.com/vertexproject/synapse/pull/1784>`_)
- Update documentation for Array types.
  (`#1791 <https://github.com/vertexproject/synapse/pull/1791>`_)


v2.2.2 - 2020-07-03
===================

Features and Enhancements
-------------------------

- Add some small enhancements to the Cortex benchmarking script.
  (`#1790 <https://github.com/vertexproject/synapse/pull/1790>`_)

Bugfixes
--------

- Fix an error in the help for the ``macro.del`` command.
  (`#1786 <https://github.com/vertexproject/synapse/pull/1786>`_)
- Fix rule indexing for the ``synapse.tools.cellauth`` tool to correctly print the rule offsets.
  (`#1787 <https://github.com/vertexproject/synapse/pull/1787>`_)
- Remove extraneous output from the Storm Parser output.
  (`#1789 <https://github.com/vertexproject/synapse/pull/1789>`_)
- Rewrite the language (and private APIs) for the Storm ``model.edge`` related commands to remove references to extended
  properties. That was confusing language which was unclear for users.
  (`#1789 <https://github.com/vertexproject/synapse/pull/1789>`_)
- During 2.0.0 migrations, ensure that Cortex and Layer idens are unique; and make minimum 0.1.6 version requirement for
  migration.
  (`#1788 <https://github.com/vertexproject/synapse/pull/1788>`_)


v2.2.1 - 2020-06-30
===================

Bugfixes
--------

- The Axon test suite was missing a test for calling ``Axon.get()`` on a file it did not have. This is now included in
  the test suite.
  (`#1783 <https://github.com/vertexproject/synapse/pull/1783>`_)

Improved Documentation
----------------------

- Improve Synapse devops documentation hierarchy. Add note about Cell directories being persistent.
  (`#1781 <https://github.com/vertexproject/synapse/pull/1781>`_)


v2.2.0 - 2020-06-26
===================

Features and Enhancements
-------------------------

- Add a ``postAnit()`` callback to the ``synapse.lib.base.Base()`` object which is called *after* the ``__anit__()``
  call chain is completed, but before ``Base.anit()`` returns the object instance to the caller. This is used by the
  Cell to defer certain Nexus actions until the Cell has completed initializing all of its instance attributes.
  (`#1768 <https://github.com/vertexproject/synapse/pull/1768>`_)
- Make ``synapse.lib.msgpack.en()`` raise a ``SynErr.NotMsgpackSafe`` exception instead of passing through the
  exception raised by msgpack.
  (`#1768 <https://github.com/vertexproject/synapse/pull/1768>`_)

Bugfixes
--------

- Add a missing ``toprim()`` call in ``$lib.globals.set()``.
  (`#1778 <https://github.com/vertexproject/synapse/pull/1778>`_)
- Fix an issue in the quickstart documentation related to permissions. Thank you ``enadjoe`` for your contribution.
  (`#1779 <https://github.com/vertexproject/synapse/pull/1779>`_)
- Fix an Cell/Cortex startup issue which caused errors when starting up a Cortex when the last Nexus event was
  replayed. This has a secondary effect that Cell implementers cannot be making Nexus changes during the ``__anit__``
  methods.
  (`#1768 <https://github.com/vertexproject/synapse/pull/1768>`_)

Improved Documentation
----------------------

- Add a minimal Storm Service example to the developer documentation.
  (`#1776 <https://github.com/vertexproject/synapse/pull/1776>`_)
- Reorganize the Synapse User Guide into a more hierarchical format.
  (`#1777 <https://github.com/vertexproject/synapse/pull/1777>`_)
- Fill out additional glossary items.
  (`#1780 <https://github.com/vertexproject/synapse/pull/1780>`_)


v2.1.2 - 2020-06-18
===================

Bugfixes
--------

- Disallow command and bare string contensts from starting with ``//`` and ``/*`` in Storm syntax.
  (`#1769 <https://github.com/vertexproject/synapse/pull/1769>`_)


v2.1.1 - 2020-06-16
===================

Bugfixes
--------

- Fix an issue in the autodoc tool which failed to account for Storm Service commands without cmdargs.
  (`#1775 <https://github.com/vertexproject/synapse/pull/1775>`_)


v2.1.0 - 2020-06-16
===================

Features and Enhancements
-------------------------

- Add information about light edges to graph carving output.
  (`#1762 <https://github.com/vertexproject/synapse/pull/1762>`_)
- Add a ``geo:json`` type and ``geo:place:geojson`` property to the model.
  (`#1759 <https://github.com/vertexproject/synapse/pull/1759>`_)
- Add the ability to record documentation for light edges.
  (`#1760 <https://github.com/vertexproject/synapse/pull/1760>`_)
- Add the ability to delete and set items inside of a MultiQueue.
  (`#1766 <https://github.com/vertexproject/synapse/pull/1766>`_)

Improved Documentation
----------------------

- Refactor ``v2.0.0`` changelog documentation.
  (`#1763 <https://github.com/vertexproject/synapse/pull/1763>`_)
- Add Vertex branding to the Synapse documentation.
  (`#1767 <https://github.com/vertexproject/synapse/pull/1767>`_)
- Update Backups documentation in the Devops guide.
  (`#1764 <https://github.com/vertexproject/synapse/pull/1764>`_)
- Update the autodoc tool to generate documentation for Cell confdefs and StormService information.
  (`#1772 <https://github.com/vertexproject/synapse/pull/1772>`_)
- Update to separate the devops guides into distinct sections.
  (`#1772 <https://github.com/vertexproject/synapse/pull/1772>`_)
- Add documentation for how to do boot-time configuration for a Synapse Cell.
  (`#1772 <https://github.com/vertexproject/synapse/pull/1772>`_)
- Remove duplicate information about backups.
  (`#1774 <https://github.com/vertexproject/synapse/pull/1774>`_)

v2.0.0 - 2020-06-08
===================

Initial 2.0.0 release.


v0.1.X Changelog
================

For the Synapse 0.1.x changelog, see `01x Changelog`_ located in the v0.1.x documentation.

.. _01x Changelog: ../../01x/synapse/changelog.html
