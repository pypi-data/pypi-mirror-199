# [Show and Tell] Presenting `asdf-pydantic`, create ASDF tags with pydantic models.


After `pip install asdf-pydantic` you can do something like this:

<div style="width: 66vw; margin:auto;">

```py
from asdf_pydantic import AsdfPydanticModel

class Rectangle(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

    width: float
    height: float

# After creating extension and install ...

af = asdf.AsdfFile()
af["rect"] = Rectangle(width=1, height=1)
```

```yaml
#ASDF 1.0.0
#ASDF_STANDARD 1.5.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
asdf_library: !core/software-1.0.0 {
    author: The ASDF Developers,
    homepage: 'http://github.com/asdf-format/asdf',
    name: asdf,
    version: 2.14.3}
history:
  extensions:
  - !core/extension_metadata-1.0.0
    extension_class: asdf.extension.BuiltinExtension
    software: !core/software-1.0.0 {
        name: asdf,
        version: 2.14.3}
  - !core/extension_metadata-1.0.0 {
    extension_class: mypackage.shapes.ShapesExtension,
    extension_uri: 'asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0'}
rect: !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {
    height: 1.0,
    width: 1.0}
...
```
</div>

## Features

- [x] Create ASDF tag from your *pydantic* models with batteries ([converters](https://asdf.readthedocs.io/en/stable/asdf/extending/converters.html)) included.
- [x] Validates data models as you create them and not only when reading and writing ASDF files.
- [x] Preserve Python types when deserializing ASDF files.
- [x] All the cool things that comes with *pydantic* (e.g., JSON encoder, JSON schema, Pydantic types)
- [ ] <span style="color: #736f73">Genereates ASDF schemas for you.</span> (TBD, talk to me if you have ideas)

## Rationale

Defining and prototyping composite types with Python standard types: `UserDict`, `Dataclasses`, `TypeDict` are okay, but nothing beats the flexibilty of *pydantic*. With ASDF you're already in the mental space of working with either YAML and JSON hierarchical structure. This feels natural with *pydantic*.

There are big potentials beyond integrating with the Python ecosystem. For example, Tags created with *asdf-pydantic* is already readily JSON-serializable (other existing tags, like astropy, may require custom serialization) and the JSON schema comes for free.  Initial adoption of JSON schema in another language (e.g., C++, C#, Java, javascript) could be much faster than with ASDF schema — and not to forget, this is the most common schema for HTTP APIs.

---

I am looking for commmunity interest and user feedback. Alongside contributors to incubate this project if ASDF is interested.

* [GitHub repository](https://github.com/ketozhang/asdf-pydantic)
* [Documentation](https://github.com/ketozhang/asdf-pydantic)