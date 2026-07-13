# Simai Framework Contract Registry

Use the exact consumer pointer in
`references/vendor/framework-contract-registry.pointer.json` before choosing
utilities, components, Smart-components or assembly recipes for a new
interface.

The pointer does not vendor framework records. Resolve its exact repository
commit, path and SHA-256, then:

1. choose the closest registry recipe for the requested interface;
2. traverse its `requires` closure instead of assembling from memory;
3. suggest only records whose readiness permits the selected compatibility
   profile;
4. trace every selected record to its owner and runtime provenance;
5. validate the actual runtime and consumer against the registry before
   accepting the interface.

If a required capability is absent or blocked, record a typed upstream gap
with the real product scenario. Do not silently replace it with new
application CSS, JavaScript, a duplicate component or copied metadata.

The current pointer is a bounded developer contract. It does not claim full
framework compatibility, production readiness or readiness of every item.
Raw framework owner sources remain authoritative for implementation behavior;
the registry is the canonical public selection contract for this exact pair.
