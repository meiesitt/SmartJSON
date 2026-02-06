# 💡 SmartJSON
Simplify JSON access in Python with a lightning fast wrapper.

# ⚙ Main Functions
- ⚡ Lightning fast initialization
- 🎨 Readiness for ColorPlus (separate dependency, source has been lost for now)
- 💪 Stable and fatal-error resistant
- 📊 Error logging (if enabled)
- 💿 Foolproof read/write
- 🔣 Built-in serialization/deserialization
- 🔒 Anti race-condition implementations
- ✅ Stress-tested (can handle thousands of large writes without breaking a sweat)
- 📄 Hooking/unhooking onto files
- ✨ Easy implementation (OOP programmed!)
- 🖥 Windows-Linux cross-platform support!
- ℹ Majority of functions has an informative docstring

# ❓ How to use
It is extremely easy to use SmartJSON in your projects.

1. Download this library and put the SmartJSON.py file into your project folder.
2. Import it in your project like this:
```py
import SmartJSON
```
3. Initialize SmartJSON and reference it for usage
Example usage:
```py
# Importing SmartJSON
import SmartJSON
import asyncio

# Initialize a SmartJSON client
JSON = SmartJSON.SmartJSON()

# Hook onto a file and enabling function to make file if it doesn't exist
# This specific function returns a status bool.
async def main():
  OK = await JSON.HookOntoFile(AbsolutePath="...absolute path to a file...", LogError=True, CreateIfNotExists=True)
  
  # If hook was successful, load file into Data variable and print
  if OK:
  
    # Loading it in Deserialized format. For types remember to always use SmartJSON's internal enums!
    OK, Data = await JSON.LoadEntireFile(ReturnType=JSON.Enum.DataType.Deserialized, LogError=True)
  
    # Printing it
    print(Data)

# Making sure this only runs when directly ran not as module
if __name__ == "__main__":
  asyncio.run(main())
```

# ⚠ What to be aware of
- SmartJSON may not work well in environments where writes are heavily permission-restricted. To avoid problems, make sure that all scripts that run SmartJSON are run by a user that has write perms in said folder. Attempts to make SmartJSON write into write-protected directories may cause unexpected crashes since not all edge cases are handled in v1.0. There are plans for fixing this.
- SmartJSON seems to work well in small-to-medium-volume, however mass volume (e.g: 5,000 requests per second) ~~has not been tested. Operation queue system is planned.~~ As of v1.1, requests are queued. SmartJSON handles mass volume writing extremely well without any corruption.
- Cross-platform has been tested, appears to work well. MacOS hasn't been tested, so your mileage varies on how Python works on MacOS.
