# King code

#### Software that makes life easier.

- utils:

  - pid (creating a controlled number of program instances)

```Python
# example: one instance
from kcode.utils.pid import Pid

Pid("app_name").create_pid_file() # -> success create pid
Pid("app_name").create_pid_file() # -> error crete pid

# example: two instances
from kcode.utils.pid import Pid

Pid("app_name", quantity=2).create_pid_file() # -> success create pid
Pid("app_name", quantity=2).create_pid_file() # -> success create pid
Pid("app_name", quantity=2).create_pid_file() # -> error crete pid
```
