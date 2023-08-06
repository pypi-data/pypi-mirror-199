
---
# ClassyXml

An xml file parser that makes the element text and attributes of an xml file accessible as ClassyXml class attributes.

## Install it from PyPI

```bash
pip install classyxml
```

## Usage

```xml 
<!-- example.xml -->
<data>
  <country name="Liechtenstein">
    <rank>1</rank>
    <year>2008</year>
    <gdppc>141100</gdppc>
    <neighbor name="Austria" direction="E"/>
    <neighbor name="Switzerland" direction="W"/>
  </country>
  <country name="Singapore">
    <rank>4</rank>
    <year>2011</year>
    <gdppc>59900</gdppc>
    <neighbor name="Malaysia" direction="N"/>
  </country>
  <country name="Panama">
    <rank>68</rank>
    <year>2011</year>
    <gdppc>13600</gdppc>
    <neighbor name="Costa Rica" direction="W"/>
    <neighbor name="Colombia" direction="E"/>
  </country>
</data>
```

```py
from classy_xml import ClassyXml

obj = ClassyXml('example.xml')

print(len(obj.country))                     # Output: 3

print(obj.country[0].name)                  # Output: 'Liechtenstein'
print(obj.country[0].rank.text)             # Output: '1'
print(obj.country[0].year.text)             # Output: '2008'
print(obj.country[0].gdppc.text)            # Output: '141100'
print(len(obj.country[0].neighbor))         # Output: 2
print(obj.country[0].neighbor[0].name)      # Output: 'Austria'
print(obj.country[0].neighbor[0].direction) # Output: 'E'
print(obj.country[0].neighbor[1].name)      # Output: 'Switzerland'
print(obj.country[0].neighbor[1].direction) # Output: 'W'

print(obj.country[1].name)                  # Output: 'Singapore'
print(obj.country[1].rank.text)             # Output: '4'
print(obj.country[1].year.text)             # Output: '2011'
print(obj.country[1].gdppc.text)            # Output: '59900'
print(len(obj.country[1].neighbor))         # Output: 1
print(obj.country[1].neighbor.name)         # Output: 'Malaysia'
print(obj.country[1].neighbor.direction)    # Output: 'N'

print(obj.country[2].name)                  # Output: 'Panama'
print(obj.country[2].rank.text)             # Output: '68'
print(obj.country[2].year.text)             # Output: '2011'
print(obj.country[2].gdppc.text)            # Output: '13600'
print(len(obj.country[2].neighbor))         # Output: 2
print(obj.country[2].neighbor[0].name)      # Output: 'Costa Rica'
print(obj.country[2].neighbor[0].direction) # Output: 'W'
print(obj.country[2].neighbor[1].name)      # Output: 'Colombia'
print(obj.country[2].neighbor[1].direction) # Output: 'E'
```
