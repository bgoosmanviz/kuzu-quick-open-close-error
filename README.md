```
uv run main.py
```

This will print 139
```
echo $?
```

If we comment out conn.close() and db.close(), then `echo $?` will print `0`.