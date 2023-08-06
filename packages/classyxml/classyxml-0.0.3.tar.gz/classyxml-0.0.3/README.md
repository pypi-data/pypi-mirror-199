
---
# ClassyXml

An xml file parser that makes the element text and attributes of an xml file accessible as ClassyXml class attributes.

## Install it from PyPI

```bash
pip install classyxml
```

## Usage

### Parsing an XML file
```xml 
<!-- countries.xml -->
<root>
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
</root>
```

```py
from classy_xml import ClassyXml, XmlElement

# Load the countries.xml file
obj = ClassyXml('countries.xml')

# Print the XML information
print(len(obj.country))                     # Output: 2

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
```

### Generating an XML file

This will generate the *countries.xml* file illustrated above.
```py
from classy_xml import ClassyXml, XmlElement

# Create an empty ClassyXml object
obj = ClassyXml()

# Creating Country 1 Element
# Setting the text and attributes using the XmlElement arguments
obj.country = XmlElement(attributes={'name': 'Liechtenstein'})
obj.country[0].rank = XmlElement(text=1)
obj.country[0].year = XmlElement(text=2008)
obj.country[0].gdppc = XmlElement(text=141100)
obj.country[0].neighbor = XmlElement(
    attributes={'name': 'Austria', 'direction': 'E'})
obj.country[0].neighbor = XmlElement(
    attributes={'name': 'Switzerland', 'direction': 'W'})

# Creating Country 2 Element
# Setting the text and attributes directly
obj.country = XmlElement()
obj.country[1].name = 'Singapore'
obj.country[1].rank = XmlElement()
obj.country[1].rank.text = 4
obj.country[1].year = XmlElement()
obj.country[1].year.text = 2011
obj.country[1].gdppc = XmlElement()
obj.country[1].gdppc.text = 59900
obj.country[1].neighbor = XmlElement()
obj.country[1].neighbor[0].name = 'Malaysia'
obj.country[1].neighbor[0].direction = 'N'

# Save the XML file
obj.save_as('countries.xml')
```

### Modifying an existing XML file

This will add a USA element to the *countries.xml* file illustrated above.

```py
from classy_xml import ClassyXml, XmlElement

# Load the countries.xml file
obj = ClassyXml('countries.xml')

# Add a USA country element
obj.country = XmlElement(attributes={'name': 'USA'})
obj.country[-1].rank = XmlElement(text=2)
obj.country[-1].year = XmlElement(text=2012)
obj.country[-1].gdppc = XmlElement(text=12345)
obj.country[-1].neighbor = XmlElement(
    attributes={'name': 'Canada', 'direction': 'N'})
obj.country[-1].neighbor = XmlElement(
    attributes={'name': 'Mexico', 'direction': 'S'})

# Save the XML file
obj.save()
```