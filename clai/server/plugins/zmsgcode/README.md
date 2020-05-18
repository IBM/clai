# zmsgcode

`Retrieval` &nbsp; `Support`

IBM Z error messages can seem daunting to an end user.  The `zmsgcode` skill
tries to make them a little friendlier by automatically displaying a descriptive
help message whenever the console detects any IBM Z style message codes.

## Implementation
`zmsgcode` actively monitors the console's standard error stream.  Whenever new
data arrives, a regex match is performed on it to identify the style of error
message IDs used by IBM Z operating systems and software.  When it detects
one, the following occurs:

1. If the stream includes a hexadecimal reason code, `zmsgcode` will call the
`bpxmtext` application to try to get a message description.
2. If there is no reason code, or if `bpxmtext` doesn't return a message,
`zmsgcode` will try to search the USS publications on the z/OS KnowledgeCenter
website, returning the first result encountered.

## Example Usage

![zmsgcode](zmsgcode.gif?raw=1)

The skill will respond on `stderr` if it finds a reasonable solution.