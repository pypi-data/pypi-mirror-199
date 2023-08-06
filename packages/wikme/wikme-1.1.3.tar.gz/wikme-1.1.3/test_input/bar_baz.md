# Bar Baz

Hey, look at this code.

    :::python
    print("Hello world")

...or this code:

    #!python
    def get_last_edited(path: str) -> str:
        try:
            # Attempt to get the last Git commit date of the file
            last_edited = subprocess.check_output(
                ["git", "log", "-1", "--format=%cd", "--date=local", path])
            return last_edited.decode("utf-8").strip()
        except Exception:
            # Fallback to the file's modified timestamp
            return str(datetime.datetime.fromtimestamp(os.path.getmtime(path)))

...or this code!

```python
import os
os.Exit(42)
```
