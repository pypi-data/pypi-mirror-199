# nanoid
Simple Python library for generating NanoIDs

[Documentation](https://jameskabbes.github.io/nanoid)<br>
[PyPI](https://pypi.org/project/kabbes-nanoid)

# Installation
`pip install kabbes_nanoid`

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

## Importing
`import nanoid`

## Get a nanoid string
```python
nanoid_string = nanoid.generate()
print (nanoid_string)
```

## Generate a Nanoid object
```python
Obj = nanoid.Nanoid()
print (Obj.nanoid)
print (Obj.size)
print (Obj.alphabet)
```

## Set custom generation parameters
```python
print (nanoid.generate( size = 10, alphabet = '0123456789ABCDEF' ))
Obj = nanoid.Nanoid( size = 10, alphabet = '0123456789ABCDEF' )
print (Obj.nanoid)
```

# Author
James Kabbes

