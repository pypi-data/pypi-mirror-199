# gen_log_parser
- This library contains a pyCLass that can be enstantiated to create log objects "log_parser()"
- From the object various method can be used parse thru logs depending on the log format of the file
- v0.0.2 can be used to parse thru the following log formats:
  - json formated logs
  - custom formated nginx log

## NOTE:
- The nginx parser works with the following nginx log format:
  - log_format new_default $remote_addr - $remote_user - $time_local - $request - $status - $body_bytes_sent - $http_referer - $http_user_agent - $http_x_forwarded_for;
- If the log format on the nginx server is modified, then the method from the object will not work
- The class must be inherited and the nginx method must be modified to statisfy the log format


