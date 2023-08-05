# Metadeco

Metadata reflections for functions/methods. Inspired by NPM's [`reflect-metadata`](https://www.npmjs.com/package/reflect-metadata) package.

## How to use:

### To decorate a function:

```py
import metadeco

# Define a function with the "__has_print__" metadata set to "True"
# You can set anything has the value of the metadata.
@metadeco.metadata("__has_print__", True)
def my_function():
    print("Hello world!")

metadeco.has_metadata(my_function)
# We would get "True"

metadeco.get_metadata(my_function, "__has_print__")
# We obtain the value set by the function, in here, "True
metadeco.get_metadata(my_function, "__not_set__")
# "NoMetadataError" is raised here.

metadeco.delete_metadata(my_function, "__has_print__")
# Delete the metadata.
```

## To decorate a property:

```py
import metadeco


class MySettings:
    
    @metadeco.decorate("__output__", "Hey there!")
    def test():
        return "Hey there!"

# Getting the metadata of "test" property in object MySettings
metadeco.get_metadata(MySettings, "__output__", "test")
# We get "Hey there"
```
