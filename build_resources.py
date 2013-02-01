import win32rcparser

if __name__ == "__main__":
    rc_file = "resources/example.rc"
    win32rcparser.GenerateFrozenResource(rc_file, "_resources.py")
