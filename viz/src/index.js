var prettydiff = require("prettydiff"),
    args       = {
        source: "asdf",
        diff  : "asdd",
        lang  : "text"
    },
    output     = prettydiff.api(args);
